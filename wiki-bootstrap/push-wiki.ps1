# push-wiki.ps1
# Bootstraps the GitHub Wiki for KateelLearningDemosToStudents.
#
# Prerequisites:
#   1. Go to https://github.com/VinayaSharada/KateelLearningDemosToStudents/settings
#      scroll to Features → check "Wikis" → Save
#   2. Visit https://github.com/VinayaSharada/KateelLearningDemosToStudents/wiki
#      and click "Create the first page" → type anything → Save Page
#      (This initialises the wiki git repo.)
#   3. Run this script from the repo root:
#      powershell -ExecutionPolicy Bypass -File wiki-bootstrap\push-wiki.ps1

$ErrorActionPreference = 'Stop'

$WIKI_URL   = 'https://github.com/VinayaSharada/KateelLearningDemosToStudents.wiki.git'
$PAGES_DIR  = Join-Path $PSScriptRoot '.'    # the wiki-bootstrap/ directory
$CLONE_DIR  = Join-Path $env:TEMP 'kateel-wiki-bootstrap'
$AUTHOR     = 'Vinaya Sathyanarayana'
$EMAIL      = 'vinallcontact@gmail.com'

Write-Host ""
Write-Host "=== KateelLearningDemosToStudents — Wiki Bootstrap ===" -ForegroundColor Cyan
Write-Host ""

# Clean up any previous clone
if (Test-Path $CLONE_DIR) {
    Remove-Item $CLONE_DIR -Recurse -Force
}

Write-Host "Cloning wiki repo..." -ForegroundColor Yellow
git clone $WIKI_URL $CLONE_DIR
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Could not clone the wiki repository." -ForegroundColor Red
    Write-Host "Make sure you have:" -ForegroundColor Red
    Write-Host "  1. Enabled Wikis in the repo Settings → Features" -ForegroundColor Red
    Write-Host "  2. Created the first page manually at:" -ForegroundColor Red
    Write-Host "     https://github.com/VinayaSharada/KateelLearningDemosToStudents/wiki" -ForegroundColor Red
    exit 1
}

Write-Host "Copying wiki pages..." -ForegroundColor Yellow

# Copy all .md files except this script
Get-ChildItem $PAGES_DIR -Filter '*.md' | ForEach-Object {
    Copy-Item $_.FullName (Join-Path $CLONE_DIR $_.Name) -Force
    Write-Host "  + $($_.Name)"
}

Set-Location $CLONE_DIR

git config user.name  $AUTHOR
git config user.email $EMAIL
git add -A
git commit -m "Bootstrap wiki: Home, Usage-Registry, Attribution-Requirements pages

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

Write-Host "Pushing to GitHub Wiki..." -ForegroundColor Yellow
git push origin master 2>&1
if ($LASTEXITCODE -ne 0) {
    # Some wikis use 'main' instead of 'master'
    git push origin main 2>&1
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Wiki bootstrapped successfully!" -ForegroundColor Green
    Write-Host "View it at: https://github.com/VinayaSharada/KateelLearningDemosToStudents/wiki" -ForegroundColor Cyan
} else {
    Write-Host "Push failed — check your git credentials and try again." -ForegroundColor Red
}

Set-Location $PSScriptRoot
