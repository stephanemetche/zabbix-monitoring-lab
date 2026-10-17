# Zabbix Monitoring Lab

Laboratoire personnel de supervision : un serveur **Zabbix 7.0** sur **Debian 13** qui surveille lui-même et une machine **Windows Server 2025**, avec un test d'alerte réalisé de bout en bout (agent arrêté, problème détecté, problème résolu).

English summary: [README.md](README.md)

## Objectifs

- Comprendre l'architecture de Zabbix : serveur, base de données, interface web, agents.
- Superviser deux systèmes différents (Linux et Windows) depuis un seul serveur.
- Vérifier que le système détecte une panne et la signale (alerte), puis qu'il la clôture quand le service revient.

## Environnement

| Élément | Détail |
|---|---|
| Hyperviseur | VMware Fusion sur MacBook Pro, réseau NAT `192.168.209.0/24` |
| Serveur de supervision | Debian 13, hôte `srv-linux-01`, IP `192.168.209.129` |
| Machine surveillée | Windows Server 2025 Standard (évaluation), hôte `srv-windows-01`, IP `192.168.209.130` |
| Supervision | Zabbix 7.0.31 (serveur, interface web Apache/PHP, base MariaDB), Zabbix Agent 2 |

## Architecture

```
            MacBook (VMware Fusion, NAT 192.168.209.0/24)
 ┌───────────────────────────────┐        ┌───────────────────────────────┐
 │ Debian 13  srv-linux-01       │        │ Windows Server 2025           │
 │ 192.168.209.129               │        │ srv-windows-01                │
 │                               │ :10050 │ 192.168.209.130               │
 │  Serveur Zabbix  ─────────────┼───────▶│  Zabbix Agent 2               │
 │  MariaDB (archive)            │        │  (pare-feu : 10050 autorisé   │
 │  Apache + PHP (interface web) │        │   depuis 192.168.209.129 seul)│
 │  Zabbix Agent 2 (auto-surv.)  │        └───────────────────────────────┘
 └───────────────────────────────┘
```

Le serveur interroge chaque agent sur le port TCP 10050 (mode passif). L'agent répond avec les mesures de sa machine (processeur, mémoire, disques, services…).

## Ce qui a été réalisé

1. Installation de Zabbix 7.0.31 sur Debian 13 : serveur, base MariaDB, interface web.
2. Agent Zabbix Agent 2 sur la Debian (le serveur se surveille lui-même).
3. Installation de Zabbix Agent 2 7.0.31 sur Windows Server 2025, ouverture du port 10050 dans le pare-feu Windows, limitée à l'IP du serveur Zabbix.
4. Déclaration de l'hôte Windows dans Zabbix avec le modèle `Windows by Zabbix agent`.
5. Test d'alerte : arrêt de l'agent sur Windows, détection du problème par Zabbix, redémarrage de l'agent, résolution du problème.

## Résultat du test d'alerte

| Heure | Événement |
|---|---|
| 15:26 | `Stop-Service "Zabbix Agent 2"` sur Windows |
| 15:29:37 | Zabbix ouvre le problème « Windows: Zabbix agent is not available (for 3m) » (sévérité Average) |
| 15:40 | `Start-Service "Zabbix Agent 2"` sur Windows |
| 15:40:37 | Le problème passe en **RESOLVED** (durée totale : 11 min) |

Captures : [docs/04-add-host-and-alert-test.md](docs/04-add-host-and-alert-test.md).

## Documentation

1. [Architecture](docs/01-architecture.md)
2. [Installation du serveur Zabbix sur Debian](docs/02-zabbix-server-debian.md)
3. [Agent Zabbix sur Windows Server](docs/03-windows-agent.md)
4. [Ajout de l'hôte et test d'alerte](docs/04-add-host-and-alert-test.md)
5. [Limites et suite du projet](docs/05-limits-and-next-steps.md)

## Limites

Pas de notifications par e-mail, interface web en HTTP (pas de HTTPS), pas de chiffrement entre agent et serveur (PSK/TLS), pas de sauvegarde de la base Zabbix. Détails dans [docs/05-limits-and-next-steps.md](docs/05-limits-and-next-steps.md).

## Auteur

Stéphane Metche, laboratoire réalisé dans le cadre d'une reconversion vers l'administration d'infrastructures.
