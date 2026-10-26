# Sources et attribution

## France Travail — ROME

France Travail, anciennement Pôle emploi. ROME 4.0 version 62, publication du **19 octobre 2026**, validation du 26 août 2026. Export officiel intégral récupéré le 26 octobre 2026.

- [Présentation et téléchargement officiels](https://www.francetravail.org/opendata/repertoire-operationnel-des-meti.html?type=article)
- [Export JSON intégral](https://api.francetravail.fr/api-nomenclatureemploi/v1/open-data/json)
- [Licence Ouverte ROME](https://www.francetravail.org/files/live/sites/peorg/files/documents/Statistiques-et-analyses/Open-data/ROME/rome_licence_ouverte.pdf), copie dans `sources/rome-license.pdf`.

La licence téléchargée autorise notamment reproduction, adaptation et réutilisation, sous mention du producteur et de la date d'actualisation. Elle n'implique aucune reconnaissance de cette bibliothèque par France Travail. Les dates, fichiers, tailles et empreintes exactes se trouvent dans `sources/manifest.json` et `data/rome-source.json`.

## Programmes nationaux des BUT

Ministère de l'Enseignement supérieur, de la Recherche et de l'Innovation : programmes nationaux 2022, dans les éditions PDF actuellement liées par la [page ministérielle LP-BUT](https://www.enseignementsup-recherche.gouv.fr/fr/lp-86602), consultée le 26 octobre 2026. Certaines couvertures indiquent une mise à jour en 2023 ; conserver la mention propre à chaque PDF, sans attribuer une même révision à tous.

Les 24 PDF d'origine sont conservés dans `sources/but/`. Les références et extraits gardent les crédits ministériels et leur pagination. `data/but-sources.json` donne les URL, et `sources/manifest.json` les empreintes. Les droits et mentions des PDF restent ceux de leurs producteurs ; la présente attribution ne leur applique pas la licence MIT du dépôt d'inspiration.

## Inspiration Agency Agents

[msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents), sous licence MIT. Un exemple de profil et sa licence sont conservés dans `sources/agency-example.md` et `sources/agency-LICENSE` pour documenter la référence demandée.

Les profils générés reprennent l'idée d'un rôle spécialisé avec mission, méthode, livrables et critères. Leur texte est une adaptation originale à partir du ROME et des BUT ; aucune expérience personnelle ni performance d'agent n'est empruntée au projet d'origine.

## Adaptations

Les rapprochements ROME/BUT, leur classement, les workflows, les livrables proposés et les critères de recette sont des adaptations éditoriales générées. Ils ne constituent ni un référentiel officiel de formation, ni une équivalence de diplôme, ni une habilitation à exercer un métier réglementé.
