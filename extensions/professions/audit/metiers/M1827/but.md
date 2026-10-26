# Enrichissement BUT et preuves

Les rapprochements et la sélection des fiches pédagogiques sont produits par le générateur et restent à relire. Un code cité dans un programme atteste cette mention, sans prouver une équivalence diplôme/métier. Un code parent est distingué d'un code exact. Les pages sont les pages physiques du PDF, base 1. Le texte des pages est une extraction ; les tableaux peuvent perdre leur disposition.

## BUT Réseaux et télécommunications

Fondement : `rapprochement_editorial_domaine_et_termes`. Termes de rapprochement : informatique, systeme. Pages citant le code exact : aucune ; pages citant le parent M1805 : aucune.

[Programme ministériel](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/r-seaux-et-t-l-communications-30876.pdf) ; SHA-256 `5830e494d94ef80653e529e4ecd5c5e784db82aa678f9b05353fe99196e7f38f`.

### Ressource R5.DEVCLOUD.09 — Outils et méthodes du DevOps

[Page 252](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/r-seaux-et-t-l-communications-30876.pdf#page=252). Termes communs : devop.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 3.3.9. Ressource R5.DevCloud.09 : Outils et méthodes du DevOps
> Compétence ciblée :
> – Accompagner le développement d’applications
> SAÉ au sein desquelles la ressource peut être mobilisée et combinée :
> – SAÉ 5.DevCloud.03 | Orchestrer la conteneurisation d’une application
> Descriptif :
> Contexte et ancrage professionnel :
> Le professionnel DevCloud peut intervenir en tant que DevOps (développeur logiciel et administrateur des infrastructures in-
> formatiques), automatisant et suivant toutes les étapes du cycle de vie d’une application ou d’une infrastructure de services.
> Dans la continuité des ressources R5.04 "Cycle de vie d’un projet informatique" et R5.DevCloud.11 "Programmer son infra-
> structure", cette ressource approfondit et synthétise l’ensemble du pipeline DevOps lorsque les applications s’appuient sur une
> infrastructure modulaire.
> Contenus :
> Les contenus suivants sont abordés sous l’angle du développeur (versionning d’applications) et/ou de l’administrateur système
> (versionning de configurations d’infrastructures) :
> – Les éléments de conception d’un service applicatif :
> – alternatives de conception puis de mise en production : virtualisée ou conteneurisée, servless, microservices ;
> – contraintes sur les infrastructures : Back-end as a Service (Baas), Function as a Service (FaaS) sur le Cloud ;
> – Les mécanismes d’interaction entre services :
> – les agents de messages/ressources avec centralisation (par ex : Broker) et abonnement ;
> – la surveillance du fonctionnement des microservices : gestion de log ;
> – La chaîne d’intégration continue et de développement continu CI/CD dans son ensemble (par ex : GitLab, Jenkins), avec
> un focus sur :
> – la phase de compilation (integrate/build), la gestion du packaging et des dépendances ;
> – les tests (unitaires et d’intégration) automatisés ;
> – l’automatisation des étapes de la CI/CD (par ex : configuration du <code>.gitlab-ci.yml</code>).
> La ressource peut introduire (ou approfondir) différents outils, par exemple :
> – pour la programmation des tests unitaires : doctest, pytest, Junit ;
> – pour l’analyse de la structure du code : SonarQube ;
> – pour la supervision et la centralisation des logs : ELK ;
> – pour la mise à disposition des versions de production : Nexus.
> Elle pourra permettre d’illustrer les méthodes de développement spécifiques aux applications informatiques (méthodes agiles,
> Scrum, ...) abordées dans le cadre de la R5.04 "Cycle de vie d’un projet informatique".
> Prérequis :
> – R5.DevCloud.11 | Programmer son infrastructure
> Apprentissages critiques ciblés :
> – AC35.01DevCloud | Adopter les pratiques de pilotage de projet
> – AC35.02DevCloud | Concevoir, gérer et sécuriser un environnement de microservices
> – AC35.03DevCloud | Gérer son infrastructure comme du code
> – AC35.04DevCloud | Gérer une chaîne d’intégration et/ou de déploiement continu
> Mots clés :
> Versionning – Log – Git – CI/CD – Tests – Automatisation – Registry
> Volume horaire :
> Volume horaire défini nationalement : 23 heures dont 13 heures de TP
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - 2022 -
> http://www.enseignementsup-recherche.gouv.fr - B.U.T. Réseaux et Télécommunications
> 252

### Ressource R5.DEVCLOUD.12 — Solutions Cloud

[Page 255](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/r-seaux-et-t-l-communications-30876.pdf#page=255). Termes communs : cloud.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 3.3.12. Ressource R5.DevCloud.12 : Solutions Cloud
> Compétence ciblée :
> – Coordonner des infrastructures modulaires
> SAÉ au sein desquelles la ressource peut être mobilisée et combinée :
> – SAÉ 5.DevCloud.03 | Orchestrer la conteneurisation d’une application
> Descriptif :
> Contexte et ancrage professionnel :
> Le professionnel DevCloud peut être amené à mettre en place un Cloud (public, privé ou hybride) pour son entreprise, no-
> tamment lorsque la sécurité des données est en jeu. Parmi les différentes solutions Cloud, il peut s’appuyer sur celles des
> fournisseurs de services (par ex : AWS, Azure...) supposant de calibrer avec justesse l’offre commerciale à ses besoins (Pla-
> teform as a Service). Il peut également opter pour sa propre infrastructure Cloud en l’hébergeant sur l’infrastructure réseau de
> son entreprise.
> Contenus :
> Sont abordés :
> – les enjeux du choix d’une solution Cloud (public, privé, hybride) ;
> – les solutions proposées par les fournisseurs de services et/ou les solutions pour l’hébergement en interne (par ex :
> Openstack, OpenNebula, ProxMox...) ;
> – (l’installation,) la configuration, et l’administration d’une solution Cloud ;
> – la surveillance (monitoring) de l’infrastructure :
> – outils de supervision centralisés ;
> – banc de test ;
> – métriques d’utilisation ;
> – la disponibilité des ressources et leur scalabilité ;
> – la sécurisation de l’infrastructure.
> La ressource pourra permettre de comparer les différentes solutions (publiques vs. privées) pour orienter une entreprise vers
> le choix de l’une ou de l’autre.
> Apprentissages critiques ciblés :
> – AC34.01DevCloud | Concevoir, administrer et superviser une infrastructure Cloud
> – AC34.02DevCloud | Orchestrer les ressources Cloud
> – AC34.03DevCloud | Investiguer sur les incidents et les résoudre afin d’améliorer la qualité et la fiabilité des infrastructures
> Mots clés :
> Cloud public – Cloud privé – Cloud hybride – Métriques – Administration – Surveillance
> Volume horaire :
> Volume horaire défini nationalement : 22 heures dont 14 heures de TP
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - 2022 -
> http://www.enseignementsup-recherche.gouv.fr - B.U.T. Réseaux et Télécommunications
> 255

### Ressource R3.DEVCLOUD.16 — Ecosystème Cloud

[Page 214](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/r-seaux-et-t-l-communications-30876.pdf#page=214). Termes communs : cloud.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 1.3.16. Ressource R3.DevCloud.16 : Ecosystème Cloud
> Compétence ciblée :
> – Coordonner des infrastructures modulaires
> SAÉ au sein desquelles la ressource peut être mobilisée et combinée :
> – SAÉ 3.DevCloud.04 | Mettre en place une infrastructure virtualisée
> Descriptif :
> Contexte et ancrage professionnel :
> Cette ressource introduit les éléments de langage et les enjeux spécifiques aux infrastructures Cloud offrant un ensemble
> de ressources virtuelles, d’espaces de stockage, d’applications/logiciels et de services. Elle vient en appui aux ressources
> techniques du parcours DevCloud.
> Contenus :
> La ressource présente, à titre de culture générale :
> – la définition des différents Cloud existants sur le marché : Cloud privé, Cloud public, Cloud hybride ;
> – les différentes formes de Cloud et la famille des AAS : Plateform-as-a-Service (PaaS), Infrastructure-as-a-Service (IasS),
> Software-as-a-Service (SaaS), Desktop-as-a-Service (DaaS), etc... ;
> – les alternatives pour la mise en place d’un Cloud (la mise en oeuvre et la configuration étant abordée dans d’autres
> ressources) :
> – les solutions commerciales (par ex : AWS, ...) ;
> – les architectures de microservices (par ex : pattern sidecar, proxy, ...) ;
> – les solutions pour l’hébergement d’un Cloud au sein de l’entreprise (par ex : OpenStack, ...).
> – les facteurs de choix d’une solution adaptée à une entreprise, notamment :
> – la sécurité globale de l’infrastructure (accès, données, ...) ;
> – le budget (coûts) ;
> – les réglementations (CNIL, RGPD) ayant trait aux problématiques de stockage, de protection des données ;
> – la charge de travail ;
> – la flexibilité et l’évolutivité de l’infrastructure ;
> – les problématiques climatiques/écologiques.
> Apprentissages critiques ciblés :
> – AC24.01DevCloud | Proposer une solution Cloud adaptée à l’entreprise
> – AC24.03DevCloud | Utiliser les services du Cloud
> Mots clés :
> Cloud privé – Cloud public – Sécurité de l’infrastructure – Sécurité des données – Enjeux
> Volume horaire :
> Volume horaire défini nationalement : 4 heures
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - 2022 -
> http://www.enseignementsup-recherche.gouv.fr - B.U.T. Réseaux et Télécommunications
> 214

### SAÉ 6.DEVCLOUD.01 — Gérer le pipeline d’une application orientée Cloud

[Page 258](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/r-seaux-et-t-l-communications-30876.pdf#page=258). Termes communs : application, cloud, pipeline.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 4.2. Fiches Situations d’apprentissage et d’évaluation (SAÉ)
> 4.2.1. SAÉ 6.DevCloud.01 : Gérer le pipeline d’une application orientée Cloud
> Compétences ciblées :
> – Coordonner des infrastructures modulaires
> – Accompagner le développement d’applications
> Objectifs et problématique professionnelle :
> Le professionnel R&T spécialisé en Développement Système et Cloud fait évoluer des applications existantes au sein de
> son entreprise en développant de nouvelles fonctionnalités. L ’application pouvant déjà être en production et utilisée par des
> collaborateurs ou des clients, il ne peut donc pas interrompre l’usage qui en est fait. Il intègre ses apports en utilisant une
> approche CI/CD (intégration continue, déploiement continu). Cette approche permet de tester les nouvelles fonctionnalités
> en s’assurant de leurs compatibilités avec l’existant avant de planifier leurs mises à disposition auprès des utilisateurs sans
> interruption de service.
> Descriptif générique :
> Le professionnel DevCloud met en œuvre la chaîne CI/CD d’une application structurée en microservices, intervient et surveille
> les différentes étapes du cycle de développement (dont la gestion des erreurs et des messages). Afin d’assurer le développe-
> ment des fonctionnalités, il applique la démarche suivante :
> – la mise en place de la chaîne d’intégration continue (CI) et ses différents tests ;
> – la mise en place de la chaîne de développement continue (CD) incluant la génération du livrable applicatif sous la forme
> d’un conteneur et le déploiement automatique de l’application avec ses améliorations ;
> – la vérification de la santé du code incluant le monitoring de l’application, un système d’alertes, la prise en compte de la
> sécurité à tous les niveaux de l’application et la gestion des messages (incluant les logs) renvoyés par l’application ;
> – la planification du déploiement avec le nettoyage des bases de données de l’orchestrateur, l’automatisation du déploie-
> ment en tenant compte de l’activité et la gestion d’un backup ;
> – la gestion des agents de messages pour la communication entre deux microservices (sous la forme d’une file FIFO par
> exemple).
> Apprentissages critiques :
> – AC34.01DevCloud | Concevoir, administrer et superviser une infrastructure Cloud
> – AC34.02DevCloud | Orchestrer les ressources Cloud
> – AC34.03DevCloud | Investiguer sur les incidents et les résoudre afin d’améliorer la qualité et la fiabilité des infrastructures
> – AC35.01DevCloud | Adopter les pratiques de pilotage de projet
> – AC35.02DevCloud | Concevoir, gérer et sécuriser un environnement de microservices
> – AC35.03DevCloud | Gérer son infrastructure comme du code
> – AC35.04DevCloud | Gérer une chaîne d’intégration et/ou de déploiement continu
> Ressources mobilisées et combinées :
> – R6.01 | Anglais : Insertion professionnelle 2
> – R6.02 | Expression-Culture-Communication professionnelles : Communiquer en tant que futur cadre intermédiaire
> – R6.DevCloud.04 | Pilotage de solutions Cloud pour l’entreprise
> Volume horaire :
> Volume horaire : à définir localement par chaque IUT
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - 2022 -
> http://www.enseignementsup-recherche.gouv.fr - B.U.T. Réseaux et Télécommunications
> 258

### SAÉ 3.DEVCLOUD.03 — Concevoir un réseau informatique multi-sites hébergeant des services virtualisés

[Page 195](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/r-seaux-et-t-l-communications-30876.pdf#page=195). Termes communs : informatique, reseau.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 1.2.3. SAÉ 3.DevCloud.03 : Concevoir un réseau informatique multi-sites hébergeant des services virtualisés
> Compétences ciblées :
> – Coordonner des infrastructures modulaires
> – Administrer les réseaux et l’Internet
> – Connecter les entreprises et les usagers
> Objectifs et problématique professionnelle :
> Le professionnel R&T spécialisé en Développement Système et Cloud doit faire évoluer régulièrement le réseau et les services
> de son entreprise. Il doit ainsi maintenir une infrastructure sécurisée au cœur du réseau qui permet aux différents sites de
> l’entreprise d’accéder aux ressources et aux services hébergés sur site et dans le Cloud.
> Descriptif générique :
> A partir d’un cahier des charges spécifiant les besoins du réseau d’une entreprise, le professionnel Développement Système
> et Cloud doit mettre en œuvre une infrastructure multi-sites adaptée et justifier les solutions apportées. Cette infrastructure
> repose sur :
> – les concepts fondamentaux du réseau :
> – routage, filtrage inter-VLAN ;
> – redondance (STP , routage dynamique, VRRP) ;
> – tunnel (VPN, VPN opérateurs) ;
> – services avancés ;
> – Wi-Fi.
> – la mise en place et la configuration des équipements ;
> – le test des fonctionnalités et les performances de l’infrastructure (QoS, MLS3) ;
> – les besoins spécifiques de la virtualisation, en utilisant les services mis en place dans le cadre de la SAÉ3.DevCloud.04
> "Mettre en place une infrastructure virtualisée" ;
> – une documentation détaillée de l’infrastructure mise en œuvre.
> Apprentissages critiques :
> – AC21.01 | Configurer et dépanner le routage dynamique dans un réseau
> – AC21.02 | Configurer et expliquer une politique simple de QoS et les fonctions de base de la sécurité d’un réseau
> – AC21.03 | Déployer des postes clients et des solutions virtualisées adaptées à une situation donnée
> – AC21.04 | Déployer des services réseaux avancés
> – AC21.05 | Identifier les réseaux opérateurs et l’architecture d’Internet
> – AC21.06 | Travailler en équipe pour développer ses compétences professionnelles
> – AC22.02 | Mettre en place un accès distant sécurisé
> – AC22.03 | Mettre en place une connexion multi-site via un réseau opérateur
> – AC24.02DevCloud | Virtualiser un environnement
> Ressources mobilisées et combinées :
> – R3.01 | Réseaux de campus
> – R3.02 | Réseaux opérateurs
> – R3.03 | Services réseaux avancés
> – R3.04 | Services d’annuaires
> – R3.11 | Anglais professionnel 1
> – R3.12 | Expression-Culture-Communication professionnelles : Savoir collaborer
> – R3.13 | Projet Personnel et Professionnel
> – R3.15 | Gestion de projet 2 : Utiliser les méthodes de gestion de projet
> – R3.DevCloud.17 | Virtualisation avancée
> Volume horaire :
> Volume horaire : à définir localement par chaque IUT
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - 2022 -
> http://www.enseignementsup-recherche.gouv.fr - B.U.T. Réseaux et Télécommunications
> 195

### Ressource R4.DEVCLOUD.09 — Fondamentaux de la conteneurisation

[Page 231](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/r-seaux-et-t-l-communications-30876.pdf#page=231). Termes communs : devops.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 2.3.9. Ressource R4.DevCloud.09 : Fondamentaux de la conteneurisation
> Compétences ciblées :
> – Coordonner des infrastructures modulaires
> – Accompagner le développement d’applications
> SAÉ au sein de laquelle la ressource peut être mobilisée et combinée :
> – SAÉ 4.DevCloud.01 | Développer et déployer un microservice dans un environnement virtualisé
> – STAGE.DevCloud | Stage
> Descriptif :
> Contexte et ancrage professionnel :
> La conteneurisation des services et des applications est l’un des outils majeurs du Cloud. Elle offre une grande flexibilité dans la
> conception et la maintenance des infrastructures. Elle facilite également la portabilité et la gestion du cycle de vie des services
> et des applications.
> Contenus :
> Cette ressource présente les éléments fondamentaux de la conteneurisation et aborde :
> – les principes des conteneurs, en les comparant notamment aux machines virtuelles ;
> – les différentes solutions : lxc/lxd, Docker, Podman, chroot, ... ;
> – les plateformes de partage et de stockage de conteneurs (par ex : le registry DockerHub, ...) ;
> – la création de conteneurs et leurs configurations (accès, stockage, parcours, mise en réseau). Cette partie pourra être
> abordée au travers de Docker et de l’usage des Dockerfiles, de docker-compose ;
> – l’architecture des infrastructures basées sur des conteneurisées (tant système qu’applicatives) et leurs bénéfices.
> Apprentissages critiques ciblés :
> – AC24.01DevCloud | Proposer une solution Cloud adaptée à l’entreprise
> – AC24.02DevCloud | Virtualiser un environnement
> – AC24.03DevCloud | Utiliser les services du Cloud
> – AC25.03DevCloud | Programmer son réseau par le code
> Mots clés :
> Conteneur – Docker
> Volume horaire :
> Volume horaire défini nationalement : 11 heures dont 6 heures de TP
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - 2022 -
> http://www.enseignementsup-recherche.gouv.fr - B.U.T. Réseaux et Télécommunications
> 231

### Ressource R5.DEVCLOUD.10 — Infrastructures conteneurisées

[Page 253](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/r-seaux-et-t-l-communications-30876.pdf#page=253). Termes communs : devops.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 3.3.10. Ressource R5.DevCloud.10 : Infrastructures conteneurisées
> Compétence ciblée :
> – Coordonner des infrastructures modulaires
> SAÉ au sein desquelles la ressource peut être mobilisée et combinée :
> – SAÉ 5.DevCloud.03 | Orchestrer la conteneurisation d’une application
> Descriptif :
> Contexte et ancrage professionnel :
> Dans la continuité de la ressource R4.DevCloud.09 "Fondamentaux de la conteneurisation" abordant les principes fondamen-
> taux des conteneurs, cette ressource présente l’orchestration des conteneurs, c’est-à-dire la gestion d’une infrastructure basée
> sur des conteneurs.
> Contenus :
> Sont abordés :
> – la définition d’un orchestrateur ;
> – le rôle de l’orchestrateur dans l’infrastructure réseau (déploiement, gestion, mise à l’échelle et mise en réseau) ;
> – les différentes solutions marchés (par ex : Kubernetes) ;
> – les éléments de mise en place d’un orchestrateur ;
> – la gestion de la sécurité des et dans les conteneurs ;
> – la disponibilité des conteneurs et l’introduction à la scalabilité.
> Apprentissages critiques ciblés :
> – AC34.01DevCloud | Concevoir, administrer et superviser une infrastructure Cloud
> – AC34.02DevCloud | Orchestrer les ressources Cloud
> Mots clés :
> Conteneur – Orchestrateur – Scalabilité – Sécurité
> Volume horaire :
> Volume horaire défini nationalement : 23 heures dont 14 heures de TP
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - 2022 -
> http://www.enseignementsup-recherche.gouv.fr - B.U.T. Réseaux et Télécommunications
> 253

### Ressource R5.DEVCLOUD.11 — Programmer son infrastructure

[Page 254](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/r-seaux-et-t-l-communications-30876.pdf#page=254). Termes communs : devops.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 3.3.11. Ressource R5.DevCloud.11 : Programmer son infrastructure
> Compétences ciblées :
> – Coordonner des infrastructures modulaires
> – Accompagner le développement d’applications
> SAÉ au sein desquelles la ressource peut être mobilisée et combinée :
> – SAÉ 5.DevCloud.03 | Orchestrer la conteneurisation d’une application
> Descriptif :
> Contexte et ancrage professionnel :
> Pour gagner en efficacité, en flexibilité et en stabilité, de nombreux outils ont été développés pour gérer et approvisionner
> (non plus manuellement mais) automatiquement les infrastructures et leurs applications informatiques, par le biais de codes
> informatiques. Ces outils sont aujourd’hui une composante essentielle du Cloud et du développement des applications, que le
> professionnel DevCloud aura à utiliser régulièrement. Cette ressource traite donc de l’Infrastructure as Code (IaC) dès lors que
> les réseaux sont programmables.
> Contenus :
> La ressource traite aussi bien le déploiement d’infrastructures, de systèmes, d’applications que de configurations notamment à
> vocation de sécurité. Sont abordés :
> – les enjeux et stratégies de déploiement pour mettre en place, reconfigurer, ajouter/modifier un réseau, ses équipements
> et ses services (incluant la gestion du stockage, des ressources et des droits d’accès) ;
> – l’intérêt de l’automatisation pour le déploiement à grande échelle, la reproductibilité de la configuration, etc. ;
> – les différentes solutions marchés (par ex : Powershell, Ansible, Terraform, Pulumi, AWS CodeDeploy, etc.) ;
> – la mise en place de déploiements automatisés, en se basant sur un ou des outils spécifiques.
> Apprentissages critiques ciblés :
> – AC34.01DevCloud | Concevoir, administrer et superviser une infrastructure Cloud
> – AC34.02DevCloud | Orchestrer les ressources Cloud
> – AC34.03DevCloud | Investiguer sur les incidents et les résoudre afin d’améliorer la qualité et la fiabilité des infrastructures
> – AC35.03DevCloud | Gérer son infrastructure comme du code
> Mots clés :
> Automatisation – Infrastructure as code
> Volume horaire :
> Volume horaire défini nationalement : 22 heures dont 13 heures de TP
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - 2022 -
> http://www.enseignementsup-recherche.gouv.fr - B.U.T. Réseaux et Télécommunications
> 254

### Ressource R4.ROM.09 — Outils DevOps

[Page 461](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/r-seaux-et-t-l-communications-30876.pdf#page=461). Termes communs : devops.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 2.3.9. Ressource R4.ROM.09 : Outils DevOps
> Compétence ciblée :
> – Gérer les infrastructures et les services des réseaux opérateurs
> SAÉ au sein de laquelle la ressource peut être mobilisée et combinée :
> – SAÉ 4.ROM.01 | Déployer une infrastructure opérateur et ses services clients
> – STAGE.ROM | Stage
> Descriptif :
> Contexte et ancrage professionnel :
> L ’étudiant devra être capable de mettre en œuvre des processus d’automatisation (de la configuration, de la gestion, des tests,
> du déploiement et de l’exploitation) des équipements réseaux et de services avec des conteneurs.
> Contenus :
> – Rôle du DevOps et introduction à la conteneurisation
> – Concepts de conteneurisation (container, image, commandes)
> – Automatisation de la gestion de l’infrastructure réseaux avec les librairies réseaux (Paramiko, Netmiko, Naplam, ... ), les
> API REST et Ansible
> – Gestion des versions avec GIT
> Prérequis :
> – R4.05 | Automatisation des tâches d’administration
> Apprentissages critiques ciblés :
> – AC24.02ROM | Virtualiser des services réseaux
> – AC24.05ROM | Automatiser la gestion des équipements réseaux
> Mots clés :
> Docker – YALM – YANG – Ansible – Conteneurisation – Automatisation – API – Cisco DEVNET
> Volume horaire :
> Volume horaire défini nationalement : 14 heures dont 6 heures de TP
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - 2022 -
> http://www.enseignementsup-recherche.gouv.fr - B.U.T. Réseaux et Télécommunications
> 461

## BUT Informatique

Fondement : `rapprochement_editorial_domaine_et_termes`. Termes de rapprochement : application, developpe, informati. Pages citant le code exact : aucune ; pages citant le parent M1805 : aucune.

[Programme ministériel](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/informatique-30855.pdf) ; SHA-256 `69027bf186ec1d059d55c37788547ed8562f753dd0becd98a750df088e1488f3`.

### Ressource R6.DEPLOI.06 — Cloud computing

[Page 245](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/informatique-30855.pdf#page=245). Termes communs : cloud, computing.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 4.3.6. Ressource R6.Deploi.06 : Cloud computing
> Compétences ciblées :
> – Développer — c’est-à-dire concevoir, coder, tester et intégrer — une solution informatique pour un client.
> – Installer, configurer, mettre à disposition, maintenir en conditions opérationnelles des infrastructures, des services et des
> réseaux et optimiser le système informatique d’une organisation
> SAÉ au sein desquelles la ressource peut être mobilisée et combinée :
> – SAÉ 6.Deploi.01 | Optimisation des services
> Descriptif :
> L ’objectif de cette ressource est d’apprendre à optimiser les accès, à organiser la gestion et à sécuriser les ressources parta-
> gées dans un cloud privé. Cette ressource permettra de comprendre comment déployer des applications et des données dans
> un cloud.
> Savoirs de référence étudiés
> – Services cloud (IAAS, PAAS, SAAS)
> – Modèles de déploiement (privé, public, hybride, communautaire)
> – Orchestration du cloud (outils de déploiement, de configuration, d’automatisation, de supervision...)
> – Supervision du cloud (outils de surveillance de l’intégrité, des performances et de la disponibilité)
> – Gestionnaire de log (par ex. : outils SIEM...)
> Prolongements suggérés
> – Les différents savoirs de référence pourront être approfondis
> Apprentissages critiques ciblés :
> – AC31.01 | Choisir et implémenter les architectures adaptées
> – AC33.03 | Appliquer une politique de sécurité au niveau de l’infrastructure
> – AC33.04 | Déployer et maintenir un réseau d’organisation en fonction de ses besoins
> Mots clés :
> Cloud – SAAS / PAAS / IAAS – Déploiement – Supervision
> Volume horaire :
> Volume horaire défini nationalement : 15 heures dont 6 heures de TP
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - Programmes nationaux 2022 – mis à jour en
> 2023 - http://www.enseignementsup-recherche.gouv.fr - B.U.T. Informatique
> 245

### Ressource R4.01 — Architecture logicielle

[Page 133](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/informatique-30855.pdf#page=133). Termes communs : architecture, logicielle.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 2.3. Fiches Ressources
> 2.3.1. Ressource R4.01 : Architecture logicielle
> Compétences ciblées :
> – Développer — c’est-à-dire concevoir, coder, tester et intégrer — une solution informatique pour un client.
> – Installer, configurer, mettre à disposition, maintenir en conditions opérationnelles des infrastructures, des services et des
> réseaux et optimiser le système informatique d’une organisation
> – Acquérir, développer et exploiter les aptitudes nécessaires pour travailler efficacement dans une équipe informatique
> SAÉ au sein de laquelle la ressource peut être mobilisée et combinée :
> – SAÉ 4.Real.01 | Développement d’une application complexe
> Descriptif :
> L ’objectif de cette ressource est de présenter des composants de la programmation qui peuvent être utilisés dans plusieurs
> domaines.
> Savoirs de référence étudiés
> – Patrons d’architecture (par ex. : MVC, MVVM...)
> – Utilisation de briques logicielles, d’interfaces de programmation, de bibliothèques tierces
> – Développement de services web
> Prolongements suggérés
> – Utilisation de services web (par ex. : requêtes asynchrones, formats d’échange de données...)
> – Organisation de l’accès aux données : base de données, annuaires, services Web...
> Apprentissages critiques ciblés :
> – AC21.01 | Élaborer et implémenter les spécifications fonctionnelles et non fonctionnelles à partir des exigences
> – AC21.02 | Appliquer des principes d’accessibilité et d’ergonomie
> – AC21.03 | Adopter de bonnes pratiques de conception et de programmation
> – AC23.01 | Concevoir et développer des applications communicantes
> – AC26.02 | Appliquer une démarche pour intégrer une équipe informatique au sein d’une organisation
> Mots clés :
> Services web – Bibliothèques – Patrons d’architecture – Accès aux données
> Volume horaire :
> Volume horaire défini nationalement : 32 heures dont 16 heures de TP
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - Programmes nationaux 2022 – mis à jour en
> 2023 - http://www.enseignementsup-recherche.gouv.fr - B.U.T. Informatique
> 133

### Ressource R5.DEPLOI.10 — Modélisations mathématiques pour les applications communicantes

[Page 231](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/informatique-30855.pdf#page=231). Termes communs : application, modelisation.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 3.3.10. Ressource R5.Deploi.10 : Modélisations mathématiques pour les applications communicantes
> Compétence ciblée :
> – Installer, configurer, mettre à disposition, maintenir en conditions opérationnelles des infrastructures, des services et des
> réseaux et optimiser le système informatique d’une organisation
> SAÉ au sein desquelles la ressource peut être mobilisée et combinée :
> – SAÉ 5.Deploi.01 | Évolution d’une infrastructure
> Descriptif :
> L ’objectif de cette ressource est d’approfondir un ou plusieurs domaines d’applications en donnant des éléments de formalisa-
> tion, de connaissances et d’usages spécifiques à ce ou ces domaines, en particulier dans le domaine des mathématiques et
> de l’algorithmique sous-jacentes.
> Savoirs de référence étudiés
> – Modélisations mathématiques et calculs liés à un domaine d’application (par ex. : cloud, traitement du signal, processus
> de Poisson, files d’attente, codage, cryptographie avancée...)
> Prolongements suggérés
> – Les différents savoirs de référence pourront être approfondis
> Apprentissage critique ciblé :
> – AC33.02 | Configurer un serveur et des services réseaux de manière avancée (virtualisation...)
> Mots clés :
> Modélisation – Domaine d’application spécifique
> Volume horaire :
> Volume horaire défini nationalement : 15 heures
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - Programmes nationaux 2022 – mis à jour en
> 2023 - http://www.enseignementsup-recherche.gouv.fr - B.U.T. Informatique
> 231

### SAÉ 3.DEPLOI.01 — Création et déploiement de services applicatifs

[Page 179](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/informatique-30855.pdf#page=179). Termes communs : deploiement.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 1.2. Fiches Situations d’apprentissage et d’évaluation (SAÉ)
> 1.2.1. SAÉ 3.Deploi.01 : Création et déploiement de services applicatifs
> Compétences ciblées :
> – Développer — c’est-à-dire concevoir, coder, tester et intégrer — une solution informatique pour un client.
> – Proposer des applications informatiques optimisées en fonction de critères spécifiques : temps d’exécution, précision,
> consommation de ressources..
> – Installer, configurer, mettre à disposition, maintenir en conditions opérationnelles des infrastructures, des services et des
> réseaux et optimiser le système informatique d’une organisation
> – Concevoir, gérer, administrer et exploiter les données de l’entreprise et mettre à disposition toutes les informations pour
> un bon pilotage de l’entreprise
> – Satisfaire les besoins des utilisateurs au regard de la chaîne de valeur du client, organiser et piloter un projet informatique
> avec des méthodes classiques ou agiles
> – Acquérir, développer et exploiter les aptitudes nécessaires pour travailler efficacement dans une équipe informatique
> Objectifs et problématique professionnelle :
> La problématique professionnelle est de créer, en équipe, une application en suivant une démarche de développement itérative
> ou incrémentale. En partant d’un besoin décrit de manière imprécise ou incomplète par un client, l’objectif est de clarifier,
> compléter, collecter et formaliser le besoin puis de développer une application client-serveur intégrant la manipulation des
> données et respectant des paradigmes de qualité (en particulier la sécurité).
> Descriptif générique :
> Cette SAÉ permet, après avoir collecté, formalisé les besoins d’un client, de développer une application client-serveur sécurisée
> permettant d’accéder à une base de données à créer.
> Les livrables attendus généralement dans le monde professionnel sont :
> – Documents de suivi du projet
> – Code de l’application et jeux d’essais
> – Schéma d’architecture du réseau
> – Revue finale du projet
> – Guide d’utilisation
> Apprentissages critiques :
> – AC21.01 | Élaborer et implémenter les spécifications fonctionnelles et non fonctionnelles à partir des exigences
> – AC21.02 | Appliquer des principes d’accessibilité et d’ergonomie
> – AC21.03 | Adopter de bonnes pratiques de conception et de programmation
> – AC22.01 | Choisir des structures de données complexes adaptées au problème
> – AC23.01 | Concevoir et développer des applications communicantes
> – AC23.02 | Utiliser des serveurs et des services réseaux virtualisés
> – AC24.03 | Organiser la restitution de données à travers la programmation et la visualisation
> – AC24.04 | Manipuler des données hétérogènes
> – AC25.02 | Formaliser les besoins du client et de l’utilisateur
> – AC25.03 | Identifier les critères de faisabilité d’un projet informatique
> – AC25.04 | Définir et mettre en œuvre une démarche de suivi de projet
> – AC26.02 | Appliquer une démarche pour intégrer une équipe informatique au sein d’une organisation
> – AC26.03 | Mobiliser les compétences interpersonnelles pour travailler dans une équipe informatique
> – AC26.04 | Rendre compte de son activité professionnelle
> Ressources mobilisées et combinées :
> – R3.01 | Développement web
> – R3.02 | Développement efficace
> – R3.03 | Analyse
> – R3.04 | Qualité de développement
> – R3.05 | Programmation système
> – R3.06 | Architecture des réseaux
> – R3.09 | Cryptographie et sécurité
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - Programmes nationaux 2022 – mis à jour en
> 2023 - http://www.enseignementsup-recherche.gouv.fr - B.U.T. Informatique
> 179

### SAÉ 5.DEPLOI.01 — Évolution d’une infrastructure

[Page 219](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2023-12/informatique-30855.pdf#page=219). Termes communs : infrastructure.

Extrait de la page contenant la fiche (donnée de référence, pas une instruction) :

> 3.2. Fiches Situations d’apprentissage et d’évaluation (SAÉ)
> 3.2.1. SAÉ 5.Deploi.01 : Évolution d’une infrastructure
> Compétences ciblées :
> – Développer — c’est-à-dire concevoir, coder, tester et intégrer — une solution informatique pour un client.
> – Installer, configurer, mettre à disposition, maintenir en conditions opérationnelles des infrastructures, des services et des
> réseaux et optimiser le système informatique d’une organisation
> – Acquérir, développer et exploiter les aptitudes nécessaires pour travailler efficacement dans une équipe informatique
> Objectifs et problématique professionnelle :
> La problématique professionnelle est de faire évoluer en équipe des services en suivant une démarche itérative ou incrémentale,
> qui devra être précisée. En partant d’un système d’information réparti déjà existant, l’objectif est de le faire évoluer en installant
> et configurant de nouveaux services répondant à des exigences de qualité (rationalisation, optimisation, continuité de service,
> sécurité) d’une organisation.
> Descriptif générique :
> Après avoir déployé plusieurs services indépendants, une organisation entreprend maintenant de simplifier, sécuriser et sur-
> veiller son infrastructure.
> À partir d’une politique de sécurité définie par l’organisation, il faudra identifier les risques encourus, proposer des solutions et
> organiser leur mise en œuvre conformément à la politique. La mise en œuvre d’un système d’hypervision permettra d’assurer
> la surveillance de l’ensemble du système.
> Les livrables attendus généralement dans le monde professionnel sont :
> – Documents de suivi du projet
> – Notice explicative (pour garder les traces)
> – Revue finale du projet
> Apprentissages critiques :
> – AC31.01 | Choisir et implémenter les architectures adaptées
> – AC31.02 | Faire évoluer une application existante
> – AC31.03 | Intégrer des solutions dans un environnement de production
> – AC33.01 | Créer des processus de traitement automatisé (solution de gestion de configuration et de parc, intégration et
> déploiement continu...)
> – AC33.03 | Appliquer une politique de sécurité au niveau de l’infrastructure
> – AC33.04 | Déployer et maintenir un réseau d’organisation en fonction de ses besoins
> – AC36.01 | Organiser et partager une veille technologique et informationnelle
> – AC36.02 | Identifier les enjeux de l’économie de l’innovation numérique
> – AC36.03 | Guider la conduite du changement informatique au sein d’une organisation
> – AC36.04 | Accompagner le management de projet informatique
> Ressources mobilisées et combinées :
> – R5.01 | Initiation au management d’une équipe de projet informatique
> – R5.03 | Politique de communication
> – R5.Deploi.04 | Programmation avancée en système
> – R5.Deploi.05 | Automatisation de la chaîne de production
> – R5.Deploi.06 | Installation & Configuration de services complexes
> – R5.Deploi.07 | Virtualisation avancée
> – R5.Deploi.08 | Continuité de service
> – R5.Deploi.09 | Cybersecurité
> – R5.Deploi.10 | Modélisations mathématiques pour les applications communicantes
> – R5.Deploi.11 | Économie durable et numérique
> – R5.Deploi.12 | Anglais
> Volume horaire :
> Volume horaire : à définir localement par chaque IUT
> ©Ministère de l’Enseignement supérieur, de la Recherche et de l’Innovation - Programmes nationaux 2022 – mis à jour en
> 2023 - http://www.enseignementsup-recherche.gouv.fr - B.U.T. Informatique
> 219
