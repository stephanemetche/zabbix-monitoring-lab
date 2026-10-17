# 05 - Limites et suite du projet

Ce lab est volontairement simple. Voici ce qui n'est **pas** fait.

## Limites actuelles

| Sujet | État | Risque ou conséquence |
|---|---|---|
| Notifications | Aucune configurée | Les alertes ne sont visibles que dans l'interface web |
| HTTPS | Interface en HTTP | Le mot de passe d'administration circule en clair sur le réseau du lab |
| Chiffrement agent/serveur | « Agent encryption : None » | Les échanges sur 10050 ne sont ni chiffrés ni authentifiés par clé |
| Sauvegarde | Aucune sauvegarde de la base `zabbix` | La configuration serait perdue en cas de perte de la VM (mitigé par les snapshots VMware) |
| Durcissement de la Debian | Non traité dans ce projet | Voir le projet séparé de socle de sécurité Debian |
| Windows | Licence d'évaluation | Machine de lab uniquement |

## Suite possible (version 2)

1. Configurer un moyen de notification (e-mail), puis tester qu'une alerte envoie un message.
2. Passer l'interface en HTTPS.
3. Activer le chiffrement par clé pré-partagée (PSK) entre serveur et agents.
4. Sauvegarder la base `zabbix` avec `mysqldump`, planifié.
5. Ajouter une alerte sur un seuil (par exemple processeur ou espace disque) et la déclencher volontairement.
6. Ajouter un outil de gestion de parc (GLPI) sur un serveur séparé.
