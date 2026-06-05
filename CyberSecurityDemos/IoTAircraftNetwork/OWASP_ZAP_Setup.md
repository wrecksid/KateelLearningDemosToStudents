# OWASP ZAP in Browser - Cyber Security Demo

## Learning Objectives
- Run OWASP ZAP entirely in a browser
- Set up a vulnerable target application
- Practice web application security testing

## Solution 1: Play with Docker (Recommended)

### Step 1: Access PWD
Go to https://labs.play-with-docker.com/ and sign in with Docker Hub

### Step 2: Start Sandbox
Click "Start" to initialize a 4-hour session

### Step 3: Run OWASP ZAP
```bash
docker run -u zap -p 8080:8080 -p 8090:8090 -i ghcr.io/zaproxy/zaproxy:stable zap-webswing.sh
```

### Step 4: Access ZAP Web UI
Click the **8080** button that appears automatically

## Solution 2: Google Cloud Shell

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
```bash
docker run -d -p 3000:3000 bkimminich/juice-shop
```
Access at: http://localhost:3000

### OWASP WebGoat
```bash
docker run -d -p 8080:8080 -i webgoat/webgoat-8.0
```
Access at: http://localhost:8080/WebGoat

## Session Limits

| Environment | Duration | Data Persistence |
|-------------|----------|------------------|
| Play with Docker | 4 hours | Lost on session end |
| Google Cloud Shell | 20 hours idle | Brief pauses OK |

## Best Practices
1. Export ZAP reports before session ends
2. Use localhost targets only
3. Never scan live public websites
4. Document findings in the AIDecisionTracker demo