"""
intrusion_detection.py
======================
Cybersecurity Intrusion Detection Demo — Main Analysis Script

This script parses three real-world log formats (Apache web server,
Linux SSH auth, and iptables firewall), runs seven detection algorithms,
prints a colour-coded threat report to the console, and saves a
matplotlib dashboard image.

Usage
-----
    python intrusion_detection.py                  # analyse all three logs
    python intrusion_detection.py --log data/apache_access.log
    python intrusion_detection.py --log data/ssh_auth.log
    python intrusion_detection.py --log data/firewall.log

Exit codes
----------
    0 — no findings, or only MEDIUM / HIGH severity findings
    1 — at least one CRITICAL severity finding

Dependencies (see requirements.txt)
------------------------------------
    pandas>=2.1.0, numpy>=1.26.0, matplotlib>=3.8.0
"""

import argparse
import os
import re
import sys
from datetime import datetime

import matplotlib
matplotlib.use("Agg")           # non-interactive backend (no display needed)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Directory layout
# ---------------------------------------------------------------------------
BASE_DIR     = os.path.dirname(__file__)
DATA_DIR     = os.path.join(BASE_DIR, "data")
REPORTS_DIR  = os.path.join(BASE_DIR, "reports")

APACHE_LOG   = os.path.join(DATA_DIR, "apache_access.log")
SSH_LOG      = os.path.join(DATA_DIR, "ssh_auth.log")
FW_LOG       = os.path.join(DATA_DIR, "firewall.log")
DASHBOARD_PNG = os.path.join(REPORTS_DIR, "intrusion_dashboard.png")

# ---------------------------------------------------------------------------
# ANSI colour codes for terminal output
# ---------------------------------------------------------------------------
RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[91m"
ORANGE = "\033[33m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
GREY   = "\033[90m"


# ===========================================================================
# SECTION 1 — LOG PARSERS
# ===========================================================================

def parse_apache_log(path: str) -> pd.DataFrame:
    """
    Parse an Apache Combined Log Format file into a DataFrame.

    Apache Combined Log Format:
        %h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"

    Returns columns:
        ip, ident, user, timestamp (datetime), method, uri, protocol,
        status (int), bytes (int), referer, user_agent
    """
    # Regex for the Combined Log Format.
    # The tricky parts are:
    #   - timestamp field is wrapped in [ ... ]
    #   - request line is in double-quotes and may contain spaces
    #   - referer and user-agent are in double-quotes at the end
    pattern = re.compile(
        r'(?P<ip>\S+) '               # %h  client IP
        r'(?P<ident>\S+) '            # %l  ident (usually -)
        r'(?P<user>\S+) '             # %u  auth user (usually -)
        r'\[(?P<timestamp>[^\]]+)\] ' # %t  [day/Mon/year:HH:MM:SS +zone]
        r'"(?P<request>[^"]*)" '      # %r  "METHOD /path HTTP/ver"
        r'(?P<status>\d{3}) '         # %>s HTTP status code
        r'(?P<bytes>\S+) '            # %b  bytes ("-" if zero)
        r'"(?P<referer>[^"]*)" '      # Referer header
        r'"(?P<ua>[^"]*)"'            # User-Agent header
    )

    records = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, raw in enumerate(fh, 1):
            raw = raw.rstrip("\n")
            if not raw:
                continue
            m = pattern.match(raw)
            if not m:
                # Skip lines that do not match (e.g., blank or malformed)
                continue

            # Parse the request line: "METHOD /path HTTP/1.1"
            req_parts = m.group("request").split()
            method   = req_parts[0] if len(req_parts) > 0 else "-"
            uri      = req_parts[1] if len(req_parts) > 1 else "-"
            protocol = req_parts[2] if len(req_parts) > 2 else "-"

            # Parse timestamp: "19/May/2026:08:03:12 +0000"
            try:
                ts = datetime.strptime(m.group("timestamp"), "%d/%b/%Y:%H:%M:%S %z")
                # Convert to tz-naive UTC for simplicity in calculations
                ts = ts.replace(tzinfo=None)
            except ValueError:
                ts = pd.NaT

            # bytes field is "-" when there's no body (e.g., 304 Not Modified)
            byte_val = m.group("bytes")
            byte_int = int(byte_val) if byte_val.isdigit() else 0

            records.append({
                "ip":         m.group("ip"),
                "ident":      m.group("ident"),
                "user":       m.group("user"),
                "timestamp":  ts,
                "method":     method,
                "uri":        uri,
                "protocol":   protocol,
                "status":     int(m.group("status")),
                "bytes":      byte_int,
                "referer":    m.group("referer"),
                "user_agent": m.group("ua"),
            })

    df = pd.DataFrame(records)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def parse_ssh_log(path: str) -> pd.DataFrame:
    """
    Parse a Linux syslog SSH auth file into a DataFrame.

    Syslog format:
        Month DD HH:MM:SS hostname service[pid]: message

    Returns columns:
        timestamp (datetime), hostname, service, pid (int),
        event_type (str: Accepted | Failed | Other),
        user, source_ip, port (int), auth_method
    """
    # Month abbreviation -> number mapping (for manual year injection)
    MONTH_MAP = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
        "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
        "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
    }
    ASSUMED_YEAR = 2026   # syslog does not include a year

    # General syslog header pattern
    header_re = re.compile(
        r'(?P<month>[A-Z][a-z]{2})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+'
        r'(?P<host>\S+)\s+(?P<service>\S+?)\[(?P<pid>\d+)\]:\s+(?P<msg>.*)'
    )

    # Sub-patterns for specific event types
    accepted_re = re.compile(
        r'Accepted (?P<auth>\S+) for (?P<user>\S+) from (?P<ip>\S+) port (?P<port>\d+)'
    )
    failed_re = re.compile(
        r'Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\S+) port (?P<port>\d+)'
    )

    records = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            raw = raw.rstrip("\n")
            if not raw:
                continue
            h = header_re.match(raw)
            if not h:
                continue

            # Build datetime from syslog fields (inject assumed year)
            month_num = MONTH_MAP.get(h.group("month"), 1)
            day = int(h.group("day"))
            h_m_s = h.group("time").split(":")
            try:
                ts = datetime(ASSUMED_YEAR, month_num, day,
                              int(h_m_s[0]), int(h_m_s[1]), int(h_m_s[2]))
            except ValueError:
                ts = pd.NaT

            msg = h.group("msg")

            # Classify event type and extract fields
            event_type  = "Other"
            user        = ""
            source_ip   = ""
            port        = 0
            auth_method = ""

            am = accepted_re.search(msg)
            if am:
                event_type  = "Accepted"
                auth_method = am.group("auth")
                user        = am.group("user")
                source_ip   = am.group("ip")
                port        = int(am.group("port"))
            else:
                fm = failed_re.search(msg)
                if fm:
                    event_type = "Failed"
                    user       = fm.group("user")
                    source_ip  = fm.group("ip")
                    port       = int(fm.group("port"))

            records.append({
                "timestamp":   ts,
                "hostname":    h.group("host"),
                "service":     h.group("service").split("[")[0],
                "pid":         int(h.group("pid")),
                "event_type":  event_type,
                "user":        user,
                "source_ip":   source_ip,
                "port":        port,
                "auth_method": auth_method,
                "raw_message": msg,
            })

    df = pd.DataFrame(records)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def parse_firewall_log(path: str) -> pd.DataFrame:
    """
    Parse an iptables/netfilter kernel log file into a DataFrame.

    Format (one line per dropped packet):
        Month DD HH:MM:SS hostname kernel: [uptime] PREFIX IN=iface ...
        SRC=x.x.x.x DST=x.x.x.x ... PROTO=TCP|UDP SPT=n DPT=n ...

    Returns columns:
        timestamp (datetime), action, src_ip, dst_ip,
        proto, src_port (int), dst_port (int), flags
    """
    MONTH_MAP = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
        "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
        "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
    }
    ASSUMED_YEAR = 2026

    # Syslog header + kernel timestamp
    header_re = re.compile(
        r'(?P<month>[A-Z][a-z]{2})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+'
        r'\S+\s+kernel:\s+\[[\d.]+\]\s+(?P<rest>.*)'
    )

    def extract(text, key):
        """Extract a key=value from the iptables log line body."""
        m = re.search(rf'{key}=(\S+)', text)
        return m.group(1) if m else ""

    records = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            raw = raw.rstrip("\n")
            if not raw:
                continue
            h = header_re.match(raw)
            if not h:
                continue

            month_num = MONTH_MAP.get(h.group("month"), 1)
            day = int(h.group("day"))
            h_m_s = h.group("time").split(":")
            try:
                ts = datetime(ASSUMED_YEAR, month_num, day,
                              int(h_m_s[0]), int(h_m_s[1]), int(h_m_s[2]))
            except ValueError:
                ts = pd.NaT

            rest = h.group("rest")
            # The action label is the first token before IN=
            action_m = re.match(r'(\S+)', rest)
            action = action_m.group(1) if action_m else "UNKNOWN"

            src_ip   = extract(rest, "SRC")
            dst_ip   = extract(rest, "DST")
            proto    = extract(rest, "PROTO")
            src_port_str = extract(rest, "SPT")
            dst_port_str = extract(rest, "DPT")

            # Flags: SYN, ACK, RST, FIN etc.
            flag_tokens = [t for t in ["SYN", "ACK", "RST", "FIN", "URG"] if t in rest]
            flags = ",".join(flag_tokens) if flag_tokens else ""

            records.append({
                "timestamp": ts,
                "action":    action,
                "src_ip":    src_ip,
                "dst_ip":    dst_ip,
                "proto":     proto,
                "src_port":  int(src_port_str) if src_port_str.isdigit() else 0,
                "dst_port":  int(dst_port_str) if dst_port_str.isdigit() else 0,
                "flags":     flags,
            })

    df = pd.DataFrame(records)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


# ===========================================================================
# SECTION 2 — DETECTION FUNCTIONS
# ===========================================================================
# Each function returns a dict with keys:
#   threat    (str)  — human-readable name
#   severity  (str)  — CRITICAL | HIGH | MEDIUM
#   details   (str)  — explanation / context
#   ips       (list) — attacker IP(s) found
#   count     (int)  — number of matching events
#   evidence  (list) — up to 3 example log lines / values for the report

def detect_ssh_brute_force(ssh_df: pd.DataFrame,
                            threshold: int = 10,
                            window_minutes: int = 10) -> dict:
    """
    Sliding-window brute force detection.

    Algorithm:
        1. Filter to Failed-password events only.
        2. For each unique source IP, sort attempts by timestamp.
        3. Use a two-pointer approach: for every attempt i, count how many
           subsequent attempts j fall within [ts_i, ts_i + window_minutes].
           If count >= threshold, flag this IP.

    threshold      — minimum failed attempts within the window to trigger
    window_minutes — width of the rolling time window
    """
    result = {"threat": "SSH Brute Force", "severity": "CRITICAL",
              "details": "", "ips": [], "count": 0, "evidence": []}

    if ssh_df.empty:
        result["details"] = "No SSH data."
        return result

    failed = ssh_df[ssh_df["event_type"] == "Failed"].copy()
    if failed.empty:
        result["details"] = "No failed SSH attempts found."
        return result

    window = pd.Timedelta(minutes=window_minutes)
    flagged = {}

    for ip, grp in failed.groupby("source_ip"):
        attempts = grp.sort_values("timestamp")["timestamp"].reset_index(drop=True)
        n = len(attempts)
        # Sliding window: for each left pointer i, advance right pointer j
        # to find all attempts within [ts_i, ts_i + window].
        # j must always be >= i+1 on each iteration of i, so we use a fresh j per i.
        max_window_count = 0
        j = 0
        for i in range(n):
            # Ensure j is at least at i+1 (the window includes attempt i itself)
            if j <= i:
                j = i + 1
            # Expand the window to the right
            while j < n and attempts[j] - attempts[i] <= window:
                j += 1
            count_in_window = j - i   # includes attempt[i] itself
            if count_in_window > max_window_count:
                max_window_count = count_in_window
            if count_in_window >= threshold:
                break   # we've already found a qualifying window; no need to continue

        if max_window_count >= threshold:
            flagged[ip] = max_window_count

    if flagged:
        result["ips"]  = sorted(flagged.keys())
        result["count"] = sum(flagged.values())
        result["details"] = (
            f"Detected {len(flagged)} IP(s) with >= {threshold} failed SSH "
            f"login attempts within any {window_minutes}-minute window. "
            f"Counts: {flagged}"
        )
        for ip in result["ips"][:2]:
            sample = failed[failed["source_ip"] == ip].head(2)
            for _, row in sample.iterrows():
                result["evidence"].append(
                    f"{row['timestamp']}  Failed password for {row['user']} from {ip} port {row['port']}"
                )
    else:
        result["severity"] = "MEDIUM"
        result["details"]  = f"No brute force pattern detected (threshold={threshold}/{window_minutes}min)."

    return result


def detect_sqli(web_df: pd.DataFrame) -> dict:
    """
    SQL Injection detection via URI pattern matching.

    Looks for common SQLi payloads in the URI:
      - UNION SELECT constructs
      - Boolean-based: OR 1=1, AND 1=1
      - Destructive: DROP TABLE, INSERT INTO
      - Execution: exec, xp_cmdshell, xp_
      - Comment sequences used to truncate queries: --, #, /*
    """
    result = {"threat": "SQL Injection", "severity": "HIGH",
              "details": "", "ips": [], "count": 0, "evidence": []}

    if web_df.empty:
        result["details"] = "No web log data."
        return result

    # Case-insensitive regex for known SQLi indicators
    sqli_re = re.compile(
        r'union\s+select|'               # UNION SELECT
        r'or\s+1\s*=\s*1|'              # OR 1=1
        r'and\s+1\s*=\s*[12]|'          # AND 1=1 / AND 1=2
        r'drop\s+table|'                # DROP TABLE
        r'insert\s+into|'               # INSERT INTO
        r'select\s+\*\s+from|'          # SELECT * FROM
        r'exec\s*\(|'                   # exec(
        r'xp_|'                         # xp_cmdshell etc.
        r'sleep\s*\(|'                  # SLEEP()
        r'extractvalue\s*\(|'           # EXTRACTVALUE() — MySQL error-based
        r'information_schema|'          # info schema enumeration
        r'%20union%20|%20select%20|'    # URL-encoded UNION SELECT
        r'%27\s*or\s*%271|'             # URL-encoded ' OR '1
        r"'--|\s*--\s|%23|/\*",        # comment truncation
        re.IGNORECASE,
    )

    # Apply the regex to the 'uri' column
    hits = web_df[web_df["uri"].str.contains(sqli_re, regex=True, na=False)]

    if not hits.empty:
        result["ips"]   = sorted(hits["ip"].unique().tolist())
        result["count"] = len(hits)
        result["details"] = (
            f"Found {len(hits)} requests containing SQL injection patterns "
            f"from {len(result['ips'])} unique IP(s)."
        )
        for _, row in hits.head(3).iterrows():
            result["evidence"].append(f"{row['ip']}  {row['uri'][:120]}")
    else:
        result["severity"] = "MEDIUM"
        result["details"]  = "No SQL injection patterns detected in web URIs."

    return result


def detect_path_traversal(web_df: pd.DataFrame) -> dict:
    """
    Path traversal detection.

    Matches:
      - ../  (Unix) and ..\\ (Windows)
      - %2e%2e (URL-encoded ..)
      - ....// (double-dot obfuscation)
      - Mixed encoding variants: ..%2f, %2e%2e%2f, ..%5c
    """
    result = {"threat": "Path Traversal", "severity": "HIGH",
              "details": "", "ips": [], "count": 0, "evidence": []}

    if web_df.empty:
        result["details"] = "No web log data."
        return result

    traversal_re = re.compile(
        r'\.\./|'           # ../
        r'\.\.\\|'          # ..\
        r'%2e%2e|'          # URL-encoded ..
        r'\.\.%2f|'         # ..%2f
        r'%2e%2e%2f|'       # %2e%2e%2f
        r'%2e%2e%5c|'       # %2e%2e%5c (Windows)
        r'\.\.\./|'         # obfuscated ..../
        r'\.\.%5c',         # ..%5c (Windows backslash)
        re.IGNORECASE,
    )

    hits = web_df[web_df["uri"].str.contains(traversal_re, regex=True, na=False)]

    if not hits.empty:
        result["ips"]   = sorted(hits["ip"].unique().tolist())
        result["count"] = len(hits)
        result["details"] = (
            f"Found {len(hits)} requests with path traversal sequences "
            f"from {len(result['ips'])} IP(s)."
        )
        for _, row in hits.head(3).iterrows():
            result["evidence"].append(f"{row['ip']}  {row['uri'][:120]}")
    else:
        result["severity"] = "MEDIUM"
        result["details"]  = "No path traversal patterns detected."

    return result


def detect_xss(web_df: pd.DataFrame) -> dict:
    """
    Cross-Site Scripting (XSS) probe detection.

    Matches:
      - <script  (opening script tag)
      - javascript: (protocol handler injection)
      - onerror= (event handler injection)
      - onload=  (event handler injection)
      - alert(   (classic XSS test payload)
      - URL-encoded variants (%3c = <, %3e = >)
    """
    result = {"threat": "XSS Probe", "severity": "MEDIUM",
              "details": "", "ips": [], "count": 0, "evidence": []}

    if web_df.empty:
        result["details"] = "No web log data."
        return result

    xss_re = re.compile(
        r'<script|'         # <script tag
        r'javascript:|'     # protocol injection
        r'onerror=|'        # event handlers
        r'onload=|'
        r'onmouseover=|'
        r'alert\s*\(|'      # alert() — common PoC payload
        r'%3cscript|'       # URL-encoded <script
        r'%3c/script|'      # URL-encoded </script>
        r'<svg|'            # SVG-based XSS
        r'<img\s+src',      # <img onerror
        re.IGNORECASE,
    )

    hits = web_df[web_df["uri"].str.contains(xss_re, regex=True, na=False)]

    if not hits.empty:
        result["ips"]   = sorted(hits["ip"].unique().tolist())
        result["count"] = len(hits)
        result["details"] = (
            f"Found {len(hits)} requests containing XSS probe patterns "
            f"from {len(result['ips'])} IP(s)."
        )
        for _, row in hits.head(3).iterrows():
            result["evidence"].append(f"{row['ip']}  {row['uri'][:120]}")
    else:
        result["details"] = "No XSS probe patterns detected."

    return result


def detect_bad_agents(web_df: pd.DataFrame) -> dict:
    """
    Known-bad User-Agent detection.

    Flags requests from well-known security scanners and attack tools:
      sqlmap, nikto, nessus, masscan, nmap, zgrab, dirbuster, gobuster,
      nuclei, havij, acunetix, metasploit, w3af, burpsuite

    These tools often use distinctive UA strings that are easy to detect.
    Real attackers sometimes disguise them, but automated scripts usually do not.
    """
    result = {"threat": "Malicious Scanner / Tool UA", "severity": "HIGH",
              "details": "", "ips": [], "count": 0, "evidence": []}

    if web_df.empty:
        result["details"] = "No web log data."
        return result

    bad_ua_re = re.compile(
        r'sqlmap|nikto|nessus|masscan|nmap|zgrab|'
        r'dirbuster|gobuster|nuclei|havij|acunetix|'
        r'metasploit|w3af|burpsuite|openvas|'
        r'python-requests/[012]\.|'   # headless script (common for bots)
        r'Go-http-client',            # Go http client (used by flood tools)
        re.IGNORECASE,
    )

    hits = web_df[web_df["user_agent"].str.contains(bad_ua_re, regex=True, na=False)]

    if not hits.empty:
        result["ips"]   = sorted(hits["ip"].unique().tolist())
        result["count"] = len(hits)
        result["details"] = (
            f"Found {len(hits)} requests from known scanner/attack tool User-Agents "
            f"originating from {len(result['ips'])} IP(s)."
        )
        for _, row in hits.head(3).iterrows():
            result["evidence"].append(
                f"{row['ip']}  UA={row['user_agent'][:80]}"
            )
    else:
        result["severity"] = "MEDIUM"
        result["details"]  = "No known scanner User-Agents detected."

    return result


def detect_rate_anomaly(web_df: pd.DataFrame, rpm_threshold: int = 20) -> dict:
    """
    HTTP request-rate anomaly detection (volumetric / flood detection).

    Algorithm:
        1. Floor each request's timestamp to the minute.
        2. Count requests per (IP, minute) bucket.
        3. Flag any IP that exceeds rpm_threshold requests in a single minute.

    rpm_threshold — requests-per-minute that triggers the alert
    """
    result = {"threat": "HTTP Flood / Rate Anomaly", "severity": "HIGH",
              "details": "", "ips": [], "count": 0, "evidence": []}

    if web_df.empty:
        result["details"] = "No web log data."
        return result

    df = web_df.copy()
    # Floor timestamp to minute granularity
    df["minute"] = df["timestamp"].dt.floor("T")

    # Count requests per IP per minute
    rpm = df.groupby(["ip", "minute"]).size().reset_index(name="req_count")
    flagged = rpm[rpm["req_count"] >= rpm_threshold]

    if not flagged.empty:
        result["ips"]   = sorted(flagged["ip"].unique().tolist())
        result["count"] = int(flagged["req_count"].sum())
        result["details"] = (
            f"Detected {len(flagged)} (IP, minute) buckets exceeding "
            f"{rpm_threshold} req/min. Peak: {int(flagged['req_count'].max())} rpm."
        )
        for _, row in flagged.head(3).iterrows():
            result["evidence"].append(
                f"{row['ip']}  {row['req_count']} requests at minute {row['minute']}"
            )
    else:
        result["severity"] = "MEDIUM"
        result["details"]  = f"No IP exceeded {rpm_threshold} req/min."

    return result


def detect_port_scan(fw_df: pd.DataFrame, port_threshold: int = 15) -> dict:
    """
    Port scan detection using firewall drop logs.

    Algorithm:
        Count the number of unique destination ports hit by each source IP.
        An IP probing more than port_threshold distinct ports is flagged as
        conducting a port scan — this is characteristic of tools like nmap,
        masscan, or zmap.

    port_threshold — minimum distinct destination ports to trigger alert
    """
    result = {"threat": "Port Scan", "severity": "HIGH",
              "details": "", "ips": [], "count": 0, "evidence": []}

    if fw_df.empty:
        result["details"] = "No firewall log data."
        return result

    # Count unique destination ports per source IP
    port_counts = (
        fw_df.groupby("src_ip")["dst_port"]
        .nunique()
        .reset_index(name="unique_ports")
    )
    flagged = port_counts[port_counts["unique_ports"] >= port_threshold]

    if not flagged.empty:
        result["ips"]   = sorted(flagged["src_ip"].tolist())
        result["count"] = int(flagged["unique_ports"].sum())
        result["details"] = (
            f"Detected {len(flagged)} IP(s) probing >= {port_threshold} unique "
            f"destination ports. Highest: "
            f"{int(flagged['unique_ports'].max())} ports from "
            f"{flagged.loc[flagged['unique_ports'].idxmax(), 'src_ip']}."
        )
        for _, row in flagged.head(3).iterrows():
            sample_ports = sorted(
                fw_df[fw_df["src_ip"] == row["src_ip"]]["dst_port"].unique()[:6].tolist()
            )
            result["evidence"].append(
                f"{row['src_ip']}  probed {row['unique_ports']} ports, e.g. {sample_ports}"
            )
    else:
        result["severity"] = "MEDIUM"
        result["details"]  = f"No port scan detected (threshold={port_threshold} unique ports)."

    return result


# ===========================================================================
# SECTION 3 — REPORT PRINTER
# ===========================================================================

SEVERITY_BADGE = {
    "CRITICAL": f"{RED}{BOLD}[CRITICAL]{RESET}",
    "HIGH":     f"{ORANGE}{BOLD}[HIGH    ]{RESET}",
    "MEDIUM":   f"{YELLOW}[MEDIUM  ]{RESET}",
}

def print_report(all_findings: list) -> None:
    """
    Print a colour-coded intrusion detection report to the console.

    Each finding block shows:
      - Severity badge
      - Threat type
      - Affected IPs
      - Event count
      - Details paragraph
      - Up to 3 evidence samples
    """
    width = 80
    divider = GREY + ("─" * width) + RESET

    print("\n" + BOLD + CYAN + "=" * width + RESET)
    print(BOLD + CYAN + "  INTRUSION DETECTION REPORT".center(width) + RESET)
    print(BOLD + CYAN + f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + RESET)
    print(BOLD + CYAN + "=" * width + RESET)

    # Summary table header
    print(f"\n{'Threat Type':<35} {'Severity':<10} {'IPs':<6} {'Events':<8}")
    print("─" * 65)
    for f in all_findings:
        sev_colour = RED if f["severity"] == "CRITICAL" else (ORANGE if f["severity"] == "HIGH" else YELLOW)
        print(f"{f['threat']:<35} {sev_colour}{f['severity']:<10}{RESET} "
              f"{len(f['ips']):<6} {f['count']:<8}")

    # Detailed findings
    for f in all_findings:
        if f["count"] == 0 and f["severity"] == "MEDIUM":
            continue  # skip negative results to reduce noise

        print("\n" + divider)
        badge = SEVERITY_BADGE.get(f["severity"], "[UNKNOWN ]")
        print(f"  {badge}  {BOLD}{f['threat']}{RESET}")
        print(f"  {GREY}Affected IPs :{RESET} {', '.join(f['ips']) if f['ips'] else 'none'}")
        print(f"  {GREY}Event count  :{RESET} {f['count']}")
        print(f"  {GREY}Details      :{RESET} {f['details']}")
        if f.get("evidence"):
            print(f"  {GREY}Evidence samples:{RESET}")
            for ev in f["evidence"][:3]:
                print(f"    {GREY}>{RESET} {ev[:110]}")

    print("\n" + divider)

    critical_count = sum(1 for f in all_findings if f["severity"] == "CRITICAL" and f["count"] > 0)
    high_count     = sum(1 for f in all_findings if f["severity"] == "HIGH"     and f["count"] > 0)

    if critical_count:
        print(f"\n  {RED}{BOLD}VERDICT: {critical_count} CRITICAL threat(s) detected! Immediate action required.{RESET}")
    elif high_count:
        print(f"\n  {ORANGE}{BOLD}VERDICT: {high_count} HIGH severity threat(s) detected. Investigate promptly.{RESET}")
    else:
        print(f"\n  {GREEN}{BOLD}VERDICT: No critical threats detected. Continue monitoring.{RESET}")

    print(BOLD + CYAN + "=" * width + RESET + "\n")


# ===========================================================================
# SECTION 4 — DASHBOARD VISUALISATION
# ===========================================================================

def plot_dashboard(web_df: pd.DataFrame,
                   ssh_df: pd.DataFrame,
                   fw_df: pd.DataFrame,
                   findings: list,
                   output_path: str) -> None:
    """
    Build and save a 2×3 matplotlib dashboard.

    Panels:
        [0,0] Requests per hour (web traffic timeline)
        [0,1] Top 10 IPs by request count (horizontal bar)
        [0,2] HTTP status code distribution (bar)
        [1,0] SSH failed login timeline (line, brute force window highlighted)
        [1,1] Firewall blocked ports (top targeted ports, bar)
        [1,2] Attack type breakdown (findings count by type, horizontal bar)
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Intrusion Detection Dashboard — May 19-21 2026",
                 fontsize=16, fontweight="bold", y=0.98)
    fig.patch.set_facecolor("#1e1e2e")
    for ax in axes.flat:
        ax.set_facecolor("#2a2a3e")
        ax.tick_params(colors="white", labelsize=8)
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")
        for spine in ax.spines.values():
            spine.set_color("#555577")

    # -- [0,0] Requests per hour (web traffic) --
    ax00 = axes[0, 0]
    if not web_df.empty and pd.api.types.is_datetime64_any_dtype(web_df["timestamp"]):
        web_df2 = web_df.copy()
        web_df2["hour"] = web_df2["timestamp"].dt.floor("H")
        hourly = web_df2.groupby("hour").size()

        # Identify anomalous hours (top 10 % of request volume)
        q90 = hourly.quantile(0.90)
        colours = ["#ff4444" if v >= q90 else "#4488ff" for v in hourly.values]
        ax00.bar(range(len(hourly)), hourly.values, color=colours, width=0.8)
        ax00.set_xticks(range(0, len(hourly), max(1, len(hourly) // 8)))
        ax00.set_xticklabels(
            [str(t.strftime("%m/%d %H")) for t in hourly.index[::max(1, len(hourly) // 8)]],
            rotation=45, ha="right", fontsize=7
        )
        normal_patch = mpatches.Patch(color="#4488ff", label="Normal")
        anomaly_patch = mpatches.Patch(color="#ff4444", label="Anomaly (top 10%)")
        ax00.legend(handles=[normal_patch, anomaly_patch], fontsize=7,
                    facecolor="#2a2a3e", labelcolor="white")
    ax00.set_title("Requests per Hour (Web)")
    ax00.set_ylabel("Request count")
    ax00.set_xlabel("Hour")

    # -- [0,1] Top 10 IPs by request count --
    ax01 = axes[0, 1]
    if not web_df.empty:
        top_ips = web_df["ip"].value_counts().head(10)
        # Colour attacker IPs red
        attack_ips = {"198.51.100.23", "203.0.113.17", "203.0.113.99",
                      "198.51.100.77", "203.0.113.55"}
        bar_colours = ["#ff4444" if ip in attack_ips else "#44bb88"
                       for ip in top_ips.index]
        bars = ax01.barh(range(len(top_ips)), top_ips.values, color=bar_colours)
        ax01.set_yticks(range(len(top_ips)))
        ax01.set_yticklabels(top_ips.index, fontsize=7)
        ax01.invert_yaxis()
        normal_p = mpatches.Patch(color="#44bb88", label="Legit")
        attack_p = mpatches.Patch(color="#ff4444", label="Attacker")
        ax01.legend(handles=[normal_p, attack_p], fontsize=7,
                    facecolor="#2a2a3e", labelcolor="white")
    ax01.set_title("Top 10 IPs by Requests")
    ax01.set_xlabel("Request count")

    # -- [0,2] HTTP status code distribution --
    ax02 = axes[0, 2]
    if not web_df.empty:
        status_counts = web_df["status"].value_counts().sort_index()
        status_colours = {200: "#44bb88", 304: "#4488ff", 301: "#aaaaff",
                          400: "#ffaa44", 403: "#ff8844", 404: "#ff6666",
                          500: "#ff2222"}
        sc = [status_colours.get(s, "#888888") for s in status_counts.index]
        ax02.bar([str(s) for s in status_counts.index], status_counts.values, color=sc)
        ax02.set_xlabel("Status code")
        ax02.set_ylabel("Count")
    ax02.set_title("HTTP Status Distribution")

    # -- [1,0] SSH failed logins timeline --
    ax10 = axes[1, 0]
    if not ssh_df.empty and pd.api.types.is_datetime64_any_dtype(ssh_df["timestamp"]):
        failed_ssh = ssh_df[ssh_df["event_type"] == "Failed"].copy()
        if not failed_ssh.empty:
            failed_ssh["minute"] = failed_ssh["timestamp"].dt.floor("T")
            failed_by_min = failed_ssh.groupby("minute").size()
            ax10.plot(range(len(failed_by_min)), failed_by_min.values,
                      color="#ff8844", linewidth=1.5, marker="o", markersize=3)
            ax10.set_xticks(range(0, len(failed_by_min), max(1, len(failed_by_min) // 8)))
            ax10.set_xticklabels(
                [str(t.strftime("%m/%d %H:%M")) for t in
                 failed_by_min.index[::max(1, len(failed_by_min) // 8)]],
                rotation=45, ha="right", fontsize=6
            )
            # Highlight brute force window (23:15–23:52 May 19)
            try:
                bf_start = pd.Timestamp("2026-05-19 23:15:00")
                bf_end   = pd.Timestamp("2026-05-19 23:52:00")
                idx_list = list(failed_by_min.index)
                idx_start = next((i for i, t in enumerate(idx_list) if t >= bf_start), None)
                idx_end   = next((i for i, t in enumerate(idx_list) if t > bf_end), len(idx_list))
                if idx_start is not None:
                    ax10.axvspan(idx_start, idx_end, color="#ff2222", alpha=0.25,
                                 label="Brute force window")
                    ax10.legend(fontsize=7, facecolor="#2a2a3e", labelcolor="white")
            except Exception:
                pass
    ax10.set_title("SSH Failed Logins / Minute")
    ax10.set_ylabel("Failed attempts")
    ax10.set_xlabel("Time")

    # -- [1,1] Top targeted firewall ports --
    ax11 = axes[1, 1]
    if not fw_df.empty:
        top_ports = fw_df["dst_port"].value_counts().head(15).sort_values()
        ax11.barh([str(p) for p in top_ports.index], top_ports.values, color="#bb44ff")
        ax11.set_xlabel("Drop count")
    ax11.set_title("Top Blocked Destination Ports")

    # -- [1,2] Attack type breakdown --
    ax12 = axes[1, 2]
    finding_counts = [(f["threat"], f["count"]) for f in findings if f["count"] > 0]
    finding_counts.sort(key=lambda x: x[1])
    if finding_counts:
        labels, counts = zip(*finding_counts)
        cmap_colours = plt.cm.plasma(np.linspace(0.2, 0.85, len(counts)))
        ax12.barh(range(len(labels)), counts, color=cmap_colours)
        ax12.set_yticks(range(len(labels)))
        ax12.set_yticklabels(labels, fontsize=7)
        ax12.set_xlabel("Event count")
    ax12.set_title("Attack Type Breakdown")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=120, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"[+] Dashboard saved to: {output_path}")


# ===========================================================================
# SECTION 5 — MAIN ENTRY POINT
# ===========================================================================

def run_analysis(apache_path: str, ssh_path: str, fw_path: str) -> int:
    """
    Parse all logs, run all detections, print the report, generate the
    dashboard, and return an exit code (1 if CRITICAL findings, else 0).
    """
    print(f"\n{CYAN}[*] Parsing log files...{RESET}")

    # --- Parse ---
    web_df = pd.DataFrame()
    ssh_df = pd.DataFrame()
    fw_df  = pd.DataFrame()

    if os.path.isfile(apache_path):
        web_df = parse_apache_log(apache_path)
        print(f"    Apache log : {len(web_df):>5} records  ({apache_path})")
    else:
        print(f"    {YELLOW}[!] Apache log not found: {apache_path}{RESET}")

    if os.path.isfile(ssh_path):
        ssh_df = parse_ssh_log(ssh_path)
        print(f"    SSH log    : {len(ssh_df):>5} records  ({ssh_path})")
    else:
        print(f"    {YELLOW}[!] SSH log not found: {ssh_path}{RESET}")

    if os.path.isfile(fw_path):
        fw_df = parse_firewall_log(fw_path)
        print(f"    Firewall   : {len(fw_df):>5} records  ({fw_path})")
    else:
        print(f"    {YELLOW}[!] Firewall log not found: {fw_path}{RESET}")

    # --- Run detections ---
    print(f"\n{CYAN}[*] Running detection algorithms...{RESET}")
    findings = [
        detect_ssh_brute_force(ssh_df),
        detect_sqli(web_df),
        detect_path_traversal(web_df),
        detect_xss(web_df),
        detect_bad_agents(web_df),
        detect_rate_anomaly(web_df),
        detect_port_scan(fw_df),
    ]
    print(f"    {len(findings)} detectors ran.")

    # --- Report ---
    print_report(findings)

    # --- Dashboard ---
    print(f"{CYAN}[*] Generating dashboard...{RESET}")
    try:
        plot_dashboard(web_df, ssh_df, fw_df, findings, DASHBOARD_PNG)
    except Exception as exc:
        print(f"    {YELLOW}[!] Dashboard generation failed: {exc}{RESET}")

    # Exit 1 if any CRITICAL finding has events
    has_critical = any(
        f["severity"] == "CRITICAL" and f["count"] > 0
        for f in findings
    )
    return 1 if has_critical else 0


def main():
    parser = argparse.ArgumentParser(
        description="Cybersecurity intrusion detection demo."
    )
    parser.add_argument(
        "--log",
        help="Analyse a single log file (apache, ssh, or firewall). "
             "If omitted, all three files in data/ are analysed.",
        default=None,
    )
    args = parser.parse_args()

    if args.log:
        # Single-file mode: detect which parser to use from the filename
        path = args.log
        fname = os.path.basename(path).lower()
        if "apache" in fname or "access" in fname:
            sys.exit(run_analysis(path, "", ""))
        elif "ssh" in fname or "auth" in fname:
            sys.exit(run_analysis("", path, ""))
        elif "firewall" in fname or "fw" in fname or "iptables" in fname:
            sys.exit(run_analysis("", "", path))
        else:
            # Attempt all parsers and use the one that returns rows
            sys.exit(run_analysis(path, path, path))
    else:
        # Default: analyse all three standard files
        sys.exit(run_analysis(APACHE_LOG, SSH_LOG, FW_LOG))


if __name__ == "__main__":
    main()
