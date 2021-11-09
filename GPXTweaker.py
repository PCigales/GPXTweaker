from functools import partial
import urllib.parse
import socket
import selectors
import ssl
import http.client
import math
from xml.dom import minidom
import html
import socket
import socketserver
import email.utils
import time
import threading
import os, os.path
from pathlib import Path
import json
import base64 
import zlib
import gzip
import lzma
import zipfile
from io import BytesIO
import ctypes, ctypes.wintypes
import subprocess
import struct
import uuid
import webbrowser
import msvcrt
import locale
import argparse

FR_STRINGS = {
  'tilescache': {
    '_id': 'Cache de tuiles',
    'init': 'initialisation (taille: %s, fils: %s)',
    'get': 'tuile (%s, %s) demandée',
    'cancel': 'abandon de la fourniture de la tuile (%s, %s)',
    'found': 'tuile (%s, %s) trouvée dans le cache en position %s',
    'del': 'suppression de la position %s du cache',
    'add': 'insertion de la tuile (%s, %s) dans le cache en position %s',
    'error': 'échec du chargement de la tuile (%s, %s)',
    'load': 'tuile (%s, %s) chargée',
    'configure': 'configuration (jeu de tuile: %s, matrice: %s)',
    'ifound': 'informations trouvées dans le cache (jeu de tuiles: %s, matrice: %s)',
    'fail': 'échec de la configuration (jeu de tuile: %s, matrice: %s)',
    'close': 'fermeture'
  },
  'map': {
    '_id': 'Gestionnaire de carte',
    'mapfetch': 'récupération de la carte %s',
    'maplfail': 'échec de la récupération de la carte %s',
    'maploaded': 'carte %s chargée',
    'mapsave': 'enregistrement de la carte sous %s',
    'mapsfail': 'échec de l\'enregistrement de la carte sous %s',
    'mapsaved': 'carte sauvée sous %s',
    'tileretrieve': 'fourniture de la tuile %s',
    'tilelfound': 'tuile %s trouvée localement',
    'tilelexpired': 'tuile locale %s expirée',
    'tilefetch': 'récupération de la tuile %s',
    'tilerfail': 'échec de la fourniture de la tuile %s',
    'tileretrieved': 'tuile %s fournie',
  },
  'track': {
    '_id': 'Gestionnaire de trace',
    'init': 'initialisation',
    'load': 'chargement de la trace %s',
    'new': 'création d\'une nouvelle trace sous %s',
    'lerror': 'échec du chargement de la trace %s',
    'loaded': 'trace %s chargée (nom: "%s", points de cheminement: %s, segments: %s, points: %s)',
    'save': 'enregistrement de la trace sous %s',
    'serror': 'échec de l\'enregistrement de la trace sous %s',
    'saved': 'trace enregistrée sous %s',
  },
  'interface': {
    '_id': 'Interface',
    'conf': 'chargement de la configuration',
    'cerror': 'échec du chargement de la configuration (%s)',
    'cloaded': 'configuration chargée',
    'build': 'génération de la page d\'interface',
    'buildexp': 'génération de la page d\'interface de l\'explorateur',
    'berror': 'échec de la génération de la page d\'interface',
    'berror1': 'échec de la génération de la page d\'interface (conversion en WebMercator)',
    'berror2': 'échec de la génération de la page d\'interface (trace vide sans délimitation du cadre)',
    'berror3': 'échec de la génération de la page d\'interface (carte "%s" pas définie)',
    'berror4': 'échec de la génération de la page d\'interface (trace débordant de la vue)',
    'berror5': 'échec de la génération de la page d\'interface (paramètres de jeux ou de cache de tuiles)',
    'berror6': 'trace sautée car débordant de la vue',
    'elevation': 'fournisseur d\'élévations configuré (%s)',
    'eerror': 'échec de la configuration du fournisseur d\'élévations (%s)',
    'itinerary': 'fournisseur d\'itinéraires configuré (%s)',
    'built': 'page d\'interface générée',
    'builtexp': 'page d\'interface de l\'explorateur générée',
    'request': 'réception de la requête %s %s',
    'response': 'réponse à la requête %s %s envoyée',
    'rerror': 'échec de la réponse à la requête %s %s',
    'rbad': 'rejet de la requête %s %s (mauvais identifiant de session)',
    'rnfound': 'rejet de la requête %s %s (ressource demandée indisponible)',
    'rfailed': 'réponse d\'échec à la requête %s %s envoyée',
    '3dbuild': 'génération de la page de visionnage 3D',
    '3derror1': 'échec de la génération de la page de visionnage 3D (récupération des altitudes du terrain)',
    '3derror2': 'échec de la génération de la page de visionnage 3D (récupération de la cartographie du terrain)',
    '3dmodeled': 'modélisation du terrain achevée (%s = %s x %s points, source: "%s")',
    '3dbuilt': 'page de visionnage 3D générée',
    'jsession': 'Une session est déjà active !',
    'jexpfail': 'Le chargement des données a échoué !',
    'jserror': 'La sauvegarde a échoué: ',
    'jesconfirm': 'Remplacer toutes les données d\'élévation du segment ?',
    'jeconfirm': 'Remplacer toutes les données d\'élévation de la trace ?',
    'jeasconfirm': 'Intervertir les données d\'élévation et d\'altitude du segment ?',
    'jeaconfirm': 'Intervertir les données d\'élévation et d\'altitude de la trace ?',
    'jrconfirm': 'Inverser la trace dans son ensemble ?',
    'junload': 'Attention, les données seront perdues !',
    'jundo': 'annuler la dernière action d\'insertion ou de modification de propriétés de points&#13;&#10;+alt: seulement pour l\'élément qui a le focus',
    'jredo': 'rétablir la dernière action annulée&#13;&#10;+alt: seulement pour l\'élément qui a le focus',
    'jinsertb': 'focus sur segment: insérer un point en début de segment&#13;&#10;focus sur point / point de cheminement: dupliquer le point / point de cheminement au-dessus&#13;&#10;pas de focus: insérer un point de cheminement au début',
    'jinserta': 'focus sur segment: insérer un point en fin de segment&#13;&#10;focus sur point / point de cheminement: dupliquer le point / point de cheminement au-dessous&#13;&#10;pas de focus: insérer un point de cheminement à la fin',
    'jpath': 'tracer un chemin vers le point qui a le focus depuis le point précédent',
    'jelementup': 'focus sur segment: monter l\'élément (annuler pour rétablir l\'horodatage d\'origine)&#13;&#10;focus sur point: déplacer le focus sur le segment courant&#13;&#10;focus sur point de cheminement: monter l\'élément',
    'jelementdown': 'focus sur segment: descendre l\'élément (annuler pour rétablir l\'horodatage d\'origine)&#13;&#10;focus sur point: déplacer le focus sur le segment suivant&#13;&#10;focus sur point de cheminement: descendre l\'élément',
    'jsegmentcut': 'focus sur segment: dupliquer le segment&#13;&#10;focus sur point: diviser le segment au-dessus',
    'jsegmentabsorb': 'fusionner le segment qui a le focus avec le segment suivant',
    'jsegmentreverse': 'focus sur segment / pas de focus: inverser le segment / la trace',
    'jelevationsadd': 'focus sur segment ou point / pas de focus: ajouter les élévations manquantes à l\'élément / la trace&#13;&#10;+alt: à partir des données d\'altitude',
    'jelevationsreplace': 'focus sur segment ou point / pas de focus: remplacer les élévations de l\'élément / la trace&#13;&#10;+alt: à partir des données d\'altitude&#13;&#10;+shift: intervertir avec les données d\'altitude',
    'jaltitudesjoin': 'focus sur segment: égaliser l\'altitude du dernier point avec celle du premier point du segment suivant par décalage uniforme de tout le segment&#13;&#10;focus sur point: égaliser l\'altitude du dernier point avec celle du premier point du segment suivant par décalage progressif du segment à partir du point qui a le focus',
    'jdatetime': 'focus sur segment ou point / pas de focus: compléter par inter/extra polation l\'horodatage de l\'élément / la trace',
    'jsave': 'sauvegarder la trace&#13;&#10;(puis recharger la page pour éliminer irréversiblement les éléments désactivés)',
    'jswitchpoints': 'afficher / masquer les points et points de cheminement',
    'jgraph': 'afficher / masquer le graphique&#13;&#10;+shift: afficher / masquer les contrôles du filtre de calcul de dénivelé&#13;&#10;+ctrl: afficher / masquer les contrôles du filtre de calcul de pente&#13;&#10;+alt: afficher / masquer les contrôles du filtre de calcul de vitesse',
    'j3dviewer': 'ouvrir la visionneuse 3D',
    'jascending': 'permuter l\'ordre de tri des traces sur croissant',
    'jdescending': 'permuter l\'ordre de tri des traces sur décroissant',
    'joset': 'sélectionner le critère de tri des traces',
    'jsortnone': 'Aucun',
    'jsortname': 'Nom',
    'jsortfilepath': 'Chemin d\'accès',
    'jsortduration': 'Durée',
    'jsortdistance': 'Distance',
    'jsortelegain': 'Dénivelé élévation',
    'jsortaltgain': 'Dénivelé altitude',
    'jsortdate': 'Date',
    'jsortproximity': 'Proximité',
    'jfolders': 'afficher / masquer le panneau de sélection des répertoires des traces à lister',
    'jhidetracks': 'masquer les traces listées&#13;&#10;+alt: masquer les traces pas listées',
    'jshowtracks': 'afficher les traces listées&#13;&#10;+alt: afficher les traces pas listées',
    'jedit': 'éditer la trace',
    'jzoomall': 'recadrer sur toutes les traces',
    'jtset': 'sélectionner le jeu de tuiles&#13;&#10;+shift: sélection du fournisseur d\'élévations&#13;&#10;+ctrl: sélection du fournisseur d\'itinéraires',
    'jeset': 'sélectionner le fournisseur d\'élévations&#13;&#10;+alt: sélection du jeu de tuiles&#13;&#10;+ctrl: sélection du fournisseur d\'itinéraires',
    'jiset': 'sélectionner le fournisseur d\'itinéraires&#13;&#10;+alt: sélection du jeu de tuiles&#13;&#10;+shift: sélection du fournisseur d\'élévations',
    'jtsetonly': 'sélectionner le jeu de tuiles',
    'jminus': 'dézoomer&#13;&#10;+ctrl: atténuer',
    'jlock': 'verrouiller / déverrouiller le jeu de tuiles',
    'jplus': 'zoomer&#13;&#10;+ctrl: réaccentuer',
    'jfilterpanel1': 'Seuils calcul dénivelé',
    'jfilterpanel2': 'Plages calcul pente',
    'jfilterpanel3': 'Plages calcul vitesse',
    'jspduration': '&nbsp;durée',
    'jsmax': 'max&nbsp;&nbsp;&nbsp;',
    'jfoldersw': 'Répertoires:',
    'jhelp': 'clic-glisse gauche sur la carte pour la faire défiler&#13;&#10;roulette souris sur la carte pour la faire défiler verticalement&#13;&#10;shift + roulette souris sur la carte pour la faire défiler horizontalement&#13;&#10;ctrl + roulette souris sur la carte pour zoomer ou dézoomer&#13;&#10;alt + roulette souris sur la carte pour passer au point de cheminement / point / segment précédent ou suivant&#13;&#10;clic / clic-glisse gauche (+ shift / alt) sur le tracé d\'un point / point de cheminement pour le sélectionner / le déplacer (et effacer / conserver ses données d\'élévation, ou à défaut choisir selon si la distance est supérieure à 25m ou pas)&#13;&#10;ctrl + clic / clic-glisse gauche sur le tracé d\'un point pour le sélectionner / le déplacer et construire un chemin depuis le point précédent jusqu\'à celui-ci&#13;&#10;clic gauche sur le tracé d\'un segment pour le sélectionner&#13;&#10;clic droit sur la carte pour insérer un point après le point qui a le focus ou un point de cheminement sinon&#13;&#10;ctrl + clic droit sur la carte pour insérer un point après le point qui a le focus en mode suivi de chemin&#13;&#10;clic droit sur le tracé d\'un point / point de cheminement / segment pour le supprimer&#13;&#10;survol souris d\'un bouton pour afficher sa légende',
    'jexphelp': 'clic-glisse gauche sur la carte pour la faire défiler&#13;&#10;roulette souris sur la carte pour la faire défiler verticalement&#13;&#10;shift + roulette souris sur la carte pour la faire défiler horizontalement&#13;&#10;ctrl + roulette souris sur la carte pour zoomer ou dézoomer&#13;&#10;alt + roulette souris sur la carte pour passer à la trace précédente ou suivante&#13;&#10;clic gauche sur le tracé d\'une trace pour la sélectionner&#13;&#10;clic droit sur le tracé d\'une trace pour la masquer&#13;&#10;survol souris d\'un bouton pour afficher sa légende',
    'jwaypoints': 'Points de cheminement',
    'jpoints': 'Points',
    'jlat': 'Lat',
    'jlon': 'Lon',
    'jhor': 'Hor',
    'jname': 'Nom',
    'jele': 'Elé',
    'jalt': 'Alt',
    'jsegment': 'Segment',
    'jtracks': 'Traces',
    'jfile': 'Fich',
    'jfolder': 'Répe',
    'jperiod': 'Péri',
    'jcontent': 'Cont',
    'jtrackcontent': '%s seg(s) | %s pt(s) | %s pt(s) de chem',
    'jgraphdistance': 'distance',
    'jgraphelevation': 'élévation',
    'jgraphaltitude': 'altitude',
    'jgraphelegain': 'déniv élé',
    'jgraphaltgain': 'déniv alt',
    'jgrapheleslope': 'pente élé',
    'jgraphaltslope': 'pente alt',
    'jgraphspeed': 'vitesse',
    'jgraphtime': 'durée',
    'jmundo1': 'Insertion de %s point(s) annulée',
    'jmundo2': 'Modification de %s point(s) annulée',
    'jmredo1': 'Insertion de %s point(s) rétablie',
    'jmredo2': 'Modification de %s point(s) rétablie',
    'jminsert1': 'Point de cheminement inséré',
    'jminsert2': 'Point inséré',
    'jmpath1': 'Récupération de l\'itinéraire en cours...',
    'jmpath2': 'Itinéraire inséré',
    'jmpath3': 'Échec de la récupération de l\'itinéraire',
    'jmelementup1': 'Point de cheminement déplacé',
    'jmelementup2': 'Segment déplacé',
    'jmsegmentcut1': 'Segment dupliqué',
    'jmsegmentcut2': 'Segment divisé',
    'jmsegmentabsorb': 'Segments fusionnés',
    'jmsegmentreverse1': 'Segment inversé',
    'jmsegmentreverse2': 'Trace inversée',
    'jmelevations1': 'Récupération des élévations en cours...',
    'jmelevations2': 'Élévation du point / point de cheminement mise à jour',
    'jmelevations3': 'Élévations du segment mises à jour (%s point(s) sur %s)',
    'jmelevations4': 'Élévations de la trace mises à jour (%s point(s) et point(s) de cheminement sur %s)',
    'jmelevations5': 'Élévations de la trace mises à jour (%s point(s) sur %s)',
    'jmelevations6': 'Échec de la récupération des élévations',
    'jmelealt1': 'Élévation et altitude du point interverties',
    'jmelealt2': 'Élévations et altitudes du segment interverties',
    'jmelealt3': 'Élévations et altitudes de la trace interverties',
    'jmaltitudesjoin1': 'Altitudes égalisées par décalage uniforme',
    'jmaltitudesjoin2': 'Altitudes égalisées par décalage progressif',
    'jmdatetime1': 'Horodatage du point mis à jour',
    'jmdatetime2': 'Horodatages du segment mis à jour',
    'jmdatetime3': 'Horodatages de la trace mis à jour',
    'jmsave1': 'Sauvegarde en cours...',
    'jmsave2': 'Sauvegarde effectuée',
    'jmsave3': 'Échec de la sauvegarde',
    'jm3dviewer1': 'Chargement de la visionneuse 3D en cours...',
    'jm3dviewer2': 'Visionneuse 3D démarrée',
    'jm3dviewer3': 'Échec du chargement de la visionneuse 3D',
    'jtilt': 'Inclinaison:',
    'jrotation': 'Rotation:',
    'jzscale': 'Échelle Z:',
    'jzscaleiso': 'iso',
    'jzscalemax': 'max',
    'jtexture': 'Texture:',
    'jtextureyiso': 'Isoplèthes Y',
    'jtextureziso': 'Isoplèthes Z',
    'jtexturemap': 'Carte',
    'jdimming': 'Estompage:',
    'jdimmingnone': 'Sans',
    'jdimmingz': 'Altitude',
    'jdimmingdeclivity': 'Déclivité',
    'jdimmingshadow': 'Ombrage',
    'jltilt': 'Inclinaison lumière:',
    'jlrotation': 'Rotation lumière:',
    'start': 'démarrage',
    'close': 'fermeture',
  },
  'parser': {
    'uri': 'chemin d\'accès à la trace ou argument pas mentionné pour démarrer avec l\'explorateur de traces',
    'conf': 'chemin d\'accès au fichier de configuration [même répertoire que le script par défaut]',
    'trk': 'indice de la trace (commençant à 0) [0 par défaut]',
    'map': 'chemin d\'accès complet à la carte ou nom du fournisseur de carte ou vide pour utiliser le premier founisseur de carte configuré, ou option pas mentionnée pour utiliser les fournisseurs de tuiles configurés [par défaut]',
    'emap': 'chemin d\'accès complet à la carte d\'altitudes ou nom du fournisseur de carte d\'altitudes ou vide pour utiliser le premier fournisseur de carte d\'altitudes configuré, ou option pas mentionnée pour utiliser les fournisseurs de tuiles et données d\'altitudes configurés [par défaut]',
    'box': '"minlat, maxlat, minlon, maxlon" (latitudes minimale et maximale, longitudes minimale et maximale, avec les "" ) de la carte à charger / à retourner (pour l\'utilisation d\'une carte / d\'un fournisseur de carte) [lu dans les métadonnées gpxtweaker de la carte / déterminé à partir de la trace par défaut]',
    'size': '"height, width" (hauteur et largeur, avec les "") de la carte à charger / "maxheight, maxwidth" (hauteur et largeur maximales, avec les "") de la carte à retourner (pour l\'utilisation d\'une carte / d\'un fournisseur de carte) [lu dans les métadonnées gpxtweaker de la carte / "2000, 4000" par défaut]',
    'noopen': 'pas d\'ouverture automatique dans le navigateur par défaut',
    'verbosity': 'niveau de verbosité de 0 à 2 [0 par défaut]',
    'gpx': 'seuls les fichiers .gpx sont pris en charge',
    'open': 'Ouvrir l\'url %s',
    'keyboard': 'Presser "S" pour quitter',
   }
}
EN_STRINGS = {
  'tilescache': {
    '_id': 'Tiles cache',
    'init': 'initialization (size: %s, threads: %s)',
    'get': 'tile (%s, %s) requested',
    'cancel': 'tile (%s, %s) providing cancelled',
    'found': 'tile (%s, %s) found in cache at position %s',
    'del': 'deletion of position %s in cache',
    'add': 'insertion of tile (%s, %s) in cache at position %s',
    'error': 'failure of tile (%s, %s) loading',
    'load': 'tile (%s, %s) loaded',
    'configure': 'configuration (tiles set: %s, matrix: %s)',
    'ifound': 'informations found in cache (tiles set: %s, matrix: %s)',
    'fail': 'failure of configuration (tiles set: %s, matrix: %s)',
    'close': 'shutdown',
  },
  'map': {
    '_id': 'Map handler',
    'mapfetch': 'fetching of map %s',
    'maplfail': 'failure of fetching of map %s',
    'maploaded': 'map %s loaded',
    'mapsave': 'saving of map as %s',
    'mapsfail': 'failure of saving of map as %s',
    'mapsaved': 'map saved as %s',
    'tileretrieve': 'providing of tile %s',
    'tilelfound': 'tile %s found locally',
    'tilelexpired': 'local tile %s expired',
    'tilefetch': 'fetching of tile %s',
    'tilerfail': 'failure of providing of tile %s',
    'tileretrieved': 'tile %s provided',
  },
  'track': {
    '_id': 'Track manager',
    'init': 'initialization',
    'load': 'loading of track %s',
    'new': 'creation of a new track as %s',
    'lerror': 'failure of loading of track %s',
    'loaded': 'track %s loaded (name: "%s", waypoints: %s, segments: %s, points: %s)',
    'save': 'saving of track as %s',
    'serror': 'failure of saving of track under %s',
    'saved': 'track saved as %s',
  },
  'interface': {
    '_id': 'Interface',
    'conf': 'loading of configuration',
    'cerror': 'failure of loading of configuration (%s)',
    'cloaded': 'configuration loaded',
    'build': 'generation of the interface page',
    'buildexp': 'generation of the interface page of the explorer',
    'berror': 'failure of the generation of the interface page',
    'berror1': 'failure of the generation of the interface page (conversion into WebMercator)',
    'berror2': 'failure of the generation of the interface page (empty track without frame boundaries)',
    'berror3': 'failure of the generation of the interface page (map "%s" not defined)',
    'berror4': 'failure of the generation of the interface page (track overflowing with the view)',
    'berror5': 'failure of the generation of the interface page (settings of tiles sets or cache)',
    'berror6': 'track skipped because overflowing with the view',
    'elevation': 'elevations provider configured (%s)',
    'eerror': 'failure of the configuration of the elevations provider (%s)',
    'itinerary': 'itineraries provider configured (%s)',
    'built': 'interface page generated',
    'builtexp': 'interface page of the explorer generated',
    'request': 'receipt of the request %s %s',
    'response': 'response to the request %s %s sent',
    'rerror': 'failure of the response to the request %s %s',
    'rbad': 'rejection of the request %s %s (bad session identifier)',
    'rnfound': 'rejection of the request %s %s (requested resource unavailable)',
    'rfailed': 'failure response to the request %s %s sent',
    '3dbuild': 'generation of the 3D viewer page',
    '3derror1': 'failure of the generation of the 3D viewer page (retrieval of the elevations of the ground)',
    '3derror2': 'failure of the generation of the 3D viewer page (retrieval of the map of the ground)',
    '3dmodeled': 'modelization of the ground achieved (%s = %s x %s dots, source: "%s")',
    '3dbuilt': '3D viewer page generated',
    'jsession': 'A session is already active !',
    'jexpfail': 'The loading of the data has failed !',
    'jserror': 'The backup has failed: ',
    'jesconfirm': 'Replace all elevation data of the segment ?',
    'jeconfirm': 'Replace all elevation data of the track ?',
    'jeasconfirm': 'Switch the elevation and altitude data of the segment ?',
    'jeaconfirm': 'Switch the elevation and altitude data of the track ?',
    'jrconfirm': 'Reverse the whole track ?',
    'junload': 'Warning, the data will be lost !',
    'jundo': 'undo the latest action of insertion or modification of properties of points&#13;&#10;+alt: only for the focused element',
    'jredo': 'redo the latest cancelled action&#13;&#10;+alt: only for the focused element',
    'jinsertb': 'focus on segment: insert a point at the start of the segment&#13;&#10;focus on point / waypoint: duplicate the point / waypoint above&#13;&#10;no focus: insert a waypoint at the start',
    'jinserta': 'focus on segment: insert a point at the end of the segment&#13;&#10;focus on point / waypoint: duplicate the point / waypoint below&#13;&#10;no focus: insert a waypoint at the end',
    'jpath': 'draw a path towards the focused point from the previous point',
    'jelementup': 'focus on segment: move the element up (undo to restore the original timestamps)&#13;&#10;focus on point: move the focus to the current segment&#13;&#10;focus on waypoint: move the element up',
    'jelementdown': 'focus on segment: move the element down (undo to restore the original timestamps)&#13;&#10;focus on point: move the focus to the next segment&#13;&#10;focus on waypoint: move the element down',
    'jsegmentcut': 'focus on segment: duplicate the segment&#13;&#10;focus on point: split the segment above',
    'jsegmentabsorb': 'merge the focused segment with the next segment',
    'jsegmentreverse': 'focus on segment / no focus: reverse the segment / the track',
    'jelevationsadd': 'focus on segment or point / no focus: add the missing elevations to the element / the track&#13;&#10;+alt: from the altitude data',
    'jelevationsreplace': 'focus on segment or point / no focus: replace the elevations of the element / the track#13;&#10;+alt: from the altitude data&#13;&#10;+shift: switch with the altitude data',
    'jaltitudesjoin': 'focus on segment: equalize the altitude of the last point with the one of the first point of the next segment by uniform offset of the whole segment&#13;&#10;focus on point: equalize the altitude of the last point with the one of the first point of the next segment by progressive offset of the segment from the focused point',
    'jdatetime': 'focus on segment or point / no focus: complete by inter/extra polation the timestamps of the element / the track',
    'jsave': 'backup the track&#13;&#10;(then reload the page to irreversibly eliminate the disabled elements)',
    'jswitchpoints': 'show / hide the points and waypoints',
    'jgraph': 'show / hide the graph&#13;&#10;+shift: show / hide the controls of the filter of calculation of the elevation gain&#13;&#10;+ctrl: show / hide the controls of the filter of calculation of the slope&#13;&#10;+alt: show / hide the controls of the filter of calculation of the speed',
    'j3dviewer': 'open the 3D viewer',
    'jascending': 'switch the sort order of the tracks to ascending',
    'jdescending': 'switch the sort order of the tracks to descending',
    'joset': 'select the sort criterion of the tracks',
    'jsortnone': 'None',
    'jsortname': 'Name',
    'jsortfilepath': 'File path',
    'jsortduration': 'Duration',
    'jsortdistance': 'Distance',
    'jsortelegain': 'Elevation gain',
    'jsortaltgain': 'Altitude gain',
    'jsortdate': 'Date',
    'jsortproximity': 'Proximity',
    'jfolders': 'show / hide the selection panel of the folders of the tracks to list',
    'jhidetracks': 'hide the listed tracks&#13;&#10;+alt: hide the not listed tracks',
    'jshowtracks': 'show the listed tracks&#13;&#10;+alt: show the not listed tracks',
    'jedit': 'edit the track',
    'jzoomall': 'reframe on all tracks',
    'jtset': 'select the set of tiles&#13;&#10;+shift: selection of the elevations provider&#13;&#10;+ctrl: selection of the itineraries provider',
    'jeset': 'select the elevations provider&#13;&#10;+alt: selection of the set of tiles&#13;&#10;+ctrl: selection of the itineraries provider',
    'jiset': 'select the itineraries provider&#13;&#10;+alt: selection of the set of tiles&#13;&#10;+shift: selection of the elevations provider',
    'jtsetonly': 'select the set of tiles',
    'jminus': 'zoom out&#13;&#10;+ctrl: attenuate',
    'jlock': 'lock / unlock the set of tiles',
    'jplus': 'zoom in&#13;&#10;+ctrl: reaccentuate',
    'jfilterpanel1': 'Thresholds gain calcul',
    'jfilterpanel2': 'Ranges slope calcul',
    'jfilterpanel3': 'Ranges speed calcul',
    'jspduration': 'duration',
    'jsmax': 'max&nbsp;&nbsp;&nbsp;',
    'jfoldersw': 'Folders:',
    'jhelp': 'left click-drag on the map to scroll it&#13;&#10;mouse wheel on the map to scroll it vertically&#13;&#10;shift + mouse wheel on the map to scroll it horizontally&#13;&#10;ctrl + mouse wheel on the map to zoom in or out&#13;&#10;alt + mouse wheel on the map to switch to the previous or the next waypoint / point / segment&#13;&#10;click / left click-drag (+ shift / alt) on the plot of a point / waypoint to select it / move it (and delete / keep its elevation data, or failing that choose depending whether the distance is greater than 25m or not)&#13;&#10;ctrl + click / left click-drag on the plot of a point to select it / move it and build a path from the previous point to this one&#13;&#10;left click on the plot of a segment to select it&#13;&#10;right click on the map to insert a point after the focused point or a waypoint otherwise&#13;&#10;ctrl + right click on the map to insert a point after the focused point in path following mode&#13;&#10;right click on the plot of a point / waypoint / segment to delete it&#13;&#10;mouse over a button to display its legend',
    'jexphelp': 'left click-drag on the map to scroll it&#13;&#10;mouse wheel on the map to scroll it vertically&#13;&#10;shift + mouse wheel on the map to scroll it horizontally&#13;&#10;ctrl + mouse wheel on the map to zoom in or out&#13;&#10;alt + mouse wheel on the map to switch to the previous or the next track&#13;&#10;left click on the plot of a track to select it&#13;&#10;right click on the plot of a track to hide it&#13;&#10;mouse over a button to display its legend',
    'jwaypoints': 'Waypoints',
    'jpoints': 'Points',
    'jlat': 'Lat',
    'jlon': 'Lon',
    'jhor': 'Hor',
    'jname': 'Nme',
    'jele': 'Ele',
    'jalt': 'Alt',
    'jsegment': 'Segment',
    'jtracks': 'Tracks',
    'jfile': 'File',
    'jfolder': 'Fold',
    'jperiod': 'Peri',
    'jcontent': 'Cont',
    'jtrackcontent': '%s seg(s) | %s pt(s) | %s waypt(s)',
    'jgraphdistance': 'distance',
    'jgraphelevation': 'elevation',
    'jgraphaltitude': 'altitude',
    'jgraphelegain': 'ele gain',
    'jgraphaltgain': 'alt gain',
    'jgrapheleslope': 'ele slope',
    'jgraphaltslope': 'alt slope',
    'jgraphspeed': 'speed',
    'jgraphtime': 'duration',
    'jmundo1': 'Insertion of %s point(s) cancelled',
    'jmundo2': 'Modification of %s point(s) cancelled',
    'jmredo1': 'Insertion of %s point(s) restored',
    'jmredo2': 'Modification of %s point(s) restored',
    'jminsert1': 'Waypoint inserted',
    'jminsert2': 'Point inserted',
    'jmpath1': 'Retrieval of the itinerary in progress...',
    'jmpath2': 'Itinerary inserted',
    'jmpath3': 'Failure of the retrieval of the itinerary',
    'jmelementup1': 'Waypoint moved',
    'jmelementup2': 'Segment moved',
    'jmsegmentcut1': 'Segment duplicated',
    'jmsegmentcut2': 'Segment split',
    'jmsegmentabsorb': 'Segments merged',
    'jmsegmentreverse1': 'Segment reversed',
    'jmsegmentreverse2': 'Track reversed',
    'jmelevations1': 'Retrieval of elevations in progress...',
    'jmelevations2': 'Elevation of the point / waypoint updated',
    'jmelevations3': 'Elevations of the segment updated (%s point(s) out of %s)',
    'jmelevations4': 'Elevations of the track updated (%s point(s) and waypoint(s) out of %s)',
    'jmelevations5': 'Elevations of the track updated (%s point(s) out of %s)',
    'jmelevations6': 'Failure of the retrieval of elevations',
    'jmelealt1': 'Elevation and altitude of the point switched',
    'jmelealt2': 'Elevations and altitudes of the segment switched',
    'jmelealt3': 'Elevations and altitudes of the track switched',
    'jmaltitudesjoin1': 'Altitudes equalized by uniform offset',
    'jmaltitudesjoin2': 'Altitudes equalized by progressive offset',
    'jmdatetime1': 'Timestamp of the point updated',
    'jmdatetime2': 'Timestamps of the segment updated',
    'jmdatetime3': 'Timestamps of the track updated',
    'jmsave1': 'Backup in progress...',
    'jmsave2': 'Backup completed',
    'jmsave3': 'Failure of the backup',
    'jm3dviewer1': 'Loading of the 3D viewer in progress...',
    'jm3dviewer2': '3D viewer started',
    'jm3dviewer3': 'Failure of the loading of the 3D viewer',
    'jtilt': 'Tilt:',
    'jrotation': 'Rotation:',
    'jzscale': 'Z scale:',
    'jzscaleiso': 'iso',
    'jzscalemax': 'max',
    'jtexture': 'Texture:',
    'jtextureyiso': 'Y isopleths',
    'jtextureziso': 'Z isopleths',
    'jtexturemap': 'Map',
    'jdimming': 'Dimming:',
    'jdimmingnone': 'Without',
    'jdimmingz': 'Elevation',
    'jdimmingdeclivity': 'Declivity',
    'jdimmingshadow': 'Shadow',
    'jltilt': 'Light tilt:',
    'jlrotation': 'Light rotation:',
    'start': 'start-up',
    'close': 'shutdown',
  },
  'parser': {
    'uri': 'path to the track or argument not mentioned to start with the explorer of tracks',
    'conf': 'full path to the configuration file [same folder as the script by default]',
    'trk': 'index of the track (starting at 0) [0 by default]',
    'map': 'full path to the map or name of the map provider or blank to use the first map provider configured, or option not mentioned to use the tiles providers configured [by default]',
    'emap': 'path to the elevations map or name of the elevations map provider or blank to use the first elevations map configured, or option not mentioned to use the elevations tiles and data providers configured [by default]',
    'box': '"minlat, maxlat, minlon, maxlon" (minimum and maximum latitudes, minimum and maximum longitudes, with the "") of the map to be loaded / retrieved (for the use of a map / of a map provider) [read from the gpxtweaker metadata of the map / determined from the track by default]',
    'size': '"height, width" (height and width, with the "") of the map to be loaded / "maxheight, maxwidth" (maximum height and width, with the "") of the map to be retrieved (for the use of a map / of a map provider) [read from the gpxtweaker metadata of the map / "2000, 4000" by default]',
    'noopen': 'no automatic opening in the default browser',
    'verbosity': 'verbosity level from 0 to 2 [0 by default]',
    'gpx': 'only .gpx files are supported',
    'open': 'Open the url %s',
    'keyboard': 'Press "S" to exit',
   }
}
LSTRINGS = EN_STRINGS
try:
  if locale.getdefaultlocale()[0][:2].lower() == 'fr':
    LSTRINGS = FR_STRINGS
except:
  pass

VERBOSITY = 0
def log(kmod, level, kmsg, *var):
  if level <= VERBOSITY:
    now = time.localtime()
    try:
      print('%02d/%02d/%04d %02d:%02d:%02d' % (now.tm_mday, now.tm_mon, now.tm_year, now.tm_hour, now.tm_min, now.tm_sec), ':', LSTRINGS[kmod]['_id'], '->', LSTRINGS[kmod][kmsg] % var)
    except:
      print('%02d/%02d/%04d %02d:%02d:%02d' % (now.tm_mday, now.tm_mon, now.tm_year, now.tm_hour, now.tm_min, now.tm_sec), ':', kmod, '->', kmsg, var)


def _XMLGetNodeText(nodes):
  text = []
  if not isinstance(nodes, (list, tuple)):
    nodes = (nodes,)
  for node in nodes:
    if node.nodeType in (minidom.Node.TEXT_NODE, minidom.Node.CDATA_SECTION_NODE):
      text.append(childNode.data)
    elif node.hasChildNodes():
      for childNode in node.childNodes:
        if childNode.nodeType in (minidom.Node.TEXT_NODE, minidom.Node.CDATA_SECTION_NODE):
          text.append(childNode.data)
  return(''.join(text))


class HTTPMessage():

  def __init__(self, message, body=True, decode='utf-8', timeout=5, max_length=1048576):
    iter = 0
    while iter < 2:
      self.method = None
      self.path = None
      self.version = None
      self.code = None
      self.message = None
      self.headers = {}
      self.body = None
      if iter == 0:
        if self._read_message(message, body, timeout, max_length):
          iter = 2
        else:
          iter = 1
      else:
        iter = 2
    if self.body != None:
      if self.header('Content-encoding', '').lower() == 'deflate':
        self.body = zlib.decompress(self.body)
      elif self.header('Content-encoding', '').lower() == 'gzip':
        self.body = gzip.decompress(self.body)
      if decode:
        self.body = self.body.decode(decode)

  def header(self, name, default = None):
    return self.headers.get(name.upper(), default)

  def _read_headers(self, msg):
    if not msg:
      return
    a = None
    for msg_line in msg.splitlines()[:-1]:
      if not msg_line:
        return
      if not a:
        try:
          a, b, c = msg_line.strip().split(None, 2)
        except:
          try:
            a, b, c = *msg_line.strip().split(None, 2), ''
          except:
            return
      else:
        try:
          header_name, header_value = msg_line.split(':', 1)
        except:
          return
        header_name = header_name.strip().upper()
        if header_name:
          header_value = header_value.strip()
          self.headers[header_name] = header_value
        else:
          return
    if a[:4].upper() == 'HTTP':
      self.version = a.upper()
      self.code = b
      self.message = c
    else:
      self.method = a.upper()
      self.path = b
      self.version = c.upper()
    if not 'Content-Length'.upper() in self.headers and self.header('Transfer-Encoding', '').lower() != 'chunked':
      self.headers['Content-Length'.upper()] = 0
    return True

  def _read_message(self, message, body, timeout=5, max_length=1048576):
    rem_length = max_length
    if not isinstance(message, socket.socket):
      resp = message[0]
    else:
      message.settimeout(timeout)
      resp = b''
    while True:
      resp = resp.lstrip(b'\r\n')
      body_pos = resp.find(b'\r\n\r\n')
      if body_pos >= 0:
        body_pos += 4
        break
      body_pos = resp.find(b'\n\n')
      if body_pos >= 0:
        body_pos += 2
        break
      if not isinstance(message, socket.socket) or rem_length <= 0:
        return None
      bloc = None
      try:
        bloc = message.recv(min(rem_length, 1048576))
      except:
        return None
      if not bloc:
        return None
      rem_length -= len(bloc)
      resp = resp + bloc
    if not self._read_headers(resp[:body_pos].decode('ISO-8859-1')):
      return None
    if not body or self.code in ('204', '304'):
      self.body = b''
      return True
    if self.header('Transfer-Encoding', '').lower() != 'chunked':
      try:
        body_len = int(self.header('Content-Length'))
      except:
        return None
      if body_pos + body_len - len(resp) > rem_length:
        return None
    if self.header('Expect', '').lower() == '100-continue' and isinstance(message, socket.socket):
      try:
        message.sendall('HTTP/1.1 100 Continue\r\n\r\n'.encode('ISO-8859-1'))
      except:
        return None
    if self.header('Transfer-Encoding', '').lower() != 'chunked':
      while len(resp) < body_pos + body_len:
        if not isinstance(message, socket.socket):
          return None
        bloc = None
        try:
          bloc = message.recv(min(body_pos + body_len - len(resp), 1048576))
        except:
          return None
        if not bloc:
          return None
        resp = resp + bloc
      self.body = resp[body_pos:body_pos + body_len]
    else:
      buff = resp[body_pos:]
      self.body = b''
      chunk_len = -1
      while chunk_len != 0:
        chunk_pos = -1
        while chunk_pos < 0:
          buff = buff.lstrip(b'\r\n')
          chunk_pos = buff.find(b'\r\n')
          if chunk_pos >= 0:
            chunk_pos += 2
            break
          chunk_pos = buff.find(b'\n')
          if chunk_pos >= 0:
            chunk_pos += 1
            break
          if not isinstance(message, socket.socket) or rem_length <= 0:
            return None
          bloc = None
          try:
            bloc = message.recv(min(rem_length, 1048576))
          except:
            return None
          if not bloc:
            return None
          rem_length -= len(bloc)
          buff = buff + bloc
        try:
          chunk_len = int(buff[:chunk_pos].rstrip(b'\r\n'), 16)
        except:
          return None
        if chunk_pos + chunk_len - len(buff) > rem_length:
          return None
        while len(buff) < chunk_pos + chunk_len:
          if not isinstance(message, socket.socket):
            return None
          bloc = None
          try:
            bloc = message.recv(min(chunk_pos + chunk_len - len(buff), 1048576))
          except:
            return None
          if not bloc:
            return None
          rem_length -= len(bloc)
          buff = buff + bloc
        self.body = self.body + buff[chunk_pos:chunk_pos+chunk_len]
        buff = buff[chunk_pos+chunk_len:]
      buff = b'\r\n' + buff
      self.headers['Content-Length'.upper()] = len(self.body)
      while not (b'\r\n\r\n' in buff or b'\n\n' in buff):
        if not isinstance(message, socket.socket) or rem_length <= 0:
          return None
        bloc = None
        try:
          bloc = message.recv(min(rem_length, 1048576))
        except:
          return None
        if not bloc:
          return None
        rem_length -= len(bloc)
        buff = buff + bloc
    return True

def HTTPRequest(url, method=None, headers=None, data=None, timeout=30, max_length=1073741824, pconnection=None):
  if not method:
    method = 'GET' if not data else 'POST'
  redir = 0
  retry = 0
  switch_get = False
  code = '0'
  url_ = url
  close = False
  if headers == None:
    headers = {}
  for k in list(k for k in headers):
    if not headers[k]:
      del headers[k]
  if not pconnection:
    pconnection = [None]
    headers['Connection'] = 'close'
  else:
    headers['Connection'] = 'keep-alive'
  try:
    if not 'accept-encoding' in (h.lower() for h in headers):
      headers['Accept-Encoding'] = 'identity, deflate, gzip'
  except:
    pass
  msg_pat = '%s %s HTTP/1.1\r\n' \
    'Host: %s\r\n%s' \
    '\r\n'
  while True:
    try:
      url_p = urllib.parse.urlparse(url_)
      if not pconnection[0]:
        if url_p.scheme.lower() == 'http':
          pconnection[0] = socket.create_connection((url_p.netloc + ':80').split(':', 2)[:2], timeout=timeout)
        elif url_p.scheme.lower() == 'https':
          sock = socket.create_connection((url_p.netloc + ':443').split(':', 2)[:2], timeout=timeout)
          pconnection[0] = ssl.SSLContext(ssl.PROTOCOL_TLS).wrap_socket(sock, server_side=False)
        else:
          raise
      try:
        msg = msg_pat % ('GET' if switch_get else method, url_[len(url_p.scheme) + 3 + len(url_p.netloc):].replace(' ', '%20'), url_p.netloc, ''.join(k + ': ' + v + '\r\n' for k, v in headers.items()))
        pconnection[0].sendall(msg.encode('iso-8859-1') + ((data or b'') if not switch_get else b''))
      except:
        try:
          pconnection[0].close()
        except:
          pass
        pconnection[0] = None
        if retry:
          raise
        retry = 1
        continue
      resp = HTTPMessage(pconnection[0], body=(method.upper() != 'HEAD'), decode=None, timeout=timeout, max_length=max_length)
      if not resp.code:
        if retry:
          raise
        retry = 1
        try:
          pconnection[0].close()
        except:
          pass
        pconnection[0] = None
        continue
      retry = 0
      code = resp.code
      if code[:2] == '30' and code != '304':
        try:
          pconnection[0].close()
        except:
          pass
        pconnection[0] = None
        if resp.header('location', '') != '':
          url_ = resp.header('location')
          redir += 1
          if code == '303':
            switch_get = True
        else:
          raise
        if redir > 5:
          raise
      else:
        break
    except:
      try:
        pconnection[0].close()
      except:
        pass
      pconnection[0] = None
      return None
  if headers['Connection'] == 'close' or resp.header('Connection', '').lower() == 'close' or ((resp.version or '').upper() != 'HTTP/1.1' and resp.header('Connection', '').lower() != 'keep-alive'):
    try:
      pconnection[0].close()
    except:
      pass
    pconnection[0] = None
  if code[:2] != '20' and code != '304':
    resp = None
  return resp


class WGS84WebMercator():

  R = 6378137.0
  
  @staticmethod
  def WGS84toWebMercator(lat, lon):
    return (math.radians(lon) * WGS84WebMercator.R, math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * WGS84WebMercator.R)

  @staticmethod
  def WebMercatortoWGS84(x, y):
    return (math.degrees(2 * math.atan(math.exp(y / WGS84WebMercator.R)) - math.pi / 2), math.degrees(x / WGS84WebMercator.R))


class TilesCache():

  def __init__(self, size, threads):
    self.Size = size
    self.Threads = threads
    self.InfosBuffer = []
    self.Buffer = []
    self.BLock = threading.RLock()
    self.Generators = []
    self.GCondition = threading.Condition()
    self.Id = None
    self.Infos = None
    self.Closed = False
    self.log = partial(log, 'tilescache')
    self.log(2, 'init', size, threads)

  def _getitem(self, pos):
    try:
      row, col = pos
    except:
      return None
    if not self.Infos or not self.Generators or self.Closed:
      self.log(2, 'cancel', row, col)
      return None
    with self.BLock:
      infos = {**self.Infos, 'row': row, 'col': col}
    def _retrieveitem():
      nonlocal ptile
      nonlocal e
      with self.GCondition:
        if infos != {**(self.Infos or {}), 'row': row, 'col': col}:
          ptile[0] = None
          e.set()
          self.log(2, 'cancel', row, col)
          return
        tgen = None
        while not tgen:
          if self.Closed:
            ptile[0] = None
            e.set()
            self.log(2, 'cancel', row, col)
            return
          for g in self.Generators:
            if g[0]:
              tgen = g
              break
          if not tgen:
            self.GCondition.wait()
        if infos == {**(self.Infos or {}), 'row': row, 'col': col}:
          tgen[0] = False
      if infos == {**(self.Infos or {}), 'row': row, 'col': col} and not tgen[0]:
        try:
          inf, tile = tgen[1](None, None, row, col).values()
          if inf != {**(self.Infos or {}), 'row': row, 'col': col}:
            tgen[1](close_connection=True)
            tile = None
            self.log(2, 'cancel', row, col)
          elif tile == None:
            self.log(1, 'error', row, col)
          else:
            self.log(2, 'load', row, col)
        except:
          tile = None
          self.log(1, 'error', row, col)
        finally:
          with self.GCondition:
            tgen[0] = True
            self.GCondition.notify()
          ptile[0] = tile
          e.set()
      else:
        ptile[0] = None
        e.set()
        self.log(2, 'cancel', row, col)
    ptile = None
    e = None
    with self.BLock:
      if self.Closed:
        self.log(2, 'cancel', row, col)
        return None
      i = 0
      while i < len(self.Buffer):
        if self.Buffer[i][0] == infos:
          if not self.Buffer[i][1][0]:
            del self.Buffer[i]
            self.log(2, 'del', i)
          else:
            ptile = self.Buffer[i][1]
            del self.Buffer[i]
            self[pos] = ptile
            self.log(2, 'found', row, col, i)
            break
        else:
          i += 1
      if not ptile:
        e = threading.Event()
        ptile = [e]
        self[pos] = ptile
        self.log(2, 'add', row, col, len(self.Buffer) - 1)
    if e:
      t = threading.Thread(target=_retrieveitem, daemon=True)
      t.start()
    return ptile

  def WaitTile(self, ptile, timeout=None):
    if ptile == None:
      return None
    tile = ptile[0]
    if isinstance(tile, threading.Event):
      if self.Closed:
        return None
      tile.wait(timeout)
      if self.Closed:
        return None
      tile = ptile[0]
      if isinstance(tile, threading.Event):
        return None
      else:
        return tile
    else:
      return tile

  def __getitem__(self, pos):
    try:
      row, col = pos
    except:
      return partial(self.WaitTile, None)
    self.log(2, 'get', row, col)
    def _get_diag():
      if not self.Closed:
        self.WaitTile(self._getitem((row + 1, col + 1)))
    if self.Size >= 10:
      t = threading.Timer(0.01, _get_diag)
      t.daemon = True
      t.start()
    return partial(self.WaitTile, self._getitem(pos))

  def __setitem__(self, pos, pvalue):
    try:
      row, col = pos
      infos = {**self.Infos, 'row': row, 'col': col}
      with self.BLock:
        self.Buffer.append((infos, pvalue))
        if len(self.Buffer) > self.Size:
          del self.Buffer[0]
    except:
      return

  def Configure(self, id, tile_generator_builder):
    if self.Closed or not id:
      return False
    self.log(1, 'configure', id[0], id[1])
    pconnections = list([None] for i in range(self.Threads))
    with self.GCondition:
      ind = 0
      for g in self.Generators:
        try:
          if (self.Id or (None, None))[0] == id[0] and g[0]:
            pconnections[ind] = g[1](close_connection=None)
          else:
            g[1](close_connection=True)
        except:
          pass
        ind += 1
      infos = {}
      ifound = False
      try:
        for id_inf in self.InfosBuffer:
          if id_inf[0] == id:
            infos = id_inf[1]
            ifound = True
            self.log(2, 'ifound', id[0], id[1])
            break
        gens = tile_generator_builder(number=self.Threads, infos_completed=infos, pconnections=pconnections)
        if not gens:
          raise
        self.Generators = list([True, g] for g in gens)
        self.Infos = infos
        self.Id = id
        if not ifound:
          self.InfosBuffer.append((id, infos))
        self.GCondition.notify_all()
      except:
        self.Infos = None
        self.GCondition.notify_all()
        self.log(0, 'fail', id[0], id[1])
        return False
    return True

  def Close(self):
    self.Closed = True
    with self.BLock:
      for infos, ptile in self.Buffer:
        try:
          ptile[0].set()
        except:
          pass
    with self.GCondition:
      self.GCondition.notify_all()
    try:
      for g in self.Generators:
        g[1](close_connection=True)
    except:
      pass
    self.log(1, 'close')


class WebMercatorMap(WGS84WebMercator):

  CRS = 'EPSG:3857'
  CRS_MPU = 1
  LOCALSTORE_DEFAULT_PATTERN = '{alias|layer}\{matrix}\{row:0>}\{alias|layer}-{matrix}-{row:0>}-{col:0>}.{ext}'
  LOCALSTORE_HGT_DEFAULT_PATTERN = '{alias|layer}\{hgt}.{ext}'
  WMS_PATTERN = {'GetCapabilities': '{source}?SERVICE=WMS&REQUEST=GetCapabilities', 'GetMap': '{source}?SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0&LAYERS={layers}&FORMAT={format}&STYLES={styles}&CRS={crs}&BBOX={bbox}&WIDTH={width}&HEIGHT={height}&DPI={dpi}'}
  WMS_BBOX = '{minx},{miny},{maxx},{maxy}'
  WMS_IGN_SOURCE = 'https://wxs.ign.fr/{key}/geoportail/r/wms'
  MS_IGN_PLANV2 = {'alias': 'IGN_PLANV2', 'source': WMS_IGN_SOURCE, 'layers':'GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2', 'format': 'image/png', 'styles': ''}
  MS_IGN_SCANEXPRESS = {'alias': 'IGN_PLANV2', 'source': WMS_IGN_SOURCE, 'layers':'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.CLASSIQUE', 'format': 'image/png', 'styles': ''}
  MS_IGN_SCAN25 = {'alias': 'IGN_SCAN25', 'source': WMS_IGN_SOURCE, 'layers':'SCAN25TOUR_PYR-PNG_FXX_LAMB93', 'format': 'image/png', 'styles': ''} #SCAN25TOUR_PYR-JPEG_WLD_WM
  MS_IGN_SCAN100 = {'alias': 'IGN_SCAN100', 'source': WMS_IGN_SOURCE, 'layers':'SCAN100_PYR-PNG_FXX_LAMB93', 'format': 'image/png', 'styles': ''} #SCAN100_PYR-JPEG_WLD_WM
  MS_IGN_CARTES = {'alias': 'IGN_CARTES', 'source': WMS_IGN_SOURCE, 'layers':'GEOGRAPHICALGRIDSYSTEMS.MAPS', 'format': 'image/png', 'styles': ''}
  MS_IGN_RGEALTI = {'alias': 'IGN_RGEALTI', 'source': WMS_IGN_SOURCE, 'layers':'ELEVATION.ELEVATIONGRIDCOVERAGE.HIGHRES', 'format': 'image/x-bil;bits=32', 'styles': '', 'nodata': -99999}
  WMS_OSM_SOURCE = 'https://ows.terrestris.de/osm/service'
  MS_OSM = {'alias': 'OSM', 'source': WMS_OSM_SOURCE, 'layers':'OSM-WMS', 'format': 'image/png', 'styles': ''}
  WMTS_PATTERN = {'GetCapabilities': '{source}?SERVICE=WMTS&REQUEST=GetCapabilities', 'GetTile': '{source}?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER={layer}&STYLE={style}&FORMAT={format}&TILEMATRIXSET={matrixset}&TILEMATRIX={matrix}&TILEROW={row}&TILECOL={col}'}
  WMTS_IGN_SOURCE = 'https://wxs.ign.fr/{key}/wmts'
  TS_IGN_PLANV2 = {'alias': 'IGN_PLANV2', 'source': WMTS_IGN_SOURCE, 'layer': 'GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2', 'matrixset': 'PM', 'style': 'normal'}
  TS_IGN_CARTES = {'alias': 'IGN_CARTES', 'source': WMTS_IGN_SOURCE, 'layer': 'GEOGRAPHICALGRIDSYSTEMS.MAPS', 'matrixset': 'PM', 'style': 'normal', 'format': 'image/jpeg'}  #SCAN 1000: 9-10 SCAN Régional: 11-12 SCAN 100: 13-14 - SCAN25: 15-16 - SCAN EXPRESS: 17-18
  TS_IGN_PHOTOS = {'alias': 'IGN_PHOTOS', 'source': WMTS_IGN_SOURCE, 'layer': 'ORTHOIMAGERY.ORTHOPHOTOS', 'matrixset': 'PM', 'style': 'normal', 'format': 'image/jpeg'}
  TS_OSM_SOURCE = 'https://a.tile.openstreetmap.org'
  TS_OSM = {'alias': 'OSM', 'pattern': TS_OSM_SOURCE + '/{matrix}/{col}/{row}.png', 'layer':'OSM', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_GOOGLE_SOURCE = 'https://mts1.google.com/vt'
  TS_GOOGLE_MAP = {'alias': 'GOOGLE_MAP', 'pattern': TS_GOOGLE_SOURCE + '/lyrs=m&x={col}&y={row}&z={matrix}', 'layer':'GOOGLE.MAP', 'format': 'image/png', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_GOOGLE_HYBRID = {'alias': 'GOOGLE_HYBRID', 'pattern': TS_GOOGLE_SOURCE + '/lyrs=y&x={col}&y={row}&z={matrix}', 'layer':'GOOGLE.MAP', 'format': 'image/png', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_GOOGLE_TERRAIN = {'alias': 'GOOGLE_TERRAIN', 'pattern': TS_GOOGLE_SOURCE + '/lyrs=p&x={col}&y={row}&z={matrix}', 'layer':'GOOGLE.MAP', 'format': 'image/png', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_BING_SOURCE = 'https://ecn.t0.tiles.virtualearth.net'
  TS_BING_MAP = {'alias': 'BING_MAP', 'pattern': TS_BING_SOURCE + '/tiles/r{quadkey}.png?g=1', 'layer':'BING.MAP', 'format': 'image/png', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_BING_HYBRID = {'alias': 'BING_HYBRID', 'pattern': TS_BING_SOURCE + '/tiles/h{quadkey}.png?g=1', 'layer':'BING.MAP', 'format': 'image/png', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}

  def __init__(self, tiles_buffer_size=None, tiles_max_threads=None):
    self.Map = None
    self.MapInfos = {}
    self.MapResolution = None
    if not tiles_buffer_size or not tiles_max_threads:
      self.Tiles = None
    else:
      self.Tiles = TilesCache(tiles_buffer_size, tiles_max_threads)
    self.TilesInfos = None
    self.log = partial(log, 'map')

  @classmethod
  def MSAlias(cls, name):
    if hasattr(cls, 'MS_' + name):
      return dict(getattr(cls, 'MS_' + name))
    else:
      return None

  @staticmethod
  def WGS84toCoord(lat, lon):
    try:
      x, y = WebMercatorMap.WGS84toWebMercator(lat, lon)
    except:
      return None
    return (x, y)

  def FetchMap(self, infos, minlat, maxlat, minlon, maxlon, maxheight, maxwidth, dpi=None, key=None, referer=None, user_agent='GPXTweaker'):
    self.log(2, 'mapfetch', infos)
    headers = {}
    if referer:
      headers['Referer'] = referer
    headers['User-Agent'] = user_agent
    if '' in map(lambda k: infos.get(k) or '', ('source', 'layers')):
      self.log(0, 'maplfail', infos)
      return False
    if key:
      try:
        infos['source'] = infos['source'].format_map({'key': key})
      except:
        pass
    infos['format'] = infos.get('format') or 'image/png'
    infos['styles'] = infos.get('styles') or ''
    infos['crs'] = self.CRS
    try:
      minx, miny = self.WGS84toCoord(minlat, minlon)
      maxx, maxy = self.WGS84toCoord(maxlat, maxlon)
      if not hasattr(self, 'WMS_BBOX'):
        infos['bbox'] = '%s,%s,%s,%s' % (minx, miny, maxx, maxy)
      else:
        infos['bbox'] = self.WMS_BBOX.format_map({'minx': minx, 'miny': miny, 'maxx': maxx, 'maxy': maxy})
      lenx = (maxx - minx)
      leny = (maxy - miny)
      resolution = max(lenx / maxwidth, leny / maxheight)
      infos['width'] = round(lenx / resolution)
      infos['height'] = round(leny / resolution)
      infos['dpi'] = dpi or max(1, 185 / resolution / self.CRS_MPU)
    except:
      self.log(0, 'maplfail', infos)
      return False
    try:
      uri = self.WMS_PATTERN['GetMap'].format_map(infos)
      rep = HTTPRequest(uri, 'GET', headers)
      nmap = rep.body
    except:
      self.log(0, 'maplfail', infos)
      return False
    if nmap:
      self.Map = nmap
      self.MapInfos = infos
      self.MapResolution = resolution
    else:
      self.log(0, 'maplfail', infos)
      return False
    self.log(1, 'maploaded', infos)
    return True

  def LoadMap(self, uri, minx=None, miny=None, maxx=None, maxy=None, resolution=None, referer=None, user_agent='GPXTweaker'):
    self.log(2, 'mapfetch', uri)
    try:
      if '://' in uri:
        headers = {'User-Agent': user_agent}
        if referer:
          headers['Referer'] = referer
        rep = HTTPRequest(uri, 'GET', headers)
        nmap = rep.body
      else:
        try:
          f = open(uri, 'rb')
        except:
          f = open(uri + '.xz', 'rb')
        nmap = f.read()
        f.close()
    except:
      self.log(0, 'maplfail', uri)
      return False
    if not nmap:
      self.log(0, 'maplfail', uri)
      return False
    if nmap[:6] == b'\xfd\x37\x7a\x58\x5a\x00':
      try:
        dec = lzma.LZMADecompressor(format=lzma.FORMAT_XZ)
        dmap = dec.decompress(nmap)
        while not dec.eof:
          dmap = dmap + dec.decompress(nmap)
        imap = dec.unused_data
      except:
        self.log(0, 'maplfail', uri)
        return False
    if minx and miny and maxx and maxy and resolution:
      infos = {'width': round((maxx - minx) / resolution), 'height': round((maxy - miny) / resolution), 'crs': self.CRS}
      if not hasattr(self, 'WMS_BBOX'):
        infos['bbox'] = '%s,%s,%s,%s' % (minx, miny, maxx, maxy)
      else:
        infos['bbox'] = self.WMS_BBOX.format_map({'minx': minx, 'miny': miny, 'maxx': maxx, 'maxy': maxy})
      if nmap[:6] == b'\xfd\x37\x7a\x58\x5a\x00':
        nmap = dmap
      infos['crs'] = self.CRS
      infos['format'] = {'jpg': 'image/jpeg', 'png': 'image/png', 'bil': 'image/x-bil;bits=32', 'hgt': 'image/hgt'}.get(uri.replace('.xz', '').rsplit('.', 1)[-1][0:3], 'image')
    else:
      try:
        if nmap[:4] == b'\x89PNG':
          cpos = nmap.rfind(b'tEXtComment\0GPXTweaker: ')
          if cpos >= 0:
            infos = json.loads(nmap[cpos+24:cpos+4+int.from_bytes(nmap[cpos-4:cpos], 'big')])
          else:
            raise
        elif nmap[:2] == b'\xff\xd8':
          cpos = nmap.rfind(b'GPXTweaker: ')
          if cpos >= 0:
            infos = json.loads(nmap[cpos+12:cpos-2+int.from_bytes(nmap[cpos-2:cpos], 'big')])
          else:
            raise
        elif nmap[:6] == b'\xfd\x37\x7a\x58\x5a\x00':
          nmap = dmap
          infos = json.loads(imap)
        if infos['crs'] != self.CRS:
          raise
        if not hasattr(self, 'WMS_BBOX'):
          bbox = dict(zip(('{minx}', '{miny}', '{maxx}', '{maxy}'), infos['bbox'].split(',')))
        else:
          bbox = dict(zip(self.WMS_BBOX.split(','), infos['bbox'].split(',')))
        resolution = (float(bbox['{maxx}']) - float(bbox['{minx}'])) / infos['width']
      except:
        self.log(0, 'maplfail', uri)
        return False
    self.Map = nmap
    self.MapInfos = infos
    self.MapResolution = resolution
    self.log(1, 'maploaded', uri)
    return True

  def SaveMap(self, uri):
    self.log(2, 'mapsave', uri)
    try:
      if not self.MapInfos or (None in self.MapInfos.values()) or not self.Map:
        self.log(0, 'mapsfail', uri)
        return False
      if self.Map[:4] == b'\x89PNG':
        f = open(uri, 'wb')
        cpos = self.Map.rfind(b'tEXtComment\0GPXTweaker: ')
        while cpos >= 0:
          self.Map = self.Map[:cpos-4] + self.Map[cpos+8+int.from_bytes(self.Map[cpos-4:cpos], 'big'):]
          cpos = self.Map.rfind(b'tEXtComment\0GPXTweaker: ')
        f.write(self.Map[:-12])
        comment = ('Comment\0GPXTweaker: ' + json.dumps(self.MapInfos)).encode('ISO-8859-1')
        f.write(len(comment).to_bytes(4, 'big') + b'tEXt' + comment + zlib.crc32(b'tEXt'+ comment).to_bytes(4,'big'))
        f.write(self.Map[-12:])
      elif self.Map[:2] == b'\xff\xd8':
        f = open(uri, 'wb')
        cpos = self.Map.rfind(b'GPXTweaker: ')
        while cpos >= 0:
          self.Map = self.Map[:cpos-4] + self.Map[cpos-2+int.from_bytes(self.Map[cpos-2:cpos], 'big'):]
          cpos = self.Map.rfind(b'GPXTweaker: ')
        f.write(self.Map[:-2])
        comment = ('GPXTweaker: ' + json.dumps(self.MapInfos)).encode('ISO-8859-1')
        f.write(b'\xff\xfe' + (len(comment) + 2).to_bytes(2, 'big') + comment)
        f.write(self.Map[-2:])
      elif self.MapInfos['format'] == 'image/x-bil;bits=32' or self.MapInfos['format'] == 'image/hgt':
        if uri[-3:].lower() != '.xz':
          uri = uri + '.xz'
        f = open(uri, 'wb')
        cmap = lzma.compress(self.Map, format=lzma.FORMAT_XZ, filters=({'id': lzma.FILTER_DELTA, 'dist': (4 if self.MapInfos['format'] == 'image/x-bil;bits=32' else 2)}, {'id': lzma.FILTER_LZMA2, 'preset': 4}))
        f.write(cmap)
        f.write(json.dumps(self.MapInfos).encode('ISO-8859-1'))
      else:
        f = open(uri, 'wb')
        f.write(self.Map)
      f.close()
    except:
      try:
        f.close()
      except:
        pass
      self.log(0, 'mapsfail', uri)
      return False
    self.log(1, 'mapsaved', uri)
    return True

  @classmethod
  def TSAlias(cls, name):
    if hasattr(cls, 'TS_' + name):
      return dict(getattr(cls, 'TS_' + name))
    else:
      return None
      
  @classmethod
  def WGS84toTile(cls, infos, lat, lon):
    try:
      x, y = cls.WGS84toCoord(lat, lon)
      col = int((x - infos['topx']) * cls.CRS_MPU / infos['width'] / infos['scale'])
      row = int((infos['topy'] - y) * cls.CRS_MPU / infos['height'] / infos['scale'])
    except:
      return None
    return (row, col)

  @classmethod
  def WGS84BoxtoTileBox(cls, infos, minlat, maxlat, minlon, maxlon):
    try:
      row1, col1 = cls.WGS84toTile(infos, minlat, minlon)
      row2, col2 = cls.WGS84toTile(infos, maxlat, maxlon)
    except:
      return None
    if col1 > col2 or row1 < row2:
      return None
    return ((row2, col1), (row1, col2))

  def GetTileInfos(self, infos, matrix=None, lat=None, lon=None, key=None, referer=None, user_agent='GPXTweaker', pconnection=None):
    if matrix != None:
      infos['matrix'] = str(matrix)
    if '{hgt}' in infos.get('pattern', ''):
      infos['matrix'] = '0'
    if not 'matrix' in infos:
      return False
    if 'pattern' in infos:
      infos['format'] = infos.get('format') or {'jpg': 'image/jpeg', 'png': 'image/png', 'bil': 'image/x-bil;bits=32', 'hgt': 'image/hgt'}.get(infos['pattern'].replace('.zip', '').rsplit('.', 1)[-1][0:3], 'image')
      try:
        infos['scale'] = infos['basescale'] / (2 ** int(infos['matrix']))
        if lat != None and lon !=None :
          infos['row'], infos['col'] = self.WGS84toTile(infos, lat, lon)
      except:
        return False
      return True
    headers = {'User-Agent': user_agent}
    if referer:
      headers['Referer'] = referer
    if '' in map(lambda k: infos.get(k) or '', ('source', 'layer', 'matrixset')):
      return False
    if key:
      try:
        infos['source'] = infos['source'].format_map({'key': key})
      except:
        pass
    infos['style'] = infos.get('style') or ''
    infos['format'] = infos.get('format') or 'image/png'
    uri = self.WMTS_PATTERN['GetCapabilities'].format_map(infos)
    rep = HTTPRequest(uri, 'GET', headers, pconnection=pconnection)
    if rep.code != '200':
      return False
    try:
      cap = minidom.parseString(rep.body)
      content = cap.getElementsByTagNameNS('*', 'Contents')[0]
      layers = content.getElementsByTagNameNS('*', 'Layer')
      matrixset = None
      for node in content.childNodes:
        if node.localName == 'TileMatrixSet':
          for c_node in node.childNodes:
            if c_node.localName == 'Identifier':
              if _XMLGetNodeText(c_node) == infos['matrixset']:
                matrixset = node
                break
        if matrixset:
          break
      infos['scale'] = None
      infos['topx'] = None
      infos['topy'] = None
      infos['width'] = None
      infos['height'] = None
      for node in matrixset.getElementsByTagNameNS('*', 'TileMatrix'):
        if _XMLGetNodeText(node.getElementsByTagNameNS('*', 'Identifier')) == infos['matrix']:
          infos['scale'] = float(_XMLGetNodeText(node.getElementsByTagNameNS('*', 'ScaleDenominator'))) * 0.28 / 1000
          infos['topx'], infos['topy'] = list(map(float, _XMLGetNodeText(node.getElementsByTagNameNS('*', 'TopLeftCorner')).split()))
          infos['width'] = int(_XMLGetNodeText(node.getElementsByTagNameNS('*', 'TileWidth')))
          infos['height'] = int(_XMLGetNodeText(node.getElementsByTagNameNS('*', 'TileHeight')))
    except:
      return False
    finally:
      try:
        cap.unlink()
      except:
        pass
    if '' in map(lambda k: infos.get(k) or '', ('scale', 'topx', 'topy', 'width', 'height')):
      return False
    if lat != None and lon !=None :
      try:
        infos['row'], infos['col'] = self.WGS84toTile(infos, lat, lon)
      except:
        return False
    return True

  def GetKnownTile(self, infos, key=None, referer=None, user_agent='GPXTweaker', pconnection=None):
    headers = {'User-Agent': user_agent}
    if referer:
      headers['Referer'] = referer
    try:
      if 'pattern' in infos:
        if '{quadkey}' in infos['pattern']:
          quadkey = ''.join(map(lambda p: str(int(p[0]+p[1], 2)), zip(bin(int(infos['row']))[2:].rjust(int(infos['matrix']), '0'), bin(int(infos['col']))[2:].rjust(int(infos['matrix']), '0'))))
        else:
          quadkey = ''
        if '{hgt}' in infos['pattern']:
          lat = 89 - infos['row']
          lon = infos['col'] - 180
          hgt = ("N" if lat >= 0 else "S") + ('%02i' % abs(lat)) + ("E" if lon >= 0 else "O") + ('%03i' % abs(lon))
        else:
          hgt = ''
        if key:
            uri = infos['pattern'].format_map({**infos, 'key': key, 'quadkey': quadkey, 'hgt': hgt})
        else:
            uri = infos['pattern'].format_map({**infos, 'quadkey': quadkey, 'hgt': hgt})
      else:
        uri = self.WMTS_PATTERN['GetTile'].format_map(infos)
        if key:
          try:
            uri = uri.format_map({'key': key})
          except:
            pass
    except:
      return None
    try:
      rep = HTTPRequest(uri, 'GET', headers, pconnection=pconnection)
      if rep.code != '200':
        return None
      if 'zip' in rep.header('content-type', '').lower() or infos.get('pattern', '').lower().rsplit('.', 1)[-1][0:3] == 'zip':
        try:
          zf = zipfile.ZipFile(BytesIO(rep.body), 'r')
          tile = zf.read(zf.namelist()[0])
          zf.close()
        except:
          tile = rep.body
      else:
        tile = rep.body
    except:
      return None
    return tile

  def GetTile(self, infos, matrix, lat, lon, key=None, referer=None, user_agent='GPXTweaker', pconnection=None):
    try:
      if not self.GetTileInfos(infos, matrix, lat, lon, key, referer, user_agent, pconnection):
        return None
      tile = self.GetKnownTile(infos, key, referer, user_agent, pconnection)
    except:
      return None
    return tile

  def _match_infos(self, pattern, infos, update_dict=False, update_json=False):
    if not '{' in pattern:
      pattern = os.path.join(pattern, (self.LOCALSTORE_DEFAULT_PATTERN if infos.get('format') != 'image/hgt' else self.LOCALSTORE_HGT_DEFAULT_PATTERN))
    infopattern = os.path.dirname(pattern)
    while '{matrix}' in os.path.dirname(infopattern) or '{hgt}' in infopattern:
      infopattern = os.path.dirname(infopattern)
    try:
      infopath = os.path.join(infopattern.format_map({**infos, **{'alias|layer': infos.get('alias') or infos.get('layer', '')}}), 'infos.json')
    except:
      return False
    if not os.path.exists(infopath):
      if update_json:
        try:
          Path(os.path.dirname(infopath)).mkdir(parents=True, exist_ok=True)
        except:
          return False
        inf = {k: v for k, v in infos.items() if not k in ('row', 'col')}
        needs_update = True
      else:
        return False
    else:
      try:
        f = open(infopath, 'rt', encoding='utf-8')
        inf = json.load(f)
        if False in (not infos.get(k, '') or infos.get(k, '') == inf.get(k, '') for k in ('layer', 'matrixset', 'style', 'format', 'matrix')):
          return False
        if 'alias' in infos and 'alias' in inf:
          if infos['alias'] != inf['alias']:
            return False
      except:
        return False
      finally:
        try:
          f.close()
        except:
          pass
      if update_dict:
        for k in inf:
          infos[k] = inf[k]
        try:
          infos['width'] = int(infos['width'])
          infos['height'] = int(infos['height'])
        except:
          return False
      needs_update = False
      if update_json:
        for k in ('alias', 'source'):
          if k in infos:
            if infos[k] != inf.get(k, ''):
              inf[k] = infos[k]
              needs_update = True
    if needs_update:
      try:
        f = open(infopath, 'wt', encoding='utf-8')
        json.dump(inf, f)
      except:
        return False
      finally:
        try:
          f.close()
        except:
          pass
    return True

  def ReadTileInfos(self, pattern, infos, matrix, lat=None, lon=None):
    if matrix != None:
      infos['matrix'] = str(matrix)
    if '{hgt}' in infos.get('pattern', ''):
      infos['matrix'] = '0'
    if not 'matrix' in infos:
      return False
    if not '{' in pattern:
      pattern = os.path.join(pattern, (self.LOCALSTORE_DEFAULT_PATTERN if infos.get('format') != 'image/hgt' else self.LOCALSTORE_HGT_DEFAULT_PATTERN))
    if not self._match_infos(pattern, infos, update_dict=True):
      return False
    try:
      if (infos.get('source') or infos.get('pattern') or '') == '':
        return False
      if '' in map(lambda k: infos.get(k) or '', ('layer', 'scale', 'topx', 'topy', 'width', 'height')):
        return False
    except:
      return False
    if lat != None and lon !=None :
      try:
        infos['row'], infos['col'] = self.WGS84toTile(infos, lat, lon)
      except:
        return False
    return True

  def ReadKnownTile(self, pattern, infos, just_lookup=False):
    try:
      if not '{' in pattern:
        pattern = os.path.join(pattern, (self.LOCALSTORE_DEFAULT_PATTERN.replace('{row:0>}', '{row:0>%s}' % len(str(int(math.pi * WGS84WebMercator.R * 2 / infos['height'] / infos['scale'])))).replace('{col:0>}', '{col:0>%s}' % len(str(int(math.pi * WGS84WebMercator.R * 2 / infos['width'] / infos['scale']))))) if infos.get('format') != 'image/hgt' else self.LOCALSTORE_HGT_DEFAULT_PATTERN)
      hgt = ''
      if infos['format'] == 'image/jpeg':
        ext = 'jpg'
      elif infos['format'] == 'image/png':
        ext = 'png'
      elif infos['format'] == 'image/x-bil;bits=32':
        ext = 'bil.xz'
      elif infos['format'] == 'image/hgt':
        ext = 'hgt.xz'
        lat = 89 - infos['row']
        lon = infos['col'] - 180
        hgt = ("N" if lat >= 0 else "S") + ('%02i' % abs(lat)) + ("E" if lon >= 0 else "O") + ('%03i' % abs(lon))
      else:
        ext = 'img'
      filepath = pattern.format_map({**infos, **{'alias|layer': infos.get('alias') or infos.get('layer', ''), 'ext': ext, 'hgt': hgt}})
      if just_lookup:
        if os.path.exists(filepath):
          return os.path.getmtime(filepath)
        elif (ext == 'bil.xz' or ext == 'hgt.xz') and os.path.exists(filepath[:-3]):
          return os.path.getmtime(filepath[:-3])
        else:
          return False
      if ext == 'bil.xz' or ext == 'hgt.xz':
        if os.path.exists(filepath):
          f = lzma.open(filepath, 'rb', format=lzma.FORMAT_XZ)
        else:
          f = open(filepath[:-3], 'rb')
      else:
        f = open(filepath, 'rb')
      tile = f.read()
    except:
      return None
    finally:
      try:
        f.close()
      except:
        pass
    return tile

  def ReadTile(self, pattern, infos, matrix, lat, lon):
    try:
      if not self.ReadTileInfos(pattern, infos, matrix, lat, lon):
        return None
      tile = self.ReadKnownTile(pattern, infos)
    except:
      return None
    return tile

  def SaveTile(self, pattern, infos, tile=None, match_json=True, just_refresh=False):
    if not '{' in pattern:
      pattern = os.path.join(pattern, (self.LOCALSTORE_DEFAULT_PATTERN.replace('{row:0>}', '{row:0>%s}' % len(str(int(math.pi * WGS84WebMercator.R * 2 / infos['height'] / infos['scale'])))).replace('{col:0>}', '{col:0>%s}' % len(str(int(math.pi * WGS84WebMercator.R * 2 / infos['width'] / infos['scale']))))) if infos.get('format') != 'image/hgt' else self.LOCALSTORE_HGT_DEFAULT_PATTERN)
    if infos['format'] == 'image/jpeg':
      ext = 'jpg'
    elif infos['format'] == 'image/png':
      ext = 'png'
    elif infos['format'] == 'image/x-bil;bits=32':
      ext = 'bil.xz'
    elif infos['format'] == 'image/hgt':
      ext = 'hgt.xz'
    else:
      ext = 'img'
    if match_json:
      if not self._match_infos(pattern, infos, update_json=True):
        return False
    if tile:
      hgt = ''
      if infos['format'] == 'image/hgt':
        lat = 89 - infos['row']
        lon = infos['col'] - 180
        hgt = ("N" if lat >= 0 else "S") + ('%02i' % abs(lat)) + ("E" if lon >= 0 else "O") + ('%03i' % abs(lon))
      try:
        filepath = pattern.format_map({**infos, **{'alias|layer': infos.get('alias') or infos.get('layer', ''),'ext': ext, 'hgt': hgt}})
        if just_refresh:
          os.utime(filepath, (time.time(),) * 2)
        else:
          Path(os.path.dirname(filepath)).mkdir(parents=True, exist_ok=True)
          if ext == 'bil.xz' or ext == 'hgt.xz':
            f = lzma.open(filepath, 'wb', format=lzma.FORMAT_XZ, filters=({'id': lzma.FILTER_DELTA, 'dist': (4 if ext == 'bil.xz' else 2)}, {'id': lzma.FILTER_LZMA2, 'preset': 4}))
          else:
            f = open(filepath, 'wb')
          f.write(tile)
      except:
        return False
      finally:
        try:
          f.close()
        except:
          pass
    return True

  @staticmethod
  def run_jpegtran(i1, i2, cmd):
    kernel32 = ctypes.WinDLL('kernel32',  use_last_error=True)
    DWORD = ctypes.wintypes.DWORD
    HANDLE = ctypes.wintypes.HANDLE
    PVOID = ctypes.c_void_p
    LPVOID = ctypes.wintypes.LPVOID
    LPCWSTR = ctypes.wintypes.LPCWSTR
    path = os.path.dirname(os.path.abspath(__file__))
    r = True
    w = True
    o = b''
    def pipe_read(p):
      nr = DWORD()
      nonlocal r
      nonlocal o
      try:
        kernel32.ConnectNamedPipe(p, LPVOID(0))
        if not r:
          return
        b = ctypes.create_string_buffer(0x100000)
        while True:
          if not kernel32.ReadFile(pipe_r, ctypes.cast(b, PVOID), DWORD(len(b)), ctypes.byref(nr), LPVOID(0)):
            r = false
          elif nr.value > 0:
            o = o + b.raw[:nr.value]
          else:
            break
        kernel32.CloseHandle(p)
      except:
        r = False
        try:
          kernel32.CloseHandle(p)
        except:
          pass
    def pipe_write(p, i):
      nw = DWORD()
      nonlocal w
      try:
        kernel32.ConnectNamedPipe(p, LPVOID(0))
        if not w:
          return
        if not kernel32.WriteFile(p, ctypes.cast(i, PVOID), DWORD(len(i)), ctypes.byref(nw), LPVOID(0)):
          w = False
        else:
          kernel32.FlushFileBuffers(p)
        kernel32.CloseHandle(p)
      except:
        w = False
        try:
          kernel32.CloseHandle(p)
        except:
          pass
    try:
      name = 'GPXTweaker' + base64.b32encode(os.urandom(10)).decode('utf-8')
      pipe_w1 = HANDLE(kernel32.CreateNamedPipeW(LPCWSTR(r'\\.\pipe\write1_' + name), DWORD(0x00000002), DWORD(0), DWORD(1), DWORD(0x100000), DWORD(0x100000), DWORD(0), HANDLE(0)))
      if i2:
        pipe_w2 = HANDLE(kernel32.CreateNamedPipeW(LPCWSTR(r'\\.\pipe\write2_' + name), DWORD(0x00000002), DWORD(0), DWORD(1), DWORD(0x100000), DWORD(0x100000), DWORD(0), HANDLE(0)))
      pipe_r = HANDLE(kernel32.CreateNamedPipeW(LPCWSTR(r'\\.\pipe\read_' + name), DWORD(0x00000001), DWORD(0), DWORD(1), DWORD(0x100000), DWORD(0x100000), DWORD(0), HANDLE(0)))
    except:
      return None
    tr = threading.Thread(target = pipe_read, args=(pipe_r,), daemon=False)
    tr.start()
    tw1 = threading.Thread(target = pipe_write, args=(pipe_w1, i1), daemon=False)
    tw1.start()
    if i2:
      tw2 = threading.Thread(target = pipe_write, args=(pipe_w2, i2), daemon=False)
      tw2.start()
    try:
      process = subprocess.Popen(r'"%s\%s"' % (path, 'jpegtran.bat'), env={**os.environ, 'command': cmd.replace('##i1##', r'\\.\pipe\write1_' + name).replace('##i2##', r'\\.\pipe\write2_' + name).replace('##o##', r'\\.\pipe\read_' + name)}, creationflags=subprocess.CREATE_NO_WINDOW, startupinfo=subprocess.STARTUPINFO(dwFlags=subprocess.STARTF_USESHOWWINDOW, wShowWindow=6))
    except:
      try:
        kernel32.CloseHandle(pipe_w1)
        kernel32.CloseHandle(pipe_w2)
        kernel32.CloseHandle(pipe_r)
      except:
        pass
      return None
    process.wait()
    r = False
    w = False
    if tr.is_alive():
      h = HANDLE(kernel32.CreateFileW(LPCWSTR(r'\\.\pipe\read_' + name), DWORD(0x40000000), DWORD(0), PVOID(0), DWORD(2), DWORD(0x00000000), HANDLE(0)))
      kernel32.CloseHandle(h)
    if tw1.is_alive():
      h = HANDLE(kernel32.CreateFileW(LPCWSTR(r'\\.\pipe\write1_' + name), DWORD(0x80000000), DWORD(0), PVOID(0), DWORD(4), DWORD(0x00000000), HANDLE(0)))
      kernel32.CloseHandle(h)
    if i2:
      if tw2.is_alive():
        h = HANDLE(kernel32.CreateFileW(LPCWSTR(r'\\.\pipe\write2_' + name), DWORD(0x80000000), DWORD(0), PVOID(0), DWORD(4), DWORD(0x00000000), HANDLE(0)))
        kernel32.CloseHandle(h)
    tr.join()
    if not o:
      return None
    else:
      return o

  def MergeTiles(self, infos, tiles):
    if infos['format'] != 'image/jpeg':
      return None
    ref_tile = None
    for c in range(len(tiles)):
      for r in range(len(tiles[0])):
        if tiles[c][r] != None:
          r0 = r
          c0 = c
          ref_tile = tiles[c][r]
          break
      if ref_tile:
        break
    if not ref_tile:
      return None
    m = self.run_jpegtran(ref_tile, None, '-crop %sx%s+0+%s ##i1## ##o##' % (infos['width'], infos['height'] * len(tiles[0]), infos['height'] * r0))
    if not m:
      return None
    cols = [m] * len(tiles)
    t = [None] * len(tiles)
    def merge_col(c):
      nonlocal cols
      for r in range(len(tiles[0])):
        if (r != r0 or c != c0) and tiles[c][r]:
          o = self.run_jpegtran(cols[c], tiles[c][r], '-drop +0+%s ##i2## ##i1## ##o##' % (infos['height'] * r))
          if o:
            cols[c] = o
    t = list(threading.Thread(target=merge_col, args = (c,)) for c in range(len(tiles)))
    for c in range(len(tiles)):
      t[c].start()
    for c in range(len(tiles)):
      t[c].join()
    m = self.run_jpegtran(cols[c0], None, '-crop %sx%s+%s+0 ##i1## ##o##' % (infos['width'] * len(tiles), infos['height'] * len(tiles[0]), infos['width'] * c0))
    for c in range(len(tiles)):
      if c != c0:
        o = self.run_jpegtran(m, cols[c], '-drop +%s+0 ##i2## ##i1## ##o##' % (infos['width'] * c))
        if o:
          m = o
    return m

  def RetrieveTile(self, infos, local_pattern, local_expiration, local_store, key, referer, user_agent, pconnection=None, action=None, only_save=False):
    self.log(2, 'tileretrieve', infos)
    tile = None
    local_tile = None
    expired = True
    if isinstance(action, list):
      if len(action) == 0:
        action.append('failed')
      else:
        action[0] = 'failed'
    last_mod = False
    try:
      if local_pattern != None:
        last_mod = self.ReadKnownTile(local_pattern, infos, just_lookup=True)
        if last_mod != False:
          self.log(2, 'tilelfound', infos)
          if only_save:
            tile = True
          else:
            tile = self.ReadKnownTile(local_pattern, infos)
          if tile:
            if local_expiration != None:
              if local_expiration > (time.time() - last_mod) / 86400:
                if isinstance(action, list):
                  action[0] = 'read_from_local'
                expired = False
              else:
                if only_save:
                  tile = self.ReadKnownTile(local_pattern, infos)
                local_tile = tile
                self.log(2, 'tilelexpired', infos)
            else:
              if isinstance(action, list):
                action[0] = 'read_from_local'
              expired = False
      if expired:
        self.log(2, 'tilefetch', infos)
        tile = self.GetKnownTile(infos, key, referer, user_agent, pconnection)
        if tile and isinstance(action, list):
          action[0] = 'read_from_server'
        if tile != None and local_pattern != None:
          if tile != local_tile:
            if local_store:
              try:
                if self.SaveTile(local_pattern, infos, tile, match_json=False):
                  if isinstance(action, list):
                    action[0] = 'written_to_local'
              except:
                pass
          elif local_store:
            self.SaveTile(local_pattern, infos, tile, match_json=False, just_refresh=True)
            if isinstance(action, list):
              action[0] = 'refreshed_on_local'
          if only_save:
            tile = True
    except:
      self.log(1, 'tilerfail', infos)
      return None
    if tile == None:
      self.log(1, 'tilerfail', infos)
    else:
      self.log(2, 'tileretrieved', infos)
    return tile

  def TileGenerator(self, infos_base, matrix, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', only_local=False, number=1, infos_completed=None, pconnections=None):
    if isinstance(pconnections, list):
      if len(pconnections) < number:
        pconnections.extend(list([None] for i in range(number - len(pconnections))))
    else:
      pconnections = list([None] for i in range(number))
    if infos_completed == None:
      infos_completed = {}
    if False in (k in infos_completed for k in ('layer',  'format', 'matrix', 'scale', 'topx', 'topy', 'width', 'height')) or (False in (k in infos_completed for k in ('source', 'matrixset', 'style')) and False in (k in infos_completed for k in ('pattern', 'basescale'))):
      infos_set = False
      for k in infos_base:
        infos_completed[k] = infos_base[k]
      try:
        if local_pattern != None:
          if self.ReadTileInfos(local_pattern, infos_completed, matrix):
            infos_set = True
          if 'source' in infos_completed and 'source' in infos_base:
            infos_completed['source'] = infos_base['source']
          if 'pattern' in infos_completed and 'pattern' in infos_base:
            infos_completed['pattern'] = infos_base['pattern']
        if not infos_set:
          if only_local:
            return None
          if not local_store:
            local_pattern = None
          if not self.GetTileInfos(infos_completed, matrix, None, None, key, referer, user_agent, pconnections[0]):
            return None
          if local_store:
            if not self.SaveTile(local_pattern, infos_completed):
              return None
      except:
        return None
    if only_local:
      if 'source' in infos_completed:
        infos_completed['source'] = ''
      if 'pattern' in infos_completed:
        infos_completed['pattern'] = ''
    linfos = list({**infos_completed} for i in range(number))
    def retrieve_tiles(a=None, b=None, c=None, d=None, just_box=False, close_connection=False, ind=0):
      nonlocal pconnections
      if close_connection == None:
        return pconnections[ind]
      if close_connection:
        try:
          pconnections[ind][0].close()
        except:
          pass
        pconnections[ind][0] = None
      if a == None and b == None and c == None and d == None:
        return {k: v for k, v in linfos[ind].items() if not k in ('row', 'col')}
      if not pconnections[ind][0]:
        pconnections[ind][0] = [None]
      if c == None or d == None:
        try:
          row, col = self.WGS84toTile(linfos[ind], a, b)
          if just_box:
            return ((row, col), (row, col))
          linfos[ind]['col'] = col
          linfos[ind]['row'] = row
          return {'infos': {**linfos[ind]}, 'tile': self.RetrieveTile(linfos[ind], local_pattern, local_expiration, local_store, key, referer, user_agent, pconnections[ind])}
        except:
          return None
      elif a == None and b == None:
        if just_box:
          return ((c, d), (c, d))
        linfos[ind]['row'] = c
        linfos[ind]['col'] = d
        try:
          return {'infos': {**linfos[ind]}, 'tile': self.RetrieveTile(linfos[ind], local_pattern, local_expiration, local_store, key, referer, user_agent, pconnections[ind])}
        except:
          return None
      else:
        try:
          (minrow, mincol), (maxrow, maxcol) = self.WGS84BoxtoTileBox(linfos[ind], a, b, c, d)
          if just_box:
            return ((minrow, mincol), (maxrow, maxcol))
          def gen_tiles():
            for linfos[ind]['col'] in range(mincol, maxcol + 1):
              for linfos[ind]['row'] in range(minrow, maxrow + 1):
                try:
                  yield {'infos': {**linfos[ind]}, 'tile': self.RetrieveTile(linfos[ind], local_pattern, local_expiration, local_store, key, referer, user_agent, pconnections[ind])}
                except:
                  yield None
          return gen_tiles()
        except:
          return None
    if number == 1:
      return retrieve_tiles
    else:
      return list(partial(retrieve_tiles, ind=i) for i in range(number))
      
  def RetrieveTiles(self, infos, matrix, minlat, maxlat, minlon, maxlon, local_pattern=None, local_expiration=None, local_store=False, memory_store=None, key=None, referer=None, user_agent='GPXTweaker', only_local=False, threads=10):
    if not local_store and memory_store == None:
      return False
    try:
      infos_set = False
      if local_pattern != None:
        inf_source = infos.get('source')
        inf_pattern = infos.get('pattern')
        if self.ReadTileInfos(local_pattern, infos, matrix):
          infos_set = True
        if 'source' in infos and inf_source:
          infos['source'] = inf_source
        if 'pattern' in infos and inf_pattern:
          infos['pattern'] = inf_pattern
      if not infos_set:
        if only_local:
          return False
        if not local_store:
          local_pattern = None
        if not self.GetTileInfos(infos, matrix, None, None, key, referer, user_agent):
          return False
        if local_store:
          if not self.SaveTile(local_pattern, infos):
            return False
    except:
      return False
    try:
      (minrow, mincol), (maxrow, maxcol) = self.WGS84BoxtoTileBox(infos, minlat, maxlat, minlon, maxlon)
    except:
      return False
    if minrow > maxrow or mincol > maxcol:
      return False
    if local_pattern:
      if not '{' in local_pattern:
        local_pattern = os.path.join(local_pattern, (self.LOCALSTORE_DEFAULT_PATTERN.replace('{row:0>}', '{row:0>%s}' % len(str(int(math.pi * WGS84WebMercator.R * 2 / infos['height'] / infos['scale'])))).replace('{col:0>}', '{col:0>%s}' % len(str(int(math.pi * WGS84WebMercator.R * 2 / infos['width'] / infos['scale']))))) if infos.get('format') != 'image/hgt' else self.LOCALSTORE_HGT_DEFAULT_PATTERN)
    if memory_store != None:
      for col in range(mincol, maxcol + 1):
        memory_store.append([None] * (maxrow + 1 - minrow))
    box = ((row, col) for col in range(mincol, maxcol + 1) for row in range(minrow, maxrow + 1))
    lock = threading.Lock()
    progress = {'box': ((minrow, mincol), (maxrow, maxcol)), 'total': (maxcol + 1 - mincol) * (maxrow +1 - minrow), 'downloaded': 0, 'skipped': 0, 'failed': 0, 'percent': '0%', 'finish_event':threading.Event(), 'process_event':threading.Event()}
    if only_local:
      infos = {**infos}
      if 'source' in infos:
        infos['source'] = ''
      if 'pattern' in infos:
        infos['pattern'] = ''
    def downloader():
      pconnection = [None]
      def update_progress(result):
        progress[result] += 1
        percent = '%2i%%' % int((progress['downloaded'] + progress['skipped'] + progress['failed']) * 100 / progress['total'])
        if progress['downloaded'] + progress['skipped'] + progress['failed'] == progress['total']:
          progress['finish_event'].set()
        if result == 'failed' or percent != progress['percent']:
          progress['percent'] = percent
          progress['process_event'].set()
      action = [None]
      while True:
        try:
          with lock:
            row, col = next(box)
          tile = self.RetrieveTile({**infos, **{'row': row, 'col': col}}, local_pattern, local_expiration, local_store, key, referer, user_agent, pconnection, action, memory_store == None)
          if memory_store != None:
            memory_store[col - mincol][row - minrow] = tile
          with lock:
            update_progress({'failed': 'failed', 'read_from_local': 'skipped', 'written_to_local': 'downloaded', 'refreshed_on_local': 'skipped', 'read_from_server': 'failed' if local_store else 'downloaded'}.get(action[0], 'failed'))
        except StopIteration:
          try:
            pconnection[0].close()
          except:
            pass
          break
        except:
          with lock:
            update_progress('failed')
          pass
    downloaders = list(threading.Thread(target=downloader) for t in range(threads))
    for downloader in downloaders:
      downloader.start()
    return progress

  def DownloadTiles(self, pattern, infos, matrix, minlat, maxlat, minlon, maxlon, expiration=None, key=None, referer=None, user_agent='GPXTweaker', threads=10):
    return self.RetrieveTiles(infos, matrix, minlat, maxlat, minlon, maxlon, local_pattern=pattern, local_expiration=expiration, local_store=True, key=key, referer=referer, user_agent=user_agent, threads=threads)

  def AssembleMap(self, infos, matrix, minlat, maxlat, minlon, maxlon, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', only_local=False, threads=10):
    tiles = []
    progress = self.RetrieveTiles(infos, matrix, minlat, maxlat, minlon, maxlon, local_pattern=local_pattern, local_expiration=local_expiration, local_store=local_store, memory_store=tiles, key=key, referer=referer, user_agent=user_agent, only_local=only_local, threads=threads)
    if not progress:
      return False
    (minrow, mincol), (maxrow, maxcol) = progress['box']
    progress['finish_event'].wait()
    map = self.MergeTiles(infos, tiles)
    if not map:
      return False
    self.Map = map
    self.MapResolution = infos['scale'] / self.CRS_MPU
    self.MapInfos = {(k + ('s' if k in ('layer', 'style') else '')): v for k, v in infos.items() if k in ('alias', 'source', 'layer', 'format', 'style', 'nodata')}
    if 'pattern' in infos:
      self.MapInfos['source'] = infos['pattern']
    self.MapInfos['crs'] = self.CRS
    minx = infos['topx'] + self.MapResolution * infos['width'] * mincol
    miny = infos['topy'] - self.MapResolution * infos['height'] * (maxrow + 1)
    maxx = infos['topx'] + self.MapResolution * infos['width'] * (maxcol + 1)
    maxy = infos['topy'] - self.MapResolution * infos['height'] * minrow
    if '{hgt}' in infos.get('pattern', ''):
      minx -= self.MapResolution / 2
      maxx += self.MapResolution / 2
      miny -= self.MapResolution / 2
      maxy += self.MapResolution / 2
    if not hasattr(self, 'WMS_BBOX'):
      self.MapInfos['bbox'] = '%s,%s,%s,%s' % (minx, miny, maxx, maxy)
    else:
      self.MapInfos['bbox'] = self.WMS_BBOX.format_map({'minx': minx, 'miny': miny, 'maxx': maxx, 'maxy': maxy})
    self.MapInfos['width'] = infos['width'] * (maxcol - mincol + 1)
    self.MapInfos['height'] = infos['height'] * (maxrow - minrow + 1)
    if '{hgt}' in infos.get('pattern', ''):
      self.MapInfos['width'] += 1
      self.MapInfos['height'] += 1
    return True

  def CoordtoPixels(self, x, y):
    tr = lambda z, s: z if z < s else z - 1
    minx, miny, maxx, maxy = map(float, self.MapInfos['bbox'].split(','))
    return (tr(int((x - minx) / self.MapResolution), round((maxx - minx) / self.MapResolution)), tr(int((maxy - y) / self.MapResolution), round((maxy - miny) / self.MapResolution)))

  def SetTilesProvider(self, id, infos_base, matrix, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', only_local=False):
    try:
      tile_generator_builder = partial(self.TileGenerator, infos_base, matrix, local_pattern=local_pattern, local_expiration=local_expiration, local_store=local_store, key=key, referer=referer, user_agent=user_agent, only_local=only_local)
      if self.TilesInfos:
        infos = {**self.TilesInfos}
      else:
        infos = None
      self.TilesInfos = {**infos_base, 'matrix': matrix}
      if not self.Tiles.Configure(id, tile_generator_builder):
        self.TilesInfos = infos
        return False
      self.TilesInfos = self.Tiles.Infos
    except:
      return False
    return True


class WGS84Map(WebMercatorMap):
  
  CRS = 'EPSG:4326'
  CRS_MPU = math.pi / 180 * WGS84WebMercator.R
  WMS_BBOX = '{miny},{minx},{maxy},{maxx}'
  TS_IGN_RGEALTI = {'alias': 'IGN_RGEALTI', 'source': WebMercatorMap.WMTS_IGN_SOURCE, 'layer': 'ELEVATION.ELEVATIONGRIDCOVERAGE.HIGHRES', 'matrixset': 'WGS84G', 'style': 'normal', 'format': 'image/x-bil;bits=32', 'nodata': -99999}

  @staticmethod
  def WGS84toCoord(lat, lon):
    return (lon, lat)


class WGS84Elevation(WGS84Map):

  AS_IGN_ALTI = {'alias': 'IGN_ALTI', 'source': 'https://wxs.ign.fr/{key}/alti/rest/elevation.json?lat={lat}&lon={lon}&zonly=true', 'separator': '|', 'key': 'elevations', 'nodata': -99999, 'limit': 200}
  TS_SRTM_SOURCE = 'http://step.esa.int/auxdata/dem'
  TS_SRTM_GL1 = {'alias': 'SRTM_GL1', 'pattern': TS_SRTM_SOURCE + '/SRTMGL1/{hgt}.SRTMGL1.hgt.zip', 'layer':'SRTM.GL1', 'basescale': WGS84Map.CRS_MPU / 3600, 'topx': -180, 'topy': 90,'width': 3600, 'height': 3600, 'format': 'image/hgt', 'nodata': -32768}

  def ElevationfromMap(self, lat, lon):
    if not self.MapInfos or not self.Map:
      return None
    if self.MapInfos['format'] != 'image/x-bil;bits=32' and self.MapInfos['format'] != 'image/hgt':
      return None
    try:
      miny, minx, maxy, maxx = list(map(float, self.MapInfos['bbox'].split(',')))
      if self.MapInfos['format'] == 'image/x-bil;bits=32':
        e_f = '<f'
        e_s = 4
      else:
        e_f = '>h'
        e_s = 2
      px = (lon - minx) * self.MapInfos['width'] / (maxx - minx)
      if px == self.MapInfos['width']:
        px = self.MapInfos['width'] - 1
      py = (maxy - lat) * self.MapInfos['height'] / (maxy - miny)
      if py == self.MapInfos['height']:
        py = self.MapInfos['height'] - 1
      if px < 0 or px >= self.MapInfos['width'] or py < 0 or py >= self.MapInfos['height']:
        return None
      pos = e_s*(int(py) * self.MapInfos['width'] + int(px))
      ele = struct.unpack(e_f, self.Map[pos:pos+e_s])[0]
      if 'nodata' in self.MapInfos:
        if ele == self.MapInfos['nodata']:
          return None
    except:
      return None
    return ele

  @classmethod
  def ElevationfromTile(cls, infos, tile, lat, lon):
    px = (lon - infos['topx']) * cls.CRS_MPU / infos['scale'] - infos['col'] * infos['width']
    py = (infos['topy'] - lat) * cls.CRS_MPU / infos['scale'] - infos['row'] * infos['height'] 
    if infos['format'] == 'image/x-bil;bits=32':
      try:
        if px < 0 or px >= infos['width'] or py < 0 or py >= infos['height']:
          return None
        pos = 4 * (int(py) * infos['width'] + int(px))
        ele = struct.unpack('<f', tile[pos:pos+4])[0]
      except:
        return None
    elif infos['format'] == 'image/hgt':
      try:
        if px < 0 or round(px) > infos['width'] or py < 0 or round(py) > infos['height']:
          return None
        pos = 2 * (round(py) * (infos['width'] + 1) + round(px))
        ele = struct.unpack('>h', tile[pos:pos+2])[0]
      except:
        return None
    else:
      return None
    if 'nodata' in infos:
      if ele == infos['nodata']:
        return None
    return ele

  def ElevationGenerator(self, infos_base=None, matrix=None, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', only_local=False):
    tgen = self.TileGenerator(infos_base, matrix, local_pattern=local_pattern, local_expiration=local_expiration, local_store=local_store, key=key, referer=referer, user_agent=user_agent, only_local=only_local)
    if not tgen:
      return None
    buf_tiles = []
    def retrieve_elevations(lat=None, lon=None, close_connection=False):
      nonlocal buf_tiles
      if close_connection:
        tgen(close_connection=True)
      if lat == None or lon == None:
        return None
      try:
        row, col = tgen(lat, lon, just_box=True)[0]
        for infos, tile in buf_tiles:
          if infos['row'] == row and infos['col'] == col:
            return self.ElevationfromTile(infos, tile, lat, lon)
        infos, tile = tgen(None, None, row, col).values()
        if infos and tile:
          buf_tiles.append((infos, tile))
          return self.ElevationfromTile(infos, tile, lat, lon)
        else:
          return None
      except:
        return None
    return retrieve_elevations

  def WGS84toElevation(self, points, infos=None, matrix=None, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', only_local=False):
    if not infos:
      if not self.MapInfos or not self.Map:
        return None
      else:
        try:
          return list(self.ElevationfromMap(lat, lon) for (lat, lon) in points)
        except:
          return None
    else:
      try:
        egen = self.ElevationGenerator(infos, matrix, local_pattern=local_pattern, local_expiration=local_expiration, local_store=local_store, key=key, referer=referer, user_agent=user_agent, only_local=only_local)
        if egen:
          return list(egen(lat, lon) for (lat, lon) in points)
        else:
          return None
      except:
        return None
      finally:
        try:
          egen(close_connection=True)
        except:
          pass

  @classmethod
  def ASAlias(cls, name):
    if hasattr(cls, 'AS_' + name):
      return dict(getattr(cls, 'AS_' + name))
    else:
      return None

  def MergeTiles(self, infos, tiles):
    if infos['format'] != 'image/x-bil;bits=32' and infos['format'] != 'image/hgt':
      return None
    if infos['format'] == 'image/x-bil;bits=32':
      mh = infos['height'] * len(tiles[0])
      mw = infos['width'] * len(tiles)
      m = bytearray(struct.pack('<f', infos.get('nodata', 0))) * (mh * mw)
      for r in range(len(tiles[0])):
        for c in range(len(tiles)):
          if tiles[c][r]:
            for l in range(infos['height']):
              pos = (r * infos['height'] + l) * mw * 4 + c * infos['width'] * 4
              m[pos: pos + infos['width'] * 4] = tiles[c][r][l * infos['width'] * 4: (l + 1) * infos['width'] * 4]
    elif infos['format'] == 'image/hgt':
      mh = infos['height'] * len(tiles[0]) + 1
      mw = infos['width'] * len(tiles) + 1
      m = bytearray(struct.pack('>h', infos.get('nodata', 0))) * (mh * mw)
      for r in range(len(tiles[0])):
        for c in range(len(tiles)):
          if tiles[c][r]:
            for l in range(infos['height'] if r < len(tiles[0]) - 1 else (infos['height'] + 1)):
              pos = (r * infos['height'] + l) * mw * 2 + c * infos['width'] * 2
              if c < len(tiles) - 1:
                m[pos: pos + infos['width'] * 2] = tiles[c][r][l * (infos['width'] + 1) * 2: ((l + 1) * (infos['width'] + 1) - 1) * 2]
              else:
                m[pos: pos + (infos['width'] + 1) * 2] = tiles[c][r][l * (infos['width'] + 1) * 2: (l + 1) * (infos['width'] + 1) * 2]
    return m

  def RequestElevation(self, infos, points, key=None, referer=None, user_agent='GPXTweaker', threads=10):
    if not isinstance(points, (list, tuple)):
      return None
    headers = {}
    if referer:
      headers['Referer'] = referer
    if user_agent:
      headers['User-Agent'] = user_agent
    if not infos.get('source'):
      return None
    is_list = True
    if not isinstance(points[0], (list, tuple)):
      is_list = False
      points = [points]
    limit = infos.get('limit', len(points))
    ele = [None] * len(points)
    ilock = threading.Lock()
    finished = threading.Event()
    posl = 0
    ind = 0
    def _request_elevation():
      nonlocal posl
      nonlocal ind
      pconnection=[None]
      while True:
        with ilock:
          if posl < len(lind):
            ind1, ind2 = lind[posl]
            posl += 1
          else:
            break
        uri = infos['source'].format_map({'key': key or '', 'lat': infos['separator'].join(str(point[0]) for point in points[ind1:ind2]), 'lon': infos['separator'].join(str(point[1]) for point in points[ind1:ind2])})
        try:
          rep = HTTPRequest(uri, 'GET', headers, pconnection=pconnection)
          if rep != None:
            if not rep.body:
              rep = None
          if rep == None:
            uri1 = infos['source'].format_map({'key': key or '', 'lat': infos['separator'].join(str(point[0]) for point in points[ind1:(ind1+ind2)//2]), 'lon': infos['separator'].join(str(point[1]) for point in points[ind1:(ind1+ind2)//2])})
            uri2 = infos['source'].format_map({'key': key or '', 'lat': infos['separator'].join(str(point[0]) for point in points[(ind1+ind2)//2:ind2]), 'lon': infos['separator'].join(str(point[1]) for point in points[(ind1+ind2)//2:ind2])})
            rep1 = HTTPRequest(uri1, 'GET', headers, pconnection=pconnection)
            rep2 = HTTPRequest(uri2, 'GET', headers, pconnection=pconnection)
            try:
              ele[ind1:(ind1+ind2)//2] = json.loads(rep1.body)[infos['key']]
            except:
              pass
            ele[(ind1+ind2)//2:ind2] = json.loads(rep2.body)[infos['key']]
          else:
            ele[ind1:ind2] = json.loads(rep.body)[infos['key']]
        except:
          pass
        with ilock:
          ind += ind2 - ind1
          if ind == len(points):
            finished.set()
    lind = list((limit * i, min(limit * (i + 1), len(points))) for i in range(1 + (len(points) - 1) // limit))
    for t in range(threads):
      th = threading.Thread(target=_request_elevation)
      th.start()
    finished.wait()
    if 'nodata' in infos:
      for i in range(len(ele)):
        if ele[i] == infos['nodata']:
          ele[i] = None
    if not is_list:
      try:
        ele = ele[0]
      except:
        return None
    return ele      

  def GenerateBil32Map(self, infos, minlat, maxlat, minlon, maxlon, nbpoints, key=None, referer=None, user_agent='GPXTweaker', threads=10):
    if nbpoints <= 1 or minlat >= maxlat or minlon >= maxlon:
      return False
    dlat = maxlat - minlat
    dlon = maxlon - minlon
    res = (dlat + dlon + math.sqrt((dlat - dlon) * (dlat - dlon) + 4 * dlat * dlon * nbpoints)) / (2 * (nbpoints - 1))
    moylat = (minlat + maxlat) / 2
    moylon = (minlon + maxlon) / 2
    if maxlat - minlat >= maxlon - minlon:
      nrow = math.floor((maxlat - minlat) / res)
      res = (maxlat - minlat) / nrow
      ncol = math.ceil((maxlon - minlon) / res)
      minlon = moylon - res * ncol / 2
      maxlon = moylon + res * ncol / 2
    else:
      ncol = math.floor((maxlon - minlon) / res)
      res = (maxlon - minlon) / ncol
      nrow = math.ceil((maxlat - minlat) / res)
      minlat = moylat - res * nrow / 2
      maxlat = moylat + res * nrow / 2
    lats = list(maxlat - (i + 0.5) * res for i in range(nrow))
    lons = list(minlon + (i + 0.5) * res for i in range(ncol))
    points = list ((lat, lon) for lat in lats for lon in lons)
    eles = self.RequestElevation(infos, points, key, referer, user_agent, threads)
    if not eles:
      return False
    self.Map = b''.join(struct.pack('<f', (ele if ele != None else infos.get('nodata', 0))) for ele in eles)
    self.MapResolution = res
    self.MapInfos = {'source': infos['source'], 'layers': '', 'styles': '', 'format': 'image/x-bil;bits=32'}
    if 'alias' in infos:
      self.MapInfos['alias'] = infos['alias']
    if 'nodata' in infos:
      self.MapInfos['nodata'] = infos['nodata']
    self.MapInfos['crs'] = self.CRS
    self.MapInfos['bbox'] = self.WMS_BBOX.format_map({'minx': minlon, 'miny': minlat, 'maxx': maxlon, 'maxy': maxlat})
    self.MapInfos['width'] = ncol
    self.MapInfos['height'] = nrow
    return True


class WGS84Itinerary(WGS84Map):

  AS_IGN_ITI = {'alias': 'IGN_ITI', 'source': 'https://itineraire.ign.fr/simple/1.0.0/route?resource=bdtopo-pgr&profile=pedestrian&optimization=shortest&start={lons},{lats}&end={lone},{late}&intermediates=&constraints={{"constraintType":"prefer","key":"importance","operator":">=","value":5}}&geometryFormat=geojson&getSteps=false&getBbox=false&crs=' + WGS84Map.CRS, 'key': ('geometry', 'coordinates')}
  AS_OSRM = {'alias': 'OSRM', 'source': 'https://router.project-osrm.org/route/v1/foot/{lons},{lats};{lone},{late}?geometries=geojson&skip_waypoints=true&steps=false&overview=full', 'key': ('routes', 0, 'geometry', 'coordinates')}

  @classmethod
  def ASAlias(cls, name):
    if hasattr(cls, 'AS_' + name):
      return dict(getattr(cls, 'AS_' + name))
    else:
      return None

  def RequestItinerary(self, infos, points, key=None, referer=None, user_agent='GPXTweaker', pconnection=None):
    if not isinstance(points, (list, tuple)):
      return None
    if len(points) != 2:
      return
    if not isinstance(points[0], (list, tuple)) or not isinstance(points[1], (list, tuple)):
      return
    if len(points[0]) != 2 or len(points[1]) != 2:
      return
    headers = {}
    if referer:
      headers['Referer'] = referer
    if user_agent:
      headers['User-Agent'] = user_agent
    if not infos.get('source'):
      return None
    uri = infos['source'].format_map({'key': key or '', 'lats': points[0][0], 'lons': points[0][1], 'late': points[1][0], 'lone': points[1][1]})
    try:
      rep = HTTPRequest(uri, 'GET', headers, pconnection=pconnection)
      if rep == None:
        return None
      if not rep.body:
        return None
      iti = json.loads(rep.body)
      for k in infos['key']:
        iti = iti[k]
      if sum(map(lambda t:(t[1]-t[0])**2, zip(WGS84WebMercator.WGS84toWebMercator(*iti[0][::-1]), WGS84WebMercator.WGS84toWebMercator(*map(float, points[0]))))) > sum(map(lambda t:(t[1]-t[0])**2, zip(WGS84WebMercator.WGS84toWebMercator(*iti[-1][::-1]), WGS84WebMercator.WGS84toWebMercator(*map(float, points[0]))))):
        iti.reverse()
      return list(map(lambda s:s[::-1], iti))
    except:
      return None


class WGS84Track(WGS84WebMercator):

  def __init__(self):
    self.OTrack = None
    self.STrack = None
    self.Track = None
    self.TrkId = None
    self.Name = None
    self.Color = None
    self.Wpts = None
    self.Pts = None
    self.WebMercatorWpts = None
    self.WebMercatorPts = None
    self.log = partial(log, 'track')
    self.log(1, 'init')

  def _XMLClean(self, node=None):
    node = node or self.Track
    if node.hasChildNodes():
      l = len(node.childNodes)
      while l > 0:
        n = node.childNodes[l - 1]
        if n.nodeType == minidom.Node.TEXT_NODE:
          if n.data.strip('\r\n ') == '':
            node.removeChild(n)
        else:
          self._XMLClean(n)
        l -= 1

  def ProcessGPX(self, mode='a'):
    flt = lambda s: float(s) if (s != None and s != '') else None
    if mode == 'a' or mode == 'w':
      wpts = self.Track.getElementsByTagNameNS('*', 'wpt')
      try:
        self.Wpts = list(zip(range(len(wpts)), ((float(pt.getAttribute('lat') or _XMLGetNodeText(pt.getElementsByTagNameNS('*', 'lat'))), float(pt.getAttribute('lon') or _XMLGetNodeText(pt.getElementsByTagNameNS('*', 'lon'))), flt(_XMLGetNodeText(pt.getElementsByTagNameNS('*', 'ele')) or pt.getAttribute('ele')), _XMLGetNodeText(pt.getElementsByTagNameNS('*', 'time')) or pt.getAttribute('time') or None, _XMLGetNodeText(pt.getElementsByTagNameNS('*', 'name')) or pt.getAttribute('name') or None) for pt in wpts)))
      except:
        return False
    try:
      trk = self.Track.getElementsByTagNameNS('*', 'trk')[self.TrkId]
    except:
      if mode != 'a' or self.TrkId > 0:
        return False
      r = self.Track.getElementsByTagNameNS('*', 'gpx')[0]
      n = self.Track.createElementNS(r.namespaceURI, r.prefix + ':trk' if r.prefix else 'trk')
      r.appendChild(n)
      trk = self.Track.getElementsByTagNameNS('*', 'trk')[self.TrkId]
    if mode == 'a' or mode == 'e':
      try:
        self.Name = _XMLGetNodeText(trk.getElementsByTagNameNS('*', 'name')[0]).replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
      except:
        self.Name = ''
      self.Color = ''
      try:
        c = trk.getElementsByTagName('mytrails:color')
        if c:
          self.Color = '#' + hex(int(_XMLGetNodeText(c[0])) % (1 << 24))[2:][-6:].rjust(6, "0").upper()
        else:
          c = trk.getElementsByTagNameNS('*', 'line')
          if c:
            c = c[0].getElementsByTagNameNS('*', 'color')
            if c:
              self.Color = '#' + hex(int(_XMLGetNodeText(c[0]), 16))[2:][-6:].rjust(6, "0").upper()
      except:
        pass
    if mode == 'a':
      pts = list(list(pt for pt in seg.getElementsByTagNameNS('*', 'trkpt')) for seg in trk.getElementsByTagNameNS('*', 'trkseg')) or [[]]
      self.Pts = []
      sn = 0
      try:
        for seg in pts:
          self.Pts.append(list(zip(range(sn, sn + len(seg)), ((float(pt.getAttribute('lat') or _XMLGetNodeText(pt.getElementsByTagNameNS('*', 'lat'))), float(pt.getAttribute('lon') or _XMLGetNodeText(pt.getElementsByTagNameNS('*', 'lon'))), flt(_XMLGetNodeText(pt.getElementsByTagNameNS('*', 'ele')) or pt.getAttribute('ele')), flt(_XMLGetNodeText(pt.getElementsByTagNameNS('*', 'ele_alt')) or pt.getAttribute('ele_alt')), _XMLGetNodeText(pt.getElementsByTagNameNS('*', 'time')) or pt.getAttribute('time') or None) for pt in seg))))
          sn += len(seg)
      except:
        return False
    return True

  def LoadGPX(self, uri, trkid=None):
    self.log(1, 'load', uri + ((' <%s>' % str(trkid)) if trkid != None else ''))
    try:
      if '://' in uri:
        rep = HTTPRequest(uri, 'GET', headers)
        track = rep.body
      else:
        try:
          f = open(uri, 'rb')
          track = f.read()
        except:
          try:
            f.close()
          except:
            if trkid:
              raise
          track = b'<?xml version="1.0" encoding="UTF-8"?><gpx version="1.1" creator="GPXTweaker" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:mytrails="http://www.frogsparks.com/mytrails" xmlns="http://www.topografix.com/GPX/1/1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"></gpx>'
          self.log(0, 'new', uri)
      self.Track = minidom.parseString(track)
      self._XMLClean()
      self.OTrack = self.Track
      self.STrack = self.Track
    except:
      self.__init__()
      self.log(0, 'lerror', uri + ((' <%s>' % str(trkid)) if trkid != None else ''))
      return False
    self.TrkId = trkid or 0
    try:
      if not self.ProcessGPX('a'):
        raise
    except:
      try:
        self.Track.unlink()
      except:
        pass
      self.__init__()
      self.log(0, 'lerror', uri + ((' <%s>' % str(trkid)) if trkid != None else ''))
      return False
    self.WebMercatorWpts = None
    self.WebMercatorPts = None
    self.log(0, 'loaded', uri + ((' <%s>' % str(trkid)) if trkid != None else ''), self.Name, len(self.Wpts), len(self.Pts), sum(len(seg) for seg in self.Pts))
    return True

  def BuildWebMercator(self):
    if self.Wpts:
      self.WebMercatorWpts = list((pt[0], WGS84Track.WGS84toWebMercator(*pt[1][0:2])) for pt in self.Wpts)
    else:
      self.WebMercatorWpts = []
    if self.Pts:
      self.WebMercatorPts = list(list((pt[0], WGS84Track.WGS84toWebMercator(*pt[1][0:2])) for pt in seg) for seg in self.Pts)
    else:
      self.WebMercatorPts = []
    return True

  def SaveGPX(self, uri):
    self.log(1, 'save', uri)
    if self.Track:
      try:
        f = open(uri, 'wb')
        f.write(self.Track.toprettyxml(indent='  ', encoding='utf-8'))
        f.close()
      except:
        try:
          f.close()
        except:
          pass
        self.log(0, 'serror', uri)
        return False
    else:
      self.log(0, 'serror', uri)
      return False
    if self.STrack != self.OTrack and self.STrack != self.Track:
      try:
        self.STrack.unlink()
      except:
        pass
    self.STrack = self.Track
    self.log(0, 'saved', uri)
    return True

  def _XMLUpdateAttribute(self, node, name, value):
    node.setAttribute(name, value)
    for n in node.getElementsByTagNameNS('*', name):
      self.Track.removeChild(n)

  def _XMLUpdateNodeText(self, model, node, name, text, def_first=False, cdata=False):
    if node.hasAttribute(name):
      node.removeAttribute(name)
    nl = node.getElementsByTagNameNS('*', name)
    no = None
    if nl:
      no = nl[0]
    for n in nl[1:] :
      node.removeChild(n)
    if text:
      if cdata:
        t = self.Track.createCDATASection(text)
      else:
        t = self.Track.createTextNode(text)
      n = self.Track.createElementNS(model.namespaceURI, model.prefix + ':' + name if model.prefix else 
name)
      n.appendChild(t)
      if no:
        node.replaceChild(n, no)
      elif def_first:
        node.insertBefore(n, node.firstChild)
      else:
        node.appendChild(n)

  def _XMLUpdateChildNodes(self, node, name, children, def_first=False):
    no = None
    i = 0
    cn = node.childNodes
    while i < len(cn):
      if cn[i].localName == name:
        if not no:
          no = cn[i]
        else:
          node.removeChild(cn[i])
          i -= 1
      i += 1
    if no:
      for n in children:
        node.insertBefore(n, no)
      node.removeChild(no)
    elif def_first:
      for n in children:
        node.insertBefore(n, node.firstChild)
    else:
      for n in children:
        node.appendChild(n)

  def UpdateGPX(self, msg):
    if self.Track != self.OTrack and self.Track != self.STrack:
      try:
        self.Track.unlink()
      except:
        pass
    self.Track = self.OTrack.cloneNode(True)
    r = self.Track.getElementsByTagNameNS('*', 'gpx')[0]
    trk = self.Track.getElementsByTagNameNS('*', 'trk')[self.TrkId]
    try:
      if not '\r\n=\r\n' in msg:
        msgp = msg.split('=', 1)
        if msgp[0][-5:] == 'color':
          if not r.hasAttribute('xmlns:mytrails'):
            r.setAttributeNS('xmls', 'xmlns:mytrails', 'http://www.frogspark.com/mytrails')
          ext = trk.getElementsByTagNameNS('*', 'extensions')
          if not ext:
            e = self.Track.createElementNS(trk.namespaceURI, trk.prefix + ':extensions' if trk.prefix else 'extensions')
            e_ = None
            trk.appendChild(e)
          else:
            e = ext[0]
            e_ = None
            for ex in ext:
              if ex.getElementsByTagName('mytrails:color'):
                e = ex
                break
            for ex in ext:
              if ex.getElementsByTagNameNS('*', 'line'):
                if ex.getElementsByTagNameNS('*', 'line')[0].getElementsByTagNameNS('*', 'color'):
                  e_ = ex
                  break
          a = self.Track.createElementNS('http://www.frogspark.com/mytrails', 'mytrails:color')
          t = self.Track.createTextNode(str(int(msgp[1].lstrip('#'), 16) - (1 << 24)))
          a.appendChild(t)
          self._XMLUpdateChildNodes(e, 'color', [a])
          if e_:
            self._XMLUpdateNodeText(*([e_.getElementsByTagNameNS('*', 'line')[0]] * 2), 'color', msgp[1].lstrip('#'))
        elif msgp[0][-4:] == 'name':
          self._XMLUpdateNodeText(trk, trk, 'name', msgp[1], def_first=True, cdata=True)
        else:
          raise
        if not self.ProcessGPX('e'):
          raise
      else:
        msgp = msg.split('=\r\n')
        nmsg = msgp[0].splitlines()
        wpmsg = msgp[1].splitlines()
        smsg = msgp[2].split('-\r\n')[1:]
        wpts = self.Track.getElementsByTagNameNS('*', 'wpt')
        pts = list(list(pt for pt in seg.getElementsByTagNameNS('*', 'trkpt')) for seg in trk.getElementsByTagNameNS('*', 'trkseg')) or [[]]
        self._XMLUpdateNodeText(trk, trk, 'name', (nmsg or [''])[0], def_first=True, cdata=True)
        wpn = []
        for wp in wpmsg:
          if '&' in wp:
            v = wp.split('&')
            if int(v[0]) < len(wpts):
              nwp = wpts[int(v[0])].cloneNode(True)
            else:
              nwp = self.Track.createElementNS(trk.namespaceURI, trk.prefix + ':wpt' if trk.prefix else 'wpt')
            self._XMLUpdateAttribute(nwp, 'lat', v[1])
            self._XMLUpdateAttribute(nwp, 'lon', v[2])
            self._XMLUpdateNodeText(trk, nwp, 'ele', v[3])
            self._XMLUpdateNodeText(trk, nwp, 'time', urllib.parse.unquote(v[4]))
            self._XMLUpdateNodeText(trk, nwp, 'name', urllib.parse.unquote(v[5]), cdata=True)
          else:
            nwp = wpts[int(wp)].cloneNode(True)
          wpn.append(nwp)
        self._XMLUpdateChildNodes(r, 'wpt', wpn, def_first=True)
        sn = []
        opts = list(pt for seg in pts for pt in seg)
        for s in smsg:
          ns = self.Track.createElementNS(trk.namespaceURI, trk.prefix + ':trkseg' if trk.prefix else 'trkseg')
          pn = []
          pmsg = s.splitlines()
          for p in pmsg:
            if '&' in p:
              v = p.split('&')
              if int(v[0]) < len(opts):
                np = opts[int(v[0])].cloneNode(True)
              else:
                np = self.Track.createElementNS(trk.namespaceURI, trk.prefix + ':trkpt' if trk.prefix else 'trkpt')
              self._XMLUpdateAttribute(np, 'lat', v[1])
              self._XMLUpdateAttribute(np, 'lon', v[2])
              self._XMLUpdateNodeText(trk, np, 'ele', v[3])
              if v[4]:
                if not r.hasAttribute('xmlns:mytrails'):
                  r.setAttributeNS('xmls', 'xmlns:mytrails', 'http://www.frogspark.com/mytrails')
                ext = np.getElementsByTagNameNS('*', 'extensions')
                if not ext:
                  e = self.Track.createElementNS(trk.namespaceURI, trk.prefix + ':extensions' if trk.prefix else 'extensions')
                  np.appendChild(e)
                else:
                  e = ext[0]
                  for ex in ext:
                    if ex.getElementsByTagNameNS('*', 'ele_alt'):
                      e = ex
                      break
                a = self.Track.createElementNS('http://www.frogspark.com/mytrails', 'mytrails:ele_alt')
                t = self.Track.createTextNode(v[4])
                a.appendChild(t)
                self._XMLUpdateChildNodes(e, 'ele_alt', [a])
              self._XMLUpdateNodeText(trk, np, 'time', urllib.parse.unquote(v[5]))
            else:
              np = opts[int(p)].cloneNode(True)
            pn.append(np)
          self._XMLUpdateChildNodes(ns, 'trkpt', pn)
          sn.append(ns)
        self._XMLUpdateChildNodes(trk, 'trkseg', sn)
        if not self.ProcessGPX('a'):
          raise
        self.WebMercatorWpts = None
        self.WebMercatorPts = None
    except:
      self.Track.unlink()
      self.Track = self.OTrack
      self.ProcessGPX('a' if '\r\n=\r\n' in msg else 'e')
      return False
    return True


class ThreadedDualStackServer(socketserver.ThreadingTCPServer):

  allow_reuse_address = True

  def server_bind(self):
    try:
      self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
    except:
      pass
    super().server_bind()
    
  def shutdown(self):
    super().shutdown()
    self.socket.close()

  def server_close(self):
    pass

class GPXTweakerRequestHandler(socketserver.StreamRequestHandler):

  def handle(self):
    with selectors.DefaultSelector() as selector:
      selector.register(self.request, selectors.EVENT_READ)
      closed = False
      while not closed:
        if self.server.__dict__['_BaseServer__shutdown_request'] or self.server.__dict__['_BaseServer__is_shut_down'].is_set():
          break
        ready = selector.select(0.5)
        if self.server.__dict__['_BaseServer__shutdown_request'] or self.server.__dict__['_BaseServer__is_shut_down'].is_set():
          break
        if not ready:
          continue
        req = HTTPMessage(self.request)
        if req.header('Connection') == 'close':
          closed = True
        if not req.method:
          closed = True
          continue
        self.server.Interface.log(2, 'request', req.method, req.path)
        if req.method == 'OPTIONS':
          resp = 'HTTP/1.1 200 OK\r\n' \
          'Content-Length: 0\r\n' \
          'Date: ' + email.utils.formatdate(time.time(), usegmt=True) + '\r\n' \
          'Server: GPXTweaker\r\n' \
          'Allow: OPTIONS, HEAD, GET, POST\r\n' \
          '\r\n'
          try:
            self.request.sendall(resp.encode('ISO-8859-1'))
            self.server.Interface.log(2, 'response', req.method, req.path)
          except:
            self.server.Interface.log(2, 'rerror', req.method, req.path)
        elif req.method in ('GET', 'HEAD'):
          resp = 'HTTP/1.1 200 OK\r\n' \
          'Content-Type: ##type##\r\n' \
          'Content-Length: ##len##\r\n' \
          'Date: ' + email.utils.formatdate(time.time(), usegmt=True) + '\r\n' \
          'Server: GPXTweaker\r\n' \
          'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
          'Access-Control-Allow-Origin: %s\r\n' \
          '\r\n' % ('http://%s:%s' % (self.server.Interface.Ip, self.server.Interface.Ports[0]))
          resp_204 = 'HTTP/1.1 204 No content\r\n' \
          'Content-Length: 0\r\n' \
          'Date: ' + email.utils.formatdate(time.time(), usegmt=True) + '\r\n' \
          'Server: GPXTweaker\r\n' \
          'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
          '\r\n'
          resp_307 = 'HTTP/1.1 307 Temporary Redirect\r\n' \
          'Content-Length: 0\r\n' \
          'Location: GPXTweaker.html\r\n' \
          'Date: ' + email.utils.formatdate(time.time(), usegmt=True) + '\r\n' \
          'Server: GPXTweaker\r\n' \
          'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
          '\r\n'
          resp_err = 'HTTP/1.1 404 File not found\r\n' \
          'Content-Length: 0\r\n' \
          'Date: ' + email.utils.formatdate(time.time(), usegmt=True) + '\r\n' \
          'Server: GPXTweaker\r\n' \
          'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
          '\r\n'
          resp_bad = 'HTTP/1.1 412 Precondition failed\r\n' \
          'Content-Length: 0\r\n' \
          'Date: ' + email.utils.formatdate(time.time(), usegmt=True) + '\r\n' \
          'Server: GPXTweaker\r\n' \
          'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
          '\r\n'
          resp_body = b''
          if req.path.lower() == '/GPXTweaker.html'.lower():
            self.server.Interface.SLock.acquire()
            self.server.Interface.SLock.release()
            if not self.server.Interface.HTML:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              continue
            if self.server.Interface.SessionId == None:
              self.server.Interface.SessionId = str(uuid.uuid5(uuid.NAMESPACE_URL, self.server.Interface.Uri + str(time.time())))
              resp_body = self.server.Interface.HTML.replace('##SESSIONSTORE##', 'sessionStorage.setItem("active", "%s");\r\n      ' % self.server.Interface.SessionStoreValue).replace('##SESSIONSTOREVALUE##', self.server.Interface.SessionStoreValue).replace('##SESSIONID##', self.server.Interface.SessionId).encode('utf-8')
            else:
              resp_body = self.server.Interface.HTML.replace('##SESSIONSTORE##', '').replace('##SESSIONSTOREVALUE##', self.server.Interface.SessionStoreValue).replace('##SESSIONID##', self.server.Interface.SessionId).encode('utf-8')
            try:
              if req.method == 'GET':
                self.request.sendall(resp.replace('##type##', 'text/html').replace('##len##', str(len(resp_body))).encode('ISO-8859-1') + resp_body)
              else:
                self.request.sendall(resp.replace('##type##', 'text/html').replace('##len##', str(len(resp_body))).encode('ISO-8859-1'))
              self.server.Interface.log(2, 'response', req.method, req.path)
            except:
              self.server.Interface.log(2, 'rerror', req.method, req.path)
          elif req.path.lower() == '/GPXExplorer.html'.lower():
            self.server.Interface.SLock.acquire()
            self.server.Interface.SLock.release()
            if self.server.Interface.HTMLExp == None:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              continue
            if self.server.Interface.HTMLExp == '':
              self.server.Interface.ExploreMode()
            self.server.Interface.HTML = None
            if not self.server.Interface.HTMLExp:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              continue
            self.server.Interface.PSessionId = None
            if self.server.Interface.SessionId == None:
              self.server.Interface.SessionId = str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time())))
              resp_body = self.server.Interface.HTMLExp.replace('##SESSIONSTORE##', 'sessionStorage.setItem("active", "%s");\r\n      ' % self.server.Interface.SessionStoreValue).replace('##SESSIONSTOREVALUE##', self.server.Interface.SessionStoreValue).replace('##SESSIONID##', self.server.Interface.SessionId).encode('utf-8')
            else:
              resp_body = self.server.Interface.HTMLExp.replace('##SESSIONSTORE##', '').replace('##SESSIONSTOREVALUE##', self.server.Interface.SessionStoreValue).replace('##SESSIONID##', self.server.Interface.SessionId).encode('utf-8')
            try:
              if req.method == 'GET':
                self.request.sendall(resp.replace('##type##', 'text/html').replace('##len##', str(len(resp_body))).encode('ISO-8859-1') + resp_body)
              else:
                self.request.sendall(resp.replace('##type##', 'text/html').replace('##len##', str(len(resp_body))).encode('ISO-8859-1'))
              self.server.Interface.log(2, 'response', req.method, req.path)
            except:
              self.server.Interface.log(2, 'rerror', req.method, req.path)
          elif req.path.lower()[:13] == '/tiles/switch':
            if not req.header('If-Match') in (self.server.Interface.SessionId, self.server.Interface.PSessionId):
              try:
                self.request.sendall(resp_bad.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rbad', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              continue
            q = urllib.parse.parse_qs(urllib.parse.urlsplit(req.path).query)
            if 'set' in q:
              try:
                resp_body = json.dumps({'tlevels': self.server.Interface.TilesSets[int(q['set'][0])][3]}).encode('utf-8')
                self.server.Interface.TilesSet = int(q['set'][0])
              except:
                try:
                  self.request.sendall(resp_err.encode('ISO-8859-1'))
                  self.server.Interface.log(2, 'rnfound', req.method, req.path)
                except:
                  self.server.Interface.log(2, 'rerror', req.method, req.path)
                continue
              try:
                if req.method == 'GET':
                  self.request.sendall(resp.replace('##type##', 'application/json').replace('##len##', str(len(resp_body))).encode('ISO-8859-1') + resp_body)
                else:
                  self.request.sendall(resp.replace('##type##', 'application/json').replace('##len##', str(len(resp_body))).encode('ISO-8859-1'))
                self.server.Interface.log(2, 'response', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
            else:
              l1 = 0
              if 'auto' in q:
                tl = self.server.Interface.TilesSets[self.server.Interface.TilesSet][3]
                l1 = tl[0]
                q['matrix'] = [str(tl[l1][0])]
                try:
                  sw, sh = map(float, q['auto'][0].split('|'))
                  l1 = 1
                  l2 = 1
                  l3 = len(tl)
                  m = None
                  while True:
                    if tl[l2][0] != m:
                      if not self.server.Interface.Map.SetTilesProvider((self.server.Interface.TilesSet, str(tl[l2][0])), self.server.Interface.TilesSets[self.server.Interface.TilesSet][1], str(tl[l2][0]), **self.server.Interface.TilesSets[self.server.Interface.TilesSet][2]):
                        l2 += 1
                        if l2 >= l3:
                          l3 = (l1 + l3) // 2
                          l2 = l3 - 1
                          if l2 <= l1:
                            break
                        continue
                      m = tl[l2][0]
                    s = self.server.Interface.Map.TilesInfos['scale'] / self.server.Interface.Map.CRS_MPU / eval(tl[l2][1])
                    if sw < s and sh < s:
                      l1 = l2
                    else:
                      l3 = l2
                    l2 = (l1 + l3) // 2
                    if l2 == l1:
                      break
                  q['matrix'] = [str(tl[l1][0])]
                except:
                  pass
              if not self.server.Interface.Map.SetTilesProvider((self.server.Interface.TilesSet, q['matrix'][0]), self.server.Interface.TilesSets[self.server.Interface.TilesSet][1], q['matrix'][0], **self.server.Interface.TilesSets[self.server.Interface.TilesSet][2]):
                try:
                  self.request.sendall(resp_err.encode('ISO-8859-1'))
                  self.server.Interface.log(2, 'rnfound', req.method, req.path)
                except:
                  self.server.Interface.log(2, 'rerror', req.method, req.path)
              else:
                try:
                  resp_body = json.dumps({**{k: self.server.Interface.Map.TilesInfos[k] for k in ('topx', 'topy', 'width', 'height')}, 'scale': self.server.Interface.Map.TilesInfos['scale'] / self.server.Interface.Map.CRS_MPU, 'ext': ('.jpg' if self.server.Interface.Map.TilesInfos.get('format') == 'image/jpeg' else ('.png' if self.server.Interface.Map.TilesInfos.get('format') == 'image/png' else '.img')), 'level': l1}).encode('utf-8')
                  if req.method == 'GET':
                    self.request.sendall(resp.replace('##type##', 'application/json').replace('##len##', str(len(resp_body))).encode('ISO-8859-1') + resp_body)
                  else:
                    self.request.sendall(resp.replace('##type##', 'application/json').replace('##len##', str(len(resp_body))).encode('ISO-8859-1'))
                  self.server.Interface.log(2, 'response', req.method, req.path)
                except:
                  self.server.Interface.log(2, 'rerror', req.method, req.path)
          elif req.path.lower()[:12] == '/tiles/tile-':
            try:
              if req.path.lower()[12:].split('?')[-1].split(',') != [str(self.server.Interface.TilesSet), str(self.server.Interface.Map.TilesInfos['matrix'])]:
                try:
                  self.request.sendall(resp_bad.encode('ISO-8859-1'))
                  self.server.Interface.log(2, 'rnfound', req.method, req.path)
                except:
                  self.server.Interface.log(2, 'rerror', req.method, req.path)
                continue
              row, col = req.path.lower()[12:].split('.')[0].split('-')
              resp_body = self.server.Interface.Map.Tiles[(int(row), int(col))](10)
            except:
              pass
            if resp_body:
              try:
                if req.method == 'GET':
                  self.request.sendall(resp.replace('##type##', self.server.Interface.Map.TilesInfos.get('format')).replace('##len##', str(len(resp_body))).encode('ISO-8859-1') + resp_body)
                else:
                  self.request.sendall(resp.replace('##type##', self.server.Interface.Map.TilesInfos.get('format')).replace('##len##', str(len(resp_body))).encode('ISO-8859-1'))
                self.server.Interface.log(2, 'response', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
            else:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
          elif req.path.lower()[:8] == '/map/map':
            resp_body = self.server.Interface.Map.Map
            if resp_body:
              try:
                if req.method == 'GET':
                  self.request.sendall(resp.replace('##type##', self.server.Interface.Map.MapInfos.get('format', 'image/*')).replace('##len##', str(len(resp_body))).encode('ISO-8859-1') + resp_body)
                else:
                  self.request.sendall(resp.replace('##type##', self.server.Interface.Map.MapInfos.get('format', 'image/*')).replace('##len##', str(len(resp_body))).encode('ISO-8859-1'))
                self.server.Interface.log(2, 'response', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
            else:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
          elif req.path.lower()[:27] == '/elevationsproviders/switch' :
            if not req.header('If-Match') in (self.server.Interface.SessionId, self.server.Interface.PSessionId):
              try:
                self.request.sendall(resp_bad.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rbad', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              continue
            q = urllib.parse.parse_qs(urllib.parse.urlsplit(req.path).query)
            try:
              self.server.Interface.ElevationProviderSel = int(q['eset'][0])
              if 'layer' in self.server.Interface.ElevationsProviders[int(q['eset'][0])][1]:
                self.server.Interface.EMode = 'tiles'
                self.server.Interface.ElevationProvider = partial(self.server.Interface.Elevation.WGS84toElevation, infos=self.server.Interface.ElevationsProviders[int(q['eset'][0])][1], matrix=self.server.Interface.ElevationsProviders[int(q['eset'][0])][1].get('matrix'), **self.server.Interface.ElevationsProviders[int(q['eset'][0])][2])
                self.server.Interface.log(1, 'elevation', self.server.Interface.ElevationsProviders[int(q['eset'][0])][0])
              else:
                self.server.Interface.EMode = "api"
                self.server.Interface.ElevationProvider = partial(self.server.Interface.Elevation.RequestElevation, self.server.Interface.ElevationsProviders[int(q['eset'][0])][1], **self.server.Interface.ElevationsProviders[int(q['eset'][0])][2])
                self.server.Interface.log(1, 'elevation', self.server.Interface.ElevationsProviders[int(q['eset'][0])][0])
            except:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              continue
            try:
              self.request.sendall(resp_204.encode('ISO-8859-1'))
              self.server.Interface.log(2, 'response', req.method, req.path)
            except:
              self.server.Interface.log(2, 'rerror', req.method, req.path)
          elif req.path.lower()[:28] == '/itinerariesproviders/switch' :
            if not req.header('If-Match') in (self.server.Interface.SessionId, self.server.Interface.PSessionId):
              try:
                self.request.sendall(resp_bad.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rbad', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              continue
            q = urllib.parse.parse_qs(urllib.parse.urlsplit(req.path).query)
            try:
              self.server.Interface.ItineraryProviderConnection = [[None]]
              self.server.Interface.ItineraryProviderSel = int(q['iset'][0])
              self.server.Interface.log(1, 'itinerary', self.server.Interface.ItinerariesProviders[int(q['iset'][0])][0])
            except:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              continue
            try:
              self.request.sendall(resp_204.encode('ISO-8859-1'))
              self.server.Interface.log(2, 'response', req.method, req.path)
            except:
              self.server.Interface.log(2, 'rerror', req.method, req.path)
          elif req.path.lower()[:15] == '/3D/viewer.html'.lower():
            self.server.Interface.SLock.acquire()
            self.server.Interface.SLock.release()
            if not self.server.Interface.HTML:
              self.server.Interface.Uri, self.server.Interface.Track = self.server.Interface.Tracks[int(req.path.split('?')[1])]
              if self.server.Interface.Track.WebMercatorPts == None:
                self.server.Interface.Track.BuildWebMercator()
            if self.server.Interface.Build3DHTML():
              resp_body = (self.server.Interface.HTML3D or '').encode('utf-8')
              try:
                if req.method == 'GET':
                  self.request.sendall(resp.replace('##type##', 'text/html').replace('##len##', str(len(resp_body))).encode('ISO-8859-1') + resp_body)
                else:
                  self.request.sendall(resp.replace('##type##', 'text/html').replace('##len##', str(len(resp_body))).encode('ISO-8859-1'))
                self.server.Interface.log(2, 'response', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
            else:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
            if not self.server.Interface.HTML:
              self.server.Interface.Uri, self.server.Interface.Track = None, None
          elif req.path.lower() == '/3D/data'.lower():
            if self.server.Interface.HTML3D:
              try:
                if req.method == 'GET':
                  self.request.sendall(resp.replace('##type##', 'application/octet-stream').replace('##len##', str(len(self.server.Interface.HTML3DData))).encode('ISO-8859-1') + self.server.Interface.HTML3DData)
                else:
                  self.request.sendall(resp.replace('##type##', 'application/octet-stream').replace('##len##', str(len(self.server.Interface.HTML3DData))).encode('ISO-8859-1'))
                self.server.Interface.log(2, 'response', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
            else:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
          elif req.path.lower()[:5] == '/edit':
            self.server.Interface.SLock.acquire()
            self.server.Interface.SLock.release()
            try:
              self.server.Interface.Uri, self.server.Interface.Track = self.server.Interface.Tracks[int(req.path.split('?')[1])]
              self.server.Interface.HTML = ''
              self.server.Interface.EditMode()
              self.server.Interface.HTML = self.server.Interface.HTML.replace('//        window.onunload', '        window.onunload').replace('//        document.addEventListener("DOMContentLoaded"', '        document.addEventListener("DOMContentLoaded"')
            except:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              continue
            self.server.Interface.HTMLExp = ''
            self.server.Interface.SessionId = str(uuid.uuid5(uuid.NAMESPACE_URL, self.server.Interface.Uri + str(time.time())))
            try:
              self.request.sendall(resp_307.encode('ISO-8859-1'))
              self.server.Interface.log(2, 'response', req.method, req.path)
            except:
              self.server.Interface.log(2, 'rerror', req.method, req.path)
          elif req.path.lower() == '/GPXExplorer/data'.lower():
            if not self.server.Interface.HTMLExp:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              continue
            try:
              resp_body = b''
              f = lambda e: '' if e == None else urllib.parse.quote(str(e))
              resp_body = '==\r\n'.join('=\r\n'.join('\r\n'.join('&'.join(map(f, p[1])) for p in seg) for seg in track.Pts) for track in map(lambda t: t[1], self.server.Interface.Tracks)).encode('utf-8')
              if req.method == 'GET':
                self.request.sendall(resp.replace('##type##', 'application/octet-stream').replace('##len##', str(len(resp_body))).encode('ISO-8859-1') + resp_body)
              else:
                self.request.sendall(resp.replace('##type##', 'application/octet-stream').replace('##len##', str(len(resp_body))).encode('ISO-8859-1'))
              self.server.Interface.log(2, 'response', req.method, req.path)
            except:
              self.server.Interface.log(2, 'rerror', req.method, req.path)
          else:
            try:
              self.request.sendall(resp_err.encode('ISO-8859-1'))
              self.server.Interface.log(2, 'rnfound', req.method, req.path)
            except:
              self.server.Interface.log(2, 'rerror', req.method, req.path)
        elif req.method == 'POST':
          resp_err = 'HTTP/1.1 422 Unprocessable Entity\r\n' \
          'Content-Length: 0\r\n' \
          'Date: ' + email.utils.formatdate(time.time(), usegmt=True) + '\r\n' \
          'Server: GPXTweaker\r\n' \
          'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
          '\r\n'
          resp_bad = 'HTTP/1.1 412 Precondition failed\r\n' \
          'Content-Length: 0\r\n' \
          'Date: ' + email.utils.formatdate(time.time(), usegmt=True) + '\r\n' \
          'Server: GPXTweaker\r\n' \
          'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
          '\r\n'
          if req.path.lower()[:4] == '/ele':
            if not req.header('If-Match') in (self.server.Interface.SessionId, self.server.Interface.PSessionId):
              try:
                self.request.sendall(resp_bad.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rbad', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              continue
            resp = 'HTTP/1.1 200 OK\r\n' \
            'Content-Type: text/csv; charset=utf-8\r\n' \
            'Content-Length: ##len##\r\n' \
            'Date: ' + email.utils.formatdate(time.time(), usegmt=True) + '\r\n' \
            'Server: GPXTweaker\r\n' \
            'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
            '\r\n'
            lpoints = req.body.splitlines()
            resp_body = b''
            points = []
            ids = []
            try:
              for point in lpoints:
                if point:
                  id, lat, lon = point.split(',')
                  points.append((float(lat), float(lon)))
                  ids.append(id)
              lelevations = zip(ids, self.server.Interface.ElevationProvider(points))
              for id_ele in lelevations:
                try:
                  resp_body = resp_body + (id_ele[0] + ',' + ('%.1f' % id_ele[1]) + '\r\n').encode('utf-8')
                except:
                  resp_body = resp_body + (id_ele[0] + ', \r\n').encode('utf-8')
              try:
                self.request.sendall(resp.replace('##len##', str(len(resp_body))).encode('ISO-8859-1') + resp_body)
                self.server.Interface.log(2, 'response', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
            except:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
          elif req.path.lower()[:5] == '/path':
            if not req.header('If-Match') in (self.server.Interface.SessionId, self.server.Interface.PSessionId):
              try:
                self.request.sendall(resp_bad.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rbad', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              continue
            resp = 'HTTP/1.1 200 OK\r\n' \
            'Content-Type: text/csv; charset=utf-8\r\n' \
            'Content-Length: ##len##\r\n' \
            'Date: ' + email.utils.formatdate(time.time(), usegmt=True) + '\r\n' \
            'Server: GPXTweaker\r\n' \
            'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
            '\r\n'
            lpoints = req.body.splitlines()
            try:
              if len(lpoints) != 2:
                raise
              points = [lpoints[0].split(','), lpoints[1].split(',')]
              if len(points[0]) != 2 or len(points[1]) != 2:
                raise
              iti = self.server.Interface.ItineraryProvider(points)
              if not iti:
                raise
              if math.dist(iti[0], map(float, points[0])) < 0.000001:
                del iti[0]
              if math.dist(iti[-1], map(float, points[1])) < 0.000001:
                del iti[-1]
              resp_body = ('\r\n'.join('%.6f,%.6f' % (*p,) for p in iti)).encode('utf-8')
            except:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rnfound', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
            try:
              self.request.sendall(resp.replace('##len##', str(len(resp_body))).encode('ISO-8859-1') + resp_body)
              self.server.Interface.log(2, 'response', req.method, req.path)
            except:
              self.server.Interface.log(2, 'rerror', req.method, req.path)
          elif req.path.lower()[:6] == '/track':
            self.server.Interface.SLock.acquire()
            resp = 'HTTP/1.1 204 No content\r\n' \
            'Content-Length: 0\r\n' \
            'Date: ' + email.utils.formatdate(time.time(), usegmt=True) + '\r\n' \
            'Server: GPXTweaker\r\n' \
            'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
            '\r\n'
            if not self.server.Interface.HTML and req.body.split('=')[0][-4:] == 'file':
              try:
                ouri = self.server.Interface.Tracks[int(req.body.split('=')[0][5:-4].rstrip('c'))][0]
                nuri = os.path.join(ouri.rsplit('\\', 1)[0] + '\\', req.body.split('=', 1)[1])
                if os.path.exists (nuri):
                  raise
                os.rename(ouri, nuri)
                for tr_ind in range(len(self.server.Interface.Tracks)):
                  tr = self.server.Interface.Tracks[tr_ind]
                  if tr[0] == ouri:
                    tr[0] = nuri
                    pos = self.server.Interface.HTMLExp.find('<input type="text" id="track%sfile"' % str(tr_ind))
                    self.server.Interface.HTMLExp = self.server.Interface.HTMLExp[:self.server.Interface.HTMLExp.find('value="', pos) + 7] + html.escape(req.body.split('=', 1)[1])  + self.server.Interface.HTMLExp[self.server.Interface.HTMLExp.find('" onchange', pos + 1):]
              except:
                try:
                  self.request.sendall(resp_err.encode('ISO-8859-1'))
                  self.server.Interface.log(2, 'rfailed', req.method, req.path)
                except:
                  self.server.Interface.log(2, 'rerror', req.method, req.path)
                self.server.Interface.SLock.release()
                continue
              try:
                self.request.sendall(resp.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'response', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              self.server.Interface.SLock.release()
              continue
            nosave = False
            if self.server.Interface.HTML and '?' in req.path:
              nosave = req.path.split('?')[1].lower() == 'save=no'
            if self.server.Interface.HTML and req.header('If-Match') == self.server.Interface.SessionId:
              self.server.Interface.PSessionId = self.server.Interface.SessionId
              if self.server.Interface.Track.OTrack != self.server.Interface.Track.Track and self.server.Interface.Track.OTrack != self.server.Interface.Track.STrack:
                try:
                  self.server.Interface.Track.OTrack.unlink()
                except:
                  pass
                self.server.Interface.Track.OTrack = self.server.Interface.Track.Track
            try:
              if not self.server.Interface.HTML:
                self.server.Interface.Uri, self.server.Interface.Track = self.server.Interface.Tracks[int(req.body.split('=')[0][5:-4].rstrip('c'))]
              if self.server.Interface.Track.UpdateGPX(req.body):
                if nosave:
                  self.server.Interface.Track.BuildWebMercator()
                else:
                  if req.header('If-Match') in (self.server.Interface.PSessionId, self.server.Interface.SessionId):
                    uri_suf = '.gpx'
                  else:
                    uri_suf = ' - ' + req.header('If-Match') + '.gpx'
                  uri_pre = self.server.Interface.Uri.rsplit('.', 1)[0]
                  if os.path.exists(self.server.Interface.Uri):
                    if not os.path.exists(uri_pre + ' - original.gpx'):
                      os.rename(self.server.Interface.Uri, uri_pre + ' - original.gpx')
                    else:
                      if os.path.exists(uri_pre + ' - backup.gpx'):
                        os.remove(uri_pre + ' - backup.gpx')
                      os.rename(self.server.Interface.Uri, uri_pre + ' - backup.gpx')
                  if not self.server.Interface.Track.SaveGPX(uri_pre + uri_suf):
                    if not self.server.Interface.HTML:
                      try:
                        if self.server.Interface.Track != self.server.Interface.OTrack:
                          self.server.Interface.Track.unlink()
                      except:
                        pass
                      self.server.Interface.Track = self.server.Interface.OTrack
                      self.server.Interface.Track.ProcessGPX('e')
                    raise
                  if self.server.Interface.HTML:
                    try:
                      self.server.Interface.EditMode()
                    except:
                      pass
                    if self.server.Interface.SessionId == self.server.Interface.PSessionId:
                      self.server.Interface.SessionId = str(uuid.uuid5(uuid.NAMESPACE_URL, self.server.Interface.Uri + str(time.time())))
                if not self.server.Interface.HTML:
                  try:
                    if self.server.Interface.OTrack != self.server.Interface.STrack:
                      self.server.Interface.OTrack.unlink()
                  except:
                    pass
                  self.server.Interface.OTrack = self.server.Interface.Track
                  for tr in self.server.Interface.Tracks:
                    if tr[1] != self.server.Interface.Track and tr[0] == self.server.Interface.Uri:
                      try:
                        tr[1].Track.unlink()
                      except:
                        pass
                      tr[1].Track = self.server.Interface.Track.Track.cloneNode(True)
                      tr[1].ProcessGPX('e')
                      tr[1].OTrack = tr[1].Track
                      tr[1].STrack = tr[1].Track
                  tr_ind = int(req.body.split('=')[0][5:-4].rstrip('c'))
                  nval = html.escape(req.body.split('=', 1)[1])
                  if req.body.split('=')[0][-4:] == 'name':
                    pos = self.server.Interface.HTMLExp.find('<input type="text" id="track%sname"' % str(tr_ind))
                    self.server.Interface.HTMLExp = self.server.Interface.HTMLExp[:self.server.Interface.HTMLExp.find('value="', pos) + 7] + nval + self.server.Interface.HTMLExp[self.server.Interface.HTMLExp.find('" onchange', pos):]
                    pos = self.server.Interface.HTMLExp.find('<label for="track%svisible"' % str(tr_ind))
                    self.server.Interface.HTMLExp = self.server.Interface.HTMLExp[:self.server.Interface.HTMLExp.find('title="', pos) + 7] + nval + self.server.Interface.HTMLExp[self.server.Interface.HTMLExp.find('" onclick', pos):self.server.Interface.HTMLExp.find('>', pos) + 1] + nval + self.server.Interface.HTMLExp[self.server.Interface.HTMLExp.find('<', pos + 1):]
                    pos = self.server.Interface.HTMLExp.find('<path id="path%s"' % str(tr_ind))
                    self.server.Interface.HTMLExp = self.server.Interface.HTMLExp[:self.server.Interface.HTMLExp.find('<title>', pos) + 7] + nval + self.server.Interface.HTMLExp[self.server.Interface.HTMLExp.find('"</title>', pos):]
                  elif req.body.split('=')[0][-5:] == 'color':
                    pos = self.server.Interface.HTMLExp.find('<input type="color" id="track%scolor"' % str(tr_ind))
                    self.server.Interface.HTMLExp = self.server.Interface.HTMLExp[:self.server.Interface.HTMLExp.find('value="', pos) + 7] + nval + self.server.Interface.HTMLExp[self.server.Interface.HTMLExp.find('" onchange', pos + 1):]
                    pos = self.server.Interface.HTMLExp.find('<svg id="track%s"' % str(tr_ind))
                    self.server.Interface.HTMLExp = self.server.Interface.HTMLExp[:self.server.Interface.HTMLExp.find('stroke="', pos) + 8] + nval + '" fill="' + nval + self.server.Interface.HTMLExp[self.server.Interface.HTMLExp.find('" style', pos):]
                    pos = self.server.Interface.HTMLExp.find('<svg id="waydots%s"' % str(tr_ind))
                    self.server.Interface.HTMLExp = self.server.Interface.HTMLExp[:self.server.Interface.HTMLExp.find('stroke="', pos) + 8] + nval + '" fill="' + nval + self.server.Interface.HTMLExp[self.server.Interface.HTMLExp.find('" style', pos):]
              else:
                raise
            except:
              try:
                self.request.sendall(resp_err.encode('ISO-8859-1'))
                self.server.Interface.log(2, 'rfailed', req.method, req.path)
              except:
                self.server.Interface.log(2, 'rerror', req.method, req.path)
              self.server.Interface.SLock.release()
              continue
            finally:
              if not self.server.Interface.HTML:
                self.server.Interface.Uri, self.server.Interface.Track = None, None
            try:
              self.request.sendall(resp.encode('ISO-8859-1'))
              self.server.Interface.log(2, 'response', req.method, req.path)
            except:
              self.server.Interface.log(2, 'rerror', req.method, req.path)
            self.server.Interface.SLock.release()
          else:
            try:
              self.request.sendall(resp_err.encode('ISO-8859-1'))
              self.server.Interface.log(2, 'rnfound', req.method, req.path)
            except:
              self.server.Interface.log(2, 'rerror', req.method, req.path)
        elif req.method:
          resp_err = 'HTTP/1.1 501 Not Implemented\r\n' \
          'Content-Length: 0\r\n' \
          'Date: ' + email.utils.formatdate(time.time(), usegmt=True) + '\r\n' \
          'Server: GPXTweaker\r\n' \
          'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
          '\r\n'
          try:
            self.request.sendall(resp_err.encode('ISO-8859-1'))
            self.server.Interface.log(2, 'rnfound', req.method, req.path)
          except:
            self.server.Interface.log(2, 'rerror', req.method, req.path)


class GPXTweakerWebInterfaceServer():

  HTML_TEMPLATE = \
  '<!DOCTYPE html>\r\n' \
  '<html lang="fr-FR">\r\n' \
  '  <head>\r\n' \
  '    <meta charset="utf-8">\r\n' \
  '    <title>GPXTweaker</title>\r\n' \
  '    <style type="text/css">\r\n' \
  '      :root {\r\n' \
  '        --scale:1;\r\n' \
  '        --zoom:1;\r\n' \
  '        --wsp:6em;\r\n' \
  '        --filter:none;\r\n' \
  '      }\r\n' \
  '      input {\r\n' \
  '        background-color:rgb(30,30,35);\r\n' \
  '        color:inherit;\r\n' \
  '      }\r\n' \
  '      input[type=text] {\r\n' \
  '        border-width:0.5px;\r\n' \
  '      }\r\n' \
  '      input[type=text]:focus {\r\n' \
  '        color:rgb(200,250,240);\r\n' \
  '      }\r\n' \
  '      input[id=name_track] {\r\n' \
  '        width:calc(98vw - 60em);\r\n' \
  '        font-size:70%;\r\n' \
  '      }\r\n' \
  '      form[id*=point] {\r\n' \
  '        overflow-x:hidden;\r\n' \
  '        margin-right: 4px;\r\n' \
  '      }\r\n' \
  '      input[type=checkbox] {\r\n' \
  '        appearance:none;\r\n' \
  '        vertical-align:middle;\r\n' \
  '        margin-left:3px;\r\n' \
  '        width:1.25em;\r\n' \
  '        height:1.25em;\r\n' \
  '      }\r\n' \
  '      input[type=checkbox]:checked::before {\r\n' \
  '        content:"\\2714";\r\n' \
  '        display:inline-block;\r\n' \
  '        text-align:center;\r\n' \
  '        width:100%;\r\n' \
  '        font-weight:bold;\r\n' \
  '      }\r\n' \
  '      input[type=checkbox][id^=segment] {\r\n' \
  '        margin-left:1px;\r\n' \
  '      }\r\n' \
  '      input+label:hover,input:hover+label {\r\n' \
  '        background-color:green;\r\n' \
  '      }\r\n' \
  '      label[id^=segment], label[id^=point], div[id^=point][id$=cont] {\r\n' \
  '        text-decoration:inherit;\r\n' \
  '      }\r\n' \
  '      label[id$=desc] {\r\n' \
  '        cursor:cell;\r\n' \
  '        display:inline-block;\r\n' \
  '        vertical-align:middle;\r\n' \
  '        white-space:nowrap;\r\n' \
  '        max-width:calc(24em - 22px);\r\n' \
  '        min-height:1.35em;\r\n' \
  '      }\r\n' \
  '      label[for$=lat], label[for$=lon], label[for$=ele], label[for$=alt], label[for$=time], label[for$=name] {\r\n' \
  '        display:inline-block;\r\n' \
  '        width:2em;\r\n' \
  '        padding-left:1em;\r\n' \
  '      }\r\n' \
  '      input[id$=lat], input[id$=lon], input[id$=ele], input[id$=alt], input[id$=time], input[id$=name] {\r\n' \
  '        height:1.35em;\r\n' \
  '        width:75%;\r\n' \
  '        font-size:100%;\r\n' \
  '      }\r\n' \
  '      br+span {\r\n' \
  '        display:none;\r\n' \
  '      }\r\n' \
  '      svg[id*=dot] {\r\n' \
  '        position:absolute;\r\n' \
  '        cursor:pointer;\r\n' \
  '        stroke-width:1.5;\r\n' \
  '        stroke:gray;\r\n' \
  '        fill:none;\r\n' \
  '      }\r\n' \
  '      path {\r\n' \
  '        pointer-events:stroke;\r\n' \
  '        cursor:pointer;\r\n' \
  '        fill:none;\r\n' \
  '        vector-effect:non-scaling-stroke;\r\n' \
  '      }\r\n' \
  '      svg[id^=track] {\r\n' \
  '        position:absolute;\r\n' \
  '        pointer-events:none;\r\n' \
  '        stroke-width:1.5;\r\n' \
  '        stroke-linecap:round;\r\n' \
  '        stroke-linejoin:round;\r\n' \
  '        stroke:red;\r\n' \
  '        fill:red;\r\n' \
  '      }\r\n' \
  '      svg[id^=track] text {\r\n' \
  '        pointer-events:none;\r\n' \
  '        font-size:calc(24px * var(--scale));\r\n' \
  '        word-spacing:var(--wsp);\r\n' \
  '        stroke:none;\r\n' \
  '      }\r\n' \
  '      button {\r\n' \
  '        border:none;\r\n' \
  '        padding-left:0;\r\n' \
  '        padding-right:0;\r\n' \
  '        width:1.4em;\r\n' \
  '        height:1.4em;\r\n' \
  '        background-color:rgb(30,30,35);\r\n' \
  '        color:inherit;\r\n' \
  '        line-height:1.2em;\r\n' \
  '        font-size:100%;\r\n' \
  '        cursor:pointer;\r\n' \
  '      }\r\n' \
  '      select {\r\n' \
  '        background-color:rgb(30,30,35);\r\n' \
  '        color:inherit;\r\n' \
  '        border-width:0.5px;\r\n' \
  '      }\r\n' \
  '      select:focus {\r\n' \
  '          color:rgb(200,250,240);\r\n' \
  '      }\r\n' \
  '      @-moz-document url-prefix() {\r\n' \
  '        select {\r\n' \
  '          appearance:none;\r\n' \
  '          background-image:url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" style="fill:rgb(225,225,225)"><text x="0.2em" y="0.4em" >%E2%8C%84</text></svg>\');\r\n' \
  '          background-repeat:no-repeat;\r\n' \
  '          background-position-x:right;\r\n' \
  '          background-position-y:bottom;\r\n' \
  '          background-size:2em 1em;\r\n' \
  '        }\r\n' \
  '        select:focus {\r\n' \
  '          background-image:url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" style="fill:rgb(200,250,240)"><text x="0.2em" y="0.4em" >%E2%8C%84</text></svg>\');\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      select option {\r\n' \
  '        color:rgb(225,225,225);\r\n' \
  '      }\r\n' \
  '      label[for$=filter] {\r\n' \
  '        position:absolute;\r\n' \
  '        top:1.5em;\r\n' \
  '        text-align:center;\r\n' \
  '        font-weight:normal;\r\n' \
  '        font-size:90%;\r\n' \
  '      }\r\n' \
  '      span[id$=stren], span[id^=sl] ,span[id^=sp] {\r\n' \
  '        position:absolute;\r\n' \
  '        top:2.8em;\r\n' \
  '        width:2em;\r\n' \
  '        font-size:90%;\r\n' \
  '      }\r\n' \
  '      input[type=range] {\r\n' \
  '        position:absolute;\r\n' \
  '        top:3em;\r\n' \
  '        max-width:40vh;\r\n' \
  '        width:9em;\r\n' \
  '        margin-right:0;\r\n' \
  '        transform:rotate(-90deg);\r\n' \
  '        transform-origin:right center;\r\n' \
  '        font-size:100%;\r\n' \
  '      }\r\n' \
  '      span+span[id^=message] {\r\n' \
  '        margin-left:0.4em;\r\n' \
  '        padding-left:0.4em;\r\n' \
  '        border-left:1px rgb(225,225,225) solid;\r\n' \
  '      }\r\n' \
  '      img {\r\n' \
  '        filter:var(--filter);\r\n' \
  '      }\r\n' \
  '    </style>\r\n' \
  '    <script>\r\n' \
  '      var wmb = Math.PI * 6378137;\r\n##DECLARATIONS##\r\n' \
  '      var cleft = null;\r\n' \
  '      var cright = null;\r\n' \
  '      var ctop = null;\r\n' \
  '      var cbottom = null;\r\n' \
  '      var hpx = 0;\r\n' \
  '      var hpy = 0;\r\n' \
  '      var zoom = 1;\r\n' \
  '      if (mode == "map") {\r\n' \
  '        var zooms = ["1", "1.5", "2", "3", "4", "6", "10", "15", "25"];\r\n' \
  '        var zoom_s = "1";\r\n' \
  '      } else {\r\n' \
  '        var tset = 0;\r\n' \
  '        var tlevels = [];\r\n' \
  '        var tlevel = 0;\r\n' \
  '        var zooms = ["1/8", "1/4", "1/2", "3/4", "1", "1.5", "2", "3", "4", "6", "8"];\r\n' \
  '        var tlock = false;\r\n' \
  '        var zoom_s = "1";\r\n' \
  '      }\r\n' \
  '      var eset = 0;\r\n' \
  '      var iset = 0;\r\n' \
  '      var dots_visible = false;\r\n' \
  '      var focused = "";\r\n' \
  '      var hist = [[], []];\r\n' \
  '      var hist_b = 0;\r\n' \
  '      var foc_old = null;\r\n' \
  '      var date_conv = new Intl.DateTimeFormat("default",{year: "numeric", month:"2-digit", day:"2-digit"});\r\n' \
  '      var time_conv = new Intl.DateTimeFormat("default",{hour12:false, hour: "2-digit", minute:"2-digit", second:"2-digit"});\r\n' \
  '      var stats = [];\r\n' \
  '      var gpu_part = gpucomp >=1?true:false;\r\n' \
  '      var point_stat = [];\r\n' \
  '      var graph_ip = null;\r\n' \
  '      var graph_px = null;\r\n' \
  '      var msg_n = 0;\r\n' \
  '      class GPUStats {\r\n' \
  '        static get tw() {return 1024;}\r\n' \
  '        constructor () {\r\n' \
  '          this.canvas = document.createElement("canvas");\r\n' \
  '          this.gl = this.canvas.getContext("webgl2", {preserveDrawingBuffer: true});\r\n' \
  '          this.gl_programs = new Map();\r\n' \
  '          this.cur_prog = null;\r\n' \
  '          this.gl_attributes = new Map([["vstart", ["int", 1]]]);\r\n' \
  '          this.gl_static_uniforms = new Map([["mmlhtex", "sampler2D"], ["teatex", "sampler2D"], ["dtex", "sampler2D"], ["ssstex", "sampler2D"], ["trange", "float"], ["spmax", "float"], ["drange", "float"], ["slmax", "float"]]);\r\n' \
  '          this.gl_dynamic_uniforms = new Map([["vlength", "int"]]);\r\n' \
  '          this.gl_feedbacks = new Map([["vd", "float"], ["vsss", "vec3"]]);\r\n' \
  '          this._starts = null;\r\n' \
  '          this.tlength = null;\r\n' \
  '          this._mmlhs = null;\r\n' \
  '          this._teas = null;\r\n' \
  '          this.vstart = null;\r\n' \
  '          this.mmlhtex = 0;\r\n' \
  '          this.teatex = 1;\r\n' \
  '          this.dtex = 2;\r\n' \
  '          this.ssstex = 3;\r\n' \
  '          this.mmlh_texture = null;\r\n' \
  '          this.tea_texture = null;\r\n' \
  '          this.d_texture = null;\r\n' \
  '          this.sss_texture = null;\r\n' \
  '          this.vlength = 0;\r\n' \
  '          this.trange = 300 / 2;\r\n' \
  '          this.spmax = 8 / 3.6;\r\n' \
  '          this.drange = 500 / 2;\r\n' \
  '          this.slmax = 50 / 100;\r\n' \
  '          this.vd = null;\r\n' \
  '          this.vsss = null;\r\n' \
  '          this._ds = null;\r\n' \
  '          this._ssss = null;\r\n' \
  '          this.gl.enable(this.gl.RASTERIZER_DISCARD);\r\n' \
  '          let vertex_dshader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform sampler2D mmlhtex;\r\n' \
  '            out float vd;\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec4 mmlhe = texelFetch(mmlhtex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0) * vec4(0.00872664626, 0.00872664626, 0.0174532925, 1.0);\r\n' \
  '              vec2 lhs = gl_InstanceID > 0 ? texelFetch(mmlhtex, ivec2((pc - 1) % ${GPUStats.tw}, (pc - 1) / ${GPUStats.tw}), 0).pq * vec2(0.0174532925, 1.0) : mmlhe.pq;\r\n' \
  '              float a = sqrt(pow(mmlhe.s, 2.0) - pow(mmlhe.s, 4.0) / 3.0 + cos(lhs.s) * cos(mmlhe.p) * (pow(mmlhe.t, 2.0) - pow(mmlhe.t, 4.0) / 3.0));\r\n' \
  '              vd = sqrt(pow(12756274.0 * (a + pow(a, 3.0) / 6.0), 2.0) + pow(mmlhe.q - lhs.t, 2.0));\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let vertex_s1shader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform sampler2D teatex;\r\n' \
  '            uniform sampler2D dtex;\r\n' \
  '            uniform int vlength;\r\n' \
  '            uniform float trange;\r\n' \
  '            uniform float spmax;\r\n' \
  '            uniform float drange;\r\n' \
  '            uniform float slmax;\r\n' \
  '            out vec3 vsss;\r\n' \
  '            vec2 slope(float d, vec2 h) {\r\n' \
  '              return mix(slmax * sign(h), h / sqrt(d * d - h * h), lessThan(abs(h), vec2(d)));\r\n' \
  '            }\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec4 tdeas;\r\n' \
  '              tdeas.spq = texelFetch(teatex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).stp;\r\n' \
  '              tdeas.t = texelFetch(dtex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).s;\r\n' \
  '              vec2 tde = tdeas.st;\r\n' \
  '              vec2 tdp = tde;\r\n' \
  '              vsss = vec3(0.0);\r\n' \
  '              for (int p = pc + 1; p < vstart + vlength; p++) {\r\n' \
  '                tde = vec2(texelFetch(teatex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s, texelFetch(dtex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s + tde.t);\r\n' \
  '                if (tde.s > tdeas.s + trange) {break;}\r\n' \
  '                if (tde.s == tdeas.s) {continue;}\r\n' \
  '                vsss.s += (tde.t - tdeas.t) / (tde.s - tdeas.s) * (tde.s - tdp.s);\r\n' \
  '                tdp = tde;\r\n' \
  '              }\r\n' \
  '              if (tdp.s != tdeas.s) {\r\n' \
  '                vsss.s = (vsss.s + (tdp.t - tdeas.t) / (tdp.s - tdeas.s) * (trange + tdeas.s - tdp.s)) / trange;\r\n' \
  '              }\r\n' \
  '              vsss.s = min(vsss.s, spmax);\r\n' \
  '              vec3 deae = tdeas.tpq;\r\n' \
  '              vec3 deap = deae;\r\n' \
  '              for (int p = pc + 1; p < vstart + vlength; p++) {\r\n' \
  '                deae = vec3(texelFetch(dtex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s + deae.s, texelFetch(teatex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).tp);\r\n' \
  '                if (deae.s > tdeas.t + drange) {break;}\r\n' \
  '                if (deae.s == tdeas.t) {continue;}\r\n' \
  '                vsss.tp += slope(deae.s - tdeas.t, deae.tp - tdeas.pq) * (deae.s - deap.s);\r\n' \
  '                deap = deae;\r\n' \
  '              }\r\n' \
  '              if (deap.s != tdeas.t) {\r\n' \
  '                vsss.tp = (vsss.tp + slope(deap.s - tdeas.t, deap.tp - tdeas.pq) * (drange + tdeas.t - deap.s)) / drange;\r\n' \
  '              }\r\n' \
  '              vsss.tp = clamp(vsss.tp, vec2(-slmax), vec2(slmax));\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let vertex_s2shader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform sampler2D teatex;\r\n' \
  '            uniform sampler2D dtex;\r\n' \
  '            uniform sampler2D ssstex;\r\n' \
  '            uniform int vlength;\r\n' \
  '            uniform float trange;\r\n' \
  '            uniform float spmax;\r\n' \
  '            uniform float drange;\r\n' \
  '            uniform float slmax;\r\n' \
  '            out vec3 vsss;\r\n' \
  '            void main() {\r\n' \
  '              vsss = vec3(0.0);\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec2 tsc = vec2(texelFetch(teatex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).s, texelFetch(ssstex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).s);\r\n' \
  '              vec2 tsf = tsc;\r\n' \
  '              vec2 tsn = tsc;\r\n' \
  '              vsss.s = tsc.t;\r\n' \
  '              float c;\r\n' \
  '              float su = 0.0;\r\n' \
  '              float s = 0.0;\r\n' \
  '              if (texelFetch(teatex, ivec2((pc + 1) % ${GPUStats.tw}, (pc + 1) / ${GPUStats.tw}), 0).s - tsc.s <= trange) {\r\n' \
  '                for (int p = pc - 1; p >= vstart; p--) {\r\n' \
  '                  tsf = vec2(texelFetch(teatex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s, texelFetch(ssstex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s);\r\n' \
  '                  if (tsf.s < tsc.s - trange) {break;}\r\n' \
  '                  c = (tsn.s - tsf.s) / (tsc.s - tsf.s + 1.0);\r\n' \
  '                  s += tsf.t * c;\r\n' \
  '                  su += c;\r\n' \
  '                  tsn = tsf;\r\n' \
  '                }\r\n' \
  '                if (tsc.s != tsn.s) {\r\n' \
  '                  vsss.s = min((vsss.s + s / 2.0) / (1.0 + su / 2.0), spmax);\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              vec3 dssc = vec3(texelFetch(dtex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).s, texelFetch(ssstex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).tp);\r\n' \
  '              vec3 dssf = dssc;\r\n' \
  '              vec3 dssn = dssc;\r\n' \
  '              vsss.tp = dssc.tp;\r\n' \
  '              su = 0.0;\r\n' \
  '              vec2 ss = vec2(0.0);\r\n' \
  '              if (texelFetch(dtex, ivec2((pc + 1) % ${GPUStats.tw}, (pc + 1) / ${GPUStats.tw}), 0).s <= drange) {\r\n' \
  '                for (int p = pc - 1; p >= vstart; p--) {\r\n' \
  '                  dssf = vec3(dssf.s - texelFetch(dtex, ivec2((p + 1) % ${GPUStats.tw}, (p + 1) / ${GPUStats.tw}), 0).s, texelFetch(ssstex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).tp);\r\n' \
  '                  if (dssf.s < dssc.s - drange) {break;}\r\n' \
  '                  c = (dssn.s - dssf.s) / (dssc.s - dssf.s + 1.0);\r\n' \
  '                  ss += dssf.tp * c;\r\n' \
  '                  su += c;\r\n' \
  '                  dssn = dssf;\r\n' \
  '                }\r\n' \
  '                if (dssc.s != dssn.s) {\r\n' \
  '                  vsss.tp = clamp((vsss.tp + ss / 2.0) / (1.0 + su / 2.0), vec2(-slmax), vec2(slmax));\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let fragment_shader_s = `#version 300 es\r\n' \
  '            precision highp float;\r\n' \
  '            void main() {\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          this.program_create("dprogram", vertex_dshader_s, fragment_shader_s);\r\n' \
  '          this.program_create("s1program", vertex_s1shader_s, fragment_shader_s);\r\n' \
  '          this.program_create("s2program", vertex_s2shader_s, fragment_shader_s);\r\n' \
  '        }\r\n' \
  '        program_create(name, vshader_s, fshader_s) {\r\n' \
  '          let vertex_shader = this.gl.createShader(this.gl.VERTEX_SHADER);\r\n' \
  '          this.gl.shaderSource(vertex_shader, vshader_s);\r\n' \
  '          this.gl.compileShader(vertex_shader);\r\n' \
  '          let fragment_shader = this.gl.createShader(this.gl.FRAGMENT_SHADER);\r\n' \
  '          this.gl.shaderSource(fragment_shader, fshader_s);\r\n' \
  '          this.gl.compileShader(fragment_shader);\r\n' \
  '          let prog = this.gl.createProgram();\r\n' \
  '          this.gl.attachShader(prog, vertex_shader);\r\n' \
  '          this.gl.attachShader(prog, fragment_shader);\r\n' \
  '          this.gl_programs.set(name, new Map());\r\n' \
  '          this.gl_programs.get(name).set("program", prog);\r\n' \
  '          let f = [];\r\n' \
  '          for (let [n, t] of this.gl_feedbacks) {\r\n' \
  '            if (vshader_s.indexOf("out " + t + " " + n) >= 0) {\r\n' \
  '              this.gl_programs.get(name).set(n, f.length);\r\n' \
  '              f.push(n);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (f.length > 0) {\r\n' \
  '            this.gl.transformFeedbackVaryings(prog, f, this.gl.SEPARATE_ATTRIBS);\r\n' \
  '          }\r\n' \
  '          this.gl.linkProgram(prog);\r\n' \
  '          this.gl_programs.get(name).set("vao", this.gl.createVertexArray());\r\n' \
  '          if (f.length > 0) {\r\n' \
  '            this.gl_programs.get(name).set("tf", this.gl.createTransformFeedback());\r\n' \
  '          }\r\n' \
  '          for (let [n, ts] of this.gl_attributes) {\r\n' \
  '            if (vshader_s.indexOf("in " + ts[0] + " " + n) >= 0) {\r\n' \
  '              this.gl_programs.get(name).set(n, this.gl.getAttribLocation(prog, n));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          for (let [n, t] of [...this.gl_static_uniforms.entries(), ...this.gl_dynamic_uniforms.entries()]) {\r\n' \
  '            if (vshader_s.indexOf("uniform " + t + " " + n) >= 0 || fshader_s.indexOf("uniform " + t + " " + n) >= 0) {\r\n' \
  '              this.gl_programs.get(name).set(n, this.gl.getUniformLocation(prog, n));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        program_use(name) {\r\n' \
  '          this.cur_prog = name;\r\n' \
  '          this.gl.useProgram(this.gl_programs.get(name).get("program"));\r\n' \
  '          this.gl.bindVertexArray(this.gl_programs.get(name).get("vao"));\r\n' \
  '          this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, this.gl_programs.get(name).get("tf"));\r\n' \
  '        }\r\n' \
  '        program_attributes() {\r\n' \
  '          for (let [n, ts] of this.gl_attributes) {\r\n' \
  '            if (this.gl_programs.get(this.cur_prog).has(n)) {\r\n' \
  '              this.gl.enableVertexAttribArray(this.gl_programs.get(this.cur_prog).get(n));\r\n' \
  '              this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this[n]);\r\n' \
  '              if (ts[0] == "int") {\r\n' \
  '                this.gl.vertexAttribIPointer(this.gl_programs.get(this.cur_prog).get(n), ts[1], this.gl.INT, false, 0, 0);\r\n' \
  '              } else {\r\n' \
  '                this.gl.vertexAttribPointer(this.gl_programs.get(this.cur_prog).get(n), ts[1], this.gl.FLOAT, false, 0, 0);\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          this.gl.bindBuffer(this.gl.ARRAY_BUFFER, null);\r\n' \
  '        }\r\n' \
  '        program_uniforms(type="dynamic") {\r\n' \
  '          for (let [n, t] of type=="static"?this.gl_static_uniforms:this.gl_dynamic_uniforms) {\r\n' \
  '            if (this.gl_programs.get(this.cur_prog).has(n)) {\r\n' \
  '              switch (t) {\r\n' \
  '                case "float":\r\n' \
  '                  this.gl.uniform1f(this.gl_programs.get(this.cur_prog).get(n), this[n]);\r\n' \
  '                  break;\r\n' \
  '                case "sampler2D":\r\n' \
  '                case "int":\r\n' \
  '                  this.gl.uniform1i(this.gl_programs.get(this.cur_prog).get(n), this[n]);\r\n' \
  '                  break;\r\n' \
  '                default:\r\n' \
  '                  this.gl.uniform1f(this.gl_programs.get(this.cur_prog).get(n), this[n]);\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        program_feedbacks(offset, size) {\r\n' \
  '          for (let [n, t] of this.gl_feedbacks) {\r\n' \
  '            if (this.gl_programs.get(this.cur_prog).has(n)) {\r\n' \
  '              let s = 0;\r\n' \
  '              switch (t) {\r\n' \
  '                case "float":\r\n' \
  '                  s = 4;\r\n' \
  '                  break;\r\n' \
  '                case "vec3":\r\n' \
  '                  s = 12;\r\n' \
  '                  break;\r\n' \
  '                default:\r\n' \
  '                  s = 4;\r\n' \
  '              }\r\n' \
  '              this.gl.bindBufferRange(this.gl.TRANSFORM_FEEDBACK_BUFFER, this.gl_programs.get(this.cur_prog).get(n), this[n], offset * s, size * s);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        static pad(s) {\r\n' \
  '          return (Math.floor((s - 1) / GPUStats.tw) + 1) * GPUStats.tw;\r\n' \
  '        }\r\n' \
  '        texture_load(unit, ncomp, src, tex=null) {\r\n' \
  '          let gl_texture = tex;\r\n' \
  '          if (tex == null) {gl_texture = this.gl.createTexture();}\r\n' \
  '          this.gl.activeTexture(unit);\r\n' \
  '          this.gl.bindTexture(this.gl.TEXTURE_2D, gl_texture);\r\n' \
  '          this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_WRAP_S, this.gl.CLAMP_TO_EDGE);\r\n' \
  '          this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_WRAP_T, this.gl.CLAMP_TO_EDGE);\r\n' \
  '          this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_MIN_FILTER, this.gl.NEAREST);\r\n' \
  '          this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_MAG_FILTER, this.gl.NEAREST);\r\n' \
  '          if (Array.isArray(src)) {\r\n' \
  '            this.gl.texImage2D(this.gl.TEXTURE_2D, 0, [this.gl.R32F, this.gl.RG32F, this.gl.RGB32F, this.gl.RGBA32F][ncomp - 1], GPUStats.tw, src.length / ncomp / GPUStats.tw, 0, [this.gl.R, this.gl.RG, this.gl.RGB, this.gl.RGBA] [ncomp - 1], this.gl.FLOAT, new Float32Array(src));\r\n' \
  '          } else if (src instanceof Float32Array) {\r\n' \
  '            this.gl.texImage2D(this.gl.TEXTURE_2D, 0, [this.gl.R32F, this.gl.RG32F, this.gl.RGB32F, this.gl.RGBA32F][ncomp - 1], GPUStats.tw, src.length / ncomp / GPUStats.tw, 0, [this.gl.R, this.gl.RG, this.gl.RGB, this.gl.RGBA] [ncomp - 1], this.gl.FLOAT, src);\r\n' \
  '          } else if (src instanceof WebGLBuffer) {\r\n' \
  '            this.gl.bindBuffer(this.gl.PIXEL_UNPACK_BUFFER, src);\r\n' \
  '            this.gl.texImage2D(this.gl.TEXTURE_2D, 0, [this.gl.R32F, this.gl.RG32F, this.gl.RGB32F, this.gl.RGBA32F][ncomp - 1], GPUStats.tw, this.gl.getBufferParameter(this.gl.PIXEL_UNPACK_BUFFER, this.gl.BUFFER_SIZE) / ncomp / 4 / GPUStats.tw, 0, [this.gl.RED, this.gl.RG, this.gl.RGB, this.gl.RGBA] [ncomp - 1], this.gl.FLOAT, 0);\r\n' \
  '            this.gl.bindBuffer(this.gl.PIXEL_UNPACK_BUFFER, null);\r\n' \
  '          } else {\r\n' \
  '            this.gl.texImage2D(this.gl.TEXTURE_2D, 0, [this.gl.R32F, this.gl.RG32F, this.gl.RGB32F, this.gl.RGBA32F][ncomp - 1], GPUStats.tw, src / GPUStats.tw, 0, [this.gl.RED, this.gl.RG, this.gl.RGB, this.gl.RGBA] [ncomp - 1], this.gl.FLOAT, 0);\r\n' \
  '          }\r\n' \
  '          return gl_texture;\r\n' \
  '        }\r\n' \
  '        buffer_load(src, use, buf=null) {\r\n' \
  '          let gl_buffer = buf;\r\n' \
  '          if (buf == null) {gl_buffer = this.gl.createBuffer();}\r\n' \
  '          this.gl.bindBuffer(this.gl.ARRAY_BUFFER, gl_buffer);\r\n' \
  '          this.gl.bufferData(this.gl.ARRAY_BUFFER, src, use);\r\n' \
  '          this.gl.bindBuffer(this.gl.ARRAY_BUFFER, null);\r\n' \
  '          return gl_buffer;\r\n' \
  '        }\r\n' \
  '        set starts(a) {\r\n' \
  '          this._starts = a;\r\n' \
  '          this.tlength = this._starts[this._starts.length - 1];\r\n' \
  '          this.vstart = this.buffer_load(new Int32Array(this._starts), this.gl.STATIC_DRAW, this.vstart);\r\n' \
  '        }\r\n' \
  '        set mmlhs(a) {\r\n' \
  '          this._mmlhs = a;\r\n' \
  '          this.mmlh_texture = this.texture_load(this.gl.TEXTURE0 + this.mmlhtex, 4, this._mmlhs, this.mmlh_texture);\r\n' \
  '          this.vd = this.buffer_load(4 * GPUStats.pad(this.tlength), this.gl.STREAM_READ, this.vd);\r\n' \
  '         }\r\n' \
  '        set teas(a) {\r\n' \
  '          this._teas = a;\r\n' \
  '          this.tea_texture = this.texture_load(this.gl.TEXTURE0 + this.teatex, 3, this._teas, this.tea_texture);\r\n' \
  '          this.vsss = this.buffer_load(3 * 4 * GPUStats.pad(this.tlength), this.gl.STREAM_READ, this.vsss);\r\n' \
  '        }\r\n' \
  '        _calc() {\r\n' \
  '          for (let s=0; s<this._starts.length-1; s++) {\r\n' \
  '            this.vlength = this._starts[s + 1] - this._starts[s];\r\n' \
  '            if (this.vlength == 0) {continue;}\r\n' \
  '            this.program_uniforms();\r\n' \
  '            this.program_feedbacks(this._starts[s], this.vlength);\r\n' \
  '            this.gl.beginTransformFeedback(this.gl.POINTS);\r\n' \
  '            this.gl.drawArraysInstanced(this.gl.POINTS, s, 1, this.vlength - (this.cur_prog=="s2program"?1:0));\r\n' \
  '            this.gl.endTransformFeedback();\r\n' \
  '            this.gl.finish();\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        calc() {\r\n' \
  '          for (let n of this.gl_programs.keys()) {\r\n' \
  '            this.program_use(n);\r\n' \
  '            this.program_attributes();\r\n' \
  '            this.program_uniforms("static");\r\n' \
  '          }\r\n' \
  '          this.program_use("dprogram");\r\n' \
  '          this._calc();\r\n' \
  '          this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, null);\r\n' \
  '          this.d_texture = this.texture_load(this.gl.TEXTURE0 + this.dtex, 1, this.vd, this.d_texture);\r\n' \
  '          this.feedbacks();\r\n' \
  '          this.program_use("s1program");\r\n' \
  '          this._calc();\r\n' \
  '          this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, null);\r\n' \
  '          this.sss_texture = this.texture_load(this.gl.TEXTURE0 + this.ssstex, 3, this.vsss, this.sss_texture);\r\n' \
  '          this.program_use("s2program");\r\n' \
  '          this._calc();\r\n' \
  '          this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, null);\r\n' \
  '          this.feedbacks();\r\n' \
  '        }\r\n' \
  '        feedbacks() {\r\n' \
  '          for (let [n, t] of this.gl_feedbacks) {\r\n' \
  '            if (this.gl_programs.get(this.cur_prog).has(n)) {\r\n' \
  '              switch (t) {\r\n' \
  '                case "float":\r\n' \
  '                  this[n.replace("v", "_") + "s"] = new Float32Array(this.tlength);\r\n' \
  '                  break;\r\n' \
  '                case "vec3":\r\n' \
  '                  this[n.replace("v", "_") + "s"] = new Float32Array(3 * this.tlength);\r\n' \
  '                  break;\r\n' \
  '                default:\r\n' \
  '                  this[n.replace("v", "_") + "s"] = new Float32Array(this.tlength);\r\n' \
  '              }\r\n' \
  '              this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this[n]) ;\r\n' \
  '              this.gl.getBufferSubData(this.gl.ARRAY_BUFFER, 0, this[n.replace("v", "_") + "s"], 0, this[n.replace("v", "_") + "s"].length);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          this.gl.bindBuffer(this.gl.ARRAY_BUFFER, null) ;\r\n' \
  '        }\r\n' \
  '        get ds() {\r\n' \
  '          return this._ds;\r\n' \
  '        }\r\n' \
  '        get ssss() {\r\n' \
  '          return this._ssss;\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      if (gpucomp > 0) {var gpustats = new GPUStats();}\r\n' \
  '      function show_msg(msg, dur, msgn=null) {\r\n' \
  '        let m = null;\r\n' \
  '        if (msgn == null) {\r\n' \
  '          msgn = ++msg_n;\r\n' \
  '          m = document.createElement("span");\r\n' \
  '          m.id = "message" + msgn.toString();\r\n' \
  '        } else {\r\n' \
  '          m = document.getElementById("message" + msgn.toString());\r\n' \
  '        }\r\n' \
  '        m.innerHTML = msg;\r\n' \
  '        document.getElementById("message").insertBefore(m, document.getElementById("message").firstElementChild);\r\n' \
  '        if (dur) {setTimeout(function() {document.getElementById("message").removeChild(m);}, dur * 1000);}\r\n' \
  '        return msgn;\r\n' \
  '      }\r\n' \
  '      function load_tcb(t, nset, nlevel, kzoom=false) {\r\n' \
  '        if (t.status != 200) {\r\n' \
  '          document.getElementById("tset").selectedIndex = tset;\r\n' \
  '          if (nset == null) {\r\n' \
  '            window.stop();\r\n' \
  '            tlevel = nlevel;\r\n' \
  '            if (! kzoom) {zoom_s = tlevels[tlevel][1];}\r\n' \
  '            cleft = null;\r\n' \
  '            rescale();\r\n' \
  '          }\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        window.stop();\r\n' \
  '        let msg = JSON.parse(t.response);\r\n' \
  '        if (nset == null) {\r\n' \
  '          tlevel = nlevel;\r\n' \
  '          if (! kzoom) {zoom_s = tlevels[tlevel][1];}\r\n' \
  '          ttopx = msg.topx;\r\n' \
  '          ttopy = msg.topy;\r\n' \
  '          let sta = twidth == 0;\r\n' \
  '          twidth = msg.width;\r\n' \
  '          theight = msg.height\r\n' \
  '          text = msg.ext;\r\n' \
  '          let tscale_ex = tscale;\r\n' \
  '          tscale = msg.scale;\r\n' \
  '          cleft = null;\r\n' \
  '          rescale(tscale_ex);\r\n' \
  '          if (sta) {scroll_to_all()}\r\n' \
  '        } else {\r\n' \
  '          tset = document.getElementById("tset").selectedIndex;\r\n' \
  '          let matrix = null;\r\n' \
  '          let lf = false;\r\n' \
  '          if (nlevel >= 0) {\r\n' \
  '            tlevels = msg.tlevels;\r\n' \
  '            if (nlevel == 0) {\r\n' \
  '              nlevel = tlevels[0];\r\n' \
  '              zoom_s = tlevels[nlevel][1];\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            nlevel = tlevels[0];\r\n' \
  '            matrix = tlevels[tlevel][0];\r\n' \
  '            tlevels = msg.tlevels;\r\n' \
  '            for (let i=1; i<tlevels.length; i++) {\r\n' \
  '              if (tlevels[i][0] <= matrix) {nlevel = i;}\r\n' \
  '              if (tlevels[i][0] == matrix) {\r\n' \
  '                lf = true;\r\n' \
  '                break;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            if (! lf) {\r\n' \
  '              let zoom_t = Math.pow(2, matrix - tlevels[nlevel][0]) * zoom;\r\n' \
  '              zoom_s = zooms[0];\r\n' \
  '              let i = 0;\r\n' \
  '              while (i < zooms.length) {\r\n' \
  '                if (eval(zooms[i]) <= zoom_t) {zoom_s = zooms[i]}\r\n' \
  '                if (eval(zooms[i]) >= zoom_t) {break;}\r\n' \
  '                i ++;\r\n' \
  '              }\r\n' \
  '              matrix = tlevels[nlevel][0];\r\n' \
  '              for (let i=1; i<tlevels.length; i++) {\r\n' \
  '                if (tlevels[i][0] == matrix) {\r\n' \
  '                  nlevel = i;\r\n' \
  '                  break;\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              for (let i=nlevel; i<tlevels.length; i++) {\r\n' \
  '                if (tlevels[i][0] != matrix) {break;}\r\n' \
  '                if (eval(tlevels[i][1]) <= zoom_t) {nlevel = i;}\r\n' \
  '              }\r\n' \
  '              if (! tlock) {switch_tlock(false);}\r\n' \
  '            } else  {\r\n' \
  '              let zf = false;\r\n' \
  '              for (let i=1; i<tlevels.length; i++) {\r\n' \
  '                if (tlevels[i][0] == matrix && eval(tlevels[i][1]) <= eval(zoom_s)) {nlevel = i;}\r\n' \
  '                if (tlevels[i][0] == matrix && tlevels[i][1] == zoom_s) {\r\n' \
  '                  zf = true;\r\n' \
  '                  break;\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              if (! tlock && ! zf) {switch_tlock(false);}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          switch_tiles(null, nlevel, true);\r\n' \
  '        }\r\n' \
  '      } \r\n' \
  '      function error_tcb() {\r\n' \
  '        document.getElementById("tset").selectedIndex = tset;\r\n' \
  '      } \r\n' \
  '      function switch_tiles(nset, nlevel, kzoom=false) {\r\n' \
  '        let q = "";\r\n' \
  '        if (nset != null) {\r\n' \
  '          q = "set=" + encodeURIComponent(nset);\r\n' \
  '        } else {\r\n' \
  '          q = "matrix=" + encodeURIComponent(tlevels[nlevel][0].toString());\r\n' \
  '        }\r\n' \
  '        xhrt.onload = (e) => {load_tcb(e.target, nset, nlevel, kzoom)};\r\n' \
  '        xhrt.open("GET", "/tiles/switch?" + q);\r\n' \
  '        xhrt.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhrt.send();\r\n' \
  '      }\r\n' \
  '      function add_tile(row=0, col=0) {\r\n' \
  '        let tile = document.createElement("img");\r\n' \
  '        if (mode == "map") {\r\n' \
  '          tile.id = "map";\r\n' \
  '          tile.src = "/map/" + tile.id + text;\r\n' \
  '        } else {\r\n' \
  '          tile.id = "tile-" + row.toString() + "-" + col.toString();\r\n' \
  '          let port = portmin + (row + col) % (portmax + 1 - portmin);\r\n' \
  '          tile.src = "http://" + location.hostname + ":" + port.toString() + "/tiles/" + tile.id + text + "?" + document.getElementById("tset").selectedIndex.toString() + "," + document.getElementById("matrix").innerHTML;\r\n' \
  '        }\r\n' \
  '        tile.alt = "";\r\n' \
  '        tile.style.position = "absolute";\r\n' \
  '        tile.style.width = "calc(var(--zoom) * " + twidth.toString() + "px)";\r\n' \
  '        tile.style.height = "calc(var(--zoom) * " + theight.toString() + "px)";\r\n' \
  '        tile.style.left = "calc(var(--zoom) * " + ((ttopx - htopx) / tscale + col * twidth).toString() + "px)";\r\n' \
  '        tile.style.top = "calc(var(--zoom) * " + ((htopy - ttopy) / tscale + row * theight).toString() + "px";\r\n' \
  '        handle.insertBefore(tile, handle.firstElementChild);\r\n' \
  '      }\r\n' \
  '      function update_tiles() {\r\n' \
  '        if (mode == "map") {return;}\r\n' \
  '        let vleft = -hpx / zoom + (htopx - ttopx) / tscale;\r\n' \
  '        let vtop = -hpy / zoom + (ttopy - htopy) / tscale;\r\n' \
  '        let vright = vleft + viewpane.offsetWidth / zoom;\r\n' \
  '        let vbottom = vtop + viewpane.offsetHeight / zoom;\r\n' \
  '        let tiles = handle.getElementsByTagName("img");\r\n' \
  '        let rleft = parseInt(vleft / twidth - 1.5);\r\n' \
  '        let rright = parseInt(vright / twidth + 1.5);\r\n' \
  '        let rtop = parseInt(vtop / theight - 1.5);\r\n' \
  '        let rbottom = parseInt(vbottom / theight + 1.5);\r\n' \
  '        if (cleft == null) {\r\n' \
  '          let i = tiles.length - 1;\r\n' \
  '            while (i >= 0) {\r\n' \
  '              handle.removeChild(tiles[i]);\r\n' \
  '              i--;\r\n' \
  '            } \r\n' \
  '          cleft = rleft - 1;\r\n' \
  '          cright = rleft - 1;\r\n' \
  '          ctop = rtop - 1;\r\n' \
  '          cbottom = rtop - 1;\r\n' \
  '        }\r\n' \
  '        let i = tiles.length - 1;\r\n' \
  '        if (rleft != cleft || rright != cright || rtop != ctop || rbottom != cbottom) {\r\n' \
  '          while (i >= 0) {\r\n' \
  '            let [r, c] = tiles[i].id.split("-").slice(1, 3);\r\n' \
  '            let row = parseInt(r);\r\n' \
  '            let col = parseInt(c);\r\n' \
  '            if (row < rtop || row > rbottom || col < rleft || col > rright) {\r\n' \
  '              handle.removeChild(tiles[i]);\r\n' \
  '            }\r\n' \
  '            i--;\r\n' \
  '          } \r\n' \
  '          for (let col=rleft; col<cleft; col++) {\r\n' \
  '            for (let row=Math.max(ctop, rtop); row<=Math.min(cbottom, rbottom); row++) {add_tile(row, col);}\r\n' \
  '          }\r\n' \
  '          for (let col=cright+1; col<=rright; col++) {\r\n' \
  '            for (let row=Math.max(ctop, rtop); row<=Math.min(cbottom, rbottom); row++) {add_tile(row, col);}\r\n' \
  '          }\r\n' \
  '          cleft = rleft;\r\n' \
  '          cright = rright;\r\n' \
  '          for (let row=rtop; row<ctop; row++) {\r\n' \
  '            for (let col=cleft; col<=cright; col++) {add_tile(row, col);}\r\n' \
  '          }\r\n' \
  '          for (let row=cbottom + 1; row<=rbottom; row++) {\r\n' \
  '            for (let col=cleft; col<=cright; col++) {add_tile(row, col);}\r\n' \
  '          }\r\n' \
  '          ctop = rtop;\r\n' \
  '          cbottom = rbottom;\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function reframe() {\r\n' \
  '        hpx = Math.round(Math.min(Math.max(hpx, (htopx - vmaxx) * zoom / tscale + viewpane.offsetWidth), (htopx - vminx) * zoom / tscale));\r\n' \
  '        hpy = Math.round(Math.min(Math.max(hpy, (vminy - htopy) * zoom / tscale + viewpane.offsetHeight), (vmaxy - htopy) * zoom / tscale));\r\n' \
  '        handle.style.left = hpx.toString() + "px";\r\n' \
  '        handle.style.top = hpy.toString() + "px";\r\n' \
  '        let k = Math.cosh((htopy + (hpy - viewpane.offsetHeight) * tscale / zoom) / 6378137);\r\n' \
  '        let sc = 150 * tscale / zoom / k;\r\n' \
  '        let unit = "m";\r\n' \
  '        let b = 1;\r\n' \
  '        if (sc >= 1000) {\r\n' \
  '          unit = "km";\r\n' \
  '          b = 1000;\r\n' \
  '        } else if (sc < 0.1) {\r\n' \
  '          unit = "mm";\r\n' \
  '          b = 1/1000;\r\n' \
  '        } else if (sc < 1) {\r\n' \
  '          unit = "cm";\r\n' \
  '          b = 1/100;\r\n' \
  '        }\r\n' \
  '        let sc_c = (sc / b).toFixed(0);\r\n' \
  '        let sc_s = "";\r\n' \
  '        if (sc_c[0] == "1") {\r\n' \
  '          sc_s = "1".padEnd(sc_c.length, "0");\r\n' \
  '        } else if (sc_c[0] == "2" || sc_c[0] == "3" || sc_c[0] == "4") {\r\n' \
  '          sc_s = "2".padEnd(sc_c.length, "0");\r\n' \
  '        } else {\r\n' \
  '          sc_s = "5".padEnd(sc_c.length, "0");\r\n' \
  '        }\r\n' \
  '        sc = parseFloat(sc_s) * b;\r\n' \
  '        document.getElementById("scaleline").setAttribute("width", (sc / tscale * zoom * k).toFixed(0) + "px");\r\n' \
  '        document.getElementById("scalevalue").innerHTML = sc_s + " " + unit;\r\n' \
  '        update_tiles() \r\n' \
  '      }\r\n' \
  '      function prop_to_wmvalue(s) {\r\n' \
  '        return parseFloat(s.match(/-?\\d+[.]?\\d*/)[0]);\r\n' \
  '      }\r\n' \
  '      function wmvalue_to_prop(v, o=0) {\r\n' \
  '        if (o) {\r\n' \
  '          return "calc(" + v.toFixed(1) + "px / var(--scale) - " + o.toString() + "px)";\r\n' \
  '        } else {\r\n' \
  '          return "calc(" + v.toFixed(1) + "px / var(--scale))";\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function scroll_view(x, y) {\r\n' \
  '        hpx = viewpane.offsetWidth / 2 + (htopx - x) * zoom / tscale;\r\n' \
  '        hpy = viewpane.offsetHeight / 2 + (y - htopy) * zoom / tscale;\r\n' \
  '        reframe();\r\n' \
  '      }\r\n' \
  '      function scroll_dview(dx, dy) {\r\n' \
  '        hpx += dx;\r\n' \
  '        hpy += dy;\r\n' \
  '        reframe();\r\n' \
  '      }\r\n' \
  '      function scroll_to_dot(dot) {\r\n' \
  '        scroll_view(htopx + prop_to_wmvalue(dot.style.left), htopy - prop_to_wmvalue(dot.style.top));\r\n' \
  '      }\r\n' \
  '      function track_center(track=null) {\r\n' \
  '        let tracks = [];\r\n' \
  '        if (track != null) {\r\n' \
  '          tracks.push(track);\r\n' \
  '        } else {\r\n' \
  '          let segs = document.getElementById("pointsform").children;\r\n' \
  '          for (let s=0; s<segs.length; s++) {\r\n' \
  '            if (segs[s].firstElementChild.checked) {\r\n' \
  '              tracks.push(document.getElementById("track" + segs[s].id.slice(7, -4)));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        let gminx = null;\r\n' \
  '        let gminy = null;\r\n' \
  '        let gmaxx = null;\r\n' \
  '        let gmaxy = null;\r\n' \
  '        for (let t=0; t<tracks.length; t++) {\r\n' \
  '          let d = tracks[t].firstElementChild.getAttribute("d").match(/[LMm] *\d+([.]\d*)? +\d+([.]\d*)?/g);\r\n' \
  '          let minx = null;\r\n' \
  '          let miny = null;\r\n' \
  '          let maxx = null;\r\n' \
  '          let maxy = null;\r\n' \
  '          for (let p=1; p<d.length; p++) {\r\n' \
  '            if (d[p][0] != "m") {\r\n' \
  '              let pt = d[p].substring(1).replace(/ +/g, " ").split(" ").map(Number);\r\n' \
  '              if (minx == null) {\r\n' \
  '                [minx, miny] = pt;\r\n' \
  '                [maxx, maxy] = pt;\r\n' \
  '              } else {\r\n' \
  '                minx = Math.min(minx, pt[0]);\r\n' \
  '                miny = Math.min(miny, pt[1]);\r\n' \
  '                maxx = Math.max(maxx, pt[0]);\r\n' \
  '                maxy = Math.max(maxy, pt[1]);\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (minx != null) {\r\n' \
  '            if (gminx == null) {\r\n' \
  '              gminx = prop_to_wmvalue(tracks[t].style.left) + minx;\r\n' \
  '              gminy = prop_to_wmvalue(tracks[t].style.top) + miny;\r\n' \
  '              gmaxx = prop_to_wmvalue(tracks[t].style.left) + maxx;\r\n' \
  '              gmaxy = prop_to_wmvalue(tracks[t].style.top) + maxy;\r\n' \
  '            } else {\r\n' \
  '              gminx = Math.min(gminx, prop_to_wmvalue(tracks[t].style.left) + minx);\r\n' \
  '              gminy = Math.min(gminy, prop_to_wmvalue(tracks[t].style.top) + miny);\r\n' \
  '              gmaxx = Math.max(gmaxx, prop_to_wmvalue(tracks[t].style.left) + maxx);\r\n' \
  '              gmaxy = Math.max(gmaxy, prop_to_wmvalue(tracks[t].style.top) + maxy);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (gminx == null) {\r\n' \
  '          return null;\r\n' \
  '        } else {\r\n' \
  '          return [(gminx + gmaxx) / 2, (gminy + gmaxy) / 2];\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function scroll_to_track(track) {\r\n' \
  '        let c = track_center(track);\r\n' \
  '        if (c == null) {return;}\r\n' \
  '        scroll_view(htopx + c[0], htopy - c[1]);\r\n' \
  '      }\r\n' \
  '      function scroll_to_all() {\r\n' \
  '        let c = track_center();\r\n' \
  '        if (c == null) {\r\n' \
  '          scroll_view(defx, defy);\r\n' \
  '        } else {\r\n' \
  '          scroll_view(htopx + c[0], htopy - c[1]); \r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function dot_style(pt, over) {\r\n' \
  '        if (pt.indexOf("point") < 0) {return;}\r\n' \
  '        let dot = document.getElementById(pt.replace("point", "dot"))\r\n' \
  '        if (document.getElementById(pt).value == "error") {\r\n' \
  '          dot.style.stroke = "";\r\n' \
  '          dot.style.display = "none";\r\n' \
  '          dot.style.zIndex = "";\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let segcb = true;\r\n' \
  '        if (pt.substring(0, 3) != "way") {segcb = document.getElementById(pt).parentNode.parentNode.firstElementChild.checked;}\r\n' \
  '        let cb = document.getElementById(pt).checked;\r\n' \
  '        if (pt == focused) {\r\n' \
  '          dot.style.stroke = "blue";\r\n' \
  '          dot.style.display = "";\r\n' \
  '          dot.style.zIndex = "1";\r\n' \
  '        } else if (!cb || !segcb) {\r\n' \
  '          dot.style.stroke = "";\r\n' \
  '          dot.style.display = "none";\r\n' \
  '          dot.style.zIndex = "";\r\n' \
  '        } else if (over) {\r\n' \
  '          dot.style.stroke = "green";\r\n' \
  '          dot.style.display = "";\r\n' \
  '          dot.style.zIndex = "2";\r\n' \
  '        } else if (dots_visible) {\r\n' \
  '          dot.style.stroke = "";\r\n' \
  '          dot.style.display = "";\r\n' \
  '          dot.style.zIndex = "";\r\n' \
  '        } else {\r\n' \
  '          dot.style.stroke = "";\r\n' \
  '          dot.style.display = "none";\r\n' \
  '          dot.style.zIndex = "";\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function save_old() {\r\n' \
  '        if (! focused) {return;}\r\n' \
  '        if (focused.indexOf("point") < 0) {return;}\r\n' \
  '        let elt_foc = document.getElementById(focused + "focus");\r\n' \
  '        let c = "";\r\n' \
  '        let inputs = elt_foc.getElementsByTagName("input");\r\n' \
  '        for (let i=0; i<inputs.length;i++) {c = c + inputs[i].value + "\\r\\n";}\r\n' \
  '        foc_old = c;\r\n' \
  '      }\r\n' \
  '      function element_click(e, elt, scroll=true) {\r\n' \
  '        if (e != null) {e.preventDefault();}\r\n' \
  '        let ex_foc = focused;\r\n' \
  '        if (elt.htmlFor == ex_foc) {focused = "";} else {focused = elt.htmlFor;}\r\n' \
  '        if (ex_foc != "") {\r\n' \
  '          document.getElementById(ex_foc + "desc").style.color = "";\r\n' \
  '          if (ex_foc.indexOf("point") >= 0) {\r\n' \
  '            document.getElementById(ex_foc + "focus").style.display = "";\r\n' \
  '            dot_style(ex_foc, elt.htmlFor == ex_foc);\r\n' \
  '          }\r\n' \
  '          if (ex_foc.substring(0, 3) == "way") {\r\n' \
  '            document.getElementById("points").style.height = "88%";\r\n' \
  '            document.getElementById("waypoints").style.maxHeight = "10vh";\r\n' \
  '            document.getElementById("points").style.height = "calc(100% - " + document.getElementById("waypoints").offsetHeight.toString() + "px)";\r\n' \
  '          }\r\n' \
  '          if (ex_foc.substring(0, 3) == "seg") {\r\n' \
  '            let track = document.getElementById(ex_foc.replace("segment", "track"));\r\n' \
  '            track.style.stroke = "";\r\n' \
  '            track.style.fill = "";\r\n' \
  '            if (document.getElementById(ex_foc).checked) {\r\n' \
  '              track.style.display = "";\r\n' \
  '            } else {\r\n' \
  '              track.style.display = "none";\r\n' \
  '            }\r\n' \
  '            track.style.zIndex = "";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (focused) {\r\n' \
  '          elt.style.color = "dodgerblue";\r\n' \
  '          let elt_foc = null;\r\n' \
  '          if (focused.indexOf("point") >= 0) {\r\n' \
  '            save_old();\r\n' \
  '            elt_foc = document.getElementById(elt.htmlFor + "focus");\r\n' \
  '            elt_foc.style.display = "inline";\r\n' \
  '            dot_style(focused, elt.htmlFor == ex_foc);\r\n' \
  '          }\r\n' \
  '          if (focused.substring(0, 3) == "way") {\r\n' \
  '            document.getElementById("points").style.height = "calc(100% - 10em)";\r\n' \
  '            document.getElementById("waypoints").style.maxHeight = "10em";\r\n' \
  '            document.getElementById("points").style.height = "calc(100% - " + document.getElementById("waypoints").offsetHeight.toString() + "px)";\r\n' \
  '          }\r\n' \
  '          if (focused.substring(0, 3) == "seg") {\r\n' \
  '            let track = document.getElementById(focused.replace("segment", "track"));\r\n' \
  '            track.style.stroke = "blue";\r\n' \
  '            track.style.fill = "blue";\r\n' \
  '            track.style.display = "";\r\n' \
  '            track.style.zIndex = "1";\r\n' \
  '            if (scroll) {elt.scrollIntoView({block:"start"});}\r\n' \
  '            scroll_to_track(track);\r\n' \
  '          } else if (scroll) {\r\n' \
  '            elt.scrollIntoView({block:"nearest"});\r\n' \
  '            elt_foc.scrollIntoView({block:"nearest"});\r\n' \
  '            let par_c = true;\r\n' \
  '            if (focused.substring(0, 3) != "way") {par_c = elt.parentNode.parentNode.firstElementChild.checked;}\r\n' \
  '            if (((! document.getElementById(focused).checked || ! par_c)) && document.getElementById(focused).value != "error") {\r\n' \
  '              scroll_to_dot(document.getElementById(focused.replace("point", "dot")));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        graph_point();\r\n' \
  '      }\r\n' \
  '      function WGS84toWebMercator(lat, lon) {\r\n' \
  '        return [lon * Math.PI / 180 * 6378137, Math.log(Math.tan(Math.PI / 4 + lat * Math.PI / 360)) * 6378137];\r\n' \
  '      }\r\n' \
  '      function WebMercatortoWGS84(x, y) {\r\n' \
  '        return [(2 * Math.atan(Math.exp(y / 6378137)) - Math.PI / 2) * 180 / Math.PI, x * 180 / Math.PI / 6378137];\r\n' \
  '      }\r\n' \
  '      function point_to_position(pt) {\r\n' \
  '        let lat = parseFloat(document.getElementById(pt.htmlFor + "lat").value);\r\n' \
  '        let lon = parseFloat(document.getElementById(pt.htmlFor + "lon").value);\r\n' \
  '        let wm = WGS84toWebMercator(lat, lon);\r\n' \
  '        let o = "3.5";\r\n' \
  '        if (pt.id.substring(0, 3) == "way") {o = "4";}\r\n' \
  '        return [wmvalue_to_prop(wm[0] - htopx, o), wmvalue_to_prop(htopy - wm[1], o)];\r\n' \
  '      }\r\n' \
  '      function dpixels_to_point(dx, dy) {\r\n' \
  '        if (focused.indexOf("point") < 0) {return;}\r\n' \
  '        let lat = parseFloat(document.getElementById(focused + "lat").value);\r\n' \
  '        let lon = parseFloat(document.getElementById(focused + "lon").value);\r\n' \
  '        let wm = WGS84toWebMercator(lat, lon);\r\n' \
  '        wm[0] += dx * tscale / zoom;\r\n' \
  '        wm[0] = Math.max(Math.min(wm[0], vmaxx - 1), vminx + 1);\r\n' \
  '        wm[1] -= dy * tscale / zoom;\r\n' \
  '        wm[1] = Math.max(Math.min(wm[1], vmaxy - 1), vminy + 1);\r\n' \
  '        [lat, lon] = WebMercatortoWGS84(...wm);\r\n' \
  '        document.getElementById(focused + "lat").value = lat.toFixed(6);\r\n' \
  '        document.getElementById(focused + "lon").value = lon.toFixed(6);\r\n' \
  '        point_edit(false, false, false, true);\r\n' \
  '      }\r\n' \
  '      function rebase_track(x, y, track, exact=false, batch=false) {\r\n' \
  '        if (mode == "map") {return;}\r\n' \
  '        let path = track.firstElementChild;\r\n' \
  '        let minx = wmb;\r\n' \
  '        let maxx = -wmb;\r\n' \
  '        let miny = wmb;\r\n' \
  '        let maxy = -wmb;\r\n' \
  '        if (path.getAttribute("d").length > 4) {\r\n' \
  '          minx = prop_to_wmvalue(track.style.left) + htopx;\r\n' \
  '          maxy = htopy - prop_to_wmvalue(track.style.top);\r\n' \
  '          maxx = minx + prop_to_wmvalue(track.style.width);\r\n' \
  '          miny = maxy - prop_to_wmvalue(track.style.height);\r\n' \
  '        }\r\n' \
  '        let viewbox = track.getAttribute("viewBox").split(" ");\r\n' \
  '        let minx_ex = minx;\r\n' \
  '        let maxy_ex = maxy;\r\n' \
  '        let vb = false;\r\n' \
  '        let padding = 1000;\r\n' \
  '        if (exact) {padding = 0;}\r\n' \
  '        if (x < minx) {\r\n' \
  '          minx = Math.max(vminx, -wmb, x - padding);\r\n' \
  '          track.style.left = wmvalue_to_prop(minx - htopx);\r\n' \
  '          track.style.width = wmvalue_to_prop(maxx - minx);\r\n' \
  '          viewbox[2] = (maxx - minx).toFixed(1);\r\n' \
  '          vb = true;\r\n' \
  '        }\r\n' \
  '        if (x > maxx) {\r\n' \
  '          maxx = Math.min(vmaxx, wmb, x + padding);\r\n' \
  '          track.style.width = wmvalue_to_prop(maxx - minx);\r\n' \
  '          viewbox[2] = (maxx - minx).toFixed(1);\r\n' \
  '          vb = true;\r\n' \
  '        }\r\n' \
  '        if (y > maxy) {\r\n' \
  '          maxy = Math.min(vmaxy, wmb, y + padding);\r\n' \
  '          track.style.top = wmvalue_to_prop(htopy - maxy);\r\n' \
  '          track.style.height = wmvalue_to_prop(maxy - miny);\r\n' \
  '          viewbox[3] = (maxy - miny).toFixed(1);\r\n' \
  '          vb = true;\r\n' \
  '        }\r\n' \
  '        if (y < miny) {\r\n' \
  '          miny = Math.max(vminy, -wmb, y - padding);\r\n' \
  '          track.style.height = wmvalue_to_prop(maxy - miny);\r\n' \
  '          viewbox[3] = (maxy - miny).toFixed(1);\r\n' \
  '          vb = true;\r\n' \
  '        }\r\n' \
  '        if (vb) {track.setAttribute("viewBox", viewbox.join(" "));}\r\n' \
  '        if (! batch) {\r\n' \
  '          if (minx_ex != minx || maxy_ex != maxy) {\r\n' \
  '            let d_ex = path.getAttribute("d").substring(4);\r\n' \
  '            let d = "M0 0";\r\n' \
  '            let points = d_ex.match(/[LMm] *\\d+([.]\\d*)? +\\d+([.]\\d*)?/g);\r\n' \
  '            if (points != null) {\r\n' \
  '              for (let point of points) {\r\n' \
  '                let [px, py] = point.match(/\\d+([.]\\d*)?/g);\r\n' \
  '                d = d + " " + point[0] + (parseFloat(px) + minx_ex - minx).toFixed(1) + " " + (parseFloat(py) + maxy - maxy_ex).toFixed(1);\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            path.setAttribute("d", d);\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          if (minx_ex != minx || maxy_ex != maxy) {\r\n' \
  '            return [minx_ex - minx, maxy - maxy_ex];\r\n' \
  '          } else {\r\n' \
  '            return null;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function WGS84_to_viewbox(lat, lon, track) {\r\n' \
  '        let [x, y] = WGS84toWebMercator(lat, lon);\r\n' \
  '        rebase_track(x, y, track);\r\n' \
  '        return (x - prop_to_wmvalue(track.style.left) - htopx).toFixed(1) + " " + (htopy - prop_to_wmvalue(track.style.top) - y).toFixed(1)\r\n' \
  '      }\r\n' \
  '      function escape(s) {\r\n' \
  '        return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");\r\n' \
  '      }\r\n' \
  '      function point_desc(ptspan = null) {\r\n' \
  '        if (! ptspan) {\r\n' \
  '          let points = document.getElementById("content").getElementsByTagName("span");\r\n' \
  '          for (let p=2; p<points.length; p++) {\r\n' \
  '            points[p].parentNode.firstElementChild.nextElementSibling.innerHTML = point_desc(points[p]);\r\n' \
  '          }\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let chld = ptspan.children;\r\n' \
  '        let lat = parseFloat(chld[1].value).toFixed(4);\r\n' \
  '        let lon = parseFloat(chld[4].value).toFixed(4);\r\n' \
  '        let time_ = Date.parse(chld[(ptspan.id.substring(0, 3) == "way")?10:13].value);\r\n' \
  '        let time = isNaN(time_)?"":time_conv.format(time_)  + "˙" + date_conv.format(time_);\r\n' \
  '        if (ptspan.id.substring(0, 3) == "way") {\r\n' \
  '          let ele = chld[7].value==""?"":parseFloat(chld[7].value).toFixed(0);\r\n' \
  '          let name = chld[13].value;\r\n' \
  '          return escape("(" + lat + ", " + lon + ") " + ele + " " + time) + "<br>" + escape(name);\r\n' \
  '        } else {\r\n' \
  '          let ele = chld[7].value==""?"...":parseFloat(chld[7].value).toFixed(0);\r\n' \
  '          let alt = chld[10].value==""?"":parseFloat(chld[10].value).toFixed(0);\r\n' \
  '          return escape("(" + lat + ", " + lon + ") " + ele + " " + alt + " " + time);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function point_edit(scroll=true, cancel=true, recalc=true, coord=true) {\r\n' \
  '        let pt = document.getElementById(focused + "desc");\r\n' \
  '        let pt_cb = document.getElementById(focused);\r\n' \
  '        let valid = false;\r\n' \
  '        if (cancel) {\r\n' \
  '          hist[0].push([focused, foc_old]);\r\n' \
  '          save_old();\r\n' \
  '          for (let i=hist[1].length - 1; i>=0 ;i--) {\r\n' \
  '            if (hist[1][i][0] == focused) {hist[1].splice(i, 1);}\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (focused.substring(0, 3) == "way") {\r\n' \
  '          valid = document.getElementById(focused + "lat").checkValidity() && document.getElementById(focused + "lon").checkValidity() && document.getElementById(focused + "ele").checkValidity() && document.getElementById(focused + "time").checkValidity() && document.getElementById(focused + "name").checkValidity();\r\n' \
  '        } else {\r\n' \
  '          valid = document.getElementById(focused + "lat").checkValidity() && document.getElementById(focused + "lon").checkValidity() && document.getElementById(focused + "ele").checkValidity() && document.getElementById(focused + "alt").checkValidity() && document.getElementById(focused + "time").checkValidity();\r\n' \
  '        } \r\n' \
  '        let wm = null;\r\n' \
  '        if (valid) {\r\n' \
  '          wm = WGS84toWebMercator(parseFloat(document.getElementById(focused + "lat").value), parseFloat(document.getElementById(focused + "lon").value));\r\n' \
  '          valid = wm[0] > vminx && wm[0] < vmaxx && wm[1] > vminy && wm[1] < vmaxy;\r\n' \
  '        }\r\n' \
  '        if (valid) {\r\n' \
  '          if (pt_cb.checked) {\r\n' \
  '            pt.style.textDecoration = "inherit";\r\n' \
  '          } else {\r\n' \
  '            pt.style.textDecoration = "line-through";\r\n' \
  '          }\r\n' \
  '          document.getElementById(focused + "desc").innerHTML = point_desc(document.getElementById(focused + "focus"));\r\n' \
  '          if (pt_cb.value != "error") {pt_cb.value = "edited";}\r\n' \
  '          if (coord || pt_cb.value == "error") {\r\n' \
  '            let dot = document.getElementById(focused.replace("point", "dot"));\r\n' \
  '            [dot.style.left, dot.style.top] = point_to_position(pt);\r\n' \
  '            if (pt_cb.value == "error") {\r\n' \
  '              pt_cb.disabled = false;\r\n' \
  '              pt_cb.value = "edited";\r\n' \
  '              if (pt_cb.checked) {point_undelete(pt_cb);} else {dot_style(focused, true);}\r\n' \
  '            } else {\r\n' \
  '              if (scroll) {scroll_to_dot(dot);}\r\n' \
  '              if (focused.substring(0, 3) != "way" && pt_cb.checked) {\r\n' \
  '                let seg = pt.parentNode.parentNode;\r\n' \
  '                let track = document.getElementById("track" + seg.id.slice(7, -4));\r\n' \
  '                let np = WGS84_to_viewbox(parseFloat(document.getElementById(focused + "lat").value), parseFloat(document.getElementById(focused + "lon").value), track);\r\n' \
  '                let path = document.getElementById("path" + seg.id.slice(7, -4));\r\n' \
  '                let spans = seg.getElementsByTagName("span");\r\n' \
  '                let ind = 0;\r\n' \
  '                while (spans[ind].id != focused + "focus") {ind++;}\r\n' \
  '                let d = path.getAttribute("d");\r\n' \
  '                let d_left = d.match("( *[LMm] *\\\\d+([.]\\\\d*)? +\\\\d+([.]\\\\d*)? *){" + (ind + 2).toString() + "}");\r\n' \
  '                let d_right = d.slice(d_left[0].length);\r\n' \
  '                if (d_right.length > 0) {d_right = " " + d_right;}\r\n' \
  '                d = d_left[0].slice(0, -d_left[1].length) + d_left[1][0] + np + d_right;\r\n' \
  '                path.setAttribute("d", d);\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          if (pt_cb.value != "error") {\r\n' \
  '            pt_cb.disabled = true;\r\n' \
  '            pt_cb.value = "error";\r\n' \
  '            if (pt_cb.checked) {point_delete(pt_cb);} else {dot_style(focused, true);}\r\n' \
  '            pt.style.textDecoration = "line-through red";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (recalc && focused.substring(0, 3) != "way") {segments_calc(pt.parentNode.parentNode);}\r\n' \
  '      }\r\n' \
  '      function point_over(pt) {\r\n' \
  '        let foc = null;\r\n' \
  '        if (pt.id.indexOf("desc") < 0) {foc = pt.id;} else {foc = pt.htmlFor;}\r\n' \
  '        let par_c = true;\r\n' \
  '        if (foc.substring(0, 3) != "way") {par_c = pt.parentNode.parentNode.firstElementChild.checked;}\r\n' \
  '        dot_style(foc, true);\r\n' \
  '        if (((document.getElementById(foc).checked && par_c) || foc == focused) && document.getElementById(foc).value != "error") {\r\n' \
  '          scroll_to_dot(document.getElementById(foc.replace("point", "dot")));\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function point_outside(pt) {\r\n' \
  '        let foc = null;\r\n' \
  '        if (pt.id.indexOf("desc") < 0) {foc = pt.id;} else {foc = pt.htmlFor;}\r\n' \
  '        dot_style(foc, false);\r\n' \
  '      }\r\n' \
  '      function undo(redo, whole) {\r\n' \
  '        let s = redo?1:0;\r\n' \
  '        if (hist[s].length == 0) {return;}\r\n' \
  '        let ex_foc = focused;\r\n' \
  '        if (whole && focused) {element_click(null, document.getElementById(focused + "desc"), false);}\r\n' \
  '        let ind = null;\r\n' \
  '        let histb = 0;\r\n' \
  '        let inds=[];\r\n' \
  '        if (! focused) {\r\n' \
  '          ind = hist[s].length - 1;\r\n' \
  '          if (hist[s][ind].length >= 3) {histb = hist[s][ind][2];}\r\n' \
  '          if (histb > 0) {\r\n' \
  '            for (let i=hist[s].length-1; i>=0; i--) {\r\n' \
  '              if (hist[s][i].length >= 3) {\r\n' \
  '                if (hist[s][i][2] == histb) {inds.push(i);}\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            inds = [ind];\r\n' \
  '          }\r\n' \
  '        } else if (focused.indexOf("point") < 0) {\r\n' \
  '          for (let i=hist[s].length-1; i>=0; i--) {\r\n' \
  '            if (document.getElementById(hist[s][i][0] + "cont").parentNode.id == focused + "cont") {\r\n' \
  '              if (ind == null && hist[s][i].length >= 3) {histb = hist[s][i][2];}\r\n' \
  '              ind = i;\r\n' \
  '              if (histb > 0) {\r\n' \
  '                if (hist[s][i].length >= 3) {\r\n' \
  '                  if (hist[s][i][2] == histb) {inds.push(i);}\r\n' \
  '                }\r\n' \
  '              } else {\r\n' \
  '                inds = [ind];\r\n' \
  '                break;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (ind == null) {return;}\r\n' \
  '          histb = ++hist_b;\r\n' \
  '        } else {\r\n' \
  '          for (let i=hist[s].length-1; i>=0; i--) {\r\n' \
  '            if (hist[s][i][0] == focused) {\r\n' \
  '              ind = i;\r\n' \
  '              inds = [ind];\r\n' \
  '              break;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (ind == null) {return;}\r\n' \
  '          element_click(null, document.getElementById(focused + "desc"), false);\r\n' \
  '        }\r\n' \
  '        let gr = document.getElementById("graph").style.display != "none";\r\n' \
  '        if (gr) {refresh_graph(true);}\r\n' \
  '        document.getElementById("graph").style.display = "none";\r\n' \
  '        let segments= null;\r\n' \
  '        let points = null;\r\n' \
  '        for (let ind_=0; ind_<inds.length; ind_++) {\r\n' \
  '          ind = inds[ind_];\r\n' \
  '          focused = hist[s][ind][0];\r\n' \
  '          let elt_foc = document.getElementById(focused);\r\n' \
  '          let err = elt_foc.value == "error";\r\n' \
  '          if (hist[s][ind][1] != "") {\r\n' \
  '            let c = hist[s][ind][1].split("\\r\\n");\r\n' \
  '            save_old();\r\n' \
  '            if (histb == 0) {\r\n' \
  '              hist[1-s].push([focused, foc_old]);\r\n' \
  '            } else {\r\n' \
  '              hist[1-s].push([focused, foc_old, histb]);\r\n' \
  '            }\r\n' \
  '            let inputs = document.getElementById(focused + "focus").getElementsByTagName("input");\r\n' \
  '            let coord = (inputs[0].value != c[0]) || (inputs[1].value != c[1]);\r\n' \
  '            for (let i=0; i<inputs.length;i++) {inputs[i].value = c[i];}\r\n' \
  '            save_old();\r\n' \
  '            point_edit(false, false, histb == 0, coord);\r\n' \
  '            if (err && elt_foc.value != "error") {\r\n' \
  '              focused = "";\r\n' \
  '              dot_style(hist[s][ind][0], false);\r\n' \
  '              focused = hist[s][ind][0];\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            if (histb == 0) {\r\n' \
  '              hist[1-s].push([focused, ""]);\r\n' \
  '            } else {\r\n' \
  '              hist[1-s].push([focused, "", histb]);\r\n' \
  '              if (segments == null) {\r\n' \
  '                segments= Array(document.getElementById("pointsform").children.length).fill(false);\r\n' \
  '                points = Array(document.getElementById("points").getElementsByTagName("span").length).fill(false);\r\n' \
  '              }\r\n' \
  '              segments[parseInt(document.getElementById(focused + "cont").parentNode.id.substring(7))] = true;\r\n' \
  '              points[parseInt(focused.substring(5))] = true;\r\n' \
  '            }\r\n' \
  '            document.getElementById(focused).checked = redo;\r\n' \
  '            focused = "";\r\n' \
  '            point_checkbox(document.getElementById(hist[s][ind][0]), histb != 0);\r\n' \
  '            if (histb == 0) {dot_style(hist[s][ind][0], false)};\r\n' \
  '            focused = hist[s][ind][0];\r\n' \
  '          }\r\n' \
  '          hist[s].splice(ind, 1);\r\n' \
  '        }\r\n' \
  '        if (segments != null) {\r\n' \
  '          for (let s=0; s<segments.length; s++) {\r\n' \
  '            if (! segments[s]) {continue;}\r\n' \
  '            let track = document.getElementById("track" + s.toString());\r\n' \
  '            let path = document.getElementById("path" + s.toString());\r\n' \
  '            let pt = document.getElementById("segment" + s.toString() + "cont").firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling;\r\n' \
  '            let d = path.getAttribute("d");\r\n' \
  '            let dots = d.match(/[LMm] *\d+([.]\d*)? +\d+([.]\d*)?/g);\r\n' \
  '            let d_r = "M0 0";\r\n' \
  '            for (let p=1; p<dots.length; p++) {\r\n' \
  '              if (! points[parseInt(pt.id.substring(5))]) {\r\n' \
  '                d_r = d_r + " " + dots[p];\r\n' \
  '              } else if (redo) {\r\n' \
  '                let np = WGS84_to_viewbox(parseFloat(document.getElementById(pt.id.replace("cont", "lat")).value), parseFloat(document.getElementById(pt.id.replace("cont", "lon")).value), track);\r\n' \
  '                d_r = d_r + " L" + np;\r\n' \
  '              } else {\r\n' \
  '                d_r = d_r + " m0 0";\r\n' \
  '              }\r\n' \
  '              pt = pt.nextElementSibling;\r\n' \
  '            }\r\n' \
  '            if (d_r.substring(1).indexOf("M") < 0) {d_r = d_r.replace("L", "M");}\r\n' \
  '            path.setAttribute("d", d_r);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (hist_b !=0) {segments_calc();}\r\n' \
  '        let ex_foc_ = focused;\r\n' \
  '        focused = "";\r\n' \
  '        if (ex_foc) {element_click(null, document.getElementById(ex_foc + "desc"), false);}\r\n' \
  '        if (gr) {refresh_graph(true);}\r\n' \
  '        if (ex_foc.indexOf("point") < 0) {\r\n' \
  '          scroll_to_dot(document.getElementById(ex_foc_.replace("point", "dot")));\r\n' \
  '          document.getElementById(ex_foc_ + "cont").scrollIntoView({block:"center"});\r\n' \
  '        } else {\r\n' \
  '          document.getElementById(ex_foc + "cont").scrollIntoView({block:"nearest"});\r\n' \
  '        }\r\n' \
  '        if (hist[1-s][hist[1-s].length-1][1] == "") {\r\n' \
  '          show_msg((redo?"{#jmredo1#}":"{#jmundo1#}").replace("%s", inds.length), 3);\r\n' \
  '        } else {\r\n' \
  '          show_msg((redo?"{#jmredo2#}":"{#jmundo2#}").replace("%s", inds.length), 3);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function point_insert(pos, coord=null) {\r\n' \
  '        let ex_foc = "";\r\n' \
  '        if (focused) {\r\n' \
  '          if (document.getElementById(focused).value == "error") {return;}\r\n' \
  '          ex_foc = focused;\r\n' \
  '          element_click(null, document.getElementById(focused + "desc"), false);\r\n' \
  '          dot_style(ex_foc, false);\r\n' \
  '        }\r\n' \
  '        let el_cont = null;\r\n' \
  '        let el_dot = null;\r\n' \
  '        let seg = "";\r\n' \
  '        let ref = null;\r\n' \
  '        let par = null;\r\n' \
  '        if (ex_foc.substring(0, 3) == "seg") {\r\n' \
  '          seg = document.getElementById(ex_foc).parentNode;\r\n' \
  '          if (document.getElementById(ex_foc).nextElementSibling.nextElementSibling.nextElementSibling) {\r\n' \
  '            if (pos == "b") {\r\n' \
  '              ref = document.getElementById(ex_foc).nextElementSibling.nextElementSibling.nextElementSibling;\r\n' \
  '            } else {\r\n' \
  '              ref = document.getElementById(ex_foc).parentNode.lastElementChild;\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            pos = "b"; \r\n' \
  '          }\r\n' \
  '          par = seg;\r\n' \
  '          el_cont = document.getElementById("point%scont").cloneNode(true);\r\n' \
  '          el_dot = document.getElementById("dot%s").cloneNode(true);\r\n' \
  '        }\r\n' \
  '        if (! ex_foc) {\r\n' \
  '          if (document.getElementById("waypointsform").firstElementChild) {\r\n' \
  '            if (pos == "b") {\r\n' \
  '              ref = document.getElementById("waypointsform").firstElementChild;\r\n' \
  '            } else {\r\n' \
  '              ref = document.getElementById("waypointsform").lastElementChild;\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            pos = "b"; \r\n' \
  '          }\r\n' \
  '          par = document.getElementById("waypointsform");\r\n' \
  '          el_cont = document.getElementById("waypoint%scont").cloneNode(true);\r\n' \
  '          el_dot = document.getElementById("waydot%s").cloneNode(true);\r\n' \
  '        }\r\n' \
  '        let pref = "";\r\n' \
  '        if (ex_foc.substring(0, 3) == "way" || ! ex_foc) {\r\n' \
  '          pref = document.getElementById("waypoints").getElementsByTagName("span").length.toString();\r\n' \
  '          if (pref == "0") {\r\n' \
  '            document.getElementById("waypoints").style.borderRight = "";\r\n' \
  '            document.getElementById("waypoints").style.overflowY = "scroll";\r\n' \
  '          }\r\n' \
  '          pref = "waypoint" + pref;\r\n' \
  '        } else {\r\n' \
  '          pref = document.getElementById("points").getElementsByTagName("span").length.toString();\r\n' \
  '          if (! seg) {seg = document.getElementById(ex_foc).parentNode.parentNode;}\r\n' \
  '          pref = "point" + pref;\r\n' \
  '        }\r\n' \
  '        if (! el_cont) {\r\n' \
  '          ref = document.getElementById(ex_foc + "cont");\r\n' \
  '          par = ref.parentNode;\r\n' \
  '          el_cont = document.getElementById(ex_foc).parentNode.cloneNode(true);\r\n' \
  '        }\r\n' \
  '        el_cont.id = pref + "cont";\r\n' \
  '        let el_input = el_cont.firstElementChild;\r\n' \
  '        el_input.id = pref;\r\n' \
  '        el_input.name = pref;\r\n' \
  '        el_input.checked = true;\r\n' \
  '        el_input.value = "edited";\r\n' \
  '        let el_label = el_input.nextElementSibling;\r\n' \
  '        el_label.htmlFor = pref;\r\n' \
  '        el_label.id = pref + "desc";\r\n' \
  '        el_label.style.textDecoration = "inherit";\r\n' \
  '        let el_span = el_label.nextElementSibling.nextElementSibling;\r\n' \
  '        el_span.id = pref + "focus";\r\n' \
  '        let el_span_children = el_span.children;\r\n' \
  '        el_span_children[0].htmlFor = pref + "lat";\r\n' \
  '        el_span_children[1].id = pref + "lat";\r\n' \
  '        el_span_children[1].name = pref + "lat";\r\n' \
  '        el_span_children[3].htmlFor = pref + "lon";\r\n' \
  '        el_span_children[4].id = pref + "lon";\r\n' \
  '        el_span_children[4].name = pref + "lon";\r\n' \
  '        el_span_children[6].htmlFor = pref + "ele";\r\n' \
  '        el_span_children[7].id = pref + "ele";\r\n' \
  '        el_span_children[7].name = pref + "ele";\r\n' \
  '        if (ex_foc.substring(0, 3) == "way" || ! ex_foc) {\r\n' \
  '          el_span_children[9].htmlFor = pref + "time";\r\n' \
  '          el_span_children[10].id = pref + "time";\r\n' \
  '          el_span_children[10].name = pref + "time";\r\n' \
  '          el_span_children[12].htmlFor = pref + "name";\r\n' \
  '          el_span_children[13].id = pref + "name";\r\n' \
  '          el_span_children[13].name = pref + "name";\r\n' \
  '        } else {\r\n' \
  '          el_span_children[9].htmlFor = pref + "alt";\r\n' \
  '          el_span_children[10].id = pref + "alt";\r\n' \
  '          el_span_children[10].name = pref + "alt";\r\n' \
  '          el_span_children[12].htmlFor = pref + "time";\r\n' \
  '          el_span_children[13].id = pref + "time";\r\n' \
  '          el_span_children[13].name = pref + "time";\r\n' \
  '        }\r\n' \
  '        if (el_dot || coord) {\r\n' \
  '          let lat = null;\r\n' \
  '          let lon = null;\r\n' \
  '          if (coord) {\r\n' \
  '            [lat, lon] = coord;\r\n' \
  '          } else {\r\n' \
  '            [lat, lon] = WebMercatortoWGS84(Math.max(vminx, Math.min(vmaxx, htopx + (viewpane.offsetWidth / 2 - hpx) * tscale / zoom)), Math.max(vminy, Math.min(vmaxy, htopy - (viewpane.offsetHeight / 2 - hpy) * tscale / zoom)));\r\n' \
  '          }\r\n' \
  '          if (! el_dot) {\r\n' \
  '            el_dot = document.getElementById(ex_foc.replace("point", "dot")).cloneNode(true);\r\n' \
  '          }\r\n' \
  '          el_span_children[1].value = lat.toFixed(6);\r\n' \
  '          el_span_children[4].value = lon.toFixed(6);\r\n' \
  '          el_span_children[7].value = "";\r\n' \
  '          el_span_children[10].value = "";\r\n' \
  '          el_span_children[13].value = "";\r\n' \
  '          el_label.innerHTML = point_desc(el_span);\r\n' \
  '          let wm = WGS84toWebMercator(lat, lon);\r\n' \
  '          if (ex_foc) {\r\n' \
  '            el_dot.style.left = wmvalue_to_prop(wm[0] - htopx, 3.5);\r\n' \
  '            el_dot.style.top = wmvalue_to_prop(htopy - wm[1], 3.5);\r\n' \
  '          } else {\r\n' \
  '            el_dot.style.left = wmvalue_to_prop(wm[0] - htopx, 4);\r\n' \
  '            el_dot.style.top = wmvalue_to_prop(htopy - wm[1], 4);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (pos == "a") {ref = ref.nextElementSibling}\r\n' \
  '        par.insertBefore(el_cont, ref);\r\n' \
  '        if (! el_dot) {\r\n' \
  '          el_dot = document.getElementById(ex_foc.replace("point", "dot")).cloneNode(true);\r\n' \
  '        }\r\n' \
  '        el_dot.id = pref.replace("point", "dot");\r\n' \
  '        par = handle;\r\n' \
  '        ref = el_cont.nextElementSibling;\r\n' \
  '        if (! ref ) {\r\n' \
  '          let spans = document.getElementById("pointsform").getElementsByTagName("span");\r\n' \
  '          if (el_cont.id.substring(0,3) == "way") {\r\n' \
  '            if (spans.length > 0) {ref = spans[0].parentNode;}\r\n' \
  '          } else {\r\n' \
  '            for (let p=0; p<spans.length; p++) {\r\n' \
  '              if (spans[p].id == el_span.id && p + 1 < spans.length) {\r\n' \
  '                ref = spans[p + 1].parentNode;\r\n' \
  '                break;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (ref) {ref = document.getElementById(ref.id.slice(0, -4).replace("point", "dot"));}\r\n' \
  '        par.insertBefore(el_dot, ref);\r\n' \
  '        dot_style(pref, false);\r\n' \
  '        if (ex_foc.substring(0, 3) != "way" && ex_foc) {\r\n' \
  '          let track = document.getElementById("track" + seg.id.slice(7, -4));\r\n' \
  '          let np = WGS84_to_viewbox(parseFloat(el_span_children[1].value), parseFloat(el_span_children[4].value), track);\r\n' \
  '          let path = document.getElementById("path" + seg.id.slice(7, -4));\r\n' \
  '          let spans = seg.getElementsByTagName("span");\r\n' \
  '          let ind = 0;\r\n' \
  '          while (spans[ind].id != pref + "focus") {ind++;}\r\n' \
  '          ind++;\r\n' \
  '          let d = path.getAttribute("d");\r\n' \
  '          let d_left = d.match("( *[LMm] *\\\\d+([.]\\\\d*)? +\\\\d+([.]\\\\d*)? *){" + ind.toString() + "}");\r\n' \
  '          let d_right = d.slice(d_left[0].length);\r\n' \
  '          if (d_right.length > 0) {d_right = " " + d_right;}\r\n' \
  '          if (d_left[0].indexOf("M", 1) >= 0) {\r\n' \
  '            d = d_left[0].trimEnd() + " L" + np + d_right;\r\n' \
  '          } else {\r\n' \
  '            d = d_left[0].trimEnd() + " M" + np + d_right.replace("M", "L");\r\n' \
  '          }\r\n' \
  '          path.setAttribute("d", d);\r\n' \
  '        }\r\n' \
  '        element_click(null, el_label, false);\r\n' \
  '        hist[0].push([focused, ""]);\r\n' \
  '        el_span.scrollIntoView({block:"center"});\r\n' \
  '        if (! coord) {\r\n' \
  '          if (seg) {\r\n' \
  '            scroll_to_dot(el_dot);\r\n' \
  '            segments_calc(seg);\r\n' \
  '          } else {\r\n' \
  '            scroll_to_dot(el_dot);\r\n' \
  '            wpt_calc();\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        show_msg(((focused.substring(0, 3)=="way")?"{#jminsert1#}":"{#jminsert2#}"), 2);\r\n' \
  '      }\r\n' \
  '      function point_delete(pt, batch=false) {\r\n' \
  '        if (document.getElementById(pt.id + "desc").style.textDecoration.indexOf("red") < 0) {\r\n' \
  '          document.getElementById(pt.id + "desc").style.textDecoration = "line-through";\r\n' \
  '        }\r\n' \
  '        if (pt.id.substring(0, 3) == "way") {\r\n' \
  '          wpt_calc();\r\n' \
  '        } else if (! batch) {\r\n' \
  '          let seg = pt.parentNode.parentNode;\r\n' \
  '          let path = document.getElementById("path" + seg.id.slice(7, -4));\r\n' \
  '          let spans = seg.getElementsByTagName("span");\r\n' \
  '          let ind = 0;\r\n' \
  '          while (spans[ind].id != pt.id + "focus") {ind++;}\r\n' \
  '          let d = path.getAttribute("d");\r\n' \
  '          let d_left = d.match("( *[LMm] *\\\\d+([.]\\\\d*)? +\\\\d+([.]\\\\d*)? *){" + (ind + 2).toString() + "}");\r\n' \
  '          let d_right = d.slice(d_left[0].length);\r\n' \
  '          if (d_right.length > 0) {d_right = " " + d_right;}\r\n' \
  '          if (d_left[1][0] == "M") {\r\n' \
  '            d = d_left[0].slice(0, -d_left[1].length) + "m0 0" + d_right.replace("L", "M");\r\n' \
  '          } else {\r\n' \
  '            d = d_left[0].slice(0, -d_left[1].length) + "m0 0" + d_right;\r\n' \
  '          }\r\n' \
  '          path.setAttribute("d", d);\r\n' \
  '          segments_calc(pt.parentNode.parentNode);\r\n' \
  '        }\r\n' \
  '        dot_style(pt.id, ! batch);\r\n' \
  '      }\r\n' \
  '      function point_undelete(pt, batch=false) {\r\n' \
  '        if (document.getElementById(pt.id + "desc").style.textDecoration.indexOf("red") < 0) {\r\n' \
  '          document.getElementById(pt.id + "desc").style.textDecoration = "inherit";\r\n' \
  '        }\r\n' \
  '        if (pt.id.substring(0, 3) == "way") {\r\n' \
  '          wpt_calc();\r\n' \
  '        } else if (! batch) {\r\n' \
  '          let seg = pt.parentNode.parentNode;\r\n' \
  '          let track = document.getElementById("track" + seg.id.slice(7, -4));\r\n' \
  '          let np = WGS84_to_viewbox(parseFloat(document.getElementById(pt.id + "lat").value), parseFloat(document.getElementById(pt.id + "lon").value), track);\r\n' \
  '          let path = document.getElementById("path" + seg.id.slice(7, -4));\r\n' \
  '          let spans = seg.getElementsByTagName("span");\r\n' \
  '          let ind = 0;\r\n' \
  '          while (spans[ind].id != pt.id + "focus") {ind++;}\r\n' \
  '          let d = path.getAttribute("d");\r\n' \
  '          let d_left = d.match("( *[LMm] *\\\\d+([.]\\\\d*)? +\\\\d+([.]\\\\d*)? *){" + (ind + 2).toString() + "}");\r\n' \
  '          let d_right = d.slice(d_left[0].length);\r\n' \
  '          if (d_right.length > 0) {d_right = " " + d_right;}\r\n' \
  '          if (d_left[0].indexOf("M", 1) >= 0) {\r\n' \
  '            d = d_left[0].slice(0, -d_left[1].length) + " L" + np + d_right;\r\n' \
  '          } else {\r\n' \
  '            d = d_left[0].slice(0, -d_left[1].length) + " M" + np + d_right.replace("M", "L");\r\n' \
  '          }\r\n' \
  '          path.setAttribute("d", d);\r\n' \
  '          segments_calc(pt.parentNode.parentNode);\r\n' \
  '        }\r\n' \
  '        dot_style(pt.id, ! batch);\r\n' \
  '      }\r\n' \
  '      function point_checkbox(pt, batch=false) {\r\n' \
  '        if (pt.value == "error") {pt.checked = ! pt.checked;}\r\n' \
  '        if (pt.checked) {point_undelete(pt, batch);} else {point_delete(pt, batch);}\r\n' \
  '      }\r\n' \
  '      function distance(lat1, lon1, ele1, lat2, lon2, ele2) {\r\n' \
  '        let d = 2 * 6378137 * Math.asin(Math.sqrt((Math.sin((lat2 - lat1) * Math.PI / 360)) ** 2 + Math.cos(lat1 * Math.PI / 180) * Math.cos (lat2 * Math.PI / 180) * (Math.sin((lon2 - lon1) * Math.PI / 360)) ** 2));\r\n' \
  '        if (ele1 != null && ele2 != null) {d = Math.sqrt(d ** 2 + (ele2 - ele1) ** 2);}\r\n' \
  '        return d;\r\n' \
  '      }\r\n' \
  '      function slope(dist, heig) {\r\n' \
  '        return dist>Math.abs(heig)?(heig / Math.sqrt(dist**2 - heig**2)):(parseFloat(document.getElementById("slmax").innerHTML) / 100 * (heig==0?0:(heig>0?1:-1)));\r\n' \
  '      }\r\n' \
  '      function segment_calc(seg, fpan=0, ind=null, mmlhs=null, teas=null) {\r\n' \
  '        let seg_ind = parseInt(seg.id.slice(7, -4));\r\n' \
  '        let seg_desc = seg.firstElementChild.nextElementSibling;\r\n' \
  '        if (fpan == 0) {\r\n' \
  '          let pos_d = seg_desc.innerHTML.indexOf("(");\r\n' \
  '          if (pos_d > 0) {\r\n' \
  '            seg_desc.innerHTML = "&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;" + seg_desc.innerHTML.substring(1, pos_d) + "&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;";\r\n' \
  '          }\r\n' \
  '          while (stats.length <= seg_ind) {stats.push([]);}\r\n' \
  '          stats[seg_ind] = [];\r\n' \
  '        }\r\n' \
  '        if (! seg.firstElementChild.checked) {return;}\r\n' \
  '        if (fpan == 0 || fpan == 1 || (fpan == 2 && gpucomp == 0) || gpu_part) {\r\n' \
  '          let spans = seg.getElementsByTagName("span");\r\n' \
  '          let stat = Array(7).fill(0);\r\n' \
  '          let stat_p = null;\r\n' \
  '          let stat_i = 0;\r\n' \
  '          let t_s = null;\r\n' \
  '          let lat_p = null;\r\n' \
  '          let lon_p = null;\r\n' \
  '          let lat = null;\r\n' \
  '          let lon = null;\r\n' \
  '          let ea_s = [0, 0];\r\n' \
  '          let ea_p = [NaN, NaN];\r\n' \
  '          let ea_l = [null, null];\r\n' \
  '          let ea_h = [null, null];\r\n' \
  '          let ea_g = [null, null];\r\n' \
  '          let ea_ic = [null, null];\r\n' \
  '          let ea_f = [parseFloat(document.getElementById("egstren").innerHTML), parseFloat(document.getElementById("agstren").innerHTML)];\r\n' \
  '          let el_s = 0;\r\n' \
  '          let el = null;\r\n' \
  '          let el_p = NaN;\r\n' \
  '          let p_p = null;\r\n' \
  '          for (let p=0; p<spans.length; p++) {\r\n' \
  '            if (point_stat[parseInt(spans[p].id.slice(5, -5))] == null) {continue;}\r\n' \
  '            let p_c = spans[p].children;\r\n' \
  '            let ea = [parseFloat(p_c[7].value), parseFloat(p_c[10].value)];\r\n' \
  '            for (let v=0; v<2; v++) {\r\n' \
  '              if (! isNaN(ea[v]) && isNaN(ea_p[v])) {\r\n' \
  '                ea_p[v] = ea[v];\r\n' \
  '                ea_s[v] = ea_p[v];\r\n' \
  '              }\r\n' \
  '              if (! isNaN(ea[v]) && ea_l[v] == null) {ea_l[v] = ea[v];}\r\n' \
  '              if (! isNaN(ea[v]) && ea_h[v] == null) {ea_h[v] = ea[v];}\r\n' \
  '            }\r\n' \
  '            if (fpan == 0 || (gpucomp >= 1 && fpan != 1)) {\r\n' \
  '              let t = Date.parse(p_c[13].value);\r\n' \
  '              lat = parseFloat(p_c[1].value);\r\n' \
  '              lon = parseFloat(p_c[4].value);\r\n' \
  '              if (isNaN(t)) {\r\n' \
  '                stat[0] = t_s==null?0:stat_p[0];\r\n' \
  '              } else {\r\n' \
  '                if (t_s == null) {\r\n' \
  '                  t_s = t;\r\n' \
  '                } else {\r\n' \
  '                  stat[0] = Math.max((t - t_s) / 1000, stat_p[0]);\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              if (! isNaN(ea[1])) {\r\n' \
  '                el = ea[1];\r\n' \
  '                if (isNaN(el_p)) {\r\n' \
  '                  el_p = el;\r\n' \
  '                  el_s = el_p;\r\n' \
  '                }\r\n' \
  '              } else if (! isNaN(ea[0])) {\r\n' \
  '                el = ea[0];\r\n' \
  '                if (isNaN(el_p)) {\r\n' \
  '                  el_p = el;\r\n' \
  '                  el_s = el_p;\r\n' \
  '                }\r\n' \
  '              } else {\r\n' \
  '                el = isNaN(el_p)?0:el_p;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            if (p_p == null) {\r\n' \
  '              if (gpucomp == 0) {\r\n' \
  '                stat[4] = isNaN(ea[0])?ea_p[0]:ea[0];\r\n' \
  '                stat[5] = isNaN(ea[1])?ea_p[1]:ea[1];\r\n' \
  '              } else if (fpan != 1) {\r\n' \
  '                mmlhs.set([0, 0, lat, el_p], 4 * ind);\r\n' \
  '                teas.set([stat[0], isNaN(ea[0])?ea_p[0]:ea[0], isNaN(ea[1])?ea_p[1]:ea[1]], 3 * ind);\r\n' \
  '                ind++;\r\n' \
  '              }\r\n' \
  '            } else {\r\n' \
  '              if (gpucomp <= 1 && fpan <= 1) {\r\n' \
  '                stat[2] = stat_p[2] + ((isNaN(ea_p[0])||isNaN(ea[0]))?0:Math.max(0,ea[0]-ea_p[0]));\r\n' \
  '                stat[3] = stat_p[3] + ((isNaN(ea_p[1])||isNaN(ea[1]))?0:Math.max(0,ea[1]-ea_p[1]));\r\n' \
  '              }\r\n' \
  '              if (gpucomp == 0) {\r\n' \
  '                if (fpan == 0) {\r\n' \
  '                  stat[1] = stat_p[1] + distance(lat_p, lon_p, isNaN(el_p)?0:el_p, lat, lon, el);\r\n' \
  '                }\r\n' \
  '                stat[4] = isNaN(ea[0])?ea_p[0]:ea[0];\r\n' \
  '                stat[5] = isNaN(ea[1])?ea_p[1]:ea[1];\r\n' \
  '              } else if (fpan != 1) {\r\n' \
  '                mmlhs.set([lat - lat_p,  lon - lon_p , lat, isNaN(el_p)?el_p:el], 4 * ind);\r\n' \
  '                teas.set([stat[0], isNaN(ea[0])?ea_p[0]:ea[0], isNaN(ea[1])?ea_p[1]:ea[1]], 3 * ind);\r\n' \
  '                ind++;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            lat_p = lat;\r\n' \
  '            lon_p = lon;\r\n' \
  '            stat_p = stat.slice();\r\n' \
  '            if (fpan == 0) {\r\n' \
  '              stats[seg_ind].push(stat_p);\r\n' \
  '              if (! isNaN(el_p)) {el_p = el;}\r\n' \
  '            } else if (fpan == 1) {\r\n' \
  '              stats[seg_ind][stat_i][2] = stat_p[2];\r\n' \
  '              stats[seg_ind][stat_i][3] = stat_p[3];\r\n' \
  '            } else if (fpan == 2 && gpucomp == 0) {\r\n' \
  '              stats[seg_ind][stat_i][4] = stat_p[4];\r\n' \
  '              stats[seg_ind][stat_i][5] = stat_p[5];\r\n' \
  '            }\r\n' \
  '            stat_i++;\r\n' \
  '            p_p = p;\r\n' \
  '            if (gpucomp <= 1 && fpan <= 1) {\r\n' \
  '              for (let v=0; v<2; v++) {\r\n' \
  '                if (! isNaN(ea[v])) {\r\n' \
  '                  if (ea[v] > ea_p[v]) {\r\n' \
  '                    ea_p[v] = ea[v];\r\n' \
  '                    if (ea[v] >= ea_l[v] + ea_f[v]) {\r\n' \
  '                      ea_g[v] = "+";\r\n' \
  '                      ea_ic[v] = null;\r\n' \
  '                      ea_h[v] = ea[v];\r\n' \
  '                    }\r\n' \
  '                    if (ea_g[v] != "+" && ea_ic[v] == null) {\r\n' \
  '                      ea_ic[v] = stat_i - 2;\r\n' \
  '                    }\r\n' \
  '                  }\r\n' \
  '                  if (ea[v] < ea_p[v] && ((ea[v] <= ea_h[v] - ea_f[v]) || ea_g[v] == "-")) {\r\n' \
  '                    if (ea_ic[v] != null) {\r\n' \
  '                      stat_p[v + 2] = stats[seg_ind][ea_ic[v]][v + 2];\r\n' \
  '                      for (let i=ea_ic[v]+1; i<stat_i; i++) {stats[seg_ind][i][v + 2] = stat_p[v + 2];}\r\n' \
  '                      ea_ic[v] = null;\r\n' \
  '                    }\r\n' \
  '                    if (ea_g[v] == "+") {\r\n' \
  '                      ea_l[v] = ea[v];\r\n' \
  '                    } else {\r\n' \
  '                      ea_l[v] = Math.min(ea_l[v], ea[v]);\r\n' \
  '                    }\r\n' \
  '                    ea_g[v] = "-";\r\n' \
  '                  }\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            if (! isNaN(ea[0])) {ea_p[0] = ea[0];}\r\n' \
  '            if (! isNaN(ea[1])) {ea_p[1] = ea[1];}\r\n' \
  '          }\r\n' \
  '          if (! stat_p) {return;}\r\n' \
  '          if (gpucomp == 0 && (fpan == 0 || fpan == 2)) {\r\n' \
  '            for (let p=0; p<stat_i; p++) {\r\n' \
  '              if (isNaN(stats[seg_ind][p][4])) {\r\n' \
  '                stats[seg_ind][p][4] = ea_s[0];\r\n' \
  '                if (isNaN(stats[seg_ind][p][5])) {stats[seg_ind][p][5] = ea_s[1];}\r\n' \
  '              } else if (isNaN(stats[seg_ind][p][5])) {\r\n' \
  '                stats[seg_ind][p][5] = ea_s[1];\r\n' \
  '              } else {break;}\r\n' \
  '            }\r\n' \
  '          } else if (gpucomp != 0 && (fpan == 0 || gpu_part) && fpan != 1) {\r\n' \
  '            for (let i=ind-stat_i; i<ind; i++) {\r\n' \
  '              if (isNaN(mmlhs[4 * i + 3])) {mmlhs[4 * i + 3] = el_s;} else {break;}\r\n' \
  '            }\r\n' \
  '            for (let i=ind-stat_i; i<ind; i++) {\r\n' \
  '              if (isNaN(teas[3 * i + 1])) {teas[3 * i + 1] = ea_s[0];} else {break;}\r\n' \
  '            }\r\n' \
  '            for (let i=ind-stat_i; i<ind; i++) {\r\n' \
  '              if (isNaN(teas[3 * i + 2])) {teas[3 * i + 2] = ea_s[1];} else {break;}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (fpan == 0) {\r\n' \
  '            let dur_c = "--h--mn--s";\r\n' \
  '            if (t_s != null) {\r\n' \
  '              let dur_s = stat_p[0] % 60;\r\n' \
  '              let dur_m = ((stat_p[0] - dur_s) / 60) % 60;\r\n' \
  '              let dur_h = (stat_p[0] - dur_m * 60 - dur_s) / 3600;\r\n' \
  '              dur_c = dur_h.toFixed(0) + "h" + dur_m.toFixed(0).padStart(2, "0") + "mn" + dur_s.toFixed(0).padStart(2, "0") + "s";\r\n' \
  '            }\r\n' \
  '            let dist_c = "-km";\r\n' \
  '            if (gpucomp == 0) {dist_c = (stat_p[1] / 1000).toFixed(2) + "km";}\r\n' \
  '            let ele_c = "-m";\r\n' \
  '            if (! isNaN(ea_p[0])) {ele_c = (gpucomp<=1?stat_p[2].toFixed(0):"[eg]") + "m";}\r\n' \
  '            let alt_c = "-m";\r\n' \
  '            if (! isNaN(ea_p[1])) {alt_c = (gpucomp<=1?stat_p[3].toFixed(0):"[ag]") + "m";}\r\n' \
  '            seg_desc.innerHTML = "&ndash;" + seg_desc.innerHTML.slice(6, -6) + "(" + dur_c + "|" + dist_c + "|" + ele_c + "|" + alt_c + ") &ndash;";\r\n' \
  '          } else if (fpan == 1) {\r\n' \
  '            seg_desc.innerHTML = seg_desc.innerHTML.replace(/\d+m\|/, stat_p[2].toFixed(0) + "m|").replace(/\d+m\)/, stat_p[3].toFixed(0) + "m)");\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (gpucomp == 0 && (fpan == 0 || fpan == 2)) {\r\n' \
  '          let drange = parseFloat(document.getElementById("sldist").innerHTML) / 2;\r\n' \
  '          let slmax = parseFloat(document.getElementById("slmax").innerHTML) / 100;\r\n' \
  '          for (let p=0; p<stats[seg_ind].length; p++) {\r\n' \
  '            let ea = stats[seg_ind][p].slice(4,6);\r\n' \
  '            stats[seg_ind][p][4]=0;\r\n' \
  '            stats[seg_ind][p][5]=0;\r\n' \
  '            let ps = p;\r\n' \
  '            for (ps=p+1;ps<stats[seg_ind].length;ps++) {\r\n' \
  '              if (stats[seg_ind][ps][1] > stats[seg_ind][p][1] + drange) {break;}\r\n' \
  '              if (stats[seg_ind][ps][1] - stats[seg_ind][p][1] == 0) {continue;}\r\n' \
  '              stats[seg_ind][p][4] += slope(stats[seg_ind][ps][1] - stats[seg_ind][p][1], stats[seg_ind][ps][4] - ea[0]) * (stats[seg_ind][ps][1] - stats[seg_ind][ps-1][1]);\r\n' \
  '              stats[seg_ind][p][5] += slope(stats[seg_ind][ps][1] - stats[seg_ind][p][1], stats[seg_ind][ps][5] - ea[1]) * (stats[seg_ind][ps][1] - stats[seg_ind][ps-1][1]);\r\n' \
  '            }\r\n' \
  '            if (stats[seg_ind][ps - 1][1] - stats[seg_ind][p][1] != 0) {\r\n' \
  '              let c = (drange + stats[seg_ind][p][1] - stats[seg_ind][ps-1][1]) / (stats[seg_ind][ps-1][1] - stats[seg_ind][p][1]);\r\n' \
  '              stats[seg_ind][p][4] = (stats[seg_ind][p][4] + slope(stats[seg_ind][ps-1][1] - stats[seg_ind][p][1], stats[seg_ind][ps-1][4] - ea[0]) * (drange + stats[seg_ind][p][1] - stats[seg_ind][ps-1][1])) / drange;\r\n' \
  '              stats[seg_ind][p][5] = (stats[seg_ind][p][5] + slope(stats[seg_ind][ps-1][1] - stats[seg_ind][p][1], stats[seg_ind][ps-1][5] - ea[1]) * (drange + stats[seg_ind][p][1] - stats[seg_ind][ps-1][1])) / drange;\r\n' \
  '            }\r\n' \
  '            stats[seg_ind][p][4] = Math.max(Math.min(stats[seg_ind][p][4], slmax), -slmax);\r\n' \
  '            stats[seg_ind][p][5] = Math.max(Math.min(stats[seg_ind][p][5], slmax), -slmax);\r\n' \
  '          }\r\n' \
  '          for (let p=stats[seg_ind].length-2; p>0; p--) {\r\n' \
  '            if (stats[seg_ind][p+1][1] - stats[seg_ind][p][1] <= drange) {\r\n' \
  '              let ps = p;\r\n' \
  '              let s = [0, 0];\r\n' \
  '              let su = 0;\r\n' \
  '              for (ps=p-1; ps>=0; ps--) {\r\n' \
  '                if (stats[seg_ind][ps][1] < stats[seg_ind][p][1] - drange) {break;}\r\n' \
  '                let c = (stats[seg_ind][ps+1][1] - stats[seg_ind][ps][1]) / (stats[seg_ind][p][1] - stats[seg_ind][ps][1] + 1);\r\n' \
  '                s[0] += stats[seg_ind][ps][4] * c;\r\n' \
  '                s[1] += stats[seg_ind][ps][5] * c;\r\n' \
  '                su += c;\r\n' \
  '              }\r\n' \
  '              if (stats[seg_ind][p][1] - stats[seg_ind][ps+1][1] != 0) {\r\n' \
  '                stats[seg_ind][p][4] = Math.max(-slmax, Math.min(slmax, (stats[seg_ind][p][4] + s[0]/2 ) / (1 + su/2)));\r\n' \
  '                stats[seg_ind][p][5] = Math.max(-slmax, Math.min(slmax, (stats[seg_ind][p][5] + s[1]/2 ) / (1 + su/2)));\r\n' \
  '            }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (gpucomp == 0 && (fpan == 0 || fpan == 3)) {\r\n' \
  '          let trange = parseFloat(document.getElementById("sptime").innerHTML) / 2;\r\n' \
  '          let spmax = parseFloat(document.getElementById("spmax").innerHTML) / 3.6;\r\n' \
  '          for (let p=0; p<stats[seg_ind].length; p++) {\r\n' \
  '            stats[seg_ind][p][6] = 0;\r\n' \
  '            let ps = p;\r\n' \
  '            for (ps=p+1; ps<stats[seg_ind].length; ps++) {\r\n' \
  '              if (stats[seg_ind][ps][0] > stats[seg_ind][p][0] + trange) {break;}\r\n' \
  '              if (stats[seg_ind][ps][0] - stats[seg_ind][p][0] == 0) {continue;}\r\n' \
  '              stats[seg_ind][p][6] += (stats[seg_ind][ps][1] - stats[seg_ind][p][1]) / (stats[seg_ind][ps][0] - stats[seg_ind][p][0]) * (stats[seg_ind][ps][0] - stats[seg_ind][ps-1][0]);\r\n' \
  '            }\r\n' \
  '            if (stats[seg_ind][ps-1][0] - stats[seg_ind][p][0] != 0) {\r\n' \
  '              stats[seg_ind][p][6] = (stats[seg_ind][p][6] + (stats[seg_ind][ps-1][1] - stats[seg_ind][p][1]) / (stats[seg_ind][ps-1][0] - stats[seg_ind][p][0]) * (trange + stats[seg_ind][p][0] - stats[seg_ind][ps-1][0])) / trange;\r\n' \
  '            }\r\n' \
  '            stats[seg_ind][p][6] = Math.min(stats[seg_ind][p][6], spmax);\r\n' \
  '          }\r\n' \
  '          for (let p=stats[seg_ind].length-2; p>0; p--) {\r\n' \
  '            if (stats[seg_ind][p+1][0] - stats[seg_ind][p][0] <= trange) {\r\n' \
  '              let ps = p;\r\n' \
  '              let s = 0;\r\n' \
  '              let su = 0;\r\n' \
  '              for (ps=p-1; ps>=0; ps--) {\r\n' \
  '                if (stats[seg_ind][ps][0] < stats[seg_ind][p][0] - trange) {break;}\r\n' \
  '                let c = (stats[seg_ind][ps+1][0] - stats[seg_ind][ps][0]) / (stats[seg_ind][p][0] - stats[seg_ind][ps][0] + 1);\r\n' \
  '                s += stats[seg_ind][ps][6] * c;\r\n' \
  '                su += c;\r\n' \
  '              }\r\n' \
  '              if (stats[seg_ind][p][0] - stats[seg_ind][ps+1][0] != 0) {\r\n' \
  '                stats[seg_ind][p][6] = Math.min(spmax, (stats[seg_ind][p][6] + s/2 ) / (1 + su/2));\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function wpt_calc() {\r\n' \
  '        let nbpt = 0;\r\n' \
  '        let wpts = document.getElementById("waypointsform").getElementsByTagName("input");\r\n' \
  '        for (let w=0; w<wpts.length; w++) {\r\n' \
  '          if (wpts[w].checked && wpts[w].value != "error") {nbpt++;}\r\n' \
  '        }\r\n' \
  '        let waypoints = document.getElementById("waypoints").firstChild;\r\n' \
  '        let pos_p = waypoints.data.indexOf("(");\r\n' \
  '        if (pos_p < 0) {\r\n' \
  '          waypoints.appendData("(" + nbpt.toString() + ") ");\r\n' \
  '        } else {\r\n' \
  '          waypoints.replaceData(pos_p, waypoints.data.length - pos_p, "(" + nbpt.toString() + ") ");\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function whole_calc() {\r\n' \
  '        let points = document.getElementById("points").firstChild;\r\n' \
  '        let pos_p =  points.data.indexOf("(");\r\n' \
  '        if (pos_p >= 0) {points.deleteData(pos_p, points.length - pos_p);}\r\n' \
  '        let segs = document.getElementById("pointsform").children;\r\n' \
  '        let dur = null;\r\n' \
  '        let dist = null;\r\n' \
  '        let ele = null;\r\n' \
  '        let alt = null;\r\n' \
  '        let nbpt = 0;\r\n' \
  '        for (let s=0; s<stats.length; s++) {\r\n' \
  '          if (stats[s].length == 0) {continue;}\r\n' \
  '          nbpt = nbpt + stats[s].length;\r\n' \
  '          let stat = stats[s][stats[s].length - 1];\r\n' \
  '          dur = dur==null?stat[0]:dur+stat[0];\r\n' \
  '          dist = dist==null?stat[1]:dist+stat[1];\r\n' \
  '          ele = ele==null?stat[2]:ele+stat[2];\r\n' \
  '          alt = alt==null?stat[3]:alt+stat[3];\r\n' \
  '        }\r\n' \
  '        let dur_c = "--h--mn--s";\r\n' \
  '        if (dur != null) {\r\n' \
  '          dur = Math.round(dur);\r\n' \
  '          let dur_s = dur % 60;\r\n' \
  '          let dur_m = ((dur - dur_s) / 60) % 60;\r\n' \
  '          let dur_h = (dur - dur_m * 60 - dur_s) / 3600;\r\n' \
  '          dur_c = dur_h.toString() + "h" + dur_m.toString().padStart(2, "0") + "mn" + dur_s.toString().padStart(2, "0") + "s";\r\n' \
  '        }\r\n' \
  '        let dist_c = "-km";\r\n' \
  '        if (dist != null) {dist_c = (dist / 1000).toFixed(2) + "km";}\r\n' \
  '        let ele_c = "-m";\r\n' \
  '        if (ele != null) {ele_c = ele.toFixed(0) + "m";}\r\n' \
  '        let alt_c = "-m";\r\n' \
  '        if (alt != null) {alt_c = alt.toFixed(0) + "m";}\r\n' \
  '        points.appendData("(" + dur_c + "|" + dist_c + "|" + ele_c + "|" + alt_c + "|" + nbpt.toString() + ") ");\r\n' \
  '        refresh_graph();\r\n' \
  '      }\r\n' \
  '      function segments_calc(...args) {\r\n' \
  '        let fpan = 0;\r\n' \
  '        let segs = [];\r\n' \
  '        if (args.length == 1) {\r\n' \
  '          if ((typeof args[0]).toLowerCase() != "object") {fpan = args[0];}\r\n' \
  '        }\r\n' \
  '        if (args.length == 0 || fpan != 0) {\r\n' \
  '          segs = Array.from(document.getElementById("pointsform").children);\r\n' \
  '        } else {\r\n' \
  '          segs = args;\r\n' \
  '        }\r\n' \
  '        segs.sort((s1, s2) => parseInt(s1.id.slice(7, -4)) - parseInt(s2.id.slice(7, -4)));\r\n' \
  '        let starts = null;\r\n' \
  '        let mmlhs = null;\r\n' \
  '        let teas = null;\r\n' \
  '        if (fpan == 0 || fpan == 1 || gpucomp == 0 || gpu_part) {\r\n' \
  '          starts = [0];\r\n' \
  '          for (let s=0; s<segs.length; s++) {\r\n' \
  '            if (! segs[s].firstElementChild.checked) {continue};\r\n' \
  '            let nbp = 0;\r\n' \
  '            if (fpan == 0) {\r\n' \
  '              let spans = segs[s].getElementsByTagName("span");\r\n' \
  '              for (let p=0; p<spans.length; p++) {\r\n' \
  '                if (! spans[p].parentNode.firstElementChild.checked || spans[p].parentNode.firstElementChild.value == "error") {\r\n' \
  '                  point_stat[parseInt(spans[p].id.slice(5,-5))] = null;\r\n' \
  '                } else {\r\n' \
  '                  point_stat[parseInt(spans[p].id.slice(5,-5))] = nbp;\r\n' \
  '                  nbp++;\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '            } else {\r\n' \
  '              nbp += stats[s].length;\r\n' \
  '            }\r\n' \
  '            if (nbp != 0) {starts.push(starts[starts.length - 1] + nbp);}\r\n' \
  '          }\r\n' \
  '          if (gpucomp >= 1 && (fpan == 0 || gpu_part) && fpan != 1) {\r\n' \
  '            mmlhs = new Float32Array(GPUStats.pad(starts[starts.length - 1]) * 4);\r\n' \
  '            teas = new Float32Array(GPUStats.pad(starts[starts.length - 1]) * 3);\r\n' \
  '          }\r\n' \
  '          let ind = 0;\r\n' \
  '          for (let s=0; s<segs.length; s++) {\r\n' \
  '            segment_calc(segs[s], fpan, ind, mmlhs, teas);\r\n' \
  '            ind += stats[parseInt(segs[s].id.slice(7, -4))].length;\r\n' \
  '          }\r\n' \
  '          if (starts[starts.length - 1] == 0) {\r\n' \
  '            gpu_part = gpucomp >= 1;\r\n' \
  '            whole_calc();\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '          if (gpucomp >= 1 && (fpan == 0 || gpu_part) && fpan != 1) {\r\n' \
  '            gpustats.starts = starts;\r\n' \
  '            gpustats.mmlhs = mmlhs;\r\n' \
  '            gpustats.teas = teas;\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          for (let s=0; s<segs.length; s++) {\r\n' \
  '            if (stats[parseInt(segs[s].id.slice(7, -4))].length > 0) {\r\n' \
  '              starts = true;\r\n' \
  '              break;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (! starts) {\r\n' \
  '            gpu_part = true;\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (gpucomp >= 1 && fpan != 1) {\r\n' \
  '          gpustats.trange = parseFloat(document.getElementById("sptime").innerHTML) / 2;\r\n' \
  '          gpustats.spmax = parseFloat(document.getElementById("spmax").innerHTML) / 3.6;\r\n' \
  '          gpustats.drange = parseFloat(document.getElementById("sldist").innerHTML) / 2;\r\n' \
  '          gpustats.slmax = parseFloat(document.getElementById("slmax").innerHTML) / 100;\r\n' \
  '          gpustats.calc();\r\n' \
  '          let ds = gpustats.ds;\r\n' \
  '          let ssss = gpustats.ssss;\r\n' \
  '          let i = 0;\r\n' \
  '          for (let s=0; s<segs.length; s++) {\r\n' \
  '            let seg_ind = parseInt(segs[s].id.slice(7, -4));\r\n' \
  '            for (let p=0; p<stats[seg_ind].length; p++) {\r\n' \
  '              if (fpan == 0) {stats[seg_ind][p][1] = stats[seg_ind][p>0?p-1:0][1] + ds[i];}\r\n' \
  '              stats[seg_ind][p][6] = ssss[3 * i];\r\n' \
  '              stats[seg_ind][p][4] = ssss[3 * i + 1];\r\n' \
  '              stats[seg_ind][p][5] = ssss[3 * i + 2];\r\n' \
  '              if (gpucomp == 2 && fpan <= 2) {\r\n' \
  '                if (p == 0) {\r\n' \
  '                  stats[seg_ind][p][2] = 0;\r\n' \
  '                  stats[seg_ind][p][3] = 0;\r\n' \
  '                } else {\r\n' \
  '                  stats[seg_ind][p][2] = stats[seg_ind][p - 1][2] + Math.max(0, ssss[3 * i - 2]) * ds[i];\r\n' \
  '                  stats[seg_ind][p][3] = stats[seg_ind][p - 1][3] + Math.max(0, ssss[3 * i - 1]) * ds[i];\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              i++;\r\n' \
  '            }\r\n' \
  '            if (stats[seg_ind].length > 0) {\r\n' \
  '              let seg_desc = segs[s].firstElementChild.nextElementSibling;\r\n' \
  '              let stat = stats[seg_ind][stats[seg_ind].length - 1];\r\n' \
  '              if (gpucomp == 2 && fpan == 2) {\r\n' \
  '                seg_desc.innerHTML = seg_desc.innerHTML.replace(/\d+m\|/, "[eg]m|").replace(/\d+m\)/, "[ag]m)");\r\n' \
  '              }\r\n' \
  '              seg_desc.innerHTML = seg_desc.innerHTML.replace("-km", (stat[1] / 1000).toFixed(2) + "km").replace("[eg]", stat[2].toFixed(0)).replace("[ag]", stat[3].toFixed(0));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          gpu_part = fpan == 0 && i != stats.reduce((p,c) => p + c.length, 0);\r\n' \
  '        }\r\n' \
  '        whole_calc();\r\n' \
  '      }\r\n' \
  '      function segment_checkbox(seg) {\r\n' \
  '        if (seg.checked) {\r\n' \
  '          document.getElementById("track" + seg.id.substring(7)).style.display = "";\r\n' \
  '          seg.parentNode.style.textDecoration="inherit";\r\n' \
  '        } else {\r\n' \
  '          if (seg.id != focused) {\r\n' \
  '            document.getElementById("track" + seg.id.substring(7)).style.display = "none";\r\n' \
  '          }\r\n' \
  '          seg.parentNode.style.textDecoration="line-through";\r\n' \
  '        }\r\n' \
  '        let spans = seg.parentNode.getElementsByTagName("span");\r\n' \
  '        for (let i=0; i<spans.length;i++) {dot_style(spans[i].id.slice(0, -5), false);}\r\n' \
  '        segments_calc(seg.parentNode);\r\n' \
  '      }\r\n' \
  '      function segment_renum() {\r\n' \
  '        let segs = document.getElementById("pointsform").children;\r\n' \
  '        for (let i=0; i<segs.length; i++) {\r\n' \
  '          let seg_desc = segs[i].firstElementChild.nextElementSibling;\r\n' \
  '          seg_desc.innerHTML = seg_desc.innerHTML.replace(/\\d+/, (i + 1).toString());\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function segment_cut() {\r\n' \
  '        let seg_foc = null;\r\n' \
  '        let pt_foc = null;\r\n' \
  '        if (focused.substring(0, 3) == "seg") {\r\n' \
  '          seg_foc = document.getElementById(focused + "cont");\r\n' \
  '          if (! seg_foc.firstElementChild.checked || seg_foc.lastElementChild.id.indexOf("point") < 0) {return;}\r\n' \
  '        } else if (focused.substring(0, 5) == "point") {\r\n' \
  '          pt_foc = document.getElementById(focused + "cont");\r\n' \
  '          seg_foc = pt_foc.parentNode;\r\n' \
  '        } else {return;}\r\n' \
  '        let seg = seg_foc.cloneNode(true);\r\n' \
  '        let pref = "segment" + document.getElementById("pointsform").children.length.toString();\r\n' \
  '        let track_foc = document.getElementById("track" + seg_foc.id.slice(7, -4));\r\n' \
  '        let path_foc = track_foc.firstElementChild;\r\n' \
  '        let track = track_foc.cloneNode(true);\r\n' \
  '        let path = track.firstElementChild;\r\n' \
  '        if (focused.substring(0, 3) == "seg") {\r\n' \
  '          seg.id = pref + "cont";\r\n' \
  '          seg.children[0].id = pref;\r\n' \
  '          seg.children[0].name = pref;\r\n' \
  '          seg.children[1].htmlFor = pref;\r\n' \
  '          seg.children[1].id = pref + "desc";\r\n' \
  '          track.id = "track" + pref.substring(7);\r\n' \
  '          path.id = "path" + pref.substring(7);\r\n' \
  '          path.nextElementSibling.firstElementChild.setAttribute("href", "#" + path.id);\r\n' \
  '          let spans = seg.getElementsByTagName("span");\r\n' \
  '          let pref_num = document.getElementById("points").getElementsByTagName("span").length;\r\n' \
  '          let dot_ref = document.getElementById(spans[spans.length - 1].id.slice(0, -5).replace("point", "dot")).nextElementSibling;\r\n' \
  '          let mintime = null;\r\n' \
  '          let maxtime = null;\r\n' \
  '          for (let p=0; p<spans.length; p++) {\r\n' \
  '            if (! spans[p].parentNode.firstElementChild.checked || spans[p].parentNode.firstElementChild.value == "error") {continue;}\r\n' \
  '            let t = Date.parse(document.getElementById(spans[p].id.replace("focus", "time")).value);\r\n' \
  '            if (! isNaN(t)) {\r\n' \
  '              if (mintime == null) {mintime = t;} else {mintime = Math.min(mintime, t);}\r\n' \
  '              if (maxtime == null) {maxtime = t;} else {maxtime = Math.max(maxtime, t);}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          for (let p=0; p<spans.length; p++) {\r\n' \
  '            let dot = document.getElementById(spans[p].id.slice(0, -5).replace("point", "dot")).cloneNode(true);\r\n' \
  '            let pref = "point" + pref_num.toString();\r\n' \
  '            let el_cont = spans[p].parentNode;\r\n' \
  '            el_cont.id = pref + "cont";\r\n' \
  '            let el_input = el_cont.firstElementChild;\r\n' \
  '            el_input.id = pref;\r\n' \
  '            el_input.name = pref;\r\n' \
  '            if (el_input.value != "error") {el_input.value = "edited";}\r\n' \
  '            let el_label = el_input.nextElementSibling;\r\n' \
  '            el_label.htmlFor = pref;\r\n' \
  '            el_label.id = pref + "desc";\r\n' \
  '            let el_span = el_label.nextElementSibling.nextElementSibling;\r\n' \
  '            el_span.id = pref + "focus";\r\n' \
  '            let el_span_children = el_span.children;\r\n' \
  '            el_span_children[0].htmlFor = pref + "lat";\r\n' \
  '            el_span_children[1].id = pref + "lat";\r\n' \
  '            el_span_children[1].name = pref + "lat";\r\n' \
  '            el_span_children[3].htmlFor = pref + "lon";\r\n' \
  '            el_span_children[4].id = pref + "lon";\r\n' \
  '            el_span_children[4].name = pref + "lon";\r\n' \
  '            el_span_children[6].htmlFor = pref + "ele";\r\n' \
  '            el_span_children[7].id = pref + "ele";\r\n' \
  '            el_span_children[7].name = pref + "ele";\r\n' \
  '            el_span_children[9].htmlFor = pref + "alt";\r\n' \
  '            el_span_children[10].id = pref + "alt";\r\n' \
  '            el_span_children[10].name = pref + "alt";\r\n' \
  '            el_span_children[12].htmlFor = pref + "time";\r\n' \
  '            el_span_children[13].id = pref + "time";\r\n' \
  '            el_span_children[13].name = pref + "time";\r\n' \
  '            if (mintime != null && maxtime != null) {\r\n' \
  '              let t = Date.parse(el_span_children[13].value);\r\n' \
  '              if (! isNaN(t)) {\r\n' \
  '                el_span_children[13].value = (new Date(Math.round((maxtime + t - mintime) / 1000) * 1000)).toISOString().replace(/\\.[0-9]*/,"");\r\n' \
  '                el_label.innerHTML = point_desc(el_span);\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            dot.id = pref.replace("point", "dot");\r\n' \
  '            handle.insertBefore(dot, dot_ref);\r\n' \
  '            pref_num++;\r\n' \
  '          }\r\n' \
  '          document.getElementById("pointsform").insertBefore(seg, seg_foc.nextElementSibling);\r\n' \
  '          segment_renum();\r\n' \
  '          handle.insertBefore(track, track_foc.nextElementSibling);\r\n' \
  '          segments_calc(seg);\r\n' \
  '          element_click(null, document.getElementById(seg.id.replace("cont", "desc")));\r\n' \
  '          show_msg("{#jmsegmentcut1#}", 2);\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let pt = pt_foc.previousElementSibling;\r\n' \
  '        if (pt.id.indexOf("point") < 0) {return;}\r\n' \
  '        seg_foc.id = pref + "cont";\r\n' \
  '        seg_foc.children[0].id = pref;\r\n' \
  '        seg_foc.children[0].name = pref;\r\n' \
  '        seg_foc.children[1].htmlFor = pref;\r\n' \
  '        seg_foc.children[1].id = pref + "desc";\r\n' \
  '        while (pt.id.indexOf("point") >= 0) {\r\n' \
  '          let pt_p = pt.previousElementSibling;\r\n' \
  '          seg_foc.removeChild(pt);\r\n' \
  '          pt = pt_p;\r\n' \
  '        }\r\n' \
  '        pt = seg.lastElementChild;\r\n' \
  '        while (pt.id != pt_foc.id) {\r\n' \
  '          pt = pt.previousElementSibling;\r\n' \
  '          seg.removeChild(seg.lastElementChild);\r\n' \
  '        }\r\n' \
  '        seg.removeChild(seg.lastElementChild);\r\n' \
  '        document.getElementById("pointsform").insertBefore(seg, seg_foc);\r\n' \
  '        segment_renum();\r\n' \
  '        track_foc.id = "track" + pref.substring(7);\r\n' \
  '        path_foc.id = "path" + pref.substring(7);\r\n' \
  '        path_foc.nextElementSibling.firstElementChild.setAttribute("href", "#" + path_foc.id);\r\n' \
  '        let ind = seg.getElementsByTagName("span").length;\r\n' \
  '        let d = path_foc.getAttribute("d");\r\n' \
  '        let d_left = d.match("( *[LMm] *\\\\d+([.]\\\\d*)? +\\\\d+([.]\\\\d*)? *){" + (ind + 1).toString() + "}");\r\n' \
  '        let d_right = d.slice(d_left[0].length);\r\n' \
  '        if (d_right.indexOf("M") < 0) {d_right = d_right.replace("L", "M");}\r\n' \
  '        path_foc.setAttribute("d", "M0 0 " + d_right);\r\n' \
  '        path.setAttribute("d", d_left[0]);\r\n' \
  '        handle.insertBefore(track, track_foc);\r\n' \
  '        scroll_to_dot(document.getElementById(pt_foc.id.slice(0, -4).replace("point", "dot")));\r\n' \
  '        segments_calc(seg_foc, seg);\r\n' \
  '        show_msg("{#jmsegmentcut2#}", 2);\r\n' \
  '      }\r\n' \
  '      function segment_absorb() {\r\n' \
  '        if (focused.substring(0, 3) != "seg") {return;}\r\n' \
  '        let seg_foc = document.getElementById(focused + "cont");\r\n' \
  '        if (! seg_foc.firstElementChild.checked || seg_foc.lastElementChild.id.indexOf("point") < 0) {return;}\r\n' \
  '        let seg = seg_foc.nextElementSibling;\r\n' \
  '        while (seg) {\r\n' \
  '          if (seg.firstElementChild.checked) {break;}\r\n' \
  '          seg = seg.nextElementSibling;\r\n' \
  '        }\r\n' \
  '        if (! seg) {return;}\r\n' \
  '        let pt = seg.firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling;\r\n' \
  '        if (! pt) {return;}\r\n' \
  '        let ref_dot = document.getElementById(seg_foc.lastElementChild.id.slice(0, -4).replace("point", "dot")).nextElementSibling;\r\n' \
  '        if (ref_dot == document.getElementById(pt.id.slice(0, -4).replace("point", "dot"))) {ref_dot = null;}\r\n' \
  '        while (pt) {\r\n' \
  '          seg_foc.appendChild(pt);\r\n' \
  '          if (ref_dot) {\r\n' \
  '            handle.insertBefore(document.getElementById(pt.id.slice(0, -4).replace("point", "dot")), ref_dot);\r\n' \
  '          }\r\n' \
  '          pt = seg.firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling;\r\n' \
  '        }\r\n' \
  '        seg.firstElementChild.checked = false;\r\n' \
  '        let track_foc = document.getElementById("track" + seg_foc.id.slice(7, -4));\r\n' \
  '        let path_foc = track_foc.firstElementChild;\r\n' \
  '        let track = document.getElementById("track" + seg.id.slice(7, -4));\r\n' \
  '        let path = track.firstElementChild;\r\n' \
  '        let minx_foc = prop_to_wmvalue(track_foc.style.left) + htopx;\r\n' \
  '        let maxy_foc = htopy - prop_to_wmvalue(track_foc.style.top);\r\n' \
  '        let maxx_foc = minx_foc + prop_to_wmvalue(track_foc.style.width);\r\n' \
  '        let miny_foc = maxy_foc - prop_to_wmvalue(track_foc.style.height);\r\n' \
  '        let minx = prop_to_wmvalue(track.style.left) + htopx;\r\n' \
  '        let maxy = htopy - prop_to_wmvalue(track.style.top);\r\n' \
  '        let maxx = minx + prop_to_wmvalue(track.style.width);\r\n' \
  '        let miny = maxy - prop_to_wmvalue(track.style.height);\r\n' \
  '        rebase_track(minx, miny, track_foc, true);\r\n' \
  '        rebase_track(maxx, maxy, track_foc, true);\r\n' \
  '        rebase_track(minx_foc, miny_foc, track, true);\r\n' \
  '        rebase_track(maxx_foc, maxy_foc, track, true);\r\n' \
  '        let d_foc = path_foc.getAttribute("d");\r\n' \
  '        let d = path.getAttribute("d").substring(4);\r\n' \
  '        if (d_foc.substring(1).indexOf("M") >= 0) {d = d.replace("M", "L");}\r\n' \
  '        path_foc.setAttribute("d", d_foc + d);\r\n' \
  '        path.setAttribute("d", "M0 0");\r\n' \
  '        scroll_to_track(document.getElementById("track" + seg_foc.id.slice(7, -4)));\r\n' \
  '        seg_foc.firstElementChild.scrollIntoView({block:"start"});\r\n' \
  '        document.getElementById("track" + seg.id.slice(7, -4)).style.display = "none";\r\n' \
  '        seg.style.textDecoration="line-through";\r\n' \
  '        segments_calc(seg_foc, seg);\r\n' \
  '        show_msg("{#jmsegmentabsorb#}", 2);\r\n' \
  '      }\r\n' \
  '      function element_up() {\r\n' \
  '        if (focused.substring(0, 5) == "point") {\r\n' \
  '          let seg = document.getElementById(focused + "cont").parentNode.firstElementChild.nextElementSibling;\r\n' \
  '          element_click(null, seg);\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (focused.substring(0, 3) == "way") {\r\n' \
  '          let pt_foc = document.getElementById(focused + "cont");\r\n' \
  '          let pt = pt_foc.previousElementSibling;\r\n' \
  '          if (! pt) {return;}\r\n' \
  '          document.getElementById("waypointsform").insertBefore(pt_foc, pt);\r\n' \
  '          pt_foc.scrollIntoView({block:"start"});\r\n' \
  '          handle.insertBefore(document.getElementById(pt_foc.id.slice(0, -4).replace("point", "dot")), document.getElementById(pt.id.slice(0, -4).replace("point", "dot")));\r\n' \
  '          show_msg("{#jmelementup1#}", 2);\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (focused.substring(0, 3) != "seg") {return;}\r\n' \
  '        let seg_foc = document.getElementById(focused + "cont");\r\n' \
  '        let seg = seg_foc.previousElementSibling;\r\n' \
  '        if (! seg) {return;}\r\n' \
  '        let mintime_foc = null;\r\n' \
  '        let maxtime_foc = null;\r\n' \
  '        let mintime = null;\r\n' \
  '        let maxtime = null;\r\n' \
  '        let spans_foc = seg_foc.getElementsByTagName("span");\r\n' \
  '        let spans = seg.getElementsByTagName("span");\r\n' \
  '        for (let p=0; p<spans_foc.length; p++) {\r\n' \
  '          if (! spans_foc[p].parentNode.firstElementChild.checked || spans_foc[p].parentNode.firstElementChild.value == "error") {continue;}\r\n' \
  '          let t = Date.parse(document.getElementById(spans_foc[p].id.replace("focus", "time")).value);\r\n' \
  '          if (! isNaN(t)) {\r\n' \
  '            if (mintime_foc == null) {mintime_foc = t;} else {mintime_foc = Math.min(mintime_foc, t);}\r\n' \
  '            if (maxtime_foc == null) {maxtime_foc = t;} else {maxtime_foc = Math.max(maxtime_foc, t);}\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        for (let p=0; p<spans.length; p++) {\r\n' \
  '          if (! spans[p].parentNode.firstElementChild.checked || spans[p].parentNode.firstElementChild.value == "error") {continue;}\r\n' \
  '          let t = Date.parse(document.getElementById(spans[p].id.replace("focus", "time")).value);\r\n' \
  '          if (! isNaN(t)) {\r\n' \
  '            if (mintime == null) {mintime = t;} else {mintime = Math.min(mintime, t);}\r\n' \
  '            if (maxtime == null) {maxtime = t;} else {maxtime = Math.max(maxtime, t);}\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        document.getElementById("pointsform").insertBefore(seg_foc, seg);\r\n' \
  '        if (mintime_foc != null && maxtime_foc != null && mintime != null && maxtime != null) {\r\n' \
  '          let batch = ++hist_b;\r\n' \
  '          let offset =  mintime - mintime_foc;\r\n' \
  '          for (let sp of [spans_foc, spans]) {\r\n' \
  '            for (let p=0; p<sp.length; p++) {\r\n' \
  '              let t = Date.parse(document.getElementById(sp[p].id.replace("focus", "time")).value);\r\n' \
  '              if (! isNaN(t)) {\r\n' \
  '                focused = sp[p].id.slice(0, -5);\r\n' \
  '                let ex_time = document.getElementById(sp[p].id.replace("focus", "time")).value;\r\n' \
  '                let new_time = (new Date(Math.round((t + offset) / 1000) * 1000)).toISOString().replace(/\\.[0-9]*/,"");\r\n' \
  '                save_old();\r\n' \
  '                hist[0].push([focused, foc_old, batch]);\r\n' \
  '                document.getElementById(sp[p].id.replace("focus", "time")).value = new_time;\r\n' \
  '                for (let i=hist[1].length - 1; i>=0 ;i--) {\r\n' \
  '                 if (hist[1][i][0] == focused) {hist[1].splice(i, 1);}\r\n' \
  '                }\r\n' \
  '                point_edit(false, false, false, false);\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            offset = maxtime_foc - maxtime;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        seg_foc.scrollIntoView({block:"start"});\r\n' \
  '        let pt_ref = seg.firstElementChild;\r\n' \
  '        while (pt_ref.id.indexOf("point") < 0) {\r\n' \
  '          pt_ref = pt_ref.nextElementSibling;\r\n' \
  '          if (! pt_ref) {break;}\r\n' \
  '        }\r\n' \
  '        if (pt_ref) {\r\n' \
  '          for (let i=0; i<seg_foc.children.length; i++) {\r\n' \
  '            if (seg_foc.children[i].id.indexOf("point") < 0) {continue;}\r\n' \
  '            handle.insertBefore(document.getElementById(seg_foc.children[i].id.slice(0, -4).replace("point", "dot")), document.getElementById(pt_ref.id.slice(0, -4).replace("point", "dot")));\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        handle.insertBefore(document.getElementById("track" + seg_foc.id.slice(7, -4)), document.getElementById("track" + seg.id.slice(7, -4)));\r\n' \
  '        if (focused != seg_foc.id.slice(0, -4)) {element_click(null, seg_foc.firstElementChild.nextElementSibling);}\r\n' \
  '        segment_renum();\r\n' \
  '        segments_calc(seg, seg_foc);\r\n' \
  '        show_msg("{#jmelementup2#}", 2);\r\n' \
  '      }\r\n' \
  '      function element_down() {\r\n' \
  '        if (focused.substring(0, 5) == "point") {\r\n' \
  '          let seg = document.getElementById(focused + "cont").parentNode.nextElementSibling;\r\n' \
  '          if (seg == null) {return;}\r\n' \
  '          seg = seg.firstElementChild.nextElementSibling;\r\n' \
  '          element_click(null, seg);\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (focused.substring(0, 3) != "seg" && focused.substring(0, 3) != "way") {return;}\r\n' \
  '        let elt_foc = document.getElementById(focused + "cont");\r\n' \
  '        let elt = elt_foc.nextElementSibling;\r\n' \
  '        if (! elt) {return;}\r\n' \
  '        focused = elt.id.slice(0, -4);\r\n' \
  '        element_up();\r\n' \
  '        if (focused != elt_foc.id.slice(0, -4)) {element_click(null, elt_foc.firstElementChild.nextElementSibling);};\r\n' \
  '        elt_foc.scrollIntoView({block:"start"});\r\n' \
  '      }\r\n' \
  '      function segment_reverse() {\r\n' \
  '        let whole = false;\r\n' \
  '        let segs = null;\r\n' \
  '        let pts = document.getElementById("pointsform");\r\n' \
  '        let wpts = document.getElementById("waypointsform");\r\n' \
  '        if (focused == "") {\r\n' \
  '          if (! window.confirm("{#jrconfirm#}")) {return;}\r\n' \
  '          whole = true;\r\n' \
  '          scroll_to_all();\r\n' \
  '          segs = pts.children;\r\n' \
  '        } else if (focused.substring(0, 3) == "seg") {\r\n' \
  '          let seg_foc = document.getElementById(focused + "cont");\r\n' \
  '          seg_foc.scrollIntoView({block:"start"});\r\n' \
  '          segs = [seg_foc];\r\n' \
  '          scroll_to_track(document.getElementById("track" + seg_foc.id.slice(7, -4)));\r\n' \
  '        } else {return;}\r\n' \
  '        let mintime = null;\r\n' \
  '        let maxtime = null;\r\n' \
  '        for (let s=0; s<segs.length; s++) {\r\n' \
  '          let spans = segs[s].getElementsByTagName("span");\r\n' \
  '          for (let p=0; p<spans.length; p++) {\r\n' \
  '            if (! spans[p].parentNode.firstElementChild.checked || spans[p].parentNode.firstElementChild.value == "error") {continue;}\r\n' \
  '            let t = Date.parse(document.getElementById(spans[p].id.replace("focus", "time")).value);\r\n' \
  '            if (! isNaN(t)) {\r\n' \
  '              if (mintime == null) {mintime = t;} else {mintime = Math.min(mintime, t);}\r\n' \
  '              if (maxtime == null) {maxtime = t;} else {maxtime = Math.max(maxtime, t);}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        for (let s=0; s<segs.length; s++) {\r\n' \
  '          let pt_f = segs[s].firstElementChild;\r\n' \
  '          while (pt_f.id.indexOf("point") < 0) {\r\n' \
  '            pt_f = pt_f.nextElementSibling;\r\n' \
  '            if (! pt_f) {break;}\r\n' \
  '          }\r\n' \
  '          let seg = segs[s].cloneNode(false);\r\n' \
  '          let elt = segs[s].firstChild;\r\n' \
  '          while (elt.nodeName.toUpperCase() != "DIV") {\r\n' \
  '            seg.insertBefore(elt, null);\r\n' \
  '            elt = segs[s].firstChild;\r\n' \
  '            if (! elt) {break;}\r\n' \
  '          }\r\n' \
  '          if (pt_f) {\r\n' \
  '            let pt = segs[s].lastElementChild;\r\n' \
  '            while (pt) {\r\n' \
  '              if (mintime != null && maxtime != null) {\r\n' \
  '                let t = Date.parse(document.getElementById(pt.id.replace("cont", "time")).value);\r\n' \
  '                if (! isNaN(t)) {\r\n' \
  '                  let new_time = (new Date(Math.round((maxtime - t + mintime) / 1000) * 1000)).toISOString().replace(/\\.[0-9]*/,"");\r\n' \
  '                  if (pt.firstElementChild.value != "error") {pt.firstElementChild.value = "edited";}\r\n' \
  '                  document.getElementById(pt.id.replace("cont", "time")).value = new_time;\r\n' \
  '                  document.getElementById(pt.id.replace("cont", "desc")).innerHTML = point_desc(document.getElementById(pt.id.replace("cont", "focus")));\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              seg.insertBefore(pt, null);\r\n' \
  '              if (! whole && pt && pt != pt_f) {\r\n' \
  '                handle.insertBefore(document.getElementById(pt.id.slice(0, -4).replace("point", "dot")), document.getElementById(pt_f.id.slice(0, -4).replace("point", "dot")));\r\n' \
  '              }\r\n' \
  '              pt = segs[s].lastElementChild;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (s > 0) {\r\n' \
  '            pts.insertBefore(seg, segs[0]);\r\n' \
  '            pts.removeChild(segs[s+1]);\r\n' \
  '            handle.insertBefore(document.getElementById("track" + seg.id.slice(7, -4)), document.getElementById("track" + segs[1].id.slice(7, -4)));\r\n' \
  '          } else {\r\n' \
  '            pts.replaceChild(seg, segs[0]);\r\n' \
  '          }\r\n' \
  '          if (Array.isArray(segs)) {segs[0] = seg;}\r\n' \
  '          if (pt_f) {\r\n' \
  '            let path = document.getElementById("path" + segs[0].id.slice(7, -4));\r\n' \
  '            let d = path.getAttribute("d").substring(4).replace("M", "L");\r\n' \
  '            let d_r = "M0 0";\r\n' \
  '            let points = d.match(/[LMm] *\\d+([.]\\d*)? +\\d+([.]\\d*)?/g);\r\n' \
  '            points.reverse();\r\n' \
  '            for (let point of points) {d_r = d_r + " " + point};\r\n' \
  '            d_r = d_r.replace("L", "M");\r\n' \
  '            path.setAttribute("d", d_r);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (! whole) {\r\n' \
  '          segments_calc(segs[0]);\r\n' \
  '          show_msg("{#jmsegmentreverse1#}", 2);\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let wpt_f = wpts.firstElementChild;\r\n' \
  '        let wpt_r = wpt_f;\r\n' \
  '        let wpt = wpt_f;\r\n' \
  '        while (wpt) {\r\n' \
  '          if (mintime != null && maxtime != null) {\r\n' \
  '            let t = Date.parse(document.getElementById(wpt.id.replace("cont", "time")).value);\r\n' \
  '            if (! isNaN(t)) {\r\n' \
  '              let new_time = (new Date(Math.round((maxtime - t + mintime) / 1000) * 1000)).toISOString().replace(/\\.[0-9]*/,"");\r\n' \
  '              if (wpt.firstElementChild.value != "error") {wpt.firstElementChild.value = "edited";}\r\n' \
  '              document.getElementById(wpt.id.replace("cont", "time")).value = new_time;\r\n' \
  '              document.getElementById(wpt.id.replace("cont", "desc")).innerHTML = point_desc(document.getElementById(wpt.id.replace("cont", "focus")));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          wpt = wpt_f.nextElementSibling;\r\n' \
  '          if (wpt) {\r\n' \
  '            wpts.insertBefore(wpt, wpt_r);\r\n' \
  '            wpt_r = wpt;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        let wdot_f = document.getElementById("track" + segs[segs.length - 1].id.slice(7, -4)).nextElementSibling;\r\n' \
  '        let wdot_r = wdot_f;\r\n' \
  '        let wdot = wdot_f;\r\n' \
  '        if (wdot_f) {\r\n' \
  '          if (wdot_f.id.substring(0, 3) != "way") {wdot = null;}\r\n' \
  '        }\r\n' \
  '        while (wdot) {\r\n' \
  '          wdot = wdot_f.nextElementSibling;\r\n' \
  '          if (wdot) {\r\n' \
  '            if (wdot.id.substring(0, 3) != "way") {wdot = null;}\r\n' \
  '          }\r\n' \
  '          if (wdot) {\r\n' \
  '            handle.insertBefore(wdot, wdot_r);\r\n' \
  '            wdot_r = wdot;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        let dot_f = null;\r\n' \
  '        if (wdot_f) {\r\n' \
  '          if (wdot_f.id.substring(0, 3) == "way") {dot_f = wdot_f.nextElementSibling;} else {dot_f = wdot_f;}\r\n' \
  '        }\r\n' \
  '        let dot_r = dot_f;\r\n' \
  '        let dot = dot_f;\r\n' \
  '        if (dot_f) {\r\n' \
  '          if (dot_f.id.substring(0, 3) != "dot") {dot = null;}\r\n' \
  '        }\r\n' \
  '        while (dot) {\r\n' \
  '          dot = dot_f.nextElementSibling;\r\n' \
  '          if (dot) {\r\n' \
  '            if (dot.id.substring(0, 3) != "dot") {dot = null;}\r\n' \
  '          }\r\n' \
  '          if (dot) {\r\n' \
  '            handle.insertBefore(dot, dot_r);\r\n' \
  '            dot_r = dot;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        segments_calc();\r\n' \
  '        segment_renum();\r\n' \
  '        show_msg("{#jmsegmentreverse2#}", 2);\r\n' \
  '      }\r\n' \
  '      function error_ecb() {\r\n' \
  '      } \r\n' \
  '      function load_ecb(t, pts) {\r\n' \
  '        if (t.status != 200) {return 0;}\r\n' \
  '        if (t.response == "") {return 0;}\r\n' \
  '        let ele = t.response.split("\\r\\n");\r\n' \
  '        let p = 0;\r\n' \
  '        let e = 0;\r\n' \
  '        let ex_foc = focused;\r\n' \
  '        let segs = [];\r\n' \
  '        let batch = ++hist_b;\r\n' \
  '        let np = 0;\r\n' \
  '        while (p < pts.length) {\r\n' \
  '          while (e < ele.length) {\r\n' \
  '            let r = ele[e].split(",");\r\n' \
  '            if (r.length == 2) {\r\n' \
  '              if (pts[p] == r[0]) {\r\n' \
  '                if (r[1].replace(/(^\\s+)|(\\s+$)/g, "") != "") {\r\n' \
  '                  focused = pts[p];\r\n' \
  '                  save_old();\r\n' \
  '                  document.getElementById(focused + "ele").value = r[1];\r\n' \
  '                  hist[0].push([focused, foc_old, batch]);\r\n' \
  '                  save_old();\r\n' \
  '                  for (let i=hist[1].length - 1; i>=0 ;i--) {\r\n' \
  '                    if (hist[1][i][0] == focused) {hist[1].splice(i, 1);}\r\n' \
  '                  }\r\n' \
  '                  point_edit(false, false, false, false);\r\n' \
  '                  np++;\r\n' \
  '                  if (pts[p].slice(0,3) != "way") {\r\n' \
  '                    let seg_p = document.getElementById(pts[p]).parentNode.parentNode;\r\n' \
  '                    if (segs.length == 0) {\r\n' \
  '                      segs = [seg_p];\r\n' \
  '                    } else if (seg_p.id != segs[segs.length - 1].id) {\r\n' \
  '                      segs.push(seg_p);\r\n' \
  '                    } \r\n' \
  '                  }\r\n' \
  '                }\r\n' \
  '                e++;\r\n' \
  '              }\r\n' \
  '              break;\r\n' \
  '            } else {e++;}\r\n' \
  '          }\r\n' \
  '          p++;\r\n' \
  '        }\r\n' \
  '        focused = ex_foc;\r\n' \
  '        if (segs.length > 0) {segments_calc(...segs);}\r\n' \
  '        return np;\r\n'\
  '      }\r\n' \
  '      function ele_adds(all=false, fromalt=false) {\r\n' \
  '        let pts = [];\r\n' \
  '        let b = "";\r\n' \
  '        let spans = null;\r\n' \
  '        let msg = "";\r\n' \
  '        if (focused) {\r\n' \
  '          if (focused.substring(0, 3) == "seg") {\r\n' \
  '            if (all) {\r\n' \
  '              if (! window.confirm("{#jesconfirm#}")) {return;}\r\n' \
  '            }\r\n' \
  '            spans = document.getElementById(focused + "cont").getElementsByTagName("span");\r\n' \
  '            msg = "{#jmelevations3#}";\r\n' \
  '          } else {\r\n' \
  '            spans = [document.getElementById(focused + "focus")];\r\n' \
  '            msg = "{#jmelevations2#}";\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          if (all) {\r\n' \
  '            if (! window.confirm("{#jeconfirm#}")) {return;}\r\n' \
  '          }\r\n' \
  '          if (fromalt) {\r\n' \
  '            spans = document.getElementById("pointsform").getElementsByTagName("span");\r\n' \
  '            msg = "{#jmelevations5#}";\r\n' \
  '          } else {\r\n' \
  '            spans = document.getElementById("content").getElementsByTagName("span");\r\n' \
  '            msg = "{#jmelevations4#}";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        for (let p=(focused?0:2); p<spans.length; p++) {\r\n' \
  '          pid = spans[p].id.slice(0, -5);\r\n' \
  '          if (document.getElementById(pid).value != "error" && (all || document.getElementById(pid + "ele").value.replace(/(^\\s+)|(\\s+$)/g, "") == "")) {\r\n' \
  '           pts.push(pid);\r\n' \
  '           b = b + pid + "," + document.getElementById(pid + "lat").value + "," + document.getElementById(pid + "lon").value + "\\r\\n";\r\n' \
  '          } \r\n' \
  '        }\r\n' \
  '        if (b.length == 0) {return;}\r\n' \
  '        let msgn = show_msg("{#jmelevations1#}", 0);\r\n' \
  '        if (fromalt) {\r\n' \
  '          let t = new Object;\r\n' \
  '          t.status = 200;\r\n' \
  '          t.response = "";\r\n' \
  '          for (let p of pts) {\r\n' \
  '            t.response = t.response + p + "," + document.getElementById(p + "alt").value + "\\r\\n";\r\n' \
  '          }\r\n' \
  '          let np = load_ecb(t, pts);\r\n' \
  '          if (np) {\r\n' \
  '            show_msg(msg.replace("%s", np.toString()).replace("%s", pts.length.toString()), 4, msgn);\r\n' \
  '          } else {\r\n' \
  '            show_msg("Échec de la récupération des élévations", 10, msgn);\r\n' \
  '          }\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let xhre = new XMLHttpRequest();\r\n' \
  '        xhre.onload = (e) => {let np = load_ecb(e.target, pts); np?show_msg(msg.replace("%s", np.toString()).replace("%s", pts.length.toString()), 4, msgn):show_msg("{#jmelevations6#}", 10, msgn);};\r\n' \
  '        xhre.onerror = (e) => {error_ecb(); show_msg("{#jmelevations6#}", 10, msgn);};\r\n' \
  '        xhre.open("POST", "/ele");\r\n' \
  '        xhre.setRequestHeader("Content-Type", "application/octet-stream");\r\n' \
  '        xhre.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhre.send(b);\r\n' \
  '      }\r\n' \
  '      function ele_alt_switch() {\r\n' \
  '        let spans = null;\r\n' \
  '        let msg = "";\r\n' \
  '        let ex_foc = focused;\r\n' \
  '        let seg = null;\r\n' \
  '        if (ex_foc) {\r\n' \
  '          if (ex_foc.substring(0, 3) == "seg") {\r\n' \
  '            if (! window.confirm("{#jeasconfirm#}")) {return;}\r\n' \
  '            spans = document.getElementById(ex_foc + "cont").getElementsByTagName("span");\r\n' \
  '            msg = "{#jmelealt2#}";\r\n' \
  '            seg = document.getElementById(ex_foc + "cont");\r\n' \
  '          } else if (ex_foc.substring(0, 3) == "way") {\r\n' \
  '            return;\r\n' \
  '          } else {\r\n' \
  '            spans = [document.getElementById(ex_foc + "focus")];\r\n' \
  '            msg = "{#jmelealt1#}";\r\n' \
  '            seg = document.getElementById(ex_foc + "cont").parentNode;\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          if (! window.confirm("{#jeaconfirm#}")) {return;}\r\n' \
  '          spans = document.getElementById("points").getElementsByTagName("span");\r\n' \
  '          msg = "{#jmelealt3#}";\r\n' \
  '        }\r\n' \
  '        if (spans.length == 0) {return;}\r\n' \
  '        let batch = ++hist_b;\r\n' \
  '        for (let p=0; p<spans.length; p++) {\r\n' \
  '          focused = spans[p].id.slice(0, -5);\r\n' \
  '          save_old();\r\n' \
  '          let g = document.getElementById(focused + "ele").value;\r\n' \
  '          document.getElementById(focused + "ele").value = document.getElementById(focused + "alt").value;\r\n' \
  '          document.getElementById(focused + "alt").value = g;\r\n' \
  '          hist[0].push([focused, foc_old, batch]);\r\n' \
  '          save_old();\r\n' \
  '          for (let i=hist[1].length - 1; i>=0 ;i--) {\r\n' \
  '            if (hist[1][i][0] == focused) {hist[1].splice(i, 1);}\r\n' \
  '          }\r\n' \
  '          point_edit(false, false, false, false);\r\n' \
  '        }\r\n' \
  '        focused = ex_foc;\r\n' \
  '        if (seg != null) {segments_calc(seg);} else {segments_calc();}\r\n' \
  '        show_msg(msg, 2);\r\n' \
  '      }\r\n' \
  '      function alt_join() {\r\n' \
  '        let seg_foc = null;\r\n' \
  '        let pt_foc = null;\r\n' \
  '        if (focused.substring(0, 3) == "seg") {\r\n' \
  '          seg_foc = document.getElementById(focused + "cont");\r\n' \
  '        } else if (focused.substring(0, 5) == "point") {\r\n' \
  '          if (! document.getElementById(focused).checked || document.getElementById(focused).value == "error") {return;}\r\n' \
  '          pt_foc = document.getElementById(focused + "cont");\r\n' \
  '          seg_foc = pt_foc.parentNode;\r\n' \
  '        } else {\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (! seg_foc.firstElementChild.checked || seg_foc.lastElementChild.id.indexOf("point") < 0) {return;}\r\n' \
  '        let spans = seg_foc.getElementsByTagName("span");\r\n' \
  '        let stime = null;\r\n' \
  '        let etime = null;\r\n' \
  '        let ralt = null;\r\n' \
  '        let sp = 0;\r\n' \
  '        for (let p=0; p<spans.length; p++) {\r\n' \
  '          let pid = spans[p].id.slice(0, -5);\r\n' \
  '          if (pt_foc != null && pt_foc.id.slice(0, -4) != pid && stime == null) {continue;}\r\n' \
  '          if (document.getElementById(pid).checked && document.getElementById(pid).value != "error") {\r\n' \
  '            ralt = parseFloat(document.getElementById(pid + "alt").value);\r\n' \
  '            if (isNaN(ralt)) {continue;}\r\n' \
  '            if (pt_foc != null) {\r\n' \
  '              let tim = Date.parse(document.getElementById(pid + "time").value);\r\n' \
  '              if (stime == null) {\r\n' \
  '                if (isNaN(tim)) {return;}\r\n' \
  '                sp = p;\r\n' \
  '                stime = tim;\r\n' \
  '              }\r\n' \
  '              etime = tim;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (ralt == null) {return;}\r\n' \
  '        if (pt_foc != null) {\r\n' \
  '          if (etime == null || stime == null) {return;}\r\n' \
  '          if (stime >= etime) {return;}\r\n' \
  '        }\r\n' \
  '        let seg = seg_foc.nextElementSibling;\r\n' \
  '        while (seg) {\r\n' \
  '          if (seg.firstElementChild.checked) {break;}\r\n' \
  '          seg = seg.nextElementSibling;\r\n' \
  '        }\r\n' \
  '        if (! seg) {return;}\r\n' \
  '        let pt = seg.firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling;\r\n' \
  '        while(pt) {\r\n' \
  '          if (pt.firstElementChild.checked && pt.firstElementChild.value != "error") {break;}\r\n' \
  '          pt = pt.nextElementSibling;\r\n' \
  '        }\r\n' \
  '        if (! pt) {return;}\r\n' \
  '        let talt = parseFloat(document.getElementById(pt.id.replace("cont", "alt")).value);\r\n' \
  '        if (isNaN(talt)) {return;}\r\n' \
  '        let cor = null;\r\n' \
  '        if (pt_foc != null) {\r\n' \
  '          cor = (talt - ralt) / (etime - stime);\r\n' \
  '        } else {\r\n' \
  '          cor = talt - ralt;\r\n' \
  '        }\r\n' \
  '        let batch = ++hist_b;\r\n' \
  '        for (let p=sp; p<spans.length; p++) {\r\n' \
  '          let pid = spans[p].id.slice(0, -5);\r\n' \
  '          let palt = parseFloat(document.getElementById(pid + "alt").value);\r\n' \
  '          if (! isNaN(palt)) {\r\n' \
  '            if (pt_foc != null) {\r\n' \
  '              let ptime = Date.parse(document.getElementById(pid + "time").value);\r\n' \
  '              if (! isNaN(ptime)) {\r\n' \
  '                focused = pid;\r\n' \
  '                save_old();\r\n' \
  '                document.getElementById(pid + "alt").value = (palt + cor * (ptime - stime)).toFixed(1);\r\n' \
  '                hist[0].push([focused, foc_old, batch]);\r\n' \
  '                save_old();\r\n' \
  '                for (let i=hist[1].length - 1; i>=0 ;i--) {\r\n' \
  '                  if (hist[1][i][0] == focused) {hist[1].splice(i, 1);}\r\n' \
  '                }\r\n' \
  '                point_edit(false, false, false, false);\r\n' \
  '              }\r\n' \
  '            } else {\r\n' \
  '              focused = pid;\r\n' \
  '              save_old();\r\n' \
  '              document.getElementById(pid + "alt").value = (palt + cor).toFixed(1);\r\n' \
  '              hist[0].push([focused, foc_old, batch]);\r\n' \
  '              save_old();\r\n' \
  '              for (let i=hist[1].length - 1; i>=0 ;i--) {\r\n' \
  '                if (hist[1][i][0] == focused) {hist[1].splice(i, 1);}\r\n' \
  '              }\r\n' \
  '              point_edit(false, false, false, false);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (pt_foc) {focused = pt_foc.id.slice(0, -4);}\r\n' \
  '        if (! pt_foc) {focused = seg_foc.id.slice(0, -4);}\r\n' \
  '        segments_calc(seg_foc);\r\n' \
  '        show_msg(((pt_foc==null)?"{#jmaltitudesjoin1#}":"{#jmaltitudesjoin2#}"), 2);\r\n' \
  '      }\r\n' \
  '      function datetime_interpolate() {\r\n' \
  '        let segs = [];\r\n' \
  '        let seg_foc = null;\r\n' \
  '        let pt_foc = null;\r\n' \
  '        if (focused == "") {\r\n' \
  '          let segms = document.getElementById("pointsform").children;\r\n' \
  '          for (let s=0; s<segms.length; s++) {\r\n' \
  '            if (document.getElementById(segms[s].id.slice(0, -4)).checked) {segs.push(segms[s]);}\r\n' \
  '          }\r\n' \
  '          if (segs.length == 0) {return;}\r\n' \
  '          scroll_to_all();\r\n' \
  '        } else if (focused.substring(0, 3) == "seg") {\r\n' \
  '          seg_foc = document.getElementById(focused + "cont");\r\n' \
  '          seg_foc.scrollIntoView({block:"start"});\r\n' \
  '          segs = [seg_foc];\r\n' \
  '          scroll_to_track(document.getElementById("track" + seg_foc.id.slice(7, -4)));\r\n' \
  '        } else if (focused.substring(0, 5) == "point") {\r\n' \
  '          if (! document.getElementById(focused).checked || document.getElementById(focused).value == "error") {return;}\r\n' \
  '          pt_foc = focused;\r\n' \
  '          document.getElementById(pt_foc + "cont").scrollIntoView({block:"nearest"});\r\n' \
  '          seg_foc = document.getElementById(pt_foc + "cont").parentNode;\r\n' \
  '          segs = [seg_foc];\r\n' \
  '          scroll_to_dot(document.getElementById(pt_foc.replace("point", "dot")));\r\n' \
  '        } else {\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let batch = ++hist_b;\r\n' \
  '        for (let s=0; s<segs.length; s++) {\r\n' \
  '          let spans = segs[s].getElementsByTagName("span");\r\n' \
  '          let lc = -1;\r\n' \
  '          let pm = [];\r\n' \
  '          let pm_b = [];\r\n' \
  '          let pt = "";\r\n' \
  '          let stime = null;\r\n' \
  '          let etime = null;\r\n' \
  '          let btime = null;\r\n' \
  '          let dist = 0;\r\n' \
  '          let dist_b = 0;\r\n' \
  '          let pele = null;\r\n' \
  '          let ele = null;\r\n' \
  '          let inv_vit = 0;\r\n' \
  '          let pp = 0;\r\n' \
  '          for (let p=0; p<spans.length; p++) {\r\n' \
  '            pt = spans[p].id.slice(0, -5);\r\n' \
  '            if (! document.getElementById(pt).checked || document.getElementById(pt).value == "error") {continue;}\r\n' \
  '            etime = Date.parse(document.getElementById(pt + "time").value.trim());\r\n' \
  '            ele = parseFloat(document.getElementById(pt + "alt").value);\r\n' \
  '            if (isNaN(ele)) {\r\n' \
  '             ele = parseFloat(document.getElementById(pt + "ele").value);\r\n' \
  '            }\r\n' \
  '            if (isNaN(ele)) {ele = pele;}\r\n' \
  '            let valid = ! isNaN(etime);\r\n' \
  '            if (valid && stime != null) {valid = etime >= stime;}\r\n' \
  '            if (! valid) {\r\n' \
  '              if (pm_b != null && lc == -1) {\r\n' \
  '                dist_b += distance(document.getElementById(spans[pp].id.replace("focus", "lat")).value, document.getElementById(spans[pp].id.replace("focus", "lon")).value, pele==null?0:pele, document.getElementById(spans[p].id.replace("focus", "lat")).value, document.getElementById(spans[p].id.replace("focus", "lon")).value, pele==null?0:ele);\r\n' \
  '                if (pt_foc == null || pt_foc == pt) {\r\n' \
  '                  pm_b.push([p, dist_b]);\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              if (lc != -1) {\r\n' \
  '                dist += distance(document.getElementById(spans[pp].id.replace("focus", "lat")).value, document.getElementById(spans[pp].id.replace("focus", "lon")).value, pele==null?0:pele, document.getElementById(spans[p].id.replace("focus", "lat")).value, document.getElementById(spans[p].id.replace("focus", "lon")).value, pele==null?0:ele);\r\n' \
  '              }\r\n' \
  '              if (pt_foc == null || pt_foc == pt) {\r\n' \
  '                pm.push([p, dist]);\r\n' \
  '              }\r\n' \
  '              if (p == spans.length - 1 && inv_vit > 0) {\r\n' \
  '                for (let i=0; i<pm.length; i++) {\r\n' \
  '                  focused = spans[pm[i][0]].id.slice(0, -5);\r\n' \
  '                  save_old();\r\n' \
  '                  hist[0].push([focused, foc_old, batch]);\r\n' \
  '                  document.getElementById(spans[pm[i][0]].id.replace("focus", "time")).value = (new Date(Math.round((stime + inv_vit * pm[i][1]) / 1000) * 1000)).toISOString().replace(/\.[0-9]*/,"");\r\n' \
  '                  for (let j=hist[1].length - 1; j>=0 ;j--) {\r\n' \
  '                    if (hist[1][j][0] == focused) {hist[1].splice(j, 1);}\r\n' \
  '                  }\r\n' \
  '                  point_edit(false, false, false, false);\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '            } else {\r\n' \
  '              dist += distance(document.getElementById(spans[pp].id.replace("focus", "lat")).value, document.getElementById(spans[pp].id.replace("focus", "lon")).value, pele==null?0:pele, document.getElementById(spans[p].id.replace("focus", "lat")).value, document.getElementById(spans[p].id.replace("focus", "lon")).value, pele==null?0:ele);\r\n' \
  '              if (dist > 0 && lc != -1 && etime > stime) {inv_vit = (etime - stime) / dist;}\r\n' \
  '              if (pm_b != null) {\r\n' \
  '                if (lc == -1) {\r\n' \
  '                  dist_b += distance(document.getElementById(spans[pp].id.replace("focus", "lat")).value, document.getElementById(spans[pp].id.replace("focus", "lon")).value, pele==null?0:pele, document.getElementById(spans[p].id.replace("focus", "lat")).value, document.getElementById(spans[p].id.replace("focus", "lon")).value, pele==null?0:ele);\r\n' \
  '                  btime = etime;\r\n' \
  '                }\r\n' \
  '                if (dist_b == 0 || inv_vit > 0) {\r\n' \
  '                  for (let i=0; i<pm_b.length; i++) {\r\n' \
  '                    focused = spans[pm_b[i][0]].id.slice(0, -5);\r\n' \
  '                    save_old();\r\n' \
  '                    hist[0].push([focused, foc_old, batch]);\r\n' \
  '                    document.getElementById(spans[pm_b[i][0]].id.replace("focus", "time")).value = (new Date(Math.round((dist_b==0?btime:(btime + inv_vit * (pm_b[i][1] - dist_b))) / 1000) * 1000)).toISOString().replace(/\.[0-9]*/,"");\r\n' \
  '                    for (let j=hist[1].length - 1; j>=0 ;j--) {\r\n' \
  '                      if (hist[1][j][0] == focused) {hist[1].splice(j, 1);}\r\n' \
  '                    }\r\n' \
  '                    point_edit(false, false, false, false);\r\n' \
  '                  }\r\n' \
  '                  if (pt_foc != null && pm_b.length > 0) {\r\n' \
  '                    save_old();\r\n' \
  '                    segments_calc(segs[s]);\r\n' \
  '                    show_msg("Horodatage du point mis à jour", 2);\r\n' \
  '                    return;\r\n' \
  '                  }\r\n' \
  '                  pm_b = null;\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              if (pm.length > 0 && lc != -1) {\r\n' \
  '                for (let i=0; i<pm.length; i++) {\r\n' \
  '                  focused = spans[pm[i][0]].id.slice(0, -5);\r\n' \
  '                  save_old();\r\n' \
  '                  hist[0].push([focused, foc_old, batch]);\r\n' \
  '                  document.getElementById(spans[pm[i][0]].id.replace("focus", "time")).value = (new Date(Math.round((stime + (etime - stime) * pm[i][1] / (dist>0?dist:1)) / 1000) * 1000)).toISOString().replace(/\\.[0-9]*/,"");\r\n' \
  '                  for (let j=hist[1].length - 1; j>=0 ;j--) {\r\n' \
  '                    if (hist[1][j][0] == focused) {hist[1].splice(j, 1);}\r\n' \
  '                  }\r\n' \
  '                  point_edit(false, false, false, false);\r\n' \
  '                }\r\n' \
  '                if (pt_foc != null) {\r\n' \
  '                  save_old();\r\n' \
  '                  segments_calc(segs[s]);\r\n' \
  '                  show_msg("{#jmdatetime1#}", 2);\r\n' \
  '                  return;\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              lc = p;\r\n' \
  '              pm = [];\r\n' \
  '              stime = etime;\r\n' \
  '              dist = 0;\r\n' \
  '            }\r\n' \
  '            pele = ele;\r\n' \
  '            pp = p;\r\n' \
  '          }\r\n' \
  '          if (pt_foc != null) {\r\n' \
  '            segments_calc(segs[s]);\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        let msg = focused.indexOf("point")<0?null:(seg_foc!=null?"Horodatages du segment mis à jour":"Horodatages de la trace mis à jour");\r\n' \
  '        if (pt_foc == null && seg_foc != null && focused.substring(0, 3) != "seg") {focused = seg_foc.id.slice(0, -4);}\r\n' \
  '        if (pt_foc == null && seg_foc == null && focused != "") {focused = "";}\r\n' \
  '        segments_calc(...segs);\r\n' \
  '        if (msg) {show_msg(msg, 2);}\r\n' \
  '      }\r\n' \
  '      function switch_dots() {\r\n' \
  '        dots_visible = ! dots_visible;\r\n' \
  '        let spans = document.getElementById("points").getElementsByTagName("span");\r\n' \
  '        for (let i=0; i<spans.length; i++) {dot_style(spans[i].id.slice(0, -5), false);}\r\n' \
  '        spans = document.getElementById("waypoints").getElementsByTagName("span");\r\n' \
  '        for (let i=0; i<spans.length; i++) {dot_style(spans[i].id.slice(0, -5), false);}\r\n' \
  '      }\r\n' \
  '      function refresh_graph(sw=false) {\r\n' \
  '        let graph = document.getElementById("graph");\r\n' \
  '        let graphc = document.getElementById("graphc");\r\n' \
  '        let gwidth = null;\r\n' \
  '        let gheight = null;\r\n' \
  '        let gctx = graphc.getContext("2d");\r\n' \
  '        if (sw) {\r\n' \
  '          if (graph.style.display == "none") {\r\n' \
  '            document.getElementById("content").style.height = "calc(74vh - 2.4em - 18px)";\r\n' \
  '            viewpane.style.height = "calc(74vh - 2.4em - 18px)";\r\n' \
  '            graph.style.display = "block";\r\n' \
  '            gctx.lineWidth = 1;\r\n' \
  '            gctx.lineJoin = "round";\r\n' \
  '            gctx.lineCap = "square";\r\n' \
  '            rescale();\r\n' \
  '          } else {\r\n' \
  '            document.getElementById("content").style.height = "calc(99vh - 2.4em - 16px)";\r\n' \
  '            viewpane.style.height = "calc(99vh - 2.4em - 16px)";\r\n' \
  '            graph.style.display = "none";\r\n' \
  '            document.getElementById("gbar").style.display = "none";\r\n' \
  '            document.getElementById("gbarc").style.display = "none";\r\n' \
  '            graph_ip = null;\r\n' \
  '            graph_px = null;\r\n' \
  '            rescale();\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          if (graph.style.display == "none") {return;}\r\n' \
  '        }\r\n' \
  '        gwidth = graph.offsetWidth - graphc.offsetLeft;\r\n' \
  '        gheight = graph.offsetHeight;\r\n' \
  '        graphc.setAttribute("width", gwidth.toString());\r\n' \
  '        graphc.setAttribute("height", gheight.toString());\r\n' \
  '        let gbar = document.getElementById("gbar");\r\n' \
  '        gbar.style.top= "10px";\r\n' \
  '        gbar.setAttribute("height", (gheight - 25).toString());\r\n' \
  '        let gbarc = document.getElementById("gbarc");\r\n' \
  '        gbarc.style.top= "10px";\r\n' \
  '        gbarc.setAttribute("height", (gheight - 25).toString());\r\n' \
  '        gctx.fillStyle = "rgb(40,45,50)";\r\n' \
  '        gctx.fillRect(0, 0, gwidth, gheight);\r\n' \
  '        let xl = 45;\r\n' \
  '        let xr = gwidth - 20;\r\n' \
  '        let yt = 10;\r\n' \
  '        let yb = gheight - 15;\r\n' \
  '        let gx = [];\r\n' \
  '        let gy = [];\r\n' \
  '        let gc = [0];\r\n' \
  '        let dur = 0;\r\n' \
  '        let dist = 0;\r\n' \
  '        let ele = 0;\r\n' \
  '        let alt = 0;\r\n' \
  '        graph_ip = [];\r\n' \
  '        graph_px = Array(document.getElementById("points").getElementsByTagName("span").length);\r\n' \
  '        let segs = document.getElementById("pointsform").children;\r\n' \
  '        for (let s=0; s<segs.length; s++) {\r\n' \
  '          if (! segs[s].firstElementChild.checked) {continue;}\r\n' \
  '          let seg_ind = parseInt(segs[s].id.slice(7, -4));\r\n' \
  '          if (stats[seg_ind].length == 0) {continue;}\r\n' \
  '          let stat = null;\r\n' \
  '          let spans = segs[s].getElementsByTagName("span");\r\n' \
  '          if (gc[gc.length - 1] != graph_ip.length) {gc.push(graph_ip.length);}\r\n' \
  '          for (let p=0; p<spans.length; p++) {\r\n' \
  '            let st = point_stat[parseInt(spans[p].id.slice(5, -5))];\r\n' \
  '            if (st == null) {continue;}\r\n' \
  '            stat = stats[seg_ind][st];\r\n' \
  '            let dr = true;\r\n' \
  '            switch (document.getElementById("graphy").selectedIndex) {\r\n' \
  '              case 0:\r\n' \
  '                gy.push(dist + stat[1]);\r\n' \
  '                break;\r\n' \
  '              case 1:\r\n' \
  '                let e = parseFloat(document.getElementById(spans[p].id.replace("focus", "ele")).value);\r\n' \
  '                if (isNaN(e)) {\r\n' \
  '                  dr = false;\r\n' \
  '                } else {\r\n' \
  '                  gy.push(e);\r\n' \
  '                }\r\n' \
  '                break;\r\n' \
  '              case 2:\r\n' \
  '                let a = parseFloat(document.getElementById(spans[p].id.replace("focus", "alt")).value);\r\n' \
  '                if (isNaN(a)) {\r\n' \
  '                  dr = false;\r\n' \
  '                } else {\r\n' \
  '                  gy.push(a);\r\n' \
  '                }\r\n' \
  '                break;\r\n' \
  '              case 3:\r\n' \
  '                gy.push(ele + stat[2]);\r\n' \
  '                break;\r\n' \
  '              case 4:\r\n' \
  '                gy.push(alt + stat[3]);\r\n' \
  '                break;\r\n' \
  '              case 5:\r\n' \
  '                gy.push(stat[4] * 100);\r\n' \
  '                break;\r\n' \
  '              case 6:\r\n' \
  '                gy.push(stat[5] * 100);\r\n' \
  '                break;\r\n' \
  '              case 7:\r\n' \
  '                gy.push(stat[6] * 3.6);\r\n' \
  '                break;\r\n' \
  '            }\r\n' \
  '            if (dr) {\r\n' \
  '              switch (document.getElementById("graphx").selectedIndex) {\r\n' \
  '                case 0:\r\n' \
  '                  gx.push(dur + stat[0]);\r\n' \
  '                  break;\r\n' \
  '                case 1:\r\n' \
  '                  gx.push(dist + stat[1]);\r\n' \
  '                  break;\r\n' \
  '              }\r\n' \
  '              graph_ip.push(parseInt(spans[p].id.slice(5, -5)));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          dur += stat[0];\r\n' \
  '          dist += stat[1];\r\n' \
  '          ele += stat[2];\r\n' \
  '          alt += stat[3];\r\n' \
  '        }\r\n' \
  '        if (gx.length < 2) {\r\n' \
  '          graph_point();\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let minx = gx[0];\r\n' \
  '        let maxx = gx[0];\r\n' \
  '        let miny = gy[0];\r\n' \
  '        let maxy = gy[0];\r\n' \
  '        for (let i=0; i<gx.length; i++) {\r\n' \
  '          if (minx > gx[i]) {minx = gx[i];}\r\n' \
  '          if (maxx < gx[i]) {maxx = gx[i];}\r\n' \
  '          if (miny > gy[i]) {miny = gy[i];}\r\n' \
  '          if (maxy < gy[i]) {maxy = gy[i];}\r\n' \
  '        }\r\n' \
  '        if (maxx == minx) {maxx++;}\r\n' \
  '        if (maxy == miny) {maxy++;}\r\n' \
  '        let cx = (xr - xl) / (maxx - minx);\r\n' \
  '        let cy = (yb - yt) / (maxy - miny);\r\n' \
  '        let yl = 0;\r\n' \
  '        if (document.getElementById("graphy").selectedIndex == 0) {\r\n' \
  '          yl = yb;\r\n' \
  '        } else if (maxy < 0) {\r\n' \
  '          yl = yt;\r\n' \
  '        } else if (miny > 0) {\r\n' \
  '          yl = yb;\r\n' \
  '        } else {\r\n' \
  '          yl = maxy * cy + yt;\r\n' \
  '        }\r\n' \
  '        gctx.strokeStyle = "rgb(56,56,56)";\r\n' \
  '        gctx.beginPath();\r\n' \
  '        let x = xl;\r\n' \
  '        let dx = (xr - xl) / Math.floor((xr - xl) / 100);\r\n' \
  '        while (x <= xr) {\r\n' \
  '          gctx.moveTo(x, yb + 1);\r\n' \
  '          gctx.lineTo(x, yt);\r\n' \
  '          if (x == xr) {break;}\r\n' \
  '          x += dx;\r\n' \
  '          if (x > xr) {x = xr;}\r\n' \
  '        }\r\n' \
  '        let y = yb;\r\n' \
  '        let dy = (yb - yt) / Math.floor((yb - yt) / 50);\r\n' \
  '        while (y >= yt) {\r\n' \
  '          gctx.moveTo(xl + 1, y);\r\n' \
  '          gctx.lineTo(xr, y);\r\n' \
  '          if (y == yt) {break;}\r\n' \
  '          y -= dy;\r\n' \
  '          if (y < yt) {y = yt;}\r\n' \
  '        }\r\n' \
  '        gctx.stroke();\r\n' \
  '        gctx.strokeStyle = "rgb(225,225,225)";\r\n' \
  '        gctx.beginPath();\r\n' \
  '        gctx.moveTo(xl, yb);\r\n' \
  '        gctx.lineTo(xl, yt);\r\n' \
  '        gctx.moveTo(xl, yl);\r\n' \
  '        gctx.lineTo(xr, yl);\r\n' \
  '        gctx.lineTo(xr, yl - 1);\r\n' \
  '        gctx.lineTo(xr, yl + 1);\r\n' \
  '        gctx.stroke();\r\n' \
  '        gctx.fillStyle = "rgb(225,225,255)";\r\n' \
  '        gctx.textAlign = "center";\r\n' \
  '        gctx.textBaseline = "top";\r\n' \
  '        x = xl;\r\n' \
  '        while (x <= xr) {\r\n' \
  '          if (document.getElementById("graphx").selectedIndex == 0) {\r\n' \
  '            let dur = Math.round((minx + (x - xl) / cx) / 60) * 60;\r\n' \
  '            let dur_m = (dur / 60) % 60;\r\n' \
  '            let dur_h = (dur - dur_m * 60) / 3600;\r\n' \
  '            let dur_c = dur_h.toString() + "h" + dur_m.toString().padStart(2, "0") + "mn";\r\n' \
  '            gctx.fillText(dur_c, x, yl + 3);\r\n' \
  '          } else {\r\n' \
  '            gctx.fillText(((minx + (x - xl) / cx) / 1000).toFixed(1) + "km", x, yl + 3);\r\n' \
  '          }\r\n' \
  '          if (x == xr) {break;}\r\n' \
  '          x += dx;\r\n' \
  '          if (x > xr) {x = xr;}\r\n' \
  '        }\r\n' \
  '        gctx.textAlign = "right";\r\n' \
  '        gctx.textBaseline = "middle";\r\n' \
  '        y = yb;\r\n' \
  '        let fin = false;\r\n' \
  '        while (true) {\r\n' \
  '          if (y - yl >= 16 || yl - y >= 10 || fin) {\r\n' \
  '            if (document.getElementById("graphy").selectedIndex == 0) {\r\n' \
  '              gctx.fillText(((maxy - (y - yt) / cy) / 1000).toFixed(1).replace(/^-(0*(\.0*)?$)/,"$1") + "km", xl - 2, y);\r\n' \
  '            } else if (document.getElementById("graphy").selectedIndex == 5 || document.getElementById("graphy").selectedIndex == 6) {\r\n' \
  '              gctx.fillText((maxy - (y - yt) / cy).toFixed(0).replace(/^-(0*(\.0*)?$)/,"$1") + "%", xl - 2, y);\r\n' \
  '            } else if (document.getElementById("graphy").selectedIndex == 7) {\r\n' \
  '              gctx.fillText((maxy - (y - yt) / cy).toFixed(1).replace(/^-(0*(\.0*)?$)/,"$1") + "km/h", xl - 2, y);\r\n' \
  '            } else {\r\n' \
  '              gctx.fillText((maxy - (y - yt) / cy).toFixed(0).replace(/^-(0*(\.0*)?$)/,"$1") + "m", xl - 2, y);\r\n' \
  '            }\r\n' \
  '            if (fin) {break;}\r\n' \
  '          }\r\n' \
  '          if (y == yt) {\r\n' \
  '            y = yl;\r\n' \
  '            fin = true;\r\n' \
  '            continue;\r\n' \
  '          }\r\n' \
  '          y -= dy;\r\n' \
  '          if (y < yt) {y = yt;}\r\n' \
  '        }\r\n' \
  '        gctx.strokeStyle = "rgb(255,0,0)";\r\n' \
  '        gctx.beginPath();\r\n' \
  '        for (let i=0; i<gx.length; i++) {\r\n' \
  '          graph_px[graph_ip[i]] = (gx[i] - minx) * cx + xl;\r\n' \
  '          if (i == gc[0]) {\r\n' \
  '            gctx.moveTo(graph_px[graph_ip[i]], (maxy - gy[i]) * cy + yt);\r\n' \
  '            gc.shift();\r\n' \
  '          } else {\r\n' \
  '            gctx.lineTo(graph_px[graph_ip[i]], (maxy - gy[i]) * cy + yt);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        gctx.stroke();\r\n' \
  '        graph_point();\r\n' \
  '      }\r\n' \
  '      function graph_point(dx) {\r\n' \
  '        let graph = document.getElementById("graph");\r\n' \
  '        if (graph.style.display == "none") {return;}\r\n' \
  '        let graphc = document.getElementById("graphc");\r\n' \
  '        let xl = graphc.offsetLeft + 45;\r\n' \
  '        let xr = graphc.offsetLeft + parseFloat(graphc.getAttribute("width")) - 20;\r\n' \
  '        let gbar = document.getElementById("gbar");\r\n' \
  '        gbar.style.display = "none";\r\n' \
  '        let gbarc = document.getElementById("gbarc");\r\n' \
  '        gbarc.style.display = "none";\r\n' \
  '        let graphpx = document.getElementById("graphpx");\r\n' \
  '        let graphpy = document.getElementById("graphpy");\r\n' \
  '        let gpx = graphpx.innerHTML;\r\n' \
  '        let gpy = graphpy.innerHTML;\r\n' \
  '        graphpx.innerHTML = "";\r\n' \
  '        graphpy.innerHTML = "";\r\n' \
  '        if (graph_ip.length < 2) {return;}\r\n' \
  '        if (dx == null) {\r\n' \
  '          if (focused.substring(0, 5) != "point") {return;}\r\n' \
  '          let segf = document.getElementById(focused + "cont").parentNode;\r\n' \
  '          if (! segf.firstElementChild.checked) {return;}\r\n' \
  '          let foc_ind = parseInt(focused.substring(5));\r\n' \
  '          if (foc_ind >= point_stat.length) {return;}\r\n' \
  '          if (point_stat[foc_ind] == null) {return;}\r\n' \
  '          let segf_ind = parseInt(segf.id.slice(7, -4));\r\n' \
  '          if (graph_px[foc_ind] != undefined) {\r\n' \
  '            gbar.style.left = (graph_px[foc_ind] + graphc.offsetLeft - 1).toString() + "px";\r\n' \
  '            if (gbarc.getAttribute("stroke") != "darkgray") {\r\n' \
  '              gbarc.style.left = (graph_px[foc_ind] + graphc.offsetLeft - 1).toString() + "px";\r\n' \
  '            }\r\n' \
  '            gbar.style.display = "";\r\n' \
  '            gbarc.style.display = "";\r\n' \
  '            let segs = document.getElementById("pointsform").children;\r\n' \
  '            if (document.getElementById("graphx").selectedIndex == 0) {\r\n' \
  '              let dur = Math.round(stats[segf_ind][point_stat[foc_ind]][0]);\r\n' \
  '              let dur_s = dur % 60;\r\n' \
  '              let dur_m = ((dur - dur_s) / 60) % 60;\r\n' \
  '              let dur_h = (dur - dur_m * 60 - dur_s) / 3600;\r\n' \
  '              let dur_s_c = dur_h.toString() + "h" + dur_m.toString().padStart(2, "0") + "mn" + dur_s.toString().padStart(2, "0") + "s";\r\n' \
  '              for (let s=0; s<segs.length; s++) {\r\n' \
  '                if (! segs[s].firstElementChild.checked) {continue;}\r\n' \
  '                let seg_ind = parseInt(segs[s].id.slice(7, -4));\r\n' \
  '                if (seg_ind == segf_ind) {break;}\r\n' \
  '                if (stats[seg_ind].length == 0) {continue;}\r\n' \
  '                dur += stats[seg_ind][stats[seg_ind].length - 1][0];\r\n' \
  '              }\r\n' \
  '              dur_s = dur % 60;\r\n' \
  '              dur_m = ((dur - dur_s) / 60) % 60;\r\n' \
  '              dur_h = (dur - dur_m * 60 - dur_s) / 3600;\r\n' \
  '              let dur_c = dur_h.toString() + "h" + dur_m.toString().padStart(2, "0") + "mn" + dur_s.toString().padStart(2, "0") + "s";\r\n' \
  '              graphpx.innerHTML = dur_c + "<br>" + dur_s_c;\r\n' \
  '            } else {\r\n' \
  '              let dist_s = stats[segf_ind][point_stat[foc_ind]][1];\r\n' \
  '              let dist = dist_s;\r\n' \
  '              for (let s=0; s<segs.length; s++) {\r\n' \
  '                if (! segs[s].firstElementChild.checked) {continue;}\r\n' \
  '                let seg_ind = parseInt(segs[s].id.slice(7, -4));\r\n' \
  '                if (seg_ind == segf_ind) {break;}\r\n' \
  '                if (stats[seg_ind].length == 0) {continue;}\r\n' \
  '                dist += stats[seg_ind][stats[seg_ind].length - 1][1];\r\n' \
  '              }\r\n' \
  '              graphpx.innerHTML = (dist / 1000).toFixed(2) + "km<br>" + (dist_s / 1000).toFixed(2) + "km";\r\n' \
  '            }\r\n' \
  '            let yi = document.getElementById("graphy").selectedIndex;\r\n' \
  '            switch (yi) {\r\n' \
  '              case 0:\r\n' \
  '                let dist_s = stats[segf_ind][point_stat[foc_ind]][1];\r\n' \
  '                let dist = dist_s;\r\n' \
  '                for (let s=0; s<segs.length; s++) {\r\n' \
  '                  if (! segs[s].firstElementChild.checked) {continue;}\r\n' \
  '                  let seg_ind = parseInt(segs[s].id.slice(7, -4));\r\n' \
  '                  if (seg_ind == segf_ind) {break;}\r\n' \
  '                  if (stats[seg_ind].length == 0) {continue;}\r\n' \
  '                  dist += stats[seg_ind][stats[seg_ind].length - 1][1];\r\n' \
  '                }\r\n' \
  '                graphpy.innerHTML = (dist / 1000).toFixed(2) + "km<br>" + (dist_s / 1000).toFixed(2) + "km";\r\n' \
  '                break;\r\n' \
  '              case 1:\r\n' \
  '                graphpy.innerHTML = document.getElementById(focused + "ele").value + "m";\r\n' \
  '                break\r\n' \
  '              case 2:\r\n' \
  '                graphpy.innerHTML = document.getElementById(focused + "alt").value + "m";\r\n' \
  '                break\r\n' \
  '              case 3:\r\n' \
  '              case 4:\r\n' \
  '                let g_s = stats[segf_ind][point_stat[foc_ind]][yi - 1];\r\n' \
  '                let g = g_s;\r\n' \
  '                for (let s=0; s<segs.length; s++) {\r\n' \
  '                  if (! segs[s].firstElementChild.checked) {continue;}\r\n' \
  '                  let seg_ind = parseInt(segs[s].id.slice(7, -4));\r\n' \
  '                  if (seg_ind == segf_ind) {break;}\r\n' \
  '                  if (stats[seg_ind].length == 0) {continue;}\r\n' \
  '                  g += stats[seg_ind][stats[seg_ind].length - 1][yi - 1];\r\n' \
  '                }\r\n' \
  '                graphpy.innerHTML = g.toFixed(1) + "m<br>" + g_s.toFixed(1) + "m";\r\n' \
  '                break;\r\n' \
  '                break;\r\n' \
  '              case 5:\r\n' \
  '                graphpy.innerHTML = (stats[segf_ind][point_stat[foc_ind]][4] * 100).toFixed(1) + "%";\r\n' \
  '                break\r\n' \
  '              case 6:\r\n' \
  '                graphpy.innerHTML = (stats[segf_ind][point_stat[foc_ind]][5] * 100).toFixed(1) + "%";\r\n' \
  '                break\r\n' \
  '              case 7:\r\n' \
  '                graphpy.innerHTML = (stats[segf_ind][point_stat[foc_ind]][6] * 3.6 ).toFixed(1) + "km/h";\r\n' \
  '                break\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          let x = Math.max(Math.min(parseFloat(gbarc.style.left) + 1 + dx, xr), xl);\r\n' \
  '          gbarc.style.left = (x - 1).toString() + "px";\r\n' \
  '          gbarc.style.display = "";\r\n' \
  '          let ind1 = 0;\r\n' \
  '          let ind2 = graph_ip.length - 1;\r\n' \
  '          x = x + 45 - xl;\r\n' \
  '          while (ind1 < ind2) {\r\n' \
  '            let inda = Math.floor((ind1 + ind2) / 2);\r\n' \
  '            let indb = inda + 1;\r\n' \
  '            while (graph_px[graph_ip[inda]] == graph_px[graph_ip[indb]] && indb < ind2) {indb++;}\r\n' \
  '            let da = Math.abs(graph_px[graph_ip[inda]] - x);\r\n' \
  '            let db = Math.abs(graph_px[graph_ip[indb]] - x);\r\n' \
  '            if (da <= db) {ind2 = inda;} else {ind1 = indb;}\r\n' \
  '          }\r\n' \
  '          if ("point" + graph_ip[ind1].toString() != focused) {\r\n' \
  '            let pt = document.getElementById("point" + graph_ip[ind1].toString() + "desc");\r\n' \
  '            element_click(null, pt);\r\n' \
  '            scroll_to_dot(document.getElementById("dot" + graph_ip[ind1].toString()));\r\n' \
  '          } else {\r\n' \
  '            gbar.style.display = "";\r\n' \
  '            graphpx.innerHTML = gpx;\r\n' \
  '            graphpy.innerHTML = gpy;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function error_pcb() {\r\n' \
  '      } \r\n' \
  '      function load_pcb(t, foc) {\r\n' \
  '        if (t.status != 200) {return false;}\r\n' \
  '        let ex_foc = focused;\r\n' \
  '        if (! t.response) {return false;}\r\n' \
  '        let iti = t.response.split("\\r\\n");\r\n' \
  '        if (iti.length <= 0) {return false;}\r\n' \
  '        if (focused == foc) {element_click(null, document.getElementById(foc + "desc"), false);}\r\n' \
  '        let batch = ++hist_b;\r\n' \
  '        let frag = document.createDocumentFragment();\r\n' \
  '        let frag_dot = document.createDocumentFragment();\r\n' \
  '        let pt = document.getElementById(foc).parentNode;\r\n' \
  '        let seg = pt.parentNode;\r\n' \
  '        let track = document.getElementById("track" + seg.id.slice(7, -4));\r\n' \
  '        let path = document.getElementById("path" + seg.id.slice(7, -4));\r\n' \
  '        let dot = document.getElementById(foc.replace("point", "dot"));\r\n' \
  '        let spans = seg.getElementsByTagName("span");\r\n' \
  '        let ind = 0;\r\n' \
  '        while (spans[ind].id != foc + "focus") {ind++;}\r\n' \
  '        ind++;\r\n' \
  '        let d = path.getAttribute("d");\r\n' \
  '        let d_left = d.match("( *[LMm] *\\\\d+([.]\\\\d*)? +\\\\d+([.]\\\\d*)? *){" + ind.toString() + "}")[0];\r\n' \
  '        let d_right = " " + d.slice(d_left.length).replace("M", "L");\r\n' \
  '        let l = document.getElementById("points").getElementsByTagName("span").length;\r\n' \
  '        for (let p=iti.length - 1; p>=0; p--) {\r\n' \
  '          let [lat, lon] = iti[p].split(",").map(Number);\r\n' \
  '          let el_cont = pt.cloneNode(true);\r\n' \
  '          let pref = "point" + (l + p).toString();\r\n' \
  '          el_cont.id = pref + "cont";\r\n' \
  '          let el_input = el_cont.firstElementChild;\r\n' \
  '          el_input.id = pref;\r\n' \
  '          el_input.name = pref;\r\n' \
  '          el_input.checked = true;\r\n' \
  '          el_input.value = "edited";\r\n' \
  '          let el_label = el_input.nextElementSibling;\r\n' \
  '          el_label.htmlFor = pref;\r\n' \
  '          el_label.id = pref + "desc";\r\n' \
  '          el_label.style.textDecoration = "inherit";\r\n' \
  '          let el_span = el_label.nextElementSibling.nextElementSibling;\r\n' \
  '          el_span.id = pref + "focus";\r\n' \
  '          el_span.style="";\r\n' \
  '          let el_span_children = el_span.children;\r\n' \
  '          el_span_children[0].htmlFor = pref + "lat";\r\n' \
  '          el_span_children[1].id = pref + "lat";\r\n' \
  '          el_span_children[1].name = pref + "lat";\r\n' \
  '          el_span_children[3].htmlFor = pref + "lon";\r\n' \
  '          el_span_children[4].id = pref + "lon";\r\n' \
  '          el_span_children[4].name = pref + "lon";\r\n' \
  '          el_span_children[6].htmlFor = pref + "ele";\r\n' \
  '          el_span_children[7].id = pref + "ele";\r\n' \
  '          el_span_children[7].name = pref + "ele";\r\n' \
  '          el_span_children[9].htmlFor = pref + "alt";\r\n' \
  '          el_span_children[10].id = pref + "alt";\r\n' \
  '          el_span_children[10].name = pref + "alt";\r\n' \
  '          el_span_children[12].htmlFor = pref + "time";\r\n' \
  '          el_span_children[13].id = pref + "time";\r\n' \
  '          el_span_children[13].name = pref + "time";\r\n' \
  '          el_span_children[1].value = lat.toFixed(6);\r\n' \
  '          el_span_children[4].value = lon.toFixed(6);\r\n' \
  '          el_span_children[7].value = "";\r\n' \
  '          el_span_children[10].value = "";\r\n' \
  '          el_span_children[13].value = "";\r\n' \
  '          el_label.innerHTML = point_desc(el_span);\r\n' \
  '          let wm = WGS84toWebMercator(lat, lon);\r\n' \
  '          if (wm[0] <= vminx || wm[0] >= vmaxx || wm[1] <= vminy || wm[1] >= vmaxy) {\r\n' \
  '            el_input.disabled = true;\r\n' \
  '            el_input.value = "error";\r\n' \
  '            el_label.style.textDecoration = "line-through red";\r\n' \
  '          }\r\n' \
  '          frag.insertBefore(el_cont, frag.firstElementChild);\r\n' \
  '          let el_dot = dot.cloneNode(true);\r\n' \
  '          el_dot.id = pref.replace("point", "dot");\r\n' \
  '          el_dot.style.stroke = "gray";\r\n' \
  '          el_dot.style.display = (dots_visible && ! el_input.disabled)?"":"none";\r\n' \
  '          el_dot.style.zIndex = "";\r\n' \
  '          el_dot.style.left = wmvalue_to_prop(Math.max(vminx, Math.min(vmaxx, wm[0])) - htopx, 3.5);\r\n' \
  '          el_dot.style.top = wmvalue_to_prop(htopy - Math.max(vminy, Math.min(vmaxy, wm[1])), 3.5);\r\n' \
  '          frag_dot.insertBefore(el_dot, frag_dot.firstElementChild);\r\n' \
  '          if (el_input.disabled) {\r\n' \
  '            d_right = " m0 0" + d_right;\r\n' \
  '          } else {\r\n' \
  '            let [x, y] = WGS84toWebMercator(parseFloat(el_span_children[1].value), parseFloat(el_span_children[4].value));\r\n' \
  '            let c = rebase_track(x, y, track, false, true);\r\n' \
  '            let np = (x - prop_to_wmvalue(track.style.left) - htopx).toFixed(1) + " " + (htopy - prop_to_wmvalue(track.style.top) - y).toFixed(1);\r\n' \
  '            if (c != null) {\r\n' \
  '              for (let i=0; i<2; i++) {\r\n' \
  '                let d_ = i==0?d_left.substring(4):d_right;\r\n' \
  '                let points = d_.match(/[LMm] *\\d+([.]\\d*)? +\\d+([.]\\d*)?/g);\r\n' \
  '                d_ = "";\r\n' \
  '                if (points != null) {\r\n' \
  '                  for (let point of points) {\r\n' \
  '                    let [px, py] = point.match(/\\d+([.]\\d*)?/g);\r\n' \
  '                    d_ = d_ + " " + point[0] + (parseFloat(px) + c[0]).toFixed(1) + " " + (parseFloat(py) + c[1]).toFixed(1);\r\n' \
  '                  }\r\n' \
  '                }\r\n' \
  '                if (i == 0) {d_left = "M0 0" + d_;} else {d_right = d_;}\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            d_right = " L" + np + d_right;\r\n' \
  '          }\r\n' \
  '          hist[0].push([pref, "", batch]);\r\n' \
  '        }\r\n' \
  '        seg.insertBefore(frag, pt);\r\n' \
  '        handle.insertBefore(frag_dot, dot);\r\n' \
  '        if (d_left.indexOf("M", 1) < 0) {d_right =  d_right.replace("L", "M");}\r\n' \
  '        d = d_left.trimEnd() + d_right;\r\n' \
  '        path.setAttribute("d", d);\r\n' \
  '        segments_calc(document.getElementById(foc).parentNode.parentNode);\r\n' \
  '        if (focused != ex_foc) {element_click(null, document.getElementById(ex_foc + "desc"), false);}\r\n' \
  '        document.getElementById(ex_foc).scrollIntoView({block:"center"});\r\n' \
  '        return true;\r\n'\
  '      } \r\n' \
  '      function build_path() {\r\n' \
  '        let foc = focused;\r\n' \
  '        if (focused.substring(0, 5) != "point") {return;}\r\n' \
  '        let pt_foc = document.getElementById(focused + "cont");\r\n' \
  '        if (pt_foc.firstElementChild.value == "error" || ! pt_foc.firstElementChild.checked) {return;}\r\n' \
  '        let lat_a = document.getElementById(focused + "lat").value;\r\n' \
  '        let lon_a = document.getElementById(focused + "lon").value;\r\n' \
  '        let lat_d = null;\r\n' \
  '        let lon_d = null;\r\n' \
  '        let pt = pt_foc;\r\n' \
  '        while (pt != null) {\r\n' \
  '          pt = pt.previousElementSibling;\r\n' \
  '          if (pt.id.indexOf("point") < 0) {\r\n' \
  '            pt = null;\r\n' \
  '          } else {\r\n' \
  '            let pt_id = pt.id.slice(0, -4);\r\n' \
  '            if (document.getElementById(pt_id).value != "error" && document.getElementById(pt_id).checked) {\r\n' \
  '              lat_d = document.getElementById(pt_id + "lat").value;\r\n' \
  '              lon_d = document.getElementById(pt_id + "lon").value;\r\n' \
  '              break;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (lat_d == null || lon_d == null) {return;}\r\n' \
  '        let b = lat_d + "," + lon_d + "\\r\\n" + lat_a + "," + lon_a;\r\n' \
  '        let xhrp = new XMLHttpRequest();\r\n' \
  '        let msgn = show_msg("{#jmpath1#}", 0);\r\n' \
  '        xhrp.onload = (e) => {load_pcb(e.target, foc)?show_msg("{#jmpath2#}", 2, msgn):show_msg("{#jmpath3#}", 10, msgn);};\r\n' \
  '        xhrp.onerror = (e) => {error_pcb(); show_msg("{#jmpath3#}", 10, msgn);};\r\n' \
  '        xhrp.open("POST", "/path");\r\n' \
  '        xhrp.setRequestHeader("Content-Type", "application/octet-stream");\r\n' \
  '        xhrp.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhrp.send(b);\r\n' \
  '      }\r\n' \
  '      function open_3D() {\r\n' \
  '        track_save(true);\r\n' \
  '      }\r\n' \
  '      function rescale(tscale_ex=tscale) {\r\n' \
  '        let zoom_ex = zoom;\r\n' \
  '        if (mode == "map") {\r\n' \
  '          zoom = eval(zoom_s) * Math.min((viewpane.offsetWidth - 2) * tscale / (vmaxx - vminx), (viewpane.offsetHeight - 4) * tscale / (vmaxy - vminy));\r\n' \
  '          document.getElementById("zoom").innerHTML = zoom_s;\r\n' \
  '        } else {\r\n' \
  '          zoom = eval(zoom_s);\r\n' \
  '          if (tlevel != 0) {document.getElementById("matrix").innerHTML = tlevels[tlevel][0].toString();}\r\n' \
  '          document.getElementById("zoom").innerHTML = zoom_s;\r\n' \
  '        }\r\n' \
  '        document.documentElement.style.setProperty("--scale", tscale / zoom);\r\n' \
  '        document.documentElement.style.setProperty("--zoom", zoom);\r\n' \
  '        document.documentElement.style.setProperty("--wsp", (6 * Math.max(zoom/tscale, 1)).toFixed(1) + "em");\r\n' \
  '        if (focused) {\r\n' \
  '          if (focused.indexOf("segment") >= 0) {\r\n' \
  '            scroll_to_track(document.getElementById(focused.replace("segment", "track")));\r\n' \
  '          } else {\r\n' \
  '            scroll_to_dot(document.getElementById(focused.replace("point", "dot")));\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          let r = zoom / zoom_ex * tscale_ex / tscale;\r\n' \
  '          hpx = viewpane.offsetWidth / 2 * (1 - r) + hpx * r;\r\n' \
  '          hpy = viewpane.offsetHeight / 2 * (1 - r) + hpy * r;\r\n' \
  '        }\r\n' \
  '        reframe();\r\n' \
  '      }\r\n' \
  '      function switch_tlock(resc=true) {\r\n' \
  '        if (mode == "map") {return;}\r\n' \
  '        let zoom_s_ex = zoom_s;\r\n' \
  '        if (tlock) {\r\n' \
  '          if (tlevel == 0) {return;}\r\n' \
  '          document.getElementById("tlock").innerHTML = "&#128275;";\r\n' \
  '          let nlevel = tlevel;\r\n' \
  '          if (eval(zoom_s) < eval(tlevels[tlevel][1])) {\r\n' \
  '            while (nlevel > 1) {\r\n' \
  '              if (tlevels[nlevel - 1][0] != tlevels[tlevel][0]) {break;}\r\n' \
  '              if (eval(zoom_s) <= eval(tlevels[nlevel - 1][1])) {nlevel--;} else {break;}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (eval(zoom_s) > eval(tlevels[tlevel][1])) {\r\n' \
  '            while (nlevel < tlevels.length - 1) {\r\n' \
  '              if (tlevels[nlevel + 1][0] != tlevels[tlevel][0]) {break;}\r\n' \
  '              if (eval(zoom_s) >= eval(tlevels[nlevel + 1][1])) {nlevel++;} else {break;}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          tlevel = nlevel;\r\n' \
  '          zoom_s = tlevels[nlevel][1];\r\n' \
  '        } else {\r\n' \
  '          document.getElementById("tlock").innerHTML = "&#128274;";\r\n' \
  '        }\r\n' \
  '        tlock = ! tlock;\r\n' \
  '        if (zoom_s == zoom_s_ex || ! resc) {return;}\r\n' \
  '        rescale();\r\n' \
  '      }\r\n' \
  '      function switch_sel(e, s) {\r\n' \
  '        if (e.altKey) {\r\n' \
  '          e.preventDefault();\r\n' \
  '          e.stopPropagation();\r\n' \
  '          if (s.id != "tset") {\r\n' \
  '            s.style.display = "none";\r\n' \
  '            document.getElementById("tset").style.display = "inline-block";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (e.shiftKey) {\r\n' \
  '          e.preventDefault();\r\n' \
  '          e.stopPropagation();\r\n' \
  '          if (s.id != "eset" && document.getElementById("eset").options.length > 0) {\r\n' \
  '            s.style.display = "none";\r\n' \
  '            document.getElementById("eset").style.display = "inline-block";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (e.ctrlKey) {\r\n' \
  '          e.preventDefault();\r\n' \
  '          e.stopPropagation();\r\n' \
  '          if (s.id != "iset" && document.getElementById("iset").options.length > 0) {\r\n' \
  '            s.style.display = "none";\r\n' \
  '            document.getElementById("iset").style.display = "inline-block";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function zoom_change(o) {\r\n' \
  '        let zoom_s_ex = zoom_s;\r\n' \
  '        if (mode == "map") {\r\n' \
  '          if (o < 0) {\r\n' \
  '            zoom_s = ([zooms[0]].concat(zooms))[zooms.indexOf(zoom_s)];\r\n' \
  '          } else {\r\n' \
  '            zoom_s = (zooms.concat(zooms[zooms.length - 1]))[zooms.indexOf(zoom_s) + 1];\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          if (tlock) {\r\n' \
  '            if (o < 0) {\r\n' \
  '              let ind = zooms.length;\r\n' \
  '              while (ind >= 0) {\r\n' \
  '                if (eval(zooms[ind]) < zoom) {break;}\r\n' \
  '                ind --;\r\n' \
  '              }\r\n' \
  '              if (ind >=0) {zoom_s = zooms[ind]} else {return;}\r\n' \
  '            } else {\r\n' \
  '              let ind = 0;\r\n' \
  '              while (ind < zooms.length) {\r\n' \
  '                if (eval(zooms[ind]) > zoom) {break;}\r\n' \
  '                ind ++;\r\n' \
  '              }\r\n' \
  '              if (ind < zooms.length) {zoom_s = zooms[ind]} else {return;}\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            let ntlevel = tlevel;\r\n' \
  '            if (o < 0) {\r\n' \
  '              if (tlevel <= 1) {return;}\r\n' \
  '              ntlevel = tlevel - 1;\r\n' \
  '            } else {\r\n' \
  '              if (tlevel >= tlevels.length - 1) {return;}\r\n' \
  '              ntlevel = tlevel + 1;\r\n' \
  '            }\r\n' \
  '            if (tlevels[ntlevel][0] != tlevels[tlevel][0]) {\r\n' \
  '              switch_tiles(null, ntlevel);\r\n' \
  '              return;\r\n' \
  '            }\r\n' \
  '            tlevel = ntlevel;\r\n' \
  '            zoom_s = tlevels[tlevel][1];\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (zoom_s == zoom_s_ex) {return;}\r\n' \
  '        rescale();\r\n' \
  '      }\r\n' \
  '      function zoom_dec() {\r\n' \
  '        zoom_change(-1);\r\n' \
  '      }\r\n' \
  '      function zoom_inc() {\r\n' \
  '        zoom_change(1);\r\n' \
  '      }\r\n' \
  '      function opacity_dec() {\r\n' \
  '        let filter = document.documentElement.style.getPropertyValue("--filter");\r\n' \
  '        let opacity = 1;\r\n' \
  '        if (filter && filter != "none") {\r\n' \
  '          opacity = parseFloat(filter.match(/slope=\\\\?"(0\\.[0-9])\\\\?"/)[1]);\r\n' \
  '        }\r\n' \
  '        if (opacity > 0.19) {\r\n' \
  '          filter = "url(\'data:image/svg+xml,<svg xmlns=\\"http://www.w3.org/2000/svg\\"><filter id=\\"attenuate\\"><feComponentTransfer><feFuncR type=\\"linear\\" slope=\\"%a\\" intercept=\\"%b\\"/><feFuncG type=\\"linear\\" slope=\\"%a\\" intercept=\\"%b\\"/><feFuncB type=\\"linear\\" slope=\\"%a\\" intercept=\\"%b\\"/></feComponentTransfer></filter></svg>#attenuate\')".replace(/%a/g, (opacity - 0.1).toFixed(1)).replace(/%b/g, (1.1 - opacity).toFixed(1));\r\n' \
  '          document.documentElement.style.setProperty("--filter", filter);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function opacity_inc() {\r\n' \
  '        let filter = document.documentElement.style.getPropertyValue("--filter");\r\n' \
  '        if (filter && filter != "none") {\r\n' \
  '          let opacity = parseFloat(filter.match(/slope=\\\\?"(0\\.[0-9])\\\\?"/)[1]);\r\n' \
  '          if (opacity < 0.81) {\r\n' \
  '            filter = "url(\'data:image/svg+xml,<svg xmlns=\\"http://www.w3.org/2000/svg\\"><filter id=\\"attenuate\\"><feComponentTransfer><feFuncR type=\\"linear\\" slope=\\"%a\\" intercept=\\"%b\\"/><feFuncG type=\\"linear\\" slope=\\"%a\\" intercept=\\"%b\\"/><feFuncB type=\\"linear\\" slope=\\"%a\\" intercept=\\"%b\\"/></feComponentTransfer></filter></svg>#attenuate\')".replace(/%a/g, (opacity + 0.1).toFixed(1)).replace(/%b/g, (0.9 - opacity).toFixed(1));\r\n' \
  '          } else {filter = "none";}\r\n' \
  '          document.documentElement.style.setProperty("--filter", filter);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function load_epcb(t) {\r\n' \
  '        if (t.status != 204) {\r\n' \
  '          document.getElementById("eset").selectedIndex = eset;\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        eset = document.getElementById("eset").selectedIndex;\r\n' \
  '      } \r\n' \
  '      function error_epcb() {\r\n' \
  '        document.getElementById("eset").selectedIndex = eset;\r\n' \
  '      } \r\n' \
  '      function switch_elevations(eset) {\r\n' \
  '        let q = "eset=" + encodeURIComponent(eset);\r\n' \
  '        xhrep.onload = (e) => {load_epcb(e.target)};\r\n' \
  '        xhrep.open("GET", "/elevationsproviders/switch?" + q);\r\n' \
  '        xhrep.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhrep.send();\r\n' \
  '      }\r\n' \
  '      function load_ipcb(t) {\r\n' \
  '        if (t.status != 204) {\r\n' \
  '          document.getElementById("iset").selectedIndex = iset;\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        iset = document.getElementById("iset").selectedIndex;\r\n' \
  '      } \r\n' \
  '      function error_ipcb() {\r\n' \
  '        document.getElementById("iset").selectedIndex = iset;\r\n' \
  '      } \r\n' \
  '      function switch_itineraries(iset) {\r\n' \
  '        let q = "iset=" + encodeURIComponent(iset);\r\n' \
  '        xhrip.onload = (e) => {load_ipcb(e.target)};\r\n' \
  '        xhrip.open("GET", "/itinerariesproviders/switch?" + q);\r\n' \
  '        xhrip.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhrip.send();\r\n' \
  '      }\r\n' \
  '      function switch_filterpanel(pa) {\r\n' \
  '        let fp = [null, document.getElementById("filterpanel1"), document.getElementById("filterpanel2"), document.getElementById("filterpanel3")];\r\n' \
  '        for (let p=1; p<=3; p++) {\r\n' \
  '          if (p == pa && (pa != 1 || gpucomp <= 1)) {\r\n' \
  '            if (fp[p].style.display == "none") {fp[p].style.display="";} else {fp[p].style.display = "none";}\r\n' \
  '          } else {\r\n' \
  '            fp[p].style.display = "none";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function load_cb(t) {\r\n' \
  '        document.getElementById("save_icon").style.fontSize = "inherit";\r\n' \
  '        document.getElementById("save").disabled = false;\r\n' \
  '        if (t.status != 204) {\r\n' \
  '          if (t.responseURL.indexOf("?") < 0) {window.alert("{#jserror#}" + t.status.toString() + " " + t.statusText);}\r\n' \
  '          return false;\r\n'\
  '        } else if (t.responseURL.indexOf("?") > 0) {\r\n' \
  '          window.open("http://" + location.hostname + ":" + location.port + "/3D/viewer.html");\r\n' \
  '        }\r\n' \
  '        return true;\r\n'\
  '      }\r\n' \
  '      function error_cb(t) {\r\n' \
  '        document.getElementById("save_icon").style.fontSize = "inherit";\r\n' \
  '        document.getElementById("save").disabled = false;\r\n' \
  '        if (t.responseURL.indexOf("?") < 0) {window.alert("{#jserror#}");}\r\n' \
  '      }\r\n' \
  '      function track_save(o3d=false) {\r\n' \
  '        if (document.getElementById("save").disabled) {return;}\r\n' \
  '        if (! o3d) {document.getElementById("save_icon").style.fontSize = "10%";}\r\n' \
  '        document.getElementById("save").disabled = true;\r\n' \
  '        let body = document.getElementById("name_track").value + "\\r\\n=\\r\\n";\r\n' \
  '        let spans = document.getElementById("waypoints").getElementsByTagName("span");\r\n' \
  '        for (let p=0; p<spans.length; p++) {\r\n' \
  '          let pt = spans[p].id.slice(0, -5);\r\n' \
  '          if (document.getElementById(pt).checked && document.getElementById(pt).value != "error") {\r\n' \
  '            body = body + pt.substring(8);\r\n' \
  '            if (document.getElementById(pt).value == "edited") {\r\n' \
  '              body = body + "&" + document.getElementById(pt + "lat").value + "&" + document.getElementById(pt + "lon").value + "&" + document.getElementById(pt + "ele").value + "&" + encodeURIComponent(document.getElementById(pt + "time").value) + "&" + encodeURIComponent(document.getElementById(pt + "name").value);\r\n' \
  '            }\r\n' \
  '            body = body + "\\r\\n";\r\n' \
  '           }\r\n' \
  '        }\r\n' \
  '        body = body + "=\\r\\n";\r\n' \
  '        let segments = document.getElementById("pointsform").children;\r\n' \
  '        for (let s=0; s<segments.length; s++) {\r\n' \
  '          if (! segments[s].firstElementChild.checked) {continue;}\r\n' \
  '          body = body + "-\\r\\n";\r\n' \
  '          spans = segments[s].getElementsByTagName("span");\r\n' \
  '          for (let p=0; p<spans.length; p++) {\r\n' \
  '            let pt = spans[p].id.slice(0, -5);\r\n' \
  '            if (document.getElementById(pt).checked && document.getElementById(pt).value != "error") {\r\n' \
  '              body = body + pt.substring(5);\r\n' \
  '              if (document.getElementById(pt).value == "edited") {\r\n' \
  '                body = body + "&" + document.getElementById(pt + "lat").value + "&" + document.getElementById(pt + "lon").value + "&" + document.getElementById(pt + "ele").value + "&" + document.getElementById(pt + "alt").value + "&" + encodeURIComponent(document.getElementById(pt + "time").value);\r\n' \
  '              }\r\n' \
  '              body = body + "\\r\\n";\r\n' \
  '             }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (o3d) {\r\n' \
  '          let msgn = show_msg("{#jm3dviewer1#}", 0);\r\n' \
  '           xhr.onload = (e) => {load_cb(e.target)?show_msg("{#jm3dviewer2#}", 2, msgn):show_msg("{#jm3dviewer3#}", 10, msgn);};\r\n' \
  '           xhr.onerror = (e) => {error_cb(e.target); show_msg("{#jm3dviewer3#}", 10, msgn);};\r\n' \
  '           xhr.open("POST", "/track?save=no");\r\n' \
  '        } else {\r\n' \
  '          let msgn = show_msg("{#jmsave1#}", 0);\r\n' \
  '          xhr.onload = (e) => {load_cb(e.target)?show_msg("{#jmsave2#}", 5, msgn):show_msg("{#jmsave3#}", 10, msgn);};\r\n' \
  '          xhr.onerror = (e) => {error_cb(e.target); show_msg("{#jmsave3#}", 10, msgn);};\r\n' \
  '          xhr.open("POST", "/track");\r\n' \
  '        }\r\n' \
  '        xhr.setRequestHeader("Content-Type", "application/octet-stream");\r\n' \
  '        xhr.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhr.send(body);\r\n' \
  '      }\r\n' \
  '      var xhr = new XMLHttpRequest();\r\n' \
  '      var xhrt = new XMLHttpRequest();\r\n' \
  '      xhrt.addEventListener("error", error_tcb);\r\n' \
  '      var xhrep = new XMLHttpRequest();\r\n' \
  '      xhrep.addEventListener("error", error_epcb);\r\n' \
  '      var xhrip = new XMLHttpRequest();\r\n' \
  '      xhrip.addEventListener("error", error_ipcb);\r\n' \
  '    </script>\r\n' \
  '  </head>\r\n' \
  '  <body style="background-color:rgb(40,45,50);color:rgb(225,225,225);margin-top:2px;margin-bottom:0;"> \r\n' \
  '    <table style="width:98vw;">\r\n' \
  '      <colgroup>\r\n' \
  '        <col style="width:21em;">\r\n' \
  '        <col style="width:calc(98vw - 21em);">\r\n' \
  '      </colgroup>\r\n' \
  '      <thead>\r\n' \
  '        <tr>\r\n' \
  '          <th colspan="2" style="text-align:left;font-size:120%;width:100%;border-bottom:1px darkgray solid;">\r\n' \
  '           <input type="text" id="name_track" name="name_track" value="##NAME##">\r\n' \
  '           <span style="display:inline-block;position:absolute;right:2vw;width:51em;overflow:hidden;text-align:right;font-size:80%;"><button title="{#jundo#}" onclick="undo(false, ! event.altKey)">&cularr;</button><button title="{#jredo#}" style="margin-left:0.25em;" onclick="undo(true, ! event.altKey)">&curarr;</button><button title="{#jinsertb#}" style="margin-left:0.75em;" onclick="point_insert(\'b\')">&boxdR;</button><button title="{#jinserta#}" style="margin-left:0.25em;" onclick="point_insert(\'a\')">&boxuR;</button><button title="{#jpath#}" style="margin-left:0.25em;" onclick="build_path()">&rarrc;</button><button title="{#jelementup#}" style="margin-left:0.75em;" onclick="element_up()">&UpTeeArrow;</button><button title="{#jelementdown#}" style="margin-left:0.25em;" onclick="element_down()">&DownTeeArrow;</button><button title="{#jsegmentcut#}" style="margin-left:0.25em;" onclick="segment_cut()">&latail;</button><button title="{#jsegmentabsorb#}" style="margin-left:0.25em;"onclick="segment_absorb()">&ratail;</button><button title="{#jsegmentreverse#}" style="margin-left:0.25em;"onclick="segment_reverse()">&rlarr;</button><button title="{#jelevationsadd#}" style="margin-left:0.75em;" onclick="ele_adds(false, event.altKey)">&plusacir;</button><button title="{#jelevationsreplace#}" style="margin-left:0.25em;" onclick="event.shiftKey?ele_alt_switch():ele_adds(true, event.altKey)"><span style="vertical-align:0.2em;line-height:0.8em;">&wedgeq;</span></button><button title="{#jaltitudesjoin#}" style="margin-left:0.25em;" onclick="alt_join()">&apacir;</button><button title="{#jdatetime#}" style="margin-left:0.25em;" onclick="datetime_interpolate()">&#9201;</button><button title="{#jsave#}" id="save" style="margin-left:1.25em;" onclick="track_save()"><span id="save_icon" style="line-height:1em;font-size:inherit">&#128190;</span></button><button title="{#jswitchpoints#}" style="margin-left:1.25em;" onclick="switch_dots()">&EmptySmallSquare;</button><button title="{#jgraph#}" style="margin-left:0.25em;" onclick="(event.shiftKey||event.ctrlKey||event.altKey)?switch_filterpanel(event.shiftKey?1:(event.ctrlKey?2:3)):refresh_graph(true)">&angrt;</button><button title="{#j3dviewer#}" style="margin-left:0.25em;" onclick="open_3D()">3D</button><select id="tset" name="tset" title="{#jtset#}" autocomplete="off" style="width:10em;height:1.7em;margin-left:0.75em;" onmousedown="switch_sel(event, this)" onchange="switch_tiles(this.selectedIndex, -1)">##TSETS##</select><select id="eset" name="eset" title="{#jeset#}" autocomplete="off" style="display:none;width:10em;height:1.7em;margin-left:0.75em;" onmousedown="switch_sel(event, this)" onchange="switch_elevations(this.selectedIndex)">##ESETS##</select><select id="iset" name="iset" title="{#jiset#}" autocomplete="off" style="display:none;width:10em;height:1.7em;margin-left:0.75em;" onmousedown="switch_sel(event, this)" onchange="switch_itineraries(this.selectedIndex)">##ISETS##</select><button title="{#jminus#}" style="margin-left:0.25em;" onclick="event.ctrlKey?opacity_dec():zoom_dec()">-</button><span id="matrix" style="display:none;width:1.5em;">--</span><span id="tlock" title="{#jlock#}" style="display:none;width:1em;cursor:pointer" onclick="switch_tlock()">&#128275;</span><span id="zoom" style="display:inline-block;width:2em;text-align:center;">1</span><button title="{#jplus#}" style="" onclick="event.ctrlKey?opacity_inc():zoom_inc()">+</button></span>\r\n' \
  '            <div id="filterpanel1" style="display:none;position:absolute;top:calc(1.6em + 10px);right:2vw;width:10em;height:13.4em;background-color:rgb(30,30,35);z-index:10;font-size:75%;text-align:center;font-weight:normal;">\r\n' \
  '              <span>{#jfilterpanel1#}</span>\r\n' \
  '              <form id="filterform1" autocomplete="off" onchange="segments_calc(1)">\r\n' \
  '                <label for="egfilter" style="left:2px;">{#jgraphelevation#}</label>\r\n' \
  '                <label for="agfilter" style="right:2px;">{#jgraphaltitude#}</label>\r\n' \
  '                <span id="egstren" style="left:0.7em;">##EGTHRESHOLD##</span>\r\n' \
  '                <input type="range" id="egfilter" name="egfilter" min="0" max="25" step="1" value="##EGTHRESHOLD##" style="right:8.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '                <span id="agstren" style="right:0.7em;">##AGTHRESHOLD##</span>\r\n' \
  '                <input type="range" id="agfilter" name="agfilter" min="0" max="25" step="1" value="##AGTHRESHOLD##" style="right:1.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n' \
  '            <div id="filterpanel2" style="display:none;position:absolute;top:calc(1.6em + 10px);right:2vw;width:10em;height:13.4em;background-color:rgb(30,30,35);z-index:10;font-size:75%;text-align:center;font-weight:normal;">\r\n' \
  '              <span>{#jfilterpanel2#}</span>\r\n' \
  '              <form id="filterform2" autocomplete="off" onchange="segments_calc(2)">\r\n' \
  '                <label for="sldfilter" style="left:2px;">{#jgraphdistance#}</label>\r\n' \
  '                <label for="slmfilter" style="right:2px;">{#jsmax#}</label>\r\n' \
  '                <span id="sldist" style="left:0.7em;">##SLRANGE##</span>\r\n' \
  '                <input type="range" id="sldfilter" name="sldfilter" min="0" max="500" step="2" value="##SLRANGE##" style="right:8.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '                <span id="slmax" style="right:0.7em;">##SLMAX##</span>\r\n' \
  '                <input type="range" id="slmfilter" name="slmfilter" min="0" max="100" step="1" value="##SLMAX##" style="right:1.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n' \
  '            <div id="filterpanel3" style="display:none;position:absolute;top:calc(1.6em + 10px);right:2vw;width:10em;height:13.4em;background-color:rgb(30,30,35);z-index:10;font-size:75%;text-align:center;font-weight:normal;">\r\n' \
  '              <span>{#jfilterpanel3#}</span>\r\n' \
  '              <form id="filterform3" autocomplete="off" onchange="segments_calc(3)">\r\n' \
  '                <label for="sptfilter" style="left:2px;">{#jspduration#}</label>\r\n' \
  '                <label for="spmfilter" style="right:2px;">{#jsmax#}</label>\r\n' \
  '                <span id="sptime" style="left:0.7em;">##SPRANGE##</span>\r\n' \
  '                <input type="range" id="sptfilter" name="sptfilter" min="0" max="300" step="2" value="##SPRANGE##" style="right:8.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '                <span id="spmax" style="right:0.7em;">##SPMAX##</span>\r\n' \
  '                <input type="range" id="spmfilter" name="spmfilter" min="0" max="90" step="1" value="##SPMAX##" style="right:1.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n' \
  '          </th>\r\n' \
  '        </tr>\r\n' \
  '      </thead>\r\n' \
  '      <tbody>\r\n' \
  '        <tr style="display:table-row;">\r\n' \
  '          <td style="display:table-cell;vertical-align:top;">\r\n' \
  '            <div id="content" style="height:calc(99vh - 2.4em - 16px);width: calc(21em - 2px);">\r\n' \
  '              <div id="pattern_waypoint" style="display:none;">\r\n '\
  '                ##WAYPOINTTEMPLATE##\r\n' \
  '              </div>\r\n' \
  '              <div id="pattern_point" style="display:none;">\r\n '\
  '                ##POINTTEMPLATE##\r\n' \
  '              </div>\r\n' \
  '              <div id="pattern_waydot" style="display:none;">\r\n '\
  '                ##WAYDOTTEMPLATE##\r\n' \
  '              </div>\r\n' \
  '              <div id="pattern_dot" style="display:none;">\r\n '\
  '                ##DOTTEMPLATE##\r\n' \
  '              </div>\r\n' \
  '              <div id="waypoints" style="overflow-y:scroll;overflow-x:hidden;height:12%;font-size:80%;border-bottom:1px darkgray solid;">\r\n' \
  '                {#jwaypoints#}&nbsp;<svg width="8" height="8" stroke="green" stroke-width="1.5" fill="none"><circle cx="4" cy="4" r="3"/></svg><br>\r\n' \
  '                <form id="waypointsform" autocomplete="off">\r\n                  ##WAYPOINTS##\r\n' \
  '                </form>\r\n' \
  '              </div>\r\n' \
  '              <div id="points" style="overflow-y:scroll;overflow-x:hidden;height:88%;font-size:80%">\r\n' \
  '                {#jpoints#}&nbsp;<svg width="7" height="7" stroke="green" stroke-width="1.5" fill="none"><rect x="1" y="1" width="5" height="5"/></svg><br>\r\n' \
  '                <form id="pointsform" autocomplete="off">\r\n                  ##POINTS##\r\n' \
  '                </form>\r\n' \
  '              </div>\r\n' \
  '            </div>\r\n' \
  '          </td>\r\n' \
  '          <td style="display:table-cell;vertical-align:top;position:relative;">\r\n' \
  '            <div id="view" style="overflow:hidden;position:absolute;width:100%;height:calc(99vh - 2.4em - 16px);" onmousedown="mouse_down(event, this)" onwheel="mouse_wheel(event)">\r\n' \
  '              <div id="handle" style="position:relative;top:0px;left:0px;width:100px;height:100px;">##PATHES##\r\n##WAYDOTS####DOTS##' \
  '              </div>\r\n' \
  '              <div id="scalebox" style="position:absolute;left:4px;bottom:3px;background-color:rgba(255, 255, 255, .5);padding-left:2px;padding-right:2px;line-height:0.7em;"> \r\n' \
  '                <svg id="scaleline" stroke="black" stroke-width="1.5" width="100px" height="0.3em">\r\n' \
  '                  <line x1="0" y1="0" x2="100%" y2="0"/>\r\n' \
  '                  <line x1="0" y1="0" x2="0" y2="100%"/>\r\n' \
  '                  <line x1="100%" y1="0" x2="100%" y2="100%"/>\r\n' \
  '                </svg>\r\n' \
  '                <span id="scalevalue" style="font-size:70%;color:black;">0 m</span>\r\n' \
  '              </div>\r\n' \
  '            </div>\r\n' \
  '          </td>\r\n' \
  '        </tr>\r\n' \
  '      </tbody>\r\n' \
  '      <tfoot>\r\n' \
  '        <tr>\r\n' \
  '          <th colspan=2 style="text-align:left;font-size:80%;width:100%;border-top:1px darkgray solid;font-weight:normal;padding-bottom:0px;">\r\n' \
  '            <div style="height:1.2em;overflow-y:hidden;width:100%;">\r\n' \
  '              <div id="message" style="overflow-y:auto;width:calc(98vw - 6px - 1.4em);height:1.2em;display:inline-block;" ></div><div title="{#jhelp#}" style="overflow-y:auto;width:1.4em;height:1.2em;display:inline-block;text-align:center;background-color:lightgray;color:black;font-weight:bold;cursor:help;">?</div>\r\n' \
  '            </div>\r\n' \
  '          </th>\r\n' \
  '        </tr>\r\n' \
  '      </tfoot>\r\n' \
  '    </table>\r\n' \
  '    <div id="graph" style="height:25vh;display:none;position:relative;width:100%;border-top:1px darkgray solid;font-size:80%;">\r\n' \
  '      <select id="graphy" name="graphy" title="y" autocomplete="off" style="height:1.7em;width:7em;position:absolute;left:0;top:0;" onchange="refresh_graph()"><option value="distance">{#jgraphdistance#}</option><option value="elevation">{#jgraphelevation#}</option><option value="altitude">{#jgraphaltitude#}</option><option value="elegain">{#jgraphelegain#}</option><option value="altgain">{#jgraphaltgain#}</option><option value="eleslope">{#jgrapheleslope#}</option><option value="altslope">{#jgraphaltslope#}</option><option value="speed">{#jgraphspeed#}</option></select>\r\n' \
  '      <select id="graphx" name="graphx" title="x" autocomplete="off" style="height:1.7em;width:7em;position:absolute;left:0;bottom:0;" onchange="refresh_graph()"><option value="time">{#jgraphtime#}</option><option value="distance">{#jgraphdistance#}</option></select>\r\n' \
  '      <div id="graphp" style="width:6em;color:dodgerblue;position:absolute;left:2px;top:2em;bottom:2em;overflow:auto;text-align:right;">\r\n' \
  '        <span id="graphpx" style="bottom:0;position:absolute;right:0;"></span>\r\n' \
  '        <span id="graphpy" style="top:0;position:absolute;right:0;"></span>\r\n' \
  '      </div>\r\n' \
  '      <canvas id="graphc" width="100" height="25" style="position:absolute;left:8em;top:0;" onmousedown="mouse_down(event, this)">\r\n' \
  '      </canvas>\r\n' \
  '      <svg id="gbarc" preserveAspectRatio="none" width="3" height="1" viewbox="0 0 3 100" stroke="none" stroke-width="1" fill="none" style="position:absolute;left:20px;top:1px;cursor:ew-resize" onmousedown="mouse_down(event, this)" onmouseup="mouse_up(event, this)">\r\n' \
  '        <line vector-effect="non-scaling-stroke" x1="1" y1="0" x2="1" y2="100"/>\r\n' \
  '      </svg> \r\n' \
  '      <svg id="gbar" preserveAspectRatio="none" width="3" height="1" viewbox="0 0 3 100" stroke="dodgerblue" stroke-width="1" fill="none" style="position:absolute;left:20px;top:1px;" pointer-events="none">\r\n' \
  '        <line vector-effect="non-scaling-stroke" x1="1" y1="0" x2="1" y2="100"/>\r\n' \
  '      </svg>\r\n' \
  '    </div>\r\n' \
  '    <script>\r\n' \
  '      var mousex = null;\r\n' \
  '      var mousey = null;\r\n' \
  '      var viewpane = document.getElementById("view");\r\n' \
  '      var handle = document.getElementById("handle");\r\n' \
  '      var hand = null;\r\n' \
  '      var hand_m = false;\r\n' \
  '      function mouse_down(e, elt) {\r\n' \
  '        if (e.button != 0 && e.button != 2) {return;}\r\n' \
  '        mousex = e.pageX;\r\n' \
  '        mousey = e.pageY;\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '        document.onmousemove = mouse_move;\r\n' \
  '        document.onmouseup = mouse_up;\r\n' \
  '        document.onclick = mouse_click;\r\n' \
  '        document.oncontextmenu = mouse_click;\r\n' \
  '        if (e.button == 0) {\r\n' \
  '          if (elt.id == "view") {\r\n' \
  '            hand = elt;\r\n' \
  '            viewpane.style.cursor = "all-scroll";\r\n' \
  '          } else if (elt.id.indexOf("dot") >= 0) {\r\n' \
  '            hand = elt;\r\n' \
  '            hand_m = false;\r\n' \
  '            let pt = document.getElementById(elt.id.replace("dot", "point") + "desc");\r\n' \
  '            if (pt.htmlFor != focused) {element_click(null, pt);}\r\n' \
  '            viewpane.style.cursor = "crosshair";\r\n' \
  '            hand.style.cursor = "crosshair";\r\n' \
  '          } else if (elt.id == "gbarc") {\r\n' \
  '            hand = elt;\r\n' \
  '            graph_point(0);\r\n' \
  '            hand.setAttribute("stroke", "darkgray");\r\n' \
  '          } else if (elt.id == "graphc") {\r\n' \
  '            hand = document.getElementById("gbarc");\r\n' \
  '            hand.setAttribute("stroke", "darkgray");\r\n' \
  '            graph_point(document.getElementById("graphc").offsetLeft + e.offsetX - parseFloat(hand.style.left));\r\n' \
  '          }\r\n' \
  '        } else if (e.button == 2) {\r\n' \
  '          if (elt.id == "view") {\r\n' \
  '            let p = viewpane.parentNode;\r\n' \
  '            let x = e.pageX - p.offsetLeft;\r\n' \
  '            let y = e.pageY - p.offsetTop;\r\n' \
  '            let wm = [(x - hpx) * tscale / zoom + htopx, htopy - (y - hpy) * tscale / zoom];\r\n' \
  '            if (wm[0] <= vminx || wm[0] >= vmaxx || wm[1] <= vminy || wm[1] >= vmaxy) {return;}\r\n' \
  '            let coord = WebMercatortoWGS84(...wm);\r\n' \
  '            point_insert("a", coord);\r\n' \
  '            point_edit(false, false, false, false);\r\n' \
  '            save_old();\r\n' \
  '            hand = document.getElementById(focused.replace("point", "dot"));\r\n' \
  '            hand_m = false;\r\n' \
  '            viewpane.style.cursor = "crosshair";\r\n' \
  '            hand.style.cursor = "crosshair";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_up(e, elt) {\r\n' \
  '        mousex = null;\r\n' \
  '        mousey = null;\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '        document.onmousemove = null;\r\n' \
  '        document.onmouseup = null;\r\n' \
  '        viewpane.style.cursor = "";\r\n' \
  '        if (hand) {\r\n' \
  '          if (hand.id.indexOf("dot") >= 0) {\r\n' \
  '            hand.style.cursor = "";\r\n' \
  '            let d = 0;\r\n' \
  '            if (hand_m || (e.shiftKey && ! e.altKey)) {\r\n' \
  '              hist[0].push([focused, foc_old]);\r\n' \
  '              let c = foc_old.split("\\r\\n");\r\n' \
  '              let d = distance(parseFloat(c[0]), parseFloat(c[1]), 0, parseFloat(document.getElementById(focused + "lat").value), parseFloat(document.getElementById(focused + "lon").value), 0);\r\n' \
  '              save_old();\r\n' \
  '              for (let i=hist[1].length - 1; i>=0 ;i--) {\r\n' \
  '                if (hist[1][i][0] == focused) {hist[1].splice(i, 1);}\r\n' \
  '              }\r\n' \
  '              if ((e.shiftKey || d > 25) && ! e.altKey) {\r\n' \
  '                document.getElementById(focused + "ele").value = "";\r\n' \
  '                if (focused.indexOf("way") < 0) {document.getElementById(focused + "alt").value = "";}\r\n' \
  '                point_edit(false, false, false, false);\r\n' \
  '                save_old();\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            if (hand.id.indexOf("way") < 0) {\r\n' \
  '              segments_calc(document.getElementById(focused).parentNode.parentNode);\r\n' \
  '              if (e.ctrlKey) {build_path();}\r\n' \
  '            } else {\r\n' \
  '              wpt_calc();\r\n' \
  '            }\r\n' \
  '          } else if (hand.id == "gbarc") {\r\n' \
  '            hand.setAttribute("stroke", "none");\r\n' \
  '            graph_point();\r\n' \
  '          }\r\n' \
  '          hand = null;\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (elt && e.button == 2) {\r\n' \
  '          if (elt.id.indexOf("dot") >= 0) {\r\n' \
  '            let cb = document.getElementById(elt.id.replace("dot", "point"));\r\n' \
  '            cb.checked = ! cb.checked;\r\n' \
  '            point_checkbox(cb);\r\n' \
  '            cb.scrollIntoView({block:"nearest"});\r\n' \
  '          } else if (elt.id.substring(0, 4) == "path") {\r\n' \
  '            let cb = document.getElementById(elt.id.replace("path", "segment"));\r\n' \
  '            cb.checked = ! cb.checked;\r\n' \
  '            segment_checkbox(cb);\r\n' \
  '            cb.scrollIntoView({block:"nearest"});\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_click(e, elt) {\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '        document.onclick = null;\r\n' \
  '        document.oncontextmenu = null;\r\n' \
  '        if (elt) {\r\n' \
  '          if (elt.id.substring(0, 4) == "path") {\r\n' \
  '            let seg = document.getElementById(elt.id.replace("path", "segment") + "desc");\r\n' \
  '            element_click(null, seg);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_move(e) {\r\n' \
  '        if (mousex != null && mousey != null && hand != null) {\r\n' \
  '          let dx = e.pageX - mousex;\r\n' \
  '          let dy = e.pageY - mousey;\r\n' \
  '          mousex = e.pageX;\r\n' \
  '          mousey = e.pageY;\r\n' \
  '          let p = viewpane.parentNode;\r\n' \
  '          if (hand.id == "gbarc") {\r\n' \
  '            graph_point(dx);\r\n' \
  '          } else if (e.pageX >= p.offsetLeft && e.pageX <= p.offsetLeft + p.offsetWidth && e.pageY >= p.offsetTop && e.pageY <= p.offsetTop + p.offsetHeight) {\r\n' \
  '            if (hand.id == "view") {\r\n' \
  '              scroll_dview(dx, dy);\r\n' \
  '            } else if (hand.id.indexOf("dot") >= 0) {\r\n' \
  '              hand_m = true;\r\n' \
  '              dpixels_to_point(dx, dy);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_wheel(e) {\r\n' \
  '        e.preventDefault();\r\n' \
  '        if (e.ctrlKey) {\r\n' \
  '          if (e.deltaY < 0) {zoom_inc();} else {zoom_dec();}\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (! e.altKey) {\r\n' \
  '          if (e.shiftKey) {scroll_dview(-e.deltaY, 0);} else {scroll_dview(0, -e.deltaY);}\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (! focused) {return;}\r\n' \
  '        if (focused.indexOf("point") >= 0) {\r\n' \
  '          let dt = document.getElementById(focused.replace("point", "dot"));\r\n' \
  '          let pt = null;\r\n' \
  '          do {\r\n' \
  '            if (e.deltaY > 0) {\r\n' \
  '              dt = dt.nextElementSibling;\r\n' \
  '            } else {\r\n' \
  '              dt = dt.previousElementSibling;\r\n' \
  '            }\r\n' \
  '            if (! dt) {return;}\r\n' \
  '            if (focused.indexOf("way") != dt.id.indexOf("way")) {return;}\r\n' \
  '            pt = document.getElementById(dt.id.replace("dot", "point"));\r\n' \
  '          } while (pt.value == "error" || ! pt.checked || (focused.indexOf("way")>=0?false:!pt.parentNode.parentNode.firstElementChild.checked))\r\n' \
  '          pt = document.getElementById(dt.id.replace("dot", "point") + "desc");\r\n' \
  '          element_click(null, pt);\r\n' \
  '          scroll_to_dot(dt);\r\n' \
  '        }\r\n' \
  '        if (focused.indexOf("segment") >= 0) {\r\n' \
  '          let seg = document.getElementById(focused + "cont")\r\n' \
  '          do {\r\n' \
  '            if (e.deltaY > 0) {\r\n' \
  '              seg = seg.nextElementSibling;\r\n' \
  '            } else {\r\n' \
  '              seg = seg.previousElementSibling;\r\n' \
  '            }\r\n' \
  '            if (! seg) {return;}\r\n' \
  '          } while (! seg.firstElementChild.checked)\r\n' \
  '          seg = seg.firstElementChild.nextElementSibling;\r\n' \
  '          element_click(null, seg);\r\n' \
  '          scroll_to_track(document.getElementById(seg.id.slice(0, -4).replace("segment", "track")));\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function page_unload() {\r\n' \
  '        let filter = document.documentElement.style.getPropertyValue("--filter");\r\n' \
  '        if (! filter) {filter = "none";}\r\n' \
  '        sessionStorage.setItem("state", (mode == "map" ? "||" : (tset.toString() + "|" + tlevel.toString() + "|" + tlock.toString())) + "|" + zoom_s + "|" + dots_visible.toString() + "|" + filter + "|" + eset.toString() + "|" + iset.toString() + "|" + document.getElementById("egstren").innerHTML + "|" + document.getElementById("agstren").innerHTML + "|" + document.getElementById("sldist").innerHTML + "|" + document.getElementById("slmax").innerHTML + "|" + document.getElementById("sptime").innerHTML + "|" + document.getElementById("spmax").innerHTML + "|" + document.getElementById("graphx").selectedIndex.toString() + "|" + document.getElementById("graphy").selectedIndex.toString());\r\n' \
  '        return "{#junload#}";\r\n' \
  '      }\r\n' \
  '      function page_load() {\r\n' \
  '        if (navigator.userAgent.toLowerCase().indexOf("firefox") > 0) {\r\n' \
  '          if (! document.getElementById("waypoint0cont")) {\r\n' \
  '            document.getElementById("waypoints").style.overflowY = "auto";\r\n' \
  '            document.getElementById("waypoints").style.borderRight = "solid rgb(34,37,42) 17px";\r\n' \
  '          }\r\n' \
  '          document.getElementById("tset").focus();\r\n' \
  '          document.getElementById("tset").blur();\r\n' \
  '        }\r\n' \
  '        let prev_state = sessionStorage.getItem("state");\r\n' \
  '        if (prev_state != null) {prev_state = prev_state.split("|");}\r\n' \
  '        if (prev_state != null) {zoom_s = prev_state[3];}\r\n' \
  '        if (mode == "map") {\r\n' \
  '          add_tile();\r\n' \
  '          rescale();\r\n' \
  '        } else {\r\n' \
  '          if (prev_state == null) {\r\n' \
  '            switch_tiles(0, 0);\r\n' \
  '          } else {\r\n' \
  '            document.getElementById("tset").selectedIndex = parseInt(prev_state[0]);\r\n' \
  '            switch_tiles(parseInt(prev_state[0]), parseInt(prev_state[1]));\r\n' \
  '            if (prev_state[2] == "true") {switch_tlock(false);}\r\n' \
  '          }\r\n' \
  '          document.getElementById("matrix").style.display = "inline-block";\r\n' \
  '          document.getElementById("tlock").style.display = "inline-block";\r\n' \
  '          if (tlevel == 0) {rescale();}\r\n' \
  '        }\r\n' \
  '        scroll_to_all();\r\n' \
  '        if (prev_state != null) {\r\n' \
  '          if (prev_state[4] == "true") {switch_dots();}\r\n' \
  '          document.documentElement.style.setProperty("--filter", prev_state[5]);\r\n' \
  '          if (prev_state[6] != "0") {\r\n' \
  '            eset = parseInt(prev_state[6]);\r\n' \
  '          }\r\n' \
  '          if (prev_state[7] != "0") {\r\n' \
  '            iset = parseInt(prev_state[7]);\r\n' \
  '          }\r\n' \
  '          document.getElementById("egstren").innerHTML = prev_state[8];\r\n' \
  '          document.getElementById("egfilter").value = parseFloat(prev_state[8]);\r\n' \
  '          document.getElementById("agstren").innerHTML = prev_state[9];\r\n' \
  '          document.getElementById("agfilter").value = parseFloat(prev_state[9]);\r\n' \
  '          document.getElementById("sldist").innerHTML = prev_state[10];\r\n' \
  '          document.getElementById("sldfilter").value = parseFloat(prev_state[10]);\r\n' \
  '          document.getElementById("slmax").innerHTML = prev_state[11];\r\n' \
  '          document.getElementById("slmfilter").value = parseFloat(prev_state[11]);\r\n' \
  '          document.getElementById("sptime").innerHTML = prev_state[12];\r\n' \
  '          document.getElementById("sptfilter").value = parseFloat(prev_state[12]);\r\n' \
  '          document.getElementById("spmax").innerHTML = prev_state[13];\r\n' \
  '          document.getElementById("spmfilter").value = parseFloat(prev_state[13]);\r\n' \
  '          document.getElementById("graphx").selectedIndex = parseInt(prev_state[14]);\r\n' \
  '          document.getElementById("graphy").selectedIndex = parseInt(prev_state[15]);\r\n' \
  '        }\r\n' \
  '        point_desc();\r\n' \
  '        window.onresize = (e) => {document.getElementById("points").style.height = "calc(100% - " + document.getElementById("waypoints").offsetHeight.toString() + "px)";rescale();refresh_graph()};\r\n' \
  '        document.getElementById("waypoints").style.maxHeight = "10vh";\r\n' \
  '        document.getElementById("waypoints").style.height = "";\r\n' \
  '        document.getElementById("points").style.height = "calc(100% - " + document.getElementById("waypoints").offsetHeight.toString() + "px)";\r\n' \
  '        document.getElementById("filterpanel1").style.right = "calc(2vw + " + (mode=="tiles"?"13.3":"10.6") + "em - 30px)";\r\n' \
  '        document.getElementById("filterpanel2").style.right = "calc(2vw + " + (mode=="tiles"?"13.3":"10.6") + "em - 30px)";\r\n' \
  '        document.getElementById("filterpanel3").style.right = "calc(2vw + " + (mode=="tiles"?"13.3":"10.6") + "em - 30px)";\r\n' \
  '        segments_calc();\r\n' \
  '        wpt_calc();\r\n' \
  '        window.onbeforeunload = page_unload;\r\n' \
  '//        window.onunload = function () {window.history.replaceState({}, "", "/GPXExplorer.html")};\r\n' \
  '      }\r\n' \
  '      ##SESSIONSTORE##if (sessionStorage.getItem("active") != "##SESSIONSTOREVALUE##") {\r\n' \
  '        window.alert("{#jsession#}");\r\n' \
  '        document.body.innerHTML = "";\r\n' \
  '        document.head.innerHTML = "";\r\n' \
  '        window.close();\r\n' \
  '        throw "{#jsession#}";\r\n' \
  '      }\r\n' \
  '//        document.addEventListener("DOMContentLoaded", function () {window.history.replaceState({}, "", "/GPXTweaker.html");});\r\n' \
  '      page_load();\r\n' \
  '    </script>\r\n' \
  '  </body>\r\n' \
  '</html>'
  HTML_TEMPLATE = HTML_TEMPLATE.replace('{', '{{').replace('}', '}}').replace('{{#', '{').replace('#}}', '}').format_map(LSTRINGS['interface']).replace('{{', '{').replace('}}', '}')
  HTML_DECLARATIONS_TEMPLATE = \
  '      var portmin = ##PORTMIN##;\r\n' \
  '      var portmax = ##PORTMAX##;\r\n' \
  '      var gpucomp = ##GPUCOMP##;\r\n' \
  '      var sessionid = "##SESSIONID##";\r\n' \
  '      var mode = "##MODE##";\r\n' \
  '      var vminx = ##VMINX##;\r\n' \
  '      var vminy = ##VMINY##;\r\n' \
  '      var vmaxx = ##VMAXX##;\r\n' \
  '      var vmaxy = ##VMAXY##;\r\n' \
  '      var defx = ##DEFX##;\r\n' \
  '      var defy = ##DEFY##;\r\n' \
  '      var ttopx = ##TTOPX##;\r\n' \
  '      var ttopy = ##TTOPY##;\r\n' \
  '      var twidth = ##TWIDTH##;\r\n' \
  '      var theight = ##THEIGHT##;\r\n' \
  '      var text = "##TEXT##";\r\n' \
  '      var tscale = ##TSCALE##;\r\n' \
  '      var htopx = ##HTOPX##;\r\n' \
  '      var htopy = ##HTOPY##;'
  HTML_WAYPOINT_TEMPLATE = \
  '<div id="waypoint%scont">\r\n' \
  '                    <input type="checkbox" id="waypoint%s" checked name="waypoint%s" value="initial" onchange="point_checkbox(this)">\r\n' \
  '                    <label for="waypoint%s" id="waypoint%sdesc" onclick="element_click(event, this)" onmouseover="point_over(this)" onmouseout="point_outside(this)"><br></label><br>\r\n' \
  '                    <span id="waypoint%sfocus">\r\n' \
  '                      <label for="waypoint%slat">{jlat}</label>\r\n' \
  '                      <input type="text" id="waypoint%slat" name="waypoint%slat" required pattern="[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)" value="%f" onchange="point_edit(true, true, true, true)"><br>\r\n' \
  '                      <label for="waypoint%slon">{jlon}</label>\r\n' \
  '                      <input type="text" id="waypoint%slon" name="waypoint%slon" required pattern="[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)" value="%f" onchange="point_edit(true, true, true, true)"><br>\r\n' \
  '                      <label for="waypoint%sele">{jele}</label>\r\n' \
  '                      <input type="text" id="waypoint%sele" name="waypoint%sele" pattern="([+-]?([0-9]+([.][0-9]*)?|[.][0-9]+))|" value="%s" onchange="point_edit(false, true, true, false)"><br>\r\n' \
  '                      <label for="waypoint%stime">{jhor}</label>\r\n' \
  '                      <input type="text" id="waypoint%stime" name="waypoint%stime" value="%s" onchange="point_edit(false, true, true, false)"><br>\r\n' \
  '                      <label for="waypoint%sname">{jname}</label>\r\n' \
  '                      <input type="text" id="waypoint%sname" name="waypoint%sname" value="%s" onchange="point_edit(false, true, false, false)"><br>\r\n' \
  '                    </span>\r\n' \
  '                  </div>'
  HTML_WAYPOINT_TEMPLATE = HTML_WAYPOINT_TEMPLATE.format_map(LSTRINGS['interface'])
  HTML_POINT_TEMPLATE = \
  '<div id="point%scont">\r\n' \
  '                    <input type="checkbox" id="point%s" checked name="point%s" value="initial" onchange="point_checkbox(this)" onmouseover="point_over(this)" onmouseout="point_outside(this)">\r\n' \
  '                    <label for="point%s" id="point%sdesc" onclick="element_click(event, this)"  onmouseover="point_over(this)" onmouseout="point_outside(this)"></label><br>\r\n' \
  '                    <span id="point%sfocus">\r\n' \
  '                      <label for="point%slat">{jlat}</label>\r\n' \
  '                      <input type="text" id="point%slat" name="point%slat" required pattern="[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)" value ="%f" onchange="point_edit(true, true, true, true)"><br>\r\n' \
  '                      <label for="point%slon">{jlon}</label>\r\n' \
  '                      <input type="text" id="point%slon" name="point%slon" required pattern="[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)" value="%f" onchange="point_edit(true, true, true, true)"><br>\r\n' \
  '                      <label for="point%sele">{jele}</label>\r\n' \
  '                      <input type="text" id="point%sele" name="point%sele" pattern="([+-]?([0-9]+([.][0-9]*)?|[.][0-9]+))|" value="%s" onchange="point_edit(false, true, true, false)"><br>\r\n' \
  '                      <label for="point%salt">{jalt}</label>\r\n' \
  '                      <input type="text" id="point%salt" name="point%salt" pattern="([+-]?([0-9]+([.][0-9]*)?|[.][0-9]+))|" value="%s" onchange="point_edit(false, true, true, false)"><br>\r\n' \
  '                      <label for="point%stime">{jhor}</label>\r\n' \
  '                      <input type="text" id="point%stime" name="point%stime" value="%s" onchange="point_edit(false, true, true, false)"><br>\r\n' \
  '                    </span>\r\n' \
  '                  </div>'
  HTML_POINT_TEMPLATE = HTML_POINT_TEMPLATE.format_map(LSTRINGS['interface'])
  HTML_SEGMENT_TEMPLATE = \
  '<div id="segment%scont">\r\n' \
  '                    <input type="checkbox" id="segment%s" checked name="segment%s" value="segment" onchange="segment_checkbox(this)">\r\n' \
  '                    <label for="segment%s" id="segment%sdesc" style="text-decoration:inherit;" onclick="element_click(event, this, false)">&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&nbsp;{jsegment} %s&nbsp;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;</label>\r\n' \
  '                    <br>'
  HTML_SEGMENT_TEMPLATE = HTML_SEGMENT_TEMPLATE.format_map(LSTRINGS['interface'])
  HTML_PATH_TEMPLATE = \
  '\r\n' \
  '              <svg id="track%s" viewbox="##VIEWBOX##" style="width:##WIDTH##;height:##HEIGHT##;top:##TOP##;left:##LEFT##;">\r\n' \
  '                <path id="path%s" onmousedown="mouse_down(event, this)" onmouseup="mouse_up(event, this)" onclick="mouse_click(event, this)" d="%s"/>\r\n' \
  '                <text dy="0.25em">\r\n' \
  '                  <textPath href="#path%s">##ARROWS##</textPath>\r\n' \
  '                </text>\r\n' \
  '              </svg>'
  HTML_WAYDOT_TEMPLATE = \
  '              <svg id="waydot%s" width="8" height="8" style="left:calc(%.1fpx / var(--scale) - 4px);top:calc(%.1fpx / var(--scale) - 4px);display:none;" onmousedown="mouse_down(event, this)" onmouseup="mouse_up(event, this)">\r\n' \
  '                <circle cx="4" cy="4" r="3"/>\r\n' \
  '              </svg>\r\n'
  HTML_DOT_TEMPLATE = \
  '              <svg id="dot%s" width="7" height="7" style="left:calc(%.1fpx / var(--scale) - 3.5px);top:calc(%.1fpx / var(--scale) - 3.5px);display:none;" onmousedown="mouse_down(event, this)" onmouseup="mouse_up(event, this)">\r\n' \
  '                <rect x="1" y="1" width="5" height="5"/>\r\n' \
  '              </svg>\r\n'
  HTML_3D_TEMPLATE = \
  '<!DOCTYPE html>\r\n' \
  '<html lang="fr-FR">\r\n' \
  '  <head>\r\n' \
  '    <meta charset="utf-8">\r\n' \
  '    <title>GPXTweaker 3DViewer</title>\r\n' \
  '    <style type="text/css">\r\n' \
  '      table {\r\n' \
  '        border: none;\r\n' \
  '        border-collapse:collapse;\r\n' \
  '        width:100vw;\r\n' \
  '        table-layout:fixed;\r\n' \
  '        padding:0;\r\n' \
  '        margin:0;\r\n' \
  '      }\r\n' \
  '      td {\r\n' \
  '        padding:0;\r\n' \
  '      }\r\n' \
  '      button {\r\n' \
  '        border:none;\r\n' \
  '        background-color:transparent;\r\n' \
  '        padding-left:5px;\r\n' \
  '        padding-right:5px;\r\n' \
  '        vertical-align:top;\r\n' \
  '        color:inherit;\r\n' \
  '        font-size:100%;\r\n' \
  '      }\r\n' \
  '      button:enabled {\r\n' \
  '        cursor:pointer;\r\n' \
  '      }\r\n' \
  '      input[type=range] {\r\n' \
  '        width:80px;\r\n' \
  '      }\r\n' \
  '      input[type=range]:enabled {\r\n' \
  '        cursor:pointer;\r\n' \
  '      }\r\n' \
  '      input[type=radio] {\r\n' \
  '        vertical-align:top;\r\n' \
  '        margin-bottom:5px;\r\n' \
  '      }\r\n' \
  '      input[type=radio]:enabled {\r\n' \
  '        cursor:pointer;\r\n' \
  '      }\r\n' \
  '    </style>\r\n' \
  '    <script>\r\n' \
  '      var size = Math.min(window.innerWidth, window.innerHeight).toString();\r\n' \
  '    </script>\r\n' \
  '  </head>\r\n' \
  '  <body style="margin:0;background-color:rgb(40,45,50);color:rgb(225,225,225);">\r\n' \
  '    <table>\r\n' \
  '      <colgroup>\r\n' \
  '        <col style="width:calc(100vw - 200px);">\r\n' \
  '        <col style="width:200px;">\r\n' \
  '      </colgroup>\r\n' \
  '      <tbody>\r\n' \
  '        <tr style="display:table-row;">\r\n' \
  '        <td style="display:table-cell;vertical-align:top;height:100vh;">\r\n' \
  '          <canvas id="canvas" width="100" height="100" style="position:absolute;top:0;left:0;"></canvas>\r\n' \
  '        </td>\r\n' \
  '        <td style="display:table-cell;vertical-align:top;border-left:1px solid dimgray;">\r\n' \
  '          <div style="overflow:auto;max-height:100vh;padding-left:5px;">\r\n' \
  '            <p>{#jtilt#}</p>\r\n' \
  '            <input type="range" id="cursor_tangle" min="0" max="90" step="any" value="0" autocomplete="off" disabled oninput="set_param(\'t\')">\r\n' \
  '            <br><span>0</span><span id = "cursorv_tangle" style="display:inline-block;width:calc(80px - 1em);text-align:center;">0</span><span>90</span>\r\n' \
  '            <br><br>\r\n' \
  '            <p>{#jrotation#}</p>\r\n' \
  '            <input type="range" id="cursor_rangle" min="0" max="360" step="any" value="0" autocomplete="off" disabled oninput="set_param(\'r\')">&nbsp;&nbsp;<button id="button_rangle" disabled onclick="toggle_rotation()">&#9199;</button>\r\n' \
  '            <br><span>0</span><span id = "cursorv_rangle" style="display:inline-block;width:calc(80px - 1em);text-align:center;">0</span><span>360</span>\r\n' \
  '            <br><br>\r\n' \
  '            <p>{#jzscale#}</p>\r\n' \
  '            <input type="range" id="cursor_zfact" min="1" max="1" step="any" value="1" autocomplete="off" disabled oninput="set_param(\'zs\')">\r\n' \
  '            <br><span>{#jzscaleiso#}</span><span id = "cursorv_tangle" style="display:inline-block;width:calc(80px - 2em);text-align:center;"></span><span>{#jzscalemax#}</span>\r\n' \
  '            <br><br>\r\n' \
  '            <p>{#jtexture#}</p>\r\n' \
  '            <input type="radio" id="radio_yiso" name="texture" checked autocomplete="off" disabled onclick="toggle_filling(0)"><label for="radio_yiso">{#jtextureyiso#}</label><br>\r\n' \
  '            <input type="radio" id="radio_ziso" name="texture" autocomplete="off" disabled onclick="toggle_filling(1)"><label for="radio_ziso">{#jtextureziso#}</label><br>\r\n' \
  '            <input type="radio" id="radio_map" name="texture" autocomplete="off" disabled onclick="toggle_filling(2)"><label for="radio_map">{#jtexturemap#}</label>\r\n' \
  '            <br><br>\r\n' \
  '            <p>{#jdimming#}</p>\r\n' \
  '            <input type="radio" id="radio_dimn" name="dimming" autocomplete="off" disabled onclick="toggle_dimming(0)"><label for="radio_dimn">{#jdimmingnone#}</label><br>\r\n' \
  '            <input type="radio" id="radio_dimz" name="dimming" autocomplete="off" disabled onclick="toggle_dimming(1)"><label for="radio_dimz">{#jdimmingz#}</label><br>\r\n' \
  '            <input type="radio" id="radio_dimd" name="dimming" checked autocomplete="off" disabled onclick="toggle_dimming(2)"><label for="radio_dimd">{#jdimmingdeclivity#}</label><br>\r\n' \
  '            <input type="radio" id="radio_dims" name="dimming" autocomplete="off" disabled onclick="toggle_dimming(3)"><label for="radio_dims">{#jdimmingshadow#}</label>\r\n' \
  '            <br><br>\r\n' \
  '            <p>{#jltilt#}</p>\r\n' \
  '            <input type="range" id="cursor_ltangle" min="0" max="90" step="any" value ="0" autocomplete="off" disabled oninput="set_param(\'lt\')">\r\n' \
  '            <br><span>0</span><span id = "cursorv_ltangle" style="display:inline-block;width:calc(80px - 1em);text-align:center;">0</span><span>90</span>\r\n' \
  '            <br><br>\r\n' \
  '            <p>{#jlrotation#}:</p>\r\n' \
  '            <input type="range" id="cursor_lrangle" min="0" max="360" step="any" value ="0" autocomplete="off" disabled oninput="set_param(\'lr\')">&nbsp;&nbsp;<button id="button_lrangle" disabled onclick="toggle_lrotation()">&#9199;</button>\r\n' \
  '            <br><span>0</span><span id = "cursorv_lrangle" style="display:inline-block;width:calc(80px - 1em);text-align:center;">0</span><span>360</span>\r\n' \
  '          </div>\r\n' \
  '        </td>\r\n' \
  '      </tbody>\r\n' \
  '    </table>\r\n' \
  '    <script>\r\n' \
  '      var canvas = document.getElementById("canvas");\r\n' \
  '      var gl = canvas.getContext("webgl2", {preserveDrawingBuffer: true});\r\n' \
  '      var c_tangle = document.getElementById("cursor_tangle");\r\n' \
  '      var cv_tangle = document.getElementById("cursorv_tangle");\r\n' \
  '      var c_rangle = document.getElementById("cursor_rangle");\r\n' \
  '      var cv_rangle = document.getElementById("cursorv_rangle");\r\n' \
  '      var b_rangle = document.getElementById("button_rangle");\r\n' \
  '      var c_zfact = document.getElementById("cursor_zfact");\r\n' \
  '      var r_yiso = document.getElementById("radio_yiso");\r\n' \
  '      var r_ziso = document.getElementById("radio_ziso");\r\n' \
  '      var r_map = document.getElementById("radio_map");\r\n' \
  '      var r_dimn = document.getElementById("radio_dimn");\r\n' \
  '      var r_dimz = document.getElementById("radio_dimz");\r\n' \
  '      var r_dimd = document.getElementById("radio_dimd");\r\n' \
  '      var r_dims = document.getElementById("radio_dims");\r\n' \
  '      var c_ltangle = document.getElementById("cursor_ltangle");\r\n' \
  '      var cv_ltangle = document.getElementById("cursorv_ltangle");\r\n' \
  '      var c_lrangle = document.getElementById("cursor_lrangle");\r\n' \
  '      var cv_lrangle = document.getElementById("cursorv_lrangle");\r\n' \
  '      var b_lrangle = document.getElementById("button_lrangle");\r\n' \
  '      var gl_programs = new Map();\r\n' \
  '      var cur_prog = null;\r\n' \
  '      var gl_attributes = new Map([["tvposition", ["vec4", 3]], ["lvposition", ["vec4", 3]]]);\r\n' \
  '      var gl_static_uniforms = new Map([["zfactmax", "float"], ["mpos", "vec4"], ["mtex", "sampler2D"], ["trtex", "sampler2D"], ["ftex", "sampler2D"], ["dtex", "sampler2D"]]);\r\n' \
  '      var gl_dynamic_uniforms = new Map([["zfact", "float"], ["vmatrix", "mat4"], ["lmatrix", "mat4"], ["ylmag", "float"], ["dmode", "int"], ["pmode", "int"], ["ltype", "int"]]);\r\n' \
  '      var vpositions = null;\r\n' \
  '      var trpositions = null;\r\n' \
  '      var tvposition = null;\r\n' \
  '      var lvposition = null;\r\n' \
  '      var vmatrix = null\r\n' \
  '      var lmatrix = null;\r\n' \
  '      var ltype = null;\r\n' \
  '      const m_size = 2048;\r\n' \
  '      const tr_size = 2048;\r\n' \
  '      const s_size = 2048;\r\n' \
  '      var mtex = 0;\r\n' \
  '      var trtex = 1;\r\n' \
  '      var ftex = 2;\r\n' \
  '      var dtex = 3;\r\n' \
  '      var map_texture = null;\r\n' \
  '      var tr_texture = null;\r\n' \
  '      var f_texture = null;\r\n' \
  '      var d_texture = null;\r\n' \
  '      var sfrbuf = null;\r\n' \
  '      function set_param(p, v=null) {\r\n' \
  '        if (p == "zs") {\r\n' \
  '          if (v != null) {c_zfact.value = v.toString();}\r\n' \
  '          zfact = parseFloat(c_zfact.value);\r\n' \
  '          cv_tangle.innerHTML = Math.round(90 - 180 / Math.PI * Math.atan(stangle / ctangle * zfact)).toString();\r\n' \
  '          let angle = Math.atan(slt0angle / clt0angle / zfact);\r\n' \
  '          cltangle = Math.cos(angle);\r\n' \
  '          sltangle = Math.sin(angle)\r\n' \
  '        } else {\r\n' \
  '          let angle = null;\r\n' \
  '          let angle0 = null;\r\n' \
  '          switch (p) {\r\n' \
  '            case "t":\r\n' \
  '              if (v != null) {c_tangle.value = v.toString();}\r\n' \
  '              angle = (90 - parseFloat(c_tangle.value)) * Math.PI / 180;\r\n' \
  '              break;\r\n' \
  '            case "r":\r\n' \
  '              if (v != null) {c_rangle.value = v.toString();}\r\n' \
  '              angle =  parseFloat(c_rangle.value) * Math.PI / 180;\r\n' \
  '              break;\r\n' \
  '            case "lt":\r\n' \
  '              if (v != null) {c_ltangle.value = v.toString();}\r\n' \
  '              angle0 = (parseFloat(c_ltangle.value) - 90) * Math.PI / 180;\r\n' \
  '              clt0angle = Math.cos(angle0);\r\n' \
  '              slt0angle = Math.sin(angle0);\r\n' \
  '              angle = Math.atan(slt0angle / clt0angle / zfact);\r\n' \
  '              break;\r\n' \
  '            case "lr":\r\n' \
  '              if (v != null) {c_lrangle.value = v.toString();}\r\n' \
  '              angle = - parseFloat(c_lrangle.value) * Math.PI / 180;\r\n' \
  '              break;\r\n' \
  '          }\r\n' \
  '          window["c" + p + "angle"] = Math.cos(angle);\r\n' \
  '          window["s" + p + "angle"] = Math.sin(angle);\r\n' \
  '          if (p == "t") {\r\n' \
  '            angle0 = Math.atan(stangle / ctangle * zfact);\r\n' \
  '            cv_tangle.innerHTML = Math.round(90 - angle0 * 180 / Math.PI).toString();\r\n' \
  '          } else if (p == "lt") {\r\n' \
  '            cv_ltangle.innerHTML = Math.round(angle0 * 180 / Math.PI + 90).toString();\r\n' \
  '          } else {\r\n' \
  '            window["cv_" + p + "angle"].innerHTML = Math.round(parseFloat(window["c_" + p + "angle"].value)).toString();\r\n' \
  '          }\r\n' \
  '\r\n' \
  '        }\r\n' \
  '        if (v == null) {canvas_redraw();}\r\n' \
  '      }\r\n' \
  '      var fillmode = 0;\r\n' \
  '      var pmode = 0;\r\n' \
  '      var dmode = 2;\r\n' \
  '      var zfact = 1;\r\n' \
  '      var ylmag = 1;\r\n' \
  '      var ctangle = null;\r\n' \
  '      var stangle = null;\r\n' \
  '      set_param("t", 30);\r\n' \
  '      var crangle = null;\r\n' \
  '      var srangle = null;\r\n' \
  '      set_param("r", 0);\r\n' \
  '      var nrot = 0;\r\n' \
  '      var nlrot = 0;\r\n' \
  '      var rep_rot = null;\r\n' \
  '      var rep_lrot = null;\r\n' \
  '      var ltangle_rotmax = null;\r\n' \
  '      var clt0angle = null;\r\n' \
  '      var slt0angle = null;\r\n' \
  '      var cltangle = null;\r\n' \
  '      var sltangle = null;\r\n' \
  '      set_param("lt", 35);\r\n' \
  '      var clrangle = null;\r\n' \
  '      var slrangle = null;\r\n' \
  '      set_param("lr", 315);\r\n' \
  '      set_param("zs", 1);##DECLARATIONS##\r\n' \
  '      function mat4_mult(p, m) {\r\n' \
  '        let q = m.slice();\r\n' \
  '        for (let r=0; r<4; r++) {\r\n' \
  '          for (let c=0; c<4; c++) {\r\n' \
  '            let v = 0;\r\n' \
  '            for (let i=0; i<4; i++) {v += p[4 * r + i] * q[4 * i + c];}\r\n' \
  '            m[4* r + c] = v;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mat4_zscale(zf) {\r\n' \
  '        return new Float32Array([\r\n' \
  '          1, 0, 0, 0,\r\n' \
  '          0, 1, 0, 0,\r\n' \
  '          0, 0, -zf, 1 - zf,\r\n' \
  '          0, 0, 0, 1\r\n' \
  '        ]);\r\n' \
  '      }\r\n' \
  '      function mat4_scale(w) {\r\n' \
  '        return new Float32Array([\r\n' \
  '          1, 0, 0, 0,\r\n' \
  '          0, 1, 0, 0,\r\n' \
  '          0, 0, 1, 0,\r\n' \
  '          0, 0, 0, w\r\n' \
  '        ]);\r\n' \
  '      }\r\n' \
  '      function mat4_yscale(ymag, ymax) {\r\n' \
  '        return new Float32Array([\r\n' \
  '          1, 0, 0, 0,\r\n' \
  '          0, ymag, 0, 1 - ymax * ymag / 1.733,\r\n' \
  '          0, 0, 1, 0,\r\n' \
  '          0, 0, 0, 1\r\n' \
  '        ]);\r\n' \
  '      }\r\n' \
  '      function mat4_tilt(c, s) {\r\n' \
  '        return new Float32Array([\r\n' \
  '          1, 0, 0, 0,\r\n' \
  '          0, c, -s, 0,\r\n' \
  '          0, s, c, 0,\r\n' \
  '          0, 0, 0, 1\r\n' \
  '        ]);\r\n' \
  '      }\r\n' \
  '      function mat4_rotation(c, s) {\r\n' \
  '        return new Float32Array([\r\n' \
  '          c, s, 0, 0,\r\n' \
  '          -s, c, 0, 0,\r\n' \
  '          0, 0, 1, 0,\r\n' \
  '          0, 0, 0, 1\r\n' \
  '        ]);\r\n' \
  '      }\r\n' \
  '      function canvas_resize() {\r\n' \
  '        size = Math.min(window.innerWidth, window.innerHeight).toString();\r\n' \
  '        canvas.setAttribute("width", size);\r\n' \
  '        canvas.setAttribute("height", size);\r\n' \
  '        gl.viewport(0, 0, canvas.width, canvas.height);\r\n' \
  '      }\r\n' \
  '      function program_create(name, vshader_s, fshader_s) {\r\n' \
  '        let vertex_shader = gl.createShader(gl.VERTEX_SHADER);\r\n' \
  '        gl.shaderSource(vertex_shader, vshader_s);\r\n' \
  '        gl.compileShader(vertex_shader);\r\n' \
  '        let fragment_shader = gl.createShader(gl.FRAGMENT_SHADER);\r\n' \
  '        gl.shaderSource(fragment_shader, fshader_s);\r\n' \
  '        gl.compileShader(fragment_shader);\r\n' \
  '        let prog = gl.createProgram();\r\n' \
  '        gl.attachShader(prog, vertex_shader);\r\n' \
  '        gl.attachShader(prog, fragment_shader);\r\n' \
  '        gl.linkProgram(prog);\r\n' \
  '        gl_programs.set(name, new Map());\r\n' \
  '        gl_programs.get(name).set("program", prog);\r\n' \
  '        gl_programs.get(name).set("vao", gl.createVertexArray());\r\n' \
  '        for (let [n, ts] of gl_attributes) {\r\n' \
  '          if (vshader_s.indexOf("in " + ts[0] + " " + n) >= 0) {\r\n' \
  '            gl_programs.get(name).set(n, gl.getAttribLocation(prog, n));\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        for (let [n, t] of [...gl_static_uniforms.entries(), ...gl_dynamic_uniforms.entries()]) {\r\n' \
  '          if (vshader_s.indexOf("uniform " + t + " " + n) >= 0 || fshader_s.indexOf("uniform " + t + " " + n) >= 0) {\r\n' \
  '            gl_programs.get(name).set(n, gl.getUniformLocation(prog, n));\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function program_use(name) {\r\n' \
  '        cur_prog = name;\r\n' \
  '        gl.useProgram(gl_programs.get(name).get("program"));\r\n' \
  '        gl.bindVertexArray(gl_programs.get(name).get("vao"));\r\n' \
  '      }\r\n' \
  '      function program_attributes() {\r\n' \
  '        for (let [n, ts] of gl_attributes) {\r\n' \
  '          if (gl_programs.get(cur_prog).has(n)) {\r\n' \
  '            gl.enableVertexAttribArray(gl_programs.get(cur_prog).get(n));\r\n' \
  '            gl.bindBuffer(gl.ARRAY_BUFFER, window[n]);\r\n' \
  '            gl.vertexAttribPointer(gl_programs.get(cur_prog).get(n), ts[1], ts[0].substring(0, 3) == "vec" ? gl.FLOAT : gl.FLOAT, false, 0, 0);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function program_uniforms(type="dynamic") {\r\n' \
  '        for (let [n, t] of type=="static"?gl_static_uniforms:gl_dynamic_uniforms) {\r\n' \
  '          if (gl_programs.get(cur_prog).has(n)) {\r\n' \
  '            switch (t) {\r\n' \
  '              case "float":\r\n' \
  '                gl.uniform1f(gl_programs.get(cur_prog).get(n), window[n]);\r\n' \
  '                break;\r\n' \
  '              case "vec4":\r\n' \
  '                gl.uniform4fv(gl_programs.get(cur_prog).get(n), window[n]);\r\n' \
  '                break;\r\n' \
  '              case "mat4":\r\n' \
  '                gl.uniformMatrix4fv(gl_programs.get(cur_prog).get(n), true, window[n]);\r\n' \
  '                gl.finish();\r\n' \
  '                break;\r\n' \
  '              case "sampler2D":\r\n' \
  '              case "int":\r\n' \
  '                gl.uniform1i(gl_programs.get(cur_prog).get(n), window[n]);\r\n' \
  '                break;\r\n' \
  '              default:\r\n' \
  '                gl.uniform1f(gl_programs.get(cur_prog).get(n), window[n]);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function texture_load(unit, src) {\r\n' \
  '        let gl_texture = gl.createTexture();\r\n' \
  '        gl.activeTexture(unit);\r\n' \
  '        gl.bindTexture(gl.TEXTURE_2D, gl_texture);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);\r\n' \
  '        if (Array.isArray(src)) {\r\n' \
  '          gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array(src))\r\n' \
  '        } else {\r\n' \
  '          gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, src);\r\n' \
  '        }\r\n' \
  '        gl.generateMipmap(gl.TEXTURE_2D);\r\n' \
  '        return gl_texture;\r\n' \
  '      }\r\n' \
  '      function texture_attach(unit, type) {\r\n' \
  '        let gl_texture = gl.createTexture();\r\n' \
  '        gl.activeTexture(unit);\r\n' \
  '        gl.bindTexture(gl.TEXTURE_2D, gl_texture);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);\r\n' \
  '        gl.texImage2D(gl.TEXTURE_2D, 0, type=="depth"?gl.DEPTH_COMPONENT16:gl.R8, s_size, s_size, 0, type=="depth"?gl.DEPTH_COMPONENT:gl.RED, type=="depth"?gl.UNSIGNED_SHORT:gl.UNSIGNED_BYTE, null);\r\n' \
  '        gl.framebufferTexture2D(gl.FRAMEBUFFER, type=="depth"?gl.DEPTH_ATTACHMENT:gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, gl_texture, 0);\r\n' \
  '        return gl_texture;\r\n' \
  '      }\r\n' \
  '      function canvas_init() {\r\n' \
  '        gl.enable(gl.DEPTH_TEST);\r\n' \
  '        canvas_resize();\r\n' \
  '        let vertex_tcshader_s = `#version 300 es\r\n' \
  '          in vec4 tvposition;\r\n' \
  '          uniform float zfact;\r\n' \
  '          uniform float zfactmax;\r\n' \
  '          uniform mat4 vmatrix;\r\n' \
  '          uniform mat4 lmatrix;\r\n' \
  '          uniform int dmode;\r\n' \
  '          out vec2 pcoord;\r\n' \
  '          out float nz;\r\n' \
  '          out float dim;\r\n' \
  '          out vec4 lposition;\r\n' \
  '          void main() {\r\n' \
  '            nz = zfactmax * (tvposition.z + 1.0) - 1.0;\r\n' \
  '            gl_Position = vmatrix * tvposition;\r\n' \
  '            pcoord = (tvposition.xy + 1.0) / 2.0;\r\n' \
  '            dim = dmode == 1 ? pow(0.5 * nz + 0.5, 0.7) : 0.7;\r\n' \
  '            lposition = dmode >= 2 ? lmatrix * tvposition : vec4(vec3(0), 1);\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let vertex_ttshader_s = `#version 300 es\r\n' \
  '          in vec4 tvposition;\r\n' \
  '          uniform float zfact;\r\n' \
  '          uniform float zfactmax;\r\n' \
  '          uniform mat4 vmatrix;\r\n' \
  '          uniform mat4 lmatrix;\r\n' \
  '          uniform int dmode;\r\n' \
  '          out vec2 pcoord;\r\n' \
  '          out float dim;\r\n' \
  '          out vec4 lposition;\r\n' \
  '          void main() {\r\n' \
  '            gl_Position = vmatrix * tvposition;\r\n' \
  '            pcoord = (tvposition.xy + 1.0) / 2.0;\r\n' \
  '            dim = dmode == 1 ? pow(0.5 * zfactmax * (tvposition.z + 1.0), 0.7) : 1.0;\r\n' \
  '            lposition = dmode >= 2 ? lmatrix * tvposition : vec4(vec3(0), 1);\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let vertex_lshader_s = `#version 300 es\r\n' \
  '          in vec4 lvposition;\r\n' \
  '          uniform mat4 vmatrix;\r\n' \
  '          uniform int ltype;\r\n' \
  '          out vec4 color;\r\n' \
  '          void main() {\r\n' \
  '            gl_Position = vmatrix * lvposition;\r\n' \
  '            color = ltype == 0 ? vec4(vec3(0.35 * lvposition.z + 0.65), 1) : vec4(1, 1, 0, 1);\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let vertex_sshader_s = `#version 300 es\r\n' \
  '          in vec4 tvposition;\r\n' \
  '          uniform float zfact;\r\n' \
  '          uniform mat4 lmatrix;\r\n' \
  '          void main() {\r\n' \
  '            gl_Position = lmatrix * tvposition;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let fragment_cshader_s = `#version 300 es\r\n' \
  '          precision highp float;\r\n' \
  '          precision highp int;\r\n' \
  '          in vec2 pcoord;\r\n' \
  '          in float nz;\r\n' \
  '          in float dim;\r\n' \
  '          in vec4 lposition;\r\n' \
  '          uniform sampler2D trtex;\r\n' \
  '          uniform sampler2D ftex;\r\n' \
  '          uniform sampler2D dtex;\r\n' \
  '          uniform float ylmag;\r\n' \
  '          uniform int pmode;\r\n' \
  '          uniform int dmode;\r\n' \
  '          out vec4 pcolor;\r\n' \
  '          void main() {\r\n' \
  '            float color = fract(pmode == 0 ? pcoord.y * 100.0 : (1.0 + nz) * 25.0) <= 0.15 ? 0.0 : 1.0;\r\n' \
  '            vec2 pix = dmode >= 2 ? vec2(1) / vec2(textureSize(dtex, 0)) : vec2(0);\r\n' \
  '            vec2 pos = (lposition.xy / lposition.w + 1.0) / 2.0;\r\n' \
  '            vec3 norm = dmode >= 2 ? vec3((texture(dtex, pos + vec2(pix.x, 0)).r - texture(dtex, pos - vec2(pix.x, 0)).r) / (2.0 * pix.x), (texture(dtex, pos + vec2(0, pix.y)).r - texture(dtex, pos - vec2(0, pix.y)).r) / (2.0 * pix.y / ylmag), 1) : vec3(0);\r\n' \
  '            float cinc = dmode >= 2 ? (dmode == 2 ? dot(vec3(0, 0.82 , 0.57), norm) : 1.0) / length(norm) : 0.0;\r\n' \
  '            float pdim = dmode < 2 ? dim : dmode == 2 ? mix(0.7 + 0.3 * clamp(mix(1.5, 4.0, cinc <= 0.57) * (cinc - 0.57) + 0.8, 0.0, 1.0), 0.3, gl_FrontFacing) : mix(((texture(ftex, pos).r < 0.5) ^^ gl_FrontFacing) ? 0.2 : 0.3 + 0.7 * cinc, 0.2, lposition.z / lposition.w + 0.99 + 0.009 * cinc > 2.0 * texture(dtex, pos).r);\r\n' \
  '            pcolor = gl_FrontFacing ? mix(vec4(0, 0, pdim, 1), vec4(pdim * vec3(0.47, 0.42, 0.35), 1), color) : mix(mix(vec4(0, 0, pdim, 1), vec4(pdim * vec3(0.82, 1, 0.74), 1), color), vec4(1, 0, 0, 1), texture(trtex, pcoord).r);\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let fragment_tshader_s = `#version 300 es\r\n' \
  '          precision highp float;\r\n' \
  '          precision highp int;\r\n' \
  '          in vec2 pcoord;\r\n' \
  '          in float dim;\r\n' \
  '          in vec4 lposition;\r\n' \
  '          uniform sampler2D mtex;\r\n' \
  '          uniform sampler2D trtex;\r\n' \
  '          uniform sampler2D ftex;\r\n' \
  '          uniform sampler2D dtex;\r\n' \
  '          uniform float ylmag;\r\n' \
  '          uniform vec4 mpos;\r\n' \
  '          uniform int dmode;\r\n' \
  '          out vec4 pcolor;\r\n' \
  '          void main() {\r\n' \
  '            vec2 pix = dmode >= 2 ? vec2(1) / vec2(textureSize(dtex, 0)) : vec2(0);\r\n' \
  '            vec2 pos = (lposition.xy / lposition.w + 1.0) / 2.0;\r\n' \
  '            vec3 norm = dmode >= 2 ? vec3((texture(dtex, pos + vec2(pix.x, 0)).r - texture(dtex, pos - vec2(pix.x, 0)).r) / (2.0 * pix.x), (texture(dtex, pos + vec2(0, pix.y)).r - texture(dtex, pos - vec2(0, pix.y)).r) / (2.0 * pix.y / ylmag), 1) : vec3(0);\r\n' \
  '            float cinc = dmode >= 2 ? (dmode == 2 ? dot(vec3(0, 0.82 , 0.57), norm) : 1.0) / length(norm) : 0.0;\r\n' \
  '            float pdim = dmode < 2 ? dim : dmode == 2 ? mix(0.7 + 0.3 * clamp(mix(1.5, 4.0, cinc <= 0.57) * (cinc - 0.57) + 0.8, 0.0, 1.0), 0.3, gl_FrontFacing) : mix(((texture(ftex, pos).r < 0.5) ^^ gl_FrontFacing) ? 0.2 : 0.3 + 0.7 * cinc, 0.2, lposition.z / lposition.w + 0.99 + 0.009 * cinc > 2.0 * texture(dtex, pos).r);\r\n' \
  '            pcolor = gl_FrontFacing ? vec4(pdim * vec3(0.47, 0.42, 0.35), 1) : mix(texture(mtex, mpos.st * pcoord + mpos.pq) * vec4(vec3(pdim), 1.0), vec4(1, 0, 0, 1), texture(trtex, pcoord).r);\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let fragment_lshader_s = `#version 300 es\r\n' \
  '          precision highp float;\r\n' \
  '          in vec4 color;\r\n' \
  '          out vec4 pcolor;\r\n' \
  '          void main() {\r\n' \
  '            pcolor = color;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let fragment_sshader_s = `#version 300 es\r\n' \
  '          precision highp float;\r\n' \
  '          out float pcolor;\r\n' \
  '          void main() {\r\n' \
  '            pcolor = gl_FrontFacing ? 0.0 : 1.0;\r\n' \
  '          }\r\n' \
  '      `;\r\n' \
  '        function create_map() {\r\n' \
  '          let nrow = tmaxrow + 1 - tminrow;\r\n' \
  '          let ncol = tmaxcol + 1 - tmincol;\r\n' \
  '          let mheight = m_size * nrow / Math.max(nrow, ncol);\r\n' \
  '          let mwidth = m_size * ncol / Math.max(nrow, ncol);\r\n' \
  '          let ntiles = nrow * ncol;\r\n' \
  '          let cnv2d = document.createElement("canvas");\r\n' \
  '          let ctx = cnv2d.getContext("2d");\r\n' \
  '          cnv2d.height = mheight;\r\n' \
  '          mheight = cnv2d.height;\r\n' \
  '          cnv2d.width = mwidth;\r\n' \
  '          mwidth = cnv2d.width;\r\n' \
  '          ctx.fillStyle = "RGB(0,127,0)";\r\n' \
  '          ctx.fillRect(0, 0, mwidth, mheight);\r\n' \
  '          function map_complete() {\r\n' \
  '            gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);\r\n' \
  '            map_texture = texture_load(gl.TEXTURE0, cnv2d);\r\n' \
  '            gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);\r\n' \
  '            r_map.disabled = false;\r\n' \
  '          }\r\n' \
  '          function terr_cb() {\r\n' \
  '            ntiles--;\r\n' \
  '            if (ntiles == 0) {map_complete();}\r\n' \
  '          }\r\n' \
  '          function tload_cb(tile, row, col) {\r\n' \
  '            ctx.drawImage(tile, Math.round((col - tmincol) / ncol * mwidth), Math.round((row - tminrow) / nrow * mheight), Math.round((col + 1 - tmincol) / ncol * mwidth) - Math.round((col - tmincol) / ncol * mwidth), Math.round((row + 1 - tminrow) / nrow * mheight) - Math.round((row - tminrow) / nrow * mheight));\r\n' \
  '            terr_cb();\r\n' \
  '          }\r\n' \
  '          for (let row=tminrow; row<=tmaxrow; row++) {\r\n' \
  '            for (let col=tmincol; col<=tmaxcol; col++) {\r\n' \
  '              let tile = new Image();\r\n' \
  '              tile.crossOrigin = "anonymous";\r\n' \
  '              tile.onload = (e) => {tload_cb(e.target, row, col);}\r\n' \
  '              tile.onerror = (e) => {terr_cb();}\r\n' \
  '              tile.src = "http://" + location.hostname + ":" + (portmin + (row + col) % (portmax + 1 - portmin)).toString() + ##TILEPATH##;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        function create_track_map() {\r\n' \
  '          function move_to(x, y, d=true) {\r\n' \
  '            if (d) {\r\n' \
  '              ctx.lineTo(tr_size * (x + 1) / 2, tr_size * (y + 1) / 2);\r\n' \
  '            } else {\r\n' \
  '              ctx.moveTo(tr_size * (x + 1) / 2, tr_size * (y + 1) / 2);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          const ar_f = 0.1;\r\n' \
  '          const ar_s = 0.2;\r\n' \
  '          let cnv2d = document.createElement("canvas");\r\n' \
  '          let ctx = cnv2d.getContext("2d");\r\n' \
  '          cnv2d.height = tr_size;\r\n' \
  '          cnv2d.width = tr_size;\r\n' \
  '          ctx.strokeStyle = "red";\r\n' \
  '          ctx.lineWidth = 8;\r\n' \
  '          ctx.lineJoin = "round";\r\n' \
  '          ctx.lineCap = "round";\r\n' \
  '          ctx.fillStyle = "red";\r\n' \
  '          for (let s=0; s<trpositions.length; s++) {\r\n' \
  '            let ind = 0;\r\n' \
  '            let dr = false;\r\n' \
  '            let dist = 0;\r\n' \
  '            let ar_d = ar_f;\r\n' \
  '            let px = null;\r\n' \
  '            let py = null;\r\n' \
  '            let tx = null;\r\n' \
  '            let ty = null;\r\n' \
  '            let td = null;\r\n' \
  '            let tdx = null;\r\n' \
  '            let tdy = null;\r\n' \
  '            let ar = false;\r\n' \
  '            while (ind < trpositions[s].length - 1) {\r\n' \
  '              if (! dr) {\r\n' \
  '                px = trpositions[s][ind];\r\n' \
  '                py = trpositions[s][ind+1];\r\n' \
  '                ctx.beginPath();\r\n' \
  '                ctx.arc(tr_size * (px + 1) / 2, tr_size * (py + 1) / 2, 10, 0, 2 * Math.PI);\r\n' \
  '                ctx.stroke()\r\n' \
  '                ctx.fill();\r\n' \
  '                ctx.beginPath();\r\n' \
  '                move_to(px, py, false);\r\n' \
  '                ind += 2;\r\n' \
  '              } else {\r\n' \
  '                tdx = trpositions[s][ind] - px;\r\n' \
  '                tdy = trpositions[s][ind+1] - py;\r\n' \
  '                td = Math.sqrt(tdx * tdx + tdy * tdy);\r\n' \
  '                if (td > 0) {\r\n' \
  '                  tx = tdx / td;\r\n' \
  '                  ty = tdy / td;\r\n' \
  '                  dist += td;\r\n' \
  '                }\r\n' \
  '                if (dist < ar_d) {\r\n' \
  '                  px = trpositions[s][ind];\r\n' \
  '                  py = trpositions[s][ind+1];\r\n' \
  '                  ar = false;\r\n' \
  '                  ind += 2;\r\n' \
  '                  if (ind >= trpositions[s].length - 1) {\r\n' \
  '                    ar = true;\r\n' \
  '                  } else if (trpositions[s][ind] == null || trpositions[s][ind + 1] == null) {\r\n' \
  '                    ar = true;\r\n' \
  '                  }\r\n' \
  '                } else {\r\n' \
  '                  ar = true;\r\n' \
  '                  px = trpositions[s][ind] - (dist - ar_d) * tx;\r\n' \
  '                  py = trpositions[s][ind+1] - (dist - ar_d) * ty;\r\n' \
  '                  dist = 0;\r\n' \
  '                  ar_d = ar_s;\r\n' \
  '                }\r\n' \
  '                move_to(px, py);\r\n' \
  '                if (ar && tx != null && ty != null) {\r\n' \
  '                  move_to(px - 0.025 * tx - 0.015 * ty, py - 0.025 * ty + 0.015 * tx);\r\n' \
  '                  move_to(px - 0.025 * tx + 0.015 * ty, py - 0.025 * ty - 0.015 * tx, false);\r\n' \
  '                  move_to(px, py);\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              dr = true;\r\n' \
  '            }\r\n' \
  '            ctx.stroke();\r\n' \
  '          }\r\n' \
  '          tr_texture = texture_load(gl.TEXTURE1, cnv2d);\r\n' \
  '          create_map();\r\n' \
  '        }\r\n' \
  '        program_create("tcprogram", vertex_tcshader_s, fragment_cshader_s);\r\n' \
  '        program_create("ttprogram", vertex_ttshader_s, fragment_tshader_s);\r\n' \
  '        program_create("lprogram", vertex_lshader_s, fragment_lshader_s);\r\n' \
  '        program_create("sprogram", vertex_sshader_s, fragment_sshader_s);\r\n' \
  '        texture_load(gl.TEXTURE0, [0, 127, 0, 255]);\r\n' \
  '        texture_load(gl.TEXTURE1, [0, 0, 0, 255]);\r\n' \
  '        create_track_map();\r\n' \
  '        tvposition = gl.createBuffer();\r\n' \
  '        gl.bindBuffer(gl.ARRAY_BUFFER, tvposition);\r\n' \
  '        gl.bufferData(gl.ARRAY_BUFFER, vpositions, gl.STATIC_DRAW);\r\n' \
  '        lvposition = gl.createBuffer();\r\n' \
  '        gl.bindBuffer(gl.ARRAY_BUFFER, lvposition);\r\n' \
  '        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([\r\n' \
  '          0, 0, -1,\r\n' \
  '          1.225, 0, -1,\r\n' \
  '          0, 0, -1,\r\n' \
  '          0, 1.225, -1,\r\n' \
  '          0, 1.225, -1,\r\n' \
  '          -0.05, 1.125, -1,\r\n' \
  '          0, 1.225, -1,\r\n' \
  '          0.05, 1.125, -1,\r\n' \
  '          0, 0, -1,\r\n' \
  '          0, 0, 1.225,\r\n' \
  '          0, 0, 1.65,\r\n' \
  '          0, 0, 1.5,\r\n' \
  '          0, 0, 1.5,\r\n' \
  '          0, -0.02, 1.55,\r\n' \
  '          0, 0, 1.5,\r\n' \
  '          0, 0.02, 1.55,\r\n' \
  '          -0.5, 0, 1.65,\r\n' \
  '          -0.5, 0, 1.5,\r\n' \
  '          -0.5, 0, 1.5,\r\n' \
  '          -0.5, -0.02, 1.55,\r\n' \
  '          -0.5, 0, 1.5,\r\n' \
  '          -0.5, 0.02, 1.55,\r\n' \
  '          0.5, 0, 1.65,\r\n' \
  '          0.5, 0, 1.5,\r\n' \
  '          0.5, 0, 1.5,\r\n' \
  '          0.5, -0.02, 1.55,\r\n' \
  '          0.5, 0, 1.5,\r\n' \
  '          0.5, 0.02, 1.55\r\n' \
  '        ]), gl.STATIC_DRAW);\r\n' \
  '        for (let n of gl_programs.keys()) {\r\n' \
  '          program_use(n);\r\n' \
  '          program_attributes();\r\n' \
  '          program_uniforms("static");\r\n' \
  '        }\r\n' \
  '        sfrbuf = gl.createFramebuffer();\r\n' \
  '        gl.bindFramebuffer(gl.FRAMEBUFFER, sfrbuf);\r\n' \
  '        d_texture = texture_attach(gl.TEXTURE3, "depth");\r\n' \
  '        f_texture = texture_attach(gl.TEXTURE2, "shadow");\r\n' \
  '        gl.bindFramebuffer(gl.FRAMEBUFFER, null);\r\n' \
  '      }\r\n' \
  '      function canvas_redraw() {\r\n' \
  '        vmatrix = mat4_zscale(zfact);\r\n' \
  '        mat4_mult(mat4_scale(1.733), vmatrix);\r\n' \
  '        lmatrix = mat4_zscale(1);\r\n' \
  '        mat4_mult(mat4_rotation(crangle, srangle), vmatrix);\r\n' \
  '        mat4_mult(mat4_tilt(ctangle, stangle), vmatrix);\r\n' \
  '        if (dmode >= 2) {\r\n' \
  '          mat4_mult(mat4_scale(1.733), lmatrix);\r\n' \
  '          if (dmode == 2) {mat4_mult(mat4_rotation(crangle, srangle), lmatrix);}\r\n' \
  '          mat4_mult(mat4_rotation(clrangle, slrangle), lmatrix);\r\n' \
  '          if (dmode == 2) {;\r\n' \
  '            ylmag = 1;\r\n' \
  '          } else {;\r\n' \
  '            mat4_mult(mat4_tilt(clt0angle, slt0angle), lmatrix);\r\n' \
  '            ylmag = 1.732 / (1.415 * clt0angle - slt0angle / zfactmax);\r\n' \
  '            mat4_mult(mat4_yscale(ylmag, 1.415 * clt0angle - slt0angle), lmatrix);\r\n' \
  '          }\r\n' \
  '          gl.bindFramebuffer(gl.FRAMEBUFFER, sfrbuf);\r\n' \
  '          gl.viewport(0, 0, s_size, s_size);\r\n' \
  '          gl.clearColor(0, 0, 0, 0);\r\n' \
  '          gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);\r\n' \
  '          program_use("sprogram");\r\n' \
  '          program_uniforms();\r\n' \
  '          gl.drawArrays(gl.TRIANGLE_STRIP, 0, vpositions.length / 3);\r\n' \
  '          gl.bindFramebuffer(gl.FRAMEBUFFER, null);\r\n' \
  '          gl.viewport(0, 0, canvas.width, canvas.height);\r\n' \
  '        }\r\n' \
  '        gl.clearColor(0, 0, 0, 0);\r\n' \
  '        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);\r\n' \
  '        program_use(fillmode<2?"tcprogram":"ttprogram");\r\n' \
  '        pmode = fillmode==1?1:0;\r\n' \
  '        program_uniforms();\r\n' \
  '        gl.drawArrays(gl.TRIANGLE_STRIP, 0, vpositions.length / 3);\r\n' \
  '        program_use("lprogram");\r\n' \
  '        vmatrix = mat4_zscale(1);\r\n' \
  '        mat4_mult(mat4_scale(1.733), vmatrix);\r\n' \
  '        mat4_mult(mat4_rotation(crangle, srangle), vmatrix);\r\n' \
  '        mat4_mult(mat4_tilt(ctangle, stangle), vmatrix);\r\n' \
  '        ltype = 0;\r\n' \
  '        program_uniforms();\r\n' \
  '        gl.drawArrays(gl.LINES, 0, 10);\r\n' \
  '        if (dmode >= 2) {\r\n' \
  '          ltype = 1;\r\n' \
  '          vmatrix = mat4_zscale(1);\r\n' \
  '          mat4_mult(mat4_scale(1.733), vmatrix);\r\n' \
  '          mat4_mult(mat4_tilt(clt0angle, -slt0angle), vmatrix);\r\n' \
  '          if (dmode == 3) {mat4_mult(mat4_rotation(crangle, srangle), vmatrix);}\r\n' \
  '          mat4_mult(mat4_rotation(clrangle, -slrangle), vmatrix);\r\n' \
  '          mat4_mult(mat4_tilt(ctangle, stangle), vmatrix);\r\n' \
  '          program_uniforms();\r\n' \
  '          gl.drawArrays(gl.LINES, 10, 18);\r\n' \
  '        } \r\n' \
  '        if (dmode == 3) {\r\n' \
  '          vmatrix = mat4_zscale(1);\r\n' \
  '          mat4_mult(mat4_scale(1.733), vmatrix);\r\n' \
  '          mat4_mult(mat4_tilt(cltangle, -sltangle), vmatrix);\r\n' \
  '          mat4_mult(mat4_rotation(crangle, srangle), vmatrix);\r\n' \
  '          mat4_mult(mat4_rotation(clrangle, -slrangle), vmatrix);\r\n' \
  '          mat4_mult(mat4_tilt(ctangle, stangle), vmatrix);\r\n' \
  '          program_uniforms();\r\n' \
  '          gl.drawArrays(gl.LINES, 10, 18);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function canvas_rotate(number=null) {\r\n' \
  '        if (number != null) {\r\n' \
  '          if (nrot >= number) {\r\n' \
  '            window.clearInterval(rep_rot);\r\n' \
  '            set_param("r", 0);\r\n' \
  '            canvas_redraw();\r\n' \
  '            c_rangle.disabled = false;\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        let rangle = parseFloat(c_rangle.value) + 2;\r\n' \
  '        if (rangle >= 360) {\r\n' \
  '          nrot ++;\r\n' \
  '          rangle -= 360;\r\n' \
  '        }\r\n' \
  '        set_param("r", rangle);\r\n' \
  '        canvas_redraw();\r\n' \
  '      }\r\n' \
  '      function canvas_lrotate(number=null) {\r\n' \
  '        if (number != null) {\r\n' \
  '          if (nlrot >= number) {\r\n' \
  '            window.clearInterval(rep_lrot);\r\n' \
  '            set_param("lr", 0);\r\n' \
  '            set_param("lt", ltangle_rotmax);\r\n' \
  '            canvas_redraw();\r\n' \
  '            c_lrangle.disabled = false;\r\n' \
  '            c_ltangle.disabled = false;\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        let lrangle = parseFloat(c_lrangle.value) + 2;\r\n' \
  '        if (lrangle >= 270 + parseFloat(c_rangle.value) || (lrangle < 90 + parseFloat(c_rangle.value) && lrangle >= parseFloat(c_rangle.value) - 90)) {\r\n' \
  '          nlrot ++;\r\n' \
  '          lrangle -= 180;\r\n' \
  '        }\r\n' \
  '        if (lrangle < 0) {lrangle += 360}\r\n' \
  '        if (lrangle >= 360) {lrangle -= 360}\r\n' \
  '        set_param("lr", lrangle);\r\n' \
  '        set_param("lt", Math.sin((lrangle - 90 - parseFloat(c_rangle.value)) * Math.PI / 180) * ltangle_rotmax);\r\n' \
  '        canvas_redraw();\r\n' \
  '      }\r\n' \
  '      function data_load() {\r\n' \
  '        function derror_cb(t) {\r\n' \
  '        }\r\n' \
  '        function dload_cb(t) {\r\n' \
  '          if (t.status != 200) {derror_cb(); return;}\r\n' \
  '          let lvx = (new Uint32Array(t.response, 0, 1))[0];\r\n' \
  '          let vx = new Float32Array(t.response, 4, lvx);\r\n' \
  '          let lvy = (new Uint32Array(t.response, 4 * (1 + lvx), 1))[0];\r\n' \
  '          let vy = new Float32Array(t.response, 4 * (2 + lvx) , lvy);\r\n' \
  '          let lvz = (new Uint32Array(t.response, 4 * (2 + lvx + lvy), 1))[0];\r\n' \
  '          let vz = new Float32Array(t.response, 4 * (3 + lvx + lvy), lvz);\r\n' \
  '          let nx = vx.length;\r\n' \
  '          let ny = vy.length;\r\n' \
  '          vpositions = new Float32Array((ny - 1) * (nx + 1) * 6);\r\n' \
  '          let i = 0;\r\n' \
  '          for (let iy=0; iy<ny-1; iy++) {\r\n' \
  '            for (let ix=0; ix<nx; ix++) {\r\n' \
  '              vpositions[i] = vx[ix];\r\n' \
  '              vpositions[i + 1] = vy[iy];\r\n' \
  '              vpositions[i + 2] = vz[iy * nx + ix];\r\n' \
  '              vpositions[i + 3] = vx[ix];\r\n' \
  '              vpositions[i + 4] = vy[iy + 1];\r\n' \
  '              vpositions[i + 5] = vz[(iy + 1) * nx + ix];\r\n' \
  '              i += 6;\r\n' \
  '            }\r\n' \
  '            vpositions[i] = vx[nx - 1];\r\n' \
  '            vpositions[i + 1] = vy[iy + 1];\r\n' \
  '            vpositions[i + 2] = vz[(iy + 1) * nx + nx - 1];\r\n' \
  '            vpositions[i + 3] = vx[0];\r\n' \
  '            vpositions[i + 4] = vy[iy + 1];\r\n' \
  '            vpositions[i + 5] = vz[(iy + 1) * nx];\r\n' \
  '            i += 6;\r\n' \
  '          }\r\n' \
  '          let ns = (new Uint32Array(t.response, 4 * (3 + lvx + lvy + lvz), 1))[0];\r\n' \
  '          trpositions = new Array(ns);\r\n' \
  '          i = 0;\r\n' \
  '          for (let s=0; s<ns; s++) {\r\n' \
  '            let nspts = (new Uint32Array(t.response, 4 * (4 + lvx + lvy + lvz + s + 2 * i), 1))[0];\r\n' \
  '            trpositions[s] = (new Float32Array(t.response, 4 * (5 + lvx + lvy + lvz + s + 2 * i), 2 * nspts));\r\n' \
  '            i += nspts;\r\n' \
  '          }\r\n' \
  '          canvas_init();\r\n' \
  '          canvas_redraw();\r\n' \
  '          window.onresize = (e) => {canvas_resize(); canvas_redraw();};\r\n' \
  '          c_tangle.disabled = false;\r\n' \
  '          c_rangle.disabled = false;\r\n' \
  '          b_rangle.disabled = false;\r\n' \
  '          if (zfactmax > 1) {\r\n' \
  '            c_zfact.max = zfactmax.toString();\r\n' \
  '            c_zfact.disabled = false;\r\n' \
  '          }\r\n' \
  '          r_yiso.disabled = false;\r\n' \
  '          r_ziso.disabled = false;\r\n' \
  '          r_dimn.disabled = false;\r\n' \
  '          r_dimz.disabled = false\r\n' \
  '          r_dimd.disabled = false\r\n' \
  '          r_dims.disabled = false;\r\n' \
  '           <!-- toggle_rotation(1); -->\r\n' \
  '           <!-- toggle_lrotation(1); -->\r\n' \
  '        }\r\n' \
  '        let xhr = new XMLHttpRequest();\r\n' \
  '        xhr.onerror = (e) => derror_cb(e.target);\r\n' \
  '        xhr.onload = (e) => dload_cb(e.target);\r\n' \
  '        xhr.open("GET", "/3D/data");\r\n' \
  '        xhr.responseType = "arraybuffer";\r\n' \
  '        xhr.send();\r\n' \
  '      }\r\n' \
  '      data_load();\r\n' \
  '      function toggle_rotation(number=null) {\r\n' \
  '        if (c_rangle.disabled) {\r\n' \
  '          window.clearInterval(rep_rot);\r\n' \
  '          c_rangle.disabled = false;\r\n' \
  '        } else {\r\n' \
  '          c_rangle.disabled = true;\r\n' \
  '          nrot = 0;\r\n' \
  '          rep_rot = window.setInterval(function() {canvas_rotate(number);}, 100);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function toggle_lrotation(number=null) {\r\n' \
  '        if (c_lrangle.disabled) {\r\n' \
  '          window.clearInterval(rep_lrot);\r\n' \
  '          c_lrangle.disabled = false;\r\n' \
  '          c_ltangle.disabled = false;\r\n' \
  '        } else {\r\n' \
  '          c_lrangle.disabled = true;\r\n' \
  '          c_ltangle.disabled = true;\r\n' \
  '          ltangle_rotmax = parseFloat(c_ltangle.value);\r\n' \
  '          set_param("lt", 0);\r\n' \
  '          set_param("lr", (90 + parseFloat(c_rangle.value)) % 360);\r\n' \
  '          nlrot = 0;\r\n' \
  '          rep_lrot = window.setInterval(function() {canvas_lrotate(number);}, 100);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function toggle_filling(mode) {\r\n' \
  '        if (mode == fillmode) {return;};\r\n' \
  '        fillmode = mode;\r\n' \
  '        canvas_redraw();\r\n' \
  '      }\r\n' \
  '      function toggle_dimming(mode) {\r\n' \
  '        if (mode == dmode) {return;};\r\n' \
  '        dmode = mode;\r\n' \
  '        if (dmode == 3) {\r\n' \
  '          c_ltangle.disabled = false;\r\n' \
  '          c_lrangle.disabled = false;\r\n' \
  '          b_lrangle.disabled = false;\r\n' \
  '        } else {\r\n' \
  '          c_ltangle.disabled = true;\r\n' \
  '          c_lrangle.disabled = true;\r\n' \
  '          b_lrangle.disabled = true;\r\n' \
  '          if (dmode == 2) {\r\n' \
  '            set_param("lt", 35);\r\n' \
  '            set_param("lr", 315);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        canvas_redraw();\r\n' \
  '      }\r\n' \
  '    </script>\r\n' \
  '  </body>\r\n' \
  '</html>'
  HTML_3D_TEMPLATE = HTML_3D_TEMPLATE.replace('{', '{{').replace('}', '}}').replace('{{#', '{').replace('#}}', '}').format_map(LSTRINGS['interface']).replace('{{', '{').replace('}}', '}')
  HTML_3D_DECLARATIONS_TEMPLATE = \
  '      var portmin = ##PORTMIN##;\r\n' \
  '      var portmax = ##PORTMAX##;\r\n' \
  '      var zfactmax = ##ZFACTMAX##;\r\n' \
  '      var mpos = [##MPOS##];\r\n' \
  '      var tminrow = ##TMINROW##;\r\n' \
  '      var tmincol = ##TMINCOL##;\r\n' \
  '      var tmaxrow = ##TMAXROW##;\r\n' \
  '      var tmaxcol = ##TMAXCOL##;\r\n'
  HTMLExp_TEMPLATE = \
  '<!DOCTYPE html>\r\n' \
  '<html lang="fr-FR">\r\n' \
  '  <head>\r\n' \
  '    <meta charset="utf-8">\r\n' \
  '    <title>GPXExplorer</title>\r\n' \
  '    <style type="text/css">\r\n' \
  '      :root {\r\n' \
  '        --scale:1;\r\n' \
  '        --zoom:1;\r\n' \
  '        --wsp:6em;\r\n' \
  '        --filter:none;\r\n' \
  '      }\r\n' \
  '      div[id$=cont] {\r\n' \
  '        position:relative;\r\n' \
  '      }\r\n' \
  '      input {\r\n' \
  '        background-color:rgb(30,30,35);\r\n' \
  '        color:inherit;\r\n' \
  '      }\r\n' \
  '      input[type=text] {\r\n' \
  '        border-width:0.5px;\r\n' \
  '      }\r\n' \
  '      input[type=text]:focus {\r\n' \
  '        color:rgb(200,250,240);\r\n' \
  '      }\r\n' \
  '      input[type=text]:invalid {\r\n' \
  '        color:rgb(250,220,200);\r\n' \
  '      }\r\n' \
  '      input[id=tracksfilter] {\r\n' \
  '        width:calc(98vw - 60em);\r\n' \
  '        font-size:70%;\r\n' \
  '      }\r\n' \
  '      form[id^=track] {\r\n' \
  '        overflow-x:hidden;\r\n' \
  '        margin-right: 4px;\r\n' \
  '      }\r\n' \
  '      input[type=checkbox] {\r\n' \
  '        appearance:none;\r\n' \
  '        vertical-align:middle;\r\n' \
  '        margin-left:1px;\r\n' \
  '        width:1.25em;\r\n' \
  '        height:1.25em;\r\n' \
  '      }\r\n' \
  '      input[type=checkbox]:checked::before {\r\n' \
  '        content:"\\2714";\r\n' \
  '        display:inline-block;\r\n' \
  '        text-align:center;\r\n' \
  '        width:100%;\r\n' \
  '        font-weight:bold;\r\n' \
  '      }\r\n' \
  '      input[id$=visible] {\r\n' \
  '        appearance:none;\r\n' \
  '        vertical-align:middle;\r\n' \
  '        margin-left:0.3%;\r\n' \
  '        margin-right:2.2%;\r\n' \
  '        width:5.2%;\r\n' \
  '        height:1.25em;\r\n' \
  '      }\r\n' \
  '      input+label[id$=desc]:hover,input:hover+label[id$=desc] {\r\n' \
  '        background-color:green;\r\n' \
  '      }\r\n' \
  '      label[id$=desc] {\r\n' \
  '        cursor:cell;\r\n' \
  '        display:inline-block;\r\n' \
  '        vertical-align:middle;\r\n' \
  '        white-space:nowrap;\r\n' \
  '        width:92.3%;\r\n' \
  '        min-height:1.35em;\r\n' \
  '      }\r\n' \
  '      input[type=color] {\r\n' \
  '        position:absolute;\r\n' \
  '        right:0;\r\n' \
  '        top:calc(1em + 3px);\r\n' \
  '        width:1em;\r\n' \
  '        height:1em;\r\n' \
  '        border:none;\r\n' \
  '        padding:0;\r\n' \
  '      }\r\n' \
  '      input[type=color]::-webkit-color-swatch-wrapper{\r\n' \
  '        padding:0;\r\n' \
  '      }\r\n' \
  '      input[type=color]::-webkit-color-swatch {\r\n' \
  '        border:none;\r\n' \
  '      }\r\n' \
  '      input[type=color]::-moz-color-swatch {\r\n' \
  '        border:none;\r\n' \
  '      }\r\n' \
  '      label[for$=name], label[for$=file], label[for$=folder], label[for$=period], label[for$=content] {\r\n' \
  '        display:inline-block;\r\n' \
  '        width:2em;\r\n' \
  '        padding-left:0.8em;\r\n' \
  '      }\r\n' \
  '      input[id$=name], input[id$=file], input[id$=folder], input[id$=period], input[id$=content] {\r\n' \
  '        height:1.35em;\r\n' \
  '        width:80%;\r\n' \
  '        font-size:100%;\r\n' \
  '      }\r\n' \
  '      label[id$=desc]+br {\r\n' \
  '        margin-bottom: 1em;\r\n' \
  '      }\r\n' \
  '      span[id$=focus] {\r\n' \
  '        display:none;\r\n' \
  '      }\r\n' \
  '      svg[id*=dot] {\r\n' \
  '        position:absolute;\r\n' \
  '        cursor:pointer;\r\n' \
  '        stroke-width:1.5;\r\n' \
  '      }\r\n' \
  '      path {\r\n' \
  '        pointer-events:stroke;\r\n' \
  '        cursor:pointer;\r\n' \
  '        fill:none;\r\n' \
  '        vector-effect:non-scaling-stroke;\r\n' \
  '      }\r\n' \
  '      svg[id^=track] {\r\n' \
  '        position:absolute;\r\n' \
  '        pointer-events:none;\r\n' \
  '        stroke-width:1.5;\r\n' \
  '        stroke-linecap:round;\r\n' \
  '        stroke-linejoin:round;\r\n' \
  '      }\r\n' \
  '      svg[id^=track] text {\r\n' \
  '        pointer-events:none;\r\n' \
  '        font-size:calc(24px * var(--scale));\r\n' \
  '        word-spacing:var(--wsp);\r\n' \
  '        stroke:none;\r\n' \
  '        display:none;\r\n' \
  '      }\r\n' \
  '      button {\r\n' \
  '        border:none;\r\n' \
  '        padding-left:0;\r\n' \
  '        padding-right:0;\r\n' \
  '        width:1.4em;\r\n' \
  '        height:1.4em;\r\n' \
  '        background-color:rgb(30,30,35);\r\n' \
  '        color:inherit;\r\n' \
  '        line-height:1.2em;\r\n' \
  '        font-size:100%;\r\n' \
  '        cursor:pointer;\r\n' \
  '      }\r\n' \
  '      select {\r\n' \
  '        background-color:rgb(30,30,35);\r\n' \
  '        color:inherit;\r\n' \
  '        border-width:0.5px;\r\n' \
  '      }\r\n' \
  '      select:focus {\r\n' \
  '          color:rgb(200,250,240);\r\n' \
  '      }\r\n' \
  '      @-moz-document url-prefix() {\r\n' \
  '        select {\r\n' \
  '          appearance:none;\r\n' \
  '          background-image:url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" style="fill:rgb(225,225,225)"><text x="0.2em" y="0.4em" >%E2%8C%84</text></svg>\');\r\n' \
  '          background-repeat:no-repeat;\r\n' \
  '          background-position-x:right;\r\n' \
  '          background-position-y:bottom;\r\n' \
  '          background-size:2em 1em;\r\n' \
  '        }\r\n' \
  '        select:focus {\r\n' \
  '          background-image:url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" style="fill:rgb(200,250,240)"><text x="0.2em" y="0.4em" >%E2%8C%84</text></svg>\');\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      select option {\r\n' \
  '        color:rgb(225,225,225);\r\n' \
  '      }\r\n' \
  '      label[for^=folder] {\r\n' \
  '        display:inline-block;\r\n' \
  '        vertical-align:middle;\r\n' \
  '        white-space:nowrap;\r\n' \
  '      }\r\n' \
  '      label[for$=filter] {\r\n' \
  '        position:absolute;\r\n' \
  '        top:1.5em;\r\n' \
  '        text-align:center;\r\n' \
  '        font-weight:normal;\r\n' \
  '        font-size:90%;\r\n' \
  '      }\r\n' \
  '      span[id$=stren], span[id^=sl] ,span[id^=sp] {\r\n' \
  '        position:absolute;\r\n' \
  '        top:2.8em;\r\n' \
  '        width:2em;\r\n' \
  '        font-size:90%;\r\n' \
  '      }\r\n' \
  '      input[type=range] {\r\n' \
  '        position:absolute;\r\n' \
  '        top:3em;\r\n' \
  '        max-width:40vh;\r\n' \
  '        width:9em;\r\n' \
  '        margin-right:0;\r\n' \
  '        transform:rotate(-90deg);\r\n' \
  '        transform-origin:right center;\r\n' \
  '        font-size:100%;\r\n' \
  '      }\r\n' \
  '      span+span[id^=message] {\r\n' \
  '        margin-left:0.4em;\r\n' \
  '        padding-left:0.4em;\r\n' \
  '        border-left:1px rgb(225,225,225) solid;\r\n' \
  '      }\r\n' \
  '      img {\r\n' \
  '        filter:var(--filter);\r\n' \
  '      }\r\n' \
  '      svg circle {\r\n' \
  '        r:calc(3px * var(--scale));\r\n' \
  '        pointer-events:all;\r\n' \
  '      }\r\n' \
  '    </style>\r\n' \
  '    <script>\r\n' \
  '      var wmb = Math.PI * 6378137;\r\n##DECLARATIONS##\r\n' \
  '      var cleft = null;\r\n' \
  '      var cright = null;\r\n' \
  '      var ctop = null;\r\n' \
  '      var cbottom = null;\r\n' \
  '      var hpx = 0;\r\n' \
  '      var hpy = 0;\r\n' \
  '      var zoom = 1;\r\n' \
  '      if (mode == "map") {\r\n' \
  '        var zooms = ["1", "1.5", "2", "3", "4", "6", "10", "15", "25"];\r\n' \
  '        var zoom_s = "1";\r\n' \
  '      } else {\r\n' \
  '        var tset = 0;\r\n' \
  '        var tlevels = [];\r\n' \
  '        var tlevel = 0;\r\n' \
  '        var zooms = ["1/8", "1/4", "1/2", "3/4", "1", "1.5", "2", "3", "4", "6", "8"];\r\n' \
  '        var tlock = false;\r\n' \
  '        var zoom_s = "1";\r\n' \
  '      }\r\n' \
  '      var eset = 0;\r\n' \
  '      var iset = 0;\r\n' \
  '      var dots_visible = false;\r\n' \
  '      var focused = "";\r\n' \
  '      var date_conv = new Intl.DateTimeFormat("default",{year: "numeric", month:"2-digit", day:"2-digit"});\r\n' \
  '      var time_conv = new Intl.DateTimeFormat("default",{hour12:false, hour: "2-digit", minute:"2-digit", second:"2-digit"});\r\n' \
'        var str_comp = new Intl.Collator().compare;\r\n' \
  '      var tracks_pts = [];\r\n' \
  '      var tracks_stats = [];\r\n' \
  '      var tracks_props = [];\r\n' \
  '      var msg_n = 0;\r\n' \
  '      class GPUStats {\r\n' \
  '        static get tw() {return 1024;}\r\n' \
  '        constructor () {\r\n' \
  '          this.canvas = document.createElement("canvas");\r\n' \
  '          this.gl = this.canvas.getContext("webgl2", {preserveDrawingBuffer: true});\r\n' \
  '          this.gl_programs = new Map();\r\n' \
  '          this.cur_prog = null;\r\n' \
  '          this.gl_attributes = new Map([["vstart", ["int", 1]]]);\r\n' \
  '          this.gl_static_uniforms = new Map([["llhtex", "sampler2D"], ["teatex", "sampler2D"], ["dtex", "sampler2D"], ["ssstex", "sampler2D"], ["trange", "float"], ["spmax", "float"], ["drange", "float"], ["slmax", "float"]]);\r\n' \
  '          this.gl_dynamic_uniforms = new Map([["trlat", "float"], ["rlat", "float"], ["vlength", "int"]]);\r\n' \
  '          this.gl_feedbacks = new Map([["vxy", "vec2"], ["vd", "float"], ["vsss", "vec3"]]);\r\n' \
  '          this._starts = null;\r\n' \
  '          this.tlength = null;\r\n' \
  '          this._rlats = null;\r\n' \
  '          this._llhs = null;\r\n' \
  '          this._teas = null;\r\n' \
  '          this.vstart = null;\r\n' \
  '          this.llhtex = 0;\r\n' \
  '          this.teatex = 1;\r\n' \
  '          this.dtex = 2;\r\n' \
  '          this.ssstex = 3;\r\n' \
  '          this.llh_texture = null;\r\n' \
  '          this.tea_texture = null;\r\n' \
  '          this.d_texture = null;\r\n' \
  '          this.sss_texture = null;\r\n' \
  '          this.trlat = null;\r\n' \
  '          this.rlat = null;\r\n' \
  '          this.vlength = 0;\r\n' \
  '          this.trange = 300 / 2;\r\n' \
  '          this.spmax = 8 / 3.6;\r\n' \
  '          this.drange = 500 / 2;\r\n' \
  '          this.slmax = 50 / 100;\r\n' \
  '          this.vxy = null;\r\n' \
  '          this.vd = null;\r\n' \
  '          this.vsss = null;\r\n' \
  '          this._xys = null;\r\n' \
  '          this._ds = null;\r\n' \
  '          this._ssss = null;\r\n' \
  '          this.gl.enable(this.gl.RASTERIZER_DISCARD);\r\n' \
  '          let vertex_pshader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform float trlat;\r\n' \
  '            uniform sampler2D llhtex;\r\n' \
  '            out vec2 vxy;\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec2 ll = texelFetch(llhtex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).st * vec2(0.00872664626, 0.00872664626);\r\n' \
  '              float t = ll.s + pow(ll.s, 3.0) / 3.0;\r\n' \
  '              vxy = vec2(ll.t * 12756274.0, log((1.0 + t * trlat) / (1.0 - t / trlat)) * 6378137.0);\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let vertex_dshader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform float rlat;\r\n' \
  '            uniform sampler2D llhtex;\r\n' \
  '            out float vd;\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec3 llhe = texelFetch(llhtex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).stp * vec3(0.00872664626, 0.00872664626, 1.0);\r\n' \
  '              vec3 llhs = gl_InstanceID > 0 ? texelFetch(llhtex, ivec2((pc - 1) % ${GPUStats.tw}, (pc - 1) / ${GPUStats.tw}), 0).stp * vec3(0.00872664626, 0.00872664626, 1.0) : llhe.stp;\r\n' \
  '              vec3 dll = llhe - llhs;\r\n' \
  '              float a = sqrt(pow(dll.s, 2.0) - pow(dll.s, 4.0) / 3.0 + cos(rlat - llhs.s * 2.0) * cos(rlat - llhe.s * 2.0) * (pow(dll.t, 2.0) - pow(dll.t, 4.0) / 3.0));\r\n' \
  '              vd = sqrt(pow(12756274.0 * (a + pow(a, 3.0) / 6.0), 2.0) + pow(llhe.p - llhs.p, 2.0));\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let vertex_s1shader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform sampler2D teatex;\r\n' \
  '            uniform sampler2D dtex;\r\n' \
  '            uniform int vlength;\r\n' \
  '            uniform float trange;\r\n' \
  '            uniform float spmax;\r\n' \
  '            uniform float drange;\r\n' \
  '            uniform float slmax;\r\n' \
  '            out vec3 vsss;\r\n' \
  '            vec2 slope(float d, vec2 h) {\r\n' \
  '              return mix(slmax * sign(h), h / sqrt(d * d - h * h), lessThan(abs(h), vec2(d)));\r\n' \
  '            }\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec4 tdeas;\r\n' \
  '              tdeas.spq = texelFetch(teatex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).stp;\r\n' \
  '              tdeas.t = texelFetch(dtex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).s;\r\n' \
  '              vec2 tde = tdeas.st;\r\n' \
  '              vec2 tdp = tde;\r\n' \
  '              vsss = vec3(0.0);\r\n' \
  '              for (int p = pc + 1; p < vstart + vlength; p++) {\r\n' \
  '                tde = vec2(texelFetch(teatex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s, texelFetch(dtex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s + tde.t);\r\n' \
  '                if (tde.s > tdeas.s + trange) {break;}\r\n' \
  '                if (tde.s == tdeas.s) {continue;}\r\n' \
  '                vsss.s += (tde.t - tdeas.t) / (tde.s - tdeas.s) * (tde.s - tdp.s);\r\n' \
  '                tdp = tde;\r\n' \
  '              }\r\n' \
  '              if (tdp.s != tdeas.s) {\r\n' \
  '                vsss.s = (vsss.s + (tdp.t - tdeas.t) / (tdp.s - tdeas.s) * (trange + tdeas.s - tdp.s)) / trange;\r\n' \
  '              }\r\n' \
  '              vsss.s = min(vsss.s, spmax);\r\n' \
  '              vec3 deae = tdeas.tpq;\r\n' \
  '              vec3 deap = deae;\r\n' \
  '              for (int p = pc + 1; p < vstart + vlength; p++) {\r\n' \
  '                deae = vec3(texelFetch(dtex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s + deae.s, texelFetch(teatex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).tp);\r\n' \
  '                if (deae.s > tdeas.t + drange) {break;}\r\n' \
  '                if (deae.s == tdeas.t) {continue;}\r\n' \
  '                vsss.tp += slope(deae.s - tdeas.t, deae.tp - tdeas.pq) * (deae.s - deap.s);\r\n' \
  '                deap = deae;\r\n' \
  '              }\r\n' \
  '              if (deap.s != tdeas.t) {\r\n' \
  '                vsss.tp = (vsss.tp + slope(deap.s - tdeas.t, deap.tp - tdeas.pq) * (drange + tdeas.t - deap.s)) / drange;\r\n' \
  '              }\r\n' \
  '              vsss.tp = clamp(vsss.tp, vec2(-slmax), vec2(slmax));\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let vertex_s2shader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform sampler2D teatex;\r\n' \
  '            uniform sampler2D dtex;\r\n' \
  '            uniform sampler2D ssstex;\r\n' \
  '            uniform int vlength;\r\n' \
  '            uniform float trange;\r\n' \
  '            uniform float spmax;\r\n' \
  '            uniform float drange;\r\n' \
  '            uniform float slmax;\r\n' \
  '            out vec3 vsss;\r\n' \
  '            void main() {\r\n' \
  '              vsss = vec3(0.0);\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec2 tsc = vec2(texelFetch(teatex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).s, texelFetch(ssstex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).s);\r\n' \
  '              vec2 tsf = tsc;\r\n' \
  '              vec2 tsn = tsc;\r\n' \
  '              vsss.s = tsc.t;\r\n' \
  '              float c;\r\n' \
  '              float su = 0.0;\r\n' \
  '              float s = 0.0;\r\n' \
  '              if (texelFetch(teatex, ivec2((pc + 1) % ${GPUStats.tw}, (pc + 1) / ${GPUStats.tw}), 0).s - tsc.s <= trange) {\r\n' \
  '                for (int p = pc - 1; p >= vstart; p--) {\r\n' \
  '                  tsf = vec2(texelFetch(teatex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s, texelFetch(ssstex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s);\r\n' \
  '                  if (tsf.s < tsc.s - trange) {break;}\r\n' \
  '                  c = (tsn.s - tsf.s) / (tsc.s - tsf.s + 1.0);\r\n' \
  '                  s += tsf.t * c;\r\n' \
  '                  su += c;\r\n' \
  '                  tsn = tsf;\r\n' \
  '                }\r\n' \
  '                if (tsc.s != tsn.s) {\r\n' \
  '                  vsss.s = min((vsss.s + s / 2.0) / (1.0 + su / 2.0), spmax);\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              vec3 dssc = vec3(texelFetch(dtex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).s, texelFetch(ssstex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).tp);\r\n' \
  '              vec3 dssf = dssc;\r\n' \
  '              vec3 dssn = dssc;\r\n' \
  '              vsss.tp = dssc.tp;\r\n' \
  '              su = 0.0;\r\n' \
  '              vec2 ss = vec2(0.0);\r\n' \
  '              if (texelFetch(dtex, ivec2((pc + 1) % ${GPUStats.tw}, (pc + 1) / ${GPUStats.tw}), 0).s <= drange) {\r\n' \
  '                for (int p = pc - 1; p >= vstart; p--) {\r\n' \
  '                  dssf = vec3(dssf.s - texelFetch(dtex, ivec2((p + 1) % ${GPUStats.tw}, (p + 1) / ${GPUStats.tw}), 0).s, texelFetch(ssstex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).tp);\r\n' \
  '                  if (dssf.s < dssc.s - drange) {break;}\r\n' \
  '                  c = (dssn.s - dssf.s) / (dssc.s - dssf.s + 1.0);\r\n' \
  '                  ss += dssf.tp * c;\r\n' \
  '                  su += c;\r\n' \
  '                  dssn = dssf;\r\n' \
  '                }\r\n' \
  '                if (dssc.s != dssn.s) {\r\n' \
  '                  vsss.tp = clamp((vsss.tp + ss / 2.0) / (1.0 + su / 2.0), vec2(-slmax), vec2(slmax));\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let fragment_shader_s = `#version 300 es\r\n' \
  '            precision highp float;\r\n' \
  '            void main() {\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          this.program_create("pprogram", vertex_pshader_s, fragment_shader_s);\r\n' \
  '          this.program_create("dprogram", vertex_dshader_s, fragment_shader_s);\r\n' \
  '          this.program_create("s1program", vertex_s1shader_s, fragment_shader_s);\r\n' \
  '          this.program_create("s2program", vertex_s2shader_s, fragment_shader_s);\r\n' \
  '        }\r\n' \
  '        program_create(name, vshader_s, fshader_s) {\r\n' \
  '          let vertex_shader = this.gl.createShader(this.gl.VERTEX_SHADER);\r\n' \
  '          this.gl.shaderSource(vertex_shader, vshader_s);\r\n' \
  '          this.gl.compileShader(vertex_shader);\r\n' \
  '          let fragment_shader = this.gl.createShader(this.gl.FRAGMENT_SHADER);\r\n' \
  '          this.gl.shaderSource(fragment_shader, fshader_s);\r\n' \
  '          this.gl.compileShader(fragment_shader);\r\n' \
  '          let prog = this.gl.createProgram();\r\n' \
  '          this.gl.attachShader(prog, vertex_shader);\r\n' \
  '          this.gl.attachShader(prog, fragment_shader);\r\n' \
  '          this.gl_programs.set(name, new Map());\r\n' \
  '          this.gl_programs.get(name).set("program", prog);\r\n' \
  '          let f = [];\r\n' \
  '          for (let [n, t] of this.gl_feedbacks) {\r\n' \
  '            if (vshader_s.indexOf("out " + t + " " + n) >= 0) {\r\n' \
  '              this.gl_programs.get(name).set(n, f.length);\r\n' \
  '              f.push(n);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (f.length > 0) {\r\n' \
  '            this.gl.transformFeedbackVaryings(prog, f, this.gl.SEPARATE_ATTRIBS);\r\n' \
  '          }\r\n' \
  '          this.gl.linkProgram(prog);\r\n' \
  '          this.gl_programs.get(name).set("vao", this.gl.createVertexArray());\r\n' \
  '          if (f.length > 0) {\r\n' \
  '            this.gl_programs.get(name).set("tf", this.gl.createTransformFeedback());\r\n' \
  '          }\r\n' \
  '          for (let [n, ts] of this.gl_attributes) {\r\n' \
  '            if (vshader_s.indexOf("in " + ts[0] + " " + n) >= 0) {\r\n' \
  '              this.gl_programs.get(name).set(n, this.gl.getAttribLocation(prog, n));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          for (let [n, t] of [...this.gl_static_uniforms.entries(), ...this.gl_dynamic_uniforms.entries()]) {\r\n' \
  '            if (vshader_s.indexOf("uniform " + t + " " + n) >= 0 || fshader_s.indexOf("uniform " + t + " " + n) >= 0) {\r\n' \
  '              this.gl_programs.get(name).set(n, this.gl.getUniformLocation(prog, n));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        program_use(name) {\r\n' \
  '          this.cur_prog = name;\r\n' \
  '          this.gl.useProgram(this.gl_programs.get(name).get("program"));\r\n' \
  '          this.gl.bindVertexArray(this.gl_programs.get(name).get("vao"));\r\n' \
  '          this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, this.gl_programs.get(name).get("tf"));\r\n' \
  '        }\r\n' \
  '        program_attributes() {\r\n' \
  '          for (let [n, ts] of this.gl_attributes) {\r\n' \
  '            if (this.gl_programs.get(this.cur_prog).has(n)) {\r\n' \
  '              this.gl.enableVertexAttribArray(this.gl_programs.get(this.cur_prog).get(n));\r\n' \
  '              this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this[n]);\r\n' \
  '              if (ts[0] == "int") {\r\n' \
  '                this.gl.vertexAttribIPointer(this.gl_programs.get(this.cur_prog).get(n), ts[1], this.gl.INT, false, 0, 0);\r\n' \
  '              } else {\r\n' \
  '                this.gl.vertexAttribPointer(this.gl_programs.get(this.cur_prog).get(n), ts[1], this.gl.FLOAT, false, 0, 0);\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          this.gl.bindBuffer(this.gl.ARRAY_BUFFER, null);\r\n' \
  '        }\r\n' \
  '        program_uniforms(type="dynamic") {\r\n' \
  '          for (let [n, t] of type=="static"?this.gl_static_uniforms:this.gl_dynamic_uniforms) {\r\n' \
  '            if (this.gl_programs.get(this.cur_prog).has(n)) {\r\n' \
  '              switch (t) {\r\n' \
  '                case "float":\r\n' \
  '                  this.gl.uniform1f(this.gl_programs.get(this.cur_prog).get(n), this[n]);\r\n' \
  '                  break;\r\n' \
  '                case "sampler2D":\r\n' \
  '                case "int":\r\n' \
  '                  this.gl.uniform1i(this.gl_programs.get(this.cur_prog).get(n), this[n]);\r\n' \
  '                  break;\r\n' \
  '                default:\r\n' \
  '                  this.gl.uniform1f(this.gl_programs.get(this.cur_prog).get(n), this[n]);\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        program_feedbacks(offset, size) {\r\n' \
  '          for (let [n, t] of this.gl_feedbacks) {\r\n' \
  '            if (this.gl_programs.get(this.cur_prog).has(n)) {\r\n' \
  '              let s = 0;\r\n' \
  '              switch (t) {\r\n' \
  '                case "float":\r\n' \
  '                  s = 4;\r\n' \
  '                  break;\r\n' \
  '                case "vec2":\r\n' \
  '                  s = 8;\r\n' \
  '                  break;\r\n' \
  '                case "vec3":\r\n' \
  '                  s = 12;\r\n' \
  '                  break;\r\n' \
  '                default:\r\n' \
  '                  s = 4;\r\n' \
  '              }\r\n' \
  '              this.gl.bindBufferRange(this.gl.TRANSFORM_FEEDBACK_BUFFER, this.gl_programs.get(this.cur_prog).get(n), this[n], offset * s, size * s);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        static pad(s) {\r\n' \
  '          return (Math.floor((s - 1) / GPUStats.tw) + 1) * GPUStats.tw;\r\n' \
  '        }\r\n' \
  '        texture_load(unit, ncomp, src, tex=null) {\r\n' \
  '          let gl_texture = tex;\r\n' \
  '          if (tex == null) {gl_texture = this.gl.createTexture();}\r\n' \
  '          this.gl.activeTexture(unit);\r\n' \
  '          this.gl.bindTexture(this.gl.TEXTURE_2D, gl_texture);\r\n' \
  '          this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_WRAP_S, this.gl.CLAMP_TO_EDGE);\r\n' \
  '          this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_WRAP_T, this.gl.CLAMP_TO_EDGE);\r\n' \
  '          this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_MIN_FILTER, this.gl.NEAREST);\r\n' \
  '          this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_MAG_FILTER, this.gl.NEAREST);\r\n' \
  '          if (Array.isArray(src)) {\r\n' \
  '            this.gl.texImage2D(this.gl.TEXTURE_2D, 0, [this.gl.R32F, this.gl.RG32F, this.gl.RGB32F, this.gl.RGBA32F][ncomp - 1], GPUStats.tw, src.length / ncomp / GPUStats.tw, 0, [this.gl.R, this.gl.RG, this.gl.RGB, this.gl.RGBA] [ncomp - 1], this.gl.FLOAT, new Float32Array(src));\r\n' \
  '          } else if (src instanceof Float32Array) {\r\n' \
  '            this.gl.texImage2D(this.gl.TEXTURE_2D, 0, [this.gl.R32F, this.gl.RG32F, this.gl.RGB32F, this.gl.RGBA32F][ncomp - 1], GPUStats.tw, src.length / ncomp / GPUStats.tw, 0, [this.gl.R, this.gl.RG, this.gl.RGB, this.gl.RGBA] [ncomp - 1], this.gl.FLOAT, src);\r\n' \
  '          } else if (src instanceof WebGLBuffer) {\r\n' \
  '            this.gl.bindBuffer(this.gl.PIXEL_UNPACK_BUFFER, src);\r\n' \
  '            this.gl.texImage2D(this.gl.TEXTURE_2D, 0, [this.gl.R32F, this.gl.RG32F, this.gl.RGB32F, this.gl.RGBA32F][ncomp - 1], GPUStats.tw, this.gl.getBufferParameter(this.gl.PIXEL_UNPACK_BUFFER, this.gl.BUFFER_SIZE) / ncomp / 4 / GPUStats.tw, 0, [this.gl.RED, this.gl.RG, this.gl.RGB, this.gl.RGBA] [ncomp - 1], this.gl.FLOAT, 0);\r\n' \
  '            this.gl.bindBuffer(this.gl.PIXEL_UNPACK_BUFFER, null);\r\n' \
  '          } else {\r\n' \
  '            this.gl.texImage2D(this.gl.TEXTURE_2D, 0, [this.gl.R32F, this.gl.RG32F, this.gl.RGB32F, this.gl.RGBA32F][ncomp - 1], GPUStats.tw, src / GPUStats.tw, 0, [this.gl.RED, this.gl.RG, this.gl.RGB, this.gl.RGBA] [ncomp - 1], this.gl.FLOAT, 0);\r\n' \
  '          }\r\n' \
  '          return gl_texture;\r\n' \
  '        }\r\n' \
  '        buffer_load(src, use, buf=null) {\r\n' \
  '          let gl_buffer = buf;\r\n' \
  '          if (buf == null) {gl_buffer = this.gl.createBuffer();}\r\n' \
  '          this.gl.bindBuffer(this.gl.ARRAY_BUFFER, gl_buffer);\r\n' \
  '          this.gl.bufferData(this.gl.ARRAY_BUFFER, src, use);\r\n' \
  '          this.gl.bindBuffer(this.gl.ARRAY_BUFFER, null);\r\n' \
  '          return gl_buffer;\r\n' \
  '        }\r\n' \
  '        set starts(a) {\r\n' \
  '          this._starts = a;\r\n' \
  '          this.tlength = this._starts[this._starts.length - 1];\r\n' \
  '          this.vstart = this.buffer_load(new Int32Array(this._starts), this.gl.STATIC_DRAW, this.vstart);\r\n' \
  '        }\r\n' \
  '        get starts() {\r\n' \
  '          return this._starts;\r\n' \
  '        }\r\n' \
  '        set rlats(a) {\r\n' \
  '          this._rlats = a.map(function (tl) {return tl[0] * Math.PI / 180});\r\n' \
  '        }\r\n' \
  '        set llhs(a) {\r\n' \
  '          this._llhs = a;\r\n' \
  '          this.llh_texture = this.texture_load(this.gl.TEXTURE0 + this.llhtex, 3, this._llhs, this.llh_texture);\r\n' \
  '          this.vxy = this.buffer_load(2 * 4 * GPUStats.pad(this.tlength), this.gl.STREAM_READ, this.vxy);\r\n' \
  '          this.vd = this.buffer_load(4 * GPUStats.pad(this.tlength), this.gl.STREAM_READ, this.vd);\r\n' \
  '         }\r\n' \
  '        set teas(a) {\r\n' \
  '          this._teas = a;\r\n' \
  '          this.tea_texture = this.texture_load(this.gl.TEXTURE0 + this.teatex, 3, this._teas, this.tea_texture);\r\n' \
  '          this.vsss = this.buffer_load(3 * 4 * GPUStats.pad(this.tlength), this.gl.STREAM_READ, this.vsss);\r\n' \
  '        }\r\n' \
  '        _calc() {\r\n' \
  '          for (let s=0; s<this._starts.length-1; s++) {\r\n' \
  '            this.vlength = this._starts[s + 1] - this._starts[s];\r\n' \
  '            if (this.vlength == 0) {continue;}\r\n' \
  '            if (this.cur_prog == "pprogram")  {this.trlat = Math.tan(this._rlats[s] / 2 + Math.PI / 4);}\r\n' \
  '            if (this.cur_prog == "dprogram") {this.rlat = this._rlats[s];}\r\n' \
  '            this.program_uniforms();\r\n' \
  '            this.program_feedbacks(this._starts[s], this.vlength);\r\n' \
  '            this.gl.beginTransformFeedback(this.gl.POINTS);\r\n' \
  '            this.gl.drawArraysInstanced(this.gl.POINTS, s, 1, this.vlength - (this.cur_prog=="s2program"?1:0));\r\n' \
  '            this.gl.endTransformFeedback();\r\n' \
  '            this.gl.finish();\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        calc(pos=true) {\r\n' \
  '          for (let n of this.gl_programs.keys()) {\r\n' \
  '            this.program_use(n);\r\n' \
  '            this.program_attributes();\r\n' \
  '            this.program_uniforms("static");\r\n' \
  '          }\r\n' \
  '          if (pos) {\r\n' \
  '            this.program_use("pprogram");\r\n' \
  '            this._calc();\r\n' \
  '            this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, null);\r\n' \
  '            this.feedbacks();\r\n' \
  '            this.program_use("dprogram");\r\n' \
  '            this._calc();\r\n' \
  '            this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, null);\r\n' \
  '            this.d_texture = this.texture_load(this.gl.TEXTURE0 + this.dtex, 1, this.vd, this.d_texture);\r\n' \
  '          this.feedbacks();\r\n' \
  '          }\r\n' \
  '          this.program_use("s1program");\r\n' \
  '          this._calc();\r\n' \
  '          this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, null);\r\n' \
  '          this.sss_texture = this.texture_load(this.gl.TEXTURE0 + this.ssstex, 3, this.vsss, this.sss_texture);\r\n' \
  '          this.program_use("s2program");\r\n' \
  '          this._calc();\r\n' \
  '          this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, null);\r\n' \
  '          this.feedbacks();\r\n' \
  '        }\r\n' \
  '        feedbacks() {\r\n' \
  '          for (let [n, t] of this.gl_feedbacks) {\r\n' \
  '            if (this.gl_programs.get(this.cur_prog).has(n)) {\r\n' \
  '              switch (t) {\r\n' \
  '                case "float":\r\n' \
  '                  this[n.replace("v", "_") + "s"] = new Float32Array(this.tlength);\r\n' \
  '                  break;\r\n' \
'                case "vec2":\r\n' \
  '                  this[n.replace("v", "_") + "s"] = new Float32Array(2 * this.tlength);\r\n' \
  '                  break;\r\n' \
  '                case "vec3":\r\n' \
  '                  this[n.replace("v", "_") + "s"] = new Float32Array(3 * this.tlength);\r\n' \
  '                  break;\r\n' \
  '                default:\r\n' \
  '                  this[n.replace("v", "_") + "s"] = new Float32Array(this.tlength);\r\n' \
  '              }\r\n' \
  '              this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this[n]) ;\r\n' \
  '              this.gl.getBufferSubData(this.gl.ARRAY_BUFFER, 0, this[n.replace("v", "_") + "s"], 0, this[n.replace("v", "_") + "s"].length);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          this.gl.bindBuffer(this.gl.ARRAY_BUFFER, null) ;\r\n' \
  '        }\r\n' \
  '        get xys() {\r\n' \
  '          return this._xys;\r\n' \
  '        }\r\n' \
  '        get ds() {\r\n' \
  '          return this._ds;\r\n' \
  '        }\r\n' \
  '        get ssss() {\r\n' \
  '          return this._ssss;\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      if (gpucomp > 0) {var gpustats = new GPUStats();}\r\n' \
  '      function show_msg(msg, dur, msgn=null) {\r\n' \
  '        let m = null;\r\n' \
  '        if (msgn == null) {\r\n' \
  '          msgn = ++msg_n;\r\n' \
  '          m = document.createElement("span");\r\n' \
  '          m.id = "message" + msgn.toString();\r\n' \
  '        } else {\r\n' \
  '          m = document.getElementById("message" + msgn.toString());\r\n' \
  '        }\r\n' \
  '        m.innerHTML = msg;\r\n' \
  '        document.getElementById("message").insertBefore(m, document.getElementById("message").firstElementChild);\r\n' \
  '        if (dur) {setTimeout(function() {document.getElementById("message").removeChild(m);}, dur * 1000);}\r\n' \
  '        return msgn;\r\n' \
  '      }\r\n' \
  '      function load_tcb(t, nset, nlevel, kzoom=false) {\r\n' \
  '        if (t.status != 200) {\r\n' \
  '          document.getElementById("tset").selectedIndex = tset;\r\n' \
  '          if (nset == null) {\r\n' \
  '            window.stop();\r\n' \
  '            tlevel = nlevel;\r\n' \
  '            if (! kzoom) {zoom_s = tlevels[tlevel][1];}\r\n' \
  '            cleft = null;\r\n' \
  '            rescale();\r\n' \
  '          }\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        window.stop();\r\n' \
  '        let msg = JSON.parse(t.response);\r\n' \
  '        if (nset == null) {\r\n' \
  '          if (nlevel == null) {\r\n' \
  '            if (tlock) {switch_tlock(false);}\r\n' \
  '            tlevel = msg.level;\r\n' \
  '          } else {\r\n' \
  '            tlevel = nlevel;\r\n' \
  '          }\r\n' \
  '          if (! kzoom || nlevel == null) {zoom_s = tlevels[tlevel][1];}\r\n' \
  '          ttopx = msg.topx;\r\n' \
  '          ttopy = msg.topy;\r\n' \
  '          twidth = msg.width;\r\n' \
  '          theight = msg.height\r\n' \
  '          text = msg.ext;\r\n' \
  '          let tscale_ex = tscale;\r\n' \
  '          tscale = msg.scale;\r\n' \
  '          cleft = null;\r\n' \
  '          rescale(tscale_ex);\r\n' \
  '          if (nlevel == null) {scroll_to_all();}\r\n' \
  '        } else {\r\n' \
  '          tset = document.getElementById("tset").selectedIndex;\r\n' \
  '          let matrix = null;\r\n' \
  '          let lf = false;\r\n' \
  '          if (nlevel >= 0) {\r\n' \
  '            tlevels = msg.tlevels;\r\n' \
  '            if (nlevel == 0) {\r\n' \
  '              nlevel = tlevels[0];\r\n' \
  '              zoom_s = tlevels[nlevel][1];\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            nlevel = tlevels[0];\r\n' \
  '            matrix = tlevels[tlevel][0];\r\n' \
  '            tlevels = msg.tlevels;\r\n' \
  '            for (let i=1; i<tlevels.length; i++) {\r\n' \
  '              if (tlevels[i][0] <= matrix) {nlevel = i;}\r\n' \
  '              if (tlevels[i][0] == matrix) {\r\n' \
  '                lf = true;\r\n' \
  '                break;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            if (! lf) {\r\n' \
  '              let zoom_t = Math.pow(2, matrix - tlevels[nlevel][0]) * zoom;\r\n' \
  '              zoom_s = zooms[0];\r\n' \
  '              let i = 0;\r\n' \
  '              while (i < zooms.length) {\r\n' \
  '                if (eval(zooms[i]) <= zoom_t) {zoom_s = zooms[i]}\r\n' \
  '                if (eval(zooms[i]) >= zoom_t) {break;}\r\n' \
  '                i ++;\r\n' \
  '              }\r\n' \
  '              matrix = tlevels[nlevel][0];\r\n' \
  '              for (let i=1; i<tlevels.length; i++) {\r\n' \
  '                if (tlevels[i][0] == matrix) {\r\n' \
  '                  nlevel = i;\r\n' \
  '                  break;\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              for (let i=nlevel; i<tlevels.length; i++) {\r\n' \
  '                if (tlevels[i][0] != matrix) {break;}\r\n' \
  '                if (eval(tlevels[i][1]) <= zoom_t) {nlevel = i;}\r\n' \
  '              }\r\n' \
  '              if (! tlock) {switch_tlock(false);}\r\n' \
  '            } else  {\r\n' \
  '              let zf = false;\r\n' \
  '              for (let i=1; i<tlevels.length; i++) {\r\n' \
  '                if (tlevels[i][0] == matrix && eval(tlevels[i][1]) <= eval(zoom_s)) {nlevel = i;}\r\n' \
  '                if (tlevels[i][0] == matrix && tlevels[i][1] == zoom_s) {\r\n' \
  '                  zf = true;\r\n' \
  '                  break;\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              if (! tlock && ! zf) {switch_tlock(false);}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          switch_tiles(null, nlevel, true);\r\n' \
  '        }\r\n' \
  '      } \r\n' \
  '      function error_tcb() {\r\n' \
  '        document.getElementById("tset").selectedIndex = tset;\r\n' \
  '      } \r\n' \
  '      function switch_tiles(nset, nlevel, kzoom=false) {\r\n' \
  '        let q = "";\r\n' \
  '        if (nset != null) {\r\n' \
  '          q = "set=" + encodeURIComponent(nset);\r\n' \
  '        } else if (nlevel != null) {\r\n' \
  '          q = "matrix=" + encodeURIComponent(tlevels[nlevel][0].toString());\r\n' \
  '        } else {\r\n' \
  '          let b = track_boundaries();\r\n' \
  '          if (b == null) {\r\n' \
  '            nlevel = tlevels[0];\r\n' \
  '            q = "matrix=" + encodeURIComponent(tlevels[nlevel][0].toString());\r\n' \
  '          } else {\r\n' \
  '            q = "auto=" + encodeURIComponent(((b[1] - b[0]) / viewpane.offsetWidth).toString() + "|" + ((b[3] - b[2]) / viewpane.offsetHeight).toString());\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        xhrt.onload = (e) => {load_tcb(e.target, nset, nlevel, kzoom)};\r\n' \
  '        xhrt.open("GET", "/tiles/switch?" + q);\r\n' \
  '        xhrt.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhrt.send();\r\n' \
  '      }\r\n' \
  '      function add_tile(row=0, col=0) {\r\n' \
  '        let tile = document.createElement("img");\r\n' \
  '        if (mode == "map") {\r\n' \
  '          tile.id = "map";\r\n' \
  '          tile.src = "/map/" + tile.id + text;\r\n' \
  '        } else {\r\n' \
  '          tile.id = "tile-" + row.toString() + "-" + col.toString();\r\n' \
  '          let port = portmin + (row + col) % (portmax + 1 - portmin);\r\n' \
  '          tile.src = "http://" + location.hostname + ":" + port.toString() + "/tiles/" + tile.id + text + "?" + document.getElementById("tset").selectedIndex.toString() + "," + document.getElementById("matrix").innerHTML;\r\n' \
  '        }\r\n' \
  '        tile.alt = "";\r\n' \
  '        tile.style.position = "absolute";\r\n' \
  '        tile.style.width = "calc(var(--zoom) * " + twidth.toString() + "px)";\r\n' \
  '        tile.style.height = "calc(var(--zoom) * " + theight.toString() + "px)";\r\n' \
  '        tile.style.left = "calc(var(--zoom) * " + ((ttopx - htopx) / tscale + col * twidth).toString() + "px)";\r\n' \
  '        tile.style.top = "calc(var(--zoom) * " + ((htopy - ttopy) / tscale + row * theight).toString() + "px";\r\n' \
  '        handle.insertBefore(tile, handle.firstElementChild);\r\n' \
  '      }\r\n' \
  '      function update_tiles() {\r\n' \
  '        if (mode == "map") {return;}\r\n' \
  '        let vleft = -hpx / zoom + (htopx - ttopx) / tscale;\r\n' \
  '        let vtop = -hpy / zoom + (ttopy - htopy) / tscale;\r\n' \
  '        let vright = vleft + viewpane.offsetWidth / zoom;\r\n' \
  '        let vbottom = vtop + viewpane.offsetHeight / zoom;\r\n' \
  '        let tiles = handle.getElementsByTagName("img");\r\n' \
  '        let rleft = parseInt(vleft / twidth - 1.5);\r\n' \
  '        let rright = parseInt(vright / twidth + 1.5);\r\n' \
  '        let rtop = parseInt(vtop / theight - 1.5);\r\n' \
  '        let rbottom = parseInt(vbottom / theight + 1.5);\r\n' \
  '        if (cleft == null) {\r\n' \
  '          let i = tiles.length - 1;\r\n' \
  '            while (i >= 0) {\r\n' \
  '              handle.removeChild(tiles[i]);\r\n' \
  '              i--;\r\n' \
  '            } \r\n' \
  '          cleft = rleft - 1;\r\n' \
  '          cright = rleft - 1;\r\n' \
  '          ctop = rtop - 1;\r\n' \
  '          cbottom = rtop - 1;\r\n' \
  '        }\r\n' \
  '        let i = tiles.length - 1;\r\n' \
  '        if (rleft != cleft || rright != cright || rtop != ctop || rbottom != cbottom) {\r\n' \
  '          while (i >= 0) {\r\n' \
  '            let [r, c] = tiles[i].id.split("-").slice(1, 3);\r\n' \
  '            let row = parseInt(r);\r\n' \
  '            let col = parseInt(c);\r\n' \
  '            if (row < rtop || row > rbottom || col < rleft || col > rright) {\r\n' \
  '              handle.removeChild(tiles[i]);\r\n' \
  '            }\r\n' \
  '            i--;\r\n' \
  '          } \r\n' \
  '          for (let col=rleft; col<cleft; col++) {\r\n' \
  '            for (let row=Math.max(ctop, rtop); row<=Math.min(cbottom, rbottom); row++) {add_tile(row, col);}\r\n' \
  '          }\r\n' \
  '          for (let col=cright+1; col<=rright; col++) {\r\n' \
  '            for (let row=Math.max(ctop, rtop); row<=Math.min(cbottom, rbottom); row++) {add_tile(row, col);}\r\n' \
  '          }\r\n' \
  '          cleft = rleft;\r\n' \
  '          cright = rright;\r\n' \
  '          for (let row=rtop; row<ctop; row++) {\r\n' \
  '            for (let col=cleft; col<=cright; col++) {add_tile(row, col);}\r\n' \
  '          }\r\n' \
  '          for (let row=cbottom + 1; row<=rbottom; row++) {\r\n' \
  '            for (let col=cleft; col<=cright; col++) {add_tile(row, col);}\r\n' \
  '          }\r\n' \
  '          ctop = rtop;\r\n' \
  '          cbottom = rbottom;\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function reframe() {\r\n' \
  '        hpx = Math.round(Math.min(Math.max(hpx, (htopx - vmaxx) * zoom / tscale + viewpane.offsetWidth), (htopx - vminx) * zoom / tscale));\r\n' \
  '        hpy = Math.round(Math.min(Math.max(hpy, (vminy - htopy) * zoom / tscale + viewpane.offsetHeight), (vmaxy - htopy) * zoom / tscale));\r\n' \
  '        handle.style.left = hpx.toString() + "px";\r\n' \
  '        handle.style.top = hpy.toString() + "px";\r\n' \
  '        let k = Math.cosh((htopy + (hpy - viewpane.offsetHeight) * tscale / zoom) / 6378137);\r\n' \
  '        let sc = 150 * tscale / zoom / k;\r\n' \
  '        let unit = "m";\r\n' \
  '        let b = 1;\r\n' \
  '        if (sc >= 1000) {\r\n' \
  '          unit = "km";\r\n' \
  '          b = 1000;\r\n' \
  '        } else if (sc < 0.1) {\r\n' \
  '          unit = "mm";\r\n' \
  '          b = 1/1000;\r\n' \
  '        } else if (sc < 1) {\r\n' \
  '          unit = "cm";\r\n' \
  '          b = 1/100;\r\n' \
  '        }\r\n' \
  '        let sc_c = (sc / b).toFixed(0);\r\n' \
  '        let sc_s = "";\r\n' \
  '        if (sc_c[0] == "1") {\r\n' \
  '          sc_s = "1".padEnd(sc_c.length, "0");\r\n' \
  '        } else if (sc_c[0] == "2" || sc_c[0] == "3" || sc_c[0] == "4") {\r\n' \
  '          sc_s = "2".padEnd(sc_c.length, "0");\r\n' \
  '        } else {\r\n' \
  '          sc_s = "5".padEnd(sc_c.length, "0");\r\n' \
  '        }\r\n' \
  '        sc = parseFloat(sc_s) * b;\r\n' \
  '        document.getElementById("scaleline").setAttribute("width", (sc / tscale * zoom * k).toFixed(0) + "px");\r\n' \
  '        document.getElementById("scalevalue").innerHTML = sc_s + " " + unit;\r\n' \
  '        update_tiles() \r\n' \
  '        if (document.getElementById("oset").selectedIndex == 8) {tracks_sort();}\r\n' \
  '      }\r\n' \
  '      function prop_to_wmvalue(s) {\r\n' \
  '        return parseFloat(s.match(/-?\\d+[.]?\\d*/)[0]);\r\n' \
  '      }\r\n' \
  '      function scroll_view(x, y) {\r\n' \
  '        hpx = viewpane.offsetWidth / 2 + (htopx - x) * zoom / tscale;\r\n' \
  '        hpy = viewpane.offsetHeight / 2 + (y - htopy) * zoom / tscale;\r\n' \
  '        reframe();\r\n' \
  '      }\r\n' \
  '      function scroll_dview(dx, dy) {\r\n' \
  '        hpx += dx;\r\n' \
  '        hpy += dy;\r\n' \
  '        reframe();\r\n' \
  '      }\r\n' \
  '      function track_boundaries(track=null) {\r\n' \
  '        let tracks = [];\r\n' \
  '        if (track != null) {\r\n' \
  '          tracks.push(track);\r\n' \
  '        } else {\r\n' \
  '          let trks = document.getElementById("tracksform").children;\r\n' \
  '          for (let t=0; t<trks.length; t++) {\r\n' \
  '            if (trks[t].firstElementChild.checked) {\r\n' \
  '              tracks.push(document.getElementById(trks[t].id.slice(0, -4)));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        let gminx = null;\r\n' \
  '        let gminy = null;\r\n' \
  '        let gmaxx = null;\r\n' \
  '        let gmaxy = null;\r\n' \
  '        for (let t=0; t<tracks.length; t++) {\r\n' \
  '          let empt = true;\r\n' \
  '          for (let s=0; s<tracks_pts[t].length; s++) {\r\n' \
  '            if (tracks_pts[t][s].length > 0) {empt = false; break;}\r\n' \
  '          }\r\n' \
  '          if (empt) {continue;}\r\n' \
  '          let minx = prop_to_wmvalue(tracks[t].style.left);\r\n' \
  '          let maxy = - prop_to_wmvalue(tracks[t].style.top);\r\n' \
  '          let maxx = minx + prop_to_wmvalue(tracks[t].style.width);\r\n' \
  '          let miny = maxy - prop_to_wmvalue(tracks[t].style.height);\r\n' \
  '          if (gminx == null) {\r\n' \
  '            gminx = minx;\r\n' \
  '            gminy = miny;\r\n' \
  '            gmaxx = maxx;\r\n' \
  '            gmaxy = maxy;\r\n' \
  '          } else {\r\n' \
  '            gminx = Math.min(gminx, minx);\r\n' \
  '            gminy = Math.min(gminy, miny);\r\n' \
  '            gmaxx = Math.max(gmaxx, maxx);\r\n' \
  '            gmaxy = Math.max(gmaxy, maxy);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (gminx == null) {\r\n' \
  '          return null;\r\n' \
  '        } else {\r\n' \
  '          return [gminx, gmaxx, gminy, gmaxy];\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function track_center(track=null) {\r\n' \
  '        let b = track_boundaries(track);\r\n' \
  '        if (b == null) {\r\n' \
  '          return null;\r\n' \
  '        } else {\r\n' \
  '          return [htopx + (b[0] + b[1]) / 2, htopy + (b[2] + b[3]) / 2];\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function scroll_to_track(track) {\r\n' \
  '        let c = track_center(track);\r\n' \
  '        if (c == null) {return;}\r\n' \
  '        scroll_view(c[0], c[1]);\r\n' \
  '      }\r\n' \
  '      function scroll_to_all() {\r\n' \
  '        let c = track_center();\r\n' \
  '        if (c == null) {\r\n' \
  '          scroll_view(defx, defy);\r\n' \
  '        } else {\r\n' \
  '          scroll_view(c[0], c[1]); \r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function track_click(e, trk, scroll=true) {\r\n' \
  '        if (e != null) {e.preventDefault();}\r\n' \
  '        let ex_foc = focused;\r\n' \
  '        if (trk.htmlFor == ex_foc + "visible") {focused = "";} else {focused = trk.htmlFor.slice(0, -7);}\r\n' \
  '        if (ex_foc != "") {\r\n' \
  '          document.getElementById(ex_foc + "desc").style.color = "";\r\n' \
  '          document.getElementById(ex_foc + "focus").style.display = "";\r\n' \
  '          if (! document.getElementById(ex_foc + "visible").checked) {\r\n' \
  '            document.getElementById(ex_foc.replace("track", "waydots")).style.display = "none";\r\n' \
  '            document.getElementById(ex_foc).style.display = "none";\r\n' \
  '          }\r\n' \
  '          if (focused || e == null) {\r\n' \
  '            document.getElementById(ex_foc.replace("track", "waydots")).style.zIndex = "";\r\n' \
  '            document.getElementById(ex_foc).style.zIndex = "";\r\n' \
  '            document.getElementById(ex_foc.replace("track", "patharrows")).style.display = "";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (focused) {\r\n' \
  '          trk.style.color = "dodgerblue";\r\n' \
  '          document.getElementById(focused + "focus").style.display = "inline";\r\n' \
  '          document.getElementById(focused.replace("track", "waydots")).style.display = "";\r\n' \
  '          document.getElementById(focused).style.display = "";\r\n' \
  '          document.getElementById(focused.replace("track", "waydots")).style.zIndex = "1";\r\n' \
  '          document.getElementById(focused).style.zIndex = "1";\r\n' \
  '          document.getElementById(focused.replace("track", "patharrows")).style.display = "inline";\r\n' \
  '          if (scroll) {\r\n' \
  '            trk.scrollIntoView({block:"nearest"});\r\n' \
  '            document.getElementById(focused + "focus").scrollIntoView({block:"nearest"});\r\n' \
  '            scroll_to_track(document.getElementById(focused));\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        refresh_graph();\r\n' \
  '      }\r\n' \
  '      function WGS84toWebMercator(lat, lon) {\r\n' \
  '        return [lon * Math.PI / 180 * 6378137, Math.log(Math.tan(Math.PI / 4 + lat * Math.PI / 360)) * 6378137];\r\n' \
  '      }\r\n' \
  '      function WebMercatortoWGS84(x, y) {\r\n' \
  '        return [(2 * Math.atan(Math.exp(y / 6378137)) - Math.PI / 2) * 180 / Math.PI, x * 180 / Math.PI / 6378137];\r\n' \
  '      }\r\n' \
  '      function track_over(trk) {\r\n' \
  '        let foc = trk.id.indexOf("color")<0?((trk.id.indexOf("desc")<0?trk.id:trk.htmlFor).slice(0, -7)):trk.id.slice(0, -5);\r\n' \
  '        document.getElementById(foc.replace("track", "waydots")).style.zIndex = "2";\r\n' \
  '        document.getElementById(foc).style.zIndex = "2";\r\n' \
  '        document.getElementById(foc.replace("track", "patharrows")).style.display = "inline";\r\n' \
  '        if (document.getElementById(foc + "visible").checked || foc == focused) {\r\n' \
  '          scroll_to_track(document.getElementById(foc));\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function track_outside(trk) {\r\n' \
  '        let foc = trk.id.indexOf("color")<0?((trk.id.indexOf("desc")<0?trk.id:trk.htmlFor).slice(0, -7)):trk.id.slice(0, -5);\r\n' \
  '        document.getElementById(foc.replace("track", "waydots")).style.zIndex = foc==focused?"1":"";\r\n' \
  '        document.getElementById(foc).style.zIndex = foc==focused?"1":"";\r\n' \
  '        document.getElementById(foc.replace("track", "patharrows")).style.display = foc==focused?"inline":"";\r\n' \
  '      }\r\n' \
  '      function distance(lat1, lon1, ele1, lat2, lon2, ele2) {\r\n' \
  '        let d = 2 * 6378137 * Math.asin(Math.sqrt((Math.sin((lat2 - lat1) * Math.PI / 360)) ** 2 + Math.cos(lat1 * Math.PI / 180) * Math.cos (lat2 * Math.PI / 180) * (Math.sin((lon2 - lon1) * Math.PI / 360)) ** 2));\r\n' \
  '        if (ele1 != null && ele2 != null) {d = Math.sqrt(d ** 2 + (ele2 - ele1) ** 2);}\r\n' \
  '        return d;\r\n' \
  '      }\r\n' \
  '      function slope(dist, heig) {\r\n' \
  '        return dist>Math.abs(heig)?(heig / Math.sqrt(dist**2 - heig**2)):(parseFloat(document.getElementById("slmax").innerHTML) / 100 * (heig==0?0:(heig>0?1:-1)));\r\n' \
  '      }\r\n' \
  '      function segment_calc(seg, seg_ind, stats, fpan=0, ind=null, tl=null, llhs=null, teas=null) {\r\n' \
  '        if (fpan == 0) {\r\n' \
  '          while (stats.length <= seg_ind) {stats.push([]);}\r\n' \
  '          stats[seg_ind] = [];\r\n' \
  '        }\r\n' \
  '        if (fpan <= 1 || (fpan == 2 && gpucomp == 0)) {\r\n' \
  '          let stat = Array(7).fill(0);\r\n' \
  '          let stat_p = null;\r\n' \
  '          let t_s = null;\r\n' \
  '          let lat_p = null;\r\n' \
  '          let lon_p = null;\r\n' \
  '          let lat = null;\r\n' \
  '          let lon = null;\r\n' \
  '          let ea_s = [0, 0];\r\n' \
  '          let ea_p = [NaN, NaN];\r\n' \
  '          let ea_l = [null, null];\r\n' \
  '          let ea_h = [null, null];\r\n' \
  '          let ea_g = [null, null];\r\n' \
  '          let ea_ic = [null, null];\r\n' \
  '          let ea_f = [parseFloat(document.getElementById("egstren").innerHTML), parseFloat(document.getElementById("agstren").innerHTML)];\r\n' \
  '          let el_s = 0;\r\n' \
  '          let el = null;\r\n' \
  '          let el_p = NaN;\r\n' \
  '          let p_p = null;\r\n' \
  '          for (let p=0; p<seg.length; p++) {\r\n' \
  '            let pt = seg[p];\r\n' \
  '            let ea = [parseFloat(pt[2]), parseFloat(pt[3])];\r\n' \
  '            for (let v=0; v<2; v++) {\r\n' \
  '              if (! isNaN(ea[v]) && isNaN(ea_p[v])) {\r\n' \
  '                ea_p[v] = ea[v];\r\n' \
  '                ea_s[v] = ea_p[v];\r\n' \
  '              }\r\n' \
  '              if (! isNaN(ea[v]) && ea_l[v] == null) {ea_l[v] = ea[v];}\r\n' \
  '              if (! isNaN(ea[v]) && ea_h[v] == null) {ea_h[v] = ea[v];}\r\n' \
  '            }\r\n' \
  '            if (fpan == 0) {\r\n' \
  '              let t = Date.parse(pt[4]);\r\n' \
  '              lat = parseFloat(pt[0]);\r\n' \
  '              lon = parseFloat(pt[1]);\r\n' \
  '              if (isNaN(t)) {\r\n' \
  '                stat[0] = t_s==null?0:stat_p[0];\r\n' \
  '              } else {\r\n' \
  '                if (t_s == null) {\r\n' \
  '                  t_s = t;\r\n' \
  '                } else {\r\n' \
  '                  stat[0] = Math.max((t - t_s) / 1000, stat_p[0]);\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              if (! isNaN(ea[1])) {\r\n' \
  '                el = ea[1];\r\n' \
  '                if (isNaN(el_p)) {\r\n' \
  '                  el_p = el;\r\n' \
  '                  el_s = el_p;\r\n' \
  '                }\r\n' \
  '              } else if (! isNaN(ea[0])) {\r\n' \
  '                el = ea[0];\r\n' \
  '                if (isNaN(el_p)) {\r\n' \
  '                  el_p = el;\r\n' \
  '                  el_s = el_p;\r\n' \
  '                }\r\n' \
  '              } else {\r\n' \
  '                el = isNaN(el_p)?0:el_p;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            if (p_p == null) {\r\n' \
  '              if (gpucomp == 0) {\r\n' \
  '                stat[4] = isNaN(ea[0])?ea_p[0]:ea[0];\r\n' \
  '                stat[5] = isNaN(ea[1])?ea_p[1]:ea[1];\r\n' \
  '              } else if (fpan == 0) {\r\n' \
  '                llhs.set([tl[0] - lat, lon - tl[1], el_p], 3 * ind);\r\n' \
  '                teas.set([stat[0], isNaN(ea[0])?ea_p[0]:ea[0], isNaN(ea[1])?ea_p[1]:ea[1]], 3 * ind);\r\n' \
  '                ind++;\r\n' \
  '              }\r\n' \
  '            } else {\r\n' \
  '              if (gpucomp <= 1 && fpan <= 1) {\r\n' \
  '                stat[2] = stat_p[2] + ((isNaN(ea_p[0])||isNaN(ea[0]))?0:Math.max(0,ea[0]-ea_p[0]));\r\n' \
  '                stat[3] = stat_p[3] + ((isNaN(ea_p[1])||isNaN(ea[1]))?0:Math.max(0,ea[1]-ea_p[1]));\r\n' \
  '              }\r\n' \
  '              if (gpucomp == 0) {\r\n' \
  '                if (fpan == 0) {\r\n' \
  '                  stat[1] = stat_p[1] + distance(lat_p, lon_p, isNaN(el_p)?0:el_p, lat, lon, el);\r\n' \
  '                }\r\n' \
  '                stat[4] = isNaN(ea[0])?ea_p[0]:ea[0];\r\n' \
  '                stat[5] = isNaN(ea[1])?ea_p[1]:ea[1];\r\n' \
  '              } else if (fpan == 0) {\r\n' \
  '                llhs.set([tl[0] - lat, lon - tl[1], isNaN(el_p)?el_p:el], 3 * ind);\r\n' \
  '                teas.set([stat[0], isNaN(ea[0])?ea_p[0]:ea[0], isNaN(ea[1])?ea_p[1]:ea[1]], 3 * ind);\r\n' \
  '                ind++;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            lat_p = lat;\r\n' \
  '            lon_p = lon;\r\n' \
  '            stat_p = stat.slice();\r\n' \
  '            if (fpan == 0) {\r\n' \
  '              stats[seg_ind].push(stat_p);\r\n' \
  '              if (! isNaN(el_p)) {el_p = el;}\r\n' \
  '            } else if (fpan == 1) {\r\n' \
  '              stats[seg_ind][p][2] = stat_p[2];\r\n' \
  '              stats[seg_ind][p][3] = stat_p[3];\r\n' \
  '            } else if (fpan == 2 && gpucomp == 0) {\r\n' \
  '              stats[seg_ind][p][4] = stat_p[4];\r\n' \
  '              stats[seg_ind][p][5] = stat_p[5];\r\n' \
  '            }\r\n' \
  '            p_p = p;\r\n' \
  '            if (gpucomp <= 1 && fpan <= 1) {\r\n' \
  '              for (let v=0; v<2; v++) {\r\n' \
  '                if (! isNaN(ea[v])) {\r\n' \
  '                  if (ea[v] > ea_p[v]) {\r\n' \
  '                    ea_p[v] = ea[v];\r\n' \
  '                    if (ea[v] >= ea_l[v] + ea_f[v]) {\r\n' \
  '                      ea_g[v] = "+";\r\n' \
  '                      ea_ic[v] = null;\r\n' \
  '                      ea_h[v] = ea[v];\r\n' \
  '                    }\r\n' \
  '                    if (ea_g[v] != "+" && ea_ic[v] == null) {\r\n' \
  '                      ea_ic[v] = p - 1;\r\n' \
  '                    }\r\n' \
  '                  }\r\n' \
  '                  if (ea[v] < ea_p[v] && ((ea[v] <= ea_h[v] - ea_f[v]) || ea_g[v] == "-")) {\r\n' \
  '                    if (ea_ic[v] != null) {\r\n' \
  '                      stat_p[v + 2] = stats[seg_ind][ea_ic[v]][v + 2];\r\n' \
  '                      for (let i=ea_ic[v]+1; i<=p; i++) {stats[seg_ind][i][v + 2] = stat_p[v + 2];}\r\n' \
  '                      ea_ic[v] = null;\r\n' \
  '                    }\r\n' \
  '                    if (ea_g[v] == "+") {\r\n' \
  '                      ea_l[v] = ea[v];\r\n' \
  '                    } else {\r\n' \
  '                      ea_l[v] = Math.min(ea_l[v], ea[v]);\r\n' \
  '                    }\r\n' \
  '                    ea_g[v] = "-";\r\n' \
  '                  }\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            if (! isNaN(ea[0])) {ea_p[0] = ea[0];}\r\n' \
  '            if (! isNaN(ea[1])) {ea_p[1] = ea[1];}\r\n' \
  '          }\r\n' \
  '          if (! stat_p) {return;}\r\n' \
  '          if (gpucomp == 0 && (fpan == 0 || fpan == 2)) {\r\n' \
  '            for (let p=0; p<stats[seg_ind].length; p++) {\r\n' \
  '              if (isNaN(stats[seg_ind][p][4])) {\r\n' \
  '                stats[seg_ind][p][4] = ea_s[0];\r\n' \
  '                if (isNaN(stats[seg_ind][p][5])) {stats[seg_ind][p][5] = ea_s[1];}\r\n' \
  '              } else if (isNaN(stats[seg_ind][p][5])) {\r\n' \
  '                stats[seg_ind][p][5] = ea_s[1];\r\n' \
  '              } else {break;}\r\n' \
  '            }\r\n' \
  '          } else if (gpucomp != 0 && fpan == 0) {\r\n' \
  '            for (let i=ind-stats[seg_ind].length; i<ind; i++) {\r\n' \
  '              if (isNaN(llhs[3 * i + 2])) {llhs[3 * i + 2] = el_s;} else {break;}\r\n' \
  '            }\r\n' \
  '            for (let i=ind-stats[seg_ind].length; i<ind; i++) {\r\n' \
  '              if (isNaN(teas[3 * i + 1])) {teas[3 * i + 1] = ea_s[0];} else {break;}\r\n' \
  '            }\r\n' \
  '            for (let i=ind-stats[seg_ind].length; i<ind; i++) {\r\n' \
  '              if (isNaN(teas[3 * i + 2])) {teas[3 * i + 2] = ea_s[1];} else {break;}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (gpucomp == 0 && (fpan == 0 || fpan == 2)) {\r\n' \
  '          let drange = parseFloat(document.getElementById("sldist").innerHTML) / 2;\r\n' \
  '          let slmax = parseFloat(document.getElementById("slmax").innerHTML) / 100;\r\n' \
  '          for (let p=0; p<stats[seg_ind].length; p++) {\r\n' \
  '            let ea = stats[seg_ind][p].slice(4,6);\r\n' \
  '            stats[seg_ind][p][4]=0;\r\n' \
  '            stats[seg_ind][p][5]=0;\r\n' \
  '            let ps = p;\r\n' \
  '            for (ps=p+1;ps<stats[seg_ind].length;ps++) {\r\n' \
  '              if (stats[seg_ind][ps][1] > stats[seg_ind][p][1] + drange) {break;}\r\n' \
  '              if (stats[seg_ind][ps][1] - stats[seg_ind][p][1] == 0) {continue;}\r\n' \
  '              stats[seg_ind][p][4] += slope(stats[seg_ind][ps][1] - stats[seg_ind][p][1], stats[seg_ind][ps][4] - ea[0]) * (stats[seg_ind][ps][1] - stats[seg_ind][ps-1][1]);\r\n' \
  '              stats[seg_ind][p][5] += slope(stats[seg_ind][ps][1] - stats[seg_ind][p][1], stats[seg_ind][ps][5] - ea[1]) * (stats[seg_ind][ps][1] - stats[seg_ind][ps-1][1]);\r\n' \
  '            }\r\n' \
  '            if (stats[seg_ind][ps - 1][1] - stats[seg_ind][p][1] != 0) {\r\n' \
  '              let c = (drange + stats[seg_ind][p][1] - stats[seg_ind][ps-1][1]) / (stats[seg_ind][ps-1][1] - stats[seg_ind][p][1]);\r\n' \
  '              stats[seg_ind][p][4] = (stats[seg_ind][p][4] + slope(stats[seg_ind][ps-1][1] - stats[seg_ind][p][1], stats[seg_ind][ps-1][4] - ea[0]) * (drange + stats[seg_ind][p][1] - stats[seg_ind][ps-1][1])) / drange;\r\n' \
  '              stats[seg_ind][p][5] = (stats[seg_ind][p][5] + slope(stats[seg_ind][ps-1][1] - stats[seg_ind][p][1], stats[seg_ind][ps-1][5] - ea[1]) * (drange + stats[seg_ind][p][1] - stats[seg_ind][ps-1][1])) / drange;\r\n' \
  '            }\r\n' \
  '            stats[seg_ind][p][4] = Math.max(Math.min(stats[seg_ind][p][4], slmax), -slmax);\r\n' \
  '            stats[seg_ind][p][5] = Math.max(Math.min(stats[seg_ind][p][5], slmax), -slmax);\r\n' \
  '          }\r\n' \
  '          for (let p=stats[seg_ind].length-2; p>0; p--) {\r\n' \
  '            if (stats[seg_ind][p+1][1] - stats[seg_ind][p][1] <= drange) {\r\n' \
  '              let ps = p;\r\n' \
  '              let s = [0, 0];\r\n' \
  '              let su = 0;\r\n' \
  '              for (ps=p-1; ps>=0; ps--) {\r\n' \
  '                if (stats[seg_ind][ps][1] < stats[seg_ind][p][1] - drange) {break;}\r\n' \
  '                let c = (stats[seg_ind][ps+1][1] - stats[seg_ind][ps][1]) / (stats[seg_ind][p][1] - stats[seg_ind][ps][1] + 1);\r\n' \
  '                s[0] += stats[seg_ind][ps][4] * c;\r\n' \
  '                s[1] += stats[seg_ind][ps][5] * c;\r\n' \
  '                su += c;\r\n' \
  '              }\r\n' \
  '              if (stats[seg_ind][p][1] - stats[seg_ind][ps+1][1] != 0) {\r\n' \
  '                stats[seg_ind][p][4] = Math.max(-slmax, Math.min(slmax, (stats[seg_ind][p][4] + s[0]/2 ) / (1 + su/2)));\r\n' \
  '                stats[seg_ind][p][5] = Math.max(-slmax, Math.min(slmax, (stats[seg_ind][p][5] + s[1]/2 ) / (1 + su/2)));\r\n' \
  '            }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (gpucomp == 0 && (fpan == 0 || fpan == 3)) {\r\n' \
  '          let trange = parseFloat(document.getElementById("sptime").innerHTML) / 2;\r\n' \
  '          let spmax = parseFloat(document.getElementById("spmax").innerHTML) / 3.6;\r\n' \
  '          for (let p=0; p<stats[seg_ind].length; p++) {\r\n' \
  '            stats[seg_ind][p][6] = 0;\r\n' \
  '            let ps = p;\r\n' \
  '            for (ps=p+1; ps<stats[seg_ind].length; ps++) {\r\n' \
  '              if (stats[seg_ind][ps][0] > stats[seg_ind][p][0] + trange) {break;}\r\n' \
  '              if (stats[seg_ind][ps][0] - stats[seg_ind][p][0] == 0) {continue;}\r\n' \
  '              stats[seg_ind][p][6] += (stats[seg_ind][ps][1] - stats[seg_ind][p][1]) / (stats[seg_ind][ps][0] - stats[seg_ind][p][0]) * (stats[seg_ind][ps][0] - stats[seg_ind][ps-1][0]);\r\n' \
  '            }\r\n' \
  '            if (stats[seg_ind][ps-1][0] - stats[seg_ind][p][0] != 0) {\r\n' \
  '              stats[seg_ind][p][6] = (stats[seg_ind][p][6] + (stats[seg_ind][ps-1][1] - stats[seg_ind][p][1]) / (stats[seg_ind][ps-1][0] - stats[seg_ind][p][0]) * (trange + stats[seg_ind][p][0] - stats[seg_ind][ps-1][0])) / trange;\r\n' \
  '            }\r\n' \
  '            stats[seg_ind][p][6] = Math.min(stats[seg_ind][p][6], spmax);\r\n' \
  '          }\r\n' \
  '          for (let p=stats[seg_ind].length-2; p>0; p--) {\r\n' \
  '            if (stats[seg_ind][p+1][0] - stats[seg_ind][p][0] <= trange) {\r\n' \
  '              let ps = p;\r\n' \
  '              let s = 0;\r\n' \
  '              let su = 0;\r\n' \
  '              for (ps=p-1; ps>=0; ps--) {\r\n' \
  '                if (stats[seg_ind][ps][0] < stats[seg_ind][p][0] - trange) {break;}\r\n' \
  '                let c = (stats[seg_ind][ps+1][0] - stats[seg_ind][ps][0]) / (stats[seg_ind][p][0] - stats[seg_ind][ps][0] + 1);\r\n' \
  '                s += stats[seg_ind][ps][6] * c;\r\n' \
  '                su += c;\r\n' \
  '              }\r\n' \
  '              if (stats[seg_ind][p][0] - stats[seg_ind][ps+1][0] != 0) {\r\n' \
  '                stats[seg_ind][p][6] = Math.min(spmax, (stats[seg_ind][p][6] + s/2 ) / (1 + su/2));\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function tracks_calc(fpan=0) {\r\n' \
  '        let starts = null;\r\n' \
  '        let tls = null;\r\n' \
  '        let llhs = null;\r\n' \
  '        let teas = null;\r\n' \
  '        if (fpan == 0) {\r\n' \
  '          starts = [0];\r\n' \
  '          tls = [];\r\n' \
  '          for (let t=0; t<tracks_pts.length; t++) {\r\n' \
  '            let segs = tracks_pts[t];\r\n' \
  '            tracks_stats.push([]);\r\n' \
  '            let tl = WebMercatortoWGS84(htopx + prop_to_wmvalue(document.getElementById("track" + t.toString()).style.left), htopy - prop_to_wmvalue(document.getElementById("track" + t.toString()).style.top));\r\n' \
  '            for (let s=0; s<segs.length; s++) {\r\n' \
  '              let nbp = segs[s].length;\r\n' \
  '              if (nbp != 0) {\r\n' \
  '                starts.push(starts[starts.length - 1] + nbp);\r\n' \
  '                tls.push(tl);\r\n' \
  '               }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (starts[starts.length - 1] == 0) {\r\n' \
  '            if (gpucomp >= 1) {gpustats.starts = starts;}\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '          if (gpucomp >= 1) {\r\n' \
  '            llhs = new Float32Array(GPUStats.pad(starts[starts.length - 1]) * 3);\r\n' \
  '            teas = new Float32Array(GPUStats.pad(starts[starts.length - 1]) * 3);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (tracks_stats.length == 0) {\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (fpan <= 1 || gpucomp == 0) {\r\n' \
  '          let ind = 0;\r\n' \
  '          let i = 0;\r\n' \
  '          for (let t=0; t<tracks_pts.length; t++) {\r\n' \
  '            let segs = tracks_pts[t];\r\n' \
  '            for (let s=0; s<segs.length; s++) {\r\n' \
  '              segment_calc(segs[s], s, tracks_stats[t], fpan, ind, tls==null?null:tls[i], llhs, teas);\r\n' \
  '              let nbp = segs[s].length;\r\n' \
  '              ind += nbp;\r\n' \
  '              if (nbp != 0) {i++;}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (fpan == 0 && gpucomp >= 1) {\r\n' \
  '          gpustats.starts = starts;\r\n' \
  '          gpustats.rlats = tls;\r\n' \
  '          gpustats.llhs = llhs;\r\n' \
  '          gpustats.teas = teas;\r\n' \
  '        }\r\n' \
  '        if (gpucomp == 0 && fpan == 0) {\r\n' \
  '          for (let t=0; t<tracks_pts.length; t++) {\r\n' \
  '            let segs = tracks_pts[t];\r\n' \
  '            let topx = htopx + prop_to_wmvalue(document.getElementById("track" + t.toString()).style.left);\r\n' \
  '            let topy = htopy - prop_to_wmvalue(document.getElementById("track" + t.toString()).style.top);\r\n' \
  '            let d = "M0 0";\r\n' \
  '            for (let s=0; s<segs.length; s++) {\r\n' \
  '              for (let p=0; p<segs[s].length; p++) {\r\n' \
  '                let [x, y] = WGS84toWebMercator(segs[s][p][0], segs[s][p][1]);\r\n' \
  '                d = d + (p==0?" M":" L") + (x - topx).toFixed(1) + " " + (topy - y).toFixed(1);\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            document.getElementById("path" + t.toString()).setAttribute("d", d);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (gpucomp >= 1 && fpan != 1) {\r\n' \
  '          if (gpustats.starts[gpustats.starts.length - 1] == 0) {\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '          gpustats.trange = parseFloat(document.getElementById("sptime").innerHTML) / 2;\r\n' \
  '          gpustats.spmax = parseFloat(document.getElementById("spmax").innerHTML) / 3.6;\r\n' \
  '          gpustats.drange = parseFloat(document.getElementById("sldist").innerHTML) / 2;\r\n' \
  '          gpustats.slmax = parseFloat(document.getElementById("slmax").innerHTML) / 100;\r\n' \
  '          gpustats.calc(fpan==0);\r\n' \
  '          let ds = gpustats.ds;\r\n' \
  '          let ssss = gpustats.ssss;\r\n' \
  '          let xys = gpustats.xys;\r\n' \
  '          let i = 0;\r\n' \
  '          for (let t=0; t<tracks_pts.length; t++) {\r\n' \
  '            let segs = tracks_pts[t];\r\n' \
  '            let stats = tracks_stats[t];\r\n' \
  '            let d = "M0 0";\r\n' \
  '            for (let s=0; s<segs.length; s++) {\r\n' \
  '              for (let p=0; p<segs[s].length; p++) {\r\n' \
  '                if (fpan == 0) {\r\n' \
  '                  stats[s][p][1] = stats[s][p>0?p-1:0][1] + ds[i];\r\n' \
  '                  d = d + (p==0?" M":" L") + xys[2 * i].toFixed(1) + " " + xys[2 * i + 1].toFixed(1);\r\n' \
  '                }\r\n' \
  '                stats[s][p][6] = ssss[3 * i];\r\n' \
  '                stats[s][p][4] = ssss[3 * i + 1];\r\n' \
  '                stats[s][p][5] = ssss[3 * i + 2];\r\n' \
  '                if (gpucomp == 2 && fpan != 3) {\r\n' \
  '                  if (p == 0) {\r\n' \
  '                    stats[s][p][2] = 0;\r\n' \
  '                    stats[s][p][3] = 0;\r\n' \
  '                  } else {\r\n' \
  '                    stats[s][p][2] = stats[s][p - 1][2] + Math.max(0, ssss[3 * i - 2]) * ds[i];\r\n' \
  '                    stats[s][p][3] = stats[s][p - 1][3] + Math.max(0, ssss[3 * i - 1]) * ds[i];\r\n' \
  '                  }\r\n' \
  '                }\r\n' \
  '                i++;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            if (fpan == 0) {\r\n' \
  '              document.getElementById("path" + t.toString()).setAttribute("d", d);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (fpan <= 1 || (fpan == 2 && gpucomp == 2)) {\r\n' \
  '          for (let t=0; t<tracks_pts.length; t++) {\r\n' \
  '            let dur = null;\r\n' \
  '            let dist = null;\r\n' \
  '            let ele = null;\r\n' \
  '            let alt = null;\r\n' \
  '            let stats = tracks_stats[t];\r\n' \
  '            for (let s=0; s<stats.length; s++) {\r\n' \
  '              if (stats[s].length == 0) {continue;}\r\n' \
  '              let stat = stats[s][stats[s].length - 1];\r\n' \
  '              dur = dur==null?stat[0]:dur+stat[0];\r\n' \
  '              dist = dist==null?stat[1]:dist+stat[1];\r\n' \
  '              ele = ele==null?stat[2]:ele+stat[2];\r\n' \
  '              alt = alt==null?stat[3]:alt+stat[3];\r\n' \
  '            }\r\n' \
  '            let noe = true;\r\n' \
  '            let noa = true;\r\n' \
  '            if (fpan == 0) {\r\n' \
  '              let segs = tracks_pts[t];\r\n' \
  '              let ts = null;\r\n' \
  '              let te = null;\r\n' \
  '              let slat = null;\r\n' \
  '              let slon = null;\r\n' \
  '              for (let s=0; s<segs.length; s++) {\r\n' \
  '                for (let p=0; p<segs[s].length; p++) {\r\n' \
  '                  let t = Date.parse(segs[s][p][4]);\r\n' \
  '                  if (! isNaN(t)) {\r\n' \
  '                    ts = Math.min(t, ts==null?t:ts);\r\n' \
  '                    te = Math.max(t, te==null?t:te);\r\n' \
  '                  }\r\n' \
  '                  if (noe) {\r\n' \
  '                    if (! isNaN(parseFloat(segs[s][p][2]))) {noe = false;}\r\n' \
  '                  }\r\n' \
  '                  if (noa) {\r\n' \
  '                    if (! isNaN(parseFloat(segs[s][p][3]))) {noa = false;}\r\n' \
  '                  }\r\n' \
  '                  if (slat == null) {\r\n' \
  '                    slat = segs[s][p][0];\r\n' \
  '                    slon = segs[s][p][1];\r\n' \
  '                  }\r\n' \
  '                  if (! noe && ! noa && slat != null && ts != null) {break;}\r\n' \
  '                }\r\n' \
  '                if (! noe && ! noa && slat != null && ts != null) {break;}\r\n' \
  '              }\r\n' \
  '              tracks_props.push([ts==null?NaN:dur, dist==null?NaN:dist, noe?NaN:ele, noa?NaN:alt, ts==null?NaN:ts, slat==null?[NaN, NaN]:[slat, slon]]);\r\n' \
  '              if (ts != null) {\r\n' \
  '                document.getElementById("track" + t.toString() + "period").value = time_conv.format(ts)  + " " + date_conv.format(ts) + " - " + time_conv.format(te)  + " " + date_conv.format(te);\r\n' \
  '              }\r\n' \
  '            } else {\r\n' \
  '              if (! isNaN(tracks_props[t][2])) {tracks_props[t][2] = ele;}\r\n' \
  '              if (! isNaN(tracks_props[t][3])) {tracks_props[t][3] = alt;}\r\n' \
  '            }\r\n' \
  '            let dur_c = "--h--mn--s";\r\n' \
  '            if (! isNaN(tracks_props[t][0])) {\r\n' \
  '              dur = Math.round(dur);\r\n' \
  '              let dur_s = dur % 60;\r\n' \
  '              let dur_m = ((dur - dur_s) / 60) % 60;\r\n' \
  '              let dur_h = (dur - dur_m * 60 - dur_s) / 3600;\r\n' \
  '              dur_c = dur_h.toString() + "h" + dur_m.toString().padStart(2, "0") + "mn" + dur_s.toString().padStart(2, "0") + "s";\r\n' \
  '            }\r\n' \
  '            let dist_c = "-km";\r\n' \
  '            if (dist != null) {dist_c = (dist / 1000).toFixed(2) + "km";}\r\n' \
  '            let ele_c = "-m";\r\n' \
  '            if (! noe) {ele_c = ele.toFixed(0) + "m";}\r\n' \
  '            let alt_c = "-m";\r\n' \
  '            if (! noa) {alt_c = alt.toFixed(0) + "m";}\r\n' \
  '            document.getElementById("track" + t.toString() + "desc").innerHTML = document.getElementById("track" + t.toString() + "desc").innerHTML.replace(/(.*<br>).*/,"$1(" + dur_c + " | " + dist_c + " | " + ele_c + " | " + alt_c + ")");\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        tracks_sort();\r\n' \
  '        refresh_graph();\r\n' \
  '      }\r\n' \
  '      function track_checkbox(trk) {\r\n' \
  '        if (trk.checked) {\r\n' \
  '          document.getElementById(trk.id.slice(0, -7)).style.display = "";\r\n' \
  '          document.getElementById("waydots" + trk.id.slice(5, -7)).style.display = "";\r\n' \
  '        } else {\r\n' \
  '          if (trk.id.slice(0, -7) != focused) {\r\n' \
  '            document.getElementById(trk.id.slice(0, -7)).style.display = "none";\r\n' \
  '            document.getElementById("waydots" + trk.id.slice(5, -7)).style.display = "none";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function show_hide_tracks(show, others) {\r\n' \
  '        let trks = document.getElementById("tracksform").children;\r\n' \
  '        for (let t=0; t<trks.length; t++) {\r\n' \
  '          if (trks[t].style.display != (others?"none":"")) {continue;}\r\n' \
  '          let cb = trks[t].firstElementChild;\r\n' \
  '          if (cb.checked != show) {\r\n' \
  '            cb.checked = show;\r\n' \
  '            track_checkbox(cb);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function track_color(trk) {\r\n' \
  '        if (document.getElementById(trk.id.slice(0, -5)).getAttribute("stroke").toUpperCase() != trk.value.toUpperCase()) {track_save(trk);}\r\n' \
  '      }\r\n' \
  '      function refresh_graph(sw=false) {\r\n' \
  '        let graph = document.getElementById("graph");\r\n' \
  '        let graphc = document.getElementById("graphc");\r\n' \
  '        let gwidth = null;\r\n' \
  '        let gheight = null;\r\n' \
  '        let gctx = graphc.getContext("2d");\r\n' \
  '        if (sw) {\r\n' \
  '          if (graph.style.display == "none") {\r\n' \
  '            document.getElementById("content").style.height = "calc(74vh - 2.4em - 18px)";\r\n' \
  '            viewpane.style.height = "calc(74vh - 2.4em - 18px)";\r\n' \
  '            graph.style.display = "block";\r\n' \
  '            gctx.lineWidth = 1;\r\n' \
  '            gctx.lineJoin = "round";\r\n' \
  '            gctx.lineCap = "square";\r\n' \
  '            rescale();\r\n' \
  '          } else {\r\n' \
  '            document.getElementById("content").style.height = "calc(99vh - 2.4em - 16px)";\r\n' \
  '            viewpane.style.height = "calc(99vh - 2.4em - 16px)";\r\n' \
  '            graph.style.display = "none";\r\n' \
  '            rescale();\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          if (graph.style.display == "none") {return;}\r\n' \
  '        }\r\n' \
  '        gwidth = graph.offsetWidth - graphc.offsetLeft;\r\n' \
  '        gheight = graph.offsetHeight;\r\n' \
  '        graphc.setAttribute("width", gwidth.toString());\r\n' \
  '        graphc.setAttribute("height", gheight.toString());\r\n' \
  '        gctx.fillStyle = "rgb(40,45,50)";\r\n' \
  '        gctx.fillRect(0, 0, gwidth, gheight);\r\n' \
  '        if (focused == "") {return;}\r\n' \
  '        let xl = 45;\r\n' \
  '        let xr = gwidth - 20;\r\n' \
  '        let yt = 10;\r\n' \
  '        let yb = gheight - 15;\r\n' \
  '        let gx = [];\r\n' \
  '        let gy = [];\r\n' \
  '        let gc = [];\r\n' \
  '        let dur = 0;\r\n' \
  '        let dist = 0;\r\n' \
  '        let ele = 0;\r\n' \
  '        let alt = 0;\r\n' \
  '        let stats = tracks_stats[parseInt(focused.substring(5))];\r\n' \
  '        for (let s=0; s<stats.length; s++) {\r\n' \
  '          if (stats[s].length == 0) {continue;}\r\n' \
  '          let stat = null;\r\n' \
  '          gc.push(gx.length);\r\n' \
  '          for (let p=0; p<stats[s].length; p++) {\r\n' \
  '            stat = stats[s][p];\r\n' \
  '            let pt = tracks_pts[parseInt(focused.substring(5))][s][p];\r\n' \
  '            let dr = true;\r\n' \
  '            switch (document.getElementById("graphy").selectedIndex) {\r\n' \
  '              case 0:\r\n' \
  '                gy.push(dist + stat[1]);\r\n' \
  '                break;\r\n' \
  '              case 1:\r\n' \
  '                let e = parseFloat(pt[2]);\r\n' \
  '                if (isNaN(e)) {\r\n' \
  '                  dr = false;\r\n' \
  '                } else {\r\n' \
  '                  gy.push(e);\r\n' \
  '                }\r\n' \
  '                break;\r\n' \
  '              case 2:\r\n' \
  '                let a = parseFloat(pt[3]);\r\n' \
  '                if (isNaN(a)) {\r\n' \
  '                  dr = false;\r\n' \
  '                } else {\r\n' \
  '                  gy.push(a);\r\n' \
  '                }\r\n' \
  '                break;\r\n' \
  '              case 3:\r\n' \
  '                gy.push(ele + stat[2]);\r\n' \
  '                break;\r\n' \
  '              case 4:\r\n' \
  '                gy.push(alt + stat[3]);\r\n' \
  '                break;\r\n' \
  '              case 5:\r\n' \
  '                gy.push(stat[4] * 100);\r\n' \
  '                break;\r\n' \
  '              case 6:\r\n' \
  '                gy.push(stat[5] * 100);\r\n' \
  '                break;\r\n' \
  '              case 7:\r\n' \
  '                gy.push(stat[6] * 3.6);\r\n' \
  '                break;\r\n' \
  '            }\r\n' \
  '            if (dr) {\r\n' \
  '              switch (document.getElementById("graphx").selectedIndex) {\r\n' \
  '                case 0:\r\n' \
  '                  gx.push(dur + stat[0]);\r\n' \
  '                  break;\r\n' \
  '                case 1:\r\n' \
  '                  gx.push(dist + stat[1]);\r\n' \
  '                  break;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          dur += stat[0];\r\n' \
  '          dist += stat[1];\r\n' \
  '          ele += stat[2];\r\n' \
  '          alt += stat[3];\r\n' \
  '        }\r\n' \
  '        if (gx.length < 2) {return;}\r\n' \
  '        let minx = gx[0];\r\n' \
  '        let maxx = gx[0];\r\n' \
  '        let miny = gy[0];\r\n' \
  '        let maxy = gy[0];\r\n' \
  '        for (let i=0; i<gx.length; i++) {\r\n' \
  '          if (minx > gx[i]) {minx = gx[i];}\r\n' \
  '          if (maxx < gx[i]) {maxx = gx[i];}\r\n' \
  '          if (miny > gy[i]) {miny = gy[i];}\r\n' \
  '          if (maxy < gy[i]) {maxy = gy[i];}\r\n' \
  '        }\r\n' \
  '        if (maxx == minx) {maxx++;}\r\n' \
  '        if (maxy == miny) {maxy++;}\r\n' \
  '        let cx = (xr - xl) / (maxx - minx);\r\n' \
  '        let cy = (yb - yt) / (maxy - miny);\r\n' \
  '        let yl = 0;\r\n' \
  '        if (document.getElementById("graphy").selectedIndex == 0) {\r\n' \
  '          yl = yb;\r\n' \
  '        } else if (maxy < 0) {\r\n' \
  '          yl = yt;\r\n' \
  '        } else if (miny > 0) {\r\n' \
  '          yl = yb;\r\n' \
  '        } else {\r\n' \
  '          yl = maxy * cy + yt;\r\n' \
  '        }\r\n' \
  '        gctx.strokeStyle = "rgb(56,56,56)";\r\n' \
  '        gctx.beginPath();\r\n' \
  '        let x = xl;\r\n' \
  '        let dx = (xr - xl) / Math.floor((xr - xl) / 100);\r\n' \
  '        while (x <= xr) {\r\n' \
  '          gctx.moveTo(x, yb + 1);\r\n' \
  '          gctx.lineTo(x, yt);\r\n' \
  '          if (x == xr) {break;}\r\n' \
  '          x += dx;\r\n' \
  '          if (x > xr) {x = xr;}\r\n' \
  '        }\r\n' \
  '        let y = yb;\r\n' \
  '        let dy = (yb - yt) / Math.floor((yb - yt) / 50);\r\n' \
  '        while (y >= yt) {\r\n' \
  '          gctx.moveTo(xl + 1, y);\r\n' \
  '          gctx.lineTo(xr, y);\r\n' \
  '          if (y == yt) {break;}\r\n' \
  '          y -= dy;\r\n' \
  '          if (y < yt) {y = yt;}\r\n' \
  '        }\r\n' \
  '        gctx.stroke();\r\n' \
  '        gctx.strokeStyle = "rgb(225,225,225)";\r\n' \
  '        gctx.beginPath();\r\n' \
  '        gctx.moveTo(xl, yb);\r\n' \
  '        gctx.lineTo(xl, yt);\r\n' \
  '        gctx.moveTo(xl, yl);\r\n' \
  '        gctx.lineTo(xr, yl);\r\n' \
  '        gctx.lineTo(xr, yl - 1);\r\n' \
  '        gctx.lineTo(xr, yl + 1);\r\n' \
  '        gctx.stroke();\r\n' \
  '        gctx.fillStyle = "rgb(225,225,255)";\r\n' \
  '        gctx.textAlign = "center";\r\n' \
  '        gctx.textBaseline = "top";\r\n' \
  '        x = xl;\r\n' \
  '        while (x <= xr) {\r\n' \
  '          if (document.getElementById("graphx").selectedIndex == 0) {\r\n' \
  '            let dur = Math.round((minx + (x - xl) / cx) / 60) * 60;\r\n' \
  '            let dur_m = (dur / 60) % 60;\r\n' \
  '            let dur_h = (dur - dur_m * 60) / 3600;\r\n' \
  '            let dur_c = dur_h.toString() + "h" + dur_m.toString().padStart(2, "0") + "mn";\r\n' \
  '            gctx.fillText(dur_c, x, yl + 3);\r\n' \
  '          } else {\r\n' \
  '            gctx.fillText(((minx + (x - xl) / cx) / 1000).toFixed(1) + "km", x, yl + 3);\r\n' \
  '          }\r\n' \
  '          if (x == xr) {break;}\r\n' \
  '          x += dx;\r\n' \
  '          if (x > xr) {x = xr;}\r\n' \
  '        }\r\n' \
  '        gctx.textAlign = "right";\r\n' \
  '        gctx.textBaseline = "middle";\r\n' \
  '        y = yb;\r\n' \
  '        let fin = false;\r\n' \
  '        while (true) {\r\n' \
  '          if (y - yl >= 16 || yl - y >= 10 || fin) {\r\n' \
  '            if (document.getElementById("graphy").selectedIndex == 0) {\r\n' \
  '              gctx.fillText(((maxy - (y - yt) / cy) / 1000).toFixed(1).replace(/^-(0*(\.0*)?$)/,"$1") + "km", xl - 2, y);\r\n' \
  '            } else if (document.getElementById("graphy").selectedIndex == 5 || document.getElementById("graphy").selectedIndex == 6) {\r\n' \
  '              gctx.fillText((maxy - (y - yt) / cy).toFixed(0).replace(/^-(0*(\.0*)?$)/,"$1") + "%", xl - 2, y);\r\n' \
  '            } else if (document.getElementById("graphy").selectedIndex == 7) {\r\n' \
  '              gctx.fillText((maxy - (y - yt) / cy).toFixed(1).replace(/^-(0*(\.0*)?$)/,"$1") + "km/h", xl - 2, y);\r\n' \
  '            } else {\r\n' \
  '              gctx.fillText((maxy - (y - yt) / cy).toFixed(0).replace(/^-(0*(\.0*)?$)/,"$1") + "m", xl - 2, y);\r\n' \
  '            }\r\n' \
  '            if (fin) {break;}\r\n' \
  '          }\r\n' \
  '          if (y == yt) {\r\n' \
  '            y = yl;\r\n' \
  '            fin = true;\r\n' \
  '            continue;\r\n' \
  '          }\r\n' \
  '          y -= dy;\r\n' \
  '          if (y < yt) {y = yt;}\r\n' \
  '        }\r\n' \
  '        gctx.strokeStyle = "rgb(255,0,0)";\r\n' \
  '        gctx.beginPath();\r\n' \
  '        for (let i=0; i<gx.length; i++) {\r\n' \
  '          if (i == gc[0]) {\r\n' \
  '            gctx.moveTo((gx[i] - minx) * cx + xl, (maxy - gy[i]) * cy + yt);\r\n' \
  '            gc.shift();\r\n' \
  '          } else {\r\n' \
  '            gctx.lineTo((gx[i] - minx) * cx + xl, (maxy - gy[i]) * cy + yt);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        gctx.stroke();\r\n' \
  '      }\r\n' \
  '      function open_3D() {\r\n' \
  '        if (document.getElementById("edit").disabled) {return;}\r\n' \
  '        if (focused == "") {return;}\r\n' \
  '        window.open("http://" + location.hostname + ":" + location.port + "/3D/viewer.html?" + focused.substring(5));\r\n' \
  '      }\r\n' \
  '      function rescale(tscale_ex=tscale) {\r\n' \
  '        let zoom_ex = zoom;\r\n' \
  '        if (mode == "map") {\r\n' \
  '          zoom = eval(zoom_s) * Math.min((viewpane.offsetWidth - 2) * tscale / (vmaxx - vminx), (viewpane.offsetHeight - 4) * tscale / (vmaxy - vminy));\r\n' \
  '          document.getElementById("zoom").innerHTML = zoom_s;\r\n' \
  '        } else {\r\n' \
  '          zoom = eval(zoom_s);\r\n' \
  '          if (tlevel != 0) {document.getElementById("matrix").innerHTML = tlevels[tlevel][0].toString();}\r\n' \
  '          document.getElementById("zoom").innerHTML = zoom_s;\r\n' \
  '        }\r\n' \
  '        document.documentElement.style.setProperty("--scale", tscale / zoom);\r\n' \
  '        document.documentElement.style.setProperty("--zoom", zoom);\r\n' \
  '        document.documentElement.style.setProperty("--wsp", (6 * Math.max(zoom/tscale, 1)).toFixed(1) + "em");\r\n' \
  '        if (focused) {\r\n' \
  '          scroll_to_track(document.getElementById(focused));\r\n' \
  '        } else {\r\n' \
  '          let r = zoom / zoom_ex * tscale_ex / tscale;\r\n' \
  '          hpx = viewpane.offsetWidth / 2 * (1 - r) + hpx * r;\r\n' \
  '          hpy = viewpane.offsetHeight / 2 * (1 - r) + hpy * r;\r\n' \
  '        }\r\n' \
  '        reframe();\r\n' \
  '      }\r\n' \
  '      function switch_tlock(resc=true) {\r\n' \
  '        if (mode == "map") {return;}\r\n' \
  '        let zoom_s_ex = zoom_s;\r\n' \
  '        if (tlock) {\r\n' \
  '          if (tlevel == 0) {return;}\r\n' \
  '          document.getElementById("tlock").innerHTML = "&#128275;";\r\n' \
  '          let nlevel = tlevel;\r\n' \
  '          if (eval(zoom_s) < eval(tlevels[tlevel][1])) {\r\n' \
  '            while (nlevel > 1) {\r\n' \
  '              if (tlevels[nlevel - 1][0] != tlevels[tlevel][0]) {break;}\r\n' \
  '              if (eval(zoom_s) <= eval(tlevels[nlevel - 1][1])) {nlevel--;} else {break;}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (eval(zoom_s) > eval(tlevels[tlevel][1])) {\r\n' \
  '            while (nlevel < tlevels.length - 1) {\r\n' \
  '              if (tlevels[nlevel + 1][0] != tlevels[tlevel][0]) {break;}\r\n' \
  '              if (eval(zoom_s) >= eval(tlevels[nlevel + 1][1])) {nlevel++;} else {break;}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          tlevel = nlevel;\r\n' \
  '          zoom_s = tlevels[nlevel][1];\r\n' \
  '        } else {\r\n' \
  '          document.getElementById("tlock").innerHTML = "&#128274;";\r\n' \
  '        }\r\n' \
  '        tlock = ! tlock;\r\n' \
  '        if (zoom_s == zoom_s_ex || ! resc) {return;}\r\n' \
  '        rescale();\r\n' \
  '      }\r\n' \
  '      function zoom_change(o) {\r\n' \
  '        let zoom_s_ex = zoom_s;\r\n' \
  '        if (mode == "map") {\r\n' \
  '          if (o < 0) {\r\n' \
  '            zoom_s = ([zooms[0]].concat(zooms))[zooms.indexOf(zoom_s)];\r\n' \
  '          } else {\r\n' \
  '            zoom_s = (zooms.concat(zooms[zooms.length - 1]))[zooms.indexOf(zoom_s) + 1];\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          if (tlock) {\r\n' \
  '            if (o < 0) {\r\n' \
  '              let ind = zooms.length;\r\n' \
  '              while (ind >= 0) {\r\n' \
  '                if (eval(zooms[ind]) < zoom) {break;}\r\n' \
  '                ind --;\r\n' \
  '              }\r\n' \
  '              if (ind >=0) {zoom_s = zooms[ind]} else {return;}\r\n' \
  '            } else {\r\n' \
  '              let ind = 0;\r\n' \
  '              while (ind < zooms.length) {\r\n' \
  '                if (eval(zooms[ind]) > zoom) {break;}\r\n' \
  '                ind ++;\r\n' \
  '              }\r\n' \
  '              if (ind < zooms.length) {zoom_s = zooms[ind]} else {return;}\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            let ntlevel = tlevel;\r\n' \
  '            if (o < 0) {\r\n' \
  '              if (tlevel <= 1) {return;}\r\n' \
  '              ntlevel = tlevel - 1;\r\n' \
  '            } else {\r\n' \
  '              if (tlevel >= tlevels.length - 1) {return;}\r\n' \
  '              ntlevel = tlevel + 1;\r\n' \
  '            }\r\n' \
  '            if (tlevels[ntlevel][0] != tlevels[tlevel][0]) {\r\n' \
  '              switch_tiles(null, ntlevel);\r\n' \
  '              return;\r\n' \
  '            }\r\n' \
  '            tlevel = ntlevel;\r\n' \
  '            zoom_s = tlevels[tlevel][1];\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (zoom_s == zoom_s_ex) {return;}\r\n' \
  '        rescale();\r\n' \
  '      }\r\n' \
  '      function zoom_dec() {\r\n' \
  '        zoom_change(-1);\r\n' \
  '      }\r\n' \
  '      function zoom_inc() {\r\n' \
  '        zoom_change(1);\r\n' \
  '      }\r\n' \
  '      function opacity_dec() {\r\n' \
  '        let filter = document.documentElement.style.getPropertyValue("--filter");\r\n' \
  '        let opacity = 1;\r\n' \
  '        if (filter && filter != "none") {\r\n' \
  '          opacity = parseFloat(filter.match(/slope=\\\\?"(0\\.[0-9])\\\\?"/)[1]);\r\n' \
  '        }\r\n' \
  '        if (opacity > 0.19) {\r\n' \
  '          filter = "url(\'data:image/svg+xml,<svg xmlns=\\"http://www.w3.org/2000/svg\\"><filter id=\\"attenuate\\"><feComponentTransfer><feFuncR type=\\"linear\\" slope=\\"%a\\" intercept=\\"%b\\"/><feFuncG type=\\"linear\\" slope=\\"%a\\" intercept=\\"%b\\"/><feFuncB type=\\"linear\\" slope=\\"%a\\" intercept=\\"%b\\"/></feComponentTransfer></filter></svg>#attenuate\')".replace(/%a/g, (opacity - 0.1).toFixed(1)).replace(/%b/g, (1.1 - opacity).toFixed(1));\r\n' \
  '          document.documentElement.style.setProperty("--filter", filter);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function opacity_inc() {\r\n' \
  '        let filter = document.documentElement.style.getPropertyValue("--filter");\r\n' \
  '        if (filter && filter != "none") {\r\n' \
  '          let opacity = parseFloat(filter.match(/slope=\\\\?"(0\\.[0-9])\\\\?"/)[1]);\r\n' \
  '          if (opacity < 0.81) {\r\n' \
  '            filter = "url(\'data:image/svg+xml,<svg xmlns=\\"http://www.w3.org/2000/svg\\"><filter id=\\"attenuate\\"><feComponentTransfer><feFuncR type=\\"linear\\" slope=\\"%a\\" intercept=\\"%b\\"/><feFuncG type=\\"linear\\" slope=\\"%a\\" intercept=\\"%b\\"/><feFuncB type=\\"linear\\" slope=\\"%a\\" intercept=\\"%b\\"/></feComponentTransfer></filter></svg>#attenuate\')".replace(/%a/g, (opacity + 0.1).toFixed(1)).replace(/%b/g, (0.9 - opacity).toFixed(1));\r\n' \
  '          } else {filter = "none";}\r\n' \
  '          document.documentElement.style.setProperty("--filter", filter);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function tracks_filter() {\r\n' \
  '        let filt = document.getElementById("tracksfilter").value;\r\n' \
  '        let trks = document.getElementById("tracksform").children;\r\n' \
  '        for (let t=0; t<trks.length; t++) {\r\n' \
  '          let tname = document.getElementById(trks[t].id.replace("cont", "name"));\r\n' \
  '          if (tname.value.toLowerCase().indexOf(filt) >= 0) {\r\n' \
  '            trks[t].style.display = document.getElementById(trks[t].id.replace("cont", "folder")).style.display;\r\n' \
  '            tname.style.display = "";\r\n' \
  '          } else {\r\n' \
  '            trks[t].style.display = "none";\r\n' \
  '            tname.style.display = "none";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (focused) {\r\n' \
  '          if (document.getElementById(focused + "cont").style.display == "none") {track_click(null, document.getElementById(focused + "desc"));}\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function tracks_sort() {\r\n' \
  '        let crit = document.getElementById("oset").selectedIndex;\r\n' \
  '        let asc = document.getElementById("sortup").style.display != "none";\r\n' \
  '        let trks = Array.from({length:tracks_props.length}).map((v,k)=>k);\r\n' \
  '        let c = function (a, b) {return a - b};\r\n' \
  '        let vals = [];\r\n' \
  '        function flt_comp(a, b) {\r\n' \
  '          if (a == b) {return 0;}\r\n' \
  '          if (isNaN(a)) {return 1;}\r\n' \
  '          if (isNaN(b)) {return -1;}\r\n' \
  '          return asc?a-b:b-a;\r\n' \
  '        }\r\n' \
  '        switch (crit) {\r\n' \
  '          case 0:\r\n' \
  '            break;\r\n' \
  '          case 1:\r\n' \
  '          case 2:\r\n' \
  '            vals = trks.map(function (t) {return document.getElementById("track" + t.toString() + (crit==1?"name":"visible")).value;});\r\n' \
  '            c = function (a, b) {return asc?str_comp(vals[a], vals[b]):-str_comp(vals[a], vals[b]);};\r\n' \
  '            break;\r\n' \
  '          case 3:\r\n' \
  '          case 4:\r\n' \
  '          case 5:\r\n' \
  '          case 6:\r\n' \
  '          case 7:\r\n' \
  '            c = function (a, b) {return flt_comp(tracks_props[a][crit - 3], tracks_props[b][crit - 3]);};\r\n' \
  '            break;\r\n' \
  '          case 8:\r\n' \
  '            let [clat, clon] = WebMercatortoWGS84(htopx + (viewpane.offsetWidth / 2 - hpx) * tscale / zoom, htopy + (hpy - viewpane.offsetHeight / 2) * tscale / zoom);\r\n' \
  '            vals = trks.map(function (t) {return (tracks_props[t][5][0]==null || tracks_props[t][5][1]==null)?NaN:distance(clat, clon, 0, tracks_props[t][5][0], tracks_props[t][5][1], 0);});\r\n' \
  '            c = function (a, b) {return flt_comp(vals[a], vals[b]);};\r\n' \
  '            break;\r\n' \
  '        }\r\n' \
  '        trks.sort(c);\r\n' \
  '        let frag = document.createDocumentFragment();\r\n' \
  '        for (let t of trks) {frag.appendChild(document.getElementById("track" + t.toString() + "cont"));}\r\n' \
  '        document.getElementById("tracksform").appendChild(frag);\r\n' \
  '      }\r\n' \
  '      function switch_sortorder() {\r\n' \
  '        let g = document.getElementById("sortup").style.display;\r\n' \
  '        document.getElementById("sortup").style.display = document.getElementById("sortdown").style.display;\r\n' \
  '        document.getElementById("sortdown").style.display = g;\r\n' \
  '        tracks_sort();\r\n' \
  '      }\r\n' \
  '      function switch_folderspanel() {\r\n' \
  '        let fp = document.getElementById("folderspanel");\r\n' \
  '        if (fp.style.display == "none") {fp.style.display="";} else {fp.style.display = "none";}\r\n' \
  '      }\r\n' \
  '      function folders_select() {\r\n' \
  '        let folders = document.getElementById("foldersform").getElementsByTagName("input");\r\n' \
  '        let t = 0;\r\n' \
  '        for (let f=1; f<folders.length; f++) {\r\n' \
  '          while (t < tracks_pts.length) {\r\n' \
  '            if (document.getElementById("track" + t.toString() + "folder" ).value.toLowerCase().indexOf(folders[f].value.toLowerCase()) >= 0) {\r\n' \
  '              if (folders[f].checked) {\r\n' \
  '                document.getElementById("track" + t.toString() + "cont").style.display = document.getElementById("track" + t.toString() + "name").style.display;\r\n' \
  '                document.getElementById("track" + t.toString() + "folder").style.display = "";\r\n' \
  '              } else {\r\n' \
  '                document.getElementById("track" + t.toString() + "cont").style.display = "none";\r\n' \
  '                document.getElementById("track" + t.toString() + "folder").style.display = "none";\r\n' \
  '              }\r\n' \
  '              t++;\r\n' \
  '            } else {\r\n' \
  '              break;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (focused) {\r\n' \
  '          if (document.getElementById(focused + "cont").style.display == "none") {track_click(null, document.getElementById(focused + "desc"));}\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function folders_whole() {\r\n' \
  '       let folders = document.getElementById("foldersform").getElementsByTagName("input");\r\n' \
  '       for (let f=1; f<folders.length; f++) {\r\n' \
  '         folders[f].checked = folders[0].checked;\r\n' \
  '       }\r\n' \
  '      }\r\n' \
  '      function switch_filterpanel(pa) {\r\n' \
  '        let fp = [null, document.getElementById("filterpanel1"), document.getElementById("filterpanel2"), document.getElementById("filterpanel3")];\r\n' \
  '        for (let p=1; p<=3; p++) {\r\n' \
  '          if (p == pa && (pa != 1 || gpucomp <= 1)) {\r\n' \
  '            if (fp[p].style.display == "none") {fp[p].style.display="";} else {fp[p].style.display = "none";}\r\n' \
  '          } else {\r\n' \
  '            fp[p].style.display = "none";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function track_edit() {\r\n' \
  '        if (focused == "") {return;}\r\n' \
  '        window.location.assign(window.location.href.replace("/GPXExplorer.html", "/edit?" + focused.substring(5)));\r\n' \
  '      }\r\n' \
  '      function escape(s) {\r\n' \
  '        return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");\r\n' \
  '      }\r\n' \
  '      function load_cb(t, prop) {\r\n' \
  '        if (t.status != 204) {\r\n' \
  '          window.alert("{#jserror#}" + t.status.toString() + " " + t.statusText);\r\n' \
  '          error_cb(null, prop);\r\n' \
  '          document.getElementById("edit").disabled = false;\r\n' \
  '          return false;\r\n'\
  '        }\r\n' \
  '        if (prop.id.slice(-4) == "file") {\r\n' \
  '          let uri_ex = document.getElementById(prop.id.replace("file", "visible")).value;\r\n' \
  '          let uri = uri_ex.replace(/(.*)(\\\\.*?)$/, "$1\\\\" + prop.value);\r\n' \
  '          let trks = document.getElementById("tracksform").children;\r\n' \
  '          for (let t=0; t<trks.length; t++) {\r\n' \
  '            if (trks[t].firstElementChild.value == uri_ex) {\r\n' \
  '              trks[t].firstElementChild.value = uri;\r\n' \
  '              document.getElementById(trks[t].id.replace("cont", "file")).value = prop.value;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          tracks_sort();\r\n' \
  '        } else if (prop.id.slice(-4) == "name") {\r\n' \
  '          document.getElementById(prop.id.replace("name", "desc")).innerHTML = document.getElementById(prop.id.replace("name", "desc")).innerHTML.replace(/.*(<br>.*)/, escape(prop.value) + "$1");\r\n' \
  '          document.getElementById(prop.id.replace("name", "desc")).title = prop.value;\r\n' \
  '          document.getElementById(prop.id.slice(0, -4).replace("track", "path")).firstElementChild.innerHTML = escape(prop.value);\r\n' \
  '          tracks_sort();\r\n' \
  '          tracks_filter();\r\n' \
  '        } else if (prop.id.slice(-5) == "color") {\r\n' \
  '          let trk = prop.id.slice(0, -5);\r\n' \
  '          let col = prop.value.toUpperCase();\r\n' \
  '          document.getElementById(trk).setAttribute("stroke", col);\r\n' \
  '          document.getElementById(trk).setAttribute("fill", col);\r\n' \
  '          document.getElementById(trk.replace("track", "waydots")).setAttribute("stroke", col);\r\n' \
  '          document.getElementById(trk.replace("track", "waydots")).setAttribute("fill", col);\r\n' \
  '        }\r\n' \
  '        document.getElementById("edit").disabled = false;\r\n' \
  '        return true;\r\n'\
  '      }\r\n' \
  '      function error_cb(t, prop) {\r\n' \
  '        if (t != null) {window.alert("{#jserror#}");}\r\n' \
  '        if (prop.id.slice(-4) == "file") {\r\n' \
  '          prop.value = document.getElementById(prop.id.replace("file", "visible")).value.split("\\\\").slice(-1);\r\n' \
  '        } else if (prop.id.slice(-4) == "name") {\r\n' \
  '          prop.value = document.getElementById(prop.id.replace("name", "desc")).title;\r\n' \
  '        } else if (prop.id.slice(-5) == "color") {\r\n' \
  '          prop.value = document.getElementById(prop.id.slice(0, -5)).getAttribute("stroke");\r\n' \
  '        } \r\n' \
  '        if (t != null) {document.getElementById("edit").disabled = false;}\r\n' \
  '      }\r\n' \
  '      function track_save(prop) {\r\n' \
  '        if (document.getElementById("edit").disabled) {error_cb(null, prop);return;}\r\n' \
  '        document.getElementById("edit").disabled = true;\r\n' \
  '        if (prop.id.slice(-4) == "file") {\r\n' \
  '          if (! prop.checkValidity()) {\r\n' \
  '            prop.value = document.getElementById(prop.id.replace("file", "visible")).value.split("\\\\").slice(-1);\r\n' \
  '            document.getElementById("edit").disabled = false;\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '          if (prop.value.slice(-4) != ".gpx") {\r\n' \
  '            if (prop.value.slice(-4).toLowerCase() != ".gpx") {\r\n' \
  '              prop.value = prop.value + ".gpx";\r\n' \
  '            } else {\r\n' \
  '              prop.value = prop.value.slice(0, -4) + ".gpx";\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        let body = prop.id + "=" + (prop.id.slice(-5)=="color"?prop.value.toUpperCase():prop.value);\r\n' \
  '        let msgn = show_msg("{#jmsave1#}", 0);\r\n' \
  '        xhr.onload = (e) => {load_cb(e.target, prop)?show_msg("{#jmsave2#}", 5, msgn):show_msg("{#jmsave3#}", 10, msgn);};\r\n' \
  '        xhr.onerror = (e) => {error_cb(e.target, prop); show_msg("{#jmsave3#}", 10, msgn);};\r\n' \
  '        xhr.open("POST", "/track");\r\n' \
  '        xhr.setRequestHeader("Content-Type", "application/octet-stream");\r\n' \
  '        xhr.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhr.send(body);\r\n' \
  '      }\r\n' \
  '      var xhr = new XMLHttpRequest();\r\n' \
  '      var xhrt = new XMLHttpRequest();\r\n' \
  '      xhrt.addEventListener("error", error_tcb);\r\n' \
  '    </script>\r\n' \
  '  </head>\r\n' \
  '  <body style="background-color:rgb(40,45,50);color:rgb(225,225,225);margin-top:2px;margin-bottom:0;"> \r\n' \
  '    <table style="width:98vw;">\r\n' \
  '      <colgroup>\r\n' \
  '        <col style="width:21em;">\r\n' \
  '        <col style="width:calc(98vw - 21em);">\r\n' \
  '      </colgroup>\r\n' \
  '      <thead>\r\n' \
  '        <tr>\r\n' \
  '          <th colspan="2" style="text-align:left;font-size:120%;width:100%;border-bottom:1px darkgray solid;">\r\n' \
  '           <input type="text" id="tracksfilter" name="tracksfilter" value="" oninput="tracks_filter()">\r\n' \
  '           <span style="display:inline-block;position:absolute;right:2vw;width:51em;overflow:hidden;text-align:right;font-size:80%;"><button title="{#jdescending#}" id="sortup" style="margin-left:0em;" onclick="switch_sortorder()">&#9699;</button><button title="{#jascending#}" id="sortdown" style="margin-left:0.25em;display:none;" onclick="switch_sortorder()">&#9700</button><select id="oset" name="oset" title="{#joset#}" autocomplete="off" style="width:10em;height:1.7em;margin-left:0.25em;" onchange="tracks_sort()"><option value="none">{#jsortnone#}</option><option value="name">{#jsortname#}</option><option value="file path">{#jsortfilepath#}</option><option value="duration">{#jsortduration#}</option><option value="distance">{#jsortdistance#}</option><option value="elevation gain">{#jsortelegain#}</option><option value="altitude gain">{#jsortaltgain#}</option><option value="date">{#jsortdate#}</option><option value="proximity">{#jsortproximity#}</option><</select><button title="{#jfolders#}" style="margin-left:0.75em;" onclick="switch_folderspanel()">&#128193;&#xfe0e;</button><button title="{#jhidetracks#}" style="margin-left:0.75em;" onclick="show_hide_tracks(false, event.altKey)">&EmptySmallSquare;</button><button title="{#jshowtracks#}" style="margin-left:0.25em;" onclick="show_hide_tracks(true, event.altKey)">&FilledSmallSquare;</button><button title="{#jedit#}" id="edit" style="margin-left:1em;" onclick="track_edit()">&#9998;</button><button title="{#jgraph#}" style="margin-left:1em;" onclick="(event.shiftKey||event.ctrlKey||event.altKey)?switch_filterpanel(event.shiftKey?1:(event.ctrlKey?2:3)):refresh_graph(true)">&angrt;</button><button title="{#j3dviewer#}" style="margin-left:0.25em;" onclick="open_3D()">3D</button><select id="tset" name="tset" title="{#jtsetonly#}" autocomplete="off" style="width:10em;height:1.7em;margin-left:0.75em;" onchange="switch_tiles(this.selectedIndex, -1)">##TSETS##</select><button title="{#jminus#}" style="margin-left:0.25em;" onclick="event.ctrlKey?opacity_dec():zoom_dec()">-</button><span id="matrix" style="display:none;width:1.5em;">--</span><span id="tlock" title="{#jlock#}" style="display:none;width:1em;cursor:pointer" onclick="switch_tlock()">&#128275;</span><span id="zoom" style="display:inline-block;width:2em;text-align:center;">1</span><button title="{#jplus#}" style="" onclick="event.ctrlKey?opacity_inc():zoom_inc()">+</button><button title="{#jzoomall#}" style="margin-left:0.25em;" onclick="switch_tiles(null, null);scroll_to_all()">&target;</button></span>\r\n' \
  '            <div id="folderspanel" style="display:none;position:absolute;top:calc(1.6em + 10px);left:25em;box-sizing:border-box;max-width:calc(98vw - 25.1em);max-height:calc(99vh - 3.2em - 25px);padding:10px;overflow:auto;white-space:nowrap;background-color:rgb(40,45,50);z-index:20;font-size:80%;font-weight:normal;">\r\n' \
  '              <form id="foldersform" autocomplete="off" onchange="folders_select()">\r\n' \
  '                <input id="folders" type="checkbox" style="margin-left:1.5em;" checked="" name="folders" value="folders" onchange="folders_whole()">\r\n' \
  '                <label for="folders" style="font-weight:bold;">{#jfoldersw#}</label><br>\r\n' \
  '##FOLDERS##' \
  '              </form>\r\n' \
  '            </div>\r\n' \
  '            <div id="filterpanel1" style="display:none;position:absolute;top:calc(1.6em + 10px);right:2vw;width:10em;height:13.4em;background-color:rgb(30,30,35);z-index:10;font-size: 75%;text-align:center;font-weight:normal;">\r\n' \
  '              <span>{#jfilterpanel1#}</span>\r\n' \
  '              <form id="filterform1" autocomplete="off" onchange="tracks_calc(1)">\r\n' \
  '                <label for="egfilter" style="left:2px;">{#jgraphelevation#}</label>\r\n' \
  '                <label for="agfilter" style="right:2px;">{#jgraphaltitude#}</label>\r\n' \
  '                <span id="egstren" style="left:0.7em;">##EGTHRESHOLD##</span>\r\n' \
  '                <input type="range" id="egfilter" name="egfilter" min="0" max="25" step="1" value="##EGTHRESHOLD##" style="right:8.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '                <span id="agstren" style="right:0.7em;">##AGTHRESHOLD##</span>\r\n' \
  '                <input type="range" id="agfilter" name="agfilter" min="0" max="25" step="1" value="##AGTHRESHOLD##" style="right:1.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n' \
  '            <div id="filterpanel2" style="display:none;position:absolute;top:calc(1.6em + 10px);right:2vw;width:10em;height:13.4em;background-color:rgb(30,30,35);z-index:10;font-size: 75%;text-align:center;font-weight:normal;">\r\n' \
  '              <span>{#jfilterpanel2#}</span>\r\n' \
  '              <form id="filterform2" autocomplete="off" onchange="tracks_calc(2)">\r\n' \
  '                <label for="sldfilter" style="left:2px;">{#jgraphdistance#}</label>\r\n' \
  '                <label for="slmfilter" style="right:2px;">{#jsmax#}</label>\r\n' \
  '                <span id="sldist" style="left:0.7em;">##SLRANGE##</span>\r\n' \
  '                <input type="range" id="sldfilter" name="sldfilter" min="0" max="500" step="2" value="##SLRANGE##" style="right:8.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '                <span id="slmax" style="right:0.7em;">##SLMAX##</span>\r\n' \
  '                <input type="range" id="slmfilter" name="slmfilter" min="0" max="100" step="1" value="##SLMAX##" style="right:1.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n' \
  '            <div id="filterpanel3" style="display:none;position:absolute;top:calc(1.6em + 10px);right:2vw;width:10em;height:13.4em;background-color:rgb(30,30,35);z-index:10;font-size: 75%;text-align:center;font-weight:normal;">\r\n' \
  '              <span>{#jfilterpanel3#}</span>\r\n' \
  '              <form id="filterform3" autocomplete="off" onchange="tracks_calc(3)">\r\n' \
  '                <label for="sptfilter" style="left:2px;">{#jspduration#}</label>\r\n' \
  '                <label for="spmfilter" style="right:2px;">{#jsmax#}</label>\r\n' \
  '                <span id="sptime" style="left:0.7em;">##SPRANGE##</span>\r\n' \
  '                <input type="range" id="sptfilter" name="sptfilter" min="0" max="300" step="2" value="##SPRANGE##" style="right:8.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '                <span id="spmax" style="right:0.7em;">##SPMAX##</span>\r\n' \
  '                <input type="range" id="spmfilter" name="spmfilter" min="0" max="90" step="1" value="##SPMAX##" style="right:1.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n' \
  '          </th>\r\n' \
  '        </tr>\r\n' \
  '      </thead>\r\n' \
  '      <tbody>\r\n' \
  '        <tr style="display:table-row;">\r\n' \
  '          <td style="display:table-cell;vertical-align:top;">\r\n' \
  '            <div id="content" style="height:calc(99vh - 2.4em - 16px);width: calc(21em - 2px);">\r\n' \
  '              <div id="tracks" style="overflow-y:scroll;overflow-x:hidden;height:100%;font-size:80%">\r\n' \
  '                {#jtracks#} (##NBTRACKS##)<br>\r\n' \
  '                <form id="tracksform" autocomplete="off">\r\n                  ##TRACKS##\r\n' \
  '                </form>\r\n' \
  '              </div>\r\n' \
  '            </div>\r\n' \
  '          </td>\r\n' \
  '          <td style="display:table-cell;vertical-align:top;position:relative;">\r\n' \
  '            <div id="view" style="overflow:hidden;position:absolute;width:100%;height:calc(99vh - 2.4em - 16px);" onmousedown="mouse_down(event, this)" onwheel="mouse_wheel(event)">\r\n' \
  '              <div id="handle" style="position:relative;top:0px;left:0px;width:100px;height:100px;">##PATHES##\r\n##WAYDOTS##' \
  '              </div>\r\n' \
  '              <div id="scalebox" style="position:absolute;left:4px;bottom:3px;background-color:rgba(255, 255, 255, .5);padding-left:2px;padding-right:2px;line-height:0.7em;"> \r\n' \
  '                <svg id="scaleline" stroke="black" stroke-width="1.5" width="100px" height="0.3em">\r\n' \
  '                  <line x1="0" y1="0" x2="100%" y2="0"/>\r\n' \
  '                  <line x1="0" y1="0" x2="0" y2="100%"/>\r\n' \
  '                  <line x1="100%" y1="0" x2="100%" y2="100%"/>\r\n' \
  '                </svg>\r\n' \
  '                <span id="scalevalue" style="font-size:70%;color:black;">0 m</span>\r\n' \
  '              </div>\r\n' \
  '            </div>\r\n' \
  '          </td>\r\n' \
  '        </tr>\r\n' \
  '      </tbody>\r\n' \
  '      <tfoot>\r\n' \
  '        <tr>\r\n' \
  '          <th colspan=2 style="text-align:left;font-size:80%;width:100%;border-top:1px darkgray solid;font-weight:normal;padding-bottom:0px;">\r\n' \
  '            <div style="height:1.2em;overflow-y:hidden;width:100%;">\r\n' \
  '              <div id="message" style="overflow-y:auto;width:calc(98vw - 6px - 1.4em);height:1.2em;display:inline-block;" ></div><div title="{#jexphelp#}" style="overflow-y:auto;width:1.4em;height:1.2em;display:inline-block;text-align:center;background-color:lightgray;color:black;font-weight:bold;cursor:help;">?</div>\r\n' \
  '            </div>\r\n' \
  '          </th>\r\n' \
  '        </tr>\r\n' \
  '      </tfoot>\r\n' \
  '    </table>\r\n' \
  '    <div id="graph" style="height:25vh;display:none;position:relative;width:100%;border-top:1px darkgray solid;font-size:80%;">\r\n' \
  '      <select id="graphy" name="graphy" title="y" autocomplete="off" style="height:1.7em;width:7em;position:absolute;left:0;top:0;" onchange="refresh_graph()"><option value="distance">{#jgraphdistance#}</option><option value="elevation">{#jgraphelevation#}</option><option value="altitude">{#jgraphaltitude#}</option><option value="elegain">{#jgraphelegain#}</option><option value="altgain">{#jgraphaltgain#}</option><option value="eleslope">{#jgrapheleslope#}</option><option value="altslope">{#jgraphaltslope#}</option><option value="speed">{#jgraphspeed#}</option></select>\r\n' \
  '      <select id="graphx" name="graphx" title="x" autocomplete="off" style="height:1.7em;width:7em;position:absolute;left:0;bottom:0;" onchange="refresh_graph()"><option value="time">{#jgraphtime#}</option><option value="distance">{#jgraphdistance#}</option></select>\r\n' \
  '      <canvas id="graphc" width="100" height="25" style="position:absolute;left:8em;top:0;">\r\n' \
  '      </canvas>\r\n' \
  '    </div>\r\n' \
  '    <script>\r\n' \
  '      var mousex = null;\r\n' \
  '      var mousey = null;\r\n' \
  '      var viewpane = document.getElementById("view");\r\n' \
  '      var handle = document.getElementById("handle");\r\n' \
  '      var hand = null;\r\n' \
  '      function mouse_down(e, elt) {\r\n' \
  '        if (e.button != 0 && e.button != 2) {return;}\r\n' \
  '        mousex = e.pageX;\r\n' \
  '        mousey = e.pageY;\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '        document.onmousemove = mouse_move;\r\n' \
  '        document.onmouseup = mouse_up;\r\n' \
  '        document.onclick = mouse_click;\r\n' \
  '        document.oncontextmenu = mouse_click;\r\n' \
  '        if (e.button == 0) {\r\n' \
  '          if (elt.id == "view") {\r\n' \
  '            hand = elt;\r\n' \
  '            viewpane.style.cursor = "all-scroll";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_up(e, elt) {\r\n' \
  '        mousex = null;\r\n' \
  '        mousey = null;\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '        document.onmousemove = null;\r\n' \
  '        document.onmouseup = null;\r\n' \
  '        viewpane.style.cursor = "";\r\n' \
  '        if (hand) {\r\n' \
  '          hand = null;\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (elt && e.button == 2) {\r\n' \
  '          if (elt.id.substring(0, 4) == "path") {\r\n' \
  '            let cb = document.getElementById(elt.id.replace("path", "track") + "visible");\r\n' \
  '            cb.checked = ! cb.checked;\r\n' \
  '            track_checkbox(cb);\r\n' \
  '            cb.scrollIntoView({block:"nearest"});\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_click(e, elt) {\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '        document.onclick = null;\r\n' \
  '        document.oncontextmenu = null;\r\n' \
  '        if (elt) {\r\n' \
  '          if (elt.id.substring(0, 4) == "path") {\r\n' \
  '            if (document.getElementById(elt.id.replace("path", "track") + "cont").style.display != "none") {\r\n' \
  '              let trk = document.getElementById(elt.id.replace("path", "track") + "desc");\r\n' \
  '              track_click(null, trk);\r\n' \
  '            }\r\n' \
  '          } else if (elt.id.substring(0, 7) == "waydots") {\r\n' \
  '            if (document.getElementById(elt.id.replace("waydots", "track") + "cont").style.display != "none") {\r\n' \
  '              let trk = document.getElementById(elt.id.replace("waydots", "track") + "desc");\r\n' \
  '              track_click(null, trk);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_move(e) {\r\n' \
  '        if (mousex != null && mousey != null && hand != null) {\r\n' \
  '          let dx = e.pageX - mousex;\r\n' \
  '          let dy = e.pageY - mousey;\r\n' \
  '          mousex = e.pageX;\r\n' \
  '          mousey = e.pageY;\r\n' \
  '          let p = viewpane.parentNode;\r\n' \
  '          if (e.pageX >= p.offsetLeft && e.pageX <= p.offsetLeft + p.offsetWidth && e.pageY >= p.offsetTop && e.pageY <= p.offsetTop + p.offsetHeight) {\r\n' \
  '            if (hand.id == "view") {\r\n' \
  '              scroll_dview(dx, dy);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_wheel(e) {\r\n' \
  '        e.preventDefault();\r\n' \
  '        if (e.ctrlKey) {\r\n' \
  '          if (e.deltaY < 0) {zoom_inc();} else {zoom_dec();}\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (! e.altKey) {\r\n' \
  '          if (e.shiftKey) {scroll_dview(-e.deltaY, 0);} else {scroll_dview(0, -e.deltaY);}\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (! focused) {return;}\r\n' \
  '        tr = document.getElementById(focused + "cont");\r\n' \
  '        do {\r\n' \
  '          if (e.deltaY > 0) {\r\n' \
  '            tr = tr.nextElementSibling;\r\n' \
  '          } else {\r\n' \
  '            tr = tr.previousElementSibling;\r\n' \
  '          }\r\n' \
  '          if (! tr) {return;}\r\n' \
  '        } while (! tr.firstElementChild.checked || tr.style.display == "none")\r\n' \
  '        track_click(null, document.getElementById(tr.id.replace("cont", "desc")));\r\n' \
  '      }\r\n' \
  '      function page_unload() {\r\n' \
  '        let filter = document.documentElement.style.getPropertyValue("--filter");\r\n' \
  '        if (! filter) {filter = "none";}\r\n' \
  '        sessionStorage.setItem("state", (mode == "map" ? "||" : (tset.toString() + "|" + tlevel.toString() + "|" + tlock.toString())) + "|" + zoom_s + "|" + dots_visible.toString() + "|" + filter + "|" + eset.toString() + "|" + iset.toString() + "|" + document.getElementById("egstren").innerHTML + "|" + document.getElementById("agstren").innerHTML + "|" + document.getElementById("sldist").innerHTML + "|" + document.getElementById("slmax").innerHTML + "|" + document.getElementById("sptime").innerHTML + "|" + document.getElementById("spmax").innerHTML + "|" + document.getElementById("graphx").selectedIndex.toString() + "|" + document.getElementById("graphy").selectedIndex.toString());\r\n' \
  '        sessionStorage.setItem("state_exp", document.getElementById("tracksfilter").value.replace(/&/g, "&amp;").replace(/\\|/g, "&;") + "|" + (document.getElementById("sortup").style.display == "").toString() + "|" + document.getElementById("oset").selectedIndex.toString() + "|" + Array.from(document.getElementById("foldersform").getElementsByTagName("input"), f => f.checked?"t":"f").slice(1).join("-") + "|" + Array.from({length:document.getElementById("tracksform").children.length}, (v, k) => document.getElementById("track" + k.toString() + "visible").checked?"t":"f").join("-"));\r\n' \
  '      }\r\n' \
  '      function error_dcb() {\r\n' \
  '        window.alert("{#jexpfail#}");\r\n' \
  '        document.body.innerHTML = "";\r\n' \
  '        document.head.innerHTML = "";\r\n' \
  '        window.close();\r\n' \
  '        throw "{#jexpfail#}";\r\n' \
  '      } \r\n' \
  '      function load_dcb(t) {\r\n' \
  '        if (t.status != 200) {error_dcb();return;}\r\n' \
  '        let tracks = t.response.split("==\\r\\n");\r\n' \
  '        if (document.getElementById("tracksform").children.length == 0) {tracks = [];}\r\n' \
  '        for (let t=0; t<tracks.length; t++) {\r\n' \
  '          tracks_pts.push([]);\r\n' \
  '          if (tracks[t] == "") {continue;}\r\n' \
  '          let segs = tracks[t].split("=\\r\\n");\r\n' \
  '          for (let s=0; s<segs.length; s++) {\r\n' \
  '            let s_p = [];\r\n' \
  '            if (segs[s] != "") {\r\n' \
  '              let pts = segs[s].split("\\r\\n");\r\n' \
  '              for (let p=0; p<pts.length; p++) {\r\n' \
  '                s_p.push(pts[p].split("&").map(decodeURIComponent));\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            tracks_pts[t].push(s_p);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        page_load(true);\r\n' \
  '      }\r\n' \
  '      function page_load(fol=false) {\r\n' \
  '        if (! fol) {\r\n' \
  '          let xhrd = new XMLHttpRequest();\r\n' \
  '          xhrd.onerror = (e) => error_dcb(e.target);\r\n' \
  '          xhrd.onload = (e) => load_dcb(e.target);\r\n' \
  '          xhrd.open("GET", "/GPXExplorer/data");\r\n' \
  '          xhrd.send();\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (navigator.userAgent.toLowerCase().indexOf("firefox") > 0) {\r\n' \
  '          document.getElementById("tset").focus();\r\n' \
  '          document.getElementById("tset").blur();\r\n' \
  '        }\r\n' \
  '        let prev_state = sessionStorage.getItem("state");\r\n' \
  '        if (prev_state != null) {prev_state = prev_state.split("|");}\r\n' \
  '        if (prev_state != null) {zoom_s = prev_state[3]}\r\n' \
  '        if (mode == "map") {\r\n' \
  '          add_tile();\r\n' \
  '          rescale();\r\n' \
  '        } else {\r\n' \
  '          if (prev_state == null) {\r\n' \
  '            switch_tiles(0, null);\r\n' \
  '            scroll_to_all();\r\n' \
  '          } else {\r\n' \
  '            document.getElementById("tset").selectedIndex = parseInt(prev_state[0]);\r\n' \
  '            switch_tiles(parseInt(prev_state[0]), parseInt(prev_state[1]));\r\n' \
  '            if (prev_state[2] == "true") {switch_tlock(false);}\r\n' \
  '          }\r\n' \
  '          document.getElementById("matrix").style.display = "inline-block";\r\n' \
  '          document.getElementById("tlock").style.display = "inline-block";\r\n' \
  '          if (tlevel == 0) {rescale();}\r\n' \
  '        }\r\n' \
  '        if (prev_state != null) {\r\n' \
  '          dots_visible = prev_state[4] == "true";\r\n' \
  '          document.documentElement.style.setProperty("--filter", prev_state[5]);\r\n' \
  '          eset = parseInt(prev_state[6]);\r\n' \
  '          iset = parseInt(prev_state[7]);\r\n' \
  '          document.getElementById("egstren").innerHTML = prev_state[8];\r\n' \
  '          document.getElementById("egfilter").value = parseFloat(prev_state[8]);\r\n' \
  '          document.getElementById("agstren").innerHTML = prev_state[9];\r\n' \
  '          document.getElementById("agfilter").value = parseFloat(prev_state[9]);\r\n' \
  '          document.getElementById("sldist").innerHTML = prev_state[10];\r\n' \
  '          document.getElementById("sldfilter").value = parseFloat(prev_state[10]);\r\n' \
  '          document.getElementById("slmax").innerHTML = prev_state[11];\r\n' \
  '          document.getElementById("slmfilter").value = parseFloat(prev_state[11]);\r\n' \
  '          document.getElementById("sptime").innerHTML = prev_state[12];\r\n' \
  '          document.getElementById("sptfilter").value = parseFloat(prev_state[12]);\r\n' \
  '          document.getElementById("spmax").innerHTML = prev_state[13];\r\n' \
  '          document.getElementById("spmfilter").value = parseFloat(prev_state[13]);\r\n' \
  '          document.getElementById("graphx").selectedIndex = parseInt(prev_state[14]);\r\n' \
  '          document.getElementById("graphy").selectedIndex = parseInt(prev_state[15]);\r\n' \
  '        }\r\n' \
  '        prev_state = sessionStorage.getItem("state_exp");\r\n' \
  '        if (prev_state != null) {\r\n' \
  '          prev_state = prev_state.split("|");\r\n' \
  '          document.getElementById("tracksfilter").value = prev_state[0].replace(/\\&;/g, "|").replace(/&amp;/g, "&");\r\n' \
  '          document.getElementById("sortup").style.display = prev_state[1]=="true"?"":"none";\r\n' \
  '          document.getElementById("sortdown").style.display = prev_state[1]=="true"?"none":"";\r\n' \
  '          document.getElementById("oset").selectedIndex = parseInt(prev_state[2]);\r\n' \
  '          let folders = document.getElementById("foldersform").getElementsByTagName("input");\r\n' \
  '          let st = prev_state[3].split("-");\r\n' \
  '          for (let f=1; f<folders.length; f++) {folders[f].checked = st[f-1]=="t";}\r\n' \
  '          st = prev_state[4].split("-");\r\n' \
  '          for (let t=0; t<st.length; t++) {document.getElementById("track" + t.toString() + "visible").checked = st[t]=="t";}\r\n' \
  '        }\r\n' \
  '        tracks_calc();\r\n' \
  '        tracks_sort();\r\n' \
  '        tracks_filter();\r\n' \
  '        folders_select();\r\n' \
  '        window.onresize = (e) => {rescale();refresh_graph()};\r\n' \
  '        document.getElementById("filterpanel1").style.right = "calc(2vw + " + (mode=="tiles"?"13.3":"10.6") + "em - 30px)";\r\n' \
  '        document.getElementById("filterpanel2").style.right = "calc(2vw + " + (mode=="tiles"?"13.3":"10.6") + "em - 30px)";\r\n' \
  '        document.getElementById("filterpanel3").style.right = "calc(2vw + " + (mode=="tiles"?"13.3":"10.6") + "em - 30px)";\r\n' \
  '        window.onbeforeunload = page_unload;\r\n' \
  '        if (focused != "") {\r\n' \
  '          foc = focused;\r\n' \
  '          focused = "";\r\n' \
  '          track_click(null, document.getElementById(foc + "desc"));\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      ##SESSIONSTORE##if (sessionStorage.getItem("active") != "##SESSIONSTOREVALUE##") {\r\n' \
  '        window.alert("{#jsession#}");\r\n' \
  '        document.body.innerHTML = "";\r\n' \
  '        document.head.innerHTML = "";\r\n' \
  '        window.close();\r\n' \
  '        throw "{#jsession#}";\r\n' \
  '      }\r\n' \
  '      page_load();\r\n' \
  '    </script>\r\n' \
  '  </body>\r\n' \
  '</html>'
  HTMLExp_TEMPLATE = HTMLExp_TEMPLATE.replace('{', '{{').replace('}', '}}').replace('{{#', '{').replace('#}}', '}').format_map(LSTRINGS['interface']).replace('{{', '{').replace('}}', '}')
  HTMLExp_FOLDER_TEMPLATE = \
  '                <input id="folder%s" type="checkbox" checked="" name="folder%s" value="%s">\r\n' \
  '                <label for="folder%s">%s</label><br>\r\n'
  HTMLExp_TRACK_TEMPLATE = \
  '<div id="track%scont">\r\n' \
  '                    <input type="checkbox" id="track%svisible" checked name="track%svisible" value="%s" onchange="track_checkbox(this)" onmouseover="track_over(this)" onmouseout="track_outside(this)">' \
  '<label for="track%svisible" id="track%sdesc" title="%s" onclick="track_click(event, this)" onmouseover="track_over(this)" onmouseout="track_outside(this)">%s<br>(--h--mn--s | -km | -m | -m)</label><br>\r\n' \
  '                    <input type="color" id="track%scolor" value="%s" onchange="track_color(this)" onmouseover="track_over(this)" onmouseout="track_outside(this)">\r\n' \
  '                    <span id="track%sfocus">\r\n' \
  '                      <label for="track%sname">{jname}</label>\r\n' \
  '                      <input type="text" id="track%sname" name="track%sname" value="%s" onchange="track_save(this)"><br>\r\n' \
  '                      <label for="track%sfile">{jfile}</label>\r\n' \
  '                      <input type="text" id="track%sfile" name="track%sfile" required pattern="[^\\\\\\/\\?\\*:<>&quot;\\|]*" value="%s" onchange="track_save(this)"><br>\r\n' \
  '                      <label for="track%sfolder">{jfolder}</label>\r\n' \
  '                      <input type="text" id="track%sfolder" name="track%sfolder" value="%s" readOnly><br>\r\n' \
  '                      <label for="track%speriod">{jperiod}</label>\r\n' \
  '                      <input type="text" id="track%speriod" name="track%speriod" value="%s" readOnly><br>\r\n' \
  '                      <label for="track%scontent">{jcontent}</label>\r\n' \
  '                      <input type="text" id="track%scontent" name="track%scontent" value="%s" readOnly><br>\r\n' \
  '                    </span>\r\n' \
  '                  </div>'
  HTMLExp_TRACK_TEMPLATE = HTMLExp_TRACK_TEMPLATE.format_map(LSTRINGS['interface'])
  HTMLExp_PATH_TEMPLATE = \
  '\r\n' \
  '              <svg id="track%s" viewbox="##VIEWBOX##" stroke="%s" fill="%s" style="width:##WIDTH##;height:##HEIGHT##;top:##TOP##;left:##LEFT##;">\r\n' \
  '                <path id="path%s" onmousedown="mouse_down(event, this)" onmouseup="mouse_up(event, this)" onclick="mouse_click(event, this)" d="M0 0">\r\n' \
  '                  <title>%s</title>;\r\n' \
  '                </path>\r\n' \
  '                <text id="patharrows%s" dy="0.25em">\r\n' \
  '                  <textPath href="#path%s">##ARROWS##</textPath>\r\n' \
  '                </text>\r\n' \
  '              </svg>'
  HTMLExp_WAYDOT_TEMPLATE = \
  '                <circle onmousedown="mouse_down(event, this)" onmouseup="mouse_up(event, this)" onclick="mouse_click(event, this.parentNode)" cx="%s" cy="%s"><title>%s</title></circle>\r\n'
  HTMLExp_WAYDOTS_TEMPLATE = \
  '              <svg id="waydots%s" pointer-events="none" viewbox="##VIEWBOX##" stroke="%s" fill="%s" style="width:##WIDTH##;height:##HEIGHT##;top:##TOP##;left:##LEFT##;">\r\n%s' \
  '              </svg>\r\n'

  def _load_config(self, uri=os.path.dirname(os.path.abspath(__file__)) + '\GPXTweaker.cfg'):
    try:
      f = open(uri, "rt", encoding='utf-8')
      cfg = f.read()
    except:
      self.log(0, 'cerror', uri)
      return False
    finally:
      try:
        f.close()
      except:
        pass
    hcur = ''
    scur = ''
    for l in cfg.splitlines():
      if len(l) == 0:
        continue
      if l[0] == '#':
        continue
      if l[:2] == '[[' and l[-2:] == ']]':
        hcur = l[2:-2]
        if hcur[:9].lower() == 'maptiles ':
          hcur = hcur[:9].lower() + hcur[9:]
          self.TilesSets.append([hcur[9:].strip(), {}, {}, [1, ]])
          s = self.TilesSets[-1]
        elif hcur[:4].lower() == 'map ':
          hcur = hcur[:4].lower() + hcur[4:]
          self.MapSets.append([hcur[4:].strip(), {}, {}])
          s = self.MapSets[-1]
        elif hcur[:15].lower() == 'elevationtiles ':
          hcur = hcur[:15].lower() + hcur[15:]
          self.ElevationsProviders.append([hcur[15:].strip(), {}, {}])
          s = self.ElevationsProviders[-1]
        elif hcur[:13].lower() == 'elevationmap ':
          hcur = hcur[:13].lower() + hcur[13:]
          self.ElevationMapSets.append([hcur[13:].strip(), {}, {}])
          s = self.ElevationMapSets[-1]
        elif hcur[:13].lower() == 'elevationapi ':
          hcur = hcur[:13].lower() + hcur[13:]
          self.ElevationsProviders.append([hcur[13:].strip(), {}, {}])
          s = self.ElevationsProviders[-1]
        elif hcur[:13].lower() == 'itineraryapi ':
          hcur = hcur[:13].lower() + hcur[13:]
          self.ItinerariesProviders.append([hcur[13:].strip(), {}, {}])
          s = self.ItinerariesProviders[-1]
        elif hcur.lower() == 'global':
          hcur = hcur.lower()
        else:
          self.log(0, 'cerror', hcur)
          return False
        continue
      if l[0] == '[' and l[-1] == ']':
        scur = l[1:-1].lower()
        if hcur == 'global':
          if not scur in ('interfaceserver', 'tilesbuffer', 'boundaries', 'folders', 'statistics'):
            self.log(0, 'cerror', hcur + ' - ' + scur)
            return False
        elif hcur[:9] == 'maptiles ':
          if not scur in ('infos', 'handling', 'display'):
            self.log(0, 'cerror', hcur + ' - ' + scur)
            return False
        elif hcur[:4] == 'map ' or hcur[:15] == 'elevationtiles ' or hcur[:13] in ('elevationmap ', 'elevationapi ', 'itineraryapi '):
          if not scur in ('infos', 'handling'):
            self.log(0, 'cerror', hcur + ' - ' + scur)
            return False
        else:
          self.log(0, 'cerror', hcur + ' - ' + scur)
          return False
        continue
      if not (hcur[:9] == 'maptiles ' and scur == 'display') and not (hcur == 'global' and scur == 'folders'):
        if ':' in l:
          field, value = l.split(':', 1)
          field = field.lower().strip()
          value = value.lstrip()
          if value.lower() == 'true':
            value = True
          elif value.lower() == 'false':
            value = False
          elif value.lower() == 'none':
            value = None
          elif value.lower() == '':
            value = None if scur in ('boundaries', 'statistics', 'handling') else ''
        else:
          self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
          return False
      if hcur == 'global':
        if scur == 'interfaceserver':
          if field == 'ip':
            self.Ip = value or self.Ip
          elif field == 'port':
            port = value or self.Ports
            if '-' in port:
              self.Ports = port.split('-', 1)
            else:
              self.Ports = (port, port)
            if not self.Ports[0].isdecimal() or not self.Ports[1].isdecimal():
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
            self.Ports = (int(self.Ports[0]), int(self.Ports[1]))
            if self.Ports[0] > self.Ports[1]:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'tilesbuffer':
          if field == 'size':
            self.TilesBufferSize = None if value == None else int(value)
          elif field == 'threads':
            self.TilesBufferThreads = None if value == None else int(value)
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'boundaries':
          if field == 'min_lat':
            if value == None:
              self.VMinLat = None
            else:
              self.VMinLat = float(value)
              if self.VMinLat < -math.degrees(2 * math.atan(math.exp(math.pi)) - math.pi / 2):
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              if self.VMaxLat != None:
                if self.VMinLat >= self.VMaxLat:
                  self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                  return False
          elif field == 'max_lat':
            if value == None:
              self.VMaxLat = None
            else:
              self.VMaxLat = float(value)
              if self.VMaxLat > math.degrees(2 * math.atan(math.exp(math.pi)) - math.pi / 2):
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              if self.VMinLat != None:
                if self.VMinLat >= self.VMaxLat:
                  self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                  return False
          elif field == 'min_lon':
            if value == None:
              self.VMinLon = None
            else:
              self.VMinLon = float(value)
              if self.VMinLon < -180:
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              if self.VMaxLon != None:
                if self.VMinLon >= self.VMaxLon:
                  self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                  return False
          elif field == 'max_lon':
            if value == None:
              self.VMaxLon = None
            else:
              self.VMaxLon = float(value)
              if self.VMaxLon > 180:
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              if self.VMinLon != None:
                if self.VMinLon >= self.VMaxLon:
                  self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                  return False
          elif field == 'def_lat':
            self.DefLat = None if value == None else float(value)
          elif field == 'def_lon':
            self.DefLon = None if value == None else float(value)
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
          if not None in (self.VMinLat, self.VMaxLat, self.DefLat):
            if self.DefLat <= self.VMinLat or self.DefLat >= self.VMaxLat:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          if not None in (self.VMinLon, self.VMaxLon, self.DefLon):
            if self.DefLon <= self.VMinLon or self.DefLon >= self.VMaxLon:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
        elif scur == 'folders':
          if l.rstrip().endswith('*'):
            self.Folders.insert(0, os.path.abspath(os.path.expandvars(l.lstrip().rstrip(' *'))))
            if not os.path.isdir(self.Folders[0]):
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          else:
            self.Folders.append(os.path.abspath(os.path.expandvars(l.lstrip().rstrip())))
            if not os.path.isdir(self.Folders[-1]):
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
        elif scur == 'statistics':
          if field == 'gpu_comp':
            self.GpuComp = 0 if value == None else value
          elif field == 'ele_gain_threshold':
            if value != None:
              self.EleGainThreshold = int(value)
          elif field == 'alt_gain_threshold':
            if value != None:
              self.AltGainThreshold = int(value)
          elif field == 'slope_range':
            if value != None:
              self.SlopeRange = int(value)
          elif field == 'slope_max':
            if value != None:
              self.SlopeMax = int(value)
          elif field == 'speed_range':
            if value != None:
              self.SpeedRange = int(value)
          elif field == 'speed_max':
            if value != None:
              self.SpeedMax = int(value)
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        else:
          self.log(0, 'cerror', hcur + ' - ' + scur)
          return False
      elif hcur[:9] == 'maptiles ' or hcur[:15] == 'elevationtiles ':
        if scur == 'infos':
          if field == 'alias':
            s[1] = WebMercatorMap.TSAlias(value) if hcur[:9] == 'maptiles ' else WGS84Elevation.TSAlias(value)
            if not s[1]:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          elif field in ('source', 'pattern', 'layer', 'matrixset', 'style', 'format') or (hcur[:15] == 'elevationtiles ' and field in ('matrix', 'nodata')):
            s[1][field] = value
            if field == 'nodata':
              try:
                s[1][field] = float(value)
              except:
                pass
          elif field in ('basescale', 'topx', 'topy'):
            try:
              s[1][field] = float(value)
            except:
              pass
          elif field in ('width', 'height'):
            try:
              s[1][field] = int(value)
            except:
              pass
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'handling':
          if field in ('key', 'referer', 'user_agent', 'local_pattern', 'local_store', 'local_expiration', 'only_local'):
            s[2][field] = value
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif hcur[:9] == 'maptiles ' and scur == 'display':
          if ',' in l:
            matrix, zoom = l.split(',')
          elif '*' in l:
            matrix = l.rstrip(' *')
            zoom = '1' + l[len(matrix):]
          else:
            matrix = l
            zoom = '1'
          try:
            matrix = int(matrix.strip())
          except:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
          zoom = zoom.strip()
          if zoom[-1] == '*':
            zoom = zoom[:-1].strip()
            s[3][0] = len(s[3])
          s[3].append([matrix, zoom])
      elif hcur[:4] == 'map ' or hcur[:13] == 'elevationmap ':
        if scur == 'infos':
          if field == 'alias':
            s[1] = WebMercatorMap.MSAlias(value) if hcur[:9] == 'maptiles ' else WGS84Elevation.MSAlias(value)
            if not s[1]:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          elif field in ('source', 'layers', 'styles', 'format') or (hcur[:13] == 'elevationmap ' and field == 'nodata'):
            s[1][field] = value
            if field == 'nodata':
              try:
                s[1][field] = float(value)
              except:
                pass
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'handling':
          if field in ('key', 'referer', 'user_agent'):
            s[2][field] = value
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        else:
          self.log(0, 'cerror', hcur + ' - ' + scur)
          return False
      elif hcur[:13] in ('elevationapi ', 'itineraryapi '):
        if scur == 'infos':
          if field == 'alias':
            s[1] = WGS84Elevation.ASAlias(value) if hcur[:13] == 'elevationapi ' else WGS84Itinerary.ASAlias(value)
            if not s[1]:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          elif field in ('source', 'json_key') + (('separator', 'nodata') if hcur[:13] == 'elevationapi ' else ()):
            s[1][field.replace('json_', '')] = value
            if field == 'nodata':
              try:
                s[1][field] = float(value)
              except:
                pass
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'handling':
          if field in ('key', 'referer', 'user_agent'):
            s[2][field] = value
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
      else:
        self.log(0, 'cerror', hcur)
        return False
    self.log(1, 'cloaded')
    return True

  def __init__(self, uri=None, trk=None, bmap=None, emap=None, map_minlat=None, map_maxlat=None, map_minlon=None, map_maxlon=None, map_resolution=None, map_maxheight=2000, map_maxwidth=4000, map_dpi=None, cfg=os.path.dirname(os.path.abspath(__file__)) + '\GPXTweaker.cfg'):
    self.Uri = None
    self.SessionStoreValue = str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time())))
    self.SessionId = None
    self.PSessionId = None
    self.Ip = '127.0.0.1'
    self.Ports = '8000'
    self.TilesBufferSize = None
    self.TilesBufferThreads = None
    self.VMinLat = - math.degrees(2 * math.atan(math.exp(math.pi)) - math.pi / 2)
    self.VMaxLat = - self.VMinLat
    self.VMinLon = -180
    self.VMaxLon = 180
    self.DefLat = None
    self.DefLon = None
    self.Folders = []
    self.GpuComp = 0;
    self.EleGainThreshold = 4;
    self.AltGainThreshold = 3;
    self.SlopeRange = 100;
    self.SlopeMax = 50;
    self.SpeedRange = 60;
    self.SpeedMax = 8;
    self.Mode = None
    self.EMode = None
    self.TilesSets = []
    self.MapSets = []
    self.ElevationsProviders = []
    self.ElevationMapSets = []
    self.ItinerariesProviders = []
    self.Tracks = []
    self.Track = None
    self.TilesSet = None
    self.MapSet = None
    self.ElevationMapSet = None
    self.ElevationProviderSel = None
    self.ItineraryProviderSel = None
    self.HTML = None
    self.HTML3D = None
    self.HTML3DData = None
    self.HTMLExp = None
    self.TracksBoundaries = []
    self.Minx = None
    self.Maxx = None
    self.Miny = None
    self.Maxy = None
    self.SLock = threading.Lock()
    self.log = partial(log, 'interface')
    self.log(1, 'conf')
    if not self._load_config(cfg):
      return
    self.GPXTweakerInterfaceServerInstances = [None] * (self.Ports[1] - self.Ports[0] + 1)
    err = False
    if map_minlat != None:
      if map_minlat < self.VMinLat:
        err = True
      if bmap:
        self.VMinLat = map_minlat
    if map_maxlat != None:
      if map_maxlat > self.VMaxLat:
        err = True
      if bmap:
        self.VMaxLat = map_maxlat
    if map_minlon != None:
      if map_minlon < self.VMinLon:
        err = True
      if bmap:
        self.VMinLon = map_minlon
    if map_maxlat != None:
      if map_maxlat > self.VMaxLat:
        err = True
      if bmap:
        self.VMaxLon = map_maxlon
    if err:
      self.log(0, 'berror4')
      return
    self.DefLat = self.DefLat if self.DefLat != None else (self.VMinLat + self.VMaxLat) / 2
    self.DefLon = self.DefLon if self.DefLon != None else (self.VMinLon + self.VMaxLon) / 2
    if len(self.Folders) == 0:
      self.Folders.append(os.path.abspath(''))
    if uri != None:
      u = os.path.abspath(uri)
    else:
      f1 = 0
      while f1 < len(self.Folders):
        f2 = f1 + 1
        while f2 < len(self.Folders):
          if os.path.commonpath((self.Folders[f1], self.Folders[f2])) == self.Folders[f1]:
            del self.Folders[f2]
          else:
            f2 += 1
        f1 += 1
      k = lambda f: f[2].lower() == 'gpx' and not f[0].lower().endswith(' - original') and not f[0].lower().endswith(' - backup')
      uris = (os.path.join(e[0], f) for folder in self.Folders for e in os.walk(folder) for f in e[2] if k(f.rpartition('.')))
      trk = 0
      nbtrk = None
      u = next(uris, None)
    while u != None:
      track = WGS84Track()
      if not track.LoadGPX(u, trk):
        if uri == None:
          u = next(uris, None)
          continue
        else:
          return
      minlat = min((p[1][0] for seg in (*track.Pts, track.Wpts) for p in seg), default=(self.DefLat if (not bmap or map_minlat == None) else map_minlat))
      maxlat = max((p[1][0] for seg in (*track.Pts, track.Wpts) for p in seg), default=(self.DefLat if (not bmap or map_maxlat == None) else map_maxlat))
      minlon = min((p[1][1] for seg in (*track.Pts, track.Wpts) for p in seg), default=(self.DefLon if (not bmap or map_minlon == None) else map_minlon))
      maxlon = max((p[1][1] for seg in (*track.Pts, track.Wpts) for p in seg), default=(self.DefLon if (not bmap or map_maxlon == None) else map_maxlon))
      if minlat < self.VMinLat or maxlat > self.VMaxLat or minlon < self.VMinLon or maxlon > self.VMaxLon:
        if uri == None:
          self.log(0, 'berror6')
          u = next(uris, None)
          continue
        else:
          self.log(0, 'berror4')
          return
      track.Ind = len(self.Tracks)
      self.Tracks.append([u, track])
      self.TracksBoundaries.append((minlat, maxlat, minlon, maxlon))
      if uri != None:
        self.Uri, self.Track = self.Tracks[0]
        break
      if nbtrk == None:
        nbtrk = len(track.Track.getElementsByTagNameNS('*', 'trk'))
      trk += 1
      if trk >= nbtrk:
        trk = 0
        nbtrk = None
        u = next(uris, None)
    minlat = min((b[0] for b in self.TracksBoundaries), default=(self.DefLat if (not bmap or map_minlat == None) else map_minlat))
    maxlat = max((b[1] for b in self.TracksBoundaries), default=(self.DefLat if (not bmap or map_maxlat == None) else map_maxlat))
    minlon = min((b[2] for b in self.TracksBoundaries), default=(self.DefLon if (not bmap or map_minlon == None) else map_minlon))
    maxlon = max((b[3] for b in self.TracksBoundaries), default=(self.DefLon if (not bmap or map_maxlon == None) else map_maxlon))
    if minlat < self.VMinLat or maxlat > self.VMaxLat or minlon < self.VMinLon or maxlon > self.VMaxLon:
      self.log(0, 'berror4')
      return
    if bmap:
      self.Mode = 'map'
      self.TilesSets = [['Map']]
      self.Map = WebMercatorMap()
      if '://' in bmap or ':\\' in bmap:
        if not self.Map.LoadMap(bmap, *(WGS84WebMercator.WGS84toWebMercator(map_minlat, map_minlon) if not None in (map_minlat, map_minlon) else (None, None)), *(WGS84WebMercator.WGS84toWebMercator(map_maxlat, map_maxlon) if not None in (map_maxlat, map_maxlon) else (None, None)), resolution=map_resolution):
          self.log(0, 'berror')
          return
      else:
        for i in range(len(self.MapSets)):
          if self.MapSets[i][0].lower() == bmap.lower() or bmap == " ":
            self.MapSet = i
            break
        if self.MapSet == None:
          self.log(0, 'berror3', bmap)
          return
        minlat = minlat if map_minlat == None else map_minlat
        maxlat = maxlat if map_maxlat == None else map_maxlat
        minlon = minlon if map_minlon == None else map_minlon
        maxlon = maxlon if map_maxlon == None else map_maxlon
        if not self.Map.FetchMap(self.MapSets[self.MapSet][1], max(self.VMinLat, minlat - 0.014), min(self.VMaxLat, maxlat + 0.014), max(self.VMinLon, minlon - 0.019), min(self.VMaxLon, maxlon + 0.019), map_maxheight, map_maxwidth, dpi=map_dpi, **self.MapSets[self.MapSet][2]):
          self.log(0, 'berror')
          return
      if not hasattr(self.Map, 'WMS_BBOX'):
        bbox = dict(zip(('{minx}', '{miny}', '{maxx}', '{maxy}'), self.Map.MapInfos['bbox'].split(',')))
      else:
        bbox = dict(zip(self.Map.WMS_BBOX.split(','), self.Map.MapInfos['bbox'].split(',')))
      self.VMinx, self.VMiny, self.VMaxx, self.VMaxy = list(float(bbox[k]) for k in ('{minx}', '{miny}', '{maxx}', '{maxy}'))
      minlat, minlon = WGS84WebMercator.WebMercatortoWGS84(float(bbox['{minx}']), float(bbox['{miny}']))
      maxlat, maxlon = WGS84WebMercator.WebMercatortoWGS84(float(bbox['{maxx}']), float(bbox['{maxy}']))
      minlat += 0.014
      maxlat -= 0.014
      minlon += 0.019
      maxlon -= 0.019
      if next((p[1][0] for seg in (*self.Track.Pts, self.Track.Wpts) for p in seg), None) != None:
        self.Minx, self.Miny = WGS84WebMercator.WGS84toWebMercator(minlat, minlon)
        self.Maxx, self.Maxy = WGS84WebMercator.WGS84toWebMercator(maxlat, maxlon)
        if self.Minx < self.VMinx or self.Maxx > self.VMaxx or self.Miny < self.VMiny or self.Maxy > self.VMaxy:
          self.log(0, 'berror4')
          return
      self.Minx, self.Miny, self.Maxx, self.Maxy = self.VMinx, self.VMiny, self.VMaxx, self.VMaxy
      for t in range(len(self.TracksBoundaries)):
        self.TracksBoundaries[t] = (self.Minx, self.Maxx, self.Miny, self.Maxy)
    else:
      if len(self.TilesSets) == 0 or not self.TilesBufferSize or not self.TilesBufferThreads:
        self.log(0, 'berror5')
        return
      self.Mode = 'tiles'
      self.Map = WebMercatorMap(self.TilesBufferSize, self.TilesBufferThreads)
      self.TilesSet = 0
      self.VMinx, self.VMiny = WGS84WebMercator.WGS84toWebMercator(self.VMinLat, self.VMinLon)
      self.VMaxx, self.VMaxy = WGS84WebMercator.WGS84toWebMercator(self.VMaxLat, self.VMaxLon)
      self.Minx, self.Miny = WGS84WebMercator.WGS84toWebMercator(max(self.VMinLat, minlat - 0.008), max(self.VMinLon, minlon - 0.011))
      self.Maxx, self.Maxy = WGS84WebMercator.WGS84toWebMercator(min(self.VMaxLat, maxlat + 0.008), min(self.VMaxLon, maxlon + 0.011))
      for t in range(len(self.TracksBoundaries)):
        self.TracksBoundaries[t] = tuple(b[i] for i in (0,1) for b in (WGS84WebMercator.WGS84toWebMercator(max(self.VMinLat, self.TracksBoundaries[t][0] - 0.008), max(self.VMinLon, self.TracksBoundaries[t][2] - 0.011)), WGS84WebMercator.WGS84toWebMercator(min(self.VMaxLat, self.TracksBoundaries[t][1] + 0.008), min(self.VMaxLon, self.TracksBoundaries[t][3] + 0.011))))
    self.Elevation = WGS84Elevation()
    if emap:
      self.ElevationsProviders = []
      if '://' in emap or ':\\' in emap:
        if self.Elevation.LoadMap(emap):
          self.EMode = 'map'
          self.ElevationProvider = partial(self.Elevation.WGS84toElevation, infos=None)
          self.log(1, 'elevation', emap)
        else:
          self.ElevationProvider = None
          self.log(0, 'eerror', emap)
      else:
        for i in range(len(self.ElevationMapSets)):
          if self.ElevationMapSets[i][0].lower() == emap.lower() or emap == " ":
            self.ElevationMapSet = i
            break
        if self.ElevationMapSet == None:
          self.log(0, 'eerror', emap)
        else:
          minlat = minlat if map_minlat == None else map_minlat
          maxlat = maxlat if map_maxlat == None else map_maxlat
          minlon = minlon if map_minlon == None else map_minlon
          maxlon = maxlon if map_maxlon == None else map_maxlon
          if self.Elevation.FetchMap(self.ElevationMapSets[self.ElevationMapSet][1], max(self.VMinLat, minlat - 0.014), min(self.VMaxLat, maxlat + 0.014), max(self.VMinLon, minlon - 0.019), min(self.VMaxLon, maxlon + 0.019), map_maxheight, map_maxwidth, dpi=map_dpi, **self.ElevationMapSets[self.ElevationMapSet][2]):
            self.EMode = 'map'
            self.ElevationProvider = partial(self.Elevation.WGS84toElevation, infos=None)
            self.log(1, 'elevation', self.ElevationMapSets[self.ElevationMapSet][0])
          else:
            self.ElevationProvider = None
            self.log(0, 'eerror', self.ElevationMap[0])
    elif len(self.ElevationsProviders) > 0:
      self.ElevationProviderSel = 0
      if 'layer' in self.ElevationsProviders[0][1]:
        self.EMode = 'tiles'
        self.ElevationProvider = partial(self.Elevation.WGS84toElevation, infos=self.ElevationsProviders[0][1], matrix=self.ElevationsProviders[0][1].get('matrix'), **self.ElevationsProviders[0][2])
        self.log(1, 'elevation', self.ElevationsProviders[0][0])
      else:
        self.EMode = "api"
        self.ElevationProvider = partial(self.Elevation.RequestElevation, self.ElevationsProviders[0][1], **self.ElevationsProviders[0][2])
        self.log(1, 'elevation', self.ElevationsProviders[0][0])
    else:
      self.log(0, 'eerror', '-')
      self.ElevationProvider = None
    self.Itinerary = WGS84Itinerary()
    if len(self.ItinerariesProviders) > 0:
      self.ItineraryProviderSel = 0
      self.ItineraryProviderConnection = [[None]]
      def ItineraryProvider(points):
        try:
          pcon = self.ItineraryProviderConnection.pop()
        except:
          pcon = None
        iti = self.Itinerary.RequestItinerary(self.ItinerariesProviders[self.ItineraryProviderSel][1], points, **self.ItinerariesProviders[self.ItineraryProviderSel][2], pconnection=pcon)
        if pcon:
          self.ItineraryProviderConnection.append(pcon)
        return iti
      self.ItineraryProvider = ItineraryProvider
      self.log(1, 'itinerary', self.ItinerariesProviders[self.ItineraryProviderSel][0])
    else:
      self.ItineraryProvider = None
    if uri != None:
      self.HTML = ''
    else:
      self.HTMLExp = ''

  def _build_pathes(self):
    def _coord_to_vb(x, y):
      return '%.1f %.1f' % (x - self.Minx, self.Maxy - y)
    pathes = ''
    pathes = ''.join(GPXTweakerWebInterfaceServer.HTML_PATH_TEMPLATE.replace('##WIDTH##', 'calc(%.1fpx / var(--scale))' % (self.Maxx - self.Minx)).replace('##HEIGHT##', 'calc(%.1fpx / var(--scale))' % (self.Maxy - self.Miny)).replace('##LEFT##', 'calc(0px / var(--scale))').replace('##TOP##', 'calc(0px / var(--scale))').replace('##VIEWBOX##', '%.1f %.1f %.1f %.1f' % (0, 0, self.Maxx - self.Minx, self.Maxy - self.Miny)).replace('##ARROWS##', "&rsaquo; " * 500) % (s, s, 'M0 0' + ''.join(' M' + _coord_to_vb(*pt[1]) for pt in self.Track.WebMercatorPts[s][0:1]) + ''.join(' L' + _coord_to_vb(*pt[1]) for pt in self.Track.WebMercatorPts[s][1:]), s) for s in range(len(self.Track.WebMercatorPts)))
    return pathes

  def _build_waypoints(self):
    f = lambda e: '' if e == None else html.escape(e) if isinstance(e, str) else e
    return ''.join((GPXTweakerWebInterfaceServer.HTML_WAYPOINT_TEMPLATE % (*([pt[0]] * 6), *(a for b in zip(*([[pt[0]] * 5] * 3), map(f, pt[1])) for a in b))) for pt in self.Track.Wpts)

  def _build_points(self):
    f = lambda e: '' if e == None else html.escape(e) if isinstance(e, str) else e
    return ''.join(GPXTweakerWebInterfaceServer.HTML_SEGMENT_TEMPLATE % (*([s] * 5), s + 1) + ''.join(GPXTweakerWebInterfaceServer.HTML_POINT_TEMPLATE % (*([pt[0]] * 6), *(a for b in zip(*([[str(pt[0])] * 5] * 3), map(f, pt[1])) for a in b)) for pt in self.Track.Pts[s]) +   '</div>' for s in range(len(self.Track.Pts)))

  def _build_waydots(self):
    return ''.join(GPXTweakerWebInterfaceServer.HTML_WAYDOT_TEMPLATE % (pt[0], *(lambda x, y: (x - self.Minx, self.Maxy - y))(*pt[1])) for pt in self.Track.WebMercatorWpts)

  def _build_dots(self):
    return ''.join(GPXTweakerWebInterfaceServer.HTML_DOT_TEMPLATE % (pt[0], *(lambda x, y: (x - self.Minx, self.Maxy - y))(*pt[1])) for s in range(len(self.Track.WebMercatorPts)) for pt in self.Track.WebMercatorPts[s])

  def _build_tsets(self):
    return ''.join('<option value="%s">%s</option>' % (*([html.escape(tset[0])] * 2),) for tset in self.TilesSets)

  def _build_esets(self):
    return ''.join('<option value="%s">%s</option>' % (*([html.escape(epro[0])] * 2),) for epro in self.ElevationsProviders)

  def _build_isets(self):
    return ''.join('<option value="%s">%s</option>' % (*([html.escape(ipro[0])] * 2),) for ipro in self.ItinerariesProviders)

  def BuildHTML(self):
    if self.HTML == None:
      return False
    defx, defy = WGS84WebMercator.WGS84toWebMercator(self.DefLat, self.DefLon)
    declarations = GPXTweakerWebInterfaceServer.HTML_DECLARATIONS_TEMPLATE.replace('##PORTMIN##', str(self.Ports[0])).replace('##PORTMAX##', str(self.Ports[1])).replace('##GPUCOMP##', str(self.GpuComp)).replace('##MODE##', self.Mode).replace('##VMINX##', str(self.VMinx)).replace('##VMAXX##', str(self.VMaxx)).replace('##VMINY##', str(self.VMiny)).replace('##VMAXY##', str(self.VMaxy)).replace('##DEFX##', str(defx)).replace('##DEFY##', str(defy)).replace('##TTOPX##', str(self.Minx)).replace('##TTOPY##', str(self.Maxy)).replace('##TWIDTH##', '0' if self.Mode == 'tiles' else str(self.Map.MapInfos['width'])).replace('##THEIGHT##', '0' if self.Mode == 'tiles' else str(self.Map.MapInfos['height'])).replace('##TEXT##', '' if self.Mode == 'tiles' else ('.jpg' if self.Map.MapInfos.get('format') == 'image/jpeg' else ('.png' if self.Map.MapInfos.get('format') == 'image/png' else '.img'))).replace('##TSCALE##', '1' if self.Mode =='tiles' else str(self.Map.MapResolution)).replace('##HTOPX##', str(self.Minx)).replace('##HTOPY##', str(self.Maxy))
    pathes = self._build_pathes()
    waydots = self._build_waydots()
    dots = self._build_dots()
    waypoints = self._build_waypoints()
    points = self._build_points()
    tsets = self._build_tsets()
    esets = self._build_esets()
    isets = self._build_isets()
    self.HTML = GPXTweakerWebInterfaceServer.HTML_TEMPLATE.replace('##DECLARATIONS##', declarations).replace('##TSETS##', tsets).replace('##ESETS##', esets).replace('##ISETS##', isets).replace('##EGTHRESHOLD##', str(self.EleGainThreshold)).replace('##AGTHRESHOLD##', str(self.AltGainThreshold)).replace('##SLRANGE##', str(self.SlopeRange)).replace('##SLMAX##', str(self.SlopeMax)).replace('##SPRANGE##', str(self.SpeedRange)).replace('##SPMAX##', str(self.SpeedMax)).replace('##NAME##', html.escape(self.Track.Name)).replace('##WAYPOINTTEMPLATE##', GPXTweakerWebInterfaceServer.HTML_WAYPOINT_TEMPLATE.replace('checked', '')).replace('##POINTTEMPLATE##',  GPXTweakerWebInterfaceServer.HTML_POINT_TEMPLATE.replace('checked', '')).replace('##WAYDOTTEMPLATE##',  GPXTweakerWebInterfaceServer.HTML_WAYDOT_TEMPLATE).replace('##DOTTEMPLATE##',  GPXTweakerWebInterfaceServer.HTML_DOT_TEMPLATE).replace('##WAYPOINTS##', waypoints).replace('##POINTS##', points).replace('##PATHES##', pathes).replace('##WAYDOTS##', waydots).replace('##DOTS##', dots)
    self.log(2, 'built')
    return True

  def Build3DHTML(self):
    self.HTML3D = None
    self.HTML3DData = None
    if next((p for seg in self.Track.Pts for p in seg), None) == None:
      return False
    self.log(1, '3dbuild')
    vminlat, vminlon = WGS84WebMercator.WebMercatortoWGS84(self.VMinx, self.VMiny)
    vmaxlat, vmaxlon = WGS84WebMercator.WebMercatortoWGS84(self.VMaxx, self.VMaxy)
    minlat = max(vminlat, min(p[1][0] for seg in self.Track.Pts for p in seg) - 0.005)
    maxlat = min(vmaxlat, max(p[1][0] for seg in self.Track.Pts for p in seg) + 0.005)
    minlon = max(vminlon, min(p[1][1] for seg in self.Track.Pts for p in seg) - 0.006)
    maxlon = min(vmaxlon, max(p[1][1] for seg in self.Track.Pts for p in seg) + 0.006)
    try:
      if self.EMode == 'map':
        tminlat, tminlon, tmaxlat, tmaxlon = list(map(float, self.Elevation.MapInfos['bbox'].split(',')))
        if tminlat > minlat or tminlon > minlon or tmaxlat < maxlat or tmaxlon < maxlon:
          self.log(0, '3derror1')
          return False
      elif self.EMode == 'tiles':
        infos = {**self.ElevationsProviders[self.ElevationProviderSel][1]}
        if not self.Elevation.AssembleMap(infos, self.ElevationsProviders[self.ElevationProviderSel][1].get('matrix'), minlat, maxlat, minlon, maxlon, **self.ElevationsProviders[self.ElevationProviderSel][2]):
          self.log(0, '3derror1')
          return False
      elif self.EMode == 'api':
        infos = {**self.ElevationsProviders[self.ElevationProviderSel][1]}
        if not self.Elevation.GenerateBil32Map(infos, minlat, maxlat, minlon, maxlon, 65536, **self.ElevationsProviders[self.ElevationProviderSel][2], threads=(self.TilesBufferThreads or 10)):
          self.log(0, '3derror1')
          return False
      else:
        self.log(0, '3derror1')
        return False
    except:
      self.log(0, '3derror1')
      return False
    if self.Elevation.MapInfos.get('format') != 'image/x-bil;bits=32' and self.Elevation.MapInfos.get('format') != 'image/hgt':
      self.log(0, '3derror1')
      return False
    scale = self.Elevation.MapResolution
    width = self.Elevation.MapInfos['width']
    height = self.Elevation.MapInfos['height']
    tminlat, tminlon, tmaxlat, tmaxlon = list(map(float, self.Elevation.MapInfos['bbox'].split(',')))
    minpx = max(0, math.floor((minlon - tminlon) / scale))
    minlon = tminlon + (minpx + 0.5) * scale
    maxpx = min(math.floor((maxlon - tminlon) / scale), width - 1)
    maxlon = tminlon + (maxpx + 0.5) * scale
    minpy = max(0, math.floor((tmaxlat - maxlat) / scale))
    maxlat = tmaxlat - (minpy + 0.5) * scale
    maxpy = min(math.floor((tmaxlat - minlat) / scale), height - 1)
    minlat = tmaxlat - (maxpy + 0.5) * scale
    if self.Elevation.MapInfos['format'] == 'image/x-bil;bits=32':
      e_f = '<f'
      e_s = 4
    else:
      e_f = '>h'
      e_s = 2
    if self.EMode == 'api':
      stepx = 1
      stepy = 1
    else:
      step = math.sqrt((maxpx - minpx + 1) * (maxpy - minpy + 1) / 262144)
      c = math.sqrt(math.cos(minlat))
      stepy = math.ceil(step)
      if math.ceil(step * c) < stepy:
        stepx = math.ceil(step / c)
        stepy = math.ceil(step * c)
      else:
        stepx = stepy
    lpx = list(range(minpx, maxpx, stepx)) or [minpx]
    lpx.append(maxpx)
    lpy = list(range(minpy, maxpy, stepy)) or [minpy]
    lpy.append(maxpy)
    lpy.reverse()
    nrow = len(lpy)
    ncol = len(lpx)
    ef = lambda e: e if e != self.Elevation.MapInfos.get('nodata') and e > -100 else 0
    eles = list(list(ef(struct.unpack(e_f, self.Elevation.Map[e_s * (min(py, height - 1) * width + min(px, width - 1)): e_s * (min(py, height - 1) * width + min(px, width - 1)) + e_s])[0]) for px in lpx) for py in lpy)
    minele = min(eles[row][col] for row in range(nrow) for col in range(ncol))
    maxele = max(eles[row][col] for row in range(nrow) for col in range(ncol))
    minx, miny = WGS84WebMercator.WGS84toWebMercator(minlat, minlon)
    maxx, maxy = WGS84WebMercator.WGS84toWebMercator(maxlat, maxlon)
    xy_den = max(maxx - minx, maxy - miny) / 2
    z_den = (maxele - minele) / 2
    if xy_den > z_den:
      den = xy_den
      zfactor = xy_den / z_den
    else:
      den = z_den
      zfactor = 1
    moyx = (minx + maxx) / 2
    moyy = (miny + maxy) / 2
    self.HTML3DData = struct.pack('L', ncol) + b''.join(struct.pack('f', (WGS84WebMercator.WGS84toWebMercator(tmaxlat, tminlon + (px + 0.5) * scale)[0] - moyx) / den) for px in lpx) + struct.pack('L', nrow) + b''.join(struct.pack('f', (WGS84WebMercator.WGS84toWebMercator(tmaxlat - (py + 0.5) * scale, tminlon)[1] - moyy) / den) for py in lpy) + struct.pack('L', ncol * nrow) + b''.join(struct.pack('f', (eles[r][c] - minele) / den - 1) for r in range(nrow) for c in range(ncol)) + struct.pack('L', len(self.Track.WebMercatorPts)) + b''.join(struct.pack('L', len(self.Track.WebMercatorPts[s])) + b''.join(struct.pack('f', (pt[1][0] - moyx) / den) + struct.pack('f', (pt[1][1] - moyy) / den) for pt in self.Track.WebMercatorPts[s]) for s in range(len(self.Track.WebMercatorPts)))
    self.log(2, '3dmodeled', ncol * nrow, ncol, nrow, self.Elevation.MapInfos.get('source', ''))
    if self.Mode == 'map':
      minrow, mincol = 1, 1
      maxrow, maxcol = 1, 1
      tminx, tminy = self.VMinx, self.VMiny
      tmaxx, tmaxy = self.VMaxx, self.VMaxy
      tpath = '"/map/map"'
    elif self.Mode == 'tiles':
      try:
        infos = {**self.Map.TilesInfos}
        (minrow, mincol), (maxrow, maxcol) = WebMercatorMap.WGS84BoxtoTileBox(infos, minlat, maxlat, minlon, maxlon)
      except:
        self.log(0, '3derror2')
        return False
      scale = infos['scale'] / WebMercatorMap.CRS_MPU
      tminx = infos['topx'] + scale * infos['width'] * mincol
      tminy = infos['topy'] - scale * infos['height'] * (maxrow + 1)
      tmaxx = infos['topx'] + scale * infos['width'] * (maxcol + 1)
      tmaxy = infos['topy'] - scale * infos['height'] * minrow
      tpath = '"/tiles/tile-" + row.toString() + "-" + col.toString() + ".?%s,%s"' % (str(self.TilesSet), str(self.Map.TilesInfos['matrix']))
    else:
      self.log(0, '3derror2')
      return False
    ax = 2 * den / (tmaxx - tminx)
    bx = (moyx - tminx - den) / (tmaxx - tminx)
    ay = 2 * den / (tmaxy - tminy)
    by = (moyy - tminy - den) / (tmaxy - tminy)
    declarations = GPXTweakerWebInterfaceServer.HTML_3D_DECLARATIONS_TEMPLATE.replace('##PORTMIN##', str(self.Ports[0])).replace('##PORTMAX##', str(self.Ports[1])).replace('##ZFACTMAX##', str(zfactor)).replace('##MPOS##', str('%f, %f, %f, %f' % (ax, ay, bx, by))).replace('##TMINROW##', str(minrow)).replace('##TMINCOL##', str(mincol)).replace('##TMAXROW##', str(maxrow)).replace('##TMAXCOL##', str(maxcol))
    self.HTML3D = GPXTweakerWebInterfaceServer.HTML_3D_TEMPLATE.replace('##DECLARATIONS##', declarations).replace('##TILEPATH##', tpath)
    self.log(0, '3dbuilt')
    return True

  def _build_folders_exp(self):
    return ''.join(GPXTweakerWebInterfaceServer.HTMLExp_FOLDER_TEMPLATE % (f, *([f, html.escape(self.Folders[f])] * 2)) for f in range(len(self.Folders)))

  def _build_pathes_exp(self):
    f = lambda e: '' if e == None else html.escape(e) if isinstance(e, str) else e
    def _coord_to_vb(x, y):
      return '%.1f %.1f' % (x - self.Minx, self.Maxy - y)
    pathes = ''
    pathes = ''.join(GPXTweakerWebInterfaceServer.HTMLExp_PATH_TEMPLATE.replace('##WIDTH##', 'calc(%.1fpx / var(--scale))' % (self.TracksBoundaries[t][1] - self.TracksBoundaries[t][0])).replace('##HEIGHT##', 'calc(%.1fpx / var(--scale))' % (self.TracksBoundaries[t][3] - self.TracksBoundaries[t][2])).replace('##LEFT##', 'calc(%.1fpx / var(--scale))' % (self.TracksBoundaries[t][0] - self.Minx)).replace('##TOP##', 'calc(%.1fpx / var(--scale))' % (self.Maxy - self.TracksBoundaries[t][3])).replace('##VIEWBOX##', '%.1f %.1f %.1f %.1f' % (0, 0, self.TracksBoundaries[t][1] - self.TracksBoundaries[t][0], self.TracksBoundaries[t][3] - self.TracksBoundaries[t][2])).replace('##ARROWS##', "&rsaquo; " * 500) % (t, *([self.Tracks[t][1].Color or '#000000'] * 2), t, f(self.Tracks[t][1].Name), t, t) for t in range(len(self.Tracks)))
    return pathes

  def _build_tracks_exp(self):
    f = lambda e: '' if e == None else html.escape(e) if isinstance(e, str) else e
    return ''.join(GPXTweakerWebInterfaceServer.HTMLExp_TRACK_TEMPLATE % (*([t] * 3), f(self.Tracks[t][0]), *([t] * 2), *([f(self.Tracks[t][1].Name)] * 2), t, self.Tracks[t][1].Color or '#000000', t, *(a for b in zip(*([[t] * 5] * 3), map(f, (self.Tracks[t][1].Name, *self.Tracks[t][0].rpartition('\\')[::-2], '', '{jtrackcontent}'.format_map(LSTRINGS['interface']) % (str(len(self.Tracks[t][1].Pts)) , str(sum(len(s) for s in self.Tracks[t][1].Pts)), str(len(self.Tracks[t][1].Wpts)))))) for a in b)) for t in range(len(self.Tracks)))

  def _build_waydots_exp(self):
    f = lambda e: '' if e == None else html.escape(e) if isinstance(e, str) else e
    def _coord_to_vb(x, y, t):
      return '%.1f' % (x - self.TracksBoundaries[t][0]), '%.1f' % (self.TracksBoundaries[t][3] - y)
    return ''.join(GPXTweakerWebInterfaceServer.HTMLExp_WAYDOTS_TEMPLATE.replace('##WIDTH##', 'calc(%.1fpx / var(--scale))' % (self.TracksBoundaries[t][1] - self.TracksBoundaries[t][0])).replace('##HEIGHT##', 'calc(%.1fpx / var(--scale))' % (self.TracksBoundaries[t][3] - self.TracksBoundaries[t][2])).replace('##LEFT##', 'calc(%.1fpx / var(--scale))' % (self.TracksBoundaries[t][0] - self.Minx)).replace('##TOP##', 'calc(%.1fpx / var(--scale))' % (self.Maxy - self.TracksBoundaries[t][3])).replace('##VIEWBOX##', '%.1f %.1f %.1f %.1f' % (0, 0, self.TracksBoundaries[t][1] - self.TracksBoundaries[t][0], self.TracksBoundaries[t][3] - self.TracksBoundaries[t][2])) % (t, *([self.Tracks[t][1].Color or '#000000'] * 2), ''.join(GPXTweakerWebInterfaceServer.HTMLExp_WAYDOT_TEMPLATE % (*_coord_to_vb(*WGS84Track.WGS84toWebMercator(*pt[1][0:2]), t), f(pt[1][4])) for pt in self.Tracks[t][1].Wpts)) for t in range(len(self.Tracks)))

  def BuildHTMLExp(self):
    if self.HTMLExp == None:
      return False
    defx, defy = WGS84WebMercator.WGS84toWebMercator(self.DefLat, self.DefLon)
    declarations = GPXTweakerWebInterfaceServer.HTML_DECLARATIONS_TEMPLATE.replace('##PORTMIN##', str(self.Ports[0])).replace('##PORTMAX##', str(self.Ports[1])).replace('##GPUCOMP##', str(self.GpuComp)).replace('##MODE##', self.Mode).replace('##VMINX##', str(self.VMinx)).replace('##VMAXX##', str(self.VMaxx)).replace('##VMINY##', str(self.VMiny)).replace('##VMAXY##', str(self.VMaxy)).replace('##DEFX##', str(defx)).replace('##DEFY##', str(defy)).replace('##TTOPX##', str(self.Minx)).replace('##TTOPY##', str(self.Maxy)).replace('##TWIDTH##', '0' if self.Mode == 'tiles' else str(self.Map.MapInfos['width'])).replace('##THEIGHT##', '0' if self.Mode == 'tiles' else str(self.Map.MapInfos['height'])).replace('##TEXT##', '' if self.Mode == 'tiles' else ('.jpg' if self.Map.MapInfos.get('format') == 'image/jpeg' else ('.png' if self.Map.MapInfos.get('format') == 'image/png' else '.img'))).replace('##TSCALE##', '1' if self.Mode =='tiles' else str(self.Map.MapResolution)).replace('##HTOPX##', str(self.Minx)).replace('##HTOPY##', str(self.Maxy))
    folders = self._build_folders_exp()
    pathes = self._build_pathes_exp()
    waydots = self._build_waydots_exp()
    tracks = self._build_tracks_exp()
    tsets = self._build_tsets()
    self.HTMLExp = GPXTweakerWebInterfaceServer.HTMLExp_TEMPLATE.replace('##DECLARATIONS##', declarations).replace('##TSETS##', tsets).replace('##FOLDERS##', folders).replace('##EGTHRESHOLD##', str(self.EleGainThreshold)).replace('##AGTHRESHOLD##', str(self.AltGainThreshold)).replace('##SLRANGE##', str(self.SlopeRange)).replace('##SLMAX##', str(self.SlopeMax)).replace('##SPRANGE##', str(self.SpeedRange)).replace('##SPMAX##', str(self.SpeedMax)).replace('##NBTRACKS##', str(len(self.Tracks))).replace('##TRACKS##', tracks).replace('##PATHES##', pathes).replace('##WAYDOTS##', waydots)
    self.log(2, 'builtexp')
    return True

  def EditMode(self):
    if self.HTML == None:
      return False
    if self.Mode == 'tiles':
      if self.HTML != '':
        minlat = min((p[1][0] for seg in (*self.Track.Pts, self.Track.Wpts) for p in seg), default=self.DefLat)
        maxlat = max((p[1][0] for seg in (*self.Track.Pts, self.Track.Wpts) for p in seg), default=self.DefLat)
        minlon = min((p[1][1] for seg in (*self.Track.Pts, self.Track.Wpts) for p in seg), default=self.DefLon)
        maxlon = max((p[1][1] for seg in (*self.Track.Pts, self.Track.Wpts) for p in seg), default=self.DefLon)
        self.Minx, self.Miny = WGS84WebMercator.WGS84toWebMercator(max(self.VMinLat, minlat - 0.008), max(self.VMinLon, minlon - 0.011))
        self.Maxx, self.Maxy = WGS84WebMercator.WGS84toWebMercator(min(self.VMaxLat, maxlat + 0.008), min(self.VMaxLon, maxlon + 0.011))
      else:
        self.Minx, self.Maxx, self.Miny, self.Maxy = self.TracksBoundaries[self.Track.Ind]
    self.HTML = ''
    self.log(1, 'build')
    if not self.Track.BuildWebMercator():
      self.log(0, 'berror1')
      return False
    if self.BuildHTML():
      self.log(1, 'built')
      return True
    else:
      return False

  def ExploreMode(self):
    if self.HTMLExp == None:
      return False
    self.HTML = None
    self.HTMLExp = ''
    if self.Track != None:
      if self.Track.OTrack != self.Track.STrack:
        try:
          self.Track.OTrack.unlink()
        except:
          pass
        self.Track.OTrack = self.Track.STrack
      if self.Track.Track != self.Track.STrack:
        try:
          self.Track.Track.unlink()
        except:
          pass
        self.Track.Track = self.Track.STrack
      self.Track.ProcessGPX('a')
      if self.Mode == 'tiles':
        self.TracksBoundaries[self.Track.Ind] = (self.Minx, self.Maxx, self.Miny, self.Maxy)
        self.Minx = min((b[0] for b in self.TracksBoundaries), default=self.Minx)
        self.Maxx = max((b[1] for b in self.TracksBoundaries), default=self.Maxx)
        self.Miny = min((b[2] for b in self.TracksBoundaries), default=self.Miny)
        self.Maxy = max((b[3] for b in self.TracksBoundaries), default=self.Maxy)
      for track in self.Tracks:
        if track[1] != self.Track and track[0] == self.Uri:
          try:
            track[1].Track.unlink()
          except:
            pass
          track[1].Track = self.Track.Track.cloneNode(True)
          track[1].ProcessGPX('w')
          track[1].OTrack = track[1].Track
          track[1].STrack = track[1].Track
    self.log(1, 'buildexp')
    if self.BuildHTMLExp():
      if self.Track != None:
        self.HTMLExp = self.HTMLExp.replace('var focused = ""', 'var focused = "track' + str(self.Track.Ind) + '"')
        self.Track = None
      self.log(1, 'builtexp')
      return True
    else:
      return False    

  def _start_webserver(self, ind):
    with ThreadedDualStackServer((self.Ip, self.Ports[0] + ind), GPXTweakerRequestHandler) as self.GPXTweakerInterfaceServerInstances[ind]:
      self.GPXTweakerInterfaceServerInstances[ind].Interface = self
      self.GPXTweakerInterfaceServerInstances[ind].serve_forever()

  def run(self):
    try:
      if not (self.EditMode() if self.Uri != None else self.ExploreMode()):
        return False
    except:
      return False
    self.log(0, 'start')
    for ind in range(self.Ports[1] - self.Ports[0] + 1):
      webserver_thread = threading.Thread(target=self._start_webserver, args=(ind,))
      webserver_thread.start()
    return True

  def shutdown(self):
    self.log(0, 'close')
    for ind in range(self.Ports[1] - self.Ports[0] + 1):
      try:
        self.GPXTweakerInterfaceServerInstances[ind].shutdown()
      except:
        pass
    try:
      if self.Mode == 'tiles':
        self.Map.Tiles.Close()
    except:
      pass


if __name__ == '__main__':
  formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=119)
  CustomArgumentParser = partial(argparse.ArgumentParser, formatter_class=formatter)
  parser = CustomArgumentParser()
  parser.add_argument('uri', metavar='URI', help=LSTRINGS['parser']['uri'], nargs='?', default=None)
  parser.add_argument('--conf', '-c', metavar='CONF', help=LSTRINGS['parser']['conf'], default='')
  parser.add_argument('--trk', '-t', metavar='TRK', help=LSTRINGS['parser']['trk'], type=int, default=None)
  parser.add_argument('--map', '-m', metavar='MAP', help=LSTRINGS['parser']['map'], nargs ='?', const=' ', default='')
  parser.add_argument('--emap', '-e', metavar='EMAP', help=LSTRINGS['parser']['emap'], nargs ='?', const=' ', default='')
  parser.add_argument('--box', '-b', metavar='BOX', help=LSTRINGS['parser']['box'], type=(lambda b: (list((p,q,r,s) for [p,q,r,s] in (map(float, map(str.strip, b.split(','))),))[0]) if b != '' else (None, ) * 4), default='')
  parser.add_argument('--size', '-s', metavar='SIZE', help=LSTRINGS['parser']['size'], type=(lambda b: (list((p,q) for [p,q] in (map(int, map(str.strip, b.split(','))),))[0]) if b != '' else (None, ) * 2), default='')
  parser.add_argument('--noopen', '-n', help=LSTRINGS['parser']['noopen'], action='store_true')
  parser.add_argument('--verbosity', '-v', metavar='VERBOSITY', help=LSTRINGS['parser']['verbosity'], type=int, choices=[0,1,2], default=0)
  args = parser.parse_args()
  if args.uri != None:
    if args.uri.rpartition('.')[2] != 'gpx':
      parser.error(LSTRINGS['parser']['gpx'])
  VERBOSITY = args.verbosity
  try:
    GPXTweakerInterface = GPXTweakerWebInterfaceServer(uri=args.uri, trk=args.trk if args.uri != None else None, bmap=(args.map or None), emap=(args.emap or None), map_minlat=args.box[0], map_maxlat=args.box[1], map_minlon=args.box[2], map_maxlon=args.box[3], map_maxheight=(args.size[0] or 2000), map_maxwidth=(args.size[1] or 4000), map_resolution=((WGS84WebMercator.WGS84toWebMercator(args.box[1], args.box[3])[0] - WGS84WebMercator.WGS84toWebMercator(args.box[0], args.box[2])[0]) / args.size[0] if not (None in args.box or None in args.size) else None), cfg=((os.path.expandvars(args.conf).rstrip('\\') or os.path.dirname(os.path.abspath(__file__))) + '\GPXTweaker.cfg'))
  except:
    log('interface', 0, 'berror')
    exit()
  if not GPXTweakerInterface.run():
    exit()
  if args.noopen:
    print(LSTRINGS['parser']['open'] % ('http://%s:%s/GPX%s.html' % (GPXTweakerInterface.Ip, GPXTweakerInterface.Ports[0], ('Tweaker' if args.uri != None else 'Explorer'))))
  else:
    webbrowser.open('http://%s:%s/GPX%s.html' % (GPXTweakerInterface.Ip, GPXTweakerInterface.Ports[0], ('Tweaker' if args.uri != None else 'Explorer')))
  print(LSTRINGS['parser']['keyboard'])
  while True:
    k = msvcrt.getch()
    if k == b'\xe0':
      k = msvcrt.getch()
      k = b''
    if k.upper() == b'S':
        break
  GPXTweakerInterface.shutdown()
