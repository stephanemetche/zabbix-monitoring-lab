# 02 - Installation du serveur Zabbix sur Debian 13

Machine : `srv-linux-01`, Debian 13 (trixie), 2 vCPU, 2 Go de RAM, IP `192.168.209.129`.
Version installée : Zabbix 7.0 LTS (7.0.31). Les commandes sont lancées avec un utilisateur disposant de `sudo`.

> Le mot de passe de la base est représenté par `<DB_PASSWORD>`. Choisis un mot de passe fort et ne le publie jamais.

## 1. Ajouter le dépôt officiel Zabbix

```bash
wget https://repo.zabbix.com/zabbix/7.0/debian/pool/main/z/zabbix-release/zabbix-release_7.0-5+debian13_all.deb
sudo dpkg -i zabbix-release_7.0-5+debian13_all.deb
sudo apt update
```

Le paquet `zabbix-release` ajoute le dépôt Zabbix à APT.

## 2. Installer les paquets

```bash
sudo apt install -y zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent2 mariadb-server
```

| Paquet | Rôle |
|---|---|
| `zabbix-server-mysql` | Serveur Zabbix (version MySQL/MariaDB) |
| `zabbix-frontend-php` + `zabbix-apache-conf` | Interface web et sa configuration Apache |
| `zabbix-sql-scripts` | Scripts de création des tables |
| `zabbix-agent2` | Agent qui surveille la Debian elle-même |
| `mariadb-server` | Base de données |

## 3. Créer la base de données

```bash
sudo mysql
```

```sql
create database zabbix character set utf8mb4 collate utf8mb4_bin;
create user 'zabbix'@'localhost' identified by '<DB_PASSWORD>';
grant all privileges on zabbix.* to 'zabbix'@'localhost';
set global log_bin_trust_function_creators = 1;
quit;
```

Importer le schéma initial (203 tables ont été créées) :

```bash
zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql --default-character-set=utf8mb4 -uzabbix -p zabbix
```

Puis désactiver l'option temporaire :

```bash
sudo mysql -e "set global log_bin_trust_function_creators = 0;"
```

## 4. Configurer le serveur Zabbix

Dans `/etc/zabbix/zabbix_server.conf`, renseigner le mot de passe de la base :

```
DBPassword=<DB_PASSWORD>
```

## 5. Démarrer les services

```bash
sudo systemctl restart zabbix-server zabbix-agent2 apache2
sudo systemctl enable zabbix-server zabbix-agent2 apache2
```

## 6. Assistant d'installation web

Ouvrir `http://192.168.209.129/zabbix` (en **http**, pas https).

Problème rencontré : le contrôle des prérequis indiquait **Fail** pour la locale système. Correction :

```bash
sudo sed -i 's/^# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
sudo locale-gen
sudo systemctl restart apache2
```

Après rechargement de la page, tous les prérequis passent en **OK**.

Paramètres saisis dans l'assistant :

| Champ | Valeur |
|---|---|
| Type de base | MySQL |
| Hôte de base | `localhost` (port par défaut) |
| Nom de base | `zabbix` |
| Utilisateur | `zabbix` |
| Nom du serveur Zabbix | `Lab-Zabbix` |

Connexion initiale : `Admin` avec le mot de passe par défaut de Zabbix, **changé immédiatement** (User settings > Change password).

## 7. Vérification

```bash
sudo systemctl is-active zabbix-server zabbix-agent2 apache2 mariadb
```

Résultat : 4 lignes `active`. Dans l'interface, le tableau de bord affiche « Zabbix server is running » et l'hôte « Zabbix server » est disponible (ZBX vert).
