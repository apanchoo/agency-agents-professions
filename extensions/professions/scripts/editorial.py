"""Adaptations éditoriales pour des assistants IA ; ne sont pas des textes officiels."""

# Étapes, livrables, critères : formulations originales, inspirées des activités
# pédagogiques. Les éléments officiels sélectionnés et paginés sont joints au skill.
RECIPES = {
    "info": (
        ["Traduire le besoin en cas d'usage et critères de recette", "Comparer les choix de conception, les données et les contraintes d'exploitation", "Implémenter une tranche fonctionnelle et traiter les erreurs", "Vérifier les scénarios nominaux, limites, sécurité et maintenance"],
        ["Code et instructions d'exécution", "Contrat de données ou d'API", "Résultats de recette et limites connues"],
        ["Un besoin observable correspond à chaque fonction livrée", "Les vérifications sont exécutées et leurs résultats conservés", "Les données, erreurs et dépendances sont explicites"]),
    "rt": (
        ["Cartographier les flux, équipements et niveaux de service attendus", "Proposer l'adressage, les services et la segmentation", "Préparer les configurations et un scénario de déploiement en laboratoire", "Vérifier connectivité, filtrage, supervision et restauration"],
        ["Architecture et plan d'adressage", "Configurations commentées", "Procédure de recette et retour arrière"],
        ["Chaque flux nécessaire possède un contrôle de connectivité", "Les secrets sont externalisés", "Une panne et sa restauration sont documentées"]),
    "mmi": (
        ["Identifier les publics, leurs besoins et le parcours d'usage", "Proposer une direction visuelle et éditoriale argumentée", "Produire le prototype, les médias ou l'interface demandés", "Évaluer compréhension, accessibilité et fonctionnement sur les supports cibles"],
        ["Parcours et prototype", "Assets ou interface exploitable", "Grille de recette UX et technique"],
        ["Les choix répondent à un besoin utilisateur", "Les droits des médias utilisés sont identifiés", "Le parcours principal est vérifié sur le support cible"]),
    "sd": (
        ["Définir la question, la population et le dictionnaire des variables", "Contrôler les données manquantes, doublons, unités et biais", "Choisir une analyse descriptive ou un modèle et une validation adaptés", "Présenter les résultats avec incertitude et reproductibilité"],
        ["Jeu préparé et dictionnaire", "Analyse ou modèle reproductible", "Visualisation et note d'interprétation"],
        ["Aucune fuite entre apprentissage et évaluation", "Les limites de collecte et d'inférence sont indiquées", "Chaque résultat est relié à une donnée et une méthode"]),
    "geii": (
        ["Décomposer les fonctions, interfaces et contraintes du système", "Dimensionner les fonctions électriques, électroniques ou de commande", "Préparer schéma, programme embarqué ou automatisme", "Définir et, si possible, exécuter les vérifications sur modèle ou banc"],
        ["Dossier de conception et interfaces", "Schéma ou code de commande", "Protocole de mesure et bilan de validation"],
        ["Les niveaux électriques et unités sont vérifiés", "La simulation est distinguée de la mesure physique", "Les protections et conditions de fonctionnement sont tracées"]),
    "gmp": (
        ["Formaliser fonctions, charges, interfaces et contraintes de fabrication", "Comparer les concepts puis dimensionner la solution retenue", "Produire la définition géométrique et la gamme proposée", "Vérifier tolérances, fabrication, assemblage et usage"],
        ["Dossier de définition", "Gamme ou scénario d'industrialisation", "Plan de contrôle dimensionnel"],
        ["Les hypothèses de charge sont explicites", "Les cotes fonctionnelles et tolérances sont justifiées", "La fabricabilité est examinée avec le procédé prévu"]),
    "gim": (
        ["Recueillir symptômes, historique et architecture de l'équipement", "Hiérarchiser les causes possibles et les contrôles discriminants", "Préparer l'intervention et la prévention de récurrence", "Définir la remise en service et les indicateurs de maintenance"],
        ["Diagnostic hiérarchisé", "Gamme d'intervention", "Plan de maintenance et fiche de remise en service"],
        ["Une cause proposée possède une preuve ou un contrôle à réaliser", "Les conditions de consignation sont identifiées", "Le retour au fonctionnement attendu est vérifiable"]),
    "gccd": (
        ["Recueillir site, usages, relevés et contraintes de l'ouvrage", "Comparer les solutions constructives et environnementales", "Préparer calculs, plans, quantités et organisation du chantier", "Contrôler cohérence des hypothèses, interfaces et points de réception"],
        ["Note de conception ou de calcul", "Plans et quantitatif", "Plan de contrôle et phasage"],
        ["Les données de site sont séparées des hypothèses", "Les unités et combinaisons de charge sont traçables", "La validation du professionnel compétent est identifiée"]),
    "mt2e": (
        ["Établir les usages et le bilan des consommations avec leurs unités", "Modéliser les flux thermiques et les conditions d'exploitation", "Comparer les variantes techniques, coûts et impacts", "Préparer le dimensionnement, le suivi et la vérification des gains"],
        ["Bilan énergétique", "Comparatif de solutions", "Plan de mesure et de suivi"],
        ["Les périmètres et conditions climatiques sont explicités", "Les rendements et facteurs de conversion sont sourcés", "Les gains estimés sont séparés des gains mesurés"]),
    "mp": (
        ["Définir le mesurande, la plage et la décision attendue", "Choisir chaîne de mesure, étalonnage et protocole", "Traiter les observations et établir le budget d'incertitude", "Comparer au critère d'acceptation et rédiger le compte rendu"],
        ["Protocole métrologique", "Calcul d'incertitude", "Rapport d'essai avec données"],
        ["Les unités, étalons et conditions ambiantes sont tracés", "Les valeurs aberrantes ne sont pas supprimées sans justification", "L'incertitude est prise en compte dans la décision"]),
    "chimie": (
        ["Définir l'objectif d'analyse, de synthèse ou de formulation", "Identifier échantillons, méthodes, conditions et risques", "Préparer le protocole, les calculs et les contrôles qualité", "Interpréter les résultats fournis et documenter écarts et limites"],
        ["Protocole et calculs préparatoires", "Plan de contrôle analytique", "Compte rendu d'interprétation"],
        ["Les concentrations, unités et bilans de matière sont cohérents", "Les blancs et références sont prévus", "Aucun résultat expérimental n'est inventé"]),
    "gcgp": (
        ["Définir le procédé, les flux entrants et les spécifications", "Construire les bilans de matière et d'énergie", "Comparer équipements, régulation et conditions opératoires", "Vérifier performance, risques et stratégie de suivi"],
        ["Schéma de procédé", "Bilans et dimensionnement", "Plan de conduite et contrôle"],
        ["Les bilans sont fermés ou leurs écarts justifiés", "Les conditions limites et régimes sont précisés", "Les scénarios de dérive sont identifiés"]),
    "gb": (
        ["Définir la question biologique, alimentaire, agronomique ou environnementale", "Préciser échantillonnage, méthodes et facteurs de variation", "Préparer le protocole et les traitements des observations", "Interpréter les données en distinguant constat, hypothèse et recommandation"],
        ["Protocole d'étude", "Tableau de résultats et contrôles", "Note d'interprétation et limites"],
        ["L'origine et la traçabilité des échantillons sont décrites", "Les témoins et répétitions pertinents sont prévus", "Aucune analyse de laboratoire ni qualification humaine n'est simulée comme acquise"]),
    "sgm": (
        ["Définir propriétés visées, sollicitations et fin de vie", "Comparer familles de matériaux et procédés", "Préparer les essais de caractérisation et le choix matière", "Vérifier propriétés, transformation et contraintes de recyclage"],
        ["Matrice de choix matière", "Plan de caractérisation", "Dossier procédé et fin de vie"],
        ["Les propriétés sont rattachées à une nuance et des conditions", "Les hypothèses de vieillissement sont indiquées", "Le choix considère fabrication et usage"]),
    "pec": (
        ["Décrire produit, protection attendue et circuit logistique", "Comparer matériaux, formes, assemblages et fin de vie", "Préparer le concept et le scénario d'industrialisation", "Définir essais de tenue, conformité et optimisation matière"],
        ["Cahier des charges emballage", "Concept et nomenclature", "Plan d'essais et comparatif environnemental"],
        ["La protection répond aux contraintes de distribution", "Les dimensions et quantités sont vérifiées", "Les allégations environnementales possèdent une méthode explicite"]),
    "qlio": (
        ["Cartographier les flux, ressources, temps et critères qualité", "Mesurer le fonctionnement et identifier contraintes et causes", "Proposer organisation, planification et amélioration", "Vérifier l'effet sur qualité, délai, charge et stocks"],
        ["Cartographie et diagnostic", "Planification ou plan d'amélioration", "Tableau de bord et recette"],
        ["Les capacités et délais utilisent le même horizon", "Les indicateurs possèdent une définition de calcul", "Les effets attendus sont séparés des résultats observés"]),
    "hse": (
        ["Définir activité, exposition, personnes concernées et environnement", "Identifier dangers, scénarios et mesures existantes", "Hiérarchiser les risques et proposer des mesures de prévention", "Définir responsabilités, contrôles et suivi des actions"],
        ["Analyse de risques", "Plan de prévention proposé", "Grille de contrôle et suivi"],
        ["Chaque risque relie danger, exposition et conséquence", "Les critères de cotation sont explicités", "Les obligations sont vérifiées à la date et dans le contexte concernés"]),
    "gea": (
        ["Définir le périmètre, la période et les décisions de gestion", "Contrôler les pièces, imputations et règles de calcul", "Produire budget, analyse financière ou dispositif RH demandé", "Rapprocher les résultats et présenter les écarts"],
        ["Dossier de calcul justifié", "Tableau de gestion", "Note de décision et contrôles"],
        ["Les totaux sont réconciliés avec les sources", "Les règles de gestion et dates d'application sont explicites", "Les données personnelles sont limitées au besoin"]),
    "gaco": (
        ["Décrire le besoin, les parties prenantes et les objectifs", "Comparer les options commerciales et organisationnelles", "Préparer plan d'action, budget et répartition des responsabilités", "Définir les jalons, indicateurs et ajustements"],
        ["Diagnostic d'organisation", "Plan de projet budgété", "Tableau de suivi et arbitrages"],
        ["Chaque objectif possède une mesure et un horizon", "Les ressources et responsables sont identifiés", "Les hypothèses commerciales sont distinguées des données constatées"]),
    "cj": (
        ["Qualifier les faits, les parties et la question à traiter", "Rechercher les textes et pièces applicables à la date concernée", "Comparer les qualifications et options avec leurs conséquences", "Préparer l'acte ou la note et les vérifications professionnelles nécessaires"],
        ["Chronologie et inventaire des pièces", "Note juridique sourcée", "Projet d'acte ou grille de vérification"],
        ["Chaque règle est reliée à une source et une date", "Les faits incertains restent signalés", "Le document distingue projet, avis et acte validé"]),
    "cs": (
        ["Décrire le besoin exprimé, le public et le territoire", "Analyser ressources, acteurs et conditions de participation", "Co-construire une proposition d'accompagnement ou d'action", "Prévoir l'évaluation, les relais et la confidentialité"],
        ["Diagnostic de situation", "Projet d'action et partenariats", "Grille d'évaluation et relais"],
        ["Les besoins sont distingués des interprétations", "La participation du public est prévue", "Les informations sensibles sont limitées à l'usage autorisé"]),
    "infocom": (
        ["Identifier publics, objectif d'information et ligne éditoriale", "Recouper les sources et organiser l'information", "Produire le contenu ou le dispositif documentaire demandé", "Vérifier exactitude, droits, lisibilité et diffusion"],
        ["Brief éditorial ou documentaire", "Contenu ou système de classement", "Grille de vérification des sources"],
        ["Chaque affirmation vérifiable possède une source", "Les droits et crédits sont identifiés", "Le format répond aux usages du public cible"]),
    "tc": (
        ["Définir marché, segment, offre et objectif commercial", "Analyser concurrence, besoins et données disponibles", "Préparer argumentaire, offre et plan d'actions", "Vérifier marge, parcours client et indicateurs de résultat"],
        ["Analyse de marché sourcée", "Offre et argumentaire", "Plan commercial et tableau de bord"],
        ["Les chiffres de marché ont une source et une date", "Les hypothèses de prix et marge sont explicites", "Les actions répondent à un segment et un objectif mesurable"]),
    "mlt": (
        ["Décrire flux, volumes, délais et contraintes de livraison", "Comparer modes, itinéraires, capacités et coûts", "Préparer plan de transport ou organisation logistique", "Vérifier faisabilité, traçabilité et gestion des aléas"],
        ["Schéma des flux", "Plan de transport chiffré", "Tableau de suivi et scénario d'aléa"],
        ["Les capacités et fenêtres de temps sont compatibles", "Les hypothèses de coût sont sourcées", "Les contraintes réglementaires et de traçabilité sont identifiées"]),
}


ROLE_RECIPES = {
    "M1827": (
        ["Définir les environnements, dépendances, secrets et critères de disponibilité",
         "Construire et tester une image conteneurisée avec un Dockerfile et une configuration de services",
         "Versionner le pipeline de compilation, tests, analyse et publication des artefacts",
         "Préparer le plan d'infrastructure et automatiser la configuration puis le déploiement",
         "Vérifier les sondes de santé, la supervision, la montée en charge et le retour arrière"],
        ["Dockerfile et configuration Docker Compose ou manifeste Kubernetes selon le besoin",
         "Pipeline GitLab CI ou Jenkins et rapports de tests",
         "Code Terraform ou Pulumi et playbooks Ansible adaptés à l'environnement",
         "Procédure de déploiement, supervision et retour arrière"],
        ["L'image construite est identifiée et testée avant sa publication",
         "Le pipeline arrête la livraison lorsqu'un test ou un contrôle requis échoue",
         "Les secrets sont externalisés et les changements d'infrastructure sont relus avant application",
         "Le déploiement possède un contrôle de disponibilité et un scénario de retour arrière vérifiable"]),
}

DOMAINS = {
    "A": ("Agriculture, nature et animaux", "gb", ["Calendrier d'opérations et observations à recueillir", "Fiche de suivi terrain et anomalies"]),
    "B": ("Artisanat et métiers d'art", "sgm", ["Brief de création et contraintes de matière", "Gamme de réalisation et contrôle de finition"]),
    "C": ("Banque, assurance et immobilier", "gea", ["Analyse du dossier et des pièces", "Comparatif de solutions et hypothèses chiffrées"]),
    "D": ("Commerce et vente", "tc", ["Proposition commerciale", "Suivi de relation client et indicateurs"]),
    "E": ("Communication et médias", "infocom", ["Brief et contenu éditorial", "Plan de production ou de diffusion"]),
    "F": ("Construction et travaux publics", "gccd", ["Préparation de travaux", "Quantitatif et contrôles de réception"]),
    "G": ("Hôtellerie, restauration, tourisme et animation", "gaco", ["Fiche de prestation et préparation", "Planning et contrôle de qualité de service"]),
    "H": ("Industrie", "qlio", ["Dossier de préparation industrielle", "Gamme et plan de contrôle"]),
    "I": ("Installation et maintenance", "gim", ["Diagnostic et contrôles discriminants", "Gamme d'intervention et remise en service"]),
    "J": ("Santé", None, ["Synthèse des informations fournies et questions à clarifier", "Support documentaire à faire vérifier par un professionnel de santé"]),
    "K": ("Services à la personne et à la collectivité", "cs", ["Analyse du besoin et acteurs concernés", "Plan d'action et critères de suivi"]),
    "L": ("Spectacle", "mmi", ["Dossier artistique ou technique", "Conducteur et contraintes de production"]),
    "M": ("Fonctions support de l'entreprise", "gea", ["Diagnostic et dossier de décision", "Plan de mise en œuvre et indicateurs"]),
    "N": ("Transport et logistique", "mlt", ["Plan d'exploitation et contraintes", "Suivi des flux et scénario d'aléa"]),
}


def recipe_for(code, programme_id=None):
    if code in ROLE_RECIPES:
        return ROLE_RECIPES[code]
    if programme_id:
        return RECIPES[programme_id]
    domain, fallback, outputs = DOMAINS[code[0]]
    steps = ["Qualifier la demande, les données disponibles et les limites de l'assistance",
             "Sélectionner les activités réellement utiles à la demande",
             "Produire le support documentaire, l'analyse ou la préparation demandée",
             "Confronter le livrable aux pièces disponibles et signaler les contrôles restant à réaliser"]
    checks = ["Les informations constatées sont séparées des hypothèses", "Chaque conclusion possède une preuve ou une vérification proposée", "Les interventions physiques et validations professionnelles restent identifiées comme telles"]
    return steps, outputs, checks
