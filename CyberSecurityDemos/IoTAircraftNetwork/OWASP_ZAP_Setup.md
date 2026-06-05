# OWASP ZAP in Browser - Cyber Security Demo

## Learning Objectives
- Run OWASP ZAP entirely in a browser
- Set up a vulnerable target application
- Practice web application security testing

## Prerequisites
- Docker Hub account (free)
- Modern web browser with tabs
- 4-6 hours of session time

## Solution 1: Play with Docker (Recommended)

### Step 1: Access PWD
Go to https://labs.play-with-docker.com/ and sign in with Docker Hub

### Step 2: Start Sandbox
Click "Start" to initialize a 4-hour session

### Step 3: Run OWASP ZAP
```bash
docker run -u zap -p 8080:8080 -p 8090:8090 -i ghcr.io/zaproxy/zaproxy:stable zap-webswing.sh
```

### Step 4: Verify ZAP is Running
1. Wait 30-60 seconds for container to start
2. A blue button labeled **"8080"** will appear at the top of the PWD screen
3. Click the **8080** button - a new tab opens showing ZAP's Webswing GUI
4. **Verification:** You should see the OWASP ZAP interface with "Tools" menu

### Step 5: Run Quick Test
1. In ZAP, go to **Tools** → **Automated Scan**
2. Enter target: `http://host.docker.internal:3000` (or use Juice Shop below)
3. Click **Attack** - scan should complete in 1-2 minutes
4. **Verification:** Results show vulnerabilities found

## Solution 2: Google Cloud Shell (Alternative)

### Step 1: Access Cloud Shell
Go to https://shell.cloud.google.com

### Step 2: Run ZAP
```bash
docker run -u zap -p 8080:8080 -p 8090:8090 -i ghcr.io/zaproxy/zaproxy:stable zap-webswing.sh
```

### Step 3: Preview
Click **Web Preview** → **Change Port** → enter `8080`

## Safe Target Applications

### OWASP Juice Shop (Recommended)
**Terminal 1:**
```bash
docker run -d -p 3000:3000 bkimminich/juice-shop
```
**Verification:** Visit `http://localhost:3000` - see Juice Shop login page

**Terminal 2 (in same PWD instance):**
```bash
docker run -u zap -p 8080:8080 -p 8090:8090 -i ghcr.io/zaproxy/zaproxy:stable zap-webswing.sh
```

### OWASP WebGoat
```bash
docker run -d -p 8080:8080 webgoat/webgoat-8.0
```
Access at: http://localhost:8080/WebGoat

## Testing Checklist

### Before Starting
- [ ] Docker Hub account created
- [ ] PWD session started (or Cloud Shell ready)
- [ ] Juice Shop container running (if using local target)

### During Test
- [ ] ZAP Web UI loads in new tab
- [ ] Can navigate ZAP menus
- [ ] Automated scan completes
- [ ] Vulnerability results appear

### Common Issues & Fixes

**Issue:** "8080" button doesn't appear
- Wait 60+ seconds for container initialization
- Refresh PWD page if needed

**Issue:** ZAP UI won't load
- Check browser pop-up blocker
- Try incognito/private browsing mode

**Issue:** "Connection refused" scanning localhost
- Use `host.docker.internal` instead of `localhost` in PWD
- In Cloud Shell, use external IP of target

**Issue:** Scan returns "No alerts"
- Verify target URL is correct
- Check Juice Shop is actually running (`docker ps`)

## Session Limits

| Environment | Duration | Data Persistence |
|-------------|----------|------------------|
| Play with Docker | 4 hours | Lost on session end |
| Google Cloud Shell | 20 hours idle | Brief pauses OK |

## Best Practices
1. Export ZAP reports before session ends (**File** → **Export** → **XML**)
2. Use localhost targets only (never scan live public sites)
3. Document findings in the AIDecisionTracker demo
4. Run scans during low-traffic hours to minimize resource usage

## Alternative Targets (if Juice Shop unavailable)
- **DVWA:** `docker run -d -p 8080:8080 vulnerables/web-dvwa`
- **bWAPP:** `docker run -d -p 8080:8080 raulreyn/bwapp`
- **DVNA:** `docker run -d -p 8080:8080 aquasec/dvnv`