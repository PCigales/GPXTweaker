# GPXTweaker (éditeur GPX / GPX editor)
A script in Python 3 to visualize, in 2D and 3D, and edit GPX tracks

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.


Description in english in the second part of this document.


----------Français----------

GPXTweaker est une application, écrite en Python (≥ 3.8) et en Javascript, de visualisation, en 2D et en 3D, et d'édition, au travers d'une interface web, de trace GPX sur fond cartographique. Elle offre également la possibilité d'afficher des photos et vidéos géolocalisées. Aucune dépendance n'est requise.

Lors de la sauvegarde de la trace mise à jour, le fichier inital est renommé, par ajout du suffixe " - original" ou, les fois suivantes, " - backup", dans le même répertoire. Les données inchangées sont, autant que faire se peut, conservées en l'état, sans altération, pour assurer la préservation des champs constituant des extensions par rapport aux standards.

Malgré des tests approfondis, l'utilitaire est toujours susceptible de comporter des erreurs de programmation. Il convient de ce fait de faire preuve de prudence lors de son utilisation en conditions réelles en s'assurant de l'absence de perte ou de corruption de données au niveau de la trace modifiée telle qu'enregistrée par rapport à la version d'origine avant de supprimer le fichier initial.
L'outil est compatible avec MyTrails, quant à la prise en compte des données d'altitude issues du capteur de pression barométrique.
Si le fichier indiqué n'existe pas, une nouvelle trace sera créée à partir de zéro.

Le fond sur lequel est affichée la trace peut être formé d'une carte générée par interrogation d'un serveur WMS ou enregistrée en local ou sur un serveur, ou bien être construit à partir de tuiles récupérées sur un serveur WMTS ou Web ou sauvegardées localement.
Sont déjà paramétrées et utilisables au travers d'un alias les sources suivantes: IGN (moyennant l'indication de la clé et d'informations complémentaires de connexion au serveur), OSM, Google, Bing.

Les données d'élévation contenues dans la trace peuvent être complétées ou remplacées par les informations obtenues par interrogation d'un serveur WMS ou WMTS ou l'API IGN (moyennant l'indication de la clé et d'informations complémentaires de connexion au serveur) renvoyant une réponse au format x-bil-32 ou hgt.

Le tracé de point en point peut s'effectuer en ligne droite ou en suivant les chemins, grâce à un service de calcul d'itinéraires (IGN et OSRM sont déjà configurés).

Les modifications et insertions de points peuvent être annulées/rétablies soit point par point, soit par segment et, s'il s'agit d'une opération portant sur plusieurs points (comme un suivi de chemin), par lot, sur un segment ou sur l'ensemble de la trace.

La trace peut, irréversiblement, être purgée des éléments décochés en la sauvant puis en actualisant la page d'interface.

Le calcul des statistiques de la trace peut être partiellement (option Gpu_comp sur 1) ou totalement (option Gpu_comp sur 2) déchargé vers le processeur graphique.

Il est possible d'assembler une carte à partir de tuiles au format jpeg au moyen du programme jpegtran.

Mode d'emploi:
  - copier le script GPXTweaker.py dans un répertoire
  - copier et personnaliser le fichier de configuration GPXTweaker.cfg dans le même répertoire
  - en option: copier le fichier de commandes jpegtran.bat et modifier le chemin d'accès vers le programme jpegtran (à télécharger)
  - lancer GPXTweaker en observant la syntaxe de ligne de commande décrite ci-dessous

Le module fournit diverses classes destinées à la manipulation directe de contenus cartographiques. Le fichier "test.py" expose différents cas d'usage possibles.

Syntaxe:  

  GPXTweaker [-h] URI [--conf|-c CONF] [--trk|-t TRK] [--map|-m MAP] [--emap|-e EMAP] [--box|-b BOX] [--size|-s SIZE] [--dpi|-d DPI] [--noopen|-n] [--v|-v VERBOSITY]  
où:  
  -h: afficher l'aide  
  URI: le chemin d'accès à la trace (en local ou, en lecture seule, sur un serveur) ou argument pas mentionné pour démarrer avec l'explorateur de traces  
  CONF: le chemin d'accès au fichier de configuration (même répertoire que le script par défaut)  
  TRK: l'indice de la trace (commençant à 0, pour les fichiers gpx contenant plusieurs traces) (0, c'est à dire la première, par défaut)  
  MAP: le chemin d'accès complet à la carte (en local ou sur un serveur) ou le nom d'un fournisseur de carte paramétré dans le fichier de configuration ou vide pour utiliser le premier founisseur de carte configuré, ou non mentionné pour utiliser les fournisseurs de tuiles définis dans ce même fichier  
  EMAP: le chemin d'accès complet à la carte d'altitudes ou le nom d'un fournisseur de cartes d'altitudes paramétré dans le fichier de configuration ou vide pour utiliser le premier fournisseur de carte d'altitudes configuré, ou non mentionné pour utiliser les fournisseurs de tuiles et données d'altitudes définis dans ce même fichier  
  BOX: si le chemin d'une carte ou le nom d'un fournisseur de carte est mentionné ou laissé vide, la boîte au format "minlat, maxlat, minlon, maxlon" (avec les "") de la carte à retourner peut être indiquée au moyen de ce paramètre  
  SIZE: si le chemin d'une carte ou le nom d'un fournisseur de carte est mentionné ou laissé vide, les dimensions au format "hauteur, largeur" (avec les "") de la carte à retourner peuvent être indiquées au moyen de ce paramètre  
  DPI: si le nom d'un fournisseur de carte est mentionné ou laissé vide, la densité d'image en pixels par pouce de la carte à retourner peut être indiquée au moyen de ce paramètre (90 par défaut)  
  -noopen: pour que le script n'ouvre pas la page d'interface dans le navigateur par défaut (et ainsi pouvoir utiliser un autre navigateur)  
  VERBOSITY: niveau de verbosité de 0 à 2 (0 par défaut)

Exemples:  

  GPXTweaker -v 1  
  GPXTweaker t.gpx  
  GPXTweaker t.gpx -m "d:\maps\m.png" -v 1  
  GPXTweaker t.gpx -c "%appdata%\gpxtweaker\" -m "IGN PLANV2" -e -s "3000, 6000"

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
  - alt + roulette souris pour passer au point ou segment suivant ou précédent
  - ctrl + clic sur les boutons de zoom pour modifier l'opacité de la carte

Pour associer les fichers dont l'extension est ".gpx" avec GPXTweaker:
  - créer dans le même répertoire un fichier GPXTweaker.bat contenant la ligne, en remplaçant [path] par le chemin d'accès au script: @"[path]\GPXTweaker.py" %1
  - dans l'explorateur de fichiers, double-cliquer sur un fichier ".gpx", cliquer sur "plus d'applications" puis sur "rechercher une autre application", et naviguer jusque puis choisir "GPXTweaker.bat"


----------English----------

GPXTweaker is an application, in Python (≥ 3.8) and Javascript, for visualizing, in 2D and in 3D, and editing, throught a web interface, GPX tracks on a cartographic background. It also offers the possibility of displaying geotagged photos and videos. No dependency is required.

When saving the updated track, the inital file is renamed, by adding the suffix "- original" or, the following times, "- backup", in the same folder. Unchanged datas are, as much as possible, kept as they are, without alteration, in order to ensure the conservation of fields constituting extensions relatively to standards.

Despite extensive testing, the utility is still susceptible to include programming errors. It is therefore necessary to be careful when using it in real conditions by making sure that no data loss or corruption occurred in the modified track as saved compared to the original version before deleting the initial file.
The tool is compatible with MyTrails in taking into account altitude datas coming from the barometric pressure sensor.
If the indicated file does not exist, a new track will be created from scratch.

The background on which the track is displayed can be made of a map generated by interrogation of a WMS server or saved locally or on a server, or also be built from tiles retrieved from a WMTS or Web server or stored locally.
Are already set and callable under an alias these sources: IGN (provided a key and suitable connexion infos are given), OSM, Google, Bing.

Elevation datas included in the track can be completed or replaced by the informations obtained by interrogation or a WMS or WMTS server
 or the IGN API (provided a key and suitable connexion infos are given) sending back a response in x-bil-32 or hgt format.

The drawing from point to point can be done in straight line or following pathes, thanks to a service of itineraries calculation (IGN ans OSRM are already configured).

Modifications and insertions of points can be undone/redone either point by point, or by segment and, if an operation dealing with several points is concerned (such as path following), by batch, on a segment or on the whole track.

The track can, irreversibly, be purged of unchecked elements by saving it then reloading the interface page.

The computation of the statistics of the track can be partially (option Gpu_comp on 1) ou totally (option Gpu_comp on 2) onto the graphics processor unit.

It is possible to assemble a map from tiles in jpeg format thanks to the program jpegtran.

Instructions:
  - copy the script GPXTWeaker in a folder
  - copy and customize the configuration file GPXTweaker.cfg in the same folder
  - optionally: copy the batch file jpegtean.bat and modify the path to the program jpegtran (needs to be downloaded)
  - run GPXTweaker accordingly to the command line syntax describede below

The module provides different classes designed for direct handling of cartographic contents. The file "test.py" exsposes different possible use cases.

Syntax:  

  GPXTweaker [-h] URI [--conf|-c CONF] [--trk|-t TRK] [--map|-m MAP] [--emap|-e EMAP] [--box|-b BOX] [--size|-s SIZE] [--dpi|-d DPI] [--noopen|-n] [--v|-v VERBOSITY]  
where:  
  -h: shows the help  
  URI: the path to the track (on local or, in read only mode, on a server) or argument not mentioned to start with the explorer of tracks  
  CONF: the path to the configuration file (same folder as the script by default)  
  TRK: the index of the track (starting at 0, for the gpx files containing several tracks) (0, that is to say the first one, by défault)  
  MAP: the full path to the map (on local or on a server) or the name of a map provider set in the configuration file or blank to use the first map provider configured, or not mentioned in order to use the tiles providers defined in this file  
  EMAP: the full path to the elevations map or the name of an elevations map provider set in the configuration file or blank to use the first elevations map provider configured, or not mentioned in order to use the elevations tiles or data providers defined in this file  
  BOX: if the path to a map or the name of a map provider is mentioned or kept blank, the box in format "minlat, maxlat, minlon, maxlon" (with the "") of the map to be retrieved can be indicated with this argument  
  SIZE: if the path to a map or the name of a map provider is mentioned or kept blank, the dimensions in format "height, width" (with the "") of the map to be retrieved can be indicated with this argument  
  DPI: if the name of a map provider is mentioned or kept blank, the image density in dots per inch of the map to be retrieved can be indicated with this argument (90 by default)  
  -noopen: so that the script does not open the interface page in the default browser (and so, be able to use another browser)  
  VERBOSITY: verbosity level from 0 to 2 (0 by default)

Examples:  

  GPXTweaker -v 1  
  GPXTweaker t.gpx  
  GPXTweaker t.gpx -m "d:\maps\m.png" -v 1  
  GPXTweaker t.gpx -c "%appdata%\gpxtweaker\" -m "IGN PLANV2" -e -s "3000, 6000"

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
  - alt + mouse wheel to switch to the next or previous point or segment
  - ctrl + click on the zoom buttons to change the opacity of the map

In order to associate the files whose extension is ".gpx" with GPXTweaker:
  - create in the same folder a file GPXTweaker.bat containing the line, replacing [path] by the path to the script: @"[path]\GPXTweaker.py" %1
  - in the files explorer, double-click on a ".gpx" file, click on "more applications" then on "look for another application", and navigate towards then choose "GPXTweaker.bat"
