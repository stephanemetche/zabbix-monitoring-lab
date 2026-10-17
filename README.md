# Zabbix Monitoring Lab

Home lab: a **Zabbix 7.0** monitoring server on **Debian 13**, monitoring itself and a **Windows Server 2025** machine, with a tested alert (agent stopped, problem detected, problem resolved).

French version with full details: [README_FR.md](README_FR.md)

## Architecture

```
            MacBook (VMware Fusion, NAT 192.168.209.0/24)
 ┌───────────────────────────────┐        ┌───────────────────────────────┐
 │ Debian 13  srv-linux-01       │        │ Windows Server 2025           │
 │ 192.168.209.129               │        │ srv-windows-01                │
 │                               │ :10050 │ 192.168.209.130               │
 │  Zabbix server  ──────────────┼───────▶│  Zabbix Agent 2               │
 │  MariaDB (archive)            │        │  (firewall: 10050 allowed     │
 │  Apache + PHP (web UI)        │        │   from 192.168.209.129 only)  │
 │  Zabbix Agent 2 (self-monitor)│        └───────────────────────────────┘
 └───────────────────────────────┘
```

## What was actually done

- Zabbix 7.0.31 installed on Debian 13: server, MariaDB database, Apache/PHP web interface
- Zabbix Agent 2 on the Debian server (it monitors itself)
- Zabbix Agent 2 7.0.31 installed on Windows Server 2025, Windows firewall rule for port 10050 (source restricted to the Zabbix server)
- Windows host declared in Zabbix with the template `Windows by Zabbix agent`
- Alert test: agent stopped on Windows, problem detected by Zabbix, agent restarted, problem resolved

## Structure

```
zabbix-monitoring-lab/
├── README.md
├── README_FR.md
├── docs/
│   ├── 01-architecture.md
│   ├── 02-zabbix-server-debian.md
│   ├── 03-windows-agent.md
│   ├── 04-add-host-and-alert-test.md
│   └── 05-limits-and-next-steps.md
└── images/            (screenshots of the alert test)
```

## Limits (not done yet)

No e-mail notifications, web interface in HTTP (no HTTPS), no agent encryption (PSK/TLS), no backup of the Zabbix database. See [docs/05-limits-and-next-steps.md](docs/05-limits-and-next-steps.md).

## Author

Stéphane Metche, lab built as part of a retraining towards infrastructure administration.
