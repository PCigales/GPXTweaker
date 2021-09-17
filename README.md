# GPXTweaker
A script in Python 3 to visualize, in 2D and 3D, and edit GPX tracks

Description in english in the second part of this document.


----------Français----------

GPXTweaker est une application, écrite en Python (≥ 3.8) et en Javascript, de visualisation, en 2D et en 3D, et d'édition, au travers d'une interface web, de trace GPX sur fond cartographique. Aucune dépendance n'est requise.

La sauvegarde de la trace mise à jour s'effectue dans un fichier distinct (par ajout du suffixe " - updated"), dans le même répertoire. Les données inchangées sont, autant que faire se peut, conservées en l'état, sans altération, pour assurer la préservation des champs constituant des extensions par rapport aux standards.

L'utilitaire est en phase de développement et de test, et comporte probablement encore de multiples erreurs de programmation. Il convient de ce fait de faire preuve de prudence lors de son utilisation en conditions réelles en s'assurant de l'absence de perte ou de corruption de données au niveau de la trace modifiée telle qu'enregistrée par rapport à la version d'origine avant de supprimer le fichier initial.
De nouvelles fonctionnalités seront, en outre, progressivement incorporées.  L'outil est, à ce stade, compatible avec MyTrails, quant à la prise en compte des données d'altitude issues du capteur de pression barométrique.
Seule la première trace préseente dans le fichier dont le chemin est fourni en paramètre est chargée.
Si le fichier indiqué n'existe pas, une nouvelle trace sera créée à partir de zéro.

Le fond sur lequel est affichée la trace peut être formé d'une carte générée par interrogation d'un serveur WMS ou enregistrée en local ou sur un serveur, ou bien être construit à partir de tuiles récupérées sur un serveur WMTS ou Web ou sauvegardées localement.
Sont déjà paramétrées et utilisables au travers d'un alias les sources suivantes: IGN (moyennant l'indication de la clé et d'informations complémentaires de connexion au serveur), OSM.

Les données d'élévation contenues dans la trace peuvent être complétées ou remplacées par les informations obtenues par interrogation d'un serveur WMS ou WMTS ou l'API IGN (moyennant l'indication de la clé et d'informations complémentaires de connexion au serveur) renvoyant une réponse au format x-bil-32.

Le tracé de point en point peut s'effectuer en ligne droite ou en suivant les chemins.

Les modifications et insertions de points peuvent être annulées/rétablies soit point par point (si un point est sélectionné), soit par segment et, s'il s'agit d'une opération portant sur plusieurs points (comme un suivi de chemin), par lot (si un segment est sélectionné), soit sur l'ensemble de la trace et par lot (si aucun élément n'est sélectionné).

Il est possible d'assembler une carte à partir de tuiles au format jpeg au moyen du programme jpegtran.

Mode d'emploi:
  - copier le script GPXTweaker.py dans un répertoire
  - copier et personnaliser le fichier de configuration GPXTweaker.cfg dans le même répertoire
  - en option: copier le fichier de commandes jpegtran.bat et modifier le chemin d'accès vers le programme jpegtran (à télécharger)
  - lancer GPXTweaker en observant la syntaxe de ligne de commande décrite ci-dessous

Le module fournit diverses classes destinées à la manipulation directe de contenus cartographiques. Le fichier "test.py" expose différents cas d'usage possibles.

Syntaxe:  

  GPXTweaker [-h] URI [--conf|-c CONF] [--map|-m MAP] [--emap|-e EMAP] [--maxheight|-mh MAX_HEIGHT] [--maxwidth|-mw MAX_WIDTH] [--v|-v VERBOSITY]  
où:  
  -h: afficher l'aide  
  URI: le chemin d'accès à la trace (en local ou, en lecture seule, sur un serveur)  
  CONF: le chemin d'accès au fichier de configuration (même répertoire que le script par défaut)  
  MAP: le chemin d'accès à la carte (en local ou sur un serveur) ou le nom d'un fournisseur de carte paramétré dans le fichier de configuration, ou non mentionné pour utiliser les fournisseurs de tuiles définis dans ce même fichier  
  EMAP: le chemin d'accès à la carte d'altitudes ou vide (ou '.') pour utiliser le fournisseur de cartes d'altitudes paramétré dans le fichier de configuration, ou non mentionné pour utiliser le fournisseur de tuiles ou données d'altitudes définis dans ce même fichier  
  MAX_HEIGHT et MAX_WIDTH: si le nom d'un fournisseur de carte est mentionné, la hauteur et la largeur maximales de la carte à retourner doit être indiquée au moyen de ces deux paramètres  
  VERBOSITY: niveau de verbosité de 0 à 2 (0 par défaut)

Exemples:  

  GPXTweaker t.gpx  
  GPXTweaker t.gpx -m m.png -v 1  
  GPXTweaker t.gpx -c "%appdata%\gpxtweaker\" -m "IGN PLANV2" -e -h 3000 -w 6000

Dans l'interface:
  - clic gauche sur la carte pour la faire glisser
  - clic gauche sur un point pour le sélectionner ou le déplacer
  - clic gauche sur un segment pour le sélectionner
  - clic droit sur la carte pour insérer un point après le point sélectionné ou un point de cheminement sinon
  - ctrl + clic droit sur la carte pour insérer un point après le point sélectionné en mode suivi de chemin
  - clic droit sur un point ou un segment pour le masquer
  - roulette souris pour faire glisser la carte verticalement
  - shift + roulette souris pour faire glisser la carte horizontalement
  - ctrl + roulette souris pour zoomer ou dézoomer
  - alt + roulette souris pour passer au point suivant ou précédent


----------English----------

GPXTwekaer is an application, in Python (≥ 3.8) and Javascript, for visualizing, in 2D and in 3D, and editing, throught a web interface, of GPX tracks on a cartographic background. No dependency is required.

The backup of the updated track is done in a distinct file (by addition of the suffix " - updated"), in the same folder. Unchanged datas are, as much as possible, kept as they are, without alteraton, in order to ensure the conservation of fields constituting extensions relatively to standards.

The utility is in development and test phase, and probably still includes many bugs. It is therefore necessary to be careful when using it in real conditions by making sure that no data loss or corruption occurred in the modified track as saved compared to the original version before deleting the initial file.
New features will, besides, preogressively be inplemented. The tool is, currently, compatible with MyTrails in taking into account altitude datas coming from the barometric pressure sensor.
Only the first track present in the file whose path is provided as argument is loaded.
If the indicated file does not exist, a new track will be created from scratch.

The background on which the track is displayed can be made of a map generated by interrogation of a WMS server or saved locally or on a server, or also be built from tiles retrieved from a WMTS or Web server or stored locally.
Are already set and callable under an alias these sources: IGN (provided a key and suitable connexion infos are given), OSM.

Elevation datas included in the track can be completed or replaced by the informations obtained by interrogation or a WMS or WMTS server
 or the IGN API (provided a key and suitable connexion infos are given) sending back a response in x-bil-32 format.

The drawing from point to point can be done in straight line or following pathes.

Modifications and insertions of points can be undone/redone either point by point (if a point is selected), or by segment and, if an operation dealing with several points is concerned (such as path following), by batch (if a segment is selected), or on the whole track and by batch (if no element is selected).

It is possible to assemble a map from tiles in jpeg format thanks to the program jpegtran.

Instructions:
  - copy the script GPXTWeaker in a folder
  - copy and customize the configuration file GPXTweaker.cfg in the same folder
  - optionally: copy the batch file jpegtean.bat and modify the path to the program jpegtran (needs to be downloaded)
  - run GPXTweaker accordingly to the command line syntax describede below

The module provides different classes designed for direct handling of cartographic contents. The file "test.py" exsposes different possible use cases.

Syntax:  

  GPXTweaker [-h] URI [--conf|-c CONF] [--map|-m MAP] [--emap|-e EMAP] [--maxheight|-mh MAX_HEIGHT] [--maxwidth|-mw MAX_WIDTH] [--v|-v VERBOSITY]  
where:  
  -h: shows the help  
  URI: the path to the track (on local or, in read only mode, on a server)  
  CONF: the path to the configuration file (same folder as the script by default)  
  MAP: the path to the map (on local or on a server) or the name of a map provider set in the configuration file, or not mentioned in order to use the tiles providers defined in this file  
  EMAP: the path to the elevations map or blank (or '.') to use the elevations map provider setin the configuration file, or not mentioned in order to use the elevations tiles or data defined in this file  
  MAX_HEIGHT and MAX_WIDTH: if the name of a map provider is mentioned, the max height and width of the map to be retrieved has to be indicated with these two arguments  
  VERBOSITY: verbosity level from 0 to 2 (0 by default)

Examples:  

  GPXTweaker t.gpx  
  GPXTweaker t.gpx -m m.png -v 1  
  GPXTweaker t.gpx -c "%appdata%\gpxtweaker\" -m "IGN PLANV2" -e -h 3000 -w 6000

In the interface:
  - left click on the map to scroll it
  - left click on a dot to select or move it
  - left click on a segment to select it
  - right click on the map to insert a dot after the selected dot or a waypoint otherwise
  - ctrl + right click on the map to insert a dot after the selected one in path following mode
  - right click on a dot or a segment to hide it
  - mouse wheel to scroll the map vertically
  - shift + mouse wheel to scroll the map horizontally
  - ctrl + mouse wheel to zoom in or out
  - alt + mouse wheel to switch to the next or previous point
