# PoussePousseEditData
PoussePousseEditData est un plugIn QGis de création et de contrôle de jeu de données géographiques sur fond cartographique. La création des objets ponctuels se fait à la manière du jeu de pousse-pousse où l'on doit reconstituer une image en déplaçant des cases. Une grille recouvre le jeu de données ce qui permet de saisir des objets ponctuels cellule après cellule. Une fois la saisie terminée, une seconde saisie des objets géographiques sur un nombre aléatoire de cellule permet de contrôler la qualité de la saisie.



Installation
===

PoussePousseEditData est un plugin pour le logiciel QGIS. Il est donc nécessaire que ce dernier soit installé sur l’ordinateur. QGIS peut être téléchargé gratuitement via l’URL suivant : http://www.qgis.org/fr/site/

Le plugin a été testé avec succès sur les versions 2.18.22 de QGIS.



Guide d’utilisation du logiciel
===

Démarrage
---

La grille doit être déjà créée, carrée et de type polygone. Le premier attribut doit contenir l’index (type entier) des cellules.

Le fichier CSV doit aussi être créé. Le caractère séparateur est la virgule, la première ligne contient les entêtes des colonnes et les 2 premières colonnes contiennent les coordonnées des points.



