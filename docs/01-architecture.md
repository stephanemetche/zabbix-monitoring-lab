# 01 - Architecture

## Les composants de Zabbix

| Composant | Rôle | Où il tourne dans le lab |
|---|---|---|
| **Serveur Zabbix** | Le cerveau : interroge les agents, calcule les alertes | Debian (`srv-linux-01`) |
| **Base de données** | L'archive : stocke les mesures et la configuration | MariaDB sur la Debian |
| **Interface web** | L'écran : tableaux de bord, hôtes, problèmes | Apache + PHP sur la Debian, `http://192.168.209.129/zabbix` |
| **Agent (Zabbix Agent 2)** | L'espion : mesure sa machine et répond au serveur | Sur chaque machine surveillée |

La Debian porte aussi un agent : le serveur se surveille lui-même (hôte « Zabbix server », `127.0.0.1:10050`).

## Plan réseau

| Machine | Nom | IP | Rôle |
|---|---|---|---|
| Debian 13 | `srv-linux-01` | `192.168.209.129` | Serveur Zabbix + agent |
| Windows Server 2025 | `srv-windows-01` | `192.168.209.130` | Machine surveillée + agent |

Réseau NAT de VMware Fusion : `192.168.209.0/24`, passerelle `192.168.209.2`.

## Flux

- **Serveur vers agent, TCP 10050** : le serveur demande les valeurs à l'agent (mode passif). C'est le flux utilisé par l'hôte `srv-windows-01`.
- **Agent vers serveur, TCP 10051** : utilisé pour les vérifications actives. L'agent Windows a été installé avec `SERVERACTIVE` renseigné, mais l'hôte du lab utilise l'interface passive.

## Choix

- Agent 2 plutôt que l'agent classique : version actuelle fournie par Zabbix pour Linux et Windows.
- Modèles fournis par Zabbix (`Linux by Zabbix agent`, `Windows by Zabbix agent`) plutôt que des mesures écrites à la main.
- Règle de pare-feu Windows restreinte à l'IP du serveur Zabbix, pour n'ouvrir le port qu'à la machine qui en a besoin.
