# GPXTweaker v1.16.0 (https://github.com/PCigales/GPXTweaker)
# Copyright © 2022 PCigales
# This program is licensed under the GNU GPLv3 copyleft license (see https://www.gnu.org/licenses)

from functools import partial
import urllib.parse
import socket
import selectors
import ssl
import math
from xml.dom import minidom
from xml.parsers import expat
from html import escape
import socketserver
import email.utils
import time
import threading
import os, os.path
import multiprocessing
from pathlib import Path
import re
import json
import base64
import zlib
import gzip
import lzma
import zipfile
from io import BytesIO, StringIO
import ctypes, ctypes.wintypes
import subprocess
import struct
import array
from collections import deque
import types
import sys
import uuid
import webbrowser
import msvcrt
import locale
import argparse
import gc
import pickle

locale.setlocale(locale.LC_TIME, '')

FR_STRINGS = {
  'tilescache': {
    '_id': 'Cache de tuiles',
    'init': 'initialisation (taille: %s, fils: %s)',
    'get': 'tuile (%s, %s) demandée',
    'cancel': 'abandon de la fourniture de la tuile (%s, %s)',
    'found': 'tuile (%s, %s) trouvée dans le cache',
    'del': 'réduction du cache',
    'add': 'ajout de la tuile (%s, %s) dans le cache portant sa longueur à %s',
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
    'tileretrieved': 'tuile %s fournie'
  },
  'jsontiles': {
    '_id': 'Gestionnaire de jeu de tuiles json',
    'styleload': 'chargement du style %s',
    'stylecloaded': 'style %s chargé depuis le cache',
    'stylelfound': 'style %s trouvé localement',
    'stylelexpired': 'style local %s expiré',
    'stylefetch': 'récupération du style %s',
    'styleloaded': 'style %s chargé',
    'stylefail': 'échec du chargement du style %s',
    'glyphretrieve': 'fourniture du glyph %s [%s - %s]',
    'glyphcretrieved': 'glyph %s [%s - %s] fourni depuis le cache',
    'glyphlfound': 'glyph %s [%s - %s] trouvé localement',
    'glyphlexpired': 'glyph local %s [%s - %s] expiré',
    'glyphfetch': 'récupération du glyph %s [%s - %s]',
    'glyphretrieved': 'glyph %s [%s - %s] fourni',
    'glyphfail': 'échec de la fourniture du glyph %s [%s - %s]',
    'spritejsonretrieve': 'fourniture du sprite json %s [%s]',
    'spritejsoncretrieved': 'sprite json %s [%s] fourni depuis le cache',
    'spritejsonlfound': 'sprite json %s [%s] trouvé localement',
    'spritejsonlexpired': 'sprite json local %s [%s] expiré',
    'spritejsonfetch': 'récupération du sprite json %s [%s]',
    'spritejsonretrieved': 'sprite json %s [%s] fourni',
    'spritejsonfail': 'échec de la fourniture du sprite json %s [%s]',
    'spritepngretrieve': 'fourniture du sprite png %s [%s]',
    'spritepngcretrieved': 'sprit png %s [%s] fourni depuis le cache',
    'spritepnglfound': 'sprite png %s [%s] trouvé localement',
    'spritepnglexpired': 'sprite png local %s [%s] expiré',
    'spritepngfetch': 'récupération du sprite png %s [%s]',
    'spritepngretrieved': 'sprite png %s [%s] fourni',
    'spritepngfail': 'échec de la fourniture du sprite png %s [%s]',
  },
  'legend': {
    '_id': 'Gestionnaire de légende',
    'legendretrieve': 'fourniture de la légende %s',
    'legendretrieved1': 'légende %s fournie: %s composant(s)',
    'legendlfound': 'légende %s trouvée localement',
    'legendlexpired': 'légende locale %s expirée',
    'legendfetch': 'récupération de la légende %s',
    'legendfail': 'échec de la fourniture de la légende %s',
    'legendretrieved2': 'légende %s fournie'
  },
  'track': {
    '_id': 'Gestionnaire de trace',
    'init': 'initialisation',
    'load': 'chargement de la trace %s',
    'new': 'création d\'une nouvelle trace sous %s',
    'oerror': 'échec du chargement du fichier %s',
    'lerror': 'échec du chargement de la trace %s',
    'perrorw': 'donnée invalide: point de cheminement %s',
    'perrorp': 'donnée invalide: segment %s - point %s',
    'loaded': 'trace %s chargée (nom: "%s", points de cheminement: %s, segments: %s, points: %s)',
    'save': 'enregistrement de la trace sous %s',
    'serror': 'échec de l\'enregistrement de la trace sous %s',
    'saved': 'trace enregistrée sous %s'
  },
  'geomedia': {
     '_id': 'Gestionnaire de médias géolocalisés',
     'mdlerror': 'échec de la récupération des données du média %s',
     'mdloaded': 'données du média %s récupérées',
     'mskipped': 'média %s sauté car débordant de la vue',
     'mtloaded': '%d photo(s) et %d vidéo(s) prise(s) en compte en %.1fs',
     'moerror': 'échec de l\'ouverture du média %s',
     'mopened': 'média %s ouvert'
  },
  'loader': {
     '_id': 'Chargeur de traces',
     'init': 'initialisation (processus de travail: %s)',
     'rtrack': 'réception des données de la trace %s <%s>',
     'itrack': 'interruption de la réception des données de trace',
     'etrack': 'fin de la réception des données de trace',
     'wstart': 'processus de travail %s - démarrage',
     'wload': 'processus de travail %s - prise en charge du chargement du fichier %s',
     'wiqueue': 'processus de travail %s - mise en queue des données de la trace %s <%s>',
     'wsqueue': 'processus de travail %s - transfert des données de la trace %s <%s>',
     'weload': 'processus de travail %s - fin du chargement de fichier',
     'wrdoc': 'processus de travail %s - réception de la demande de transfert du document du fichier %s',
     'wsdoc': 'processus de travail %s - transfert du document du fichier %s',
     'winterrupt': 'processus de travail: %s - interruption',
     'wend': 'processus de travail: %s - arrêt',
     'rstarty': 'démarrage du gestionnaire de rapatriement de document de fichier (par anticipation: oui)',
     'rstartn': 'démarrage du gestionnaire de rapatriement de document de fichier (par anticipation: non)',
     'rrequest': 'gestionnaire de rapatriement - réception de la demande de récupération de la trace %s <%s>',
     'rhandle': 'gestionnaire de rapatriement - récupération anticipée de la trace %s <%s>',
     'rabort': 'gestionnaire de rapatriement - trace %s <%s> déjà récupérée',
     'rretrieved': 'gestionnaire de rapatriement - trace %s <%s> récupérée',
     'rend': 'fin du rapatriement de document de fichier',
     'rstop': 'arrêt du gestionnaire de rapatriement de document de fichier',
     'close': 'fermeture'
  },
  'interface': {
    '_id': 'Interface',
    'conf': 'chargement de la configuration',
    'cerror': 'échec du chargement de la configuration (%s)',
    'cloaded': 'configuration chargée',
    'build': 'génération de la page d\'interface',
    'buildexp': 'génération de la page d\'interface de l\'explorateur',
    'bloaded1': '%s trace(s) chargée(s) en %.1fs',
    'bloaded2': '%s trace(s) chargée(s) en %.1fs, %s trace(s) sautée(s), %s trace(s) rejetée(s), %s fichier(s) gpx rejeté(s)',
    'berror': 'échec de la génération de la page d\'interface',
    'berror1': 'échec de la génération de la page d\'interface (conversion en WebMercator)',
    'berror2': 'échec de la génération de la page d\'interface (carte extérieure au cadre)',
    'berror3': 'échec de la génération de la page d\'interface (carte "%s" pas définie)',
    'berror4': 'échec de la génération de la page d\'interface (trace débordant de la vue)',
    'berror5': 'échec de la génération de la page d\'interface (paramètres de jeux ou de cache de tuiles)',
    'berror6': 'trace sautée car débordant de la vue',
    'berrori': 'génération de la page d\'interface interrompue',
    'elevation': 'fournisseur d\'élévations configuré (%s)',
    'eerror': 'échec de la configuration du fournisseur d\'élévations (%s)',
    'itinerary': 'fournisseur d\'itinéraires configuré (%s)',
    'reversegeocoding': 'fournisseur de géocodages inversés configuré (%s)',
    'maplibre': 'Ce programme fait appel à la bibliothèque MapLibre GL JS (https://github.com/maplibre/maplibre-gl-js), sous licence BSD 3-Clause, pour l\'affichage des jeux de tuiles définis à partir d\'un style au format JSON, par import depuis %s',
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
    'jfconfirm': 'Lisser la trace dans son ensemble ?',
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
    'jdatetime': 'focus sur segment ou point / pas de focus: compléter par inter/extra polation l\'horodatage de l\'élément / la trace&#13;&#10;+shift: supprimer l\'horodatage',
    'jsave': 'sauvegarder la trace&#13;&#10;(puis recharger la page pour éliminer irréversiblement les éléments désactivés)',
    'jswitchpoints': 'afficher / masquer les marques de point et point de cheminement&#13;&#10;+ctrl: afficher / masquer les contrôles du filtre de lissage&#13;&#10;+shift: lisser le segment / la trace (attention, une valeur de plage de distance de filtrage élevée ou une application répétée du lissage altèrera probablement la trace)',
    'jgraph': 'afficher / masquer le graphique&#13;&#10;+shift: afficher / masquer les contrôles du filtre de calcul de dénivelé&#13;&#10;+ctrl: afficher / masquer les contrôles du filtre de calcul de pente&#13;&#10;+alt: afficher / masquer les contrôles du filtre de calcul de vitesse',
    'j3dviewer': 'ouvrir la visionneuse 3D en mode vue panoramique&#13;&#10;+alt: ouvrir la visionneuse 3D en mode vue subjective&#13;&#10;+ctrl: afficher / masquer les contrôles de la marge autour de la trace',
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
    'jdownloadmap': 'télécharger une carte des traces cochées&#13;&#10;+shift: télécharger la liste des traces&#13;&#10;+alt: télécharger la liste des traces avec les points de cheminement&#13;&#10;+ctrl: télécharger le graphique affiché',
    'jswitchmedia': 'afficher / masquer les photos et vidéos&#13;&#10;+alt: ouvrir aussi / fermer le panneau de prévisualisation&#13;&#10;+ctrl: afficher / masquer les contrôles de taille de miniature',
    'jtrackdetach': 'détacher la trace (d\'un fichier multi-traces)',
    'jtrackintegrate': 'intégrer l\'autre trace cochée avant (dans un fichier multi-traces)&#13;&#10;+alt:intégrer l\'autre trace cochée après (dans un fichier multi-traces)',
    'jtrackincorporate': 'incorporer les points de cheminement et segments de l\'autre trace cochée',
    'jtracknew': 'créer une nouvelle trace vide dans le premier répertoire coché',
    'jtrackedit': 'éditer la trace',
    'jzoomall': 'recadrer sur toutes les traces cochées&#13;&#10;+alt: recadrer sur toutes les traces cochées et listées&#13;&#10;+shift: recadrer sur la trace qui a le focus',
    'jwebmapping': 'afficher le point de départ dans le service de cartographie en ligne',
    'jswitchsmooth': 'activer / désactiver le lissage des traces (∻ désactivé | ÷ activé)&#13;&#10;+ctrl: afficher / masquer les contrôles du filtre de lissage',
    'jtset': 'sélectionner le jeu de tuiles&#13;&#10;+shift: sélection du fournisseur d\'élévations&#13;&#10;+ctrl: sélection du fournisseur d\'itinéraires&#13;&#10;en mode superposition de jeux de tuiles, clic droit: afficher / masquer les contrôles de transparence de couche&#13;&#10;alt + clic droit: afficher la légende si disponible',
    'jeset': 'sélectionner le fournisseur d\'élévations&#13;&#10;+alt: sélection du jeu de tuiles&#13;&#10;+ctrl: sélection du fournisseur d\'itinéraires',
    'jiset': 'sélectionner le fournisseur d\'itinéraires&#13;&#10;+alt: sélection du jeu de tuiles&#13;&#10;+shift: sélection du fournisseur d\'élévations',
    'jexptset': 'sélectionner le jeu de tuiles&#13;&#10;+shift: sélection du fournisseur d\'élévations&#13;&#10;+ctrl: sélection du service de cartographie en ligne&#13;&#10;en mode superposition de jeux de tuiles, clic droit: afficher / masquer les contrôles de transparence de couche&#13;&#10;alt + clic droit: afficher la légende si disponible',
    'jexpeset': 'sélectionner le fournisseur d\'élévations&#13;&#10;+alt: sélection du jeu de tuiles&#13;&#10;+ctrl: sélection du service de cartographie en ligne',
    'jexpiset': 'sélectionner le service de cartographie en ligne&#13;&#10;+alt: sélection du jeu de tuiles&#13;&#10;+shift: sélection du fournisseur d\'élévations',
    'jminus': 'dézoomer&#13;&#10;+ctrl: atténuer&#13;&#10;+shift: éclaircir',
    'jexpminus': 'dézoomer&#13;&#10;+ctrl: atténuer&#13;&#10;+shift: éclaircir&#13;&#10;+alt: affiner',
    'jlock': 'verrouiller / déverrouiller le jeu de tuiles',
    'jplus': 'zoomer&#13;&#10;+ctrl: réaccentuer&#13;&#10;+shift: réassombrir',
    'jexpplus': 'zoomer&#13;&#10;+ctrl: réaccentuer&#13;&#10;+shift: réassombrir&#13;&#10;+alt: épaissir',
    'jdfpanel': 'Plage lissage points',
    'jmtpanel': 'Taille des miniatures',
    'jpixels': '&nbsp;pixels',
    'jfilterpanel1': 'Seuils calcul dénivelé',
    'jfilterpanel2': 'Plages calcul pente',
    'jfilterpanel3': 'Plages calcul vitesse',
    'jspduration': '&nbsp;durée',
    'jsmax': 'max&nbsp;&nbsp;&nbsp;',
    'j3dpanel': 'Marges vue 3D',
    'j3dpanoramic': 'panoram',
    'j3dsubjective': 'subject',
    'jopacityreset': 'double-clic pour rétablir la valeur d\'origine\\r\\n+shift: rétablir l\'ensemble des valeurs d\'origine',
    'jfoldersw': 'Répertoires:',
    'jscrollcross': 'centrer sur l\'élément qui a le focus&#13;&#10;+shift: recadrer sur la trace&#13;&#10;+ctrl: alterner entre les modes de défilement automatique de la carte (grisé: pas de défilement, bleu: défilement sur focus, vert: centrage sur focus et défilement sur survol)',
    'jhelp': 'clic-glisse gauche sur la carte pour la faire défiler&#13;&#10;roulette souris sur la carte pour la faire défiler verticalement&#13;&#10;shift + roulette souris sur la carte pour la faire défiler horizontalement&#13;&#10;ctrl + roulette souris sur la carte pour zoomer ou dézoomer&#13;&#10;alt + roulette souris sur la carte pour passer au point de cheminement / point / segment précédent ou suivant&#13;&#10;clic / clic-glisse gauche (+ shift / alt) sur le tracé d\'un point / point de cheminement pour le sélectionner / le déplacer (et effacer / conserver ses données d\'élévation, ou à défaut choisir selon si la distance est supérieure à 25m ou pas)&#13;&#10;ctrl + clic / clic-glisse gauche sur le tracé d\'un point pour le sélectionner / le déplacer et construire un chemin depuis le point précédent jusqu\'à celui-ci&#13;&#10;clic gauche sur le tracé d\'un segment pour le sélectionner&#13;&#10;clic droit sur la carte pour insérer un point après le point qui a le focus ou un point de cheminement sinon&#13;&#10;ctrl + clic droit sur la carte pour insérer un point après le point qui a le focus en mode suivi de chemin&#13;&#10;clic droit sur le tracé d\'un point / point de cheminement / segment pour le supprimer&#13;&#10;survol souris d\'un bouton pour afficher sa légende',
    'jexpscrollcross': 'centrer sur l\'élément qui a le focus&#13;&#10;+ctrl: alterner entre les modes de défilement automatique de la carte (grisé: pas de défilement, bleu: défilement sur focus, vert: centrage sur focus et défilement sur survol)',
    'jexphelp': 'clic-glisse gauche sur la carte pour la faire défiler&#13;&#10;roulette souris sur la carte pour la faire défiler verticalement&#13;&#10;shift + roulette souris sur la carte pour la faire défiler horizontalement&#13;&#10;ctrl + roulette souris sur la carte pour zoomer ou dézoomer&#13;&#10;alt + roulette souris sur la carte pour passer à la trace précédente ou suivante&#13;&#10;clic gauche sur le tracé d\'une trace pour la sélectionner&#13;&#10;clic gauche sur une photo / vidéo pour l\'afficher en grand puis clic gauche sur une photo pour activer / quitter le mode plein écran et clic droit pour revenir à l\'explorateur de traces&#13;&#10;clic droit sur le tracé d\'une trace pour la masquer&#13;&#10;survol souris d\'un bouton pour afficher sa légende',
    'jhelp3d': 'survol souris de la mini-carte pour afficher sa légende&#13;&#10;clic sur la vue 3d puis :&#13;&#10;flèche haut / bas ou roulette souris pour avancer / reculer&#13;&#10;flèche gauche / droite ou clic-glisse horizontal pour pivoter sur la gauche / droite&#13;&#10;page précédente / suivante  ou clic-glisse vertical pour incliner vers le haut / bas&#13;&#10;+shift pour accélérer le mouvement&#13;&#10;suppression ou clic roulette pour activer / désactiver la rotation automatique avec la progression&#13;&#10;insertion pour retirer l\'inclinaison&#13;&#10;moins / plus pour abaisser / élever la vue&#13;&#10;entrée ou, directement, double-clic pour activer / quitter le mode plein écran',
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
    'jexplorer': 'double-clic pour afficher dans l\'explorateur de fichier',
    'jfolder': 'Répe',
    'jperiod': 'Péri',
    'jcontent': 'Cont',
    'jtrackcontent': '%d seg(s) | %d pt(s) | %d pt(s) de chem',
    'jgraphdistance': 'distance',
    'jgraphelevation': 'élévation',
    'jgraphaltitude': 'altitude',
    'jgraphelegain': 'déniv élé',
    'jgraphaltgain': 'déniv alt',
    'jgrapheleslope': 'pente élé',
    'jgraphaltslope': 'pente alt',
    'jgraphspeed': 'vitesse',
    'jgraphtime': 'durée',
    'jmadjust': 'Ajustement de la carte (amplitude: %s - exposant: %s)',
    'jmundo1': 'Insertion de %s point(s) annulée',
    'jmundo2': 'Modification de %s point(s) annulée',
    'jmredo1': 'Insertion de %s point(s) rétablie',
    'jmredo2': 'Modification de %s point(s) rétablie',
    'jminsert1': 'Point de cheminement inséré',
    'jminsert2': 'Point inséré',
    'jmpathno': 'Aucun fournisseur d\'itinéraires configuré',
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
    'jmsegmentfilter1': 'Segment lissé: %s point(s) déplacé(s)',
    'jmsegmentfilter2': 'Trace lissée: %s point(s) déplacé(s)',
    'jmelevationsno': 'Aucune source d\'élévations configurée',
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
    'jmdatetime4': 'Horodatage du point supprimé',
    'jmdatetime5': 'Horodatages du segment supprimés',
    'jmdatetime6': 'Horodatages de la trace supprimés',
    'jmsave1': 'Sauvegarde en cours...',
    'jmsave2': 'Sauvegarde effectuée',
    'jmsave3': 'Échec de la sauvegarde',
    'jm3dviewer1': 'Chargement de la visionneuse 3D en cours...',
    'jm3dviewer2': 'Visionneuse 3D démarrée',
    'jm3dviewer3': 'Échec du chargement de la visionneuse 3D',
    'jm3dviewer4': 'Visionneuse 3D indisponible en mode superposition de jeux de tuiles ou jeu de tuile json',
    'jmmedia1': 'Récupération des données des médias en cours...',
    'jmmedia2': 'Récupération des données des médias effectuée',
    'jmmedia3': 'Échec de la récupération des données des médias',
    'jmdownmap1': 'Préparation de la carte en cours (phase 1/4)...',
    'jmdownmap2': 'Préparation de la carte en cours (phase 2/4)...',
    'jmdownmap3': 'Préparation de la carte en cours (phase 3/4)...',
    'jmdownmap4': 'Préparation de la carte en cours (phase 4/4)...',
    'jmdownmap5': 'Carte prête pour téléchargement (%s trace(s) - %s x %s)',
    'jmdownmap6': 'Échec de la préparation de la carte',
    'jmdownmap7': 'Carte trop grande, dézoom nécessaire',
    'jmopenlegend1': 'Récupération de la (des) légende(s) en cours...',
    'jmopenlegend2': 'Fin de la récupération de la (des) légende(s): %s légende(s) obtenue(s)',
    'jmdetach1': 'Détachement en cours...',
    'jmdetach2': 'Détachement effectué',
    'jmdetach3': 'Échec du détachement',
    'jmdetach4': 'Détachement annulé: trace ne faisant pas partie d\'un fichier multi-traces',
    'jmincorporate1': 'Incorporation en cours...',
    'jmincorporate2': 'Incorporation effectuée',
    'jmincorporate3': 'Échec de l\'incorporation',
    'jmincorporate4': 'Incorporation annulée: pas ou plus d\'une autre trace visible cochée',
    'jmintegrate1': 'Intégration en cours...',
    'jmintegrate2': 'Intégration effectuée',
    'jmintegrate3': 'Échec de l\'intégration',
    'jmintegrate4': 'Intégration annulée: pas ou plus d\'une autre trace visible cochée',
    'jmintegrate5': 'Intégration annulée: trace à intégrer faisant partie d\'un fichier multi-traces',
    'jmnew1': 'Création en cours...',
    'jmnew2': 'Création effectuée',
    'jmnew3': 'Échec de la création',
    'jtilt': 'Inclinaison:',
    'jrotation': 'Rotation:',
    'jzscale': 'Échelle Z:',
    'jzscaleiso': 'iso',
    'jzscalemax': 'max',
    'jtexture': 'Texture:',
    'jtextureyiso': 'Isoplèthes Y',
    'jtextureziso': 'Isoplèthes Z',
    'jtexturemap': 'Carte',
    'jtexturemaploading': 'Carte (en cours: %s%...)',
    'jdimming': 'Estompage:',
    'jdimmingnone': 'Sans',
    'jdimmingz': 'Altitude',
    'jdimmingdeclivity': 'Déclivité',
    'jdimmingshadow': 'Ombrage',
    'jltilt': 'Inclinaison lumière:',
    'jlrotation': 'Rotation lumière:',
    'jpace': 'Progression:',
    'jvfov': 'Champ de vue vertical:',
    'jheight': 'Hauteur de vue:',
    'jminimap': 'clic sur la mini-carte pour l\'agrandir / la réduire&#13;&#10;clic droit sur la mini-carte pour afficher / masquer le panneau d\'informations, et lorsqu\'il est visible:&#13;&#10;clic droit sur la vue 3D pour afficher la description du point&#13;&#10;alt + clic droit sur la vue 3D pour afficher la description du point et son géocodage inversé&#13;&#10;clic sur l\'oeil ou la cible pour créer ou déplacer à cet emplacement le point de cheminement dédié dans l\'onglet d\'édition de trace&#13;&#10;alt + clic sur l\'oeil ou la cible pour compléter la description du point par son géocodage inversé&#13;&#10;ctrl + clic droit sur la mini-carte pour afficher / masquer le panneau de sélection du fournisseur de géocodages inversés',
    'jplat': 'lat:',
    'jplon': 'lon:',
    'jpele': 'ele:',
    'jpdist': 'dist:',
    'start': 'démarrage',
    'close': 'fermeture'
  },
  'parser': {
    'license': 'Ce programme est sous licence copyleft GNU GPLv3 (voir https://www.gnu.org/licenses)',
    'help': 'affichage du message d\'aide et interruption du script',
    'uri': 'chemin d\'accès à la trace ou argument pas mentionné pour démarrer avec l\'explorateur de traces',
    'conf': 'chemin d\'accès au fichier de configuration [même répertoire que le script par défaut]',
    'trk': 'indice de la trace (commençant à 0) [0 par défaut]',
    'map': 'chemin d\'accès complet à la carte ou nom du fournisseur de carte ou vide pour utiliser le premier founisseur de carte configuré, ou option pas mentionnée pour utiliser les fournisseurs de tuiles configurés [par défaut]',
    'emap': 'chemin d\'accès complet à la carte d\'altitudes ou nom du fournisseur de carte d\'altitudes ou vide pour utiliser le premier fournisseur de carte d\'altitudes configuré, ou option pas mentionnée pour utiliser les fournisseurs de tuiles et données d\'altitudes configurés [par défaut]',
    'box': '"minlat, maxlat, minlon, maxlon" (latitudes minimale et maximale, longitudes minimale et maximale, avec les "" ) de la carte à charger / à retourner (pour l\'utilisation d\'une carte / d\'un fournisseur de carte) [lu dans les métadonnées gpxtweaker de la carte / déterminé à partir de la trace par défaut]',
    'size': '"height, width" (hauteur et largeur, avec les "") de la carte à charger / "maxheight, maxwidth" (hauteur et largeur maximales, avec les "") de la carte à retourner (pour l\'utilisation d\'une carte / d\'un fournisseur de carte) [lu dans les métadonnées gpxtweaker de la carte / "2000, 4000" par défaut]',
    'dpi': 'densité de la carte à retourner en pixels par pouce (pour l\'utilisation d\'un fournisseur de carte) [90 par défaut]',
    'record': 'enregistre les cartes récupérées dans le répertoire indiqué',
    'noopen': 'pas d\'ouverture automatique dans le navigateur par défaut',
    'verbosity': 'niveau de verbosité de 0 à 2 [0 par défaut]',
    'gpx': 'seuls les fichiers .gpx sont pris en charge',
    'openc': 'Ouvrir l\'url (copiée dans le presse-papier) %s',
    'open': 'Ouvrir l\'url %s',
    'keyboard': 'Presser "S" pour quitter'
   }
}
EN_STRINGS = {
  'tilescache': {
    '_id': 'Tiles cache',
    'init': 'initialization (size: %s, threads: %s)',
    'get': 'tile (%s, %s) requested',
    'cancel': 'tile (%s, %s) providing cancelled',
    'found': 'tile (%s, %s) found in the cache',
    'del': 'reduction of the cache',
    'add': 'addition of the tile (%s, %s) to the cache bringing its length to %s',
    'error': 'failure of tile (%s, %s) loading',
    'load': 'tile (%s, %s) loaded',
    'configure': 'configuration (tiles set: %s, matrix: %s)',
    'ifound': 'informations found in cache (tiles set: %s, matrix: %s)',
    'fail': 'failure of configuration (tiles set: %s, matrix: %s)',
    'close': 'shutdown'
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
    'tileretrieved': 'tile %s provided'
  },
  'jsontiles': {
    '_id': 'Handler of json tile set',
    'styleload': 'loading of the style %s',
    'stylecloaded': 'style %s loaded from the cache',
    'stylelfound': 'style %s found locally',
    'stylelexpired': 'local style %s expired',
    'stylefetch': 'retrieval of the style %s',
    'styleloaded': 'style %s loaded',
    'stylefail': 'failure of the loading of the style %s',
    'glyphretrieve': 'providing of the glyph %s [%s - %s]',
    'glyphcretrieved': 'glyph %s [%s - %s] provided from the cache',
    'glyphlfound': 'glyph %s [%s - %s] found locally',
    'glyphlexpired': 'glyph local %s [%s - %s] expired',
    'glyphfetch': 'retrieval of the glyph %s [%s - %s]',
    'glyphretrieved': 'glyph %s [%s - %s] provided',
    'glyphfail': 'failure of the providing of the glyph %s [%s - %s]',
    'spritejsonretrieve': 'providing of the sprite json %s [%s]',
    'spritejsoncretrieved': 'sprite json %s [%s] provided from the cache',
    'spritejsonlfound': 'sprite json %s [%s] found locally',
    'spritejsonlexpired': 'local sprite json %s [%s] expired',
    'spritejsonfetch': 'retrieval of the sprite json %s [%s]',
    'spritejsonretrieved': 'sprite json %s [%s] provided',
    'spritejsonfail': 'failure of the providing of the sprite json %s [%s]',
    'spritepngretrieve': 'providing of the sprite png %s [%s]',
    'spritepngcretrieved': 'sprit png %s [%s] provided from the cache',
    'spritepnglfound': 'sprite png %s [%s] found locally',
    'spritepnglexpired': 'local sprite png %s [%s] expired',
    'spritepngfetch': 'retrieval of the sprite png %s [%s]',
    'spritepngretrieved': 'sprite png %s [%s] provided',
    'spritepngfail': 'failure of the providing of the sprite png %s [%s]',
  },
  'legend': {
    '_id': 'Legend handler',
    'legendretrieve': 'providing of legend %s',
    'legendretrieved1': 'legend %s provided: %s component(s)',
    'legendlfound': 'legend %s found locally',
    'legendlexpired': 'local legend %s expired',
    'legendfetch': 'fetching of legend %s',
    'legendfail': 'failure of providing of legend %s',
    'legendretrieved2': 'legend %s provided'
  },
  'track': {
    '_id': 'Track manager',
    'init': 'initialization',
    'load': 'loading of track %s',
    'new': 'creation of a new track as %s',
    'oerror': 'failure of loading of file %s',
    'lerror': 'failure of loading of track %s',
    'perrorw': 'invalid data: waypoint %s',
    'perrorp': 'invalid data: segment %s - point %s',
    'loaded': 'track %s loaded (name: "%s", waypoints: %s, segments: %s, points: %s)',
    'save': 'saving of track as %s',
    'serror': 'failure of saving of track under %s',
    'saved': 'track saved as %s'
  },
  'geomedia': {
     '_id': 'Geotagged media manager',
     'mdlerror': 'failure of the retrieval of the data of the media %s',
     'mdloaded': 'data of the media %s retrieved',
     'mskipped': 'media %s skipped because overflowing with the view',
     'mtloaded': '%d photo(s) and %d video(s) taken into account in %.1fs',
     'moerror': 'failure of the opening of the media %s',
     'mopened': 'media %s opened'
  },
  'loader': {
     '_id': 'Tracks loader',
     'init': 'initialization (worker processes: %s)',
     'rtrack': 'receipt of the data of the track %s <%s>',
     'itrack': 'interruption of the receipt of the data of track',
     'etrack': 'end of the receipt of the data of track',
     'wstart': 'worker process %s - start',
     'wload': 'worker process %s - handling of the loading of the file %s',
     'wiqueue': 'worker process %s - queuing of the data of the track %s <%s>',
     'wsqueue': 'worker process %s - transfer of the data of the track %s <%s>',
     'weload': 'worker process %s - end of the loading of file',
     'wrdoc': 'worker process %s - receipt of the transfer request of the document of the file %s',
     'wsdoc': 'worker process %s - transfer of the document of the file %s',
     'winterrupt': 'worker process: %s - interruption',
     'wend': 'worker process: %s - stop',
     'rstarty': 'start of the handler of repatriation of document of file (anticipatory: yes)',
     'rstartn': 'start of the handler of repatriation of document of file (anticipatory: no)',
     'rrequest': 'handler of repatriation - receipt of the request of retrieval of the track %s <%s>',
     'rhandle': 'handler of repatriation - anticipatory retrieving of the track %s <%s>',
     'rabort': 'handler of repatriation - track %s <%s> already retrieved',
     'rretrieved': 'handler of repatriation - track %s <%s> retrieved',
     'rend': 'end of the repatriation of document of file',
     'rstop': 'shutdown of the handler of repatriation of document of file',
     'close': 'shutdown'
  },
  'interface': {
    '_id': 'Interface',
    'conf': 'loading of configuration',
    'cerror': 'failure of loading of configuration (%s)',
    'cloaded': 'configuration loaded',
    'build': 'generation of the interface page',
    'buildexp': 'generation of the interface page of the explorer',
    'bloaded1': '%s track(s) loaded in %.1fs',
    'bloaded2': '%s track(s) loaded in %.1fs, %s track(s) skipped, %s track(s) rejected, %s gpx file(s) rejected',
    'berror': 'failure of the generation of the interface page',
    'berror1': 'failure of the generation of the interface page (conversion into WebMercator)',
    'berror2': 'failure of the generation of the interface page (map outside frame)',
    'berror3': 'failure of the generation of the interface page (map "%s" not defined)',
    'berror4': 'failure of the generation of the interface page (track overflowing with the view)',
    'berror5': 'failure of the generation of the interface page (settings of tiles sets or cache)',
    'berror6': 'track skipped because overflowing with the view',
    'berrori': 'generation of the interface page interrupted',
    'elevation': 'elevations provider configured (%s)',
    'eerror': 'failure of the configuration of the elevations provider (%s)',
    'itinerary': 'itineraries provider configured (%s)',
    'reversegeocoding': 'reverse geocodings provider configured (%s)',
    'maplibre': 'This program uses the MapLibre GL JS library (https://github.com/maplibre/maplibre-gl-js), licensed under the 3-Clause BSD license, to display tiles sets defined from a style in JSON format, by import from %s',
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
    'jfconfirm': 'Smooth the whole track ?',
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
    'jdatetime': 'focus on segment or point / no focus: complete by inter/extra polation the timestamps of the element / the track&#13;&#10;+shift: remove the timestamp(s)',
    'jsave': 'backup the track&#13;&#10;(then reload the page to irreversibly eliminate the disabled elements)',
    'jswitchpoints': 'show / hide the marks of point and waypoint&#13;&#10;+ctrl: show / hide the controls of the smoothing filter&#13;&#10;+shift: smooth the segment / the track (be careful, a high value of filter distance range or a repeated application of the smoothing will probably alter the track)',
    'jgraph': 'show / hide the graph&#13;&#10;+shift: show / hide the controls of the filter of calculation of the elevation gain&#13;&#10;+ctrl: show / hide the controls of the filter of calculation of the slope&#13;&#10;+alt: show / hide the controls of the filter of calculation of the speed',
    'j3dviewer': 'open the 3D viewer in panoramic view mode&#13;&#10;+alt: open the 3D viewer in subjective view mode&#13;&#10;+ctrl: show / hide the controls of the margin around the track',
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
    'jdownloadmap': 'download a map of the ticked tracks&#13;&#10;+shift: download the list of tracks&#13;&#10;+alt: download the list of tracks with the waypoints&#13;&#10;+ctrl: download the displayed graph',
    'jswitchmedia': 'show / hide the photos and videos&#13;&#10;+alt: open also / close the preview panel&#13;&#10;+ctrl: show / hide the controls of thumbnail size',
    'jtrackdetach': 'detach the track (from a multi-tracks files)',
    'jtrackintegrate': 'integrate the track before (in a multi-tracks files)&#13;&#10;+alt:integrate the track after (in a multi-tracks files)',
    'jtrackincorporate': 'incorporate the waypoints and segments of the other ticked track',
    'jtracknew': 'create a new empty track in the first ticked folder',
    'jtrackedit': 'edit the track',
    'jzoomall': 'reframe on all ticked tracks&#13;&#10;+alt: reframe on all ticked and listed tracks&#13;&#10;+shift: reframe on the focused track',
    'jwebmapping': 'display the starting point in the online mapping service',
    'jswitchsmooth': 'toggle the smoothing of the tracks (∻ disabled | ÷ enabled)&#13;&#10;+ctrl: show / hide the controls of the smoothing filter',
    'jtset': 'select the set of tiles&#13;&#10;+shift: selection of the elevations provider&#13;&#10;+ctrl: selection of the itineraries provider&#13;&#10;in superposition of tiles sets mode, right click: show / hide the controls of layer transparency&#13;&#10;alt + right click: display the legend if available',
    'jeset': 'select the elevations provider&#13;&#10;+alt: selection of the set of tiles&#13;&#10;+ctrl: selection of the itineraries provider',
    'jiset': 'select the itineraries provider&#13;&#10;+alt: selection of the set of tiles&#13;&#10;+shift: selection of the elevations provider',
    'jexptset': 'select the set of tiles&#13;&#10;+shift: selection of the elevations provider&#13;&#10;+ctrl: selection of the online mapping service&#13;&#10;in superposition of tiles sets mode, right click: show / hide the controls of layer transparency&#13;&#10;alt + right click: display the legend if available',
    'jexpeset': 'select the elevations provider&#13;&#10;+alt: selection of the set of tiles&#13;&#10;+ctrl: selection of the online mapping service',
    'jexpiset': 'select the online mapping service&#13;&#10;+alt: selection of the set of tiles&#13;&#10;+shift: selection of the elevations provider',
    'jminus': 'zoom out&#13;&#10;+ctrl: attenuate&#13;&#10;+shift: lighten',
    'jexpminus': 'zoom out&#13;&#10;+ctrl: attenuate&#13;&#10;+shift: lighten&#13;&#10;+alt: thin',
    'jlock': 'lock / unlock the set of tiles',
    'jplus': 'zoom in&#13;&#10;+ctrl: reaccentuate&#13;&#10;+shift: redarken',
    'jexpplus': 'zoom in&#13;&#10;+ctrl: reaccentuate&#13;&#10;+shift: redarken&#13;&#10;+alt: thicken',
    'jdfpanel': 'Range points smoothing',
    'jmtpanel': 'Thumbnails size',
    'jpixels': '&nbsp;pixels',
    'jfilterpanel1': 'Thresholds gain calcul',
    'jfilterpanel2': 'Ranges slope calcul',
    'jfilterpanel3': 'Ranges speed calcul',
    'jspduration': 'duration',
    'jsmax': 'max&nbsp;&nbsp;&nbsp;',
    'j3dpanel': 'Margins 3D view',
    'j3dpanoramic': 'panoram',
    'j3dsubjective': 'subject',
    'jopacityreset': 'double-click to restore the original value\\r\\n+alt:+shift: restore all the original values',
    'jfoldersw': 'Folders:',
    'jscrollcross': 'center on the focused element&#13;&#10;+shift: reframe on the track&#13;&#10;+ctrl: cycle between the map auto-scrolling modes (grayed: no scrolling, blue: scrolling on focus, green: centering on focus and scrolling on hover)',
    'jhelp': 'left click-drag on the map to scroll it&#13;&#10;mouse wheel on the map to scroll it vertically&#13;&#10;shift + mouse wheel on the map to scroll it horizontally&#13;&#10;ctrl + mouse wheel on the map to zoom in or out&#13;&#10;alt + mouse wheel on the map to switch to the previous or the next waypoint / point / segment&#13;&#10;click / left click-drag (+ shift / alt) on the plot of a point / waypoint to select it / move it (and delete / keep its elevation data, or failing that choose depending whether the distance is greater than 25m or not)&#13;&#10;ctrl + click / left click-drag on the plot of a point to select it / move it and build a path from the previous point to this one&#13;&#10;left click on the plot of a segment to select it&#13;&#10;right click on the map to insert a point after the focused point or a waypoint otherwise&#13;&#10;ctrl + right click on the map to insert a point after the focused point in path following mode&#13;&#10;right click on the plot of a point / waypoint / segment to delete it&#13;&#10;mouse over a button to display its legend',
    'jexpscrollcross': 'center on the focused element&#13;&#10;+ctrl: cycle between the map auto-scrolling modes (grayed: no scrolling, blue: scrolling on focus, green: centering on focus and scrolling on hover)',
    'jexphelp': 'left click-drag on the map to scroll it&#13;&#10;mouse wheel on the map to scroll it vertically&#13;&#10;shift + mouse wheel on the map to scroll it horizontally&#13;&#10;ctrl + mouse wheel on the map to zoom in or out&#13;&#10;alt + mouse wheel on the map to switch to the previous or the next track&#13;&#10;left click on the plot of a track to select it&#13;&#10;right click on the plot of a track to hide it&#13;&#10;left click on a photo / video to display it big then left click on a photo to toggle the fullscreen mode and right click to go back to the tracks explorer&#13;&#10;mouse over a button to display its legend',
    'jhelp3d': 'mouse over the mini-map to display its legend&#13;&#10;click on the 3d view then :&#13;&#10;arrow up / down or mouse wheel to move forward / backward&#13;&#10;arrow left / right or horizontal click-drag to rotate left / right&#13;&#10;page up / down or vertical click-drag to tilt up / down&#13;&#10;+shift to accelerate the move&#13;&#10;delete or wheel click to toggle the automatic rotation with the progression&#13;&#10;insertion to remove the tilt&#13;&#10;minus / plus to lower / raise the view&#13;&#10;enter or, directly, double-click to toggle the fullscreen mode',
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
    'jexplorer': 'double-click to display in the file explorer',
    'jfolder': 'Fold',
    'jperiod': 'Peri',
    'jcontent': 'Cont',
    'jtrackcontent': '%d seg(s) | %d pt(s) | %d waypt(s)',
    'jgraphdistance': 'distance',
    'jgraphelevation': 'elevation',
    'jgraphaltitude': 'altitude',
    'jgraphelegain': 'ele gain',
    'jgraphaltgain': 'alt gain',
    'jgrapheleslope': 'ele slope',
    'jgraphaltslope': 'alt slope',
    'jgraphspeed': 'speed',
    'jgraphtime': 'duration',
    'jmadjust': 'Adjustement of the map (amplitude: %s - exponent: %s)',
    'jmundo1': 'Insertion of %s point(s) cancelled',
    'jmundo2': 'Modification of %s point(s) cancelled',
    'jmredo1': 'Insertion of %s point(s) restored',
    'jmredo2': 'Modification of %s point(s) restored',
    'jminsert1': 'Waypoint inserted',
    'jminsert2': 'Point inserted',
    'jmpathno': 'No itineraries provider configured',
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
    'jmsegmentfilter1': 'Segment smoothed: %s point(s) moved',
    'jmsegmentfilter2': 'Track smoothed: %s point(s) moved',
    'jmelevationsno': 'No elevations source configured',
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
    'jmdatetime4': 'Timestamp of the point removed',
    'jmdatetime5': 'Timestamps of the segment removed',
    'jmdatetime6': 'Timestamps of the track removed',
    'jmsave1': 'Backup in progress...',
    'jmsave2': 'Backup completed',
    'jmsave3': 'Failure of the backup',
    'jmmedia1': 'Retrieval of the data of the media in progress...',
    'jmmedia2': 'Retrieval of the data of the media completed',
    'jmmedia3': 'Failure of the retrieval of the data of the media',
    'jmdownmap1': 'Preparation of the map in progress (phase 1/4)...',
    'jmdownmap2': 'Preparation of the map in progress (phase 2/4)...',
    'jmdownmap3': 'Preparation of the map in progress (phase 3/4)...',
    'jmdownmap4': 'Preparation of the map in progress (phase 4/4)...',
    'jmdownmap5': 'Map ready for download (%s track(s) - %s x %s)',
    'jmdownmap6': 'Failure of the preparation of the map',
    'jmdownmap7': 'Map too big, zoom out required',
    'jmopenlegend1': 'Retrieval of the legend(s) in progress...',
    'jmopenlegend2': 'End of the retrieval of the legend(s): %s legend(s) obtained',
    'jmdetach1': 'Detachment in progress...',
    'jmdetach2': 'Detachment completed',
    'jmdetach3': 'Failure of the detachment',
    'jmdetach4': 'Detachment cancelled: track not part of a multi-tracks file',
    'jmincorporate1': 'Incorporation in progress...',
    'jmincorporate2': 'Incorporation completed',
    'jmincorporate3': 'Failure of the incorporation',
    'jmincorporate4': 'Incorporation cancelled: none or more than another visible ticked track',
    'jmintegrate1': 'Integration in progress...',
    'jmintegrate2': 'Integration completed',
    'jmintegrate3': 'Failure of the integration',
    'jmintegrate4': 'Integration cancelled: none or more than another visible ticked track',
    'jmintegrate5': 'Integration cancelled: track to be integrated part of a multi-tracks file',
    'jmnew1': 'Creation in progress...',
    'jmnew2': 'Creation completed',
    'jmnew3': 'Failure of the creation',
    'jm3dviewer1': 'Loading of the 3D viewer in progress...',
    'jm3dviewer2': '3D viewer started',
    'jm3dviewer3': 'Failure of the loading of the 3D viewer',
    'jm3dviewer4': '3D viewer unavailable in superposition of tiles sets or json tile set mode',
    'jtilt': 'Tilt:',
    'jrotation': 'Rotation:',
    'jzscale': 'Z scale:',
    'jzscaleiso': 'iso',
    'jzscalemax': 'max',
    'jtexture': 'Texture:',
    'jtextureyiso': 'Y isopleths',
    'jtextureziso': 'Z isopleths',
    'jtexturemap': 'Map',
    'jtexturemaploading': 'Map (in progress: %s%...)',
    'jdimming': 'Dimming:',
    'jdimmingnone': 'Without',
    'jdimmingz': 'Elevation',
    'jdimmingdeclivity': 'Declivity',
    'jdimmingshadow': 'Shadow',
    'jltilt': 'Light tilt:',
    'jlrotation': 'Light rotation:',
    'jpace': 'Progression:',
    'jvfov': 'Vertical field of view:',
    'jheight': 'Height of view:',
    'jminimap': 'click on the mini-map to enlarge / reduce it&#13;&#10;right click on the mini-map to show / hide the informations panel, and when it is visible:&#13;&#10;right click on the 3D view to display the description of the point&#13;&#10;alt + right click on the 3D view to display the description of the point and its reverse geocoding&#13;&#10;click on the eye or the target to create or move to this location the dedicated waypoint in the track edition tab&#13;&#10;alt + click on the eye or the target to complete the description of the point with its reverse geocoding&#13;&#10;ctrl + right click on the mini-map to show / hide the reverse geocodings provider panel',
    'jplat': 'lat:',
    'jplon': 'lon:',
    'jpele': 'ele:',
    'jpdist': 'dist:',
    'start': 'start-up',
    'close': 'shutdown'
  },
  'parser': {
    'license': 'This program is licensed under the GNU GPLv3 copyleft license (see https://www.gnu.org/licenses)',
    'help': 'display of the help message and interruption of the script',
    'uri': 'path to the track or argument not mentioned to start with the explorer of tracks',
    'conf': 'full path to the configuration file [same folder as the script by default]',
    'trk': 'index of the track (starting at 0) [0 by default]',
    'map': 'full path to the map or name of the map provider or blank to use the first map provider configured, or option not mentioned to use the tiles providers configured [by default]',
    'emap': 'path to the elevations map or name of the elevations map provider or blank to use the first elevations map configured, or option not mentioned to use the elevations tiles and data providers configured [by default]',
    'box': '"minlat, maxlat, minlon, maxlon" (minimum and maximum latitudes, minimum and maximum longitudes, with the "") of the map to be loaded / retrieved (for the use of a map / of a map provider) [read from the gpxtweaker metadata of the map / determined from the track by default]',
    'size': '"height, width" (height and width, with the "") of the map to be loaded / "maxheight, maxwidth" (maximum height and width, with the "") of the map to be retrieved (for the use of a map / of a map provider) [read from the gpxtweaker metadata of the map / "2000, 4000" by default]',
    'dpi': 'density of the map to be retrieved in dots per inch (for the use of a map provider) [90 by default]',
    'record': 'saves the retrieved maps in the specified folder',
    'noopen': 'no automatic opening in the default browser',
    'verbosity': 'verbosity level from 0 to 2 [0 by default]',
    'gpx': 'only .gpx files are supported',
    'openc': 'Open the url (copied in the clipboard) %s',
    'open': 'Open the url %s',
    'keyboard': 'Press "S" to exit'
   }
}
LSTRINGS = EN_STRINGS
try:
  if locale.getlocale()[0][:2].lower() == 'fr':
    LSTRINGS = FR_STRINGS
except:
  pass

def enable_vt100():
  try:
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    byref = ctypes.byref
    DWORD = ctypes.wintypes.DWORD
    HANDLE = ctypes.wintypes.HANDLE
    m = DWORD()
    h = HANDLE(msvcrt.get_osfhandle(sys.stdout.fileno()))
    if not kernel32.GetConsoleMode(h, byref(m)):
      return False
    if not kernel32.SetConsoleMode(h, DWORD(m.value | 5)):
      return False
  except:
    return False
  return True

VERBOSITY = 0
if __name__ == '__mp_main__':
  VT100 = False
  LogBuffer = []
  def log(kmod, level, kmsg, *var, color=None, buffer=True):
    if level <= VERBOSITY:
      now = time.strftime('%x %X', time.localtime())
      if color and VT100:
        now = '\033[%dm%s\033[0m' % (color, now)
      if buffer:
        try:
          LogBuffer.append('%s : %s -> %s' % (now, LSTRINGS[kmod]['_id'], LSTRINGS[kmod][kmsg] % var))
        except:
          LogBuffer.append('%s : %s -> %s' % (now, kmod, '->', kmsg, var))
      else:
        try:
          print('%s : %s -> %s' % (now, LSTRINGS[kmod]['_id'], LSTRINGS[kmod][kmsg] % var))
        except:
          print('%s : %s -> %s' % (now, kmod, '->', kmsg, var))
else:
  VT100 = enable_vt100()
  def log(kmod, level, kmsg, *var, color=None):
    if level <= VERBOSITY:
      now = time.strftime('%x %X', time.localtime())
      if color and VT100:
        now = '\033[%dm%s\033[0m' % (color, now)
      try:
        print(now, ':', LSTRINGS[kmod]['_id'], '->', LSTRINGS[kmod][kmsg] % var)
      except:
        print(now, ':', kmod, '->', kmsg, var)


def _XMLGetNodeText(nodes):
  text = []
  if not isinstance(nodes, (list, tuple)):
    nodes = (nodes,)
  for node in nodes:
    if node.nodeType in (minidom.Node.TEXT_NODE, minidom.Node.CDATA_SECTION_NODE):
      text.append(node.data)
    elif node.hasChildNodes():
      for childNode in node.childNodes:
        if childNode.nodeType in (minidom.Node.TEXT_NODE, minidom.Node.CDATA_SECTION_NODE):
          text.append(childNode.data)
  return(''.join(text))


class HTTPExplodedMessage():

  __slots__ = ('method', 'path', 'version', 'code', 'message', 'headers', 'body', 'expect_close')

  def __init__(self):
    self.method = self.path = self.version = self.code = self.message = self.body = self.expect_close = None
    self.headers = {}

  def __bool__(self):
    return self.method is not None or self.code is not None

  def clear(self):
    self.__init__()
    return self

  def header(self, name, default=None):
    return self.headers.get(name.title(), default)

  def in_header(self, name, value):
    h = self.header(name)
    return False if h is None else (value.lower() in map(str.strip, h.lower().split(',')))

  def cookies(self, domain, path):
    hck = self.header('Set-Cookie')
    domain = domain.lower()
    dom_ip = all(c in '.:[]0123456789' for c in domain)
    path = path.rstrip('/') if (path != '/' and path[:1] == '/') else '/'
    ck = {}
    if hck is not None:
      hck = map(str.strip, hck.split('\n'))
      for co in hck:
        c = map(str.strip, co.split(';'))
        try:
          cn, cv = next(c).split('=', 1)
          if not cn:
            continue
          cd = cp = None
          for ca in c:
            try:
              can, cav = ca.split('=', 1)
            except:
              continue
            if cd is None and can.lower() == 'domain' and cav:
              cav = cav.lstrip('.').lower()
              if (domain != cav) if dom_ip else (not domain[-len(cav) - 1 :] in (cav, '.' + cav)):
                raise
              cd = (cav, True)
            if cp is None and can.lower() == 'path':
              if not path[: len(cav) + (1 if cav[-1:] != '/' else 0)] in (cav, cav + '/'):
                raise
              cp = cav
          if cd is None:
            cd = (domain, False)
          if cp is None:
            cp = ''
          ck[(cd, cp, cn)] = cv
        except:
          pass
    return ck

  def __repr__(self):
    if self:
      try:
        return '\r\n'.join(('<HTTPExplodedMessage at %#x>\r\n----------' % id(self), (' '.join(filter(None, (self.method, self.path, self.version, self.code, self.message)))), *('%s: %s' % (k, l) for k, v in self.headers.items() for l in v.split('\n')), '----------\r\nLength of body: %s byte(s)' % len(self.body or ''), '----------\r\nClose expected: %s' % self.expect_close))
      except:
        return '<HTTPExplodedMessage at %#x>\r\n<corrupted object>' % id(self)
    else:
      return '<HTTPExplodedMessage at %#x>\r\n<no message>' % id(self)


class HTTPMessage():

  @staticmethod
  def _read_headers(msg, http_message):
    if not msg:
      return False
    a = None
    for msg_line in msg.replace('\r\n', '\n').split('\n')[:-2]:
      if a is None:
        try:
          a, b, c = msg_line.strip().split(None, 2)
        except:
          try:
            a, b, c = *msg_line.strip().split(None, 2), ''
          except:
            return False
      else:
        try:
          header_name, header_value = msg_line.split(':', 1)
        except:
          return False
        header_name = header_name.strip().title()
        if header_name:
          header_value = header_value.strip()
          if not header_name in ('Content-Length', 'Location', 'Host') and http_message.headers.get(header_name):
            if header_value:
              http_message.headers[header_name] += ('\n' if header_name in ('Set-Cookie', 'Www-Authenticate', 'Proxy-Authenticate') else ', ') + header_value
          else:
            http_message.headers[header_name] = header_value
        else:
          return False
    if a is None:
      return False
    if a[:4].upper() == 'HTTP':
      http_message.version = a.upper()
      http_message.code = b
      http_message.message = c
    else:
      http_message.method = a.upper()
      http_message.path = b
      http_message.version = c.upper()
    http_message.expect_close = http_message.in_header('Connection', 'close') or (http_message.version.upper() != 'HTTP/1.1' and not http_message.in_header('Connection', 'keep-alive'))
    return True

  @staticmethod
  def _read_trailers(msg, http_message):
    if not msg:
      return False
    for msg_line in msg.replace('\r\n', '\n').split('\n')[:-2]:
      try:
        header_name, header_value = msg_line.split(':', 1)
      except:
        return False
      header_name = header_name.strip().title()
      if header_name:
        if header_name in ('Transfer-Encoding', 'Content-Length', 'Host', 'Content-Encoding', 'Location'):
          continue
        header_value = header_value.strip()
        if http_message.headers.get(header_name):
          if header_value:
            http_message.headers[header_name] += ('\n' if header_name in ('Set-Cookie', 'Www-Authenticate', 'Proxy-Authenticate') else ', ') + header_value
        else:
          http_message.headers[header_name] = header_value
      else:
        return False
    return True

  def __new__(cls, message=None, body=True, decode='utf-8', timeout=5, max_length=1048576, max_hlength=1048576, decompress=True, exceeded=None):
    http_message = HTTPExplodedMessage()
    if isinstance(exceeded, list):
      exceeded[:] = [False]
    else:
      exceeded = None
    if message is None:
      return http_message
    max_hlength = min(max_length, max_hlength)
    rem_length = max_hlength
    iss = isinstance(message, socket.socket)
    if not iss:
      msg = message[0]
    else:
      message.settimeout(timeout)
      msg = b''
    while True:
      msg = msg.lstrip(b'\r\n')
      if msg and msg[0] < 0x20:
        return http_message
      body_pos = msg.find(b'\r\n\r\n')
      if body_pos >= 0:
        body_pos += 4
        break
      body_pos = msg.find(b'\n\n')
      if body_pos >= 0:
        body_pos += 2
        break
      if not iss or rem_length <= 0:
        return http_message
      try:
        bloc = message.recv(min(rem_length, 1048576))
        if not bloc:
          return http_message
      except:
        return http_message
      rem_length -= len(bloc)
      msg = msg + bloc
    if not cls._read_headers(msg[:body_pos].decode('ISO-8859-1'), http_message):
      return http_message.clear()
    if not iss:
      http_message.expect_close = True
    if http_message.code in ('100', '101', '204', '304'):
      http_message.body = b''
      return http_message
    if not body:
      http_message.body = msg[body_pos:]
      return http_message
    rem_length += max_length - max_hlength
    chunked = http_message.in_header('Transfer-Encoding', 'chunked')
    if chunked:
      body_len = -1
    else:
      body_len = http_message.header('Content-Length')
      if body_len is None:
        if not iss or (http_message.code in ('200', '206') and http_message.expect_close):
          body_len = -1
        else:
          body_len = 0
      else:
        try:
          body_len = max(0, int(body_len))
        except:
          return http_message.clear()
    if decompress and body_len != 0:
      hce = [e for h in (http_message.header('Content-Encoding', ''), http_message.header('Transfer-Encoding', '')) for e in map(str.strip, h.lower().split(',')) if not e in ('chunked', '', 'identity')]
      for ce in hce:
        if not ce in ('deflate', 'gzip'):
          if http_message.method is not None and iss:
            try:
              message.sendall(('HTTP/1.1 415 Unsupported media type\r\nContent-Length: 0\r\nDate: %s\r\nCache-Control: no-cache, no-store, must-revalidate\r\n\r\n' % email.utils.formatdate(time.time(), usegmt=True)).encode('ISO-8859-1'))
            except:
              pass
          return http_message.clear()
    else:
      hce = []
    if http_message.in_header('Expect', '100-continue') and iss:
      if body_pos + body_len - len(msg) <= rem_length:
        try:
          message.sendall('HTTP/1.1 100 Continue\r\n\r\n'.encode('ISO-8859-1'))
        except:
          return http_message.clear()
      else:
        try:
          message.sendall(('HTTP/1.1 413 Payload too large\r\nContent-Length: 0\r\nDate: %s\r\nCache-Control: no-cache, no-store, must-revalidate\r\n\r\n' % email.utils.formatdate(time.time(), usegmt=True)).encode('ISO-8859-1'))
        except:
          pass
        if exceeded is not None:
          exceeded[0] = True
        return http_message.clear()
    if not chunked:
      if body_len < 0:
        if not iss:
          http_message.body = msg[body_pos:]
        else:
          bbuf = BytesIO()
          rem_length -= bbuf.write(msg[body_pos:])
          while rem_length > 0:
            try:
              bw = bbuf.write(message.recv(min(rem_length, 1048576)))
              if not bw:
                break
              rem_length -= bw
            except:
              return http_message.clear()
          if rem_length <= 0:
            if exceeded is not None:
              exceeded[0] = True
            return http_message.clear()
          http_message.body = bbuf.getvalue()
      elif len(msg) < body_pos + body_len:
        if not iss:
          return http_message.clear()
        if body_pos + body_len - len(msg) > rem_length:
          if exceeded is not None:
            exceeded[0] = True
          return http_message.clear()
        bbuf = BytesIO()
        body_len -= bbuf.write(msg[body_pos:])
        while body_len:
          try:
            bw = bbuf.write(message.recv(min(body_len, 1048576)))
            if not bw:
              return http_message.clear()
            body_len -= bw
          except:
            return http_message.clear()
        http_message.body = bbuf.getvalue()
      else:
        http_message.body = msg[body_pos:body_pos+body_len]
    else:
      bbuf = BytesIO()
      buff = msg[body_pos:]
      while True:
        chunk_pos = -1
        rem_slength = max_hlength - len(buff)
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
          if not iss or rem_slength <= 0:
            return http_message.clear()
          if rem_length <= 0:
            if exceeded is not None:
              exceeded[0] = True
            return http_message.clear()
          try:
            bloc = message.recv(min(rem_length, rem_slength, 1048576))
            if not bloc:
              return http_message.clear()
          except:
            return http_message.clear()
          rem_length -= len(bloc)
          rem_slength -= len(bloc)
          buff = buff + bloc
        try:
          chunk_len = int(buff[:chunk_pos].split(b';', 1)[0].rstrip(b'\r\n'), 16)
          if not chunk_len:
            break
        except:
          return http_message.clear()
        if chunk_pos + chunk_len - len(buff) > rem_length:
          if exceeded is not None:
            exceeded[0] = True
          return http_message.clear()
        if len(buff) < chunk_pos + chunk_len:
          if not iss:
            return http_message.clear()
          chunk_len -= bbuf.write(buff[chunk_pos:])
          while chunk_len:
            try:
              bw = bbuf.write(message.recv(min(chunk_len, 1048576)))
              if not bw:
                return http_message.clear()
              chunk_len -= bw
            except:
              return http_message.clear()
            rem_length -= bw
          buff = b''
        else:
          bbuf.write(buff[chunk_pos:chunk_pos+chunk_len])
          buff = buff[chunk_pos+chunk_len:]
      http_message.body = bbuf.getvalue()
      rem_length = min(rem_length, max_hlength - body_pos - len(buff) + chunk_pos)
      while not (b'\r\n\r\n' in buff or b'\n\n' in buff):
        if not iss:
          return http_message.clear()
        if rem_length <= 0:
          if exceeded is not None:
            exceeded[0] = True
          return http_message.clear()
        try:
          bloc = message.recv(min(rem_length, 1048576))
          if not bloc:
            return http_message.clear()
        except:
          return http_message.clear()
        rem_length -= len(bloc)
        buff = buff + bloc
      if len(buff) - chunk_pos > 2:
        cls._read_trailers(buff[chunk_pos:].decode('ISO-8859-1'), http_message)
    if http_message.body:
      try:
        if hce:
          for ce in hce[::-1]:
            if ce == 'deflate':
              try:
                http_message.body = zlib.decompress(http_message.body)
              except:
                http_message.body = zlib.decompress(http_message.body, wbits=-15)
            elif ce == 'gzip':
              http_message.body = gzip.decompress(http_message.body)
            else:
              raise
        if decode:
          http_message.body = http_message.body.decode(decode)
      except:
        if http_message.method is not None and iss:
          try:
            message.sendall(('HTTP/1.1 415 Unsupported media type\r\nContent-Length: 0\r\nDate: %s\r\nCache-Control: no-cache, no-store, must-revalidate\r\n\r\n' % email.utils.formatdate(time.time(), usegmt=True)).encode('ISO-8859-1'))
          except:
            pass
        return http_message.clear()
    return http_message


class HTTPBaseRequest():

  RequestPattern = \
    '%s %s HTTP/1.1\r\n' \
    'Host: %s\r\n%s' \
    '\r\n'

  def __init_subclass__(cls, context_class=ssl.SSLContext):
    cls.SSLContext = context_class(ssl.PROTOCOL_TLS_CLIENT)
    cls.SSLContext.check_hostname = False
    cls.SSLContext.verify_mode = ssl.CERT_NONE

  @classmethod
  def connect(cls, url, url_p, headers, max_length, max_hlength, timeout, pconnection):
    raise

  @staticmethod
  def _netloc_split(loc, def_port=''):
    n, s, p = loc.rpartition(':')
    return (n, p or def_port) if (s == ':' and ']' not in p) else (loc, def_port)

  def __new__(cls, url, method=None, headers=None, data=None, timeout=30, max_length=1073741824, max_hlength=1048576, decompress=True, pconnection=None, basic_auth=None):
    if url is None:
      return HTTPMessage()
    if method is None:
      method = 'GET' if data is None else 'POST'
    redir = 0
    retried = False
    exceeded = [False]
    try:
      url_p = urllib.parse.urlsplit(url, allow_fragments=False)
      if headers is None:
        headers = {}
      hitems = headers.items()
      if pconnection is None:
        pconnection = [None, {}, []]
        hccl = True
      else:
        l = len(pconnection)
        pconnection[0:3] = [pconnection[0] if l >= 1 else None, pconnection[1] if l >= 2 else {}, []]
        hccl = 'close' in (e.strip() for k, v in hitems if k.lower() == 'connection' for e in v.lower().split(','))
      if data:
        hexp = '100-continue' in (e.strip() for k, v in hitems if k.lower() == 'expect' for e in v.lower().split(','))
      else:
        hexp = False
      headers = {k: v for k, v in hitems if not k.lower() in ('host', 'content-length', 'connection', 'expect')}
      if hexp:
        headers['Expect'] = '100-continue'
      if not 'accept-encoding' in (k.lower() for k, v in hitems):
        headers['Accept-Encoding'] = 'identity, deflate, gzip' if decompress else 'identity'
      if data is not None:
        if not 'chunked' in (e.strip() for k, v in hitems if k.lower() == 'transfer-encoding' for e in v.lower().split(',')):
          headers['Content-Length'] = str(len(data))
      headers['Connection'] = 'close' if hccl else 'keep-alive'
      hauth = headers.get('Authorization')
    except:
      return HTTPMessage()
    cook = pconnection[1]
    auth = False
    while True:
      try:
        pconnection[2].append(url)
        ck = {}
        if basic_auth is not None:
          domain = cls._netloc_split(url_p.netloc)[0].lower()
          dom_ip = all(c in '.:[]0123456789' for c in domain)
          path = url_p.path.split('#', 1)[0]
          path = path.rstrip('/') if (path != '/' and path[:1] == '/') else '/'
          for k, v in cook.items():
            if ((domain[-len(k[0][0]) - 1 :] in (k[0][0], '.' + k[0][0])) if (k[0][1] and not dom_ip) else (domain == k[0][0])) and path[: len(k[1]) + (1 if k[1][-1:] != '/' else 0)] in (k[1], k[1] + '/'):
              if (not k[2] in ck) or (len(k[0][0]) > len(ck[k[2]][1]) or (len(k[0][0]) == len(ck[k[2]][1]) and len(k[1]) >= len(ck[k[2]][2]))):
                ck[k[2]] = (v, k[0][0], k[1])
        path = cls.connect(url, url_p, headers, max_length, max_hlength, timeout, pconnection)
        try:
          code = '100'
          msg = cls.RequestPattern % (method, path, url_p.netloc, ''.join(k + ': ' + v + '\r\n' for k, v in (headers if not ck else {**headers, 'Cookie': '; '.join(k + '=' + v[0] for k, v in ck.items())}).items()))
          if hexp and data:
            pconnection[0].sendall(msg.encode('iso-8859-1'))
            resp = HTTPMessage(pconnection[0], body=(method.upper() != 'HEAD'), decode=None, timeout=min(3, 3 if timeout is None else timeout), max_length=max_length, max_hlength=max_hlength, decompress=False)
            code = resp.code
            if code is None:
              code = '100'
            if code == '100':
              pconnection[0].sendall(data)
          else:
            pconnection[0].sendall(msg.encode('iso-8859-1') + (data or b''))
        except:
          if retried:
            raise
          retried = True
          try:
            pconnection[0].close()
          except:
            pass
          pconnection[0] = None
          pconnection[2].pop()
          continue
        while code == '100':
          resp = HTTPMessage(pconnection[0], body=(method.upper() != 'HEAD'), decode=None, timeout=timeout, max_length=max_length, max_hlength=max_hlength, decompress=decompress, exceeded=exceeded)
          code = resp.code
          if code == '100':
            redir += 1
            if redir > 5:
              raise
        if code is None:
          if retried or exceeded == [True]:
            raise
          retried = True
          try:
            pconnection[0].close()
          except:
            pass
          pconnection[0] = None
          pconnection[2].pop()
          continue
        retried = False
        if basic_auth is not None and resp.header('Set-Cookie') is not None:
          cook.update(resp.cookies(cls._netloc_split(url_p.netloc)[0], url_p.path.split('#', 1)[0]))
        if code == '401':
          if not auth and basic_auth is not None and any((l or 'basic')[:5].lower() == 'basic' for l in resp.header('WWW-Authenticate').split('\n')):
            auth = True
            headers['Authorization'] = 'Basic ' + base64.b64encode(basic_auth.encode('utf-8')).decode('utf-8')
            if headers['Connection'] == 'close' or resp.expect_close:
              pconnection[0] = None
          else:
            auth = False
            break
        elif code[:2] == '30' and code != '304':
          auth = False
          if resp.header('location'):
            url = urllib.parse.urljoin(url, resp.header('location'))
            urlo_p = url_p
            url_p = urllib.parse.urlsplit(url, allow_fragments=False)
            if headers['Connection'] == 'close' or resp.expect_close or (urlo_p.scheme != url_p.scheme or urlo_p.netloc != url_p.netloc):
              try:
                pconnection[0].close()
              except:
                pass
              pconnection[0] = None
              headers['Connection'] = 'close'
            redir += 1
            if redir > 5:
              break
            if code == '303':
              if method.upper() != 'HEAD':
                method = 'GET'
              data = None
              for k in list(headers.keys()):
                if k.lower() in ('transfer-encoding', 'content-length', 'content-type', 'expect'):
                  del headers[k]
          else:
            raise
        else:
          auth = False
          break
      except:
        auth = False
        try:
          pconnection[0].close()
        except:
          pass
        pconnection[0] = None
        return HTTPMessage()
      finally:
        if not auth and 'Authorization' in headers:
          if hauth is not None:
            headers['Authorization'] = hauth
          else:
            del headers['Authorization']
    if headers['Connection'] == 'close' or resp.expect_close:
      try:
        pconnection[0].close()
      except:
        pass
      pconnection[0] = None
    return resp


class NestedSSLContext(ssl.SSLContext):

  class SSLSocket(ssl.SSLSocket):

    def __new__(cls, *args, **kwargs):
      if not hasattr(cls, 'sock'):
        raise TypeError('%s does not have a public constructor. Instances are returned by NestedSSLContext.wrap_socket().' % cls.__name__)
      cls_ = cls.__bases__[0]
      self = super(cls_, cls_).__new__(cls_, *args, **kwargs)
      self.socket = cls.sock
      cls.sock = None
      return self

    class _PSocket:

      def __init__(self, s):
        self.s = s

      def detach(self):
        pass

      def __getattr__(self, name):
        return getattr(self.s, name)

    @classmethod
    def _create(cls, sock, *args, do_handshake_on_connect=True, **kwargs):
      self = ssl.SSLSocket._create.__func__(type('BoundSSLSocket', (cls,), {'sock': sock}), cls._PSocket(sock), *args, **kwargs)
      return self

    def close(self):
      super().close()
      try:
        self.socket.close()
      except:
        pass

    def shutdown(self, how):
      super().shutdown(how)
      try:
        self.socket.shutdown(how)
      except:
        pass

    def settimeout(self, value):
      super().settimeout(value)
      try:
        self.socket.settimeout(value)
      except:
        pass

  sslsocket_class = SSLSocket

  class _SSLSocket():

    def __init__(self, context, ssl_sock, server_side, server_hostname):
      self.sslsocket = ssl_sock
      self.inc = ssl.MemoryBIO()
      self.out = ssl.MemoryBIO()
      self._sslobj = context.wrap_bio(self.inc, self.out, server_side, server_hostname)._sslobj

    def __getattr__(self, name):
      return self._sslobj.__getattribute__(name)

    def __setattr__(self, name, value):
      if name in ('sslsocket', 'inc', 'out', '_sslobj'):
        object.__setattr__(self, name, value)
      else:
        self._sslobj.__setattr__(name, value)

    def _read_record(self):
      bl = b''
      while len(bl) < 5:
        b_ = self.sslsocket.socket.recv(5 - len(bl))
        if not b_:
          raise ConnectionResetError
        bl += b_
      l = int.from_bytes(bl[3:5], 'big')
      b = bytearray(l + 5)
      b[0:5] = bl
      m = memoryview(b)
      while l > 0:
        bl = self.sslsocket.socket.recv_into(m[-l:], l)
        if not bl:
          raise ConnectionResetError
        l -= bl
      self.inc.write(b)

    def interface(self, action, *args, **kwargs):
      timeout = self.sslsocket.gettimeout()
      if timeout:
        t = time.monotonic()
      while True:
        try:
          res = action(*args, **kwargs)
        except (ssl.SSLWantReadError, ssl.SSLWantWriteError) as err:
          if timeout:
            if time.monotonic() - t > timeout:
              raise TimeoutError(10060, 'timed out')
          if self.out.pending:
            self.sslsocket.socket.sendall(self.out.read())
          if err.errno == ssl.SSL_ERROR_WANT_READ and not self.inc.pending:
            if timeout:
              if time.monotonic() - t > timeout:
                raise TimeoutError(10060, 'timed out')
            try:
              self._read_record()
            except ConnectionResetError:
              if action == self._sslobj.do_handshake:
                raise ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host')
              else:
                raise ssl.SSLEOFError(ssl.SSL_ERROR_EOF, 'EOF occurred in violation of protocol')
        else:
          if self.out.pending:
            if timeout:
              if time.monotonic() - t > timeout:
                raise TimeoutError(10060, 'timed out')
            self.sslsocket.socket.sendall(self.out.read())
          return res

    def do_handshake(self):
      return self.interface(self._sslobj.do_handshake)

    def read(self, length=16384, buffer=None):
      return self.interface(self._sslobj.read, length) if buffer is None else self.interface(self._sslobj.read, length, buffer)

    def write(self, bytes):
      return self.interface(self._sslobj.write, bytes)

    def shutdown(self):
      self.interface(self._sslobj.shutdown)
      return self.sslsocket.socket

    def verify_client_post_handshake(self):
      return self.interface(self._sslobj.verify_client_post_handshake)

  def __init__(self, *args, **kwargs):
    self.DefaultSSLContext = ssl.SSLContext(*args, **kwargs)
    ssl.SSLContext.__init__(*args, **kwargs)

  def wrap_callable(self, name):
    def new_callable(*args, **kwargs):
      object.__getattribute__(self.DefaultSSLContext, name)(*args, **kwargs)
      return object.__getattribute__(self, name)(*args, **kwargs)
    return new_callable

  def __getattribute__(self, name):
    if not name in NestedSSLContext.__dict__ and type(object.__getattribute__(self, name)) in (types.BuiltinMethodType, types.MethodType):
      return self.wrap_callable(name)
    else:
      return object.__getattribute__(self, name)

  def __setattr__(self, name, value):
    object.__setattr__(self, name, value)
    if name != 'DefaultSSLContext':
      self.DefaultSSLContext.__setattr__(name, value)

  def wrap_socket(self, sock, *args, **kwargs):
    return ssl.SSLContext.wrap_socket(self if isinstance(sock, ssl.SSLSocket) else self.DefaultSSLContext, sock, *args, **kwargs)

  def _wrap_socket(self, ssl_sock, server_side, server_hostname, *args, **kwargs):
    return NestedSSLContext._SSLSocket(self, ssl_sock, server_side, server_hostname)

  def wrap_bio(self, *args, **kwargs):
    return self.DefaultSSLContext.wrap_bio(*args, **kwargs)


def gen_HTTPRequest(proxy=None):
  global HTTPRequest
  if not proxy or not (proxy or {}).get('ip', None):
    class HTTPRequest(HTTPBaseRequest):
      @classmethod
      def connect(cls, url, url_p, headers, max_length, max_hlength, timeout, pconnection):
        if pconnection[0] is None:
          if url_p.scheme.lower() == 'http':
            pconnection[0] = socket.create_connection((url_p.hostname, url_p.port if url_p.port is not None else 80), timeout=timeout)
          elif url_p.scheme.lower() == 'https':
            pconnection[0] = cls.SSLContext.wrap_socket(socket.create_connection((url_p.hostname, url_p.port if url_p.port is not None else 443), timeout=timeout), server_side=False, server_hostname=cls._netloc_split(url_p.netloc)[0])
          else:
            raise
        else:
          try:
            pconnection[0].settimeout(timeout)
          except:
            pass
        return (url_p.path + ('?' + url_p.query if url_p.query else '')).replace(' ', '%20') or '/'
  else:
    class HTTPRequest(HTTPBaseRequest, context_class=NestedSSLContext):
      PROXY = ('', 8080)
      PROXY_AUTH = ''
      PROXY_SECURE = False
      @classmethod
      def connect(cls, url, url_p, headers, max_length, max_hlength, timeout, pconnection):
        if pconnection[0] is None:
          if url_p.scheme.lower() == 'http':
            if not cls.PROXY_SECURE:
              pconnection[0] = socket.create_connection(cls.PROXY, timeout=timeout)
            else:
              pconnection[0] = cls.SSLContext.wrap_socket(socket.create_connection(cls.PROXY, timeout=timeout),  server_side=False, server_hostname=cls.PROXY[0])
          elif url_p.scheme.lower() == 'https':
            if not cls.PROXY_SECURE:
              psock = socket.create_connection(cls.PROXY, timeout=timeout)
            else:
              psock = cls.SSLContext.wrap_socket(socket.create_connection(cls.PROXY, timeout=timeout), server_side=False, server_hostname=cls.PROXY[0])
            psock.sendall(('CONNECT %s:%s HTTP/1.1\r\nHost: %s:%s\r\n%s\r\n' % (*(cls._netloc_split(url_p.netloc, '443') * 2), ('Proxy-Authorization: %s\r\n' % cls.PROXY_AUTH) if cls.PROXY_AUTH else '')).encode('iso-8859-1'))
            if not HTTPMessage(psock, body=False, decode=None, timeout=timeout, max_length=max_length, max_hlength=max_hlength, decompress=False).code in ('200', '204'):
              raise
            pconnection[0] = cls.SSLContext.wrap_socket(psock, server_side=False, server_hostname=cls._netloc_split(url_p.netloc)[0])
          else:
            raise
        else:
          try:
            pconnection[0].settimeout(timeout)
          except:
            pass
        if url_p.scheme.lower() == 'http':
          if cls.PROXY_AUTH:
            headers['Proxy-Authorization'] = cls.PROXY_AUTH
          else:
            headers.pop('Proxy-Authorization', None)
        return ((url_p.path + ('?' + url_p.query if url_p.query else '')) if url_p.scheme.lower() != 'http' else url).replace(' ', '%20') or '/'
    HTTPRequest.PROXY = (proxy['ip'], proxy['port'])
    if proxy['auth']:
      HTTPRequest.PROXY_AUTH = 'Basic ' + base64.b64encode(proxy['auth'].encode('utf-8')).decode('utf-8')
    if proxy['secure']:
      HTTPRequest.PROXY_SECURE = True


class WGS84WebMercator():

  R = 6378137.0

  @staticmethod
  def WGS84toWebMercator(lat, lon):
    return (math.radians(lon) * WGS84WebMercator.R, math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * WGS84WebMercator.R)

  @staticmethod
  def WebMercatortoWGS84(x, y):
    return (math.degrees(2 * math.atan(math.exp(y / WGS84WebMercator.R)) - math.pi / 2), math.degrees(x / WGS84WebMercator.R))


class TilesCache():

  def __init__(self, size, threads, preload=None):
    self.Size = size
    self.Threads = threads
    if preload is None:
      self.Preload = size >= 10
    else:
      self.Preload = preload
    self.InfosBuffer = {}
    self.Buffer = {}
    self.BLock = threading.RLock()
    self.Events = {}
    self.Generators = []
    self.GAvailable = []
    self.GCondition = threading.Condition()
    self.Seq = 1
    self.Id = None
    self.Infos = None
    self.Closed = False
    self.log = partial(log, 'tilescache')
    self.log(2, 'init', size, threads)

  def _getitem(self, rid, pos):
    try:
      row, col = pos
    except:
      return None
    if self.Id is None or not self.Generators or self.Closed:
      self.log(2, 'cancel', row, col)
      return None
    ptile = None
    e = None
    seq = 0
    def _retrieveitem():
      nonlocal ptile
      nonlocal e
      with self.GCondition:
        tgen = None
        while tgen is None:
          if seq != self.Seq or self.Closed:
            ptile[0] = None
            e.set()
            with self.BLock:
              self.Events.pop(e, None)
              self.Buffer.pop((rid, pos), None)
            self.log(2, 'cancel', row, col)
            return
          if (a := self.GAvailable):
            tgen = self.Generators[a.pop()]
            gen = tgen[1]
          else:
            self.GCondition.wait()
        tgen[0] = False
      try:
        if (tile := gen(None, None, row, col)['tile']) is None:
          self.log(1, 'error', row, col)
        else:
          self.log(2, 'load', row, col)
      except:
        tile = None
        self.log(1, 'error', row, col)
      finally:
        with self.GCondition:
          if tgen[0]:
            gen(close_connection=True)
          else:
            tgen[0] = True
            if gen.pconnection[0] is None:
              a.appendleft(gen.ind)
            else:
              a.append(gen.ind)
            self.GCondition.notify()
        ptile[0] = tile
        e.set()
        with self.BLock:
          self.Events.pop(e, None)
    with self.BLock:
      if self.Closed:
        self.log(2, 'cancel', row, col)
        return None
      if (ptile := self.Buffer.pop((rid, pos), None)) is not None and (ptile[0] is not None or ptile[1] == self.Seq):
        self[(rid, pos)] = ptile
        self.log(2, 'found', row, col)
      else:
        seq = self.Seq
        if seq:
          e = threading.Event()
          self.Events[e] = self[(rid, pos)] = ptile = [e, seq]
          self.log(2, 'add', row, col, len(self.Buffer))
        else:
          self.log(2, 'cancel', row, col)
          return [None, 0]
    if e:
      t = threading.Thread(target=_retrieveitem, daemon=True)
      t.start()
    return ptile

  def WaitTile(self, ptile, timeout=None):
    if ptile is None:
      return None
    if isinstance((tile := ptile[0]), threading.Event):
      if self.Closed:
        return None
      tile.wait(timeout)
      if self.Closed:
        return None
      if isinstance((tile := ptile[0]), threading.Event):
        return None
      else:
        return tile
    else:
      return tile

  def __getitem__(self, id_pos):
    try:
      rid, pos = id_pos
      row, col = pos
    except:
      return partial(self.WaitTile, None)
    self.log(2, 'get', row, col)
    ptile = self._getitem(rid, pos)
    if self.Preload:
      self._getitem(rid, (row + 1, col + 1))
    return partial(self.WaitTile, ptile)

  def __setitem__(self, id_pos, ptile):
    try:
      rid, pos = id_pos
      row, col = pos
    except:
      return
    with self.BLock:
      self.Buffer[(rid, pos)] = ptile
      while len(self.Buffer) > self.Size:
        del self.Buffer[next(iter(self.Buffer))]
        self.log(2, 'del')

  def Configure(self, rid, tile_generator_builder):
    if self.Closed or not rid:
      return False
    self.log(1, 'configure', *rid)
    pconnections = [[None] for i in range(self.Threads)]
    with self.GCondition:
      seq = self.Seq
      self.Seq = 0
      for g in self.Generators:
        try:
          if (self.Id or (None, None))[0] == rid[0] and g[0]:
            pconnections[g[1].ind] = g[1].pconnection
          elif g[0]:
            g[1](close_connection=True)
          else:
            g[0] = True
        except:
          pass
      infos = self.InfosBuffer.get(rid, {})
      ifound = bool(infos)
      if ifound:
        self.log(2, 'ifound', *rid)
        infos_greedy = None
      else:
        infos_greedy = {}
      try:
        gens = tile_generator_builder(number=self.Threads, infos_completed=infos, pconnections=pconnections, infos_greedy=infos_greedy)
        if not gens:
          raise
        if self.Threads == 1:
          gens = [gens]
        self.Generators = [[True, g] for g in gens]
        self.Id = rid
        self.Infos = infos
        self.GAvailable = deque()
        for i in range(self.Threads):
          if pconnections[i][0] is None:
            self.GAvailable.appendleft(i)
          else:
            self.GAvailable.append(i)
        if not ifound:
          self.InfosBuffer.update({(rid[0], m): i for m, i in infos_greedy.items()})
      except:
        self.Id = None
        self.Infos = None
        self.GAvailable = []
        if rid[0] != -1:
          self.log(0, 'fail', *rid)
        return False
      finally:
        with self.BLock:
          for e, ptile in self.Events.items():
            ptile[0] = None
            e.set()
          self.Events.clear()
        self.Seq = seq + 1
        self.GCondition.notify_all()
    return True

  def Close(self):
    self.Closed = True
    with self.BLock:
      for e, ptile in self.Events.items():
        ptile[0] = None
        e.set()
      self.Events.clear()
      self.Buffer.clear()
    with self.GCondition:
      self.Id = None
      self.Infos = None
      self.GAvailable = []
      self.InfosBuffer.clear()
      self.GCondition.notify_all()
    for g in self.Generators:
      g[0] = True
      try:
        g[1](close_connection=True)
      except:
        pass
    self.Generators = []
    self.log(1, 'close')


class TilesMixCache(TilesCache):

  def __init__(self, size=None, threads=None, preload=None, wrap=None):
    self.Wrap = wrap
    if wrap is not None:
      self.Size = wrap.Size
      self.Threads = wrap.Threads
      self.Preload = wrap.Preload
      self.InfosBuffer = wrap.InfosBuffer
      self.Buffer = wrap.Buffer
      self.BLock = wrap.BLock
      if wrap.Id is not None:
        self.Generators = {wrap.Id: wrap.Generators}
        self.GAvailable = {wrap.Id: wrap.GAvailable}
        self.Id = [wrap.Id]
        self.Infos = {wrap.Id: wrap.Infos}
      else:
        self.Generators = {}
        self.GAvailable = {}
        self.Id = []
        self.Infos = {}
      self.GCondition = wrap.GCondition
      self.Seq = wrap.Seq + 1
      wrap.Closed = True
      with wrap.BLock:
        for e, ptile in wrap.Events.items():
          ptile[0] = None
          e.set()
        wrap.Events.clear()
      with wrap.GCondition:
        wrap.GCondition.notify_all()
    else:
      self.Size = size
      self.Threads = threads
      if preload is None:
        self.Preload = size >= 10
      else:
        self.Preload = preload
      self.InfosBuffer = {}
      self.Buffer = {}
      self.BLock = threading.RLock()
      self.Generators = {}
      self.GAvailable = {}
      self.GCondition = threading.Condition()
      self.Seq = 1
      self.Id = []
      self.Infos = {}
    self.TRunning = [0, 0]
    self.Queue = deque()
    self.Events = {}
    self.Closed = False
    self.log = partial(log, 'tilescache')
    self.log(2, 'init', size, threads)

  def _retriever(self, seq):
    while True:
      end = time.time() + 10
      with self.GCondition:
        if seq != self.Seq:
          return
        tr = self.TRunning
        tr[1] += 1
        while not self.Queue and not self.Closed and seq == self.Seq:
          if not self.GCondition.wait(end - time.time()):
            tr[0] -= 1
            tr[1] -= 1
            return
        if self.Closed or seq != self.Seq:
          return
        tr[1] -= 1
        rid, pos, ptile = self.Queue.popleft()
        row, col = pos
        e = ptile[0]
        if not (a := self.GAvailable.get(rid)):
          ptile[0] = None
          e.set()
          with self.BLock:
            self.Events.pop(e, None)
            self.Buffer.pop((rid, pos), None)
          self.log(2, 'cancel', row, col)
          continue
        tgen = self.Generators[rid][a.pop()]
        tgen[0] = False
      gen = tgen[1]
      try:
        if (tile := gen(None, None, row, col)['tile']) is None:
          self.log(1, 'error', row, col)
        else:
          self.log(2, 'load', row, col)
      except:
        tile = None
        self.log(1, 'error', row, col)
      finally:
        with self.GCondition:
          if tgen[0]:
            gen(close_connection=True)
          else:
            tgen[0] = True
            if gen.pconnection[0] is None:
              a.appendleft(gen.ind)
            else:
              a.append(gen.ind)
        ptile[0] = tile
        e.set()
        with self.BLock:
          self.Events.pop(e, None)

  def _getitem(self, rid, pos):
    try:
      row, col = pos
    except:
      return None
    ptile = None
    e = None
    with self.BLock:
      if not self.Id or self.Closed:
        self.log(2, 'cancel', row, col)
        return None
      if (ptile := self.Buffer.pop((rid, pos), None)) is not None and (ptile[0] is not None or ptile[1] == self.Seq):
        self[(rid, pos)] = ptile
        self.log(2, 'found', row, col)
      else:
        with self.GCondition:
          seq = self.Seq
          if seq:
            e = threading.Event()
            self.Events[e] = self[(rid, pos)] = ptile = [e, seq]
            self.log(2, 'add', row, col, len(self.Buffer))
          else:
            self.log(2, 'cancel', row, col)
            return [None, 0]
          self.Queue.append((rid, pos, ptile))
          if not self.TRunning[1] and self.TRunning[0] < self.Threads:
            self.TRunning[0] += 1
            t = threading.Thread(target=self._retriever, args=(seq,), daemon=True)
            t.start()
          self.GCondition.notify()
    return ptile

  def Configure(self, tile_generator_builders):
    if self.Closed or not tile_generator_builders:
      return False
    with self.GCondition:
      seq = self.Seq
      self.Seq = 0
      if not seq:
        return False
      self.GCondition.notify_all()
    rids = tile_generator_builders.keys()
    for rid in rids:
      self.log(1, 'configure', *rid)
    pconnections = {rid: [[None] for i in range(self.Threads)] for rid in rids}
    _rids = {rid: True for rid in rids}
    self.Queue.clear()
    for rid_, gens_ in self.Generators.items():
      pcons = next(((pconnections[rid], _rids.pop(rid))[0] for rid in _rids if rid_[0] == rid[0]), None)
      for g in gens_:
        try:
          if pcons and g[0]:
            pcons[g[1].ind] = g[1].pconnection
          elif g[0]:
            g[1](close_connection=True)
          else:
            g[0] = True
        except:
          pass
    self.TRunning = [0, 0]
    self.Generators = {}
    self.GAvailable = {}
    self.Id = list(rids)
    self.Infos = {}
    gens = {}
    infos = {}
    infos_greedy = {}
    def _build(rid):
      nonlocal gens
      try:
        gens[rid][:] = tile_generator_builders[rid](number=self.Threads, infos_completed=infos[rid], pconnections=pconnections[rid], infos_greedy=infos_greedy[rid])
      except:
        gens[rid].clear()
    th = []
    for rid in rids:
      infos[rid] = self.InfosBuffer.get(rid, {})
      if infos[rid]:
        self.log(2, 'ifound', *rid)
        infos_greedy[rid] = None
      else:
        infos_greedy[rid] = {}
      gens[rid] = []
      t = threading.Thread(target=_build, args=(rid,), daemon=True)
      th.append(t)
      t.start()
    try:
      for t in th:
        if self.Closed:
          raise
        t.join()
      if [] in gens.values():
        raise
      for rid in rids:
        if self.Threads == 1:
          gens[rid] = [gens[rid]]
        self.Generators[rid] = [[True, g] for g in gens[rid]]
        self.Infos[rid] = infos[rid]
        self.GAvailable[rid] = a = deque()
        pcons = pconnections[rid]
        for i in range(self.Threads):
          if pcons[i][0] is None:
            a.appendleft(i)
          else:
            a.append(i)
        if infos_greedy[rid] is not None:
          self.InfosBuffer.update({(rid[0], m): i for m, i in infos_greedy[rid].items()})
    except:
      self.Id = []
      self.Infos = {}
      self.Generators = {}
      self.GAvailable = {}
      self.log(0, 'fail', *rid)
      return False
    finally:
      with self.BLock:
        for e, ptile in self.Events.items():
          ptile[0] = None
          e.set()
        self.Events.clear()
      with self.GCondition:
        self.Seq = seq + 1
        self.GCondition.notify_all()
    return True

  def Close(self):
    with self.GCondition:
      if self.Closed:
        return
      self.Closed = True
      while not self.Seq:
        self.GCondition.wait()
      seq = self.Seq
      self.Seq = 0
      self.GCondition.notify_all()
    with self.BLock:
      for e, ptile in self.Events.items():
        ptile[0] = None
        e.set()
      self.Events.clear()
    gens = iter(self.Generators.values())
    wrap = self.Wrap
    if wrap is not None:
      if self.Id:
        wrap.Id = self.Id[0]
        wrap.Infos = self.Infos[wrap.Id]
        wrap.Generators = self.Generators[wrap.Id]
        wrap.GAvailable = self.GAvailable[wrap.Id]
      else:
        wrap.Id = None
        wrap.Generators = []
        wrap.Infos = None
        wrap.GAvailable = None
      wrap.Seq = seq + 1
      wrap.Closed = False
      next(gens, None)
    for gens_ in gens:
      for g in gens_:
        try:
          g[1](close_connection=True)
        except:
          pass
    self.Id = []
    self.Infos = {}
    self.InfosBuffer = {}
    self.Buffer = {}
    self.Generators = {}
    self.GAvailable = {}
    self.log(1, 'close')


class BaseMap(WGS84WebMercator):

  EXT_MIME = {'jpg': 'image/jpeg', 'png': 'image/png', 'bil': 'image/x-bil;bits=32', 'hgt': 'image/hgt', 'tif': 'image/tiff', 'png': 'image/png', 'bmp': 'image/bmp', 'web': 'image/webp', 'webp': 'image/webp', 'gif': 'image/gif', 'pdf': 'application/pdf', 'pbf': 'application/x-protobuf', 'mvt': 'application/vnd.mapbox-vector-tile', 'geojson': 'application/geo+json', 'geo': 'application/geo+json', 'json': 'application/json', 'svg': 'image/svg+xml'}
  DOTEXT_MIME = {'.' + e: m for e, m in EXT_MIME.items()}
  MIME_EXT = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/x-bil;bits=32': 'bil.xz', 'image/hgt': 'hgt.xz', 'image/tiff': 'tif', 'image/geotiff': 'tif', 'image/bmp': 'bmp', 'image/webp': 'webp', 'image/gif': 'gif', 'application/pdf': 'pdf', 'application/x-protobuf': 'pbf', 'application/vnd.mapbox-vector-tile': 'mvt', 'application/geo+json': 'geojson', 'application/json': 'json', 'image/svg+xml': 'svg'}
  MIME_DOTEXT = {m: '.' + e for m, e in MIME_EXT.items()}

  LOCALSTORE_DEFAULT_PATTERN = r'{alias|layer}\{matrix}\{row:0>}\{alias|layer}-{matrix}-{row:0>}-{col:0>}.{ext}'
  LOCALSTORE_HGT_DEFAULT_PATTERN = r'{alias|layer}\{hgt}.{ext}'
  WMS_PATTERN = {'GetCapabilities': '?SERVICE=WMS&REQUEST=GetCapabilities', 'GetMap': '?SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0&LAYERS={layers}&FORMAT={format}&STYLES={styles}&CRS={crs}&BBOX={bbox}&WIDTH={width}&HEIGHT={height}&DPI={dpi}&FORMAT_OPTIONS=DPI:{dpi}'}
  WMTS_PATTERN = {'GetCapabilities': '?SERVICE=WMTS&REQUEST=GetCapabilities', 'GetTile': '?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER={layer}&STYLE={style}&FORMAT={format}&TILEMATRIXSET={matrixset}&TILEMATRIX={matrix}&TILEROW={row}&TILECOL={col}'}

  def __new__(cls, *args, **kwargs):
    if cls is BaseMap:
      raise TypeError('the class BaseMap is not intended to be instantiated directly')
    return object.__new__(cls)

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

  def FetchMap(self, infos, minlat, maxlat, minlon, maxlon, maxheight, maxwidth, dpi=None, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None):
    self.log(2, 'mapfetch', infos)
    headers = {}
    if referer:
      headers['Referer'] = referer
    headers['User-Agent'] = user_agent
    if not infos.get('source') or not infos.get('layers'):
      self.log(0, 'maplfail', infos)
      return False
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
      infos['dpi'] = dpi or 90
    except:
      self.log(0, 'maplfail', infos)
      return False
    try:
      if '{wms}' in infos['source']:
        uri = infos['source'].format_map({'wms': self.WMS_PATTERN['GetMap'], 'key': key or ''}).format_map(infos)
      else:
        uri = infos['source'].format_map({**infos, 'key': key or ''})
      rep = HTTPRequest(uri, 'GET', headers, basic_auth=basic_auth)
      if rep.code != '200':
        raise
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

  def LoadMap(self, uri, minx=None, miny=None, maxx=None, maxy=None, resolution=None, referer=None, user_agent='GPXTweaker', basic_auth=None):
    self.log(2, 'mapfetch', uri)
    try:
      if '://' in uri:
        headers = {'User-Agent': user_agent}
        if referer:
          headers['Referer'] = referer
        rep = HTTPRequest(uri, 'GET', headers, basic_auth=basic_auth)
        if rep.code != '200':
          raise
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
      infos['format'] = WebMercatorMap.EXT_MIME.get(uri.replace('.xz', '').rsplit('.', 1)[-1][0:3], 'image')
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
        elif nmap[:4] in (b'\x49\x49\x2a\x00', b'\x4d\x4d\x00\x2a'):
          ba = {b'\x49\x49\x2a\x00': '<', b'\x4d\x4d\x00\x2a': '>'}[nmap[:4]]
          cpos = nmap.find(b'GPXTweaker: ')
          if cpos >= 0:
            infos = json.loads(nmap[cpos+12:cpos-8+struct.unpack(ba + 'L', nmap[cpos-20:cpos-16])[0]])
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
      elif self.Map[:4] in (b'\x49\x49\x2a\x00', b'\x4d\x4d\x00\x2a'):
        ba = {b'\x49\x49\x2a\x00': '<', b'\x4d\x4d\x00\x2a': '>'}[self.Map[:4]]
        L = ba + 'L'
        H = ba + 'H'
        ifd = struct.unpack(L, self.Map[4:8])[0]
        f = open(uri, 'wb')
        cpos = self.Map.find(b'GPXTweaker: ')
        if cpos >= 0:
          self.Map = self.Map[:cpos-26]
        while True:
          ne = struct.unpack(H, self.Map[ifd:ifd+2])[0]
          nifd =  struct.unpack(L, self.Map[ifd+2+12*ne:ifd+6+12*ne])[0]
          if cpos < 0:
            if not nifd:
              break
          else:
            if nifd == cpos - 26:
              self.Map = struct.pack(L, 0).join((self.Map[:ifd+2+12*ne], self.Map[ifd+6+12*ne:]))
              break
          ifd = nifd
        f.write(self.Map[:ifd+2+12*ne])
        f.write(struct.pack(L, len(self.Map)))
        f.write(self.Map[ifd+6+12*ne:])
        comment = ('GPXTweaker: ' + json.dumps(self.MapInfos)).encode('utf-8')
        f.write(struct.pack(H + 'HHLLL', 1, 37510, 7, 8 + len(comment), len(self.Map) + 18, 0) + b'\x55\x4e\x49\x43\x4F\x44\x45\x00' + comment + (b'\x00' if len(comment) % 2 else b''))
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

  def GetTileInfos(self, infos, matrix=None, lat=None, lon=None, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, pconnection=None, infos_wmts=None):
    if 'source' not in infos:
      return False
    if matrix is not None:
      infos['matrix'] = str(matrix)
    hgt = '{hgt}' in infos['source']
    if hgt:
      infos['matrix'] = '0'
    if 'matrix' not in infos:
      return False
    if '{wmts}' not in infos['source']:
      infos['format'] = infos.get('format') or WebMercatorMap.EXT_MIME.get(infos['source'].replace('.zip', '').rsplit('.', 1)[-1][0:3], 'image')
      if 'width' not in infos and 'height' not in infos:
        infos['width'] = infos['height'] = 3600 if hgt else 256
      if 'topx' not in infos and 'topy' not in infos:
        infos['topx'] = -180 if hgt else WGS84WebMercator.WGS84toWebMercator(0, -180)[0]
        infos['topy'] = 90 if hgt else WGS84WebMercator.WGS84toWebMercator(0, 180)[0]
      try:
        infos['scale'] = infos.setdefault('basescale', WGS84WebMercator.WGS84toWebMercator(0, 360)[0] /  infos['width'] / (360 if hgt else (2 if self.CRS == 'EPSG:4326' else 1))) / (2 ** int(infos['matrix']))
        if lat is not None and lon is not None :
          infos['row'], infos['col'] = self.WGS84toTile(infos, lat, lon)
      except:
        return False
      return True
    headers = {'User-Agent': user_agent}
    if referer:
      headers['Referer'] = referer
    if not infos.get('layer') or not infos.get('matrixset'):
      return False
    infos['style'] = infos.get('style') or ''
    infos['format'] = infos.get('format') or 'image/png'
    try:
      uri = infos['source'].format_map({'wmts': self.WMTS_PATTERN['GetCapabilities'], 'key': key or ''}).format_map(infos)
    except:
      return False
    rep = HTTPRequest(uri, 'GET', headers, pconnection=pconnection, basic_auth=basic_auth)
    if rep.code != '200':
      return False
    try:
      cap = minidom.parseString(rep.body)
      content = cap.getElementsByTagNameNS('*', 'Contents')[0]
      layer = None
      for node in content.getElementsByTagNameNS('*', 'Layer'):
        for c_node in node.childNodes:
          if c_node.localName == 'Identifier':
            if _XMLGetNodeText(c_node) == infos['layer']:
              layer = node
              break
        if layer:
          break
      if not layer:
        return False
      style = None
      for node in layer.getElementsByTagNameNS('*', 'Style'):
        for c_node in node.childNodes:
          if c_node.localName == 'Identifier':
            if _XMLGetNodeText(c_node) == infos['style']:
              style = node
            break
          if style:
            break
      if not style:
        return False
      matrixset = None
      for node in layer.getElementsByTagNameNS('*', 'TileMatrixSetLink'):
        for c_node in node.childNodes:
          if c_node.localName == 'TileMatrixSet':
            if _XMLGetNodeText(c_node) == infos['matrixset']:
              matrixset = node
            break
          if matrixset:
            break
      if not matrixset:
        return False
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
      if not matrixset:
        return False
      if hasattr(self, 'Legend'):
        try:
          self.Legend.GetTilesLegendInfos(infos, key, referer, user_agent, basic_auth, cap)
        except:
          pass
      infos['scale'] = None
      infos['topx'] = None
      infos['topy'] = None
      infos['width'] = None
      infos['height'] = None
      for node in matrixset.getElementsByTagNameNS('*', 'TileMatrix'):
        mtrx = _XMLGetNodeText(node.getElementsByTagNameNS('*', 'Identifier'))
        if mtrx == infos['matrix'] or infos_wmts is not None:
          infos_ = {}
          infos_['scale'] = float(_XMLGetNodeText(node.getElementsByTagNameNS('*', 'ScaleDenominator'))) * 0.28 / 1000
          infos_['topx'], infos_['topy'] = list(map(float, _XMLGetNodeText(node.getElementsByTagNameNS('*', 'TopLeftCorner')).split()))
          infos_['width'] = int(_XMLGetNodeText(node.getElementsByTagNameNS('*', 'TileWidth')))
          infos_['height'] = int(_XMLGetNodeText(node.getElementsByTagNameNS('*', 'TileHeight')))
        if mtrx == infos['matrix']:
          infos.update(infos_)
        if infos_wmts is not None:
          infos_wmts[mtrx] = infos_wmts_ = {k: infos[k] for k in ('source', 'layer', 'matrixset', 'style', 'format')}
          if 'alias' in infos:
            infos_wmts_['alias'] = infos['alias']
          infos_wmts_['matrix'] = mtrx
          infos_wmts_.update(infos_)
    except:
      return False
    finally:
      try:
        cap.unlink()
      except:
        pass
    if '' in map(lambda k: infos.get(k) or '', ('scale', 'topx', 'topy', 'width', 'height')):
      return False
    if lat is not None and lon is not None :
      try:
        infos['row'], infos['col'] = self.WGS84toTile(infos, lat, lon)
      except:
        return False
    return True

  def GetKnownTile(self, infos, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, pconnection=None):
    if 'source' not in infos:
      return None
    headers = {'User-Agent': user_agent}
    if referer:
      headers['Referer'] = referer
    try:
      if '{wmts}' not in infos['source']:
        if '{quadkey}' in infos['source']:
          quadkey = ''.join(map(lambda p: str(int(p[0]+p[1], 2)), zip(bin(int(infos['row']))[2:].rjust(int(infos['matrix']), '0'), bin(int(infos['col']))[2:].rjust(int(infos['matrix']), '0'))))
        else:
          quadkey = ''
        if '{hgt}' in infos['source']:
          lat = 89 - infos['row']
          lon = infos['col'] - 180
          hgt = ('N' if lat >= 0 else 'S') + ('%02i' % abs(lat)) + ('E' if lon >= 0 else 'O') + ('%03i' % abs(lon))
        else:
          hgt = ''
        if '{invrow}' in infos['source']:
          invrow = str(round(infos['topy'] / infos['scale'] / infos['height'] * 2 - infos['row'] - 1))
        else:
          invrow = ''
        uri = infos['source'].format_map({**infos, 'quadkey': quadkey, 'hgt': hgt, 'invrow': invrow, 'key': key or ''})
      else:
        uri = infos['source'].format_map({'wmts': self.WMTS_PATTERN['GetTile'], 'key': key or ''}).format_map(infos)
    except:
      return None
    try:
      rep = HTTPRequest(uri, 'GET', headers, pconnection=pconnection, basic_auth=basic_auth)
      if rep.code != '200':
        return None
      if 'zip' in rep.header('content-type', '').lower() or infos.get('source', '').lower().rsplit('.', 1)[-1][0:3] == 'zip':
        try:
          zf = zipfile.ZipFile(BytesIO(rep.body), 'r')
          nl = zf.namelist()
          tile = zf.read(next((n for n in nl if os.path.splitext(n)[1].lower() in ('.hgt', '.bil')), next((n for n in nl if 'dem' in n), nl[0])))
          zf.close()
        except:
          tile = rep.body
      else:
        tile = rep.body
    except:
      return None
    return tile

  def GetTile(self, infos, matrix, lat, lon, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, pconnection=None):
    try:
      if not self.GetTileInfos(infos, matrix, lat, lon, key, referer, user_agent, basic_auth, pconnection):
        return None
      tile = self.GetKnownTile(infos, key, referer, user_agent, basic_auth, pconnection)
    except:
      return None
    return tile

  def _match_infos(self, pattern, infos, update_dict=False, update_json=False):
    if '{' not in pattern:
      pattern = os.path.join(pattern, (self.LOCALSTORE_DEFAULT_PATTERN if (infos.get('format') != 'image/hgt' and '{hgt}' not in infos.get('source', '')) else self.LOCALSTORE_HGT_DEFAULT_PATTERN))
    infopattern = os.path.dirname(pattern)
    while '{matrix}' in os.path.dirname(infopattern) or '{hgt}' in infopattern:
      infopattern = os.path.dirname(infopattern)
    try:
      infopath = os.path.join(infopattern.format_map({**infos, **{'alias|layer': infos.get('alias') or infos.get('layer', '')}}), 'infos.json')
    except:
      return False
    if not os.path.exists(infopath):
      if update_json and not update_dict:
        try:
          Path(os.path.dirname(infopath)).mkdir(parents=True, exist_ok=True)
        except:
          return False
        inf = {k: v for k, v in infos.items() if k not in ('row', 'col')}
        needs_update = True
      else:
        return False
    else:
      try:
        f = open(infopath, 'rt', encoding='utf-8')
        inf = json.load(f)
        if False in (k not in infos or infos.get(k, '') == inf.get(k, '') for k in ('layer', 'matrixset', 'style', 'format', 'matrix')):
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
      needs_update = False
      if update_json:
        for k in ('alias', 'source'):
          if k in infos and infos.get(k, '') != inf.get(k, ''):
            inf[k] = infos[k]
            needs_update = True
      if update_dict:
        infos.update({k: v for k, v in inf.items() if (not infos.get(k) or k not in ('alias', 'source'))})
        try:
          infos['width'] = int(infos['width'])
          infos['height'] = int(infos['height'])
        except:
          return False
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

  def ReadTileInfos(self, pattern, infos, matrix=None, lat=None, lon=None, update_json=False):
    if matrix is not None:
      infos['matrix'] = str(matrix)
    if '{hgt}' in infos.get('source', '') or infos.get('format') == 'image/hgt':
      infos['matrix'] = '0'
    if 'matrix' not in infos:
      return False
    if '{' not in pattern:
      pattern = os.path.join(pattern, (self.LOCALSTORE_DEFAULT_PATTERN if (infos.get('format') != 'image/hgt' and '{hgt}' not in infos.get('source', '')) else self.LOCALSTORE_HGT_DEFAULT_PATTERN))
    if not self._match_infos(pattern, infos, update_dict=True, update_json=update_json):
      return False
    try:
      if not infos.get('source'):
        return False
      if '' in map(lambda k: infos.get(k) or '', ('layer', 'topx', 'topy', 'width', 'height')):
        return False
      if not infos.get('scale'):
        if '{wmts}' in infos['source']:
          return False
        infos['scale'] = infos['basescale'] / (2 ** int(infos['matrix']))
    except:
      return False
    if lat is not None and lon is not None :
      try:
        infos['row'], infos['col'] = self.WGS84toTile(infos, lat, lon)
      except:
        return False
    return True

  def ReadKnownTile(self, pattern, infos, just_lookup=False):
    try:
      if '{' not in pattern:
        pattern = os.path.join(pattern, (self.LOCALSTORE_DEFAULT_PATTERN.replace('{row:0>}', '{row:0>%s}' % len(str(int(math.pi * WGS84WebMercator.R * 2 / infos['height'] / infos['scale'])))).replace('{col:0>}', '{col:0>%s}' % len(str(int(math.pi * WGS84WebMercator.R * 2 / infos['width'] / infos['scale']))))) if (infos.get('format') != 'image/hgt' and '{hgt}' not in infos.get('source', '')) else self.LOCALSTORE_HGT_DEFAULT_PATTERN)
      hgt = ''
      ext = WebMercatorMap.MIME_EXT.get(infos['format'], 'img')
      if ext == 'hgt.xz' or '{hgt}' in pattern:
        lat = 89 - infos['row']
        lon = infos['col'] - 180
        hgt = ('N' if lat >= 0 else 'S') + ('%02i' % abs(lat)) + ('E' if lon >= 0 else 'O') + ('%03i' % abs(lon))
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
      return False if just_lookup else None
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
    if '{' not in pattern:
      pattern = os.path.join(pattern, (self.LOCALSTORE_DEFAULT_PATTERN.replace('{row:0>}', '{row:0>%s}' % len(str(int(math.pi * WGS84WebMercator.R * 2 / infos['height'] / infos['scale'])))).replace('{col:0>}', '{col:0>%s}' % len(str(int(math.pi * WGS84WebMercator.R * 2 / infos['width'] / infos['scale']))))) if (infos.get('format') != 'image/hgt' and '{hgt}' not in infos.get('source', '')) else self.LOCALSTORE_HGT_DEFAULT_PATTERN)
    ext = WebMercatorMap.MIME_EXT.get(infos['format'], 'img')
    if match_json:
      if not self._match_infos(pattern, infos, update_json=True):
        return False
    if tile is not None:
      hgt = ''
      if ext == 'hgt.xz' or '{hgt}' in pattern:
        lat = 89 - infos['row']
        lon = infos['col'] - 180
        hgt = ('N' if lat >= 0 else 'S') + ('%02i' % abs(lat)) + ('E' if lon >= 0 else 'O') + ('%03i' % abs(lon))
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

  def RetrieveTile(self, infos, local_pattern, local_expiration, local_store, key, referer, user_agent, basic_auth, only_local, pconnection=None, action=None, only_save=False):
    self.log(2, 'tileretrieve', infos)
    tile = None
    local_tile = None
    expired = True
    if isinstance(action, list):
      if len(action) == 0:
        action.append('failed')
      else:
        action[0] = 'failed'
    try:
      if local_pattern is not None:
        last_mod = self.ReadKnownTile(local_pattern, infos, just_lookup=True)
        if last_mod != False:
          self.log(2, 'tilelfound', infos)
          if only_save:
            tile = True
          else:
            tile = self.ReadKnownTile(local_pattern, infos)
          if tile:
            if local_expiration is not None:
              if local_expiration > max(time.time() - last_mod, 0) / 86400:
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
        if only_local:
          tile = None
        else:
          self.log(2, 'tilefetch', infos)
          tile = self.GetKnownTile(infos, key, referer, user_agent, basic_auth, pconnection)
          if tile and isinstance(action, list):
            action[0] = 'read_from_server'
        if tile is not None and local_pattern is not None:
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
    if tile is None:
      self.log(1, 'tilerfail', infos)
    else:
      self.log(2, 'tileretrieved', infos)
    return tile

  def TileGenerator(self, infos_base, matrix, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, only_local=False, number=1, infos_completed=None, pconnections=None, infos_greedy=None):
    if isinstance(pconnections, list):
      if len(pconnections) < number:
        pconnections.extend([[None] for i in range(number - len(pconnections))])
    else:
      pconnections = [[None] for i in range(number)]
    if infos_completed is None:
      infos_completed = {}
    if (False in (k in infos_completed for k in ('source', 'layer',  'format', 'matrix', 'scale', 'topx', 'topy', 'width', 'height'))) or (False in (k in infos_completed for k in (('matrixset', 'style') if '{wmts}' in infos_completed.get('source', '') else ('basescale', )))):
      infos_set = False
      infos_completed.update(infos_base)
      try:
        if local_pattern is not None:
          if self.ReadTileInfos(local_pattern, infos_completed, matrix, update_json=local_store):
            infos_set = True
        if not infos_set:
          if only_local:
            return None
          if not self.GetTileInfos(infos_completed, matrix, None, None, key, referer, user_agent, basic_auth, next((pconnection for pconnection in pconnections if pconnection[0] is not None), pconnections[0]), infos_greedy):
            return None
          if local_store:
            if not self.SaveTile(local_pattern, infos_completed):
              return None
          else:
            local_pattern = None
      except:
        return None
    if infos_greedy is not None:
      infos_greedy[infos_completed['matrix']] = infos_completed
    linfos = [{**infos_completed} for i in range(number)]
    def retrieve_tiles(a=None, b=None, c=None, d=None, just_box=False, close_connection=False, ind=0):
      nonlocal pconnections
      if close_connection is None:
        return pconnections[ind]
      if close_connection:
        try:
          pconnections[ind][0].close()
        except:
          pass
        pconnections[ind][0] = None
      if a is None and b is None and c is None and d is None:
        return {k: v for k, v in linfos[ind].items() if k not in ('row', 'col')}
      if not pconnections[ind]:
        pconnections[ind] = [None]
      if c is None or d is None:
        try:
          row, col = self.WGS84toTile(linfos[ind], a, b)
          if just_box:
            return ((row, col), (row, col))
          linfos[ind]['col'] = col
          linfos[ind]['row'] = row
          return {'infos': {**linfos[ind]}, 'tile': self.RetrieveTile(linfos[ind], local_pattern, local_expiration, local_store, key, referer, user_agent, basic_auth, only_local, pconnections[ind])}
        except:
          return None
      elif a is None and b is None:
        if just_box:
          return ((c, d), (c, d))
        linfos[ind]['row'] = c
        linfos[ind]['col'] = d
        try:
          return {'infos': {**linfos[ind]}, 'tile': self.RetrieveTile(linfos[ind], local_pattern, local_expiration, local_store, key, referer, user_agent, basic_auth, only_local, pconnections[ind])}
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
                  yield {'infos': {**linfos[ind]}, 'tile': self.RetrieveTile(linfos[ind], local_pattern, local_expiration, local_store, key, referer, user_agent, basic_auth, only_local, pconnections[ind])}
                except:
                  yield None
          return gen_tiles()
        except:
          return None
    def bind_retrieve_tiles(ind):
      def bound_retrieve_tiles(a=None, b=None, c=None, d=None, just_box=False, close_connection=False):
        return retrieve_tiles(a, b, c, d, just_box, close_connection, ind)
      bound_retrieve_tiles.ind = ind
      bound_retrieve_tiles.pconnection = pconnections[ind]
      return bound_retrieve_tiles
    return bind_retrieve_tiles(0) if number == 1 else [bind_retrieve_tiles(i) for i in range(number)]

  def RetrieveTiles(self, infos, matrix, minlat, maxlat, minlon, maxlon, local_pattern=None, local_expiration=None, local_store=False, memory_store=None, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, only_local=False, threads=10):
    if not local_store and memory_store is None:
      return False
    infos_set = False
    try:
      if local_pattern is not None:
        if self.ReadTileInfos(local_pattern, infos, matrix, update_json=local_store):
          infos_set = True
      if not infos_set:
        if only_local:
          return False
        if not self.GetTileInfos(infos, matrix, None, None, key, referer, user_agent, basic_auth):
          return False
        if local_store:
          if not self.SaveTile(local_pattern, infos):
            return None
        else:
          local_pattern = None
    except:
      return False
    try:
      (minrow, mincol), (maxrow, maxcol) = self.WGS84BoxtoTileBox(infos, minlat, maxlat, minlon, maxlon)
    except:
      return False
    if minrow > maxrow or mincol > maxcol:
      return False
    if local_pattern:
      if '{' not in local_pattern:
        local_pattern = os.path.join(local_pattern, (self.LOCALSTORE_DEFAULT_PATTERN.replace('{row:0>}', '{row:0>%s}' % len(str(int(math.pi * WGS84WebMercator.R * 2 / infos['height'] / infos['scale'])))).replace('{col:0>}', '{col:0>%s}' % len(str(int(math.pi * WGS84WebMercator.R * 2 / infos['width'] / infos['scale']))))) if (infos.get('format') != 'image/hgt' and '{hgt}' not in infos.get('source', '')) else self.LOCALSTORE_HGT_DEFAULT_PATTERN)
    if memory_store is not None:
      for col in range(mincol, maxcol + 1):
        memory_store.append([None] * (maxrow + 1 - minrow))
    box = ((row, col) for col in range(mincol, maxcol + 1) for row in range(minrow, maxrow + 1))
    lock = threading.Lock()
    progress = {'box': ((minrow, mincol), (maxrow, maxcol)), 'total': (maxcol + 1 - mincol) * (maxrow +1 - minrow), 'downloaded': 0, 'skipped': 0, 'failed': 0, 'percent': '0%', 'finish_event':threading.Event(), 'process_event':threading.Event()}
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
          tile = self.RetrieveTile({**infos, **{'row': row, 'col': col}}, local_pattern, local_expiration, local_store, key, referer, user_agent, basic_auth, only_local, pconnection, action, memory_store is None)
          if memory_store is not None:
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
    downloaders = [threading.Thread(target=downloader, daemon=True) for t in range(threads)]
    for downloader in downloaders:
      downloader.start()
    return progress

  def DownloadTiles(self, pattern, infos, matrix, minlat, maxlat, minlon, maxlon, expiration=None, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, threads=10):
    return self.RetrieveTiles(infos, matrix, minlat, maxlat, minlon, maxlon, local_pattern=pattern, local_expiration=expiration, local_store=True, key=key, referer=referer, user_agent=user_agent, basic_auth=basic_auth, threads=threads)

  def AssembleMap(self, infos, matrix, minlat, maxlat, minlon, maxlon, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, only_local=False, threads=10, tiles_cache=None):
    tiles = []
    if tiles_cache is not None:
      if matrix is not None:
        infos['matrix'] = matrix
      rid = tiles_cache.Id
      if isinstance(rid, list):
        _rid = next((rid_ for rid_, inf_ in tiles_cache.Infos.items() if not any((infos[k] != inf_[k] for k in infos if ((k in inf_) and ((k in ('layer', 'format', 'matrix')) or (k in ('matrixset', 'style') and '{wmts}' in inf_.get('source', ''))))))), None)
        if _rid is None:
          return False
        rid = _rid
        infos.update({k:v for k,v in tiles_cache.Infos[rid].items() if k != 'source'})
      else:
        if any(infos[k] != tiles_cache.Infos[k] for k in infos if ((k in tiles_cache.Infos) and ((k in ('layer', 'format', 'matrix')) or (k in ('matrixset', 'style') and '{wmts}' in tiles_cache.Infos.get('source', ''))))):
          return False
        infos.update({k:v for k,v in tiles_cache.Infos.items() if k != 'source'})
      try:
        (minrow, mincol), (maxrow, maxcol) = self.WGS84BoxtoTileBox(infos, minlat, maxlat, minlon, maxlon)
      except:
        return False
      if minrow > maxrow or mincol > maxcol:
        return False
      box = ((row, col) for col in range(mincol, maxcol + 1) for row in range(minrow, maxrow + 1))
      for col in range(mincol, maxcol + 1):
        tiles.append([None] * (maxrow + 1 - minrow))
      lock = threading.Lock()
      tot = (maxcol + 1 - mincol) * (maxrow +1 - minrow)
      finished = threading.Event()
      def retriever():
        nonlocal tot
        while True:
          try:
            with lock:
              row, col = next(box)
            tiles[col - mincol][row - minrow] = tiles_cache[rid, (row, col)](30)
          except StopIteration:
            break
          except:
            tiles[col - mincol][row - minrow] = None
          with lock:
            tot -= 1
            if tot == 0:
              finished.set()
      retrievers = [threading.Thread(target=retriever, daemon=True) for t in range(tiles_cache.Threads)]
      for retriever in retrievers:
        retriever.start()
      finished.wait()
    else:
      progress = self.RetrieveTiles(infos, matrix, minlat, maxlat, minlon, maxlon, local_pattern=local_pattern, local_expiration=local_expiration, local_store=local_store, memory_store=tiles, key=key, referer=referer, user_agent=user_agent, basic_auth=basic_auth, only_local=only_local, threads=threads)
      if not progress:
        return False
      (minrow, mincol), (maxrow, maxcol) = progress['box']
      progress['finish_event'].wait()
    map = self.MergeTiles(infos, tiles)
    if not map:
      return False
    self.Map = map
    self.MapResolution = infos['scale'] / self.CRS_MPU
    self.MapInfos = {(k + ('s' if k in ('layer', 'style') else '')): v for k, v in infos.items() if k in ('alias', 'layer', 'format', 'style', 'nodata')}
    self.MapInfos['source'] = infos.get('source', '')
    self.MapInfos['crs'] = self.CRS
    minx = infos['topx'] + self.MapResolution * infos['width'] * mincol
    miny = infos['topy'] - self.MapResolution * infos['height'] * (maxrow + 1)
    maxx = infos['topx'] + self.MapResolution * infos['width'] * (maxcol + 1)
    maxy = infos['topy'] - self.MapResolution * infos['height'] * minrow
    hgt = '{hgt}' in infos.get('source', '') or infos.get('format') in ('image/hgt', 'image/tiff', 'image/geotiff')
    if hgt:
      self.MapInfos['format'] = 'image/hgt'
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
    if hgt:
      self.MapInfos['width'] += 1
      self.MapInfos['height'] += 1
    return True

  def CoordtoPixels(self, x, y):
    tr = lambda z, s: z if z < s else z - 1
    minx, miny, maxx, maxy = map(float, self.MapInfos['bbox'].split(','))
    return (tr(int((x - minx) / self.MapResolution), round((maxx - minx) / self.MapResolution)), tr(int((maxy - y) / self.MapResolution), round((maxy - miny) / self.MapResolution)))

  def SetTilesProvider(self, rid, infos_base, matrix, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, only_local=False):
    try:
      tile_generator_builder = partial(self.TileGenerator, infos_base, matrix, local_pattern=local_pattern, local_expiration=local_expiration, local_store=local_store, key=key, referer=referer, user_agent=user_agent, basic_auth=basic_auth, only_local=only_local)
      if self.TilesInfos:
        infos = {**self.TilesInfos}
      else:
        infos = None
      self.TilesInfos = {**infos_base, 'matrix': matrix}
      if isinstance(self.Tiles, TilesMixCache):
        self.Tiles.Close()
        self.Tiles = self.Tiles.Wrap
      if not self.Tiles.Configure(rid, tile_generator_builder):
        self.TilesInfos = infos
        return False
      self.TilesInfos = self.Tiles.Infos
    except:
      return False
    return True


class WebMercatorMap(BaseMap):

  CRS = 'EPSG:3857'
  CRS_MPU = 1
  WMS_BBOX = '{minx},{miny},{maxx},{maxy}'
  WMS_IGN_SOURCE = 'https://wxs.ign.fr/{key}/geoportail/r/wms'
  MS_IGN_PLANV2 = {'alias': 'IGN_PLANV2', 'source': WMS_IGN_SOURCE + '{wms}', 'layers':'GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2', 'format': 'image/png', 'styles': ''}
  MS_IGN_SCAN25 = {'alias': 'IGN_SCAN25', 'source': WMS_IGN_SOURCE + '{wms}', 'layers':'SCAN25TOUR_PYR-PNG_FXX_LAMB93', 'format': 'image/png', 'styles': ''} #SCAN25TOUR_PYR-JPEG_WLD_WM
  MS_IGN_SCAN100 = {'alias': 'IGN_SCAN100', 'source': WMS_IGN_SOURCE + '{wms}', 'layers':'SCAN100_PYR-PNG_FXX_LAMB93', 'format': 'image/png', 'styles': ''} #SCAN100_PYR-JPEG_WLD_WM
  MS_IGN_CARTES = {'alias': 'IGN_CARTES', 'source': WMS_IGN_SOURCE + '{wms}', 'layers':'GEOGRAPHICALGRIDSYSTEMS.MAPS', 'format': 'image/png', 'styles': ''}
  MS_IGN_PHOTOS = {'alias': 'IGN_PHOTOS', 'source': WMS_IGN_SOURCE + '{wms}', 'layers': 'ORTHOIMAGERY.ORTHOPHOTOS', 'format': 'image/png', 'styles': ''}
  WMS_OSM_SOURCE = 'https://ows.terrestris.de/osm/service'
  MS_OSM = {'alias': 'OSM', 'source': WMS_OSM_SOURCE + '{wms}', 'layers':'OSM-WMS', 'format': 'image/png', 'styles': ''}
  WMTS_IGN_SOURCE = 'https://wxs.ign.fr/{key}/wmts'
  TS_IGN_PLANV2 = {'alias': 'IGN_PLANV2', 'source': WMTS_IGN_SOURCE + '{wmts}', 'layer': 'GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2', 'matrixset': 'PM', 'style': 'normal', 'format': 'image/png'}
  TS_IGN_CARTES = {'alias': 'IGN_CARTES', 'source': WMTS_IGN_SOURCE + '{wmts}', 'layer': 'GEOGRAPHICALGRIDSYSTEMS.MAPS', 'matrixset': 'PM', 'style': 'normal', 'format': 'image/jpeg'}  #SCAN 1000: 9-10 SCAN Régional: 11-12 SCAN 100: 13-14 - SCAN25: 15-16 - SCAN EXPRESS: 17-18
  TS_IGN_PHOTOS = {'alias': 'IGN_PHOTOS', 'source': WMTS_IGN_SOURCE + '{wmts}', 'layer': 'ORTHOIMAGERY.ORTHOPHOTOS', 'matrixset': 'PM', 'style': 'normal', 'format': 'image/jpeg'}
  TS_IGN_NOMS = {'alias': 'IGN_NOMS', 'source': WMTS_IGN_SOURCE + '{wmts}', 'layer': 'GEOGRAPHICALNAMES.NAMES', 'matrixset': 'PM', 'style': 'normal', 'format': 'image/png'}
  TC_IGN_HYBRIDE = [['IGN_PHOTOS', '1'], ['IGN_NOMS', '1', {'19':'18', '20':'18'}]]
  TS_IGN_CONTOUR = {'alias': 'IGN_CONTOUR', 'source': WMTS_IGN_SOURCE + '{wmts}', 'layer': 'ELEVATION.CONTOUR.LINE', 'matrixset': 'PM', 'style': 'normal', 'format': 'image/png'}
  TS_IGN_PENTESMONTAGNE = {'alias': 'IGN_PENTESMONTAGNE', 'source': WMTS_IGN_SOURCE + '{wmts}', 'layer': 'GEOGRAPHICALGRIDSYSTEMS.SLOPES.MOUNTAIN', 'matrixset': 'PM', 'style': 'normal', 'format': 'image/png'}
  TC_IGN_RELIEF = [['IGN_PLANV2', '100%'], ['IGN_PENTESMONTAGNE', '80%', {'18':'17', '19':'17'}], ['IGN_CONTOUR', '100%', {'19':'18'}]]
  TS_IGN_OMBRAGE = {'alias': 'IGN_OMBRAGE', 'source': WMTS_IGN_SOURCE + '{wmts}', 'layer': 'ELEVATION.ELEVATIONGRIDCOVERAGE.SHADOW', 'matrixset': 'PM', 'style': 'estompage_grayscale', 'format': 'image/png'}
  TS_IGN_VECTOR_SOURCE = 'https://wxs.ign.fr/{key}/static/vectorTiles/styles'
  TS_IGN_PLAN = {'alias': 'IGN_PLAN', 'source': TS_IGN_VECTOR_SOURCE + '/PLAN.IGN/standard.json', 'layer': 'PLAN.IGN', 'style': 'standard', 'format': 'application/json', 'overwrite_schemes': 'xyz'}
  TC_IGN_PLANESTOMPÉ = [['IGN_PLAN', '100%'], ['IGN_OMBRAGE', '80%', {'16':'15', '17': '15', '18':'15', '19': '15'}]]
  TS_OSM_SOURCE = 'https://a.tile.openstreetmap.org'
  TS_OSM = {'alias': 'OSM', 'source': TS_OSM_SOURCE + '/{matrix}/{col}/{row}.png', 'layer':'OSM', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TC_OSM_ESTOMPÉ = [['OSM', '100%'], ['IGN_OMBRAGE', '80%', {'16':'15', '17':'15', '18':'15', '19':'15'}]]
  TC_OSM_SHADED = [['OSM', '100%'], ['ESRI_HILLSHADE', 'x80%', {'16':'15', '17':'15', '18':'15', '19':'15'}]]
  TS_OTM_SOURCE = 'https://b.tile.opentopomap.org'
  TS_OTM = {'alias': 'OTM', 'source': TS_OTM_SOURCE + '/{matrix}/{col}/{row}.png', 'layer':'OSM', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_WAYMARKED_HILLSHADING = {'alias': 'WAYMARKED_HILLSHADING', 'source': 'https://hillshading.waymarkedtrails.org/srtm/{matrix}/{col}/{invrow}.png', 'layer':'hillshading', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_WAYMARKED_HIKING = {'alias': 'WAYMARKED_HIKING', 'source': 'https://tile.waymarkedtrails.org/hiking/{matrix}/{col}/{row}.png', 'layer':'hiking', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TC_WAYMARKED_TRAILSHIKING = [['OSM', '100%'], ['WAYMARKED_HILLSHADING', '40%'], ['WAYMARKED_HIKING', '100%']]
  TS_WAYMARKED_CYCLING = {'alias': 'WAYMARKED_CYCLING', 'source': 'https://tile.waymarkedtrails.org/cycling/{matrix}/{col}/{row}.png', 'layer':'cycling', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TC_WAYMARKED_TRAILSCYCLING = [['OSM', '100%'], ['WAYMARKED_HILLSHADING', '40%'], ['WAYMARKED_CYCLING', '100%']]
  TS_CYCLOSM = {'alias': 'CYCLOSM', 'source': 'https://a.tile-cyclosm.openstreetmap.fr/cyclosm/{matrix}/{col}/{row}.png', 'layer':'CyclOSM', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_TRACESTRACK_TOPO = {'alias': 'TRACESTRACK_TOPO', 'source': 'https://tile.tracestrack.com/topo__/{matrix}/{col}/{row}.png?key={key}', 'layer':'totp', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_TRACESTRACK_BICYCLE = {'alias': 'TRACESTRACK_BICYCLE', 'source': 'https://tile.tracestrack.com/bicycle-route/{matrix}/{col}/{row}.png?key={key}', 'layer':'cycle', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TC_TRACESTRACK_CYCLE = [['TRACESTRACK_TOPO', '100%'], ['TRACESTRACK_BICYCLE', '100%']]
  TS_MAPTILER_SOURCE = 'https://api.maptiler.com/maps'
  TS_MAPTILER_TOPO = {'alias': 'MAPTILER_TOPO', 'source': TS_MAPTILER_SOURCE + '/topo/style.json?key={key}', 'layer':'MAPTILER.TOPO', 'style': 'topo', 'format': 'application/json'}
  TS_MAPTILER_OUTDOOR = {'alias': 'MAPTILER_OUTDOOR', 'source': TS_MAPTILER_SOURCE + '/outdoor-v2/style.json?key={key}', 'layer':'MAPTILER.OUTDOOR', 'style': 'outdoor', 'format': 'application/json'}
  TS_GOOGLE_SOURCE = 'https://mts1.google.com/vt'
  TS_GOOGLE_MAP = {'alias': 'GOOGLE_MAP', 'source': TS_GOOGLE_SOURCE + '/lyrs=m&x={col}&y={row}&z={matrix}', 'layer':'GOOGLE.MAP', 'format': 'image/png', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_GOOGLE_HYBRID = {'alias': 'GOOGLE_HYBRID', 'source': TS_GOOGLE_SOURCE + '/lyrs=y&x={col}&y={row}&z={matrix}', 'layer':'GOOGLE.MAP', 'format': 'image/png', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_GOOGLE_TERRAIN = {'alias': 'GOOGLE_TERRAIN', 'source': TS_GOOGLE_SOURCE + '/lyrs=p&x={col}&y={row}&z={matrix}', 'layer':'GOOGLE.MAP', 'format': 'image/png', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_GOOGLE_SATELLITE = {'alias': 'GOOGLE_SATELLITE', 'source': TS_GOOGLE_SOURCE + '/lyrs=s&x={col}&y={row}&z={matrix}', 'layer':'GOOGLE.MAP', 'format': 'image/png', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_BING_SOURCE = 'https://ecn.t0.tiles.virtualearth.net'
  TS_BING_MAP = {'alias': 'BING_MAP', 'source': TS_BING_SOURCE + '/tiles/r{quadkey}.png?g=1', 'layer':'BING.MAP', 'format': 'image/png', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_BING_AERIAL = {'alias': 'BING_AERIAL', 'source': TS_BING_SOURCE + '/tiles/a{quadkey}.png?g=1', 'layer':'BING.MAP', 'format': 'image/png', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_BING_HYBRID = {'alias': 'BING_HYBRID', 'source': TS_BING_SOURCE + '/tiles/h{quadkey}.png?g=1', 'layer':'BING.MAP', 'format': 'image/png', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  WMTS_ESRI_SOURCE = 'https://services.arcgisonline.com/arcgis/rest/services'
  TS_ESRI_TOPOMAP = {'alias': 'ESRI_TOPOMAP', 'source': WMTS_ESRI_SOURCE + '/World_Topo_Map/MapServer/WMTS{wmts}', 'layer': 'World_Topo_Map', 'matrixset': 'default028mm', 'style': 'default', 'format': 'image/jpeg'}
  TS_ESRI_IMAGERY = {'alias': 'ESRI_IMAGERY', 'source': WMTS_ESRI_SOURCE + '/World_Imagery/MapServer/WMTS{wmts}', 'layer': 'World_Imagery', 'matrixset': 'default028mm', 'style': 'default', 'format': 'image/jpeg'}
  TS_ESRI_HILLSHADE = {'alias': 'ESRI_HILLSHADE', 'source': WMTS_ESRI_SOURCE + '/Elevation/World_Hillshade/MapServer/WMTS{wmts}', 'layer': 'Elevation_World_Hillshade', 'matrixset': 'default028mm', 'style': 'default', 'format': 'image/jpeg'}
  TC_ESRI_SHADED = [['ESRI_TOPOMAP', '100%'], ['ESRI_HILLSHADE', 'x80%', {'16':'15', '17':'15', '18':'15', '19':'15'}]]
  TS_ESRI_REFERENCE = {'alias': 'ESRI_REFERENCE', 'source': 'https://www.arcgis.com/sharing/rest/content/items/2a2e806e6e654ea78ecb705149ceae9f/resources/styles/root.json', 'layer': 'Hybrid_Reference_Local', 'style': 'hybrid_reference_local', 'format': 'application/json', 'slash_url': True, 'overwrite_names': 'ESRI_WORLDBASEMAPV2'}
  TC_ESRI_HYBRID = [['ESRI_IMAGERY', '100%'], ['ESRI_REFERENCE', '100%']]
  TS_THUNDERFOREST_SOURCE = 'https://tile.thunderforest.com'
  TS_THUNDERFOREST_LANDSCAPE = {'alias': 'THUNDERFOREST_LANDSCAPE', 'source': TS_THUNDERFOREST_SOURCE + '/landscape/{matrix}/{col}/{row}.png?apikey={key}', 'layer':'THUNDERFOREST.LANDSCAPE', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_THUNDERFOREST_OUTDOORS = {'alias': 'THUNDERFOREST_OUTDOORS', 'source': TS_THUNDERFOREST_SOURCE + '/outdoors/{matrix}/{col}/{row}.png?apikey={key}', 'layer':'THUNDERFOREST.OUTDOORS', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  TS_THUNDERFOREST_CYCLE = {'alias': 'THUNDERFOREST_CYCLE', 'source': TS_THUNDERFOREST_SOURCE + '/cycle/{matrix}/{col}/{row}.png?apikey={key}', 'layer':'THUNDERFOREST.CYCLE', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256}
  WMTS_EUROGEOGRAPHICS_SOURCE = 'https://www.mapsforeurope.org/maps/wmts'
  TS_EUROGEOGRAPHICS_EUROREGIONALMAP = {'alias': 'EUROGEOGRAPHICS_EUROREGIONALMAP', 'source': WMTS_EUROGEOGRAPHICS_SOURCE + '{wmts}&token={key}', 'layer': 'erm', 'matrixset': 'euro_3857', 'style': 'default', 'format': 'image/png'}
  TS_HEREBASE_SOURCE = 'https://1.base.maps.ls.hereapi.com/maptile/2.1/maptile/newest'
  TS_HERE_NORMAL = {'alias': 'HERE_NORMAL', 'source': TS_HEREBASE_SOURCE + '/normal.day/{matrix}/{col}/{row}/256/png8?pois&apiKey={key}', 'layer':'pedestrian', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256, 'format': 'image/png'}
  TS_HERE_PEDESTRIAN = {'alias': 'HERE_PEDESTRIAN', 'source': TS_HEREBASE_SOURCE + '/pedestrian.day/{matrix}/{col}/{row}/256/png8?pois&apiKey={key}', 'layer':'pedestrian', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256, 'format': 'image/png'}
  TS_HEREAERIAL_SOURCE = 'https://1.aerial.maps.ls.hereapi.com/maptile/2.1/maptile/newest'
  TS_HERE_TERRAIN = {'alias': 'HERE_TERRAIN', 'source': TS_HEREAERIAL_SOURCE + '/terrain.day/{matrix}/{col}/{row}/256/png8?pois&apiKey={key}', 'layer':'pedestrian', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256, 'format': 'image/png'}
  TS_HERE_SATELLITE = {'alias': 'HERE_SATELLITE', 'source': TS_HEREAERIAL_SOURCE + '/satellite.day/{matrix}/{col}/{row}/256/png8?apiKey={key}', 'layer':'pedestrian', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256, 'format': 'image/png'}
  TS_HERE_HYBRID = {'alias': 'HERE_HYBRID', 'source': TS_HEREAERIAL_SOURCE + '/hybrid.day/{matrix}/{col}/{row}/256/png8?pois&apiKey={key}', 'layer':'pedestrian', 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256, 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0],'width': 256, 'height': 256, 'format': 'image/png'}

  def LinkLegend(self, legend):
    self.Legend = legend

  def LinkJSONTiles(self, jsontiles):
    self.JSONTiles = jsontiles

  @staticmethod
  def WGS84toCoord(lat, lon):
    try:
      x, y = WebMercatorMap.WGS84toWebMercator(lat, lon)
    except:
      return None
    return (x, y)

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
          if not kernel32.ReadFile(p, ctypes.cast(b, PVOID), DWORD(len(b)), ctypes.byref(nr), LPVOID(0)):
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
    tr = threading.Thread(target=pipe_read, args=(pipe_r,), daemon=False)
    tr.start()
    tw1 = threading.Thread(target=pipe_write, args=(pipe_w1, i1), daemon=False)
    tw1.start()
    if i2:
      tw2 = threading.Thread(target=pipe_write, args=(pipe_w2, i2), daemon=False)
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
        if tiles[c][r] is not None:
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
    t = [threading.Thread(target=merge_col, args = (c,)) for c in range(len(tiles))]
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

  @classmethod
  def TCAlias(cls, name):
    if hasattr(cls, 'TC_' + name):
      return list(getattr(cls, 'TC_' + name))
    else:
      return None

  def SetTilesProviders(self, providers):
    try:
      provs = []
      for rid, prov in providers.items():
        if prov[0].get('format') == 'application/json':
          if not hasattr(self, 'JSONTiles') or not self.JSONTiles.Load(prov[0], rid[0], **prov[1]):
            continue
          provs.extend(((rid[0] + self.JSONTiles.TilesSetIdMult * (sid + 1), str(min(max(mat, inf.get('minmat', mat)), inf.get('maxmat', mat)))), (inf, hand)) for sid, (inf, hand) in enumerate(self.JSONTiles.InfosHandling(rid[0])) for mat in (int(rid[1]) + round(math.log2(256 / inf['width'])),))
        else:
          provs.append((rid, prov))
      tile_generator_builders = {rid: partial(self.TileGenerator, prov[0], rid[1], **prov[1]) for rid, prov in provs}
      if self.TilesInfos:
        infos = {**self.TilesInfos}
      else:
        infos = None
      self.TilesInfos = {rid: {**prov[0], 'matrix': rid[1]} for rid, prov in provs}
      if isinstance(self.Tiles, TilesMixCache):
        if not self.Tiles.Configure(tile_generator_builders):
          self.TilesInfos = infos
          return False
      else:
        self.Tiles = TilesMixCache(wrap=self.Tiles)
        if not self.Tiles.Configure(tile_generator_builders):
          self.Tiles.Close()
          self.Tiles = self.Tiles.Wrap
          self.TilesInfos = infos
          return False
      self.TilesInfos = {rid: (self.Tiles.Infos[rid] if prov[0].get('format') != 'application/json' else {**prov[0], 'matrix': rid[1], 'scale': prov[0]['basescale'] / (2 ** int(rid[1])) / self.CRS_MPU}) for rid, prov in providers.items()}
    except:
      return False
    return True

  def Close(self):
    try:
      if self.Tiles is not None:
        self.Tiles.Close()
    except:
      pass


class WGS84Map(BaseMap):

  CRS = 'EPSG:4326'
  CRS_MPU = math.pi / 180 * WGS84WebMercator.R
  WMS_BBOX = '{miny},{minx},{maxy},{maxx}'

  @staticmethod
  def WGS84toCoord(lat, lon):
    return (lon, lat)


class TIFFHandlerMeta(type):

  def __del__(cls):
    cls.__end__()

class TIFFHandler(metaclass=TIFFHandlerMeta):

  HEADER = {b'\x49\x49\x2a\x00': '<', b'\x4d\x4d\x00\x2a': '>'}
  TAGS_SHORT = {258: 'bits_per_sample', 259: 'compression' , 277: 'samples_per_pixel', 284: 'planar_configuration', 317: 'predictor', 339: 'sample_format'}
  TAGS_SHORT_LONG = {256: 'image_width', 257: 'image_length', 273: 'strip_offsets', 278: 'rows_per_strip', 279: 'strip_byte_counts', 322: 'tile_width', 323: 'tile_length', 325: 'tile_byte_counts'}
  TAGS_LONG = {324: 'tile_offsets'}

  kernel32 = None

  @classmethod
  def __end__(cls):
    if cls.kernel32 is not None:
      try:
        cls.gdiplus.GdiplusShutdown(cls.gdiplus_token)
      except:
        pass

  def __new__(cls, image, load=True):
    self = object.__new__(cls)
    self.image = image
    if load:
      if cls.load(self):
        return self
      else:
        return None
    else:
      return self

  def load(self):
    image = self.image
    try:
      ba = TIFFHandler.HEADER.get(image[:4], None)
      if ba is None:
        raise
      self.byte_order = ba
      L = ba + 'L'
      H = ba + 'H'
      id0 = struct.unpack(L, image[4:8])[0]
      ne = struct.unpack(H, image[id0:id0+2])[0]
      p = id0 + 2
      for e in range(ne):
        ei = struct.unpack(H, image[p:p+2])[0]
        t = {3: H, 4: L}.get(struct.unpack(H, image[p+2:p+4])[0], None)
        if ei in TIFFHandler.TAGS_SHORT:
          if t != H:
            raise
          tag = TIFFHandler.TAGS_SHORT[ei]
        elif ei in TIFFHandler.TAGS_SHORT_LONG:
          if t is None:
            raise
          tag = TIFFHandler.TAGS_SHORT_LONG[ei]
        elif ei in TIFFHandler.TAGS_LONG:
          if t != L:
            raise
          tag = TIFFHandler.TAGS_LONG[ei]
        else:
          tag = None
        if ei in (258, 339, 273, 279, 324, 325):
          n = struct.unpack(L, image[p+4:p+8])[0]
          if n == 1:
            if ei in (258, 339):
              setattr(self, tag, struct.unpack(t, image[p+8:p+(10 if t == H else 12)])[0])
            else:
              setattr(self, tag, struct.unpack(t, image[p+8:p+(10 if t == H else 12)]))
          else:
            if ei in (258, 339) and n != 3:
              raise
            o = struct.unpack(L, image[p+8:p+12])[0]
            setattr(self, tag, struct.unpack('%s%d%s' % (ba, n, t[-1]), image[o:o+(2 if t == H else 4)*n]))
        elif tag is not None:
          setattr(self, tag, struct.unpack(t, image[p+8:p+(10 if t == H else 12)])[0])
        p += 12
      if hasattr(self, 'tile_offsets'):
        self.offsets = self.tile_offsets
        self.byte_counts = self.tile_byte_counts
      elif hasattr(self, 'strip_offsets'):
        self.offsets = self.strip_offsets
        self.byte_counts = self.strip_byte_counts
      else:
        raise
    except:
      return False
    return True

  def _none_decompress(self, index):
    o = self.offsets[index]
    a = o + self.byte_counts[index]
    return memoryview(self.image)[o:a]

  def _lzw_decompress(self, index):
    image = self.image
    try:
      b = self.offsets[index]
      a = b + self.byte_counts[index]
      d = BytesIO()
      t = [i.to_bytes() for i in range(256)]
      t.extend([b'', b''])
      p = 0
      l = 9
      while True:
        m = 1 << l
        e = min(a, b + (m * l) // 16 + 1)
        bi = format(int.from_bytes(image[b:e], 'big'), '0' + str(8 * (e - b)) + 'b')
        for i in range(m - len(t)):
          c = int(bi[p:(p:=p+l)], 2)
          if c == 257:
            return d.getbuffer()
          if c == 256:
            l = 8
            t[257:] = [b'']
            break
          g = t[c][:1]
          t.append(t.pop() + g)
          d.write(t[c])
          t.append(t[c])
        b += p // 8
        p %= 8
        l += 1
    except:
      return None

  def _adeflate_decompress(self, index):
    o = self.offsets[index]
    a = o + self.byte_counts[index]
    try:
      return memoryview(zlib.decompress(memoryview(self.image)[o:a]))
    except:
      return None

  def _predictor_revert(self, source, byte_order=None):
    try:
      if self.predictor != 2 or self.bits_per_sample not in (8, 16, 32):
        return None
      w = self.tile_width if hasattr(self, 'tile_width') else self.image_width
      h = len(source) * 8 // self.bits_per_sample // w
      st = {8: 'B', 16: 'H', 32: 'L'}[self.bits_per_sample]
      if sys.byteorder == ('little' if self.byte_order == '<' else 'big'):
        pix = iter(source.cast(st))
      else:
        a = array.array(st)
        a.frombytes(source)
        a.byteswap()
        pix = iter(a)
      c = (1 << self.bits_per_sample) - 1
      reverted = (([p := 0] and [(p := (p + next(pix)) & c) for col in range(w)]) for row in range(h))
      spack = struct.Struct((byte_order or self.byte_order) + str(w) + st).pack
      return memoryview(b''.join(spack(*r) for r in reverted)).cast(st)
    except:
      return None

  def _none_revert(self, source, byte_order=None):
    st = {8: 'B', 16: 'H', 32: 'L'}[self.bits_per_sample]
    if byte_order in (None, self.byte_order):
      return source.cast(st)
    else:
      try:
        a = array.array(st)
        a.frombytes(source)
        a.byteswap()
        return memoryview(a)
      except:
        return None

  def decode(self, byte_order=None):
    try:
      if getattr(self, 'compression', 1) == 1:
        _decompress = self._none_decompress
      elif self.compression == 5:
        _decompress = self._lzw_decompress
      elif self.compression in (8, 32946):
        _decompress = self._adeflate_decompress
      else:
        raise
      if getattr(self, 'predictor', 1) == 1:
        _revert = partial(self._none_revert, byte_order=byte_order)
      elif self.predictor == 2:
        _revert = partial(self._predictor_revert, byte_order=byte_order)
      else:
        raise
      if self.samples_per_pixel != 1:
        raise
      image = memoryview(bytearray(self.image_width * self.image_length * self.bits_per_sample // 8)).cast({8: 'B', 16: 'H', 32: 'L'}[self.bits_per_sample])
      iwidth = self.image_width
      ilength = self.image_length
      if hasattr(self, 'tile_offsets'):
        twidth = self.tile_width
        tlength = self.tile_length
        tacross = (iwidth - 1) // twidth + 1
        tdown = (ilength - 1) // tlength + 1
        tllength = (ilength - 1) % tlength + 1
        tlwidth = (iwidth - 1) % twidth + 1
        _s = iwidth * tlength
        tiles = (_revert(_decompress(t)) for t in range(tacross * tdown))
        _tpos = list(slice(trow * twidth, trow * twidth + twidth) for trow in range(tlength))
        _tlpos = list(slice(trow * twidth, trow * twidth + tlwidth) for trow in range(tlength))
        for row in range(tdown):
          p0 = row * _s
          _trows = tlength if row < tdown - 1 else tllength
          _tps = _tpos[:_trows]
          _tw = twidth
          for col in range(tacross):
            tile = next(tiles)
            p = p0 + col * twidth
            if col == tacross - 1:
              _tps = _tlpos[:_trows]
              _tw = tlwidth
            for _tp in _tps:
              image[p: p + _tw] = tile[_tp]
              p += iwidth
      elif hasattr(self, 'strip_offsets'):
        sdown = (ilength - 1) // self.rows_per_strip + 1
        _s = iwidth * self.rows_per_strip
        _sl = iwidth * ((ilength - 1) % self.rows_per_strip + 1)
        p = 0
        for row in range(sdown):
          strip = _revert(_decompress(row))
          image[p: (p := p + (_s if row < sdown - 1 else _sl))] = strip
      else:
        raise
    except:
      return False
    self.decoded = image.obj
    return True

  def convert(self):
    cls = self.__class__
    if cls.kernel32 is None:
      cls.kernel32 = ctypes.WinDLL('kernel32',  use_last_error=True)
      cls.GlobalAlloc = cls.kernel32.GlobalAlloc
      cls.GlobalAlloc.argtypes = ctypes.wintypes.UINT, ctypes.c_ssize_t
      cls.GlobalAlloc.restype = ctypes.wintypes.HANDLE
      cls.GlobalLock = cls.kernel32.GlobalLock
      cls.GlobalLock.argtypes = ctypes.wintypes.HGLOBAL,
      cls.GlobalLock.restype = ctypes.wintypes.LPVOID
      cls.GlobalUnlock = cls.kernel32.GlobalUnlock
      cls.GlobalUnlock.argtypes = ctypes.wintypes.HGLOBAL,
      cls.GlobalUnlock.restype = ctypes.wintypes.LPVOID
      cls.GlobalSize = cls.kernel32.GlobalSize
      cls.GlobalSize.argtypes = ctypes.wintypes.HGLOBAL,
      cls.GlobalSize.restype = ctypes.c_ssize_t
      cls.ole32 = ctypes.WinDLL('ole32',  use_last_error=True)
      cls.Release = ctypes.WINFUNCTYPE(ctypes.c_ulong)(2, 'Release')
      cls.CreateStreamOnHGlobal = cls.ole32.CreateStreamOnHGlobal
      cls.CreateStreamOnHGlobal.argtypes = ctypes.wintypes.HGLOBAL, ctypes.c_bool, ctypes.c_void_p
      cls.gdiplus = ctypes.WinDLL('gdiplus',  use_last_error=True)
      cls.gdiplus_token = ctypes.wintypes.ULONG()
      cls.gdiplus.GdiplusStartup(ctypes.byref(cls.gdiplus_token), ctypes.c_char_p(ctypes.string_at(ctypes.addressof(ctypes.c_uint(1)),ctypes.sizeof(ctypes.c_uint)) + b'\x00' * 24), None)
      cls.png_clsid = struct.pack('@LHH8B', *struct.unpack('>LHH8B', int('557CF406-1A04-11D3-9A73-0000F81EF32E'.replace('-', ''), 16).to_bytes(16, 'big')))
    try:
      h = cls.GlobalAlloc(0x42, len(self.image))
      hl = cls.GlobalLock(h)
      ctypes.memmove(hl, self.image, len(self.image))
      cls.GlobalUnlock(h)
      ist = ctypes.c_void_p()
      cls.CreateStreamOnHGlobal(h, True, ctypes.byref(ist))
      i = ctypes.c_void_p()
      if cls.gdiplus.GdipLoadImageFromStream(ist, ctypes.byref(i)):
        i = None
        raise
      h_ = cls.GlobalAlloc(0x42, 0)
      ist_ = ctypes.c_void_p()
      cls.CreateStreamOnHGlobal(h_, True, ctypes.byref(ist_))
      if cls.gdiplus.GdipSaveImageToStream(i, ist_, ctypes.c_char_p(cls.png_clsid), None):
        raise
      hl_ = cls.GlobalLock(h_)
      self.converted = ctypes.string_at(hl_, cls.GlobalSize(h_))
      cls.GlobalUnlock(h_)
    except:
      return False
    finally:
      cls.Release(ist)
      if i is not None:
        cls.gdiplus.GdipDisposeImage(i)
        cls.Release(ist_)
    return True


class JSONTiles():

  LOCALSTORE_DEFAULT_PATTERN = r'{alias|layer}\{resource}'

  def __init__(self, tset_id_mult):
    self.TilesSetIdMult = tset_id_mult
    self.StylesCache = {}
    self.GlyphsCache = {}
    self.SpritesJSONCache = {}
    self.SpritesPNGCache = {}
    self.TilesInfosHandlingCache = {}
    self.log = partial(log, 'jsontiles')

  @staticmethod
  def normurl(url):
    while '/..' in url:
      u1, u2 = url.split('/..')
      url = urllib.parse.urljoin(u1 + '/', '..' + u2)
    while '/.' in url:
      u1, u2 = url.split('/.')
      url = urllib.parse.urljoin(u1 + '/', '.' + u2)
    return url

  @staticmethod
  def _get_resource(rpath, rjson, local_expiration, local_store):
    updt = False
    exp = False
    loc_res = None
    res = None
    if not rpath:
      return exp, updt, loc_res, res
    try:
      if os.path.exists(rpath):
        if rjson:
          f = open(rpath, 'rt', encoding='utf-8')
          loc_res = json.load(f)
        else:
          f = open(rpath, 'rb')
          loc_res = f.read()
        if local_expiration is not None:
          lmod = os.path.getmtime(rpath)
          if local_expiration > max(time.time() - lmod, 0) / 86400:
            res = loc_res
          else:
            exp = True
        else:
          res = loc_res
      elif local_store:
        updt = True
    except:
      pass
    finally:
      try:
        f.close()
      except:
        pass
    return exp, updt, loc_res, res

  @staticmethod
  def _put_resource(rpath, rjson, exp, updt, loc_res, res):
    if exp:
      if loc_res == res:
        try:
          os.utime(rpath, (time.time(),) * 2)
        except:
          pass
      else:
        updt = True
    if updt:
      try:
        if rjson:
          f = open(rpath, 'wt', encoding='utf-8')
          json.dump(res, f)
        else:
          f = open(rpath, 'wb')
          f.write(res)
      except:
        pass
      finally:
        try:
          f.close()
        except:
          pass

  def Load(self, infos, tid, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, only_local=False):
    if 'source' not in infos or infos.get('format') != 'application/json':
      return False
    self.log(2, 'styleload', infos)
    if tid in self.StylesCache:
      self.log(2, 'stylecloaded', infos)
      return True
    infos['width'] = infos['height'] = 256
    infos['basescale'] = WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / 256
    infos['topx'] = WGS84WebMercator.WGS84toWebMercator(0, -180)[0]
    infos['topy'] = WGS84WebMercator.WGS84toWebMercator(0, 180)[0]
    loc = False
    updt = False
    pattern = local_pattern
    if pattern is not None:
      try:
        if '{' not in pattern:
          pattern = os.path.join(pattern, self.LOCALSTORE_DEFAULT_PATTERN)
        else:
          while '{matrix}' in pattern:
            pattern = os.path.dirname(pattern)
          pattern = os.path.join(pattern, '{resource}')
        a_l = infos.get('alias') or infos.get('layer', '')
        pattern = pattern.format_map({**infos,  'alias|layer': a_l, 'resource': '{resource}'})
        infopath = pattern.replace('{resource}',  a_l + ' - infos.json')
        if os.path.exists(infopath):
          f = open(infopath, 'rt', encoding='utf-8')
          inf = json.load(f)
          if False in (k not in infos or infos.get(k) == inf.get(k) for k in ('source', 'layer', 'format', 'slash_url')):
            raise
          if 'alias' in infos and 'alias' in inf:
            if infos['alias'] != inf['alias']:
              raise
          if local_store:
            for k in ('alias', 'width', 'height', 'basescale', 'topx', 'topy', 'overwrite_schemes', 'overwrite_names'):
              if k in infos and infos[k] != inf[k]:
                inf[k] = infos[k]
                updt = True
          loc = True
        elif local_store:
          Path(os.path.dirname(infopath)).mkdir(parents=True, exist_ok=True)
          loc = True
          inf = infos
          updt = True
      except:
        pass
      finally:
        try:
          f.close()
        except:
          pass
      try:
        if updt:
          f = open(infopath, 'wt', encoding='utf-8')
          json.dump(inf, f)
      except:
        pass
      finally:
        try:
          f.close()
        except:
          pass
    style = None
    if loc:
      try:
        stylepath = pattern.replace('{resource}', a_l + ' - style.json')
      except:
        stylepath = ''
      exp, updt, loc_style, style = JSONTiles._get_resource(stylepath, True, local_expiration, local_store)
      if loc_style is not None:
        self.log(2, 'stylelfound', infos)
        if style is None:
          self.log(2, 'stylelexpired', infos)
    if style is None:
      if only_local:
        self.log(1, 'stylefail', infos)
        return False
      headers = {'User-Agent': user_agent}
      if referer:
        headers['Referer'] = referer
      if '://' in infos['source']:
        self.log(2, 'stylefetch', infos)
        try:
          uri = infos['source'].format_map({'key': key or ''})
        except:
          self.log(1, 'stylefail', infos)
          return False
        rep = HTTPRequest(uri, 'GET', headers, basic_auth=basic_auth)
        if rep.code != '200':
          self.log(1, 'stylefail', infos)
          return False
        try:
          style = json.loads(rep.body)
        except:
          self.log(1, 'stylefail', infos)
          return False
      else:
        self.log(2, 'stylefetch', infos)
        try:
          f = open(infos['source'], 'rt', encoding='utf-8')
          style = json.load(f)
        except:
          self.log(1, 'stylefail', infos)
          return False
        finally:
          try:
            f.close()
          except:
            pass
    glyphs = style.get('glyphs', '')
    sprite = style.get('sprite', '')
    self.TilesInfosHandlingCache[tid] = []
    sources = {}
    try:
      schemes = map(str.strip, infos.get('overwrite_schemes', '').split(','))
      names = map(str.strip, infos.get('overwrite_names', '').split(','))
      for name, desc in style['sources'].items():
        if desc['type'] not in ('vector', 'raster', 'raster-dem'):
          continue
        if 'url' in desc:
          uri_b = JSONTiles.normurl(urllib.parse.urljoin(infos['source'], desc['url']))
          uri = uri_b.format_map({'key': key or ''})
          rep = HTTPRequest(uri, 'GET', headers, basic_auth=basic_auth)
          if rep.code != '200':
            raise
          src = json.loads(rep.body)
          tiles = JSONTiles.normurl(urllib.parse.urljoin(((uri_b.rstrip('/') + '/') if infos.get('slash_url') else uri_b), src['tiles'][0]))
          scheme = src.get('scheme', desc.get('scheme'))
          minzoom = src.get('minzoom', None)
          maxzoom = src.get('maxzoom', None)
        else:
          tiles = JSONTiles.normurl(urllib.parse.urljoin(infos['source'], desc['tiles'][0]))
          scheme = desc.get('scheme')
          minzoom = desc.get('minzoom', None)
          maxzoom = desc.get('maxzoom', None)
        self.TilesInfosHandlingCache[tid].append(({'source': tiles.replace('{z}', '{matrix}').replace('{x}', '{col}').replace('{y}', ('{invrow}' if (next(schemes, '') or scheme) == 'tms' else '{row}')), 'layer': next(names, '') or name, 'basescale': WGS84WebMercator.WGS84toWebMercator(0, 360)[0] / desc.get('tileSize', 512), 'topx': WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'topy': -WGS84WebMercator.WGS84toWebMercator(0,-180)[0], 'width': desc.get('tileSize', 512), 'height': desc.get('tileSize', 512), **({'minmat': minzoom} if minzoom is not None else {}), **({'maxmat': maxzoom} if maxzoom is not None else {})}, {'local_pattern': local_pattern, 'local_expiration': local_expiration, 'local_store': local_store, 'key': key, 'referer': referer, 'user_agent': user_agent, 'basic_auth': basic_auth}))
        sources[name] = {'type': desc['type'], 'tiles': [tiles]}
        if 'tileSize' in desc:
          sources[name]['tileSize'] = desc['tileSize']
        if minzoom is not None:
          sources[name]['minzoom'] = minzoom
        if maxzoom is not None:
          sources[name]['maxzoom'] = maxzoom
      style['sources'] = sources
    except:
      self.log(1, 'stylefail', infos)
      return False
    if loc and local_store:
      JSONTiles._put_resource(stylepath, True, exp, updt, loc_style, style)
    try:
      if 'glyphs' in style:
        style['glyphs'] = '{netloc}/jsontiles/glyphs/%s/{fontstack}/{range}.pbf' % tid
      if 'sprite' in style:
        style['sprite'] = '{netloc}/jsontiles/sprite/%s/sprite' % tid
      sid = 0
      for name, desc in style['sources'].items():
        sid += 1
        desc['tiles'] = ['{netloc}/tiles/tile-{y}-{x}%s?%d,{z}' % (os.path.splitext(tiles)[1][0:4], tid + self.TilesSetIdMult * sid)]
      self.StylesCache[tid] = (json.dumps(style).encode('utf-8'), JSONTiles.normurl(urllib.parse.urljoin(infos['source'], glyphs)), JSONTiles.normurl(urllib.parse.urljoin(infos['source'], sprite)), {'pattern': (pattern if loc else None), 'alias_layer': (a_l if loc else None), 'local_expiration': local_expiration, 'local_store': local_store, 'key': key, 'referer': referer, 'user_agent': user_agent, 'basic_auth': basic_auth, 'only_local': only_local})
    except:
      self.log(1, 'stylefail', infos)
      return False
    self.log(2, 'styleloaded', infos)
    return True

  def Unload(self):
    self.GlyphsCache.clear()
    self.SpritesPNGCache.clear()

  def Style(self, tid):
    return self.StylesCache.get(tid, (None,))[0]

  def InfosHandling(self, tid):
    return self.TilesInfosHandlingCache.get(tid)

  def Glyph(self, tid, fontstack, fontrange):
    self.log(2, 'glyphretrieve', tid, fontstack, fontrange)
    g = self.GlyphsCache.get((tid, fontstack, fontrange))
    if g is not None:
      self.log(2, 'glyphcretrieved', tid, fontstack, fontrange)
      return g
    uri, handling = self.StylesCache.get(tid, (None,) * 4)[1:4:2]
    if uri is None:
      self.log(1, 'glyphfail', tid, fontstack, fontrange)
      return None
    glyph = None
    if handling['pattern'] is not None:
      try:
        glyphpath = handling['pattern'].replace('{resource}', '%s - %s.pbf' % (fontstack, fontrange))
      except:
        glyphpath = ''
      exp, updt, loc_glyph, glyph = JSONTiles._get_resource(glyphpath, False, handling['local_expiration'], handling['local_store'])
      if loc_glyph is not None:
        self.log(2, 'glyphlfound', tid, fontstack, fontrange)
        if glyph is None:
          self.log(2, 'glyphlexpired', tid, fontstack, fontrange)
    if glyph is None:
      if handling['only_local']:
        self.log(1, 'glyphfail', tid, fontstack, fontrange)
        return None
      self.log(2, 'glyphfetch', tid, fontstack, fontrange)
      headers = {'User-Agent': handling['user_agent']}
      if handling['referer']:
        headers['Referer'] = handling['referer']
      try:
        uri = uri.format_map({'key': handling['key'] or '', 'fontstack': fontstack, 'range': fontrange})
      except:
        self.log(1, 'glyphfail', tid, fontstack, fontrange)
        return None
      rep = HTTPRequest(uri, 'GET', headers, basic_auth=handling['basic_auth'])
      if rep.code != '200':
        self.log(1, 'glyphfail', tid, fontstack, fontrange)
        return None
      glyph = rep.body
    if handling['pattern'] is not None and handling['local_store']:
      JSONTiles._put_resource(glyphpath, False, exp, updt, loc_glyph, glyph)
    self.GlyphsCache[(tid, fontstack, fontrange)] = glyph
    self.log(1, 'glyphretrieved', tid, fontstack, fontrange)
    return glyph

  def _sprite(self, tid, target, scale):
    target= target.lower()
    self.log(2, 'sprite%sretrieve' % target, tid, scale)
    s = getattr(self, 'Sprites%sCache' % target.upper()).get((tid, scale))
    if s is not None:
      self.log(2, 'sprite%scretrieved' % target, tid, scale)
      return s
    uri, handling = self.StylesCache.get(tid, (None,) * 4)[2:4]
    if uri is None:
      self.log(1, 'sprite%sfail' % target, tid, scale)
      return None
    sprite = None
    if handling['pattern'] is not None:
      try:
        spritepath = handling['pattern'].replace('{resource}',  handling['alias_layer'] + ' - sprite%s.%s' % (scale, target.lower()))
      except:
        spritepath = ''
      exp, updt, loc_sprite, sprite = JSONTiles._get_resource(spritepath, False, handling['local_expiration'], handling['local_store'])
      if loc_sprite is not None:
        self.log(2, 'sprite%slfound' % target, tid, scale)
        if sprite is None:
          self.log(2, 'sprite%slexpired' % target, tid, scale)
    if sprite is None:
      if handling['only_local']:
        self.log(1, 'sprite%sfail' % target, tid, scale)
        return None
      self.log(2, 'sprite%sfetch' % target, tid, scale)
      headers = {'User-Agent': handling['user_agent']}
      if handling['referer']:
        headers['Referer'] = handling['referer']
      try:
        uri = uri.format_map({'key': handling['key'] or ''}) + scale + '.' + target
      except:
        self.log(1, 'sprite%sfail' % target, tid, scale)
        return None
      rep = HTTPRequest(uri, 'GET', headers, basic_auth=handling['basic_auth'])
      if rep.code != '200':
        self.log(1, 'sprite%sfail' % target, tid, scale)
        return None
      sprite = rep.body
    if handling['pattern'] is not None and handling['local_store']:
      JSONTiles._put_resource(spritepath, False, exp, updt, loc_sprite, sprite)
    getattr(self, 'Sprites%sCache' % target.upper())[(tid, scale)] = sprite
    self.log(2, 'sprite%sretrieved' % target, tid, scale)
    return sprite

  def SpriteJSON(self, tid, scale=''):
    return self._sprite(tid, 'json', scale)

  def SpritePNG(self, tid, scale=''):
    return self._sprite(tid, 'png', scale)


class ElevationTilesCache(TilesCache):

  class _dict(dict):
    def init(self, weights):
      self.Length = 0
      self.Weights = weights
      self.LengthFlag = False
    def pop(self, key, *default):
      if key in self and not self.LengthFlag:
        self.Length -= self.Weights[key[0]]
      self.LengthFlag = True
      if default:
        r = super().pop(key, *default)
      else:
        r = super().pop(key)
      self.LengthFlag = False
      return r
    def clear(self):
      super().clear()
      self.Length = 0
    def __delitem__(self, key):
      if key in self and not self.LengthFlag:
        self.Length -= self.Weights[key[0]]
      self.LengthFlag = True
      r = super().__delitem__(key)
      self.LengthFlag = False
      return r
    def __setitem__(self, key, value):
      if key not in self and not self.LengthFlag:
        self.Length += self.Weights[key[0]]
      self.LengthFlag = True
      r = super().__setitem__(key, value)
      self.LengthFlag = False
      return r
    def __len__(self):
      return round(self.Length)

  def __init__(self, size=None, threads=None):
    if size is not None:
      super().__init__(size, threads, False)
      self.Weights = {}
      self.Length = 0
      self.Buffer = ElevationTilesCache._dict()
      self.Buffer.init(self.Weights)

  @staticmethod
  def LazyConfigure(obj):
    with obj.LazyTiles.BLock:
      try:
        obj.Tiles = obj.LazyTiles
        if not obj.SetTilesProvider(obj.LazyTiles.Id, *obj.LazyTilesArgs, lazy=False):
          raise
        obj.LazyTiles.Weights[obj.LazyTiles.Id] = obj.TilesInfos['width'] * obj.TilesInfos['height'] / 65536 / (1 if obj.TilesInfos['format'] == 'image/x-bil;bits=32' else 2)
      except:
        obj.Tiles = None
        return False
    return True

  def __get__(self, obj, objtype=None):
    with obj.LazyTiles.BLock:
      if 'Tiles' not in vars(obj):
        if not self.LazyConfigure(obj):
          return None
    return obj.Tiles


class WGS84Elevation(WGS84Map):

  AS_IGN_ALTI = {'alias': 'IGN_ALTI', 'source': 'https://wxs.ign.fr/{key}/alti/rest/elevation.json?lat={lat}&lon={lon}&zonly=true', 'separator': '|', 'key': ('elevations', ), 'nodata': -99999, 'limit': 200, 'parallel': True}
  TS_IGN_RGEALTI = {'alias': 'IGN_RGEALTI', 'source': WebMercatorMap.WMTS_IGN_SOURCE + '{wmts}', 'layer': 'ELEVATION.ELEVATIONGRIDCOVERAGE.HIGHRES', 'matrixset': 'WGS84G', 'style': 'normal', 'format': 'image/x-bil;bits=32', 'nodata': -99999}
  MS_IGN_RGEALTI = {'alias': 'IGN_RGEALTI', 'source': WebMercatorMap.WMS_IGN_SOURCE + '{wms}', 'layers':'ELEVATION.ELEVATIONGRIDCOVERAGE.HIGHRES', 'format': 'image/x-bil;bits=32', 'styles': '', 'nodata': -99999}
  AS_OPENROUTE_SRTM = {'alias': 'OPENROUTE_SRTM', 'source': 'https://api.openrouteservice.org/elevation/point?api_key={key}&geometry={lon},{lat}&format_out=geojson&dataset=srtm', 'separator': ',', 'key': ('geometry', 'coordinates', 2), 'nodata': 32768, 'limit': 1, 'parallel': True}
  TS_SRTM_GL1 = {'alias': 'SRTM_GL1', 'source': 'http://step.esa.int/auxdata/dem/SRTMGL1/{hgt}.SRTMGL1.hgt.zip', 'layer': 'SRTM.GL1', 'basescale': WGS84Map.CRS_MPU / 3600, 'topx': -180, 'topy': 90,'width': 3600, 'height': 3600, 'format': 'image/hgt', 'nodata': -32768}
  AS_OTD_EUDEM = {'alias': 'AS_OTD_EUDEM', 'source': 'https://api.opentopodata.org/v1/eudem25m?locations={location}', 'separator': '|', 'key': ('results', '*', 'elevation'), 'nodata': -32767, 'limit': 100, 'parallel': False}
  TS_EUDEM_1 = {'alias': 'EUDEM_1', 'source': 'http://www.muaythaiclinch.info/opendem_europe_download/eu_4326/arc1/{hgt}.zip', 'layer':'EU-DEM.1', 'basescale': WGS84Map.CRS_MPU / 3600, 'topx': -180, 'topy': 90,'width': 3600, 'height': 3600, 'format': 'image/hgt', 'nodata': -32768}
  TS_ASTER_V3 = {'alias': 'ASTER_V3', 'source': 'https://e4ftl01.cr.usgs.gov/ASTT/ASTGTM.003/2000.03.01/ASTGTMV003_{hgt}.zip', 'layer': 'ASTER.V3', 'basescale': WGS84Map.CRS_MPU / 3600, 'topx': -180, 'topy': 90,'width': 3600, 'height': 3600, 'format': 'image/tiff', 'nodata': -9999}

  Tiles = ElevationTilesCache()

  def __init__(self, tiles_buffer_size=None, tiles_max_threads=None):
    super().__init__(None, None)
    self.Closed = False
    if not tiles_buffer_size or not tiles_max_threads:
      self.LazyTiles = None
    else:
      del self.Tiles
      self.LazyTilesArgs = None
      self.LazyTiles = ElevationTilesCache(tiles_buffer_size, tiles_max_threads)

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
    elif infos['format'] in ('image/hgt', 'image/tiff', 'image/geotiff'):
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

  def RetrieveTile(self, infos, local_pattern, local_expiration, local_store, key, referer, user_agent, basic_auth, only_local, pconnection=None, action=None, only_save=False):
    tile = super().RetrieveTile(infos, local_pattern, local_expiration, local_store, key, referer, user_agent, basic_auth, only_local, pconnection, action, only_save)
    if tile is not None and not isinstance(tile, bool) and infos.get('format') in ('image/tiff', 'image/geotiff'):
      try:
        th = TIFFHandler(tile)
        if th.bits_per_sample != 16 or th.sample_format != 2:
          raise
        th.decode(byte_order='>')
      except:
        tile = None
      tile = bytes(th.decoded)
    return tile

  def ElevationGenerator(self, infos_base=None, matrix=None, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, only_local=False):
    tgen = self.TileGenerator(infos_base, matrix, local_pattern=local_pattern, local_expiration=local_expiration, local_store=local_store, key=key, referer=referer, user_agent=user_agent, basic_auth=basic_auth, only_local=only_local)
    if not tgen:
      return None
    buf_tiles = {}
    def retrieve_elevations(lat=None, lon=None, close_connection=False):
      nonlocal buf_tiles
      if close_connection:
        tgen(close_connection=True)
      if lat is None or lon is None:
        return None
      try:
        row, col = tgen(lat, lon, just_box=True)[0]
        infos_tile = buf_tiles.get((row, col))
        if infos_tile is not None:
          return self.ElevationfromTile(*infos_tile, lat, lon)
        infos_tile = tgen(None, None, row, col).values()
        if all(infos_tile):
          buf_tiles[(row, col)] = infos_tile
          return self.ElevationfromTile(*infos_tile, lat, lon)
        else:
          return None
      except:
        return None
    return retrieve_elevations

  def WGS84toElevation(self, points, infos=None, matrix=None, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, only_local=False):
    if not infos:
      if not self.MapInfos or not self.Map:
        return None
      else:
        try:
          return [self.ElevationfromMap(lat, lon) for (lat, lon) in points]
        except:
          return None
    else:
      if self.Tiles is not None:
        try:
          prow = pcol = tile = None
          return [self.ElevationfromTile({**self.Tiles.Infos, 'row': row, 'col': col}, (tile if (prow, pcol) == ((prow := row), (pcol := col)) else (tile := self.Tiles[self.Tiles.Id, (row, col)](20))), lat, lon) for (lat, lon) in points for (row, col) in (self.WGS84toTile(self.Tiles.Infos, lat, lon), )]
        except:
          return None
      else:
        try:
          egen = self.ElevationGenerator(infos, matrix, local_pattern=local_pattern, local_expiration=local_expiration, local_store=local_store, key=key, referer=referer, user_agent=user_agent, basic_auth=basic_auth, only_local=only_local)
          if egen:
            return [egen(lat, lon) for (lat, lon) in points]
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
    if infos['format'] != 'image/x-bil;bits=32' and infos['format'] not in ('image/hgt', 'image/tiff', 'image/geotiff'):
      return None
    th = len(tiles[0])
    tw = len(tiles)
    _c_l = list(range(tw))
    _r_l = list(range(th))
    if infos['format'] == 'image/x-bil;bits=32':
      mh = infos['height'] * th
      mw = infos['width'] * tw
      m = bytearray(4 * mh * mw)
      _m = memoryview(m)
      _w = infos['width'] * 4
      _mw = mw * 4
      _mw_r = infos['height'] * _mw
      _nd = struct.pack('<f', infos.get('nodata', 0)) * infos['width'] * infos['height']
      _tiles = [[memoryview(tiles[c][r] or _nd) for r in _r_l] for c in _c_l]
      _l = [(l * _mw, l * _w, (l + 1) * _w) for l in range(infos['height'])]
      for r in _r_l:
        _r = r * _mw_r
        for c in _c_l:
          _c = c * _w
          for _l_p, _l_0, _l_1 in _l:
            pos = _r + _l_p + _c
            _m[pos: pos + _w] = _tiles[c][r][_l_0: _l_1]
    elif infos['format'] in ('image/hgt', 'image/tiff', 'image/geotiff'):
      mh = infos['height'] * th + 1
      mw = infos['width'] * tw + 1
      m = bytearray(2 * mh * mw)
      _m = memoryview(m)
      _w = infos['width'] * 2
      _mw = mw * 2
      _mw_r = infos['height'] * _mw
      _nd = struct.pack('>h', infos.get('nodata', 0)) * infos['width'] * infos['height']
      _tiles = [[memoryview(tiles[c][r] or _nd) for r in _r_l] for c in _c_l]
      _l = [(l * _mw, l * (_w + 2), (l + 1) * (_w + 2) - 2) for l in range(infos['height'])]
      for r in _r_l:
        _r = r * _mw_r
        if r == th - 1:
          l = infos['height']
          _l.append((l * _mw, l * (_w + 2), (l + 1) * (_w + 2) - 2))
        for c in _c_l:
          _c = c * _w
          if c < tw - 1:
            for _l_p, _l_0, _l_1 in _l:
              pos = _r + _l_p + _c
              m[pos: pos + _w] = tiles[c][r][_l_0: _l_1]
          else:
            for _l_p, _l_0, _l_1 in _l:
              pos = _r + _l_p + _c
              m[pos: pos + _w + 2] = tiles[c][r][_l_0: _l_1 + 2]
    return m

  def RequestElevation(self, infos, points, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, threads=10):
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
    def _proc_json(j):
      eles = json.loads(j)
      star = False
      for k in infos['key']:
        if k == '*':
          star = True
        elif star:
          for i, e in enumerate(eles):
            try:
              eles[i] = e[k]
            except:
              eles[i] = e[int(k)]
        else:
          try:
            eles = eles[k]
          except:
            eles = eles[int(k)]
      return eles if isinstance(eles, (list, tuple)) else [eles]
    def _request_elevation():
      nonlocal posl
      nonlocal ind
      pconnection=[None]
      while True:
        if self.Closed:
          finished.set()
          break
        with ilock:
          if posl < len(lind):
            ind1, ind2 = lind[posl]
            posl += 1
          else:
            break
        try:
          uri = infos['source'].format_map({'key': key or '', 'location': infos['separator'].join(','.join(map(str, point)) for point in points[ind1:ind2])} if '{location}' in infos['source'] else {'key': key or '', 'lat': infos['separator'].join(str(point[0]) for point in points[ind1:ind2]), 'lon': infos['separator'].join(str(point[1]) for point in points[ind1:ind2])})
        except:
          pass
        try:
          rep = HTTPRequest(uri, 'GET', headers, pconnection=pconnection, basic_auth=basic_auth)
          try:
            if rep.code == '200' and rep.body:
              ele[ind1:ind2] = _proc_json(rep.body)
            else:
              raise
          except:
            uri1 = infos['source'].format_map({'location': infos['separator'].join(','.join(map(str, point)) for point in points[ind1:(ind1+ind2)//2])} if '{location}' in infos['source'] else {'key': key or '', 'lat': infos['separator'].join(str(point[0]) for point in points[ind1:(ind1+ind2)//2]), 'lon': infos['separator'].join(str(point[1]) for point in points[ind1:(ind1+ind2)//2])})
            uri2 = infos['source'].format_map({'location': infos['separator'].join(','.join(map(str, point)) for point in points[(ind1+ind2)//2:ind2])} if '{location}' in infos['source'] else {'key': key or '', 'lat': infos['separator'].join(str(point[0]) for point in points[(ind1+ind2)//2:ind2]), 'lon': infos['separator'].join(str(point[1]) for point in points[(ind1+ind2)//2:ind2])})
            rep1 = HTTPRequest(uri1, 'GET', headers, pconnection=pconnection, basic_auth=basic_auth)
            rep2 = HTTPRequest(uri2, 'GET', headers, pconnection=pconnection, basic_auth=basic_auth)
            try:
              ele[ind1:(ind1+ind2)//2] = _proc_json(rep1.body)
            except:
              pass
            ele[(ind1+ind2)//2:ind2] = _proc_json(rep2.body)
        except:
          pass
        with ilock:
          ind += ind2 - ind1
          if ind == len(points):
            finished.set()
    lind = [(limit * i, min(limit * (i + 1), len(points))) for i in range(1 + (len(points) - 1) // limit)]
    for t in range(threads if infos.get('parallel', False) else 1):
      th = threading.Thread(target=_request_elevation, daemon=True)
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

  def GenerateBil32Map(self, infos, minlat, maxlat, minlon, maxlon, nbpoints, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, threads=10):
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
    lats = [maxlat - (i + 0.5) * res for i in range(nrow)]
    lons = [minlon + (i + 0.5) * res for i in range(ncol)]
    points = list ((lat, lon) for lat in lats for lon in lons)
    eles = self.RequestElevation(infos, points, key, referer, user_agent, basic_auth, threads)
    if not eles:
      return False
    self.Map = struct.pack('<' + str(len(eles)) + 'f', *[(ele if ele is not None else infos.get('nodata', 0)) for ele in eles])
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

  def SetTilesProvider(self, rid=None, infos_base=None, matrix=None, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, only_local=False, lazy=True):
    if self.LazyTiles is None:
      return False
    if lazy:
      if 'Tiles' in vars(self):
        del self.Tiles
        try:
          self.LazyTiles.TilesInfos = None
          self.LazyTiles.Configure((-1, None), None)
        except:
          pass
      if rid is None:
        self.LazyTilesArgs = None
      else:
        self.LazyTilesArgs = (infos_base, matrix, local_pattern, local_expiration, local_store, key, referer, user_agent, basic_auth, only_local)
        self.LazyTiles.Id = rid
      return False
    else:
      return super().SetTilesProvider(rid, infos_base, matrix, local_pattern=local_pattern, local_expiration=local_expiration, local_store=local_store, key=key, referer=referer, user_agent=user_agent, basic_auth=basic_auth, only_local=only_local)

  def Close(self):
    self.Closed = True
    try:
      if self.LazyTiles is not None:
        self.LazyTiles.Close()
    except:
      pass


class WGS84Itinerary():

  BASE64_TABLE = {chr(i + 63): i for i in range(64)}
  URLSAFEBASE64_TABLE = {**{chr(i + 65): i for i in range(26)}, **{chr(i + 71): i for i in range(26, 52)}, **{chr(i - 4): i for i in range(52, 62)}, '-': 62, '_': 63}
  POLYLINE_RE =  re.compile(r'^{(flexible_)polyline}$|^{polyline(\d+)?}$', re.ASCII).match

  AS_IGN_ITI = {'alias': 'IGN_ITI', 'source': 'https://wxs.ign.fr/{key}/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-pgr&profile=pedestrian&optimization=shortest&start={lons},{lats}&end={lone},{late}&intermediates=&constraints={{"constraintType":"prefer","key":"importance","operator":">=","value":5}}&geometryFormat=geojson&getSteps=false&getBbox=false&crs=' + WGS84Map.CRS, 'key': ('geometry', 'coordinates')}
  # AS_IGN_ITI = {'alias': 'IGN_ITI', 'source': 'https://wxs.ign.fr/calcul/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-pgr&profile=pedestrian&optimization=shortest&start={lons},{lats}&end={lone},{late}&intermediates=&constraints={{"constraintType":"prefer","key":"importance","operator":">=","value":5}}&geometryFormat=polyline&getSteps=false&getBbox=false&crs=' + WGS84Map.CRS, 'key': ('geometry', '{polyline5}')}
  AS_OSRM = {'alias': 'OSRM', 'source': 'https://router.project-osrm.org/route/v1/foot/{lons},{lats};{lone},{late}?geometries=geojson&skip_waypoints=true&steps=false&overview=full', 'key': ('routes', 0, 'geometry', 'coordinates')}
  AS_OPENROUTE = {'alias': 'OPENROUTE', 'source': 'https://api.openrouteservice.org/v2/directions/foot-hiking?api_key={key}&start={lons},{lats}&end={lone},{late}', 'key': ('features', 0, 'geometry', 'coordinates')}
  AS_HERE_ROUTING = {'alias': 'HERE_ROUTING', 'source': 'https://router.hereapi.com/v8/routes?transportMode=pedestrian&origin={lats},{lons}&destination={late},{lone}&return=polyline&apikey={key}', 'key': ('routes', 0, 'sections', 0, 'polyline' , '{flexible_polyline}')}

  @classmethod
  def ASAlias(cls, name):
    if hasattr(cls, 'AS_' + name):
      return dict(getattr(cls, 'AS_' + name))
    else:
      return None

  def RequestItinerary(self, infos, points, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, pconnection=None):
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
    try:
      uri = infos['source'].format_map({'key': key or '', 'lats': points[0][0], 'lons': points[0][1], 'late': points[1][0], 'lone': points[1][1]})
      rep = HTTPRequest(uri, 'GET', headers, pconnection=pconnection, basic_auth=basic_auth)
      if rep.code != '200':
        return None
      if not rep.body:
        return None
      iti = json.loads(rep.body)
      form = 'j'
      for k in infos['key']:
        if (isinstance(k, str) and (g := WGS84Itinerary.POLYLINE_RE(k))):
          if g[1] is None:
            form = 'p'
            h = 5 if g[2] is None else int(g[2])
          else:
            form = 'f'
          break
        else:
          try:
            iti = iti[k]
          except:
            iti = iti[int(k)]
      if form == 'p':
        g = map(WGS84Itinerary.BASE64_TABLE.get, iti)
      elif form == 'f':
        g = map(WGS84Itinerary.URLSAFEBASE64_TABLE.get, iti)
        h = None
        i = 0
        for c in g:
          if h is None:
            if not (c & 0x20):
              h = 0
            continue
          h |= (c & 0x1f) << i
          if (c & 0x20):
            i += 5
          else:
            break
      if form in ('p', 'f'):
        x = 0
        i = 0
        l = [0, 0]
        p = 0
        p3 = bool((h >> 4) & 0x7)
        for c in g:
          if p3:
            if p == 2:
              if not (c & 0x20):
                p = 0
              continue
            else:
              if not (c & 0x20):
                p += 1
          x += (c & 0x1f) << i
          if (c & 0x20):
            i += 5
          else:
            l.append(l[-2] + ((-((x + 1) >> 1)) if (x & 0x01) else (x >> 1)))
            x = 0
            i = 0
        g = iter(l)
        next(g)
        next(g)
        iti = list(zip(*((map((10 ** -(h & 0xf)).__mul__, g),) * 2)))
      else:
        iti = [s[::-1] for s in iti]
      if math.dist(WGS84WebMercator.WGS84toWebMercator(*iti[0]), WGS84WebMercator.WGS84toWebMercator(*map(float, points[0]))) > math.dist(WGS84WebMercator.WGS84toWebMercator(*iti[-1]), WGS84WebMercator.WGS84toWebMercator(*map(float, points[0]))):
        iti.reverse()
      return iti
    except:
      return None


class WGS84ReverseGeocoding():

  AS_IGN_GEOCODAGE_50 = {'alias': 'IGN_GEOCODAGE_50', 'source': 'https://wxs.ign.fr/{key}/geoportail/geocodage/rest/0.1/reverse?index=poi&searchgeom={{"type":"Circle","coordinates":[{lon},{lat}],"radius":50}}&lon={lon}&lat={lat}','key': ('features', 'properties', 'extrafields', 'names')}
  AS_IGN_GEOCODAGE = AS_IGN_GEOCODAGE_150 = {'alias': 'IGN_GEOCODAGE_150', 'source': 'https://wxs.ign.fr/{key}/geoportail/geocodage/rest/0.1/reverse?index=poi&searchgeom={{"type":"Circle","coordinates":[{lon},{lat}],"radius":150}}&lon={lon}&lat={lat}','key': ('features', 'properties', 'extrafields', 'names')}
  AS_IGN_GEOCODAGE_250 = {'alias': 'IGN_GEOCODAGE_250', 'source': 'https://wxs.ign.fr/{key}/geoportail/geocodage/rest/0.1/reverse?index=poi&searchgeom={{"type":"Circle","coordinates":[{lon},{lat}],"radius":250}}&lon={lon}&lat={lat}','key': ('features', 'properties', 'extrafields', 'names')}
  AS_OSM_NOMINATIM = {'alias': 'OSM_NOMINATIM', 'source': 'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=jsonv2','key': ('display_name',)}
  AS_OPENROUTE_150 = {'alias': 'OPENROUTE_150', 'source': 'https://api.openrouteservice.org/geocode/reverse?api_key={key}&point.lon={lon}&point.lat={lat}&boundary.circle.radius=0.15','key': ('features', 'properties', 'name')}
  AS_GOOGLE_MAPS_FR = {'alias': 'GOOGLE_MAPS_FR', 'source': 'https://www.google.fr/maps/place/{lat},{lon}','regex': '<[^<]*?· (.*?). itemprop="name">'}
  AS_HERE_150 = {'alias': 'HERE_150', 'source': 'https://revgeocode.search.hereapi.com/v1/revgeocode?in=circle:{lat},{lon};r=150&limit=10&apikey={key}','key': ('items', 'title')}

  @classmethod
  def ASAlias(cls, name):
    if hasattr(cls, 'AS_' + name):
      return dict(getattr(cls, 'AS_' + name))
    else:
      return None

  @staticmethod
  def _parse_json(j, k, f=0):
    if f < len(k):
      if isinstance(j[k[f]], (list, tuple)):
        return ' | '.join(WGS84ReverseGeocoding._parse_json(e, k, f+1) for e in j[k[f]])
      else:
        return WGS84ReverseGeocoding._parse_json(j[k[f]], k, f+1)
    else:
      return j

  def RequestDescription(self, infos, point, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, pconnection=None):
    if not isinstance(point, (list, tuple)):
      return None
    if len(point) != 2:
      return
    if not isinstance(point[0], (float, int)) or not isinstance(point[1], (float, int)):
      return
    headers = {}
    if referer:
      headers['Referer'] = referer
    if user_agent:
      headers['User-Agent'] = user_agent
    if not infos.get('source'):
      return None
    try:
      uri = infos['source'].format_map({'key': key or '', 'lat': point[0], 'lon': point[1]})
      rep = HTTPRequest(uri, 'GET', headers, pconnection=pconnection, basic_auth=basic_auth)
      if rep.code != '200':
        return None
      if not rep.body:
        return None
      if 'key' in infos:
        jdesc = json.loads(rep.body)
        return WGS84ReverseGeocoding._parse_json(jdesc, infos['key'])
      elif 'regex' in infos:
        return re.search(infos['regex'],rep.body.decode('utf-8')).group(1)
      else:
        return None
    except:
      return None


class MapLegend():

  ML_IGN_PLANV2 = {'*': 'https://wxs.ign.fr/static/legends/GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2-legend.png'}
  TL_IGN_PLANV2 = {'*': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2/legendes/GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2_{matrix}-legend.png', '17': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2/legendes/GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2_17-18-legend.png', '18': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2/legendes/GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2_17-18-legend.png'}
  TL_IGN_CARTES = {'9': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.MAPS/legendes/GEOGRAPHICALGRIDSYSTEMS.MAPS_1000k-legend.png', '10': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.MAPS/legendes/GEOGRAPHICALGRIDSYSTEMS.MAPS_1000k-legend.png', '11': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.MAPS/legendes/GEOGRAPHICALGRIDSYSTEMS.MAPS_REG-legend.png', '12': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.MAPS/legendes/GEOGRAPHICALGRIDSYSTEMS.MAPS_REG-legend.png', '13': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.MAPS/legendes/GEOGRAPHICALGRIDSYSTEMS.MAPS_100k-legend.png', '14': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.MAPS/legendes/GEOGRAPHICALGRIDSYSTEMS.MAPS_100k-legend.png', '15': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.MAPS/legendes/GEOGRAPHICALGRIDSYSTEMS.MAPS_25k-legend.png', '16': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.MAPS/legendes/GEOGRAPHICALGRIDSYSTEMS.MAPS_25k-legend.png', '17': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.MAPS/legendes/GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2_17-18-legend.png', '18': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.MAPS/legendes/GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2_17-18-legend.png'}
  TL_IGN_NOMS = {'8': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALNAMES.NAMES/legendes/GEOGRAPHICALNAMES.NAMES-legend-1M-10M.png', '9': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALNAMES.NAMES/legendes/GEOGRAPHICALNAMES.NAMES-legend-200k-1M.png', '10': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALNAMES.NAMES/legendes/GEOGRAPHICALNAMES.NAMES-legend-200k-1M.png', '11': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALNAMES.NAMES/legendes/GEOGRAPHICALNAMES.NAMES-legend-200k-1M.png', '12': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALNAMES.NAMES/legendes/GEOGRAPHICALNAMES.NAMES-legend-20k-200k.png', '13': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALNAMES.NAMES/legendes/GEOGRAPHICALNAMES.NAMES-legend-20k-200k.png', '14': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALNAMES.NAMES/legendes/GEOGRAPHICALNAMES.NAMES-legend-20k-200k.png', '15': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALNAMES.NAMES/legendes/GEOGRAPHICALNAMES.NAMES-legend-20k-200k.png', '16': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALNAMES.NAMES/legendes/GEOGRAPHICALNAMES.NAMES-legend-100-20k.png', '17': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALNAMES.NAMES/legendes/GEOGRAPHICALNAMES.NAMES-legend-100-20k.png', '18': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALNAMES.NAMES/legendes/GEOGRAPHICALNAMES.NAMES-legend-100-20k.png'}
  TL_IGN_PENTESMONTAGNE = {'*': 'https://www.geoportail.gouv.fr/depot/layers/GEOGRAPHICALGRIDSYSTEMS.SLOPES.MOUNTAIN/legendes/GEOGRAPHICALGRIDSYSTEMS.SLOPES.MOUNTAIN-legend.png'}
  TL_CYCLOSM = {'*': 'https://veillecarto2-0.fr/wp-content/uploads/2019/10/extrait_le%CC%81gende.png'}
  TL_THUNDERFOREST_CYCLE = {'*': 'https://www.cyclestreets.net/images/general/mapkeyopencyclemap.png'}

  def __init__(self):
    self.WMSCache = {}
    self.WMTSCache = {}
    self.log = partial(log, 'legend')

  @classmethod
  def MLAlias(cls, name):
    if hasattr(cls, 'ML_' + name):
      return dict(getattr(cls, 'ML_' + name))
    else:
      return None

  @classmethod
  def TLAlias(cls, name):
    if hasattr(cls, 'TL_' + name):
      return dict(getattr(cls, 'TL_' + name))
    else:
      return None

  def FetchMapLegendInfos(self, infos, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None):
    if 'source' not in infos or '{wms}' not in infos['source'] or not infos.get('layers'):
      return None
    headers = {'User-Agent': user_agent}
    if referer:
      headers['Referer'] = referer
    try:
      uri = infos['source'].format_map({'wms': WebMercatorMap.WMS_PATTERN['GetCapabilities'], 'key': key or ''}).format_map(infos)
    except:
      return None
    rep = HTTPRequest(uri, 'GET', headers, basic_auth=basic_auth)
    if rep.code != '200':
      return None
    try:
      inf_layers = infos['layers'].split(',')
      inf_styles = infos['styles'].split(',')
      inf_styles.extend([''] * max(0, len(inf_layers) - len(inf_styles)))
      layers_styles = {layer: [style for lay, style in zip(inf_layers, inf_styles) if lay == layer] for layer in inf_layers}
      cap = minidom.parseString(rep.body)
      capability = cap.getElementsByTagNameNS('*', 'Capability')[0]
      f_u = {}
      for node in capability.getElementsByTagNameNS('*', 'Layer'):
        layer = None
        layer_name = ''
        for c_node in node.childNodes:
          if c_node.localName == 'Name':
            layer_name = _XMLGetNodeText(c_node)
            if layer_name in layers_styles:
              layer = node
            break
        if layer:
          styles = layers_styles[layer_name]
          def_style = '' in styles
          for s_node in layer.getElementsByTagNameNS('*', 'Style'):
            style = None
            for c_node in s_node.childNodes:
              if c_node.localName == 'Name':
                style_name = _XMLGetNodeText(c_node)
                if style_name in styles or def_style:
                  style = s_node
                break
            if style:
              try:
                l_node = style.getElementsByTagNameNS('*', 'LegendURL')[0]
              except:
                l_node = None
              if l_node:
                try:
                  format = _XMLGetNodeText(l_node.getElementsByTagNameNS('*', 'Format')[0])
                except:
                  format = ''
                try:
                  url = l_node.getElementsByTagNameNS('*', 'OnlineResource')[0].getAttribute('xlink:href')
                except:
                  url = None
              if url is not None:
                if style_name in styles:
                  f_u[(layer_name, style_name)] = (format, url)
                if def_style:
                  f_u[(layer_name, '')] = (format, url)
            def_style = False
    except:
      return {}
    self.WMSCache.update({(infos['source'], *l_s): fu for l_s, fu in f_u.items()})
    return f_u

  def FetchKnownMapLegend(self, formats_urls, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None):
    headers = {'User-Agent': user_agent}
    if referer:
      headers['Referer'] = referer
    f_l = {}
    for l_s, f_u in formats_urls.items():
      try:
        uri = f_u[1].format_map({'key': key or ''})
      except:
        continue
      rep = HTTPRequest(uri, 'GET', headers, basic_auth=basic_auth)
      if rep.code != '200':
        continue
      f_l[l_s] = (rep.header('content-type', f_u[0]), rep.body)
    return f_l

  def FetchMapLegend(self, infos, urls=None, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None):
    urls_ = urls or {}
    try:
      urls_.update({(l, s): fu[1] for (so, l, s), fu in self.WMSCache.items() if so == infos['source'] and (l, s) not in urls_})
      layers = infos['layers'].split(',')
      styles = infos['styles'].split(',')
      styles.extend([''] * max(0, len(layers) - len(styles)))
    except:
      return {}
    p_l = [l_s for l_s in zip(layers, styles) if l_s in urls_]
    m_l = [l_s for l_s in zip(layers, styles) if l_s not in urls_]
    if m_l:
      try:
        inf = {**infos}
        inf['layers'] = ','.join(l_s[0] for l_s in m_l)
        inf['styles'] = ','.join(l_s[1] for l_s in m_l)
        f_u = self.FetchMapLegendInfos(inf, key, referer, user_agent, basic_auth)
        if f_u:
          f_l = self.FetchKnownMapLegend(f_u, key, referer, user_agent, basic_auth)
        else:
          f_l = {}
      except:
        f_l = {}
    else:
      f_l = {}
    if p_l:
      f_l.update(self.FetchKnownMapLegend({l_s: ('', u) for l_s, u in urls_.items() if l_s in p_l}, key, referer, user_agent, basic_auth))
    return f_l

  def RetrieveMapLegend(self, infos, urls=None, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None):
    self.log(2, 'legendretrieve', infos)
    try:
      if urls is not None:
        layers = infos['layers'].split(',')
        styles = infos['styles'].split(',')
        styles.extend([''] * max(0, len(layers) - len(styles)))
        urls_ = {l_s: urls.get(l_s, urls.get('*')).format_map({**infos, 'key': key or ''}) for l_s in zip(layers, styles) if (l_s in urls or '*' in urls)}
      else:
        urls_ = None
      f_l = self.FetchMapLegend(infos, urls_, key, referer, user_agent, basic_auth)
    except:
      self.log(2, 'legendfail', infos)
      return {}
    if f_l:
      self.log(2, 'legendretrieved1', infos, len(f_l))
    else:
      self.log(2, 'legendfail', infos)
    return f_l

  def GetTilesLegendInfos(self, infos, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, capabilities = None):
    if 'source' not in infos or '{wmts}' not in infos['source'] or not infos.get('layer') or 'style' not in infos:
      return None
    if capabilities is None:
      headers = {'User-Agent': user_agent}
      if referer:
        headers['Referer'] = referer
      try:
        uri = infos['source'].format_map({'wmts': WebMercatorMap.WMTS_PATTERN['GetCapabilities'], 'key': key or ''}).format_map(infos)
      except:
        return None
      rep = HTTPRequest(uri, 'GET', headers, basic_auth=basic_auth)
      if rep.code != '200':
        return None
    f_u = []
    try:
      cap = minidom.parseString(rep.body) if capabilities is None else capabilities
      content = cap.getElementsByTagNameNS('*', 'Contents')[0]
      layer = None
      for node in content.getElementsByTagNameNS('*', 'Layer'):
        for c_node in node.childNodes:
          if c_node.localName == 'Identifier':
            if _XMLGetNodeText(c_node) == infos['layer']:
              layer = node
              break
        if layer:
          break
      if not layer:
        return []
      style = None
      for node in layer.getElementsByTagNameNS('*', 'Style'):
        for c_node in node.childNodes:
          if c_node.localName == 'Identifier':
            if _XMLGetNodeText(c_node) == infos['style']:
              style = node
            break
        if style:
          break
      if not style:
        return []
      for node in layer.getElementsByTagNameNS('*', 'LegendURL'):
        format = node.getAttribute('format')
        url = node.getAttribute('xlink:href')
        try:
          minsd = float(node.getAttribute('minScaleDenominator'))
        except:
          minsd = 0
        try:
          maxsd = float(node.getAttribute('maxScaleDenominator'))
        except:
          maxsd = float('inf')
        f_u.append(((minsd, maxsd), (format, url)))
    except:
      return []
    finally:
      if capabilities is None:
        try:
          cap.unlink()
        except:
          pass
    f_u.sort(key=lambda k:k[0][0])
    self.WMTSCache[(infos['source'], infos['layer'], infos['style'])] = f_u
    return f_u

  def GetKnownTilesLegend(self, infos, formats_urls, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None):
    headers = {'User-Agent': user_agent}
    if referer:
      headers['Referer'] = referer
    try:
      sd = infos['scale'] / 0.28 * 1000
      f_h = next((f_u for f_u in formats_urls if f_u[0][0] <= sd and sd < f_u[0][1]), None)[1]
      uri = f_h[1].format_map({'key': key or ''})
    except:
      return None
    rep = HTTPRequest(uri, 'GET', headers, basic_auth=basic_auth)
    if rep.code != '200':
      return None
    return (rep.header('content-type') or f_h[0], rep.body)

  def GetTilesLegend(self, infos, url=None, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None):
    if url is None:
      f_u = self.WMTSCache.get((infos['source'], infos['layer'], infos['style']))
      try:
        if f_u is None:
          f_u = self.GetTilesLegendInfos(infos, key, referer, user_agent, basic_auth)
        if f_u is None:
          return None
        f_l = self.GetKnownTilesLegend(infos, f_u, key, referer, user_agent, basic_auth)
      except:
        return None
    else:
      f_l = self.GetKnownTilesLegend(infos, [((0, float('inf')), ('', url))], key, referer, user_agent, basic_auth)
    return f_l

  def ReadTilesLegend(self, pattern, infos, just_lookup=False):
    if not infos.get('source') or not infos.get('layer') or not infos.get('matrix') or '{hgt}' in infos['source'] or infos.get('format') == 'image/hgt':
      return None
    if '{' not in pattern:
      pattern = os.path.join(pattern, WebMercatorMap.LOCALSTORE_DEFAULT_PATTERN)
    try:
      legendpattern = os.path.dirname(pattern)
      while '{matrix}' in os.path.dirname(legendpattern):
        legendpattern = os.path.dirname(legendpattern)
      legendpath = legendpattern.format_map({**infos, **{'alias|layer': infos.get('alias') or infos.get('layer', '')}})
      legendpath = next((e for e in Path(legendpath).glob('legend.*') if e.is_file()), None)
      if legendpath is None:
        return None
    except:
      return None
    try:
      if just_lookup:
        return os.path.getmtime(legendpath)
      f_l = (WebMercatorMap.DOTEXT_MIME.get(legendpath.suffix.lower(), 'image'), legendpath.read_bytes())
    except:
      return None
    return f_l

  def SaveTilesLegend(self, pattern, infos, format, legend, just_refresh=False):
    if not infos.get('source') or not infos.get('layer') or not infos.get('matrix') or '{hgt}' in infos['source'] or infos.get('format') == 'image/hgt':
      return False
    if '{' not in pattern:
      pattern = os.path.join(pattern, WebMercatorMap.LOCALSTORE_DEFAULT_PATTERN)
    try:
      legendpattern = os.path.dirname(pattern)
      while '{matrix}' in os.path.dirname(legendpattern):
        legendpattern = os.path.dirname(legendpattern)
      ext = WebMercatorMap.MIME_DOTEXT.get(format, '.img')
      legendpath = os.path.join(legendpattern.format_map({**infos, **{'alias|layer': infos.get('alias') or infos.get('layer', '')}}), 'legend' + ext)
      if just_refresh:
        os.utime(legendpath, (time.time(),) * 2)
      else:
        Path(os.path.dirname(legendpath)).mkdir(parents=True, exist_ok=True)
        for e in Path(os.path.dirname(legendpath)).glob('legend.*'):
          if e.is_file():
            try:
              e.unlink()
            except:
              pass
        Path(legendpath).write_bytes(legend)
    except:
      return False
    return True

  def RetrieveTilesLegend(self, infos, url=None, local_pattern=None, local_expiration=None, local_store=False, key=None, referer=None, user_agent='GPXTweaker', basic_auth=None, only_local=False):
    self.log(2, 'legendretrieve', infos)
    f_l = None
    local_f_l = None
    expired = True
    last_mod = False
    format = 'image'
    if isinstance(url, dict):
      url = url.get(infos['matrix'], url.get('*'))
    if url is not None:
      url = url.format_map({**infos, 'key': key or ''})
    try:
      if local_pattern is not None:
        last_mod = self.ReadTilesLegend(local_pattern, infos, just_lookup=True)
        if last_mod is not None:
          self.log(2, 'legendlfound', infos)
          f_l = self.ReadTilesLegend(local_pattern, infos)
          if f_l:
            if local_expiration is not None:
              if local_expiration > max(time.time() - last_mod, 0) / 86400:
                expired = False
              else:
                local_f_l = f_l
                self.log(2, 'legendlexpired', infos)
            else:
              expired = False
      if expired:
        if only_local:
          f_l = None
        else:
          self.log(2, 'legendfetch', infos)
          f_l = self.GetTilesLegend(infos, url, key, referer, user_agent, basic_auth)
        if f_l is not None and local_pattern is not None:
          if f_l != local_f_l:
            if local_store:
              try:
                self.SaveTilesLegend(local_pattern, infos, *f_l)
              except:
                pass
          elif local_store:
            self.SaveTilesLegend(local_pattern, infos, *f_l, just_refresh=True)
    except:
      self.log(2, 'legendfail', infos)
      return None
    if f_l is None:
      self.log(2, 'legendfail', infos)
    else:
      self.log(2, 'legendretrieved2', infos)
    return f_l


class XMLNode():

  __slots__ = ()

  EMPTY_NAMESPACE = None
  XMLNS_NAMESPACE = 'http://www.w3.org/2000/xmlns/'
  EMPTY_PREFIX = None
  DOCUMENT_NODE = 1
  ELEMENT_NODE = 2
  TEXT_NODE = 3
  CDATA_SECTION_NODE = 4
  COMMENT_NODE = 5

  nodeType = 0

  def __bool__(self):
    return True

  def hasChildNodes(self):
    return bool(self.childNodes)

  @property
  def firstChild(self):
    return self.childNodes[0] if self.childNodes else None

  @firstChild.setter
  def firstChild(self, value):
    raise

  @property
  def lastChild(self):
    return self.childNodes[-1] if self.childNodes else None

  @lastChild.setter
  def lastChild(self, value):
    raise

  def __enter__(self):
    return self

  def __exit__(self, et, ev, tb):
    self.unlink()

  def toxml(self, indent='  ', newl='\n'):
    writer = StringIO()
    self.writexml(writer, '', indent, newl)
    return writer.getvalue().encode('utf-8')


class XMLElement(XMLNode):

  __slots__ = ('name', 'namespaceURI', 'localName', 'childNodes', 'attributes')

  nodeType = XMLNode.ELEMENT_NODE

  def __init__(self, name, namespaceuri, localname):
    self.name = name
    self.namespaceURI = namespaceuri
    self.localName = localname
    self.attributes = None
    self.childNodes = []

  @property
  def prefix(self):
    return self.name.rpartition(':')[0] or XMLNode.EMPTY_PREFIX

  @prefix.setter
  def prefix(self, value):
    raise

  def hasAttributes(self):
    return bool(self.attributes)

  def unlink(self):
    if self.childNodes:
      for child in self.childNodes:
        child.unlink()
      self.childNodes = []
    self.attributes = None

  def cloneNode(self):
    clone = XMLElement(self.name, self.namespaceURI, self.localName)
    if self.attributes:
      clone.attributes = {}
      for k, v in self.attributes.items():
        clone.attributes[k] = v[:]
    if self.childNodes:
      for child in self.childNodes:
        clone.childNodes.append(child.cloneNode())
    return clone

  def getAttribute(self, localname, namespaceuri=XMLNode.EMPTY_NAMESPACE):
    if self.attributes:
      return self.attributes.get((namespaceuri, localname), [None, None])[1]
    else:
      return None

  def setAttribute(self, localname, value, namespaceuri=XMLNode.EMPTY_NAMESPACE, name=''):
    if self.attributes is None:
      self.attributes = {}
    if namespaceuri == XMLNode.EMPTY_NAMESPACE:
      self.attributes[(namespaceuri, localname)] = [localname, value]
    elif namespaceuri == XMLNode.XMLNS_NAMESPACE:
      attr_i = list(self.attributes.items())
      attr = self.attributes
      self.attributes = {}
      for k, v in attr_i:
        if k[0] != XMLNode.XMLNS_NAMESPACE:
          break
        self.attributes[k] = attr.pop(k)
      self.attributes[(namespaceuri, localname)] = [name, value]
      self.attributes.update(attr)
    else:
      self.attributes[(namespaceuri, localname)] = [name, value]

  def removeAttribute(self, localname, namespaceuri=XMLNode.EMPTY_NAMESPACE):
    if self.attributes:
      self.attributes.pop((namespaceuri, localname), None)

  def hasAttribute(self, localname, namespaceuri=XMLNode.EMPTY_NAMESPACE):
    if self.attributes:
      return (namespaceuri, localname) in self.attributes
    else:
      return False

  def getNameSpaces(self):
    if self.attributes:
      return [(k[1], v) for k, v in self.attributes.items() if k[0] == XMLNode.XMLNS_NAMESPACE]
    else:
      return []

  def getChildren(self, localname, namespaceuri=' '):
    if namespaceuri == ' ':
      namespaceuri = self.namespaceURI
    return [node for node in self.childNodes if (namespaceuri == '*' or node.namespaceURI == namespaceuri) and (localname == '*' or node.localName == localname)]

  def insertBefore(self, newChildren, refChild=None):
    if not isinstance(newChildren, (tuple, list)):
      newChildren = (newChildren,)
    index = self.childNodes.index(refChild) if refChild is not None else len(self.childNodes)
    self.childNodes[index:index] = newChildren
    return newChildren

  def insertAfter(self, newChildren, refChild=None):
    if not isinstance(newChildren, (tuple, list)):
      newChildren = (newChildren,)
    index = self.childNodes.index(refChild) + 1 if refChild is not None else 0
    self.childNodes[index:index] = newChildren
    return newChildren

  def appendChild(self, newChild):
    self.childNodes.append(newChild)
    return newChild

  def replaceChild(self, newChild, oldChild):
    if newChild is oldChild:
      return
    self.childNodes[self.childNodes.index(oldChild)] = newChild
    return oldChild

  def removeChild(self, oldChild):
    self.childNodes.remove(oldChild)
    return oldChild

  def removeChildren(self, localname, namespaceuri=' '):
    if namespaceuri == ' ':
      namespaceuri = self.namespaceURI
    nodes = []
    index = 0
    while index < len(self.childNodes):
      node = self.childNodes[index]
      if node.nodeType == XMLNode.ELEMENT_NODE:
        if (namespaceuri == '*' or node.namespaceURI == namespaceuri) and (localname == '*' or node.localName == localname):
          nodes.append(self.childNodes.pop(index))
          continue
      index += 1
    return nodes

  def getText(self):
    return ''.join(childnode.data for childnode in self.childNodes if childnode.nodeType in (XMLNode.TEXT_NODE, XMLNode.CDATA_SECTION_NODE))

  def getChildrenText(self, localname, namespaceuri=' '):
    return ''.join(node.getText() for node in self.getChildren(localname, namespaceuri))

  def __repr__(self):
    return '<DOM Element: %s at %#x>' % (self.name, id(self))

  def writexml(self, writer, indent='', addindent='', newl=''):
    writer.write(f'{indent}<{self.name}')
    if self.attributes:
      for n_v in self.attributes.values():
        v = (n_v[1] or '').replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;').replace('>', '&gt;')
        writer.write(f' {n_v[0]}="{v}"')
    if self.childNodes:
      writer.write('>')
      if len(self.childNodes) == 1 and self.childNodes[0].nodeType in (XMLNode.TEXT_NODE, XMLNode.CDATA_SECTION_NODE):
        self.childNodes[0].writexml(writer, '', '', '')
      elif self.namespaceURI == 'http://www.topografix.com/GPX/1/1' and self.localName in ('trkpt', 'wpt'):
        for node in self.childNodes:
          node.writexml(writer, '', '', '')
      else:
        writer.write(newl)
        for node in self.childNodes:
          node.writexml(writer, indent + addindent, addindent, newl)
        writer.write(indent)
      writer.write(f'</{self.name}>{newl}')
    else:
      writer.write(f'/>{newl}')


class XMLCharacterData(XMLNode):

  __slots__ = ('data',)

  namespaceURI = XMLNode.EMPTY_NAMESPACE
  prefix = XMLNode.EMPTY_PREFIX

  def __init__(self, data=''):
    self.data = data

  @property
  def childNodes(self):
    return []

  @childNodes.setter
  def childNodes(self, value):
    raise

  def unlink(self):
    pass

  def __repr__(self):
    return '<DOM %s node "%r">' % (self.__class__.__name__, (self.data[0:10] + '...' if len(self.data) > 10 else self.data))


class XMLText(XMLCharacterData):

  __slots__ = ()

  nodeType = XMLNode.TEXT_NODE
  name = localName = '#text'

  def cloneNode(self):
    return XMLText(self.data)

  def writexml(self, writer, indent='', addindent='', newl=''):
    d = (self.data or '').replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;').replace('>', '&gt;')
    writer.write(f'{indent}{d}{newl}')


class XMLCDATASection(XMLCharacterData):

  __slots__ = ()

  nodeType = XMLNode.CDATA_SECTION_NODE
  name = localName = '#cdata-section'

  def cloneNode(self):
    return XMLCDATASection(self.data)

  def writexml(self, writer, indent='', addindent='', newl=''):
    writer.write(f'<![CDATA[{self.data or ""}]]>')


class XMLComment(XMLCharacterData):

  __slots__ = ()

  nodeType = XMLNode.COMMENT_NODE
  name = localName = '#comment'

  def cloneNode(self):
    return XMLComment(self.data)

  def writexml(self, writer, indent='', addindent='', newl=''):
    writer.write(f'{indent}<!--{self.data or ""}-->{newl}')


class XMLDocument(XMLNode):

  __slots__ = ('version', 'encoding', 'childNodes')

  nodeType = XMLNode.DOCUMENT_NODE
  name = localName = '#document'
  namespaceURI = XMLNode.EMPTY_NAMESPACE
  prefix = XMLNode.EMPTY_PREFIX

  def __init__(self, version=None, encoding='utf-8'):
    self.version = version
    self.encoding = encoding
    self.childNodes = []

  documentElement = XMLNode.firstChild

  def unlink(self):
    if self.documentElement is not None:
      self.documentElement.unlink()
    self.childNodes = []

  def cloneNode(self):
    clone = XMLDocument(self.version, self.encoding)
    if self.documentElement is not None:
      clone.childNodes.append(self.documentElement.cloneNode())
    return clone

  def appendChild(self, newChild):
    if self.hasChildNodes():
      raise
    self.childNodes.append(newChild)
    return newChild

  def __repr__(self):
    return '<DOM Document at %#x>' % id(self)

  def writexml(self, writer, indent='', addindent='', newl=''):
    writer.write(f'<?xml version="1.0" encoding="utf-8"?>{newl}')
    for node in self.childNodes:
      node.writexml(writer, indent, addindent, newl)


class ExpatGPXBuilder:

  def __new__(cls):
    b = object.__new__(cls)
    b.intern_dict = {}
    b.intern = b.intern_dict.setdefault
    b.XMLNS = b.intern('xmlns', 'xmlns')
    b.XMLNS_NAMESPACE = b.intern(XMLNode.XMLNS_NAMESPACE, XMLNode.XMLNS_NAMESPACE)
    b.XSI = b.intern('xsi', 'xsi')
    b.XMLNS_XSI = b.intern('xmlns:xsi', 'xmlns:xsi')
    b.XSI_NAMESPACE = b.intern('http://www.w3.org/2001/XMLSchema-instance', 'http://www.w3.org/2001/XMLSchema-instance')
    b.GPX_NAMESPACE = b.intern('http://www.topografix.com/GPX/1/1', 'http://www.topografix.com/GPX/1/1')
    b.GPXSTYLE_NAMESPACE = b.intern('http://www.topografix.com/GPX/gpx_style/0/2', 'http://www.topografix.com/GPX/gpx_style/0/2')
    return b

  def __init__(self):
    self.Parser = None
    self.Document = None
    self.CurNode = None
    self.CurNodeNSDecl = []
    self.ParNodes = []
    self.CDataSection = False
    self.CurText = ''

  def NewParser(self):
    self.__init__()
    try:
      self.Parser = expat.ParserCreate(namespace_separator=' ', intern = self.intern_dict)
    except:
      self.Parser = expat.ParserCreate(namespace_separator=' ')
      self.intern_dict = self.Parser.intern
      self.intern = self.intern_dict.setdefault
      self.XMLNS = self.intern('xmlns', 'xmlns')
      self.XMLNS_NAMESPACE = self.intern(XMLNode.XMLNS_NAMESPACE, XMLNode.XMLNS_NAMESPACE)
      self.XSI = self.intern('xsi', 'xsi')
      self.XMLNS_XSI = self.intern('xmlns:xsi', 'xmlns:xsi')
      self.XSI_NAMESPACE = self.intern('http://www.w3.org/2001/XMLSchema-instance', 'http://www.w3.org/2001/XMLSchema-instance')
      self.GPX_NAMESPACE = self.intern('http://www.topografix.com/GPX/1/1', 'http://www.topografix.com/GPX/1/1')
      self.GPXSTYLE_NAMESPACE = self.intern('http://www.topografix.com/GPX/gpx_style/0/2', 'http://www.topografix.com/GPX/gpx_style/0/2')
    self.Parser.buffer_text = True
    self.Parser.ordered_attributes = True
    self.Parser.specified_attributes = True
    self.Parser.namespace_prefixes = True
    self.Parser.XmlDeclHandler = self.XmlDeclHandler
    self.Parser.StartElementHandler = self.StartElementHandler
    self.Parser.EndElementHandler = self.EndElementHandler
    self.Parser.StartCdataSectionHandler = self.StartCdataSectionHandler
    self.Parser.EndCdataSectionHandler = self.EndCdataSectionHandler
    self.Parser.CharacterDataHandler = self.CharacterDataHandler
    self.Parser.StartNamespaceDeclHandler = self.StartNamespaceDeclHandler
    self.Parser.EndNamespaceDeclHandler = self.EndNamespaceDeclHandler
    self.Parser.CommentHandler = self.CommentHandler
    self.Parser.DefaultHandler = self.DefaultHandler

  def Parse(self, xmlstring):
    self.NewParser()
    try:
      self.Parser.Parse(xmlstring, True)
      if len(self.Document.childNodes) != 1:
        raise
      r = self.Document.documentElement
      if r.localName != 'gpx' or (r.namespaceURI != XMLNode.EMPTY_NAMESPACE and r.namespaceURI != self.GPX_NAMESPACE):
        raise
      if not r.hasAttribute(self.XMLNS, self.XMLNS_NAMESPACE):
        r.setAttribute(self.XMLNS, self.GPX_NAMESPACE, self.XMLNS_NAMESPACE, self.XMLNS)
      r.setAttribute(self.XSI, self.XSI_NAMESPACE, self.XMLNS_NAMESPACE, self.XMLNS_XSI)
      sl = r.getAttribute('schemaLocation', self.XSI_NAMESPACE) or ''
      if self.GPX_NAMESPACE not in sl:
        sl = (sl + ' http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd').lstrip()
      if self.GPXSTYLE_NAMESPACE not in sl:
        sl = (sl + ' http://www.topografix.com/GPX/gpx_style/0/2 http://www.topografix.com/GPX/gpx_style/0/2/gpx_style.xsd')
      r.setAttribute(self.intern('schemaLocation', 'schemaLocation'), sl, self.XSI_NAMESPACE, self.intern('xsi:schemaLocation', 'xsi:schemaLocation'))
    except:
      self.Document = None
    doc = self.Document
    self.__init__()
    return doc

  def XmlDeclHandler(self, version, encoding, standalone):
    self.Document = XMLDocument(version, encoding)
    self.CurNode = self.Document

  def StartElementHandler(self, name, attributes):
    self.CurText = ''
    parts = name.split(' ')
    l = len(parts)
    if l == 2:
      uri, localname = parts
      uri = self.intern(uri, uri)
      qname = localname = self.intern(localname, localname)
    elif l == 3:
      uri, localname, prefix = parts
      uri = self.intern(uri, uri)
      localname = self.intern(localname, localname)
      qname = prefix + ':' + localname
      qname = self.intern(qname, qname)
    elif l == 1:
      uri = XMLNode.EMPTY_NAMESPACE
      qname = localname = name
    else:
      raise
    node = XMLElement(qname, uri, localname)
    self.CurNode.childNodes.append(node)
    self.ParNodes.append(self.CurNode)
    self.CurNode = node
    if self.CurNodeNSDecl:
      node.attributes = {}
      for prefix, uri2 in self.CurNodeNSDecl:
        if prefix:
          node.attributes[(self.XMLNS_NAMESPACE, prefix)] = [self.intern('xmlns:' + prefix, 'xmlns:' + prefix), uri2]
        else:
          node.attributes[(self.XMLNS_NAMESPACE, self.XMLNS)] = [self.XMLNS, uri2]
      self.CurNodeNSDecl = []
    if attributes:
      if node.attributes is None:
        node.attributes = {}
      for i in range(0, len(attributes), 2):
        name = attributes[i]
        if ' ' in name:
          parts = name.split(' ')
          l = len(parts)
          if l == 3:
            uri2, localname, prefix = parts
            localname = self.intern(localname, localname)
            if uri2 == uri:
              node.attributes[(XMLNode.EMPTY_NAMESPACE, localname)] = [localname, attributes[i + 1]]
            else:
              uri2 = self.intern(uri2, uri2)
              qname = prefix + ':' + localname
              qname = self.intern(qname, qname)
              node.attributes[(uri2, localname)] = [qname, attributes[i + 1]]
          elif l == 2:
            uri2, localname = parts
            localname = self.intern(localname, localname)
            node.attributes[(XMLNode.EMPTY_NAMESPACE, localname)] = [localname, attributes[i + 1]]
          else:
            raise
        else:
          node.attributes[(XMLNode.EMPTY_NAMESPACE, name)] = [name, attributes[i + 1]]

  def EndElementHandler(self, name):
    if self.CurText and not self.CurNode.childNodes:
      self.CurNode.childNodes.append(XMLText(self.CurText))
    self.CurText = ''
    self.CurNode = self.ParNodes.pop()

  def StartCdataSectionHandler(self):
    self.CurText = ''
    self.CDataSection = True

  def EndCdataSectionHandler(self):
    self.CDataSection = False

  def CharacterDataHandler(self, data):
    nodes = self.CurNode.childNodes
    if self.CDataSection:
      if nodes:
        if nodes[-1].nodeType == XMLNode.CDATA_SECTION_NODE:
          nodes[-1].data += data
          return
      self.CurNode.childNodes.append(XMLCDATASection(data))
    else:
      if nodes:
        if nodes[-1].nodeType == XMLNode.TEXT_NODE:
          nodes[-1].data += data
          return
      self.CurText += data
      if data.strip('\r\n\t '):
        self.CurNode.childNodes.append(XMLText(self.CurText))
        self.CurText = ''

  def StartNamespaceDeclHandler(self, prefix, uri):
    self.CurNodeNSDecl.append((prefix, uri))

  def EndNamespaceDeclHandler(self, prefix):
    pass

  def CommentHandler(self, data):
    self.CurText = ''
    self.CurNode.childNodes.append(XMLComment(data))

  def DefaultHandler(self, data):
    self.CurText = ''


class GCManager():

  def __init__(self):
    self.gcie = gc.isenabled()
    self.gcnd = 0
    self.gcl = threading.Lock()

  def disable(self):
    with self.gcl:
      if not self.gcnd:
        gc.disable()
      self.gcnd += 1

  def restore(self):
    with self.gcl:
      self.gcnd -= 1
      if not self.gcnd and self.gcie:
        gc.enable()

GCMan = GCManager()


class WGS84Track(WGS84WebMercator):

  def __init__(self, unlink_lock=None):
    self.ULock = unlink_lock
    self._tracks = [None, None, None]
    self.TrkId = None
    self.Name = None
    self.Color = None
    self.Wpts = None
    self.Pts = None
    self.WebMercatorWpts = None
    self.WebMercatorPts = None
    self.intern_dict = None
    self.intern = None
    if not hasattr(self, 'log'):
      self.log = partial(log, 'track')
      self.log(2, 'init')

  def _unlink(self, track):
    if self.ULock is not None:
      self.ULock.acquire()
      self.ULock.release()
    try:
      track.unlink()
    except:
      pass

  def unlink(self, track):
    if track is not None:
      if self.ULock is None:
        self._unlink(track)
      else:
        tu = threading.Thread(target=self._unlink, args=(track,))
        tu.start()

  @property
  def OTrack(self):
    return self._tracks[0]

  @OTrack.setter
  def OTrack(self, value):
    self._tracks[0] = value

  @OTrack.deleter
  def OTrack(self):
    if self._tracks[0] != self._tracks[1] and self._tracks[0] != self._tracks[2]:
      self.unlink(self._tracks[0])
    self._tracks[0] = None

  @property
  def STrack(self):
    return self._tracks[1]

  @STrack.setter
  def STrack(self, value):
    self._tracks[1] = value

  @STrack.deleter
  def STrack(self):
    if self._tracks[1] != self._tracks[0] and self._tracks[1] != self._tracks[2]:
      self.unlink(self._tracks[1])
    self._tracks[1] = None

  @property
  def Track(self):
    return self._tracks[2]

  @Track.setter
  def Track(self, value):
    self._tracks[2] = value

  @Track.deleter
  def Track(self):
    if self._tracks[2] != self._tracks[0] and self._tracks[2] != self._tracks[1]:
      self.unlink(self._tracks[2])
    self._tracks[2] = None

  def _XMLNewNode(self, localname, uri, prefix=None):
    return XMLElement(self.intern(prefix + ':' + localname, prefix + ':' + localname) if prefix is not None else self.intern(localname, localname), self.intern(uri, uri), self.intern(localname, localname))

  def ProcessGPX(self, mode='a'):
    r = self.Track.documentElement
    rns = r.namespaceURI
    tnode = (XMLNode.TEXT_NODE, XMLNode.CDATA_SECTION_NODE)
    alat = (XMLNode.EMPTY_NAMESPACE, 'lat')
    alon = (XMLNode.EMPTY_NAMESPACE, 'lon')
    try:
      trk = r.getChildren('trk')[self.TrkId]
    except:
      if mode != 'a' or self.TrkId > 0:
        return False
      trk = self._XMLNewNode('trk', rns, r.prefix)
      r.appendChild(trk)
    if mode != 'e':
      regexp_d=  '^([0-9]{4}-(?:(?:01|03|05|07|08|10|12)-(?:0[1-9]|[12][0-9]|3[01])|(?:04|06|09|11)-(?:0[1-9]|[12][0-9]|30)|02-(?:0[1-9]|1[0-9]|2[0-8]))|(?:(?:[02468][048]|[13579][26])00|[0-9][0-9](?:0[48]|[2468][048]|[13579][26]))-02-29)'
      regexp_t =  '(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](?:\\.[0-9]{3})?(?:[Zz]|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])?$'
      regexp_dt = re.compile('[^\\r\\n]'.join((regexp_d, regexp_t))).match
      regexp_st = re.compile('^$').match
    if mode in ('a', 'w'):
      pti = 0
      try:
        self.Wpts = []
        for pt in r.getChildren('wpt'):
          pele = ptime = pname = ''
          for c in pt.childNodes:
            if c.namespaceURI == rns:
              cln = c.localName
              if cln == 'ele':
                for cc in c.childNodes:
                  if cc.nodeType in tnode:
                    pele += cc.data
              elif cln == 'time':
                for cc in c.childNodes:
                  if cc.nodeType in tnode:
                    ptime += cc.data
              elif cln == 'name':
                for cc in c.childNodes:
                  if cc.nodeType in tnode:
                    pname += cc.data
          plat = float(pt.attributes[alat][1])
          plon = float(pt.attributes[alon][1])
          ch = plat * plon * 0
          if pele.strip():
            pele = float(pele)
            ch *= pele
          else:
            pele = ''
          if ch:
              raise
          ptime = ptime.strip()
          if ptime:
            if not regexp_st(ptime):
              regexp_st = re.compile(('^%s[^\\r\\n]%s') % (regexp_dt(ptime).group(1), regexp_t)).match
          self.Wpts.append((pti, (plat, plon, pele, ptime, ' '.join(pname.splitlines()))))
          pti += 1
      except:
        self.log(1, 'perrorw', pti + 1)
        return False
    if mode in ('a', 't', 'e'):
      self.Name = ' '.join(trk.getChildrenText('name').splitlines())
      self.Color = ''
      ext = trk.getChildren('extensions')
      try:
        for e in ext:
          c = e.getChildren('color', self.MT_NAMESPACE)
          if c:
            self.Color = '#' + hex(int(c[0].getText()) % (1 << 24))[2:][-6:].rjust(6, '0').upper()
            break
      except:
        pass
      if not self.Color:
        try:
          for e in ext:
            l = e.getChildren('line', '*')
            if l:
              c = l[0].getChildren('color', '*')
              if c:
                self.Color = '#' + hex(int(c[0].getText(), 16))[2:][-6:].rjust(6, '0').upper()
                break
        except:
          pass
    if mode in ('a', 't'):
      self.Pts = []
      pti = 0
      try:
        for seg in trk.getChildren('trkseg'):
          pts = []
          for pt in seg.getChildren('trkpt'):
            pele = palt = ptime = ''
            for c in pt.childNodes:
              if c.namespaceURI == rns:
                cln = c.localName
                if cln == 'ele':
                  for cc in c.childNodes:
                    if cc.nodeType in tnode:
                      pele += cc.data
                elif cln == 'time':
                  for cc in c.childNodes:
                    if cc.nodeType in tnode:
                      ptime += cc.data
                elif cln == 'extensions':
                  for cc in c.childNodes:
                    if cc.namespaceURI == self.MT_NAMESPACE and cc.localName == 'ele_alt':
                      for ccc in cc.childNodes:
                        if ccc.nodeType in tnode:
                          palt += ccc.data
            plat = float(pt.attributes[alat][1])
            plon = float(pt.attributes[alon][1])
            ch = plat * plon * 0
            if pele.strip():
              pele = float(pele)
              ch *= pele
            else:
              pele = ''
            if palt.strip():
              palt = float(palt)
              ch *= palt
            else:
              palt = ''
            if ch:
              raise
            ptime = ptime.strip()
            if ptime:
              if not regexp_st(ptime):
                regexp_st = re.compile(('^%s[^\\r\\n]%s') % (regexp_dt(ptime).group(1), regexp_t)).match
            pts.append((pti, (plat, plon, pele, palt, ptime)))
            pti += 1
          self.Pts.append(pts)
        self.Pts = self.Pts or [[]]
      except:
        self.log(1, 'perrorp', len(self.Pts) + 1, len(pts) + 1)
        return False
    return True

  def _intern(self):
    self.intern = self.intern_dict.setdefault
    self.XMLNS = self.intern('xmlns', 'xmlns')
    self.XMLNS_NAMESPACE = self.intern(XMLNode.XMLNS_NAMESPACE, XMLNode.XMLNS_NAMESPACE)
    self.GPX_NAMESPACE = self.intern('http://www.topografix.com/GPX/1/1', 'http://www.topografix.com/GPX/1/1')
    self.GPXSTYLE_NAMESPACE = self.intern('http://www.topografix.com/GPX/gpx_style/0/2', 'http://www.topografix.com/GPX/gpx_style/0/2')
    self.MT = self.intern('mytrails', 'mytrails')
    self.XMLNS_MT = self.intern('xmlns:mytrails', 'xmlns:mytrails')
    self.MT_NAMESPACE = self.intern('http://www.frogsparks.com/mytrails', 'http://www.frogsparks.com/mytrails')

  def LoadGPX(self, uri, trkid=None, source=None, builder=None):
    if self.Track is not None:
      return False
    self.log(1, 'load', uri + ((' <%s>' % trkid) if trkid is not None else ''))
    GCMan.disable()
    try:
      if source is not None and source is not self:
        self._tracks = source._tracks
        self.intern_dict = source.intern_dict
        self.Wpts = source.Wpts
      else:
        if '://' in uri:
          rep = HTTPRequest(uri, 'GET')
          if rep.code != '200':
            raise
          track = rep.body
        else:
          try:
            f = open(uri, 'rb')
            track = f.read()
          except:
            if trkid:
              raise
            track = b'<?xml version="1.0" encoding="UTF-8"?><gpx version="1.1" creator="GPXTweaker" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:mytrails="http://www.frogsparks.com/mytrails" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.topografix.com/GPX/gpx_style/0/2 http://www.topografix.com/GPX/gpx_style/0/2/gpx_style.xsd"></gpx>'
            self.log(0, 'new', uri)
          finally:
            try:
              f.close()
            except:
              pass
        if not builder:
          builder = ExpatGPXBuilder()
        self.Track = builder.Parse(track)
        if self.Track is None:
          raise
        self.intern_dict = builder.intern_dict
      self._intern()
    except:
      self.__init__()
      self.log(0, 'oerror', uri, color=31)
      GCMan.restore()
      return False
    self.TrkId = trkid or 0
    try:
      if not self.ProcessGPX('a' if source is None or source is self else 't'):
        raise
    except:
      if source is None:
        del self.Track
      if source is not self:
        self.__init__()
      else:
        self.OTrack = self.STrack = self.Track
      self.log(0, 'lerror', uri + ((' <%s>' % trkid) if trkid is not None else ''), color=31)
      GCMan.restore()
      return False
    if source is None or source is self:
      self.OTrack = self.STrack = self.Track
    self.WebMercatorWpts = None
    self.WebMercatorPts = None
    self.log(0, 'loaded', uri + ((' <%s>' % trkid) if trkid is not None else ''), self.Name, len(self.Wpts), len(self.Pts), sum(len(seg) for seg in self.Pts), color=32)
    GCMan.restore()
    return True

  def BuildWebMercator(self):
    if self.Wpts:
      self.WebMercatorWpts = [(pt[0], WGS84Track.WGS84toWebMercator(*pt[1][0:2])) for pt in self.Wpts]
    else:
      self.WebMercatorWpts = []
    if self.Pts:
      self.WebMercatorPts = [[(pt[0], WGS84Track.WGS84toWebMercator(*pt[1][0:2])) for pt in seg] for seg in self.Pts]
    else:
      self.WebMercatorPts = []
    return True

  def BackupGPX(self, uri):
    try:
      uri_pre = uri.rsplit('.', 1)[0]
      if not os.path.exists(uri_pre + ' - original.gpx'):
        os.rename(uri, uri_pre + ' - original.gpx')
      else:
        if os.path.exists(uri_pre + ' - backup.gpx'):
          os.remove(uri_pre + ' - backup.gpx')
        os.rename(uri, uri_pre + ' - backup.gpx')
    except:
      return False
    return True

  def SaveGPX(self, uri, backup=True):
    self.log(1, 'save', uri)
    if self.Track:
      try:
        if backup and os.path.exists(uri):
          if not self.BackupGPX(uri):
            raise
        f = open(uri, 'wb')
        f.write(self.Track.toxml())
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
    del self.STrack
    self.STrack = self.Track
    self.log(0, 'saved', uri)
    return True

  def _XMLUpdateAttribute(self, node, name, value):
    node.setAttribute(self.intern(name, name), value)

  def _XMLUpdateChildNode(self, node, localname, child, predecessors='*', uri=None):
    no = None
    cn = node.getChildren(localname, uri if uri is not None else node.namespaceURI)
    if cn:
      no = cn[0]
      for n in cn[1:]:
        node.removeChild(n).unlink()
    if child is not None:
      if no is not None:
        node.replaceChild(child, no).unlink()
        return
      elif predecessors == '*':
        node.appendChild(child)
        return
      elif isinstance(predecessors, (list, tuple)):
        for e in predecessors:
          cn = node.getChildren(e)
          if cn:
            no = cn[-1]
            break
      node.insertAfter(child, no)
    elif no is not None:
      node.removeChild(no).unlink()

  def _XMLUpdateChildNodeText(self, node, localname, uri, prefix, text, predecessors='*', cdata=False):
    if text:
      if cdata:
        t = XMLCDATASection(text)
      else:
        t = XMLText(text)
      child = self._XMLNewNode(localname, uri, prefix)
      child.appendChild(t)
    else:
      child = None
    self._XMLUpdateChildNode(node, localname, child, predecessors, uri)

  def UpdateGPX(self, msg, uri=None, backup=True):
    GCMan.disable()
    del self.Track
    self.Track = self.OTrack.cloneNode()
    r = self.Track.documentElement
    trk = r.getChildren('trk')[self.TrkId]
    trkns = trk.namespaceURI
    trkp = trk.prefix
    mt = r.hasAttribute(self.MT, self.XMLNS_NAMESPACE)
    try:
      if '\r\n=\r\n' not in msg:
        msgp = msg.split('=', 1)
        if msgp[0][-5:] == 'color':
          if not mt:
            r.setAttribute(self.MT, self.MT_NAMESPACE, self.XMLNS_NAMESPACE, self.XMLNS_MT)
          ext = trk.getChildren('extensions')
          l = []
          if not ext:
            e = self._XMLNewNode('extensions', trkns, trkp)
            e_ = e
            s = trk.getChildren('trkseg')
            if s:
              trk.insertBefore(e, s[0])
            else:
              trk.appendChild(e)
          else:
            e = ext[0]
            e_ = ext[0]
            for ex in ext:
              if ex.getChildren('color', self.MT_NAMESPACE):
                e = ex
                break
            for ex in ext:
              l = ex.getChildren('line', '*')
              if l:
                e_ = ex
                if l[0].getChildren('color', '*'):
                  break
          a = self._XMLNewNode('color', self.MT_NAMESPACE, self.MT)
          t = XMLText(str(int(msgp[1].lstrip('#'), 16) - (1 << 24)))
          a.appendChild(t)
          self._XMLUpdateChildNode(e, 'color', a, '*', self.MT_NAMESPACE)
          if l:
            a = l[0]
            if not a.namespaceURI or a.namespaceURI == self.GPX_NAMESPACE:
              a.setAttribute(self.XMLNS, self.GPXSTYLE_NAMESPACE, self.XMLNS_NAMESPACE, self.XMLNS)
          else:
            a = self._XMLNewNode('line', self.GPXSTYLE_NAMESPACE)
            a.setAttribute(self.XMLNS, self.GPXSTYLE_NAMESPACE, self.XMLNS_NAMESPACE, self.XMLNS)
            e_.appendChild(a)
          b = a.getChildren('color', '*')
          if b:
            b = b[0]
          else:
            b = self._XMLNewNode('color', self.GPXSTYLE_NAMESPACE)
            a.appendChild(b)
          t = XMLText(msgp[1].lstrip('#'))
          while b.hasChildNodes():
            b.removeChild(b.firstChild).unlink()
          b.appendChild(t)
        elif msgp[0][-4:] == 'name':
          self._XMLUpdateChildNodeText(trk, 'name', trkns, trkp, ' '.join(msgp[1].splitlines()), None, True)
        else:
          raise
        if not self.ProcessGPX('e'):
          raise
      else:
        msgp = msg.split('=\r\n')
        nmsg = msgp[0].split('\r\n')[:-1]
        wpmsg = msgp[1].split('\r\n')[:-1]
        smsg = msgp[2].split('-\r\n')[1:]
        wpts = r.removeChildren('wpt')
        segs = trk.removeChildren('trkseg')
        pts = [pt for seg in segs for pt in seg.removeChildren('trkpt')]
        self._XMLUpdateChildNodeText(trk, 'name', trkns, trkp, ' '.join((nmsg or [''])[0].splitlines()), None, True)
        wpn = []
        for wp in wpmsg:
          if '&' in wp:
            v = wp.split('&')
            if int(v[0]) < len(wpts):
              nwp = wpts[int(v[0])]
              wpts[int(v[0])] = None
            else:
              nwp = self._XMLNewNode('wpt', trkns, trkp)
            self._XMLUpdateAttribute(nwp, 'lat', v[1])
            self._XMLUpdateAttribute(nwp, 'lon', v[2])
            self._XMLUpdateChildNodeText(nwp, 'ele', trkns, trkp, v[3], None)
            self._XMLUpdateChildNodeText(nwp, 'time', trkns, trkp, urllib.parse.unquote(v[4]), ('ele',))
            self._XMLUpdateChildNodeText(nwp, 'name', trkns, trkp, ' '.join(urllib.parse.unquote(v[5]).splitlines()), ('geoidheight', 'magvar', 'time', 'ele') , True)
          else:
            nwp = wpts[int(wp)]
            wpts[int(wp)] = None
          wpn.append(nwp)
        r.insertAfter(wpn, (r.getChildren('metadata') or [None])[-1])
        for wp in wpts:
          if wp is not None:
            wp.unlink()
        for s in segs:
          s.unlink()
        for s in smsg:
          ns = self._XMLNewNode('trkseg', trkns, trkp)
          pmsg = s.split('\r\n')[:-1]
          for p in pmsg:
            if '&' in p:
              v = p.split('&')
              if int(v[0]) < len(pts):
                np = pts[int(v[0])]
                pts[int(v[0])] = None
              else:
                np = self._XMLNewNode('trkpt', trkns, trkp)
              self._XMLUpdateAttribute(np, 'lat', v[1])
              self._XMLUpdateAttribute(np, 'lon', v[2])
              self._XMLUpdateChildNodeText(np, 'ele', trkns, trkp, v[3], None)
              if v[4]:
                if not mt:
                  r.setAttribute(self.MT, self.MT_NAMESPACE, self.XMLNS_NAMESPACE, self.XMLNS_MT)
                  mt = True
                ext = np.getChildren('extensions')
                if not ext:
                  e = self._XMLNewNode('extensions', trkns, trkp)
                  np.appendChild(e)
                else:
                  e = ext[0]
                  for ex in ext:
                    if ex.getChildren('ele_alt', self.MT_NAMESPACE):
                      e = ex
                      break
                a = self._XMLNewNode('ele_alt', self.MT_NAMESPACE, self.MT)
                t = XMLText(v[4])
                a.appendChild(t)
                self._XMLUpdateChildNode(e, 'ele_alt', a, '*', self.MT_NAMESPACE)
              elif mt:
                for ex in np.getChildren('extensions'):
                  self._XMLUpdateChildNode(ex, 'ele_alt', None, '*', self.MT_NAMESPACE)
              self._XMLUpdateChildNodeText(np, 'time', trkns, trkp, urllib.parse.unquote(v[5]), ('ele',))
            else:
              np = pts[int(p)]
              pts[int(p)] = None
            ns.appendChild(np)
          trk.appendChild(ns)
        for p in pts:
          if p is not None:
            p.unlink()
        if not self.ProcessGPX('a'):
          raise
      if uri:
        if not self.SaveGPX(uri, backup):
          raise
    except:
      del self.Track
      self.Track = self.STrack
      self.ProcessGPX('a' if '\r\n=\r\n' in msg else 'e')
      return False
    finally:
      GCMan.restore()
    self.WebMercatorWpts = None
    self.WebMercatorPts = None
    return True

  def DetachFromGPX(self, others, uri=None, backup=True):
    GCMan.disable()
    _tracks = self._tracks
    trkid = self.TrkId
    self.Track = self.OTrack.cloneNode()
    self._tracks = [self.OTrack, None, self.OTrack.cloneNode()]
    r = self.Track.documentElement
    nuri = None
    try:
      self._XMLUpdateChildNode(r, 'trk', r.removeChild(r.getChildren('trk')[trkid]))
      _r = _tracks[2].documentElement
      _r.removeChild(_r.getChildren('trk')[trkid]).unlink()
      if uri:
        nuri = uri.rsplit('.', 1)[0] + ' - trk.gpx'
        suf = 0
        while os.path.exists(nuri):
          suf += 1
          nuri = uri.rsplit('.', 1)[0] + ' - trk (%d).gpx' % suf
        if not self.SaveGPX(nuri, False):
          raise
    except:
      del self.Track
      self._tracks = _tracks
      del self.Track
      self.Track = self.OTrack
      GCMan.restore()
      return False
    self.TrkId = 0
    try:
      for tr in others:
        if uri:
          try:
            if not tr.SaveGPX(uri, backup):
              raise
          except:
            del tr.Track
            tr.Track = tr.OTrack
            raise
          uri = None
        if tr.TrkId > trkid:
          tr.TrkId -= 1
    except:
      pass
    GCMan.restore()
    return nuri or True

  def AppendToGPX(self, track, others, mode='s', uri=None, backup=True):
    GCMan.disable()
    trkid = self.TrkId
    del self.Track
    self.Track = self.OTrack.cloneNode()
    r = self.Track.documentElement
    trk = r.getChildren('trk')[trkid]
    try:
      _r = track.Track.documentElement
      _wpt = _r.getChildren('wpt')
      _w = len(_wpt) > 0
      if mode == 's':
        _trk = _r.getChildren('trk')[track.TrkId]
      else:
        _trk = _r.getChildren('trk')[track.TrkId].cloneNode()
      for _ln, _v in _r.getNameSpaces():
        if _w:
          u = r.getAttribute(_ln, self.XMLNS_NAMESPACE)
          if u is None:
            r.setAttribute(_ln, self.intern(_v[1], _v[1]), self.XMLNS_NAMESPACE, _v[0])
          elif u != _v[1]:
            raise
        if _trk.getAttribute(_ln, self.XMLNS_NAMESPACE) is not None:
            continue
        if mode == 's':
          u = trk.getAttribute(_ln, self.XMLNS_NAMESPACE)
          if u is None:
            if not _w:
              u = r.getAttribute(_ln, self.XMLNS_NAMESPACE)
              if u is None:
                r.setAttribute(_ln, self.intern(_v[1], _v[1]), self.XMLNS_NAMESPACE, _v[0])
              elif u != _v[1]:
                raise
          elif u != _v[1]:
            raise
        elif not _w:
          u = r.getAttribute(_ln, self.XMLNS_NAMESPACE)
          if u is None:
            r.setAttribute(_ln, self.intern(_v[1], _v[1]), self.XMLNS_NAMESPACE, _v[0])
          elif u != _v[1]:
            _trk.setAttribute(_ln, self.intern(_v[1], _v[1]), self.XMLNS_NAMESPACE, _v[0])
      if mode == 's':
        for _ln, _v in _trk.getNameSpaces():
          u = trk.getAttribute(_ln, self.XMLNS_NAMESPACE)
          if u is None:
            u = r.getAttribute(_ln, self.XMLNS_NAMESPACE)
            if u is None:
              trk.setAttribute(_ln, self.intern(_v[1], _v[1]), self.XMLNS_NAMESPACE, _v[0])
            elif u != _v[1]:
              raise
          elif u != _v[1]:
            raise
      no = None
      if mode != 'tb':
        cn = r.getChildren('wpt')
        if cn:
          no = cn[-1]
      if mode == 'tb' or no is None:
        cn = r.getChildren('metadata')
        if cn:
          no = cn[-1]
      r.insertAfter([n.cloneNode() for n in _wpt], no)
      if mode == 'tb':
        r.insertBefore(_trk, trk)
      elif mode == 'ta':
        r.insertAfter(_trk, trk)
      else:
        for seg in _trk.getChildren('trkseg'):
          trk.appendChild(seg.cloneNode())
      if mode == 's':
        self.ProcessGPX('a')
      else:
        self.ProcessGPX('w')
      if uri:
        if not self.SaveGPX(uri, backup):
          raise
    except:
      del self.Track
      self.Track = self.OTrack
      if mode == 's':
        self.ProcessGPX('a')
      else:
        self.ProcessGPX('w')
      GCMan.restore()
      return False
    for s in track.intern_dict.items():
      self.intern(*s)
    if mode in ('ta', 'tb'):
      track._tracks = self._tracks
      track.TrkId = trkid if mode == 'tb' else trkid + 1
      track.intern_dict = self.intern_dict
      track.ProcessGPX('w')
      if mode == 'tb':
        self.TrkId += 1
    for tr in others:
      if mode in ('ta', 'tb'):
        if tr.TrkId >= trkid:
          tr.TrkId += 1
      tr.ProcessGPX('w')
    GCMan.restore()
    return True


class WebMapping():

  WM_GOOGLE_MAPS = {'alias': 'GOOGLE_MAPS', 'source': 'https://www.google.com/maps/search/?api=1&query={lat},{lon}'}
  WM_GOOGLE_MAPS_FR = {'alias': 'GOOGLE_MAPS_FR', 'source': 'https://www.google.fr/maps/search/?api=1&query={lat},{lon}'}
  WM_BING_MAPS = {'alias': 'BING_MAPS', 'source': 'https://www.bing.com/maps?where1={lat},{lon}'}
  WM_MAPPY = {'alias': 'MAPPY', 'source': 'https://fr.mappy.com/plan#/{lat},{lon}'}

  @classmethod
  def WMAlias(cls, name):
    if hasattr(cls, 'WM_' + name):
      return dict(getattr(cls, 'WM_' + name))
    else:
      return None


class GeotaggedMedia():

  MP4_EPOCH = 2082844800

  def __init__(self, folders, photos=True, videos=True, box=None):
    self.Folders = folders
    self.Photos = photos
    self.Videos = videos
    self.Box = box
    self.DLock = threading.Lock()
    self.Data = None
    self.Uris = None
    self.log = partial(log, 'geomedia')

  @staticmethod
  def _read_jpg_data(photo):
    try:
      f = open(photo, 'rb')
    except:
      return None
    try:
      if f.read(2) != b'\xff\xd8':
        raise
      t = f.read(2)
      if t == b'\xff\xe0':
        l = struct.unpack('!H', f.read(2))[0]
        f.seek(l - 2, os.SEEK_CUR)
        t = f.read(2)
      if t != b'\xff\xe1':
        raise
      l = struct.unpack('!H', f.read(2))[0]
      if f.read(6) != b'Exif\x00\x00':
        raise
      ref = f.tell()
      ba = {b'MM': '>', b'II': '<'}.get(f.read(2))
      if ba is None:
        raise
      if f.read(2) != (b'\x00\x2a' if ba == '>' else b'\x2a\x00') :
        raise
      f.seek(struct.unpack(ba + 'I', f.read(4))[0] - 8, os.SEEK_CUR)
      ne = struct.unpack(ba + 'H', f.read(2))[0]
      if ne == 0:
        raise
      gps = None
      sifd = None
      orientation = 1
      dimensions = [None] * 2
      for i in range(ne):
        e = f.read(12)
        t = struct.unpack(ba + 'H', e[0:2])[0]
        if t == 0x8825:
          if struct.unpack(ba + 'H', e[2:4])[0] != 4 or struct.unpack(ba + 'I', e[4:8])[0] != 1:
            raise
          gps = ref + struct.unpack(ba + 'I', e[8:12])[0]
        elif t == 0x8769:
          if struct.unpack(ba + 'H', e[2:4])[0] != 4 or struct.unpack(ba + 'I', e[4:8])[0] != 1:
            raise
          sifd = ref + struct.unpack(ba + 'I', e[8:12])[0]
        elif t == 0x0112:
          if struct.unpack(ba + 'H', e[2:4])[0] != 3 or struct.unpack(ba + 'I', e[4:8])[0] != 1:
            continue
          orientation = struct.unpack(ba + 'H', e[8:10])[0]
        elif t in (0x0100, 0x0101):
          df = {3:'H', 4:'I'}.get(struct.unpack(ba + 'H', e[2:4])[0])
          if df is None or struct.unpack(ba + 'I', e[4:8])[0] != 1:
            raise
          dimensions[t - 0x0100] = struct.unpack(ba + df, e[8:(10 if df == 'H' else 12)])[0]
      if gps is None or sifd is None:
        raise
      f.seek(gps)
      ne = struct.unpack(ba + 'H', f.read(2))[0]
      if ne == 0:
        raise
      lref = [None] * 2
      lpos = [None] * 2
      for i in range(ne):
        e = f.read(12)
        t = struct.unpack(ba + 'H', e[0:2])[0]
        if t in (0x0001, 0x0003):
          if struct.unpack(ba + 'H', e[2:4])[0] != 2 or struct.unpack(ba + 'I', e[4:8])[0] != 2:
            raise
          lref[(t - 1) // 2] = e[8:10].strip(b'\x00').upper().decode()
        elif t in (0x0002, 0x0004):
          if struct.unpack(ba + 'H', e[2:4])[0] != 5 or struct.unpack(ba + 'I', e[4:8])[0] != 3:
            raise
          lpos[(t - 2) // 2] = struct.unpack(ba + 'I', e[8:12])[0] + ref
      if None in lref or None in lpos:
        raise
      f.seek(lpos[0])
      l = struct.unpack(ba + 'IIIIII', f.read(24))
      lat = round((-1 if lref[0] == 'S' else 1) * sum(n / d * u for n, d, u in zip(l[::2], l[1::2], (3600, 60, 1))), 3) / 3600
      if lat < -90 or lat > 90:
        raise
      f.seek(lpos[1])
      l = struct.unpack(ba + 'IIIIII', f.read(24))
      lon = 180 - (180 - (round((-1 if lref[1] == 'W' else 1) * sum(n / d * u for n, d, u in zip(l[::2], l[1::2], (3600, 60, 1))), 3)) / 3600 ) % 360
      f.seek(sifd)
      ne = struct.unpack(ba + 'H', f.read(2))[0]
      if ne == 0:
        raise
      dtpos = None
      for i in range(ne):
        e = f.read(12)
        t = struct.unpack(ba + 'H', e[0:2])[0]
        if t in (0xa002, 0xa003):
          df = {3:'H', 4:'I'}.get(struct.unpack(ba + 'H', e[2:4])[0])
          if df is None or struct.unpack(ba + 'I', e[4:8])[0] != 1:
            raise
          dimensions[t - 0xa002] = struct.unpack(ba + df, e[8:(10 if df == 'H' else 12)])[0]
        elif t == 0x9003 or (t == 0x9004 and dtpos is None):
          if struct.unpack(ba + 'H', e[2:4])[0] != 2 or struct.unpack(ba + 'I', e[4:8])[0] != 20:
            continue
          dtpos = struct.unpack(ba + 'I', e[8:12])[0] + ref
      if None in dimensions or 0 in dimensions:
        raise
      datetime = ''
      if dtpos is not None:
        try:
          f.seek(dtpos)
          datetime = time.strftime('%x %X', time.strptime(f.read(20).strip(b'\x00').decode(), '%Y:%m:%d %H:%M:%S'))
        except:
          pass
    except:
      return None
    finally:
      try:
        f.close()
      except:
        pass
    return *WGS84WebMercator.WGS84toWebMercator(lat, lon), (dimensions[1] / dimensions[0] if orientation in (6, 8) else dimensions[0] / dimensions[1]), datetime

  @staticmethod
  def _read_mp4_data(video):
    try:
      f = open(video, 'rb')
    except:
      return None
    try:
      l = struct.unpack('>I', f.read(4))[0]
      if f.read(4) != b'ftyp':
        raise
      f.seek(l - 8, os.SEEK_CUR)
      t = b''
      l = 0
      while t != b'moov':
        f.seek(l, os.SEEK_CUR)
        l = f.read(4)
        if l == b'':
          break
        l = struct.unpack('>I', l)[0]
        t = f.read(4)
        if l == 1:
          l = struct.unpack('>Q', f.read(8))[0] - 16
        else:
          l -= 8
      if t != b'moov':
        raise
      udtas = []
      mvhd = None
      traks = []
      t = b''
      e = 0
      s = l
      l = 0
      while e < s:
        f.seek(l, os.SEEK_CUR)
        l = struct.unpack('>I', f.read(4))[0]
        e += l
        t = f.read(4)
        if l == 1:
          l = struct.unpack('>Q', f.read(8))[0] - 16
        else:
          l -= 8
        if t == b'udta':
          udtas.append((f.tell(), l))
        elif t == b'mvhd':
          if l < 8:
            raise
          mvhd = (f.tell(), l)
        elif t == b'trak':
          traks.append((f.tell(), l))
      if not udtas or mvhd is None or not traks:
        raise
      gps = None
      for udta in udtas:
        t = b''
        e = 0
        s = udta[1]
        l = 0
        f.seek(udta[0])
        while t != b'\xa9xyz' and e < s:
          f.seek(l, os.SEEK_CUR)
          l = struct.unpack('>I', f.read(4))[0]
          e += l
          t = f.read(4)
          if l == 1:
            l = struct.unpack('>Q', f.read(8))[0] - 16
          else:
            l -= 8
        if t == b'\xa9xyz':
          l = struct.unpack('>H', f.read(2))[0]
          f.seek(2, os.SEEK_CUR)
          if l % 2 == 0 and l >= 8:
            gps = f.read(l)
        if gps is not None:
          break
      if gps is None:
        raise
      c = gps.find(b'+', 1)
      if c < 0:
        c = gps.find(b'-')
      if c < 0:
        raise
      lat = gps[0:c]
      d = lat.find(b'.')
      if d == 3:
        lat = float(lat)
      elif d == 5:
        lat = float(lat[0:1] + b'1') * (float(lat[1:3]) + float(lat[3:]) / 60)
      elif d == 7:
        lat = float(lat[0:1] + b'1') * (float(lat[1:3]) + float(lat[3:5]) / 60 + float(lat[5:]) / 3600)
      else:
        raise
      lon = gps[c:-1]
      d = lon.find(b'.')
      if d == 4:
        lon = float(lon)
      elif d == 6:
        lon = float(lon[0:1] + b'1') * (float(lon[1:4]) + float(lon[4:]) / 60)
      elif d == 8:
        lon = float(lon[0:1] + b'1') * (float(lon[1:4]) + float(lon[4:6]) / 60 + float(lon[6:]) / 3600)
      else:
        raise
      f.seek(mvhd[0] + 4)
      datetime = struct.unpack('>I', f.read(4))[0]
      if datetime:
        datetime = time.strftime('%x %X', time.localtime(struct.unpack('>I', f.read(4))[0] - GeotaggedMedia.MP4_EPOCH))
      else:
        datetime = ''
      matrix = None
      width = None
      height = None
      for trak in traks:
        t = b''
        e = 0
        s = trak[1]
        l = 0
        f.seek(trak[0])
        while t != b'tkhd' and e < s:
          f.seek(l, os.SEEK_CUR)
          l = struct.unpack('>I', f.read(4))[0]
          e += l
          t = f.read(4)
          if l == 1:
            l = struct.unpack('>Q', f.read(8))[0] - 16
          else:
            l -= 8
        if t == b'tkhd':
          if l < 84:
            raise
          f.seek(40, os.SEEK_CUR)
          matrix = f.read(36)
          if matrix[0:4] == b'\x00\x01\x00\x00':
            width = struct.unpack('>I', f.read(4))[0] >> 16
            height = struct.unpack('>I', f.read(4))[0] >> 16
          else:
            height = struct.unpack('>I', f.read(4))[0] >> 16
            width = struct.unpack('>I', f.read(4))[0] >> 16
          if width and height:
            break
      if not width or not height:
        raise
    except:
      return None
    finally:
      try:
        f.close()
      except:
        pass
    return *WGS84WebMercator.WGS84toWebMercator(lat, lon), width / height, datetime

  def GetData(self):
    with self.DLock:
      if self.Data is None:
        self.Uris = []
        uris_p = []
        uris_v = []
        if self.Photos:
          uris_p = (os.path.join(e[0], f) for folder in self.Folders for e in os.walk(folder) for f in e[2] if f.rpartition('.')[2].lower() in ('jpg', 'jpeg'))
        if self.Videos:
          uris_v = (os.path.join(e[0], f) for folder in self.Folders for e in os.walk(folder) for f in e[2] if f.rpartition('.')[2].lower() == 'mp4')
        ti = time.time()
        gps_ar = []
        dt = []
        nm = []
        rd = self._read_jpg_data
        for uris in (uris_p, uris_v):
          for u in uris:
            data = rd(u)
            if data is not None:
              if self.Box is not None:
                if data[0] < self.Box[0] or data[0] > self.Box[2] or data[1] < self.Box[1] or data[1] > self.Box[3]:
                  self.log(2, 'mskipped', u)
                  continue
              self.Uris.append(u)
              gps_ar.extend(data[0:3])
              dt.append(data[3])
              self.log(2, 'mdloaded', u)
            else:
              self.log(1, 'mdlerror', u)
          nm.append(len(self.Uris) - sum(nm))
          rd = self._read_mp4_data
        if len(self.Uris) > 0:
          self.Data = (struct.pack('=%dd' % len(gps_ar), *gps_ar), ('|'.join(map('\r\n'.join, zip(self.Uris, dt)))).encode('utf-8'))
        else:
          self.Data = (b'', b'')
        self.log(0, 'mtloaded', *nm, time.time() - ti)
    return self.Data

  def Open(self, ind):
    try:
      u = 'Media%s' % ind
      u = self.Uris[ind]
      f = open(u, 'rb')
    except:
      self.log(1, 'moerror', u)
      return None, None
    self.log(2, 'mopened', u)
    return ('video/mp4' if u.rpartition('.')[2].lower() == 'mp4' else 'image/jpeg'), f


class ThreadedDualStackServer(socketserver.ThreadingTCPServer):

  allow_reuse_address = True
  block_on_close = False

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


class GPXTweakerRequestHandler(socketserver.BaseRequestHandler):

  def handle(self):
    def _send_err(e):
      resp_e = 'HTTP/1.1 %d %s\r\n' \
      'Content-Length: 0\r\n' \
      'Date: %s\r\n' \
      'Server: GPXTweaker\r\n' \
      'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
      '%s' \
      '\r\n' % (e, {501: 'Not Implemented', 404: 'Not found', 412: 'Precondition failed', 422: 'Unprocessable entity', 416: 'Range not satisfiable'}.get(e, 'Not found'), email.utils.formatdate(time.time(), usegmt=True), 'Access-Control-Allow-Origin: %s\r\n' % ('http://%s:%s' % (self.server.Interface.Ip, self.server.Interface.Ports[0])) if e == 404 else '')
      try:
        self.request.sendall(resp_e.encode('ISO-8859-1'))
        if e != 501:
          self.server.Interface.log(2, {404: 'rnfound', 412: 'rbad', 422: 'rfailed', 416: 'rfailed'}.get(e, 'rnfound'), req.method, req.path)
      except:
        self.server.Interface.log(2, 'rerror', req.method, req.path)
    def _send_err_ni():
      _send_err(501)
    def _send_err_nf():
      _send_err(404)
    def _send_err_bad():
      _send_err(412)
    def _send_err_fail():
      _send_err(422)
    def _send_err_rns():
      _send_err(416)
    def _send_resp(btype, s=None):
      resp_200 = 'HTTP/1.1 200 OK\r\n' \
      'Content-Type: ##type##\r\n' \
      'Content-Length: ##len##\r\n' \
      'Date: %s\r\n' \
      'Server: GPXTweaker\r\n' \
      'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
      '%s' \
      'Access-Control-Allow-Origin: %s\r\n' \
      '\r\n' % (email.utils.formatdate(time.time(), usegmt=True), 'Accept-Ranges: bytes\r\n' if s is not None else '', 'http://%s:%s' % (self.server.Interface.Ip, self.server.Interface.Ports[0]))
      try:
        if req.method == 'GET' or req.method == 'POST':
          self.request.sendall(resp_200.replace('##type##', btype).replace('##len##', str(s or len(resp_body))).encode('ISO-8859-1') + resp_body)
        else:
          self.request.sendall(resp_200.replace('##type##', btype).replace('##len##', str(s or len(resp_body))).encode('ISO-8859-1'))
        self.server.Interface.log(2, 'response', req.method, req.path)
        return True
      except:
        self.server.Interface.log(2, 'rerror', req.method, req.path)
        return False
    def _send_resp_nc():
      resp_204 = 'HTTP/1.1 204 No content\r\n' \
      'Content-Length: 0\r\n' \
      'Date: %s\r\n' \
      'Server: GPXTweaker\r\n' \
      'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
      '\r\n' % email.utils.formatdate(time.time(), usegmt=True)
      try:
        self.request.sendall(resp_204.encode('ISO-8859-1'))
        self.server.Interface.log(2, 'response', req.method, req.path)
        return True
      except:
        self.server.Interface.log(2, 'rerror', req.method, req.path)
        return False
    def _send_resp_tr(loc):
      resp_307 = 'HTTP/1.1 307 Temporary Redirect\r\n' \
      'Content-Length: 0\r\n' \
      'Location: %s\r\n' \
      'Date: %s\r\n' \
      'Server: GPXTweaker\r\n' \
      'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
      '\r\n' % (loc, email.utils.formatdate(time.time(), usegmt=True))
      try:
        self.request.sendall(resp_307.encode('ISO-8859-1'))
        self.server.Interface.log(2, 'response', req.method, req.path)
        return True
      except:
        self.server.Interface.log(2, 'rerror', req.method, req.path)
        return False
    def _send_resp_pc(btype, rs, re, s):
      resp_206 = 'HTTP/1.1 206 Partial Content\r\n' \
      'Content-Type: ##type##\r\n' \
      'Content-Length: %d\r\n' \
      'Date: %s\r\n' \
      'Server: GPXTweaker\r\n' \
      'Cache-Control: no-cache, no-store, must-revalidate\r\n' \
      'Access-Control-Allow-Origin: %s\r\n' \
      'Accept-Ranges: bytes\r\n' \
      'Content-Range: bytes %d-%d/%d\r\n' \
      '\r\n' % (re - rs, email.utils.formatdate(time.time(), usegmt=True), 'http://%s:%s' % (self.server.Interface.Ip, self.server.Interface.Ports[0]), rs, re - 1, s)
      try:
        if req.method == 'GET' or req.method == 'POST':
          self.request.sendall(resp_206.replace('##type##', btype).encode('ISO-8859-1') + resp_body)
        else:
          self.request.sendall(resp_206.replace('##type##', btype).encode('ISO-8859-1'))
        self.server.Interface.log(2, 'response', req.method, req.path)
        return True
      except:
        self.server.Interface.log(2, 'rerror', req.method, req.path)
        return False
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
        req = HTTPMessage(self.request, max_length=1073741824)
        if req.expect_close:
          closed = True
        if not req.method:
          closed = True
          continue
        self.server.Interface.log(2, 'request', req.method, req.path)
        resp_body = b''
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
          if req.path.lower() == '/GPXTweaker.html'.lower():
            self.server.Interface.SLock.acquire()
            if not self.server.Interface.HTML:
              _send_err_nf()
              self.server.Interface.SLock.release()
              continue
            if self.server.Interface.SessionId is None:
              self.server.Interface.SessionId = str(uuid.uuid5(uuid.NAMESPACE_URL, self.server.Interface.Uri + str(time.time())))
              resp_body = self.server.Interface.HTML.replace('##SESSIONSTORE##', 'sessionStorage.setItem("active", "%s");\r\n      ' % self.server.Interface.SessionStoreValue).replace('##SESSIONSTOREVALUE##', self.server.Interface.SessionStoreValue).replace('##SESSIONID##', self.server.Interface.SessionId).encode('utf-8')
            else:
              resp_body = self.server.Interface.HTML.replace('##SESSIONSTORE##', '').replace('##SESSIONSTOREVALUE##', self.server.Interface.SessionStoreValue).replace('##SESSIONID##', self.server.Interface.SessionId).encode('utf-8')
            self.server.Interface.SLock.release()
            _send_resp('text/html; charset=utf-8')
          elif req.path.lower() == '/GPXExplorer.html'.lower():
            self.server.Interface.SLock.acquire()
            if self.server.Interface.HTMLExp is None:
              _send_err_nf()
              self.server.Interface.SLock.release()
              continue
            if self.server.Interface.HTMLExp == '':
              self.server.Interface.ExploreMode()
            self.server.Interface.HTML = None
            self.server.Interface.SLock.release()
            if not self.server.Interface.HTMLExp:
              _send_err_nf()
              continue
            self.server.Interface.PSessionId = None
            if self.server.Interface.SessionId is None:
              self.server.Interface.SessionId = str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time())))
              resp_body = self.server.Interface.HTMLExp.replace('##SESSIONSTORE##', 'sessionStorage.setItem("active", "%s");\r\n      ' % self.server.Interface.SessionStoreValue).replace('##SESSIONSTOREVALUE##', self.server.Interface.SessionStoreValue).replace('##SESSIONID##', self.server.Interface.SessionId).encode('utf-8')
            else:
              resp_body = self.server.Interface.HTMLExp.replace('##SESSIONSTORE##', '').replace('##SESSIONSTOREVALUE##', self.server.Interface.SessionStoreValue).replace('##SESSIONID##', self.server.Interface.SessionId).encode('utf-8')
            _send_resp('text/html; charset=utf-8')
          elif req.path.lower()[:13] == '/tiles/switch':
            if req.header('If-Match', '') not in (self.server.Interface.SessionId, self.server.Interface.PSessionId):
              _send_err_bad()
              continue
            self.server.Interface.TLock.acquire()
            q = urllib.parse.parse_qs(urllib.parse.urlsplit(req.path).query)
            if 'set' in q:
              try:
                rset = int(q['set'][0])
                if rset < 0 or len(self.server.Interface.TilesSets[rset][-1]) <= 1:
                  raise
                if not self.server.Interface.JSONTiles:
                  if (self.server.Interface.TilesSets[rset][1].get('format') == 'application/json') if isinstance(self.server.Interface.TilesSets[rset][1], dict) else any(self.server.Interface.TilesSets[tsos[0]][1].get('format') == 'application/json' for tsos in self.server.Interface.TilesSets[rset][1]):
                    raise
                resp_body = json.dumps({'tlevels': self.server.Interface.TilesSets[rset][-1]}).encode('utf-8')
                self.server.Interface.TilesSet = rset
                if self.server.Interface.JSONTiles:
                  self.server.Interface.JSONTiles.Unload()
                _send_resp('application/json; charset=utf-8')
              except:
                _send_err_fail()
            else:
              tsmt = isinstance(self.server.Interface.TilesSets[self.server.Interface.TilesSet][1], dict)
              tsj = self.server.Interface.TilesSets[self.server.Interface.TilesSet][1].get('format') == 'application/json' if tsmt else None
              l1 = 0
              if 'auto' in q:
                tl = self.server.Interface.TilesSets[self.server.Interface.TilesSet][-1]
                l1 = tl[0]
                q['matrix'] = [str(tl[l1][0])]
                try:
                  sm = float(q['auto'][0])
                  l1 = 1
                  l2 = 1
                  l3 = len(tl)
                  m = None
                  while True:
                    if tl[l2][0] != m:
                      if tsmt and not tsj:
                        r = self.server.Interface.Map.SetTilesProvider((self.server.Interface.TilesSet, str(tl[l2][0])), self.server.Interface.TilesSets[self.server.Interface.TilesSet][1], str(tl[l2][0]), **self.server.Interface.TilesSets[self.server.Interface.TilesSet][2])
                      elif tsmt:
                        r = self.server.Interface.Map.SetTilesProviders({(self.server.Interface.TilesSet, str(tl[l2][0])): self.server.Interface.TilesSets[self.server.Interface.TilesSet][1:3]})
                      else:
                        r = self.server.Interface.Map.SetTilesProviders({(tsos[0], tsos[2].get(str(tl[l2][0]), str(tl[l2][0]))): self.server.Interface.TilesSets[tsos[0]][1:3] for tsos in self.server.Interface.TilesSets[self.server.Interface.TilesSet][1]})
                      if not r:
                        l2 += 1
                        if l2 >= l3:
                          l3 = (l1 + l3) // 2
                          l2 = l3 - 1
                          if l2 <= l1:
                            break
                        continue
                      m = tl[l2][0]
                    z = tl[l2][1].partition('/')
                    z = float(z[0] or '1') / float(z[2] or '1')
                    if tsmt and not tsj:
                      s = self.server.Interface.Map.TilesInfos['scale'] / self.server.Interface.Map.CRS_MPU / z
                    elif tsmt:
                      s = self.server.Interface.TilesSets[self.server.Interface.TilesSet][1]['basescale'] / (2 ** tl[l2][0]) / self.server.Interface.Map.CRS_MPU / z
                    else:
                      s = next(self.server.Interface.Map.TilesInfos[(tsos[0], str(tl[l2][0]))]['scale'] for tsos in self.server.Interface.TilesSets[self.server.Interface.TilesSet][1] if str(tl[l2][0]) not in tsos[2]) / z
                    if sm < s:
                      l1 = l2
                    else:
                      l3 = l2
                    l2 = (l1 + l3) // 2
                    if l2 == l1:
                      break
                  q['matrix'] = [str(tl[l1][0])]
                except:
                  pass
              if tsmt and not tsj:
                if not self.server.Interface.Map.SetTilesProvider((self.server.Interface.TilesSet, q['matrix'][0]), self.server.Interface.TilesSets[self.server.Interface.TilesSet][1], q['matrix'][0], **self.server.Interface.TilesSets[self.server.Interface.TilesSet][2]):
                  _send_err_fail()
                else:
                  try:
                    resp_body = json.dumps({'layers': [{**{k: self.server.Interface.Map.TilesInfos[k] for k in ('matrix', 'topx', 'topy', 'width', 'height')}, 'ext': WebMercatorMap.MIME_DOTEXT.get(self.server.Interface.Map.TilesInfos.get('format'), '.img')}], 'scale': self.server.Interface.Map.TilesInfos['scale'] / self.server.Interface.Map.CRS_MPU, 'level': l1}).encode('utf-8')
                    _send_resp('application/json; charset=utf-8')
                  except:
                    _send_err_fail()
              elif tsmt:
                if not self.server.Interface.Map.SetTilesProviders({(self.server.Interface.TilesSet, q['matrix'][0]): self.server.Interface.TilesSets[self.server.Interface.TilesSet][1:3]}):
                  _send_err_fail()
                else:
                  try:
                    resp_body = json.dumps({'layers': [{**{k: self.server.Interface.TilesSets[self.server.Interface.TilesSet][1][k] for k in ('topx', 'topy', 'width', 'height')}, 'ext': '.json'}], 'matrix': q['matrix'][0], 'scale': self.server.Interface.TilesSets[self.server.Interface.TilesSet][1]['basescale'] / (2 ** int(q['matrix'][0])) / self.server.Interface.Map.CRS_MPU, 'level': l1}).encode('utf-8')
                    _send_resp('application/json; charset=utf-8')
                  except:
                    _send_err_fail()
              else:
                if not self.server.Interface.Map.SetTilesProviders({(tsos[0], tsos[2].get(q['matrix'][0], q['matrix'][0])): self.server.Interface.TilesSets[tsos[0]][1:3] for tsos in self.server.Interface.TilesSets[self.server.Interface.TilesSet][1]}):
                  _send_err_fail()
                else:
                  try:
                    bscale = next(self.server.Interface.Map.TilesInfos[(tsos[0], q['matrix'][0])]['scale'] for tsos in self.server.Interface.TilesSets[self.server.Interface.TilesSet][1] if q['matrix'][0] not in tsos[2])
                    resp_body = json.dumps({'layers': [{**{k: ti[k] for k in ('matrix', 'topx', 'topy')}, 'width': round(ti['width'] * ti['scale'] / bscale, 5), 'height': round(ti['height'] * ti['scale'] / bscale, 5), 'ext': WebMercatorMap.MIME_DOTEXT.get(ti.get('format', ''), '.img')} for t, tsos in enumerate(self.server.Interface.TilesSets[self.server.Interface.TilesSet][1]) for ti in (self.server.Interface.Map.TilesInfos[(tsos[0], tsos[2].get(q['matrix'][0], q['matrix'][0]))],)], 'scale': bscale / self.server.Interface.Map.CRS_MPU, 'level': l1}).encode('utf-8')
                    _send_resp('application/json; charset=utf-8')
                  except:
                    _send_err_fail()
            self.server.Interface.TLock.release()
          elif req.path.lower()[:12] == '/tiles/tile-':
            try:
              rid = self.server.Interface.Map.Tiles.Id
              if isinstance(rid, list):
                tid = req.path.lower()[12:].rsplit('?', 1)[-1].rsplit(',', 1)
                rid = (int(tid[0]), tid[1])
                ti = self.server.Interface.Map.Tiles.Infos[rid]
              else:
                if req.path.lower()[12:].split('?')[-1] != '%s,%s' % rid:
                  raise
                ti = self.server.Interface.Map.TilesInfos
              row, col = req.path.lower()[12:].split('.', 1)[0].split('-')
              resp_body = self.server.Interface.Map.Tiles[(rid, (int(row), int(col)))](20)
            except:
              _send_err_fail()
              continue
            if resp_body:
              _send_resp(ti.get('format'))
            else:
              _send_err_nf()
          elif req.path.lower()[:20] == '/jsontiles/maplibre_':
            if not self.server.Interface.Map.JSONTiles:
              _send_err_fail()
              continue
            resp_body = self.server.Interface.JSONTilesLib.get(req.path[20:], b'')
            if req.path.lower()[20:22] == 'js':
              uri = (self.server.Interface.JSONTilesJS[0], req.path[22:]) if not resp_body else ''
              ct = 'text/javascript'
            elif req.path.lower()[20:23] == 'css':
              uri = (self.server.Interface.JSONTilesCSS[0], req.path[23:]) if not resp_body else ''
              ct = 'text/css'
            else:
              _send_err_fail()
              continue
            try:
              f = None
              if not resp_body:
                if uri[0][:4].lower() == 'http':
                  uri = urllib.parse.urljoin(uri[0], uri[1], allow_fragments=False)
                  rep = HTTPRequest(uri)
                  if rep.code != '200':
                    raise
                  resp_body = rep.body
                else:
                  uri = os.path.join(uri[0], uri[1].replace('/', '\\').lstrip('\\'))
                  f = open(uri, 'rb')
                  resp_body = f.read()
                self.server.Interface.JSONTilesLib[req.path[20:]] = resp_body
              _send_resp(ct)
            except:
              _send_err_nf()
            finally:
              if f is not None:
                try:
                  f.close()
                except:
                  pass
          elif req.path.lower()[:17] == '/jsontiles/style/' and req.path.lower()[-11:] == '/style.json':
            try:
              if not self.server.Interface.Map.JSONTiles:
                raise
              tid = int(req.path[17:-11])
              if isinstance(self.server.Interface.TilesSets[self.server.Interface.TilesSet][1], dict):
                if tid != self.server.Interface.TilesSet:
                  raise
              elif not any(tid == tsos[0] for tsos in self.server.Interface.TilesSets[self.server.Interface.TilesSet][1]):
                raise
              resp_body = (self.server.Interface.Map.JSONTiles.Style(tid) or b'').replace(b'{netloc}', ('http://%s:%s' % (self.server.Interface.Ip, self.server.Interface.Ports[0])).encode('utf-8'))
              if resp_body:
                _send_resp('application/json; charset=utf-8')
              else:
                _send_err_nf()
            except:
              _send_err_fail()
          elif req.path.lower()[:18] == '/jsontiles/glyphs/':
            try:
              if not self.server.Interface.Map.JSONTiles:
                raise
              tid = int(req.path[18:].split('/', 1)[0])
              if isinstance(self.server.Interface.TilesSets[self.server.Interface.TilesSet][1], dict):
                if tid != self.server.Interface.TilesSet:
                  raise
              elif not any(tid == tsos[0] for tsos in self.server.Interface.TilesSets[self.server.Interface.TilesSet][1]):
                raise
              f, r = req.path[18:].split('/', 1)[1].rsplit('/', 1)
              if r[-4:] != '.pbf':
                raise
              r = r[:-4]
              resp_body = self.server.Interface.Map.JSONTiles.Glyph(tid, f, r) or ''
              if resp_body:
                _send_resp('application/json; charset=utf-8')
              else:
                _send_err_nf()
            except:
              _send_err_fail()
          elif req.path.lower()[:18] == '/jsontiles/sprite/':
            try:
              if not self.server.Interface.Map.JSONTiles:
                raise
              tid = int(req.path[18:].split('/', 1)[0])
              if isinstance(self.server.Interface.TilesSets[self.server.Interface.TilesSet][1], dict):
                if tid != self.server.Interface.TilesSet:
                  raise
              elif not any(tid == tsos[0] for tsos in self.server.Interface.TilesSets[self.server.Interface.TilesSet][1]):
                raise
              s, e = req.path[18:].split('/', 1)[1].rsplit('.', 1)
              if s[:6] != 'sprite':
                raise
              if e == 'json':
                resp_body = self.server.Interface.Map.JSONTiles.SpriteJSON(tid, s[6:]) or ''
              elif e == 'png':
                resp_body = self.server.Interface.Map.JSONTiles.SpritePNG(tid, s[6:]) or ''
              else:
                raise
              if resp_body:
                _send_resp('application/json; charset=utf-8' if e == 'json' else 'image/png')
              else:
                _send_err_nf()
            except:
              _send_err_fail()
          elif req.path.lower()[:8] == '/map/map':
            resp_body = self.server.Interface.Map.Map
            if resp_body:
              if self.server.Interface.Map.MapInfos.get('format') in ('image/tiff', 'image/geotiff') and req.path.lower()[8:12] == '.png':
                th = TIFFHandler(resp_body, False)
                if th.convert():
                  resp_body = th.converted
                  del th
                  _send_resp(self.server.Interface.Map.MapInfos.get('format', 'image/*'))
                else:
                  _send_err_nf()
              else:
                _send_resp(self.server.Interface.Map.MapInfos.get('format', 'image/*'))
            else:
              _send_err_nf()
          elif req.path.lower()[:13] == '/legend':
            if req.header('If-Match', '') not in (self.server.Interface.SessionId, self.server.Interface.PSessionId):
              _send_err_bad()
              continue
            if self.server.Interface.Mode == 'tiles':
              self.server.Interface.TLock.acquire()
              try:
                if isinstance(self.server.Interface.TilesSets[self.server.Interface.TilesSet][1], dict) and self.server.Interface.TilesSets[self.server.Interface.TilesSet][1].get('format') != 'application/json':
                  tinfos = {self.server.Interface.Map.Tiles.Id: self.server.Interface.Map.TilesInfos}
                else:
                  tinfos = self.server.Interface.Map.TilesInfos
              except:
                _send_err_fail()
                continue
              finally:
                self.server.Interface.TLock.release()
              n_f_l = []
              try:
                for trid, tinf in tinfos.items():
                  f_l = self.server.Interface.Legend.RetrieveTilesLegend(tinf, self.server.Interface.TilesSets[trid[0]][3], **self.server.Interface.TilesSets[trid[0]][2])
                  if f_l is not None:
                    n_f_l.append(((self.server.Interface.TilesSets[trid[0]][0], trid[1]), f_l))
              except:
                _send_err_fail()
                continue
            elif self.server.Interface.Mode == 'map':
              try:
                n_f_l = self.server.Interface.Legend.RetrieveMapLegend(self.server.Interface.Map.MapInfos, self.server.Interface.MapSets[self.server.Interface.MapSet][3], **self.server.Interface.MapSets[self.server.Interface.MapSet][2]).items()
              except:
                _send_err_fail()
                continue
            else:
              _send_err_fail()
              continue
            boundary = base64.b32encode(os.urandom(20)).lower()
            resp_body = b''.join(e for g in ((b'--%b\r\nContent-Disposition: form-data; name="%b"; filename="%b"\r\nContent-type: %b\r\n\r\n%b\r\n' % (boundary, b'legend', ('%s [%s]' % n).replace('"','\'').encode('utf-8'), f_l[0].encode('utf-8'), f_l[1]) for n, f_l in n_f_l), (b'--%b--\r\n' % boundary, )) for e in g)
            _send_resp('multipart/form-data; boundary=%s' % boundary.decode('utf-8'))
          elif req.path.lower()[:27] == '/elevationsproviders/switch' :
            if req.header('If-Match', '') not in (self.server.Interface.SessionId, self.server.Interface.PSessionId):
              _send_err_bad()
              continue
            self.server.Interface.TLock.acquire()
            q = urllib.parse.parse_qs(urllib.parse.urlsplit(req.path).query)
            try:
              eset = int(q['eset'][0])
              self.server.Interface.ElevationProviderSel = eset
              if 'layer' in self.server.Interface.ElevationsProviders[eset][1]:
                self.server.Interface.EMode = 'tiles'
                self.server.Interface.Elevation.SetTilesProvider((eset, self.server.Interface.ElevationsProviders[eset][1].get('matrix')), self.server.Interface.ElevationsProviders[eset][1], self.server.Interface.ElevationsProviders[eset][1].get('matrix'), **self.server.Interface.ElevationsProviders[eset][2])
                self.server.Interface.ElevationProvider = partial(self.server.Interface.Elevation.WGS84toElevation, infos=self.server.Interface.ElevationsProviders[eset][1], matrix=self.server.Interface.ElevationsProviders[eset][1].get('matrix'), **self.server.Interface.ElevationsProviders[eset][2])
                self.server.Interface.log(1, 'elevation', self.server.Interface.ElevationsProviders[eset][0])
              else:
                self.server.Interface.EMode = 'api'
                self.server.Interface.Elevation.SetTilesProvider()
                self.server.Interface.ElevationProvider = partial(self.server.Interface.Elevation.RequestElevation, self.server.Interface.ElevationsProviders[eset][1], **self.server.Interface.ElevationsProviders[eset][2])
                self.server.Interface.log(1, 'elevation', self.server.Interface.ElevationsProviders[eset][0])
            except:
              _send_err_fail()
              continue
            finally:
              self.server.Interface.TLock.release()
            _send_resp_nc()
          elif req.path.lower()[:28] == '/itinerariesproviders/switch' :
            if req.header('If-Match', '') not in (self.server.Interface.SessionId, self.server.Interface.PSessionId):
              _send_err_bad()
              continue
            q = urllib.parse.parse_qs(urllib.parse.urlsplit(req.path).query)
            try:
              self.server.Interface.ItineraryProviderConnection = [[None]]
              self.server.Interface.ItineraryProviderSel = int(q['iset'][0])
              self.server.Interface.log(1, 'itinerary', self.server.Interface.ItinerariesProviders[int(q['iset'][0])][0])
            except:
              _send_err_fail()
              continue
            _send_resp_nc()
          elif req.path.lower()[:15] == '/3D/viewer.html'.lower():
            try:
              mode3d = req.path.split('?3d=')[1][0].lower()
              if mode3d != 'p' and mode3d != 's':
                raise
              margin = float(req.path.split('?3d=')[1][1:].split(',')[0])
            except:
              _send_err_nf()
              continue
            self.server.Interface.SLock.acquire()
            if not self.server.Interface.HTML:
              self.server.Interface.TrackInd = int(req.path.split(',')[1])
              self.server.Interface.Uri, self.server.Interface.Track = self.server.Interface.Tracks[self.server.Interface.TrackInd]
              if self.server.Interface.Track.WebMercatorPts is None:
                self.server.Interface.Track.BuildWebMercator()
            try:
              if self.server.Interface.Build3DHTML(mode3d, margin):
                resp_body = (self.server.Interface.HTML3D or '').encode('utf-8')
                _send_resp('text/html; charset=utf-8')
              else:
                _send_err_nf()
            except:
              _send_err_nf()
            if not self.server.Interface.HTML:
              self.server.Interface.TrackInd = None
              self.server.Interface.Uri, self.server.Interface.Track = None, None
            self.server.Interface.SLock.release()
          elif req.path.lower() == '/3D/data'.lower():
            if self.server.Interface.HTML3D:
              resp_body = self.server.Interface.HTML3DData or b''
              _send_resp('application/octet-stream')
            else:
              _send_err_nf()
          elif req.path.lower() == '/GPXExplorer/data'.lower():
            if not self.server.Interface.HTMLExp:
              _send_err_nf()
              continue
            try:
              resp_body = json.dumps([[[p[1] for p in seg] for seg in tr[1].Pts] for tr in self.server.Interface.Tracks], check_circular=False, separators=(',', ':')).encode('utf-8')
              _send_resp('application/json; charset=utf-8')
            except:
              _send_err_fail()
          elif req.path.lower() == '/media/gps_ar':
            if req.method != 'GET' or req.header('If-Match', '') != self.server.Interface.SessionId:
              _send_err_bad()
              continue
            try:
              resp_body = self.server.Interface.Media.GetData()[0]
              if resp_body:
                _send_resp('application/octet-stream')
              else:
                _send_err_nf()
            except:
              _send_err_fail()
          elif req.path.lower() == '/media/uri_dt':
            if req.method != 'GET' or req.header('If-Match', '') != self.server.Interface.SessionId:
              _send_err_bad()
              continue
            try:
              resp_body = self.server.Interface.Media.GetData()[1]
              if resp_body:
                _send_resp('application/octet-stream')
              else:
                _send_err_nf()
            except:
              _send_err_fail()
          elif req.path.lower()[:7] == '/media?':
            try:
              mind = int(req.path.split('?')[1])
              mtype, med = self.server.Interface.Media.Open(mind)
              if not mtype:
                _send_err_nf()
                continue
              med.seek(0, os.SEEK_END)
              msize = med.tell()
              resp_body = b''
              req_range = req.header('range', '')
              if req_range:
                try:
                  unit, req_range = req_range.rpartition('=')[::2]
                  if unit and unit.lower() != 'bytes':
                    raise
                  req_range = req_range.split('-')
                  req_start = req_range[0].strip()
                  req_end = req_range[1].split(',')[0].strip()
                  if not req_start:
                    req_start = msize - int(req_end)
                    req_end = msize
                  else:
                    req_start = int(req_start)
                    if req_end:
                      req_end = min(int(req_end) + 1, msize)
                    else:
                      req_end = msize
                    if req_start < 0 or req_start >= req_end:
                      raise
                except:
                  _send_err_rns()
                  continue
              else:
                req_start = 0
                req_end = msize
              if (_send_resp(mtype, msize) if req_range == '' else _send_resp_pc(mtype, req_start, req_end, msize) and req.method == 'GET'):
                med.seek(req_start)
                while req_start < req_end:
                  if self.server.__dict__['_BaseServer__shutdown_request'] or self.server.__dict__['_BaseServer__is_shut_down'].is_set():
                    break
                  resp_body = med.read(min(1048576, req_end - req_start))
                  if not resp_body:
                    closed = True
                    break
                  req_start += len(resp_body)
                  try:
                    self.request.sendall(resp_body)
                  except:
                    closed = True
                    break
            except:
              _send_err_fail()
            finally:
              try:
                med.close()
              except:
                pass
          elif req.path.lower()[:7] == '/detach':
            if req.method != 'GET' or req.header('If-Match', '') != self.server.Interface.SessionId:
              _send_err_bad()
              continue
            self.server.Interface.SLock.acquire()
            try:
              if self.server.Interface.HTMLExp is None:
                raise
              tr_ind = int(req.path.split('?')[1])
              ouri, track = self.server.Interface.Tracks[tr_ind]
              trkid = track.TrkId
              _tracks = track._tracks
              nuri = track.DetachFromGPX((tr[1] for tr in self.server.Interface.Tracks if tr[1] != track and tr[0] == ouri), ouri)
              if not nuri:
                raise
            except:
              _send_err_fail()
              self.server.Interface.SLock.release()
              continue
            del track.OTrack
            track.OTrack = track.Track
            self.server.Interface.Tracks[tr_ind][0] = nuri
            self.server.Interface.UpdateHTMLExp(tr_ind, 't')
            track.unlink(_tracks[0])
            _tracks[0] = _tracks[2]
            resp_body = nuri.rsplit('\\', 1)[1].encode('utf-8')
            _send_resp('text/plain; charset=utf-8')
            self.server.Interface.SLock.release()
          elif req.path.lower()[:12] == '/incorporate' or req.path.lower()[:10] == '/integrate':
            if req.method != 'GET' or req.header('If-Match', '') != self.server.Interface.SessionId:
              _send_err_bad()
              continue
            mode = 's' if req.path.lower()[:12] == '/incorporate' else ('ta' if req.path.lower()[:15] == '/integrateafter' else 'tb')
            self.server.Interface.SLock.acquire()
            try:
              if self.server.Interface.HTMLExp is None:
                raise
              tr_ind1, tr_ind2 = map(int, req.path.split('?')[1].split(','))
              uri1, track1 = self.server.Interface.Tracks[tr_ind1]
              uri2, track2 = self.server.Interface.Tracks[tr_ind2]
              _tracks = track2._tracks
              if not track1.AppendToGPX(track2, (tr[1] for tr in self.server.Interface.Tracks if tr[1] != track1 and tr[0] == uri1), mode, uri1):
                raise
              del track1.OTrack
              track1.OTrack = track1.Track
            except:
              _send_err_fail()
              self.server.Interface.SLock.release()
              continue
            if mode == 'ta' or mode == 'tb':
              track2.BackupGPX(uri2)
              self.server.Interface.Tracks[tr_ind2][0] = uri1
              if next((tr for tr in self.server.Interface.Tracks if tr[0] == uri2), None) is None:
                for i in range(3):
                  try:
                    _tracks[i].unlink()
                  except:
                    pass
            resp_body = {}
            for t_ind in range(len(self.server.Interface.Tracks)):
              tr = self.server.Interface.Tracks[t_ind]
              if tr[0] == uri1:
                self.server.Interface.UpdateTrackBoundaries(t_ind)
                self.server.Interface.UpdateHTMLExp(t_ind, 'tpw', resp_body)
            resp_body = json.dumps(resp_body).encode('utf-8')
            _send_resp('application/json; charset=utf-8')
            self.server.Interface.SLock.release()
          elif req.path.lower()[:4] == '/new':
            if req.method != 'GET' or req.header('If-Match', '') != self.server.Interface.SessionId:
              _send_err_bad()
              continue
            self.server.Interface.SLock.acquire()
            try:
              if self.server.Interface.HTMLExp is None:
                raise
              f_ind = int(req.path.split('?')[1])
              uri = os.path.join(self.server.Interface.Folders[f_ind], 'new.gpx')
              suf = 0
              while os.path.exists(uri):
                suf += 1
                uri = os.path.join(self.server.Interface.Folders[f_ind], 'new (%d).gpx' % suf)
              track = WGS84Track(self.server.Interface.SLock)
              if not track.LoadGPX(uri, None, None, self.server.Interface.Builder):
                raise
              if not track.SaveGPX(uri):
                raise
              self.server.Interface.Tracks.append([uri, track])
              self.server.Interface.TracksBoundaries.append((self.server.Interface.Minx, self.server.Interface.Maxx, self.server.Interface.Miny, self.server.Interface.Maxy))
              self.server.Interface.UpdateTrackBoundaries(len(self.server.Interface.Tracks) - 1)
            except:
              _send_err_fail()
              self.server.Interface.SLock.release()
              continue
            resp_body = {}
            self.server.Interface.UpdateHTMLExp(len(self.server.Interface.Tracks) - 1, 'tpw', resp_body)
            resp_body = json.dumps(resp_body).encode('utf-8')
            _send_resp('application/json; charset=utf-8')
            self.server.Interface.SLock.release()
          elif req.path.lower()[:5] == '/edit':
            self.server.Interface.SLock.acquire()
            try:
              if self.server.Interface.HTMLExp is None:
                raise
              if self.server.Interface.HTML:
                _send_err_bad()
                continue
              tind, tdef = req.path.split('?')[1].split(',', 1)
              tdef = tdef.split('|')
              self.server.Interface.TrackInd = int(tind)
              self.server.Interface.Tracks[self.server.Interface.TrackInd][1].Track
              self.server.Interface.Uri, self.server.Interface.Track = self.server.Interface.Tracks[self.server.Interface.TrackInd]
              self.server.Interface.HTML = ''
              self.server.Interface.EditMode(*map(float, tdef))
              self.server.Interface.HTMLExp = ''
              self.server.Interface.SessionId = str(uuid.uuid5(uuid.NAMESPACE_URL, self.server.Interface.Uri + str(time.time())))
            except:
              _send_err_fail()
              self.server.Interface.TrackInd = None
              self.server.Interface.Uri, self.server.Interface.Track = None, None
              continue
            finally:
              self.server.Interface.SLock.release()
            _send_resp_tr('GPXTweaker.html')
          elif req.path.lower()[:9] == '/explorer':
            if req.method != 'GET' or req.header('If-Match', '') != self.server.Interface.SessionId:
              _send_err_bad()
              continue
            try:
              t_type, t_ind = req.path.split('?')[1].split('-')
              t_ind = int(t_ind)
              if t_type.lower() == 'folder':
                os.startfile(self.server.Interface.Folders[t_ind], 'explore')
              elif t_type.lower() == 'file':
                subprocess.run('explorer /select,' + self.server.Interface.Tracks[t_ind][0])
              else:
                raise
              resp_body = b''
              _send_resp('text/html; charset=utf-8')
            except:
              _send_err_fail()
              continue
          else:
            _send_err_nf()
        elif req.method == 'POST':
          if req.path.lower()[:4] == '/ele':
            if req.header('If-Match', '') not in (self.server.Interface.SessionId, self.server.Interface.PSessionId):
              _send_err_bad()
              continue
            if self.server.Interface.EMode == 'tiles' and self.server.Interface.Elevation.Tiles is not None and (self.server.Interface.Elevation.Tiles.Id is None or self.server.Interface.ElevationProviderSel != self.server.Interface.Elevation.Tiles.Id[0]):
              _send_err_fail()
              continue
            lpoints = req.body.splitlines()
            points = []
            ids = []
            try:
              for point in lpoints:
                if point:
                  id_p, lat, lon = point.split(',')
                  points.append((float(lat), float(lon)))
                  ids.append(id_p)
              lelevations = zip(ids, self.server.Interface.ElevationProvider(points))
              for id_ele in lelevations:
                try:
                  resp_body = resp_body + (id_ele[0] + ',' + ('%.1f' % id_ele[1]) + '\r\n').encode('utf-8')
                except:
                  resp_body = resp_body + (id_ele[0] + ', \r\n').encode('utf-8')
              _send_resp('text/csv; charset=utf-8')
            except:
              _send_err_fail()
          elif req.path.lower()[:5] == '/path':
            if req.header('If-Match', '') not in (self.server.Interface.SessionId, self.server.Interface.PSessionId):
              _send_err_bad()
              continue
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
              _send_resp('text/csv; charset=utf-8')
            except:
              _send_err_fail()
          elif req.path.lower()[:6] == '/track':
            self.server.Interface.SLock.acquire()
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
                    self.server.Interface.UpdateHTMLExp(tr_ind, 't')
                _send_resp_nc()
              except:
                _send_err_fail()
                continue
              finally:
                self.server.Interface.SLock.release()
              continue
            nosave = False
            if self.server.Interface.HTML and '?' in req.path:
              nosave = req.path.split('?')[1].lower() == 'save=no'
            if self.server.Interface.HTML and req.header('If-Match', '') == self.server.Interface.SessionId:
              self.server.Interface.PSessionId = self.server.Interface.SessionId
              del self.server.Interface.Track.OTrack
              self.server.Interface.Track.OTrack = self.server.Interface.Track.STrack
            try:
              if not self.server.Interface.HTML:
                self.server.Interface.TrackInd = int(req.body.split('=')[0][5:-4].rstrip('c'))
                self.server.Interface.Uri, self.server.Interface.Track = self.server.Interface.Tracks[self.server.Interface.TrackInd]
              if not nosave:
                if req.header('If-Match', '') in (self.server.Interface.PSessionId, self.server.Interface.SessionId):
                  uri_suf = '.gpx'
                else:
                  uri_suf = ' - ' + req.header('If-Match', '') + '.gpx'
                uri = self.server.Interface.Uri.rsplit('.', 1)[0] + uri_suf
              else:
                uri_suf = None
                uri = None
              if not self.server.Interface.Track.UpdateGPX(req.body, uri, uri_suf == '.gpx'):
                raise
              if nosave:
                self.server.Interface.Track.BuildWebMercator()
              else:
                if self.server.Interface.HTML:
                  try:
                    self.server.Interface.EditMode()
                  except:
                    pass
                  if self.server.Interface.SessionId == self.server.Interface.PSessionId:
                    self.server.Interface.SessionId = str(uuid.uuid5(uuid.NAMESPACE_URL, self.server.Interface.Uri + str(time.time())))
              if not self.server.Interface.HTML:
                del self.server.Interface.Track.OTrack
                self.server.Interface.Track.OTrack = self.server.Interface.Track.Track
                for tr in self.server.Interface.Tracks:
                  if tr[1] != self.server.Interface.Track and tr[0] == self.server.Interface.Uri:
                    tr[1].ProcessGPX('e')
                self.server.Interface.UpdateHTMLExp(self.server.Interface.TrackInd, 'tp')
                if req.body.split('=')[0][-5:] == 'color':
                  self.server.Interface.UpdateHTMLExp(self.server.Interface.TrackInd, 'w')
              _send_resp_nc()
            except:
              _send_err_fail()
              continue
            finally:
              if not self.server.Interface.HTML:
                self.server.Interface.TrackInd = None
                self.server.Interface.Uri, self.server.Interface.Track = None, None
              self.server.Interface.SLock.release()
          elif req.path.lower()[:17] == '/reversegeocoding':
            q = urllib.parse.parse_qs(urllib.parse.urlsplit(req.path).query)
            try:
              if int(q['rgset'][0]) != self.server.Interface.ReverseGeocodingProviderSel:
                self.server.Interface.ReverseGeocodingProviderConnection = [[None]]
                self.server.Interface.ReverseGeocodingProviderSel = int(q['rgset'][0])
                self.server.Interface.log(1, 'reversegeocoding', self.server.Interface.ReverseGeocodingsProviders[self.server.Interface.ReverseGeocodingProviderSel][0])
            except:
              _send_err_fail()
              continue
            lpoint = req.body.split(',')
            try:
              if len(lpoint) != 2:
                raise
              desc = self.server.Interface.ReverseGeocodingProvider(list(map(float, lpoint)))
              if not desc:
                raise
              resp_body = desc.encode('utf-8')
              _send_resp('text/plain; charset=utf-8')
            except:
              _send_err_fail()
          else:
            _send_err_nf()
        elif req.method:
          _send_err_ni()


class WGS84TrackProxy():

  def __init__(self, trkid, name, color, wpts, pts, retrieve):
    for att in ('TrkId', 'Name', 'Color', 'Wpts', 'Pts'):
      object.__setattr__(self, att, locals()[att.lower()])
    object.__setattr__(self, '_retrieve', retrieve)
    object.__setattr__(self, '_rlock', threading.Lock())
    for att in ('_track', 'WebMercatorWpts', 'WebMercatorPts'):
      object.__setattr__(self, att, None)

  def _gather(self, ulock, intern_dict, _tracks):
    with self._rlock:
      if self._track is None:
        track = object.__new__(WGS84Track)
        track.ULock = ulock
        track._tracks = _tracks
        for att in ('TrkId', 'Name', 'Color', 'Wpts', 'Pts', 'WebMercatorWpts', 'WebMercatorPts'):
          setattr(track, att, getattr(self, att))
        track.intern_dict = intern_dict
        track._intern()
        track.log = partial(log, 'track')
        object.__setattr__(self, '_track', track)
        for att in ('TrkId', 'Name', 'Color', 'Wpts', 'Pts', 'WebMercatorWpts', 'WebMercatorPts'):
          object.__delattr__(self, att)
    return self._track

  def __getattr__(self, name):
    if self._track is None:
      self._retrieve()
    return getattr(self._track, name)

  def __setattr__(self, name, value):
    if name in ('WebMercatorWpts', 'WebMercatorPts'):
      with self._rlock:
        if self._track is None:
          object.__setattr__(self, name, value)
          return
    if self._track is None:
      self._retrieve()
    setattr(self._track, name, value)

  def __delattr__(self, name):
    if self._track is None:
      self._retrieve()
    delattr(self._track, name)

  def __eq__(self, other):
    return self._track == other if (isinstance(other, WGS84Track) and self._track is not None) else NotImplemented

  def BuildWebMercator(self):
    return WGS84Track.BuildWebMercator(self)


class Interrupted(Exception):
  pass


class GPXLoader():

  def __init__(self, nworkers, repatriation, slock=None):
    self.NWorkers = nworkers
    self.Repatriation = repatriation
    self.Workers = []
    self.Connections = []
    self.SLock = slock
    self.Tracks = []
    self.CTracks = []
    self.RIndex = 0
    self.RPTracks = deque()
    self.RThread = None
    self.RCondition = threading.Condition()
    self.Closed = False
    self.log = partial(log, 'loader')
    self.log(2, 'init', nworkers)

  @staticmethod
  def Worker(gindex, connection, dboundaries, mboundaries, verbosity, vt100, anticipatory):
    global VERBOSITY
    VERBOSITY = verbosity
    global VT100
    VT100 = vt100
    wlog = partial(log, 'loader', buffer=False)
    wname = multiprocessing.current_process().name.rpartition('-')[2]
    wlog(2, 'wstart', wname)
    uris = connection.recv()
    builder = ExpatGPXBuilder()
    gtracks = {}
    squeue = deque()
    qcondition = threading.Condition()
    lend = False
    stop = False
    def send():
      nonlocal stop
      while True:
        with qcondition:
          while not squeue and not lend:
            qcondition.wait()
          if not squeue and lend:
            break
        ind, track, b = squeue.popleft()
        try:
          connection.send(ind)
          connection.send(((track.TrkId, track.Name, track.Color, track.Wpts, track.Pts), b))
          wlog(2, 'wsqueue', wname, uris[ind], track.TrkId)
        except BrokenPipeError:
          stop = True
          return
      try:
        connection.send(None)
        connection.send((tskipped, taborted, gaborted))
      except BrokenPipeError:
        stop = True
    sthread = threading.Thread(target=send)
    sthread.start()
    GCMan.disable()
    try:
      tskipped = taborted = gaborted = 0
      garb = []
      while True:
        with gindex.get_lock():
          ind = gindex.value
          if ind >= len(uris):
            break
          gindex.value += 1
        uri = uris[ind]
        wlog(2, 'wload', wname, uri)
        trk = 0
        nbtrk = 1
        trck = None
        while trk < nbtrk:
          if stop:
            raise Interrupted
          track = WGS84Track()
          trck = trck or track
          l = track.LoadGPX(uri, trk, trck, builder)
          if not l:
            with gindex.get_lock():
              print(*LogBuffer, sep='\r\n')
            LogBuffer.clear()
            if trck.Pts is None:
              if trck.Track is None:
                gaborted += 1
              else:
                for trk in range(1, len(trck.Track.documentElement.getChildren('trk'))):
                  trck.log(0, 'lerror', uri + (' <%s>' % trk))
                with gindex.get_lock():
                  print(*LogBuffer, sep='\r\n')
                LogBuffer.clear()
                taborted += trk + 1
                garb.append(trck.Track)
              break
            else:
              taborted += 1
          else:
            minlat = min((p[1][0] for seg in (*track.Pts, track.Wpts) for p in seg), default=dboundaries[0])
            maxlat = max((p[1][0] for seg in (*track.Pts, track.Wpts) for p in seg), default=dboundaries[1])
            minlon = min((p[1][1] for seg in (*track.Pts, track.Wpts) for p in seg), default=dboundaries[2])
            maxlon = max((p[1][1] for seg in (*track.Pts, track.Wpts) for p in seg), default=dboundaries[3])
            if minlat < mboundaries[0] or maxlat > mboundaries[1] or minlon < mboundaries[2] or maxlon > mboundaries[3]:
              tskipped += 1
              log('interface', 0, 'berror6', color=31)
            else:
              gtracks.setdefault(ind, trck.Track)
              with qcondition:
                wlog(2, 'wiqueue', wname, uri, trk)
                squeue.append((ind, track, (minlat, maxlat, minlon, maxlon)))
                qcondition.notify_all()
            with gindex.get_lock():
              print(*LogBuffer, sep='\r\n')
            LogBuffer.clear()
          if nbtrk == 1:
            nbtrk = len(track.Track.documentElement.getChildren('trk'))
          trk += 1
        else:
          if not gtracks.get(ind):
            garb.append(trck.Track)
    except Interrupted:
      exit()
    finally:
      lend = True
      with qcondition:
        qcondition.notify_all()
      for trck in garb:
        try:
          trck.unlink()
        except:
          pass
      garb.clear()
      if stop:
        for trck in gtracks.values():
          try:
            trck.unlink()
          except:
            pass
        wlog(2, 'winterrupt', wname)
      sthread.join()
      GCMan.restore()
    wlog(2, 'weload', wname)
    pickled = (None, None)
    while gtracks:
      try:
        ind = connection.recv()
      except EOFError:
        for trck in gtracks.values():
          try:
            trck.unlink()
          except:
            pass
        break
      wlog(2, 'wrdoc', wname, uris[ind])
      if ind == pickled[0]:
        connection.send_bytes(pickled[1])
        pickled = (None, None)
      else:
        connection.send((builder.intern_dict, gtracks[ind]))
      wlog(2, 'wsdoc', wname, uris[ind])
      try:
        gtracks[ind].unlink()
      except:
        pass
      del gtracks[ind]
      if anticipatory and pickled[0] is None and gtracks and not connection.poll(0):
        ind = next(iter(gtracks))
        pickled = (ind, pickle.dumps((builder.intern_dict, gtracks[ind])))
    wlog(2, 'wend', wname)

  def Retrieve(self, tindex):
    with self.RCondition:
      if self.CTracks[tindex] and not self.Closed:
        self.RPTracks.append(tindex)
        self.RCondition.notify_all()
      while self.CTracks[tindex]:
        if self.Closed:
          self.Tracks[tindex][1]._gather(self.SLock, {}, [None] * 3)
          return
        self.RCondition.wait()

  def Repatriate(self):
    self.log(2, 'rstarty' if self.Repatriation else 'rstartn')
    l = len(self.CTracks)
    GCMan.disable()
    while True:
      with self.RCondition:
        if self.RIndex >= l or self.Closed:
          break
        if self.RPTracks:
          tindex = self.RPTracks.popleft()
          self.log(2, 'rrequest', self.Tracks[tindex][0], self.Tracks[tindex][1].TrkId)
        else:
          if self.Repatriation:
            tindex = self.RIndex
            self.log(2, 'rhandle', self.Tracks[tindex][0], self.Tracks[tindex][1].TrkId)
            self.RIndex += 1
          else:
            GCMan.restore()
            self.RCondition.wait()
            GCMan.disable()
            continue
        if self.CTracks[tindex] is None:
          self.log(2, 'rabort', self.Tracks[tindex][0], self.Tracks[tindex][1].TrkId)
          continue
      self.CTracks[tindex][2].send(self.CTracks[tindex][0])
      intern_dict, gtrack = self.CTracks[tindex][2].recv()
      _tracks = [gtrack] * 3
      with self.RCondition:
        for _tindex in range(*map(tindex.__add__, self.CTracks[tindex][1])):
          self.Tracks[_tindex][1] = self.Tracks[_tindex][1]._gather(self.SLock, intern_dict, _tracks)
          self.CTracks[_tindex] = None
          self.log(2, 'rretrieved', self.Tracks[_tindex][0], self.Tracks[_tindex][1].TrkId)
        self.RCondition.notify_all()
    GCMan.restore()
    self.log(2, 'rend' if self.RIndex >= l else 'rstop')

  def Load(self, uris, dboundaries, mboundaries, stop=(lambda:False)):
    gindex = multiprocessing.Value('I', 0)
    pipes = tuple(multiprocessing.Pipe() for i in range(self.NWorkers))
    self.Connections = tuple(pipe[0] for pipe in pipes)
    self.Workers = tuple(multiprocessing.Process(target=self.Worker, args=(gindex, pipe[1], dboundaries, mboundaries, VERBOSITY, VT100, self.Repatriation)) for pipe in pipes)
    for worker in self.Workers:
      worker.start()
    for connection in self.Connections:
      connection.send(uris)
    gtracks = [[] for i in range(len(uris))]
    gtracksb = [[] for i in range(len(uris))]
    gtracksc = [None] * len(uris)
    nlworkers = self.NWorkers
    tskipped = taborted = gaborted = 0
    while nlworkers > 0:
      if stop():
        for connection in self.Connections:
          connection.close()
        self.log(2, 'itrack')
        raise Interrupted()
      rconnections = multiprocessing.connection.wait(self.Connections)
      for connection in rconnections:
        gind = connection.recv()
        if gind is None:
          nlworkers -= 1
          tskipped, taborted, gaborted = (a + b for a, b in zip((tskipped, taborted, gaborted), connection.recv()))
        else:
          track, trackb = connection.recv()
          gtracks[gind].append(track)
          gtracksb[gind].append(trackb)
          gtracksc[gind] = connection
          self.log(2, 'rtrack', uris[gind], gtracks[gind][-1][0])
    self.Tracks = [[uri, WGS84TrackProxy(*track, partial(self.Retrieve, tindex))] for tindex, (uri, track) in enumerate((uri, track) for uri, gtrack in zip(uris, gtracks) for track in gtrack)]
    tracksb = [trackb for gtrackb in gtracksb for trackb in gtrackb]
    self.CTracks = [(gind, (-trk, l - trk), gtrackc) for gind, (gtrackc, l) in enumerate(zip(gtracksc, map(len, gtracks))) for trk in range(l)]
    self.log(2, 'etrack')
    self.RThread = threading.Thread(target=self.Repatriate)
    self.RThread.start()
    return self.Tracks, tracksb, tskipped, taborted, gaborted

  def Close(self):
    self.Closed = True
    with self.RCondition:
      self.RCondition.notify_all()
    if self.RThread is not None:
      self.RThread.join()
    for connection in self.Connections:
      connection.close()
    for worker in self.Workers:
      worker.join()
      worker.close()
    self.log(2, 'close')


class GPXTweakerWebInterfaceServer():

  HTML_STYLES_TEMPLATE = \
  '    <style type="text/css">\r\n' \
  '      :root {\r\n' \
  '        --scale:1;\r\n' \
  '        --zoom:1;\r\n' \
  '        --wsp:6em;\r\n' \
  '        --filter:none;\r\n' \
  '        --magnify:1;\r\n' \
  '      }\r\n' \
  '      input:focus-visible, select:focus-visible, button:focus-visible {\r\n' \
  '        outline:rgb(200,250,240) solid 1px;\r\n' \
  '        outline-offset:-1px;\r\n' \
  '      }\r\n' \
  '      div:focus-visible {outline:none;}\r\n' \
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
  '      input+label[id$=desc]:hover,input:hover+label[id$=desc] {\r\n' \
  '        background-color:green;\r\n' \
  '      }\r\n' \
  '      svg[id*=dot] {\r\n' \
  '        position:absolute;\r\n' \
  '        cursor:pointer;\r\n' \
  '        stroke-width:1.5;\r\n' \
  '      }\r\n' \
  '      path {\r\n' \
  '        pointer-events:stroke;\r\n' \
  '        cursor:pointer;\r\n' \
  '        stroke-width:calc(2px * var(--magnify));\r\n' \
  '        fill:none;\r\n' \
  '        vector-effect:non-scaling-stroke;\r\n' \
  '      }\r\n' \
  '      textPath {\r\n' \
  '        vector-effect:non-scaling-stroke;\r\n' \
  '      }\r\n' \
  '      svg[id^=track] {\r\n' \
  '        position:absolute;\r\n' \
  '        stroke-linecap:round;\r\n' \
  '        stroke-linejoin:round;\r\n' \
  '      }\r\n' \
  '      svg[id^=track] text {\r\n' \
  '        stroke-width:calc(1px * var(--magnify));\r\n' \
  '        font-size:calc(24px * var(--scale) * (var(--magnify) + 1) / 2);\r\n' \
  '        word-spacing:calc(var(--wsp) * 2 / (var(--magnify) + 1));\r\n' \
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
  '        color:rgb(200,250,240);\r\n' \
  '      }\r\n' \
  '      @-moz-document url-prefix() {\r\n' \
  '        select {\r\n' \
  '          appearance:none;\r\n' \
  '          padding-right:1.7em;\r\n' \
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
  '      select[id$=set] {\r\n' \
  '        width:14em;\r\n' \
  '        height:1.7em;\r\n' \
  '      }\r\n' \
  '      select[id^=graph] {\r\n' \
  '        position:absolute;\r\n' \
  '        left:0;\r\n' \
  '        width:7em;\r\n' \
  '        height:1.7em;\r\n' \
  '      }\r\n' \
  '      div[id=dfpanel], div[id=mtpanel], div[id=v3Dpanel], div[id^=filterpanel] {\r\n' \
  '        display:none;\r\n' \
  '        position:absolute;\r\n' \
  '        top:calc(1.6em + 10px);\r\n' \
  '        right:2vw;\r\n' \
  '        width:10em;\r\n' \
  '        height:13.4em;\r\n' \
  '        background-color:rgb(30,30,35);\r\n' \
  '        z-index:10;\r\n' \
  '        font-size:75%;\r\n' \
  '        text-align:center;\r\n' \
  '        font-weight:normal;\r\n' \
  '        user-select:none;\r\n' \
  '      }\r\n' \
  '      label[for$=filter], label[for$=margin], label[for=mthumb] {\r\n' \
  '        position:absolute;\r\n' \
  '        top:1.5em;\r\n' \
  '        text-align:center;\r\n' \
  '        font-weight:normal;\r\n' \
  '        font-size:90%;\r\n' \
  '      }\r\n' \
  '      span[id=dfdist], span[id=mtsize], span[id$=stren], span[id^=sl], span[id^=sp], span[id^=v3d] {\r\n' \
  '        position:absolute;\r\n' \
  '        top:2.8em;\r\n' \
  '        width:2em;\r\n' \
  '        font-size:90%;\r\n' \
  '      }\r\n' \
  '      span+input[type=range] {\r\n' \
  '        position:absolute;\r\n' \
  '        top:3em;\r\n' \
  '        max-width:40vh;\r\n' \
  '        width:9em;\r\n' \
  '        margin-right:0;\r\n' \
  '        transform:rotate(-90deg);\r\n' \
  '        transform-origin:right center;\r\n' \
  '        font-size:100%;\r\n' \
  '      }\r\n' \
  '      label[for^=opacity] {\r\n' \
  '        display:inline-block;\r\n' \
  '        margin:0.5em;\r\n' \
  '        width:10.5em;\r\n' \
  '        overflow:hidden;\r\n' \
  '        white-space:nowrap;\r\n' \
  '        vertical-align:middle;\r\n' \
  '      }\r\n' \
  '      input[id^=opacity] {\r\n' \
  '        width:9em;\r\n' \
  '        vertical-align:middle;\r\n' \
  '      }\r\n' \
  '      span[id^=opacity] {\r\n' \
  '        display:inline-block;\r\n' \
  '        margin:0.5em;\r\n' \
  '        vertical-align:middle;\r\n' \
  '      }\r\n' \
  '      div[id$=box] {\r\n' \
  '        position:absolute;\r\n' \
  '        bottom:3px;\r\n' \
  '        background-color:rgba(255,255,255,0.7);\r\n' \
  '        padding-left:2px;\r\n' \
  '        padding-right:2px;\r\n' \
  '        user-select:none;\r\n' \
  '      }\r\n' \
  '      span+span[id^=message] {\r\n' \
  '        margin-left:0.4em;\r\n' \
  '        padding-left:0.4em;\r\n' \
  '        border-left:1px rgb(225,225,225) solid;\r\n' \
  '      }\r\n' \
  '      div[id=view]>div[id^=jmap] {\r\n' \
  '        position:absolute;\r\n' \
  '        pointer-events:none;\r\n' \
  '        overflow:hidden;\r\n' \
  '        width:calc(100% / var(--zoom));\r\n' \
  '        height:calc(100% / var(--zoom));\r\n' \
  '        transform-origin:left top;\r\n' \
  '        transform:scale(var(--zoom));\r\n' \
  '        background-color:rgba(0,0,0,0);\r\n' \
  '      }\r\n' \
  '      @supports not (selector(*::-moz-color-swatch)) {\r\n' \
  '        div[id=handle]>img::before{\r\n' \
  '          content:"";\r\n' \
  '          position:absolute;\r\n' \
  '          left:1px;\r\n' \
  '          top:1px;\r\n' \
  '          background:rgb(40,45,50);\r\n' \
  '          width:calc(100% - 2px);\r\n' \
  '          height:calc(100% - 2px);\r\n' \
  '        }\r\n' \
  '      }\r\n'
  HTML_GLOBALVARS_TEMPLATE = \
  '      const host = location.hostname + ":";\r\n' \
  '      var wmb = Math.PI * 6378137;\r\n##DECLARATIONS##\r\n' \
  '      var hpx = 0;\r\n' \
  '      var hpy = 0;\r\n' \
  '      var cpx = null;\r\n' \
  '      var cpy = null;\r\n' \
  '      var zoom = 1;\r\n' \
  '      if (mode == "map") {\r\n' \
  '        var tset = 0;\r\n' \
  '        var zooms = ["1", "1.5", "2", "3", "4", "6", "10", "15", "25"];\r\n' \
  '        var zoom_s = "1";\r\n' \
  '      } else {\r\n' \
  '        var tset = -1;\r\n' \
  '        var tlevels = [];\r\n' \
  '        var tlevel = 0;\r\n' \
  '        var zooms = ["1/8", "1/4", "1/2", "3/4", "1", "1.5", "2", "3", "4", "6", "8"];\r\n' \
  '        var tlock = false;\r\n' \
  '        var zoom_s = "1";\r\n' \
  '        var layers = [];\r\n' \
  '        var layersc = [];\r\n' \
  '        var opacities = new Map();\r\n' \
  '        var treset = 0;\r\n' \
  '        var jmaps = [];\r\n' \
  '      }\r\n' \
  '      var adjustment_a = 1.0;\r\n' \
  '      var adjustment_e = 1.0;\r\n' \
  '      var eset = -1;\r\n' \
  '      var iset = -1;\r\n' \
  '      var dots_visible = false;\r\n' \
  '      var scrollmode = 2;\r\n' \
  '      var scrollmode_ex = scrollmode;\r\n' \
  '      var focused = "";\r\n' \
  '      var tiles_hold = null;\r\n' \
  '      if (tholdsize > 0 && navigator.userAgent.toLowerCase().indexOf("firefox") < 0) {var tiles_hold = new Map();}\r\n' \
  '      var date_conv = new Intl.DateTimeFormat("default",{year: "numeric", month:"2-digit", day:"2-digit"});\r\n' \
  '      var time_conv = new Intl.DateTimeFormat("default",{hour12:false, hour: "2-digit", minute:"2-digit", second:"2-digit"});\r\n' \
  '      var xhr_ongoing = 0;\r\n'
  HTML_GPUSTATS_TEMPLATE = \
  '      class GPUStats {\r\n' \
  '        static get tw() {return 1024;}\r\n' \
  '        constructor (mode) {\r\n' \
  '          this.mode = mode;\r\n' \
  '          this.canvas = document.createElement("canvas");\r\n' \
  '          this.gl = this.canvas.getContext("webgl2", {preserveDrawingBuffer: true});\r\n' \
  '          this.gl_programs = new Map();\r\n' \
  '          this.cur_prog = null;\r\n' \
  '          this.gl_attributes = new Map([["vstart", ["int", 1]], ["vend", ["int", 1, 4]]]);\r\n' \
  '          this.gl_static_uniforms = new Map([["mmltex", "sampler2D"], ["lltex", "sampler2D"], ["xytex", "sampler2D"], ["teahtex", "sampler2D"], ["gtex", "sampler2D"], ["ssstex", "sampler2D"], ["stex", "sampler2D"], ["trange", "float"], ["spmax", "float"], ["drange", "float"], ["slmax", "float"]]);\r\n' \
  '          this.gl_dynamic_uniforms = new Map([["trlat", "float"], ["rlat", "float"]]);\r\n' \
  '          this.gl_feedbacks = new Map([["vxy", "vec2"], ["vg", "float"], ["vsss", "vec3"], ["vs", "float"]]);\r\n' \
  '          this._starts = null;\r\n' \
  '          this.tlength = null;\r\n' \
  '          this._rlats = null;\r\n' \
  '          this._mmls = null;\r\n' \
  '          this._lls = null;\r\n' \
  '          this._teahs = null;\r\n' \
  '          this.vstart = null;\r\n' \
  '          this.vend = null;\r\n' \
  '          this.mmltex = 0;\r\n' \
  '          this.lltex = 0;\r\n' \
  '          this.xytex = 0;\r\n' \
  '          this.teahtex = 1;\r\n' \
  '          this.gtex = 2;\r\n' \
  '          this.ssstex = 3;\r\n' \
  '          this.stex = 4;\r\n' \
  '          this.mml_texture = null;\r\n' \
  '          this.ll_texture = null;\r\n' \
  '          this.xy_texture = null;\r\n' \
  '          this.teah_texture = null;\r\n' \
  '          this.g_texture = null;\r\n' \
  '          this.sss_texture = null;\r\n' \
  '          this.s_texture = null;\r\n' \
  '          this.trlat = null;\r\n' \
  '          this.rlat = null;\r\n' \
  '          this.trange = 60 / 2;\r\n' \
  '          this.spmax = 8 / 3.6;\r\n' \
  '          this.drange = 80 / 2;\r\n' \
  '          this.slmax = 50 / 100;\r\n' \
  '          this.vxy = null;\r\n' \
  '          this.vg = null;\r\n' \
  '          this.vsss = null;\r\n' \
  '          this.vs = null;\r\n' \
  '          this._xys = null;\r\n' \
  '          this._gs = null;\r\n' \
  '          this._ssss = null;\r\n' \
  '          this._ss = null;\r\n' \
  '          this.gl.enable(this.gl.RASTERIZER_DISCARD);\r\n' \
  '          let vertex_pshader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform float trlat;\r\n' \
  '            uniform sampler2D lltex;\r\n' \
  '            out vec2 vxy;\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec2 ll = texelFetch(lltex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).st * vec2(0.00872664626);\r\n' \
  '              float t = ll.s + pow(ll.s, 3.0) / 3.0;\r\n' \
  '              float t2 = t * (pow(trlat, 2.0) + 1.0) / (trlat - t);\r\n' \
  '              vxy = vec2(ll.t * 12756274.0, (t2 - pow(t2, 2.0) / 2.0 + pow(t2, 3.0) / 3.0) * 6378137.0);\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let vertex_g1shader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform sampler2D mmltex;\r\n' \
  '            out float vg;\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec3 mmle = texelFetch(mmltex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).stp * vec3(0.00872664626, 0.00872664626, 0.0174532925);\r\n' \
  '              float ls = gl_InstanceID > 0 ? texelFetch(mmltex, ivec2((pc - 1) % ${GPUStats.tw}, (pc - 1) / ${GPUStats.tw}), 0).p * 0.0174532925 : mmle.p;\r\n' \
  '              float a = sqrt(pow(mmle.s, 2.0) - pow(mmle.s, 4.0) / 3.0 + cos(ls) * cos(mmle.p) * (pow(mmle.t, 2.0) - pow(mmle.t, 4.0) / 3.0));\r\n' \
  '              vg = 12756274.0 * (a + pow(a, 3.0) / 6.0);\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let vertex_g2shader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform float rlat;\r\n' \
  '            uniform sampler2D lltex;\r\n' \
  '            out float vg;\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec2 lle = texelFetch(lltex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).st * vec2(0.00872664626);\r\n' \
  '              vec2 lls = gl_InstanceID > 0 ? texelFetch(lltex, ivec2((pc - 1) % ${GPUStats.tw}, (pc - 1) / ${GPUStats.tw}), 0).st * vec2(0.00872664626) : lle;\r\n' \
  '              vec2 dll = lle - lls;\r\n' \
  '              float a = sqrt(pow(dll.s, 2.0) - pow(dll.s, 4.0) / 3.0 + cos(rlat - lls.s * 2.0) * cos(rlat - lle.s * 2.0) * (pow(dll.t, 2.0) - pow(dll.t, 4.0) / 3.0));\r\n' \
  '              vg = 12756274.0 * (a + pow(a, 3.0) / 6.0);\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let vertex_gwmshader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform float trlat;\r\n' \
  '            uniform sampler2D xytex;\r\n' \
  '            out float vg;\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec2 xye = texelFetch(xytex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).st;\r\n' \
  '              vec2 xys = gl_InstanceID > 0 ? texelFetch(xytex, ivec2((pc - 1) % ${GPUStats.tw}, (pc - 1) / ${GPUStats.tw}), 0).st : xye;\r\n' \
  '              vec2 e = trlat * exp(- vec2(xys.t, xye.t) / 6378137.0);\r\n' \
  '              vec2 c = 1.0 / (e + 1.0 / e);\r\n' \
  '              vg = distance(xys, xye) * (c.s + c.t);\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let vertex_s1ashader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            in int vend;\r\n' \
  '            uniform sampler2D teahtex;\r\n' \
  '            uniform sampler2D gtex;\r\n' \
  '            uniform float drange;\r\n' \
  '            uniform float slmax;\r\n' \
  '            out vec3 vsss;\r\n' \
  '            vec3 slope(float d, vec3 z) {\r\n' \
  '              return d==0.0 ? slmax * sign(z) : z / d;\r\n' \
  '            }\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec4 geahs = vec4(0.0, texelFetch(teahtex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).tpq);\r\n' \
  '              vsss = vec3(0.0);\r\n' \
  '              vec4 geahe = geahs;\r\n' \
  '              vec4 geahp = geahe;\r\n' \
  '              bool b = false;\r\n' \
  '              for (int p = pc + 1; p < vend; p++) {\r\n' \
  '                geahe = vec4(texelFetch(gtex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s + geahe.s, texelFetch(teahtex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).tpq);\r\n' \
  '                if (geahe.s > drange && b) {break;}\r\n' \
  '                if (geahe.s == 0.0) {continue;}\r\n' \
  '                b = true;\r\n' \
  '                vsss += slope(geahe.s, geahe.tpq - geahs.tpq) * (geahe.s - geahp.s);\r\n' \
  '                geahp = geahe;\r\n' \
  '              }\r\n' \
  '              if (pc < vend - 1) {\r\n' \
  '                vsss = (vsss + slope(geahp.s, geahp.tpq - geahs.tpq) * (drange - geahp.s)) / drange;\r\n' \
  '              }\r\n' \
  '              vsss = clamp(vsss, vec3(-slmax), vec3(slmax));\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let vertex_s1bshader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            in int vend;\r\n' \
  '            uniform sampler2D teahtex;\r\n' \
  '            uniform sampler2D ssstex;\r\n' \
  '            uniform float trange;\r\n' \
  '            uniform float spmax;\r\n' \
  '            out float vs;\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec2 tds = vec2(texelFetch(teahtex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).s, 0.0);\r\n' \
  '              vs = 0.0;\r\n' \
  '              vec2 tde = tds;\r\n' \
  '              vec2 tdp = tde;\r\n' \
  '              for (int p = pc + 1; p < vend; p++) {\r\n' \
  '                tde = vec2(texelFetch(teahtex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s, texelFetch(ssstex, ivec2((p - 1) % ${GPUStats.tw}, (p - 1) / ${GPUStats.tw}), 0).p + tde.t);\r\n' \
  '                if (tde.s > tds.s + trange) {break;}\r\n' \
  '                if (tde.s == tds.s) {continue;}\r\n' \
  '                vs += tde.t / (tde.s - tds.s) * (tde.s - tdp.s);\r\n' \
  '                tdp = tde;\r\n' \
  '              }\r\n' \
  '              if (tdp.s != tds.s) {\r\n' \
  '                vs = (vs + tdp.t / (tdp.s - tds.s) * (trange + tds.s - tdp.s)) / trange;\r\n' \
  '              }\r\n' \
  '              vs = min(vs, spmax);\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let vertex_s2ashader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform sampler2D gtex;\r\n' \
  '            uniform sampler2D ssstex;\r\n' \
  '            uniform float drange;\r\n' \
  '            uniform float slmax;\r\n' \
  '            out vec3 vsss;\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec4 gsssc = vec4(0.0, texelFetch(ssstex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).stp);\r\n' \
  '              vec4 gsssf = gsssc;\r\n' \
  '              vec4 gsssn = gsssc;\r\n' \
  '              vsss = gsssc.tpq;\r\n' \
  '              float c;\r\n' \
  '              float su = 0.0;\r\n' \
  '              vec3 sss = vec3(0.0);\r\n' \
  '              for (int p = pc - 1; p >= vstart; p--) {\r\n' \
  '                gsssf = vec4(gsssf.s - texelFetch(gtex, ivec2((p + 1) % ${GPUStats.tw}, (p + 1) / ${GPUStats.tw}), 0).s, texelFetch(ssstex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).stp);\r\n' \
  '                if (gsssf.s < - drange) {break;}\r\n' \
  '                c = (gsssn.s - gsssf.s) / (1.0 - gsssf.s);\r\n' \
  '                sss += gsssf.tpq * c;\r\n' \
  '                su += c;\r\n' \
  '                gsssn = gsssf;\r\n' \
  '              }\r\n' \
  '              if (gsssn.s != 0.0) {\r\n' \
  '                vsss = clamp((vsss + sss / 2.0) / (1.0 + su / 2.0), vec3(-slmax), vec3(slmax));\r\n' \
  '              }\r\n' \
  '              vsss.p = texelFetch(gtex, ivec2((pc + 1) % ${GPUStats.tw}, (pc + 1) / ${GPUStats.tw}), 0).s * sqrt(1.0 + pow(vsss.p, 2.0));\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let vertex_s2bshader_s = `#version 300 es\r\n' \
  '            in int vstart;\r\n' \
  '            uniform sampler2D teahtex;\r\n' \
  '            uniform sampler2D stex;\r\n' \
  '            uniform float trange;\r\n' \
  '            uniform float spmax;\r\n' \
  '            out float vs;\r\n' \
  '            void main() {\r\n' \
  '              int pc = vstart + gl_InstanceID;\r\n' \
  '              vec2 tsc = vec2(texelFetch(teahtex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).s, texelFetch(stex, ivec2(pc % ${GPUStats.tw}, pc / ${GPUStats.tw}), 0).s);\r\n' \
  '              vec2 tsf = tsc;\r\n' \
  '              vec2 tsn = tsc;\r\n' \
  '              vs = tsc.t;\r\n' \
  '              float c;\r\n' \
  '              float su = 0.0;\r\n' \
  '              float s = 0.0;\r\n' \
  '              if (texelFetch(teahtex, ivec2((pc + 1) % ${GPUStats.tw}, (pc + 1) / ${GPUStats.tw}), 0).s - tsc.s <= trange) {\r\n' \
  '                for (int p = pc - 1; p >= vstart; p--) {\r\n' \
  '                  tsf = vec2(texelFetch(teahtex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s, texelFetch(stex, ivec2(p % ${GPUStats.tw}, p / ${GPUStats.tw}), 0).s);\r\n' \
  '                  if (tsf.s < tsc.s - trange) {break;}\r\n' \
  '                  c = (tsn.s - tsf.s) / (1.0 + tsc.s - tsf.s);\r\n' \
  '                  s += tsf.t * c;\r\n' \
  '                  su += c;\r\n' \
  '                  tsn = tsf;\r\n' \
  '                }\r\n' \
  '                if (tsn.s != tsc.s) {\r\n' \
  '                  vs = min((vs + s / 2.0) / (1.0 + su / 2.0), spmax);\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          let fragment_shader_s = `#version 300 es\r\n' \
  '            precision highp float;\r\n' \
  '            void main() {\r\n' \
  '            }\r\n' \
  '          `;\r\n' \
  '          if (this.mode == "tweaker") {\r\n' \
  '            this.program_create("gprogram", vertex_g1shader_s, fragment_shader_s);\r\n' \
  '          } else if (this.mode == "explorer") {\r\n' \
  '            this.program_create("pprogram", vertex_pshader_s, fragment_shader_s);\r\n' \
  '            this.program_create("gprogram", vertex_g2shader_s, fragment_shader_s);\r\n' \
  '            this.program_create("gwmprogram", vertex_gwmshader_s, fragment_shader_s);\r\n' \
  '          }\r\n' \
  '          this.program_create("s1aprogram", vertex_s1ashader_s, fragment_shader_s);\r\n' \
  '          this.program_create("s2aprogram", vertex_s2ashader_s, fragment_shader_s);\r\n' \
  '          this.program_create("s1bprogram", vertex_s1bshader_s, fragment_shader_s);\r\n' \
  '          this.program_create("s2bprogram", vertex_s2bshader_s, fragment_shader_s);\r\n' \
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
  '                this.gl.vertexAttribIPointer(this.gl_programs.get(this.cur_prog).get(n), ts[1], this.gl.INT, 0, ts.length>2?ts[2]:0);\r\n' \
  '              } else {\r\n' \
  '                this.gl.vertexAttribPointer(this.gl_programs.get(this.cur_prog).get(n), ts[1], this.gl.FLOAT, false, 0, ts.length>2?ts[2]:0);\r\n' \
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
  '          this.vend = this.vstart;\r\n' \
  '        }\r\n' \
  '        get starts() {\r\n' \
  '          return this._starts;\r\n' \
  '        }\r\n' \
  '        set rlats(a) {\r\n' \
  '          this._rlats = a.map(function (tl) {return tl[0] * Math.PI / 180});\r\n' \
  '        }\r\n' \
  '        set mmls(a) {\r\n' \
  '          this._mmls = a;\r\n' \
  '          this.mml_texture = this.texture_load(this.gl.TEXTURE0 + this.mmltex, 3, this._mmls, this.mml_texture);\r\n' \
  '          this.vg = this.buffer_load(4 * GPUStats.pad(this.tlength), this.gl.DYNAMIC_READ, this.vg);\r\n' \
  '         }\r\n' \
  '        set lls(a) {\r\n' \
  '          this._lls = a;\r\n' \
  '          this.ll_texture = this.texture_load(this.gl.TEXTURE0 + this.lltex, 2, this._lls, this.ll_texture);\r\n' \
  '          this.vxy = this.buffer_load(2 * 4 * GPUStats.pad(this.tlength), this.gl.DYNAMIC_READ, this.vxy);\r\n' \
  '          this.vg = this.buffer_load(4 * GPUStats.pad(this.tlength), this.gl.DYNAMIC_READ, this.vg);\r\n' \
  '         }\r\n' \
  '        set xys(a) {\r\n' \
  '          this._xys = a;\r\n' \
  '          this.xy_texture = this.ll_texture = this.texture_load(this.gl.TEXTURE0 + this.xytex, 2, this._xys, this.ll_texture);\r\n' \
  '         }\r\n' \
  '        set teahs(a) {\r\n' \
  '          this._teahs = a;\r\n' \
  '          this.teah_texture = this.texture_load(this.gl.TEXTURE0 + this.teahtex, 4, this._teahs, this.teah_texture);\r\n' \
  '          this.vsss = this.buffer_load(3 * 4 * GPUStats.pad(this.tlength), this.gl.DYNAMIC_READ, this.vsss);\r\n' \
  '          this.vs = this.buffer_load(4 * GPUStats.pad(this.tlength), this.gl.DYNAMIC_READ, this.vs);\r\n' \
  '        }\r\n' \
  '        _calc() {\r\n' \
  '          for (let s=0; s<this._starts.length-1; s++) {\r\n' \
  '            let vlength = this._starts[s + 1] - this._starts[s];\r\n' \
  '            if (vlength == 0) {continue;}\r\n' \
  '            if (this.cur_prog == "pprogram" || this.cur_prog == "gwmprogram")  {\r\n' \
  '              this.trlat = Math.tan(this._rlats[s] / 2 + Math.PI / 4);\r\n' \
  '              this.program_uniforms();\r\n' \
  '            }\r\n' \
  '            if (this.mode == "explorer" && this.cur_prog == "gprogram") {\r\n' \
  '              this.rlat = this._rlats[s];\r\n' \
  '              this.program_uniforms();\r\n' \
  '            }\r\n' \
  '            this.program_feedbacks(this._starts[s], vlength);\r\n' \
  '            this.gl.beginTransformFeedback(this.gl.POINTS);\r\n' \
  '            this.gl.drawArraysInstanced(this.gl.POINTS, s, 1, vlength - ((this.cur_prog=="s2aprogram" || this.cur_prog=="s2bprogram")?1:0));\r\n' \
  '            this.gl.endTransformFeedback();\r\n' \
  '            this.gl.flush();\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        calc(param="") {\r\n' \
  '          let progs = [];\r\n' \
  '          if (this.mode == "explorer") {\r\n' \
  '            switch (param) {\r\n' \
  '              case "pos":\r\n' \
  '                progs = ["pprogram"];\r\n' \
  '                break;\r\n' \
  '              case "gdist":\r\n' \
  '              case "gwmdist":\r\n' \
  '                progs = [param.replace("dist", "program")];\r\n' \
  '              default:\r\n' \
  '                progs.push("s1aprogram", "s2aprogram", "s1bprogram", "s2bprogram");\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            progs = ["gprogram", "s1aprogram", "s2aprogram", "s1bprogram", "s2bprogram"];\r\n' \
  '          }\r\n' \
  '          for (let n of progs) {\r\n' \
  '            this.program_use(n);\r\n' \
  '            this.program_attributes();\r\n' \
  '            this.program_uniforms("static");\r\n' \
  '          }\r\n' \
  '          if (this.mode == "explorer" && param == "pos") {\r\n' \
  '            this.program_use("pprogram");\r\n' \
  '            this._calc();\r\n' \
  '            this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, null);\r\n' \
  '            this.feedbacks();\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '          if (this.mode != "explorer" || param == "gdist" || param == "gwmdist") {\r\n' \
  '            this.program_use(param=="gwmdist"?"gwmprogram":"gprogram");\r\n' \
  '            this._calc();\r\n' \
  '            this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, null);\r\n' \
  '            this.g_texture = this.texture_load(this.gl.TEXTURE0 + this.gtex, 1, this.vg, this.g_texture);\r\n' \
  '            this.feedbacks();\r\n' \
  '          }\r\n' \
  '          this.program_use("s1aprogram");\r\n' \
  '          this._calc();\r\n' \
  '          this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, null);\r\n' \
  '          this.sss_texture = this.texture_load(this.gl.TEXTURE0 + this.ssstex, 3, this.vsss, this.sss_texture);\r\n' \
  '          this.program_use("s2aprogram");\r\n' \
  '          this._calc();\r\n' \
  '          this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, null);\r\n' \
  '          this.feedbacks();\r\n' \
  '          this.sss_texture = this.texture_load(this.gl.TEXTURE0 + this.ssstex, 3, this.vsss, this.sss_texture);\r\n' \
  '          this.program_use("s1bprogram");\r\n' \
  '          this._calc();\r\n' \
  '          this.gl.bindTransformFeedback(this.gl.TRANSFORM_FEEDBACK, null);\r\n' \
  '          this.s_texture = this.texture_load(this.gl.TEXTURE0 + this.stex, 1, this.vs, this.s_texture);\r\n' \
  '          this.program_use("s2bprogram");\r\n' \
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
  '        get lls() {\r\n' \
  '          return this._lls;\r\n' \
  '        }\r\n' \
  '        get xys() {\r\n' \
  '          return this._xys;\r\n' \
  '        }\r\n' \
  '        get gs() {\r\n' \
  '          return this._gs;\r\n' \
  '        }\r\n' \
  '        get ssss() {\r\n' \
  '          return this._ssss;\r\n' \
  '        }\r\n' \
  '        get ss() {\r\n' \
  '          return this._ss;\r\n' \
  '        }\r\n' \
  '      }\r\n'
  HTML_MSG_TEMPLATE = \
  '      var msg_n = 0;\r\n' \
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
  '      }\r\n'
  HTML_TILES_TEMPLATE = \
  '      function set_opacities(){\r\n' \
  '        let oform = document.getElementById("oform");\r\n' \
  '        while (oform.firstElementChild) {oform.removeChild(oform.lastElementChild);}\r\n' \
  '        let rules = document.styleSheets[0].cssRules;\r\n' \
  '        let nrule = rules.length;\r\n' \
  '        for (let irule=nrule-1; irule>=0; irule--) {\r\n' \
  '          if ((rules[irule].selectorText || "").indexOf("tile-") > 0) {document.styleSheets[0].deleteRule(irule);}\r\n' \
  '        }\r\n' \
  '        nrule = rules.length;\r\n' \
  '        if (tlayers.has(tset)) {\r\n' \
  '          let tlays = tlayers.get(tset);\r\n' \
  '          if (! opacities.has(tset)) {\r\n' \
  '            opacities.set(tset, tlays.map((l)=>l[1].replace("x", "")));\r\n' \
  '          }\r\n' \
  '          let opcts = opacities.get(tset);\r\n' \
  '          let tiset = document.getElementById("tset");\r\n' \
  '          for (let l=0; l<tlays.length; l++) {\r\n' \
  '            let ls = l.toString();\r\n' \
  '            if (l > 0) {\r\n' \
  '              let e = document.createElement("br");\r\n' \
  '              oform.appendChild(e);\r\n' \
  '            }\r\n' \
  '            let e = document.createElement("label");\r\n' \
  '            e.htmlFor = "opacityl" + ls;\r\n' \
  '            e.innerHTML = tiset.options[tlays[l][0]].innerHTML;\r\n' \
  '            e.title = "{#jopacityreset#}";\r\n' \
  '            e.ondblclick = (e) => {if (e.shiftKey) {let inp=e.target.parentNode.getElementsByTagName("input");tlays.forEach((o, i) => {inp[i].value=tlays[i][1].replace("x", "");inp[i].dispatchEvent(new Event("input"));})} else {let inp=e.target.nextElementSibling;inp.value=tlays[l][1].replace("x", "");inp.dispatchEvent(new Event("input"));};};\r\n' \
  '            oform.appendChild(e);\r\n' \
  '            e = document.createElement("input");\r\n' \
  '            e.type = "range";\r\n' \
  '            e.name = e.id = "opacityl" + ls;\r\n' \
  '            e.min = "0";\r\n' \
  '            e.max = "1";\r\n' \
  '            e.step = "0.01";\r\n' \
  '            e.value = opcts[l];\r\n' \
  '            e.oninput = (e) => {e.target.nextElementSibling.innerHTML=(parseFloat(e.target.value)*100).toFixed(0)+" %";opacities.get(tset)[l]=e.target.value;document.documentElement.style.setProperty("--opacity" + ls, e.target.value);};\r\n' \
  '            e.onfocus = (e) => {e.target.previousElementSibling.style.color=e.target.nextElementSibling.style.color="rgb(200, 250,240)";};\r\n' \
  '            e.onblur = (e) => {e.target.previousElementSibling.style.color=e.target.nextElementSibling.style.color="";}\r\n' \
  '            oform.appendChild(e);\r\n' \
  '            e = document.createElement("span");\r\n' \
  '            e.id = "opacity" + ls;\r\n' \
  '            e.innerHTML = (parseFloat(opcts[l])*100).toFixed(0)+" %";\r\n' \
  '            oform.appendChild(e);\r\n' \
  '            document.documentElement.style.setProperty("--opacity" + ls, opcts[l]);\r\n' \
  '            if (layers[l].ext != ".json") {\r\n' \
  '              document.styleSheets[0].insertRule("div[id=handle]>img[id^=tile-" + ls + "] {opacity:var(--opacity" + ls + ");z-index:" + (l-tlays.length).toString() + (tlays[l][1].indexOf("x")>=0?";mix-blend-mode:multiply":"") + ";}", nrule++);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        } else if (layers[0].ext != ".json") {\r\n' \
  '          document.styleSheets[0].insertRule("div[id=handle]>img[id^=tile-0] {z-index:-1;}", nrule);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function set_jmaps() {\r\n' \
  '        if (tmaplibre != true) {return;}\r\n' \
  '        for (let jm=0; jm<jmaps.length; jm++) {\r\n' \
  '          jmaps[jm].remove();\r\n' \
  '          viewpane.removeChild(document.getElementById("jmap" + jm.toString()));\r\n' \
  '        }\r\n' \
  '        jmaps = [];\r\n' \
  '        let [lat, lon] = WebMercatortoWGS84(htopx + (viewpane.offsetWidth / 2 - hpx) * tscale / zoom, htopy - (viewpane.offsetHeight / 2 - hpy) * tscale / zoom);\r\n' \
  '        let tlays = null;\r\n' \
  '        if (tlayers.has(tset)) {tlays = tlayers.get(tset);}\r\n' \
  '        for (let l=0; l<layers.length; l++) {\r\n' \
  '          if (layers[l].ext != ".json") {continue;}\r\n' \
  '          let jdiv = document.createElement("div");\r\n' \
  '          jdiv.id = "jmap" + jmaps.length.toString();\r\n' \
  '          jdiv.style.zIndex = (l - layers.length).toString();\r\n' \
  '          if (tlays != null) {\r\n' \
  '            jdiv.style.opacity = "var(--opacity" + l.toString() + ")";\r\n' \
  '            if (tlays[l][1].indexOf("x")>=0) {jdiv.style.mixBlendMode = "multiply";}\r\n' \
  '          }\r\n' \
  '          viewpane.insertBefore(jdiv, handle);\r\n' \
  '          try {\r\n' \
  '            jmaps.push(new maplibregl.Map({container: jdiv, interactive: false, attributionControl: false, trackResize: false, renderWorldCopies: false, style: "jsontiles/style/" + (tlayers.has(tset)?tlayers.get(tset)[l][0]:tset).toString() + "/style.json", center: [lon, lat], zoom: tlevels[tlevel][0] - 1}));\r\n' \
  '          } catch(error) {\r\n' \
  '            viewpane.removeChild(jdiv);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function load_tcb(t, nset, nlevel, kzoom=false) {\r\n' \
  '        if (t.status != 200) {\r\n' \
  '          document.getElementById("tset").selectedIndex = tset;\r\n' \
  '          if (nset == null) {\r\n' \
  '            tlevel = nlevel || 1;\r\n' \
  '            layers = [];\r\n' \
  '            if (treset == 2) {set_jmaps();}\r\n' \
  '            for (const jmap of jmaps) {\r\n' \
  '              jmap.setZoom(tlevels[tlevel][0] - 1);\r\n' \
  '              for (const e of Object.entries(jmap.style.sourceCaches)) {\r\n' \
  '                try {e[1].clearTiles();} catch(error) {null;}\r\n' \
  '              };\r\n' \
  '            }\r\n' \
  '            if (! kzoom && tlevels.length > 0) {zoom_s = tlevels[tlevel][1];}\r\n' \
  '          }\r\n' \
  '          document.getElementById("tset").disabled = false;\r\n' \
  '          document.getElementById("tset").style.pointerEvents = "";\r\n' \
  '          if (treset == 0) {treset = 1;}\r\n' \
  '          rescale();\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let msg = JSON.parse(t.response);\r\n' \
  '        if (nset == null) {\r\n' \
  '          if (treset == 2 && tmaplibre == false) {\r\n' \
  '            if (msg.layers.some((l)=>l.ext==".json")) {\r\n' \
  '              let sc = document.createElement("script");\r\n' \
  '              sc.src = "/jsontiles/maplibre_js/##TMAPLIBREJS##";\r\n' \
  '              let li = document.createElement("link");\r\n' \
  '              li.href = "/jsontiles/maplibre_css/##TMAPLIBRECSS##";\r\n' \
  '              li.rel = "stylesheet";\r\n' \
  '              sc.onload = li.onload = (e) => {if (tmaplibre==false) {tmaplibre=true;} else {load_tcb(t,nset,nlevel,kzoom);if (tmaplibre==null) {sc.remove();li.remove();};};};\r\n' \
  '              sc.onerror = li.onerror = (e) => {if (tmaplibre!=false) {tmaplibre=null;load_tcb(t,nset,nlevel,kzoom);sc.remove();li.remove();} else {tmaplibre=null;};};\r\n' \
  '              document.head.insertBefore(sc, document.head.getElementsByTagName("script")[0]);\r\n' \
  '              document.head.insertBefore(li, document.head.getElementsByTagName("script")[1]);\r\n' \
  '              return;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (nlevel == null) {\r\n' \
  '            if (tlock) {switch_tlock(false);}\r\n' \
  '            tlevel = msg.level;\r\n' \
  '          } else {\r\n' \
  '            tlevel = nlevel;\r\n' \
  '          }\r\n' \
  '          if (! kzoom || nlevel == null) {zoom_s = tlevels[tlevel][1];}\r\n' \
  '          layers = msg.layers;\r\n' \
  '          layersc = Array(layers.length).fill([null, null, null, null]);\r\n' \
  '          let tscale_ex = tscale;\r\n' \
  '          tscale = msg.scale;\r\n' \
  '          if (treset == 2) {\r\n' \
  '            set_jmaps();\r\n' \
  '            set_opacities();\r\n' \
  '          } else {\r\n' \
  '            let [lat, lon] = WebMercatortoWGS84(htopx + (viewpane.offsetWidth / 2 - hpx) * tscale / zoom, vmaxy, htopy - (viewpane.offsetHeight / 2 - hpy) * tscale / zoom);\r\n' \
  '            for (const jmap of jmaps) {\r\n' \
  '              jmap.setZoom(tlevels[tlevel][0] - 1);\r\n' \
  '              jmap.setCenter([lon, lat]);\r\n' \
  '              for (const e of Object.entries(jmap.style.sourceCaches)) {\r\n' \
  '                try {\r\n' \
  '                  e[1].clearTiles();\r\n' \
  '                  jmap.getSource(e[0]).load();\r\n' \
  '                } catch(error) {null;}\r\n' \
  '              };\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          treset = 1;\r\n' \
  '          rescale(tscale_ex);\r\n' \
  '          document.getElementById("tset").disabled = false;\r\n' \
  '          document.getElementById("tset").style.pointerEvents = "";\r\n' \
  '        } else {\r\n' \
  '          treset = 2;\r\n' \
  '          tset = document.getElementById("tset").selectedIndex;\r\n' \
  '          let matrix = null;\r\n' \
  '          let lf = false;\r\n' \
  '          if (nlevel == null) {\r\n' \
  '            tlevels = msg.tlevels;\r\n' \
  '          } else if (nlevel >= 0) {\r\n' \
  '            tlevels = msg.tlevels;\r\n' \
  '            if (nlevel == 0) {\r\n' \
  '              nlevel = tlevels[0];\r\n' \
  '              zoom_s = tlevels[nlevel][1];\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            matrix = tlevels[tlevel][0];\r\n' \
  '            tlevels = msg.tlevels;\r\n' \
  '            nlevel = 1;\r\n' \
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
  '      }\r\n' \
  '      function error_tcb() {\r\n' \
  '        document.getElementById("tset").selectedIndex = tset;\r\n' \
  '        document.getElementById("tset").disabled = false;\r\n' \
  '        document.getElementById("tset").style.pointerEvents = "";\r\n' \
  '        cpx = cpy = null;\r\n' \
  '      }\r\n' \
  '      function add_tile(row=0, col=0, suf="", pref="", width="", height="", oleft=0, otop=0) {\r\n' \
  '        let tile = document.createElement("img");\r\n' \
  '        if (mode == "map") {\r\n' \
  '          tile.id = "map";\r\n' \
  '          width = "calc(var(--zoom) * " + twidth.toString() + "px)";\r\n' \
  '          height = "calc(var(--zoom) * " + theight.toString() + "px)";\r\n' \
  '          oleft = (ttopx - htopx) / tscale;\r\n' \
  '          otop = (htopy - ttopy) / tscale;\r\n' \
  '          if (text == ".tif") {\r\n' \
  '            tile.onerror =  function(e) {tile.onerror = null; text = ".png"; tile.src = "/map/" + tile.id + text;};\r\n' \
  '          }\r\n' \
  '          tile.src = "/map/" + tile.id + text;\r\n' \
  '          tile.style.zIndex = -1;\r\n' \
  '        } else {\r\n' \
  '          let tpos = row.toString() + "-" + col.toString();\r\n' \
  '          tile.id = pref + tpos;\r\n' \
  '          let port = portmin + (row + col) % (portmax + 1 - portmin);\r\n' \
  '          tile.src = "http://" + host + port.toString() + "/tiles/tile-" + tpos + (suf || (text + "?" + document.getElementById("tset").selectedIndex.toString() + "," + document.getElementById("matrix").innerHTML));\r\n' \
  '        }\r\n' \
  '        tile.alt = "";\r\n' \
  '        tile.style.position = "absolute";\r\n' \
  '        tile.style.width = width;\r\n' \
  '        tile.style.height = height;\r\n' \
  '        tile.style.left = "calc(var(--zoom) * " + (oleft + col * twidth).toString() + "px)";\r\n' \
  '        tile.style.top = "calc(var(--zoom) * " + (otop + row * theight).toString() + "px)";\r\n' \
  '        handle.insertBefore(tile, handle.firstElementChild);\r\n' \
  '        return tile;\r\n' \
  '      }\r\n' \
  '      function update_tiles() {\r\n' \
  '        if (mode == "map") {return;}\r\n' \
  '        let tiles = Array.from(handle.getElementsByTagName("img"));\r\n' \
  '        if (treset >= 1) {\r\n' \
  '          tiles.forEach((t) => handle.removeChild(t));\r\n' \
  '          tiles = [];\r\n' \
  '        }\r\n' \
  '        for (let l=0; l<layers.length; l++) {\r\n' \
  '          let layer = layers[l];\r\n' \
  '          let tmatrix = layer.matrix;\r\n' \
  '          ttopx = layer.topx;\r\n' \
  '          ttopy = layer.topy;\r\n' \
  '          twidth = layer.width;\r\n' \
  '          theight = layer.height;\r\n' \
  '          text = layer.ext;\r\n' \
  '          if (text == ".json" || twidth == 0 || theight == 0) {continue;}\r\n' \
  '          let [cleft, cright, ctop, cbottom] = layersc[l];\r\n' \
  '          let vleft = -hpx / zoom + (htopx - ttopx) / tscale;\r\n' \
  '          let vtop = -hpy / zoom + (ttopy - htopy) / tscale;\r\n' \
  '          let vright = vleft + viewpane.offsetWidth / zoom;\r\n' \
  '          let vbottom = vtop + viewpane.offsetHeight / zoom;\r\n' \
  '          let rleft = parseInt(vleft / twidth - 1.5);\r\n' \
  '          let rright = parseInt(vright / twidth + 1.5);\r\n' \
  '          let rtop = parseInt(vtop / theight - 1.5);\r\n' \
  '          let rbottom = parseInt(vbottom / theight + 1.5);\r\n' \
  '          if (treset >= 1) {\r\n' \
  '            cleft = rright + 1;\r\n' \
  '            cright = rleft - 1;\r\n' \
  '            ctop = rbottom + 1;\r\n' \
  '            cbottom = rtop - 1;\r\n' \
  '          }\r\n' \
  '          let iwidth = "calc(var(--zoom) * " + twidth.toString() + "px)";\r\n' \
  '          let iheight = "calc(var(--zoom) * " + theight.toString() + "px)";\r\n' \
  '          let ioleft = (ttopx - htopx) / tscale;\r\n' \
  '          let iotop = (htopy - ttopy) / tscale;\r\n' \
  '          if (rleft != cleft || rright != cright || rtop != ctop || rbottom != cbottom) {\r\n' \
  '            for (let tile of tiles) {\r\n' \
  '              let [tlayer, row, col] = tile.id.split("-").slice(1, 4).map(Number);\r\n' \
  '              if (tlayer == l && (row < rtop || row > rbottom || col < rleft || col > rright)) {\r\n' \
  '                handle.removeChild(tile);\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            let suf = text + "?" + (tlayers.has(document.getElementById("tset").selectedIndex)?tlayers.get(document.getElementById("tset").selectedIndex)[l][0]:document.getElementById("tset").selectedIndex).toString() + "," + tmatrix;\r\n' \
  '            let pref = "tile-" + l.toString() + "-";\r\n' \
  '            if (tiles_hold == null) {\r\n' \
  '              for (let row=rtop; row<=rbottom; row++) {\r\n' \
  '                for (let col=rleft; col<=rright; col++) {\r\n' \
  '                  if (col < cleft || col > cright || row < ctop || row > cbottom) {add_tile(row, col, suf, pref, iwidth, iheight, ioleft, iotop);}\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '            } else {\r\n' \
  '              for (let row=rtop; row<=rbottom; row++) {\r\n' \
  '                for (let col=rleft; col<=rright; col++) {\r\n' \
  '                  if (col < cleft || col > cright || row < ctop || row > cbottom) {\r\n' \
  '                    let tpos = row.toString() + "-" + col.toString();\r\n' \
  '                    let tk = "tile-" + tpos + suf;\r\n' \
  '                    let tile = tiles_hold.get(tk);\r\n' \
  '                    if (tile) {\r\n' \
  '                      tiles_hold.delete(tk);\r\n' \
  '                      if (tile.naturalWidth) {\r\n' \
  '                        tile.id = pref + tpos;\r\n' \
  '                        handle.insertBefore(tile, handle.firstElementChild);\r\n' \
  '                      } else {\r\n' \
  '                        tile = add_tile(row, col, suf, pref, iwidth, iheight, ioleft, iotop);\r\n' \
  '                      }\r\n' \
  '                    } else {\r\n' \
  '                      tile = add_tile(row, col, suf, pref, iwidth, iheight, ioleft, iotop);\r\n' \
  '                    }\r\n' \
  '                    tiles_hold.set(tk, tile);\r\n' \
  '                  }\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              let thr = tiles_hold.size - tholdsize - (rright - rleft + 1) * (rbottom - rtop + 1) ;\r\n' \
  '              if (thr > 0) {\r\n' \
  '                for (const tk of tiles_hold.keys()) {\r\n' \
  '                  tiles_hold.delete(tk);\r\n' \
  '                  thr--;\r\n' \
  '                  if (! thr) {break;}\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            cleft = rleft;\r\n' \
  '            cright = rright;\r\n' \
  '            ctop = rtop;\r\n' \
  '            cbottom = rbottom;\r\n' \
  '            layersc[l] = [cleft, cright, ctop, cbottom];\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (treset == 1) {treset = 0;}\r\n' \
  '        if (jmaps.length > 0) {\r\n' \
  '          let [lat, lon] = WebMercatortoWGS84(htopx + (viewpane.offsetWidth / 2 - hpx) * tscale / zoom, htopy - (viewpane.offsetHeight / 2 - hpy) * tscale / zoom);\r\n' \
  '          for (const jmap of jmaps) {\r\n' \
  '            jmap.setCenter([lon, lat]);\r\n' \
  '          }\r\n' \
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
  '        update_tiles();\r\n' \
  '      }\r\n'
  HTML_UTIL_TEMPLATE = \
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
  '      function scroll_dview(dx, dy) {\r\n' \
  '        hpx += dx;\r\n' \
  '        hpy += dy;\r\n' \
  '        reframe();\r\n' \
  '      }\r\n' \
  '      function WGS84toWebMercator(lat, lon) {\r\n' \
  '        return [lon * Math.PI / 180 * 6378137, Math.log(Math.tan(Math.PI / 4 + lat * Math.PI / 360)) * 6378137];\r\n' \
  '      }\r\n' \
  '      function WebMercatortoWGS84(x, y) {\r\n' \
  '        return [(2 * Math.atan(Math.exp(y / 6378137)) - Math.PI / 2) * 180 / Math.PI, x * 180 / Math.PI / 6378137];\r\n' \
  '      }\r\n' \
  '      function distance(lat1, lon1, ele1, lat2, lon2, ele2) {\r\n' \
  '        let d = 2 * 6378137 * Math.asin(Math.sqrt((Math.sin((lat2 - lat1) * Math.PI / 360)) ** 2 + Math.cos(lat1 * Math.PI / 180) * Math.cos (lat2 * Math.PI / 180) * (Math.sin((lon2 - lon1) * Math.PI / 360)) ** 2));\r\n' \
  '        if (ele1 != null && ele2 != null) {d = Math.sqrt(d ** 2 + (ele2 - ele1) ** 2);}\r\n' \
  '        return d;\r\n' \
  '      }\r\n' \
  '      function slope(gdist, heig) {\r\n' \
  '        return gdist>0?(heig / gdist):(parseFloat(document.getElementById("slmax").innerHTML) / 100 * (heig==0?0:(heig>0?1:-1)));\r\n' \
  '      }\r\n' \
  '      function escape(s) {\r\n' \
  '        return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");\r\n' \
  '      }\r\n'
  HTML_SCROLL_TEMPLATE = \
  '      function scroll_to_track(track=null, center=true, b=0) {\r\n' \
  '        if (b == 0) {b = track_boundaries(track);}\r\n' \
  '        if (b == null) {\r\n' \
  '          if (track == null) {\r\n' \
  '            hpx = viewpane.offsetWidth / 2 + (htopx - defx) * zoom / tscale;\r\n' \
  '            hpy = viewpane.offsetHeight / 2 + (defy - htopy) * zoom / tscale;\r\n' \
  '          }\r\n' \
  '          reframe();\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (center || b[1] - b[0] > viewpane.offsetWidth * tscale / zoom) {\r\n' \
  '          hpx = viewpane.offsetWidth / 2 - (b[0] + b[1]) / 2 * zoom / tscale;\r\n' \
  '        } else {\r\n' \
  '          hpx = Math.max(Math.min(hpx, - b[1] * zoom / tscale + viewpane.offsetWidth), - b[0] * zoom / tscale);\r\n' \
  '        }\r\n' \
  '        if (center || b[3] - b[2] > viewpane.offsetHeight * tscale / zoom) {\r\n' \
  '          hpy = viewpane.offsetHeight / 2 - (b[2] + b[3]) / 2 * zoom / tscale;\r\n' \
  '        } else {\r\n' \
  '          hpy = Math.max(Math.min(hpy, - b[3] * zoom / tscale + viewpane.offsetHeight), - b[2] * zoom / tscale);\r\n' \
  '        }\r\n' \
  '        reframe();\r\n' \
  '      }\r\n'
  HTML_SEGCALC_1_TEMPLATE = \
  '          let stat = Array(8).fill(0);\r\n' \
  '          let stat_p = null;\r\n' \
  '          let stat_i = 0;\r\n' \
  '          let t_s = null;\r\n' \
  '          let lat_p = null;\r\n' \
  '          let lon_p = null;\r\n' \
  '          let lat = null;\r\n' \
  '          let lon = null;\r\n' \
  '          let ea_s = [0, 0];\r\n' \
  '          let ea_p = [NaN, NaN];\r\n' \
  '          let ea_r = [NaN, NaN];\r\n' \
  '          let ea_b = [NaN, NaN];\r\n' \
  '          let ea_g = [null, null];\r\n' \
  '          let ea_ic = [null, null];\r\n' \
  '          let ea_f = [parseFloat(document.getElementById("egstren").innerHTML), parseFloat(document.getElementById("agstren").innerHTML)];\r\n' \
  '          let el_s = 0;\r\n' \
  '          let el = null;\r\n' \
  '          let el_p = NaN;\r\n' \
  '          let p_p = null;\r\n'
  HTML_SEGCALC_2_TEMPLATE = \
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
  '            }\r\n'
  HTML_SEGCALC_3_TEMPLATE = \
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
  '              stats[seg_ind][stat_i][6] = stat_p[6];\r\n' \
  '            }\r\n' \
  '            stat_i++;\r\n' \
  '            p_p = p;\r\n' \
  '            if (gpucomp <= 1 && fpan <= 1) {\r\n' \
  '              for (let v=0; v<2; v++) {\r\n' \
  '                if (! isNaN(ea[v])) {\r\n' \
  '                  if (ea[v] >= ea_r[v] && ea_g[v] == "+") {\r\n' \
  '                    ea_r[v] = ea_b[v] = ea[v];\r\n' \
  '                  } else if (ea[v] > ea_r[v] + ea_f[v]) {\r\n' \
  '                    ea_r[v] = ea_b[v] = ea[v];\r\n' \
  '                    ea_g[v] = "+";\r\n' \
  '                    ea_ic[v] = null;\r\n' \
  '                  } else if ((ea[v] <= ea_r[v] && ea_g[v] == "-") || ea[v] < ea_r[v] - ea_f[v]) {\r\n' \
  '                    if (ea_ic[v] != null) {\r\n' \
  '                      stat_p[v + 2] = stats[seg_ind][ea_ic[v]][v + 2];\r\n' \
  '                      for (let i=ea_ic[v]+1; i<stat_i; i++) {stats[seg_ind][i][v + 2] = stat_p[v + 2];}\r\n' \
  '                      ea_ic[v] = null;\r\n' \
  '                    }\r\n' \
  '                    ea_r[v] = ea_b[v] = ea[v];\r\n' \
  '                    ea_g[v] = "-";\r\n' \
  '                  } else if (ea[v] > ea_b[v]) {\r\n' \
  '                    ea_b[v] = ea[v];\r\n' \
  '                    if (ea_ic[v] == null) {ea_ic[v] = stat_i - 2;}\r\n' \
  '                  }\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            if (! isNaN(ea[0])) {ea_p[0] = ea[0];}\r\n' \
  '            if (! isNaN(ea[1])) {ea_p[1] = ea[1];}\r\n' \
  '          }\r\n' \
  '          for (let v=0; v<2; v++) {\r\n' \
  '            if (ea_ic[v] != null) {\r\n' \
  '              stat_p[v + 2] = stats[seg_ind][ea_ic[v]][v + 2];\r\n' \
  '              for (let i=ea_ic[v]+1; i<stat_i; i++) {stats[seg_ind][i][v + 2] = stat_p[v + 2];}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (! stat_p) {return;}\r\n' \
  '          if (gpucomp == 0 && (fpan == 0 || fpan == 2)) {\r\n' \
  '            for (let p=0; p<stat_i; p++) {\r\n' \
  '              if (isNaN(stats[seg_ind][p][4])) {\r\n' \
  '                stats[seg_ind][p][4] = ea_s[0];\r\n' \
  '                if (isNaN(stats[seg_ind][p][5])) {\r\n' \
  '                  stats[seg_ind][p][5] = ea_s[1];\r\n' \
  '                  stats[seg_ind][p][6] = el_s;\r\n' \
  '                }\r\n' \
  '              } else if (isNaN(stats[seg_ind][p][5])) {\r\n' \
  '                stats[seg_ind][p][5] = ea_s[1];\r\n' \
  '              } else {break;}\r\n' \
  '            }\r\n'
  HTML_SEGCALC_4_TEMPLATE = \
  '          if (gpucomp == 0 && (fpan == 0 || fpan == 2)) {\r\n' \
  '            let drange = Math.max(0.01, parseFloat(document.getElementById("sldist").innerHTML)) / 2;\r\n' \
  '            let slmax = parseFloat(document.getElementById("slmax").innerHTML) / 100;\r\n' \
  '            for (let p=0; p<stats[seg_ind].length; p++) {\r\n' \
  '              let ea = stats[seg_ind][p].slice(4,6);\r\n' \
  '              let el = stats[seg_ind][p][6];\r\n' \
  '              stats[seg_ind][p][4]=0;\r\n' \
  '              stats[seg_ind][p][5]=0;\r\n' \
  '              stats[seg_ind][p][6]=0;\r\n' \
  '              let ps = p;\r\n' \
  '              let b = false;\r\n' \
  '              let dt = 0;\r\n' \
  '              for (ps=p+1; ps<stats[seg_ind].length; ps++) {\r\n' \
  '                if (stats[seg_ind][ps][1] > stats[seg_ind][p][1] + drange && b) {break;}\r\n' \
  '                let d = stats[seg_ind][ps][1] - stats[seg_ind][ps-1][1];\r\n' \
  '                if (d == 0) {continue;}\r\n' \
  '                b = true;\r\n' \
  '                dt += d;\r\n' \
  '                stats[seg_ind][p][4] += slope(dt, stats[seg_ind][ps][4] - ea[0]) * d;\r\n' \
  '                stats[seg_ind][p][5] += slope(dt, stats[seg_ind][ps][5] - ea[1]) * d;\r\n' \
  '                stats[seg_ind][p][6] += slope(dt, stats[seg_ind][ps][6] - el) * d;\r\n' \
  '              }\r\n' \
  '              if (ps - 1 > p) {\r\n' \
  '                stats[seg_ind][p][4] = (stats[seg_ind][p][4] + slope(dt, stats[seg_ind][ps-1][4] - ea[0]) * (drange - dt)) / drange;\r\n' \
  '                stats[seg_ind][p][5] = (stats[seg_ind][p][5] + slope(dt, stats[seg_ind][ps-1][5] - ea[1]) * (drange - dt)) / drange;\r\n' \
  '                stats[seg_ind][p][6] = (stats[seg_ind][p][6] + slope(dt, stats[seg_ind][ps-1][6] - el) * (drange - dt)) / drange;\r\n' \
  '              }\r\n' \
  '              stats[seg_ind][p][4] = Math.max(Math.min(stats[seg_ind][p][4], slmax), -slmax);\r\n' \
  '              stats[seg_ind][p][5] = Math.max(Math.min(stats[seg_ind][p][5], slmax), -slmax);\r\n' \
  '              stats[seg_ind][p][6] = Math.max(Math.min(stats[seg_ind][p][6], slmax), -slmax);\r\n' \
  '            }\r\n' \
  '            for (let p=stats[seg_ind].length-2; p>0; p--) {\r\n' \
  '              let ps = p;\r\n' \
  '              let s = [0, 0, 0];\r\n' \
  '              let su = 0;\r\n' \
  '              for (ps=p-1; ps>=0; ps--) {\r\n' \
  '                if (stats[seg_ind][ps][1] < stats[seg_ind][p][1] - drange) {break;}\r\n' \
  '                let c = (stats[seg_ind][ps+1][1] - stats[seg_ind][ps][1]) / (stats[seg_ind][p][1] - stats[seg_ind][ps][1] + 1);\r\n' \
  '                s[0] += stats[seg_ind][ps][4] * c;\r\n' \
  '                s[1] += stats[seg_ind][ps][5] * c;\r\n' \
  '                s[2] += stats[seg_ind][ps][6] * c;\r\n' \
  '                su += c;\r\n' \
  '              }\r\n' \
  '              if (stats[seg_ind][p][1] - stats[seg_ind][ps+1][1] != 0) {\r\n' \
  '                stats[seg_ind][p][4] = Math.max(-slmax, Math.min(slmax, (stats[seg_ind][p][4] + s[0]/2 ) / (1 + su/2)));\r\n' \
  '                stats[seg_ind][p][5] = Math.max(-slmax, Math.min(slmax, (stats[seg_ind][p][5] + s[1]/2 ) / (1 + su/2)));\r\n' \
  '                stats[seg_ind][p][6] = Math.max(-slmax, Math.min(slmax, (stats[seg_ind][p][6] + s[2]/2 ) / (1 + su/2)));\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            let sl = stats[seg_ind][0][6];\r\n' \
  '            stats[seg_ind][0][6] = 0;\r\n' \
  '            for (let p=1; p<stats[seg_ind].length; p++) {\r\n' \
  '              let nsl = stats[seg_ind][p][6];\r\n' \
  '              stats[seg_ind][p][6] = stats[seg_ind][p - 1][6] + (stats[seg_ind][p][1] - stats[seg_ind][p - 1][1]) * Math.sqrt(1 + sl ** 2);\r\n' \
  '              sl = nsl;\r\n' \
  '            }\r\n' \
  '            stat_p[6] = stats[seg_ind][stats[seg_ind].length - 1][6];\r\n' \
  '          }\r\n'
  HTML_SEGCALC_5_TEMPLATE = \
  '        if (gpucomp == 0 && (fpan == 0 || fpan == 3)) {\r\n' \
  '          let trange = parseFloat(document.getElementById("sptime").innerHTML) / 2;\r\n' \
  '          let spmax = parseFloat(document.getElementById("spmax").innerHTML) / 3.6;\r\n' \
  '          for (let p=0; p<stats[seg_ind].length; p++) {\r\n' \
  '            stats[seg_ind][p][7] = 0;\r\n' \
  '            let ps = p;\r\n' \
  '            for (ps=p+1; ps<stats[seg_ind].length; ps++) {\r\n' \
  '              if (stats[seg_ind][ps][0] > stats[seg_ind][p][0] + trange) {break;}\r\n' \
  '              if (stats[seg_ind][ps][0] == stats[seg_ind][p][0]) {continue;}\r\n' \
  '              stats[seg_ind][p][7] += (stats[seg_ind][ps][6] - stats[seg_ind][p][6]) / (stats[seg_ind][ps][0] - stats[seg_ind][p][0]) * (stats[seg_ind][ps][0] - stats[seg_ind][ps-1][0]);\r\n' \
  '            }\r\n' \
  '            if (stats[seg_ind][ps-1][0] - stats[seg_ind][p][0] != 0) {\r\n' \
  '              stats[seg_ind][p][7] = (stats[seg_ind][p][7] + (stats[seg_ind][ps-1][6] - stats[seg_ind][p][6]) / (stats[seg_ind][ps-1][0] - stats[seg_ind][p][0]) * (trange + stats[seg_ind][p][0] - stats[seg_ind][ps-1][0])) / trange;\r\n' \
  '            }\r\n' \
  '            stats[seg_ind][p][7] = Math.min(stats[seg_ind][p][7], spmax);\r\n' \
  '          }\r\n' \
  '          for (let p=stats[seg_ind].length-2; p>0; p--) {\r\n' \
  '            if (stats[seg_ind][p+1][0] - stats[seg_ind][p][0] <= trange) {\r\n' \
  '              let ps = p;\r\n' \
  '              let s = 0;\r\n' \
  '              let su = 0;\r\n' \
  '              for (ps=p-1; ps>=0; ps--) {\r\n' \
  '                if (stats[seg_ind][ps][0] < stats[seg_ind][p][0] - trange) {break;}\r\n' \
  '                let c = (stats[seg_ind][ps+1][0] - stats[seg_ind][ps][0]) / (stats[seg_ind][p][0] - stats[seg_ind][ps][0] + 1);\r\n' \
  '                s += stats[seg_ind][ps][7] * c;\r\n' \
  '                su += c;\r\n' \
  '              }\r\n' \
  '              if (stats[seg_ind][p][0] - stats[seg_ind][ps+1][0] != 0) {\r\n' \
  '                stats[seg_ind][p][7] = Math.min(spmax, (stats[seg_ind][p][7] + s/2 ) / (1 + su/2));\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n'
  HTML_GRAPH1_TEMPLATE = \
  '      function switch_dfpanel() {\r\n' \
  '        if (document.getElementById("dfpanel").style.display != "initial") {\r\n' \
  '          document.getElementById("dfpanel").style.display = "initial";\r\n' \
  '        } else {\r\n' \
  '          document.getElementById("dfpanel").style.display = "none";\r\n' \
  '        }\r\n' \
  '        for (let fp of [document.getElementById("filterpanel1"), document.getElementById("filterpanel2"), document.getElementById("filterpanel3")]) {fp.style.display = "none";}\r\n' \
  '        document.getElementById("v3Dpanel").style.display = "none";\r\n' \
  '      }\r\n' \
  '      function switch_filterpanel(pa) {\r\n' \
  '        let fp = [null, document.getElementById("filterpanel1"), document.getElementById("filterpanel2"), document.getElementById("filterpanel3")];\r\n' \
  '        for (let p=1; p<=3; p++) {\r\n' \
  '          if (p == pa && (pa != 1 || gpucomp <= 1)) {\r\n' \
  '            if (fp[p].style.display != "initial") {fp[p].style.display = "initial";} else {fp[p].style.display = "none";}\r\n' \
  '          } else {\r\n' \
  '            fp[p].style.display = "none";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        document.getElementById("dfpanel").style.display = "none";\r\n' \
  '        document.getElementById("mtpanel").style.display = "none";\r\n' \
  '        document.getElementById("v3Dpanel").style.display = "none";\r\n' \
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
  '            if (typeof graph_ip != typeof undefined) {\r\n' \
  '              graph_ip = null;\r\n' \
  '              graph_px = null;\r\n' \
  '            }\r\n' \
  '            graphc.setAttribute("width", graphc.getAttribute("width"));\r\n' \
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
  '        gctx.globalCompositeOperation = "copy";\r\n' \
  '        gctx.fillStyle = "rgba(0,0,0,0)";\r\n' \
  '        gctx.fillRect(0, 0, gwidth, gheight);\r\n' \
  '        gctx.globalCompositeOperation = "source-over";\r\n' \
  '        gctx.fillStyle = "rgb(40,45,50)";\r\n' \
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
  '        let gx_ind = document.getElementById("graphx").selectedIndex;\r\n' \
  '        let gy_ind = document.getElementById("graphy").selectedIndex;\r\n'
  HTML_GRAPH2_TEMPLATE = \
  '            let dr = true;\r\n' \
  '            switch (gy_ind) {\r\n' \
  '              case 0:\r\n' \
  '                gy.push(dist + stat[6]);\r\n' \
  '                break;\r\n' \
  '              case 1:\r\n' \
  '              case 2:\r\n' \
  '                if (isNaN(ea)) {\r\n' \
  '                  dr = false;\r\n' \
  '                } else {\r\n' \
  '                  gy.push(ea);\r\n' \
  '                }\r\n' \
  '                break;\r\n' \
  '              case 3:\r\n' \
  '                gy.push(ele + stat[2]);\r\n' \
  '                break;\r\n' \
  '              case 4:\r\n' \
  '                gy.push(alt + stat[3]);\r\n' \
  '                break;\r\n' \
  '              case 5:\r\n' \
  '              case 6:\r\n' \
  '                gy.push(stat[gy_ind - 1] * 100);\r\n' \
  '                break;\r\n' \
  '              case 7:\r\n' \
  '                gy.push(stat[7] * 3.6);\r\n' \
  '                break;\r\n' \
  '            }\r\n' \
  '            if (dr) {\r\n' \
  '              switch (gx_ind) {\r\n' \
  '                case 0:\r\n' \
  '                  gx.push(dur + stat[0]);\r\n' \
  '                  break;\r\n' \
  '                case 1:\r\n' \
  '                  gx.push(dist + stat[6]);\r\n' \
  '                  break;\r\n' \
  '              }\r\n'
  HTML_GRAPH3_TEMPLATE = \
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
  '        if (gy_ind == 0) {\r\n' \
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
  '        gctx.font = "10px sans-serif";\r\n' \
  '        gctx.textAlign = "center";\r\n' \
  '        gctx.textBaseline = "top";\r\n' \
  '        x = xl;\r\n' \
  '        while (x <= xr) {\r\n' \
  '          if (gx_ind == 0) {\r\n' \
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
  '            if (gy_ind == 0) {\r\n' \
  '              gctx.fillText(((maxy - (y - yt) / cy) / 1000).toFixed(1).replace(/^-(0*(\\.0*)?$)/,"$1") + "km", xl - 2, y);\r\n' \
  '            } else if (gy_ind == 5 || gy_ind == 6) {\r\n' \
  '              gctx.fillText((maxy - (y - yt) / cy).toFixed(0).replace(/^-(0*(\\.0*)?$)/,"$1") + "%", xl - 2, y);\r\n' \
  '            } else if (gy_ind == 7) {\r\n' \
  '              gctx.fillText((maxy - (y - yt) / cy).toFixed(1).replace(/^-(0*(\\.0*)?$)/,"$1") + "km/h", xl - 2, y);\r\n' \
  '            } else {\r\n' \
  '              gctx.fillText((maxy - (y - yt) / cy).toFixed(0).replace(/^-(0*(\\.0*)?$)/,"$1") + "m", xl - 2, y);\r\n' \
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
  '        gctx.beginPath();\r\n'
  HTML_MAP_TEMPLATE = \
  '      function switch_3Dpanel() {\r\n' \
  '        if (eset < 0) {show_msg("{#jmelevationsno#}", 10); return;}\r\n' \
  '        if (document.getElementById("v3Dpanel").style.display != "initial") {\r\n' \
  '          document.getElementById("v3Dpanel").style.display = "initial";\r\n' \
  '        } else {\r\n' \
  '          document.getElementById("v3Dpanel").style.display = "none";\r\n' \
  '        }\r\n' \
  '        document.getElementById("dfpanel").style.display = "none";\r\n' \
  '        document.getElementById("mtpanel").style.display = "none";\r\n' \
  '        for (let fp of [document.getElementById("filterpanel1"), document.getElementById("filterpanel2"), document.getElementById("filterpanel3")]) {fp.style.display = "none";}\r\n' \
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
  '        let r = zoom / zoom_ex * tscale_ex / tscale;\r\n' \
  '        let cx = cpx==null?(viewpane.offsetWidth/2):cpx;\r\n' \
  '        let cy = cpy==null?(viewpane.offsetHeight/2):cpy;\r\n' \
  '        cpx = cpy = null;\r\n' \
  '        hpx = cx * (1 - r) + hpx * r;\r\n' \
  '        hpy = cy * (1 - r) + hpy * r;\r\n' \
  '        if (mode != "map") {\r\n' \
  '          if (jmaps.length > 0) {\r\n' \
  '            for (const jmap of jmaps) {\r\n' \
  '              jmap.setPixelRatio(Math.max(zoom, Math.min(1.5 * zoom, 1)));\r\n' \
  '              jmap.resize();\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (focused && scrollmode > 0) {\r\n' \
  '          if (focused.indexOf("segment") >= 0) {\r\n' \
  '            scroll_to_track(document.getElementById(focused.replace("segment", "track")), scrollmode == 2);\r\n' \
  '          } else if (focused.indexOf("track") >= 0){\r\n' \
  '            scroll_to_track(document.getElementById(focused), scrollmode == 2);\r\n' \
  '          } else {\r\n' \
  '            scroll_to_dot(document.getElementById(focused.replace("point", "dot")), scrollmode == 2);\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          reframe();\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function switch_tlock(resc=true) {\r\n' \
  '        if (mode == "map" || (document.getElementById("tset").disabled && resc)) {return;}\r\n' \
  '        let zoom_s_ex = zoom_s;\r\n' \
  '        if (tlock) {\r\n' \
  '          if (tlevel == 0) {return;}\r\n' \
  '          document.getElementById("tlock").innerHTML = "&#128275;&#xfe0e;";\r\n' \
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
  '          document.getElementById("tlock").innerHTML = "&#128274;&#xfe0e;";\r\n' \
  '        }\r\n' \
  '        tlock = ! tlock;\r\n' \
  '        if (zoom_s == zoom_s_ex || ! resc) {return;}\r\n' \
  '        rescale();\r\n' \
  '      }\r\n' \
  '      function zoom_change(o, cx=null, cy=null) {\r\n' \
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
  '              cpx = cx;\r\n' \
  '              cpy = cy;\r\n' \
  '              switch_tiles(null, ntlevel);\r\n' \
  '              return;\r\n' \
  '            }\r\n' \
  '            tlevel = ntlevel;\r\n' \
  '            zoom_s = tlevels[tlevel][1];\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (zoom_s == zoom_s_ex) {return;}\r\n' \
  '        cpx = cx;\r\n' \
  '        cpy = cy;\r\n' \
  '        rescale();\r\n' \
  '      }\r\n' \
  '      function zoom_dec(cx=null, cy=null) {\r\n' \
  '        if (! document.getElementById("tset").disabled) {zoom_change(-1, cx, cy);}\r\n' \
  '      }\r\n' \
  '      function zoom_inc(cx=null, cy=null) {\r\n' \
  '        if (! document.getElementById("tset").disabled) {zoom_change(1, cx, cy);}\r\n' \
  '      }\r\n' \
  '      function map_adjust(s, t) {\r\n' \
  '        let adj = "adjustment_" + t;\r\n' \
  '        if (s == "-") {\r\n' \
  '          if (window[adj] > 0.19) {window[adj] -= 0.1;} else {return;}\r\n' \
  '        } else {\r\n' \
  '          if (window[adj] < 0.91) {window[adj] += 0.1;} else {return;}\r\n' \
  '        }\r\n' \
  '        Array.from(document.getElementById("attenuate").firstElementChild.children).forEach(function (f) {f.setAttribute("offset", (1.0 - adjustment_a).toFixed(1)); f.setAttribute("amplitude", adjustment_a.toFixed(1)); f.setAttribute("exponent", adjustment_e.toFixed(1));});\r\n' \
  '        if (adjustment_a < 0.91 || adjustment_e < 0.91) {\r\n' \
  '          if ((document.documentElement.style.getPropertyValue("--filter") || "").length <= 4) {document.documentElement.style.setProperty("--filter", "url(#attenuate)");}\r\n' \
  '        } else {\r\n' \
  '          document.documentElement.style.setProperty("--filter", "none");\r\n' \
  '        }\r\n' \
  '        show_msg("{#jmadjust#}".replace("%s", adjustment_a.toFixed(1)).replace("%s", adjustment_e.toFixed(1)), 2);\r\n' \
  '      }\r\n' \
  '      function scrollcross(sw=false) {\r\n' \
  '        if (sw) {\r\n' \
  '          scrollmode = (scrollmode + 1) % 3;\r\n' \
  '          document.getElementById("scrollcross").style.color = scrollmode==0?"rgb(90,90,90)":(scrollmode==1?"blue":"green");\r\n' \
  '        } else {\r\n' \
  '          if (! focused) {return;}\r\n' \
  '          if (focused.substring(0, 3) == "seg") {\r\n' \
  '            document.getElementById(focused + "desc").scrollIntoView({block:"start"});\r\n' \
  '            scroll_to_track(document.getElementById(focused.replace("segment", "track")), true);\r\n' \
  '          } else if (focused.substring(0, 3) == "tra") {\r\n' \
  '            document.getElementById(focused + "desc").scrollIntoView({block:"nearest"});\r\n' \
  '            scroll_to_track(document.getElementById(focused), true);\r\n' \
  '          } else {\r\n' \
  '            document.getElementById(focused + "desc").scrollIntoView({block:"nearest"});\r\n' \
  '            document.getElementById(focused + "focus").scrollIntoView({block:"nearest"});\r\n' \
  '            if (document.getElementById(focused).value != "error") {\r\n' \
  '              scroll_to_dot(document.getElementById(focused.replace("point", "dot")));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function open_legend() {\r\n' \
  '        let msgn = show_msg("{#jmopenlegend1#}", 0);\r\n' \
  '        xhr_ongoing++;\r\n' \
  '        fetch("/legend", {headers:{"If-Match": sessionid}, method: "GET"}).then((r) => r.formData()).then((fd) => {xhr_ongoing--;fd.forEach((e) => {let url=URL.createObjectURL(e);let w=open(url);URL.revokeObjectURL(url);w.onload=(ev)=>{ev.target.title=e.name;};w.document.title=e.name;});show_msg("{#jmopenlegend2#}".replace("%s", Array.from(fd.keys()).length.toString()), 5, msgn);}).catch((er) => {show_msg("{#jmopenlegend2#}".replace("%s", "0"), 10, msgn);});\r\n' \
  '      }\r\n' \
  '      function switch_sel(e, s) {\r\n' \
  '        if (e.button == 2) {\r\n' \
  '          e.preventDefault();\r\n' \
  '          e.stopPropagation();\r\n' \
  '          if (e.altKey) {\r\n' \
  '            if (s.id == "tset") {\r\n' \
  '              open_legend();\r\n' \
  '            }\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '          if (s.id == "tset" && mode != "map" && layers.length > 1) {\r\n' \
  '            document.getElementById("opanel").style.display = document.getElementById("opanel").style.display=="none"?"block":"none";\r\n' \
  '          }\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        document.getElementById("opanel").style.display = "none";\r\n' \
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
  '      function load_epcb(t) {\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        if (t.status != 204) {\r\n' \
  '          document.getElementById("eset").selectedIndex = eset;\r\n' \
  '          document.getElementById("eset").disabled = false;\r\n' \
  '          document.getElementById("eset").style.pointerEvents = "";\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        eset = document.getElementById("eset").selectedIndex;\r\n' \
  '        document.getElementById("eset").disabled = false;\r\n' \
  '        document.getElementById("eset").style.pointerEvents = "";\r\n' \
  '      }\r\n' \
  '      function error_epcb() {\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        document.getElementById("eset").selectedIndex = eset;\r\n' \
  '        document.getElementById("eset").disabled = false;\r\n' \
  '        document.getElementById("eset").style.pointerEvents = "";\r\n' \
  '      }\r\n' \
  '      function switch_elevations(eset) {\r\n' \
  '        document.getElementById("eset").disabled = true;\r\n' \
  '        document.getElementById("eset").style.pointerEvents = "none";\r\n' \
  '        let q = "eset=" + encodeURIComponent(eset.toString());\r\n' \
  '        xhrep.onload = (e) => {load_epcb(e.target)};\r\n' \
  '        xhrep.open("GET", "/elevationsproviders/switch?" + q);\r\n' \
  '        xhrep.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhr_ongoing++;\r\n' \
  '        xhrep.send();\r\n' \
  '      }\r\n'
  HTML_ATTENUATE_TEMPLATE = \
  '            <svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute;top:0px;left:0px;">\r\n' \
  '              <filter id="attenuate">\r\n' \
  '                <feComponentTransfer color-interpolation-filters="sRGB">\r\n' \
  '                  <feFuncR type="gamma" offset="0" amplitude="1" exponent="1"/>\r\n' \
  '                  <feFuncG type="gamma" offset="0" amplitude="1" exponent="1"/>\r\n' \
  '                  <feFuncB type="gamma" offset="0" amplitude="1" exponent="1"/>\r\n' \
  '                </feComponentTransfer>\r\n' \
  '              </filter>\r\n' \
  '            </svg>\r\n'
  HTML_OPACITYPANEL_TEMPLATE = \
  '            <div id="opanel" style="position:absolute;display:none;top:calc(1.6em + 10px);right:2vw;width:26em;max-height:20em;overflow-y:auto;background-color:rgb(30,30,35);z-index:9;font-size:70%;text-align:left;font-weight:normal;user-select:none;">\r\n' \
  '              <form id="oform" autocomplete="off" onsubmit="return(false);"/>\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n'
  HTML_DFMTPANEL_TEMPLATE = \
  '            <div id="dfpanel">\r\n' \
  '              <span>{#jdfpanel#}</span>\r\n' \
  '              <form id="dfform" autocomplete="off" onsubmit="return(false);" onchange="smoothed?tracks_smooth(true):null;">\r\n' \
  '                <label for="dffilter" style="left:1.5em;width:8em;">{#jgraphdistance#}</label>\r\n' \
  '                <span id="dfdist" style="left:4.5em;">##SMRANGE##</span>\r\n' \
  '                <input type="range" id="dffilter" name="dffilter" min="5" max="50" step="1" value="##SMRANGE##" style="right:5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n' \
  '            <div id="mtpanel">\r\n' \
  '              <span>{#jmtpanel#}</span>\r\n' \
  '              <form id="mtform" autocomplete="off" onsubmit="return(false);" onchange="update_media();">\r\n' \
  '                <label for="mthumb" style="left:1.5em;width:8em;">{#jpixels#}</label>\r\n' \
  '                <span id="mtsize" style="left:4.5em;">##THUMBSIZE##</span>\r\n' \
  '                <input type="range" id="mthumb" name="mthumb" min="16" max="512" step="4" value="##THUMBSIZE##" style="right:5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n'
  HTML_FILTERPANEL_TEMPLATE = \
  '            <div id="filterpanel1">\r\n' \
  '              <span>{#jfilterpanel1#}</span>\r\n' \
  '              <form id="filterform1" autocomplete="off" onsubmit="return(false);" onchange="segments_calc(1)">\r\n' \
  '                <label for="egfilter" style="left:2px;">{#jgraphelevation#}</label>\r\n' \
  '                <label for="agfilter" style="right:2px;">{#jgraphaltitude#}</label>\r\n' \
  '                <span id="egstren" style="left:0.7em;">##EGTHRESHOLD##</span>\r\n' \
  '                <input type="range" id="egfilter" name="egfilter" min="0" max="25" step="1" value="##EGTHRESHOLD##" style="right:8.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '                <span id="agstren" style="right:0.7em;">##AGTHRESHOLD##</span>\r\n' \
  '                <input type="range" id="agfilter" name="agfilter" min="0" max="25" step="1" value="##AGTHRESHOLD##" style="right:1.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n' \
  '            <div id="filterpanel2">\r\n' \
  '              <span>{#jfilterpanel2#}</span>\r\n' \
  '              <form id="filterform2" autocomplete="off" onsubmit="return(false);" onchange="segments_calc(2)">\r\n' \
  '                <label for="sldfilter" style="left:2px;">{#jgraphdistance#}</label>\r\n' \
  '                <label for="slmfilter" style="right:2px;">{#jsmax#}</label>\r\n' \
  '                <span id="sldist" style="left:0.7em;">##SLRANGE##</span>\r\n' \
  '                <input type="range" id="sldfilter" name="sldfilter" min="0" max="500" step="2" value="##SLRANGE##" style="right:8.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '                <span id="slmax" style="right:0.7em;">##SLMAX##</span>\r\n' \
  '                <input type="range" id="slmfilter" name="slmfilter" min="0" max="100" step="1" value="##SLMAX##" style="right:1.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n' \
  '            <div id="filterpanel3">\r\n' \
  '              <span>{#jfilterpanel3#}</span>\r\n' \
  '              <form id="filterform3" autocomplete="off" onsubmit="return(false);" onchange="segments_calc(3)">\r\n' \
  '                <label for="sptfilter" style="left:2px;">{#jspduration#}</label>\r\n' \
  '                <label for="spmfilter" style="right:2px;">{#jsmax#}</label>\r\n' \
  '                <span id="sptime" style="left:0.7em;">##SPRANGE##</span>\r\n' \
  '                <input type="range" id="sptfilter" name="sptfilter" min="0" max="300" step="2" value="##SPRANGE##" style="right:8.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '                <span id="spmax" style="right:0.7em;">##SPMAX##</span>\r\n' \
  '                <input type="range" id="spmfilter" name="spmfilter" min="0" max="90" step="1" value="##SPMAX##" style="right:1.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n'
  HTML_3DPANEL_TEMPLATE = \
  '            <div id="v3Dpanel">\r\n' \
  '              <span>{#j3dpanel#}</span>\r\n' \
  '              <form id="v3dform" autocomplete="off" onsubmit="return(false);">\r\n' \
  '                <label for="v3dpmargin" style="left:2px;">{#j3dpanoramic#}</label>\r\n' \
  '                <label for="v3dsmargin" style="right:2px;">{#j3dsubjective#}</label>\r\n' \
  '                <span id="v3dpdist" style="left:0.7em;">##V3DPMARGIN##</span>\r\n' \
  '                <input type="range" id="v3dpmargin" name="v3dpmargin" min="0.5" max="20" step="0.5" value="##V3DPMARGIN##" style="right:8.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '                <span id="v3dsdist" style="right:0.7em;">##V3DSMARGIN##</span>\r\n' \
  '                <input type="range" id="v3dsmargin" name="v3dsmargin" min="0.5" max="20" step="0.5" value="##V3DSMARGIN##" style="right:1.5em;" oninput="this.previousElementSibling.innerHTML=this.value" onfocus="this.previousElementSibling.style.color=\'rgb(200, 250,240)\'" onblur="this.previousElementSibling.style.color=\'\'">\r\n' \
  '              </form>\r\n' \
  '            </div>\r\n'
  HTML_SSB_GRAPH_TEMPLATE = \
  '              <div id="scalebox" style="left:1.5em;line-height:0.7em;">\r\n' \
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
  '            <div style="height:1.2em;overflow-y:hidden;width:100%;user-select:none;">\r\n' \
  '              <div id="message" style="overflow-y:auto;width:calc(98vw - 6px - 1.4em);height:1.2em;display:inline-block;" ></div><div title="{#jhelp#}" style="overflow-y:auto;width:1.4em;height:1.2em;display:inline-block;text-align:center;background-color:lightgray;color:black;font-weight:bold;cursor:help;">?</div>\r\n' \
  '            </div>\r\n' \
  '          </th>\r\n' \
  '        </tr>\r\n' \
  '      </tfoot>\r\n' \
  '    </table>\r\n' \
  '    <div id="graph" style="height:25vh;display:none;position:relative;width:100%;border-top:1px darkgray solid;font-size:80%;">\r\n' \
  '      <select id="graphy" name="graphy" title="y" autocomplete="off" style="top:0;" onchange="refresh_graph()"><option value="distance">{#jgraphdistance#}</option><option value="elevation">{#jgraphelevation#}</option><option value="altitude">{#jgraphaltitude#}</option><option value="elegain">{#jgraphelegain#}</option><option value="altgain">{#jgraphaltgain#}</option><option value="eleslope">{#jgrapheleslope#}</option><option value="altslope">{#jgraphaltslope#}</option><option value="speed">{#jgraphspeed#}</option></select>\r\n' \
  '      <select id="graphx" name="graphx" title="x" autocomplete="off" style="bottom:0;" onchange="refresh_graph()"><option value="time">{#jgraphtime#}</option><option value="distance">{#jgraphdistance#}</option></select>\r\n' \
  '      <div id="graphp" style="width:6em;color:dodgerblue;position:absolute;left:2px;top:2em;bottom:2em;overflow:auto;text-align:right;">\r\n' \
  '        <span id="graphpx" style="bottom:0;position:absolute;right:0;"></span>\r\n' \
  '        <span id="graphpy" style="top:0;position:absolute;right:0;"></span>\r\n' \
  '      </div>\r\n' \
  '      <canvas id="graphc" width="100" height="25" style="position:absolute;left:8em;top:0;" onmousedown="mouse_down(event)" onpointerdown="pointer_down(event)">\r\n' \
  '      </canvas>\r\n' \
  '      <svg id="gbarc" preserveAspectRatio="none" width="3" height="1" viewbox="0 0 3 100" stroke="none" stroke-width="1" fill="none" style="position:absolute;display:none;left:20px;top:1px;cursor:ew-resize;" onmousedown="mouse_down(event)" onpointerdown="pointer_down(event)">\r\n' \
  '        <line vector-effect="non-scaling-stroke" pointer-events="none" x1="1" y1="0" x2="1" y2="100"/>\r\n' \
  '      </svg>\r\n' \
  '      <svg id="gbar" preserveAspectRatio="none" width="3" height="1" viewbox="0 0 3 100" stroke="dodgerblue" stroke-width="1" fill="none" style="position:absolute;display:none;left:20px;top:1px;" pointer-events="none">\r\n' \
  '        <line vector-effect="non-scaling-stroke" x1="1" y1="0" x2="1" y2="100"/>\r\n' \
  '      </svg>\r\n' \
  '    </div>\r\n'
  HTML_PAGE_LOAD_TEMPLATE = \
  '        document.getElementById("dfpanel").style.right = "calc(2vw + " + (mode=="tiles"?"18.7":"16.1") + "em - 30px)";\r\n' \
  '        document.getElementById("mtpanel").style.right = "calc(2vw + " + (mode=="tiles"?"36.2":"33.6") + "em - 30px)";\r\n' \
  '        document.getElementById("filterpanel1").style.right = "calc(2vw + " + (mode=="tiles"?"17.1":"14.3") + "em - 30px)";\r\n' \
  '        document.getElementById("filterpanel2").style.right = "calc(2vw + " + (mode=="tiles"?"17.1":"14.3") + "em - 30px)";\r\n' \
  '        document.getElementById("filterpanel3").style.right = "calc(2vw + " + (mode=="tiles"?"17.1":"14.3") + "em - 30px)";\r\n' \
  '        document.getElementById("v3Dpanel").style.right = "calc(2vw + " + (mode=="tiles"?"15.3":"12.6") + "em - 30px)";\r\n' \
  '        let prev_state = sessionStorage.getItem("state");\r\n' \
  '        if (prev_state != null) {prev_state = prev_state.split("|");}\r\n' \
  '        if (prev_state != null) {zoom_s = prev_state[3];}\r\n' \
  '        xhr_ongoing++;\r\n' \
  '        if (mode == "map") {\r\n' \
  '          add_tile();\r\n' \
  '          rescale();\r\n' \
  '        } else {\r\n' \
  '          if (prev_state == null) {\r\n' \
  '            document.getElementById("tset").selectedIndex = Array.from(document.getElementById("tset").options).findIndex((o)=>o.style.display!="none");\r\n' \
  '            switch_tiles(-1, 0);\r\n' \
  '          } else {\r\n' \
  '            document.getElementById("tset").selectedIndex = parseInt(prev_state[0]);\r\n' \
  '            opacities = new Map(JSON.parse(prev_state[20]));\r\n' \
  '            switch_tiles(parseInt(prev_state[0]), parseInt(prev_state[1]));\r\n' \
  '            if (prev_state[2] == "true") {switch_tlock(false);}\r\n' \
  '          }\r\n' \
  '          document.getElementById("matrix").style.display = "inline-block";\r\n' \
  '          document.getElementById("tlock").style.display = "";\r\n' \
  '          if (tlevel == 0) {rescale();}\r\n' \
  '        }\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        scroll_to_track();\r\n' \
  '        if (prev_state != null) {\r\n' \
  '          [adjustment_a, adjustment_e] = prev_state[5].split("-").map(Number);\r\n' \
  '          if (adjustment_a < 0.91 || adjustment_e < 0.91) {\r\n' \
  '            Array.from(document.getElementById("attenuate").firstElementChild.children).forEach(function (f) {f.setAttribute("offset", (1.0 - adjustment_a).toFixed(1)); f.setAttribute("amplitude", adjustment_a.toFixed(1)); f.setAttribute("exponent", adjustment_e.toFixed(1));});\r\n' \
  '            document.documentElement.style.setProperty("--filter", "url(#attenuate)");\r\n' \
  '          }\r\n' \
  '          eset = parseInt(prev_state[6]);\r\n' \
  '          if (eset >= 0 && document.getElementById("eset").options.length > eset) {document.getElementById("eset").selectedIndex = eset;}\r\n' \
  '          iset = parseInt(prev_state[7]);\r\n' \
  '          if (document.getElementById("iset").name == "iset") {\r\n' \
  '            if (iset >= 0) {\r\n' \
  '              if (document.getElementById("iset").options.length > iset) {document.getElementById("iset").selectedIndex = iset;}\r\n' \
  '            } else {\r\n' \
  '              iset = document.getElementById("iset").selectedIndex;\r\n' \
  '            }\r\n' \
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
  '          document.getElementById("v3dpdist").innerHTML = prev_state[16];\r\n' \
  '          document.getElementById("v3dpmargin").value = parseFloat(prev_state[16]);\r\n' \
  '          document.getElementById("v3dsdist").innerHTML = prev_state[17];\r\n' \
  '          document.getElementById("v3dsmargin").value = parseFloat(prev_state[17]);\r\n' \
  '          document.getElementById("dfdist").innerHTML = prev_state[18];\r\n' \
  '          document.getElementById("dffilter").value = parseFloat(prev_state[18]);\r\n' \
  '          scrollmode = parseInt(prev_state[19]);\r\n' \
  '        } else {\r\n' \
  '          eset = document.getElementById("eset").selectedIndex;\r\n' \
  '          if (document.getElementById("iset").name == "iset") {iset = document.getElementById("iset").selectedIndex;}\r\n' \
  '        }\r\n' \
  '        document.getElementById("scrollcross").style.color = scrollmode==0?"rgb(90,90,90)":(scrollmode==1?"blue":"green");\r\n'
  HTML_PAGE_UNLOAD_TEMPLATE = \
  '        sessionStorage.setItem("state", (mode == "map" ? "||" : (tset.toString() + "|" + tlevel.toString() + "|" + tlock.toString())) + "|" + zoom_s + "|" + dots_visible.toString() + "|" + adjustment_a.toFixed(1) + "-" + adjustment_e.toFixed(1) + "|" + eset.toString() + "|" + iset.toString() + "|" + document.getElementById("egstren").innerHTML + "|" + document.getElementById("agstren").innerHTML + "|" + document.getElementById("sldist").innerHTML + "|" + document.getElementById("slmax").innerHTML + "|" + document.getElementById("sptime").innerHTML + "|" + document.getElementById("spmax").innerHTML + "|" + document.getElementById("graphx").selectedIndex.toString() + "|" + document.getElementById("graphy").selectedIndex.toString() + "|" + document.getElementById("v3dpdist").innerHTML + "|" + document.getElementById("v3dsdist").innerHTML +  "|" + document.getElementById("dfdist").innerHTML + "|" + scrollmode.toString() + "|" + (mode == "map" ? "{}" : JSON.stringify(Array.from(opacities))));\r\n'
  HTML_TEMPLATE = \
  '<!DOCTYPE html>\r\n' \
  '<html lang="fr-FR">\r\n' \
  '  <head>\r\n' \
  '    <meta charset="utf-8">\r\n' \
  '    <title>GPXTweaker</title>\r\n' + HTML_STYLES_TEMPLATE + \
  '      input[id=name_track] {\r\n' \
  '        width:calc(98vw - 64em);\r\n' \
  '        font-size:70%;\r\n' \
  '      }\r\n' \
  '      form[id*=point] {\r\n' \
  '        overflow-x:hidden;\r\n' \
  '        margin-right: 4px;\r\n' \
  '      }\r\n' \
  '      input[type=checkbox][id*=point] {\r\n' \
  '        margin-left:3px;\r\n' \
  '        margin-right:2px;\r\n' \
  '      }\r\n' \
  '      label[id^=segment], label[id^=point], div[id^=point][id$=cont] {\r\n' \
  '        text-decoration:inherit;\r\n' \
  '      }\r\n' \
  '      label[id$=desc] {\r\n' \
  '        cursor:cell;\r\n' \
  '        display:inline-block;\r\n' \
  '        vertical-align:middle;\r\n' \
  '        white-space:nowrap;\r\n' \
  '        width:calc(24em - 22px);\r\n' \
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
  '      svg[id^=dot] {\r\n' \
  '        stroke:gray;\r\n' \
  '        fill:none;\r\n' \
  '        pointer-events:all;\r\n' \
  '      }\r\n' \
  '      svg[id^=waydot] {\r\n' \
  '        stroke:red;\r\n' \
  '        fill:red;\r\n' \
  '        pointer-events:all;\r\n' \
  '      }\r\n' \
  '      svg[id^=dot] rect, svg[id^=waydot] circle {\r\n' \
  '        pointer-events:none;\r\n' \
  '      }\r\n' \
  '      svg[id^=track] {\r\n' \
  '        stroke:red;\r\n' \
  '        fill:red;\r\n' \
  '      }\r\n' \
  '    </style>\r\n' \
  '    <script>\r\n' + HTML_GLOBALVARS_TEMPLATE + \
  '      var hist = [[], []];\r\n' \
  '      var hist_b = 0;\r\n' \
  '      var foc_old = null;\r\n' \
  '      var stats = [];\r\n' \
  '      var gpu_part = gpucomp >=1?true:false;\r\n' \
  '      var smoothed = false;\r\n' \
  '      var point_stat = [];\r\n' \
  '      var graph_ip = null;\r\n' \
  '      var graph_px = null;\r\n' + HTML_GPUSTATS_TEMPLATE + \
  '      if (gpucomp > 0) {var gpustats = new GPUStats("tweaker");}\r\n' + HTML_MSG_TEMPLATE + \
  '      function switch_tiles(nset, nlevel, kzoom=false) {\r\n' \
  '        if (mode == "map") {\r\n' \
  '          if (nset == null && nlevel == null) {\r\n' \
  '            let b = track_boundaries();\r\n' \
  '            if (b == null) {return;}\r\n' \
  '            let r = Math.max((b[1] - b[0]) / viewpane.offsetWidth, (b[3] - b[2]) / viewpane.offsetHeight);\r\n' \
  '            let z = eval(zooms.slice(-1)[0]);\r\n' \
  '            if (r > 0) {z = 1 / r / Math.min((viewpane.offsetWidth - 2) / (vmaxx - vminx), (viewpane.offsetHeight - 4) / (vmaxy - vminy));}\r\n' \
  '            let zoom_s_ex = zoom_s;\r\n' \
  '            zoom_s = "1";\r\n' \
  '            for (let i=1; i<zooms.length; i++) {\r\n' \
  '              if (eval(zooms[i]) <= z) {zoom_s = zooms[i];} else {break;}\r\n' \
  '            }\r\n' \
  '            if (zoom_s != zoom_s_ex) {rescale();}\r\n' \
  '            scroll_to_track(null, true, b);\r\n' \
  '          }\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        document.getElementById("tset").disabled = true;\r\n' \
  '        document.getElementById("tset").style.pointerEvents = "none";\r\n' \
  '        let q = "";\r\n' \
  '        let sta = false;\r\n' \
  '        if (nset != null) {\r\n' \
  '          document.getElementById("opanel").style.display="none";\r\n' \
  '          if (nset == -1) {\r\n' \
  '            nset = 0;\r\n' \
  '            q = "set=" + encodeURIComponent(document.getElementById("tset").selectedIndex);\r\n' \
  '          } else {\r\n' \
  '            q = "set=" + encodeURIComponent(nset);\r\n' \
  '          }\r\n' \
  '        } else if (nlevel != null) {\r\n' \
  '          q = "matrix=" + encodeURIComponent(tlevels[nlevel][0].toString());\r\n' \
  '          sta = twidth == 0;\r\n' \
  '        } else {\r\n' \
  '          sta = true;\r\n' \
  '          let b = track_boundaries();\r\n' \
  '          if (b == null) {\r\n' \
  '            document.getElementById("tset").disabled = false;\r\n' \
  '            document.getElementById("tset").style.pointerEvents = "";\r\n' \
  '            return;\r\n' \
  '          } else {\r\n' \
  '            q = "auto=" + encodeURIComponent(Math.max((b[1] - b[0]) / viewpane.offsetWidth, (b[3] - b[2]) / viewpane.offsetHeight).toString());\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (xhr_ongoing == 0) {window.stop();}\r\n' \
  '        xhrt.onload = (e) => {load_tcb(e.target, nset, nlevel, kzoom); if(sta) {scroll_to_track();};};\r\n' \
  '        xhrt.open("GET", "/tiles/switch?" + q);\r\n' \
  '        xhrt.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhrt.send();\r\n' \
  '      }\r\n' + HTML_TILES_TEMPLATE + HTML_UTIL_TEMPLATE + \
  '      function scroll_to_dot(dot, center=true) {\r\n' \
  '        let dl = prop_to_wmvalue(dot.style.left);\r\n' \
  '        let dt = prop_to_wmvalue(dot.style.top);\r\n' \
  '        let o = Math.min(50, viewpane.offsetWidth / 2.5, viewpane.offsetHeight / 2.5);\r\n' \
  '        if (center) {\r\n' \
  '          hpx = viewpane.offsetWidth / 2 - dl * zoom / tscale;\r\n' \
  '          hpy = viewpane.offsetHeight / 2 - dt * zoom / tscale;\r\n' \
  '        } else {\r\n' \
  '          hpx = Math.max(Math.min(hpx, -o - dl * zoom / tscale + viewpane.offsetWidth), o - dl * zoom / tscale);\r\n' \
  '          hpy = Math.max(Math.min(hpy, -o - dt * zoom / tscale + viewpane.offsetHeight), o - dt * zoom / tscale);\r\n' \
  '        }\r\n' \
  '        reframe();\r\n' \
  '      }\r\n' \
  '      function drag_dot(x, y) {\r\n' \
  '       let wm = [(x - hpx) * tscale / zoom + htopx, htopy - (y - hpy) * tscale / zoom];\r\n' \
  '       wm[0] = Math.max(Math.min(wm[0], vmaxx - 1), vminx + 1);\r\n' \
  '       wm[1] = Math.max(Math.min(wm[1], vmaxy - 1), vminy + 1);\r\n' \
  '       let [lat, lon] = WebMercatortoWGS84(...wm);\r\n' \
  '       document.getElementById(focused + "lat").value = lat.toFixed(6);\r\n' \
  '       document.getElementById(focused + "lon").value = lon.toFixed(6);\r\n' \
  '       point_edit(false, false, false, true);\r\n' \
  '      }\r\n' \
  '      function track_boundaries(track=null) {\r\n' \
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
  '          let d = tracks[t].firstElementChild.getAttribute("d").match(/[LMm] *\\d+([.]\\d*)? +\\d+([.]\\d*)?/g);\r\n' \
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
  '        if (track == null) {\r\n' \
  '          let wpts = document.getElementById("waypointsform").children;\r\n' \
  '          for (let w=0; w<wpts.length; w++) {\r\n' \
  '            let wpt = wpts[w].firstElementChild;\r\n' \
  '            if (wpt.checked && wpt.value != "error") {\r\n' \
  '              let wdot = document.getElementById(wpt.id.replace("point", "dot"));\r\n' \
  '              if (gminx == null) {\r\n' \
  '                gminx = prop_to_wmvalue(wdot.style.left);\r\n' \
  '                gminy = prop_to_wmvalue(wdot.style.top);\r\n' \
  '                gmaxx = gminx;\r\n' \
  '                gmaxy = gminy;\r\n' \
  '              } else {\r\n' \
  '                gminx = Math.min(gminx, prop_to_wmvalue(wdot.style.left));\r\n' \
  '                gminy = Math.min(gminy, prop_to_wmvalue(wdot.style.top));\r\n' \
  '                gmaxx = Math.max(gmaxx, prop_to_wmvalue(wdot.style.left));\r\n' \
  '                gmaxy = Math.max(gmaxy, prop_to_wmvalue(wdot.style.top));\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (gminx == null) {\r\n' \
  '          return null;\r\n' \
  '        } else {\r\n' \
  '          let o = Math.min(50, viewpane.offsetWidth / 2.5, viewpane.offsetHeight / 2.5);\r\n' \
  '          return [gminx - o, gmaxx + o, gminy - o, gmaxy + o];\r\n' \
  '        }\r\n' \
  '      }\r\n' + HTML_SCROLL_TEMPLATE + \
  '      function dot_style(pt, over) {\r\n' \
  '        if (pt.indexOf("point") < 0) {return;}\r\n' \
  '        let dot = document.getElementById(pt.replace("point", "dot"))\r\n' \
  '        if (document.getElementById(pt).value == "error") {\r\n' \
  '          dot.style.stroke = "";\r\n' \
  '          dot.style.display = "none";\r\n' \
  '          dot.style.zIndex = "";\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let cb = document.getElementById(pt).checked;\r\n' \
  '        let segcb = true;\r\n' \
  '        let iswpt = pt.substring(0, 3) == "way";\r\n' \
  '        if (iswpt) {\r\n' \
  '          if (cb) {dot.style.fill = "";} else {dot.style.fill = "none";}\r\n' \
  '        } else {\r\n' \
  '          segcb = document.getElementById(pt).parentNode.parentNode.firstElementChild.checked;\r\n' \
  '        }\r\n' \
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
  '          dot.style.stroke = iswpt?"gray":"";\r\n' \
  '          dot.style.display = "";\r\n' \
  '          dot.style.zIndex = "";\r\n' \
  '        } else {\r\n' \
  '          dot.style.stroke = "";\r\n' \
  '          dot.style.display = iswpt?"":"none";\r\n' \
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
  '        if (e == null) {\r\n' \
  '          if (document.activeElement) {\r\n' \
  '            if (document.activeElement.id) {\r\n' \
  '              if (document.activeElement.id.indexOf("point") >= 0 || document.activeElement.id == "name_track") {document.activeElement.blur();}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          e.preventDefault();\r\n' \
  '        }\r\n' \
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
  '            if (scrollmode > 0) {scroll_to_track(track, scrollmode == 2);}\r\n' \
  '          } else if (scroll) {\r\n' \
  '            elt.scrollIntoView({block:"nearest"});\r\n' \
  '            elt_foc.scrollIntoView({block:"nearest"});\r\n' \
  '            let par_c = true;\r\n' \
  '            if (focused.substring(0, 3) != "way") {par_c = elt.parentNode.parentNode.firstElementChild.checked;}\r\n' \
  '            if ((! document.getElementById(focused).checked || ! par_c || e) && document.getElementById(focused).value != "error" && scrollmode > 0) {\r\n' \
  '              scroll_to_dot(document.getElementById(focused.replace("point", "dot")), scrollmode == 2);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        graph_point();\r\n' \
  '      }\r\n' \
  '      function point_to_position(pt) {\r\n' \
  '        let lat = parseFloat(document.getElementById(pt.htmlFor + "lat").value);\r\n' \
  '        let lon = parseFloat(document.getElementById(pt.htmlFor + "lon").value);\r\n' \
  '        let wm = WGS84toWebMercator(lat, lon);\r\n' \
  '        let o = "3.5";\r\n' \
  '        if (pt.id.substring(0, 3) == "way") {o = "4";}\r\n' \
  '        return [wmvalue_to_prop(wm[0] - htopx, o), wmvalue_to_prop(htopy - wm[1], o)];\r\n' \
  '      }\r\n' \
  '      function rebase_track(x, y, track, exact=false, batch=false) {\r\n' \
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
  '                if (point[0] != "m") {\r\n' \
  '                  let [px, py] = point.match(/\\d+([.]\\d*)?/g);\r\n' \
  '                  d = d + " " + point[0] + (parseFloat(px) + minx_ex - minx).toFixed(1) + " " + (parseFloat(py) + maxy - maxy_ex).toFixed(1);\r\n' \
  '                } else {\r\n' \
  '                  d = d + " " + point;\r\n' \
  '                }\r\n' \
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
  '        return (x - prop_to_wmvalue(track.style.left) - htopx).toFixed(1) + " " + (htopy - prop_to_wmvalue(track.style.top) - y).toFixed(1);\r\n' \
  '      }\r\n' \
  '      function point_desc(ptspan = null) {\r\n' \
  '        if (! ptspan) {\r\n' \
  '          let points = Array.from(document.getElementById("content").getElementsByTagName("span"));\r\n' \
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
  '        }\r\n' \
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
  '              if (scrollmode > 0) {scroll_to_dot(dot, scrollmode == 2);}\r\n' \
  '            } else {\r\n' \
  '              if (scroll && scrollmode > 0) {scroll_to_dot(dot, scrollmode == 2);}\r\n' \
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
  '      function point_edit_oc(point, recalc=true, coord=true) {\r\n' \
  '        let ex_foc = focused;\r\n' \
  '        if (point != focused) {focused = point;}\r\n' \
  '        point_edit(coord, true, recalc, coord);\r\n' \
  '        focused = ex_foc;\r\n' \
  '      }\r\n' \
  '      function point_over(pt) {\r\n' \
  '        let foc = null;\r\n' \
  '        if (pt.id.indexOf("desc") < 0) {foc = pt.id;} else {foc = pt.htmlFor;}\r\n' \
  '        let par_c = true;\r\n' \
  '        if (foc.substring(0, 3) != "way") {par_c = pt.parentNode.parentNode.firstElementChild.checked;}\r\n' \
  '        dot_style(foc, true);\r\n' \
  '        if (((document.getElementById(foc).checked && par_c) || foc == focused) && document.getElementById(foc).value != "error" && scrollmode == 2) {\r\n' \
  '          scroll_to_dot(document.getElementById(foc.replace("point", "dot")), false);\r\n' \
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
  '        let inds = [];\r\n' \
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
  '        let segments = null;\r\n' \
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
  '            point_edit(false, false, histb == 0, coord && histb == 0);\r\n' \
  '            if (err && elt_foc.value != "error") {\r\n' \
  '              focused = "";\r\n' \
  '              dot_style(hist[s][ind][0], false);\r\n' \
  '              focused = hist[s][ind][0];\r\n' \
  '            }\r\n' \
  '            if (coord && histb != 0) {\r\n' \
  '              if (segments == null) {\r\n' \
  '                segments= Array(document.getElementById("pointsform").children.length).fill(null);\r\n' \
  '                points = Array(document.getElementById("points").getElementsByTagName("span").length).fill(null);\r\n' \
  '              }\r\n' \
  '              segments[parseInt(document.getElementById(focused + "cont").parentNode.id.slice(7, -4))] = true;\r\n' \
  '              points[parseInt(focused.substring(5))] = elt_foc.checked && elt_foc.value != "error";\r\n' \
  '              let dot = document.getElementById(focused.replace("point", "dot"));\r\n' \
  '              [dot.style.left, dot.style.top] = point_to_position(document.getElementById(focused + "desc"));\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            if (histb == 0) {\r\n' \
  '              hist[1-s].push([focused, ""]);\r\n' \
  '            } else {\r\n' \
  '              hist[1-s].push([focused, "", histb]);\r\n' \
  '              if (segments == null) {\r\n' \
  '                segments= Array(document.getElementById("pointsform").children.length).fill(null);\r\n' \
  '                points = Array(document.getElementById("points").getElementsByTagName("span").length).fill(null);\r\n' \
  '              }\r\n' \
  '              segments[parseInt(document.getElementById(focused + "cont").parentNode.id.slice(7, -4))] = true;\r\n' \
  '              points[parseInt(focused.substring(5))] = redo;\r\n' \
  '            }\r\n' \
  '            elt_foc.checked = redo;\r\n' \
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
  '            let tl = prop_to_wmvalue(track.style.left) + htopx;\r\n' \
  '            let tt = htopy - prop_to_wmvalue(track.style.top);\r\n' \
  '            let path = document.getElementById("path" + s.toString());\r\n' \
  '            let pt = document.getElementById("segment" + s.toString() + "cont").firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling;\r\n' \
  '            let d = path.getAttribute("d");\r\n' \
  '            let dots = d.match(/[LMm] *\\d+([.]\\d*)? +\\d+([.]\\d*)?/g);\r\n' \
  '            let d_r = "M0 0";\r\n' \
  '            for (let p=1; p<dots.length; p++) {\r\n' \
  '              let pt_s = points[parseInt(pt.id.slice(5, -4))];\r\n' \
  '              if (pt_s == null) {\r\n' \
  '                d_r = d_r + " " + dots[p];\r\n' \
  '              } else if (pt_s) {\r\n' \
  '                let [x, y] = WGS84toWebMercator(parseFloat(document.getElementById(pt.id.replace("cont", "lat")).value), parseFloat(document.getElementById(pt.id.replace("cont", "lon")).value));\r\n' \
  '                d_r = d_r + " L" + (x - tl).toFixed(1) + " " + (tt - y).toFixed(1);\r\n' \
  '              } else {\r\n' \
  '                d_r = d_r + " m0 0";\r\n' \
  '              }\r\n' \
  '              pt = pt.nextElementSibling;\r\n' \
  '            }\r\n' \
  '            if (d_r.substring(1).indexOf("M") < 0) {d_r = d_r.replace("L", "M");}\r\n' \
  '            path.setAttribute("d", d_r);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (histb != 0) {segments_calc();}\r\n' \
  '        let ex_foc_ = focused;\r\n' \
  '        focused = "";\r\n' \
  '        if (ex_foc) {element_click(null, document.getElementById(ex_foc + "desc"), false);}\r\n' \
  '        if (gr) {refresh_graph(true);}\r\n' \
  '        if (ex_foc.indexOf("point") < 0) {\r\n' \
  '          if (scrollmode > 0) {scroll_to_dot(document.getElementById(ex_foc_.replace("point", "dot")), scrollmode == 2);}\r\n' \
  '          document.getElementById(ex_foc_ + "cont").scrollIntoView({block:"center"});\r\n' \
  '        } else {\r\n' \
  '          if (scrollmode > 0) {scroll_to_dot(document.getElementById(ex_foc.replace("point", "dot")), scrollmode == 2);}\r\n' \
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
  '            pos = "b";\r\n' \
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
  '            pos = "b";\r\n' \
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
  '          if (scrollmode > 0) {scroll_to_dot(el_dot, scrollmode == 2);}\r\n' \
  '          if (seg) {\r\n' \
  '            segments_calc(seg);\r\n' \
  '          } else {\r\n' \
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
  '      function pointed_waypoint(coord) {\r\n' \
  '        let wm = WGS84toWebMercator(...coord);\r\n' \
  '        if (wm[0] <= vminx || wm[0] >= vmaxx || wm[1] <= vminy || wm[1] >= vmaxy) {return;}\r\n' \
  '        if (focused) {\r\n' \
  '          ex_foc = focused;\r\n' \
  '          element_click(null, document.getElementById(focused + "desc"), false);\r\n' \
  '          dot_style(ex_foc, false);\r\n' \
  '        }\r\n' \
  '        let wpts = document.getElementById("waypointsform").children;\r\n' \
  '        let w = 0;\r\n' \
  '        let wpt = null;\r\n' \
  '        while (w < wpts.length) {\r\n' \
  '          wpt = wpts[w].firstElementChild;\r\n' \
  '          if (! wpt.checked && document.getElementById(wpt.id + "name").value == "#### 3D ####") {break;}\r\n' \
  '          w++;\r\n' \
  '        }\r\n' \
  '        if (w < wpts.length) {\r\n' \
  '          element_click(null, document.getElementById(wpt.id + "desc"), false);\r\n' \
  '          document.getElementById(wpt.id + "lat").value = coord[0].toFixed(6);\r\n' \
  '          document.getElementById(wpt.id + "lon").value = coord[1].toFixed(6);\r\n' \
  '          document.getElementById(wpt.id + "ele").value = "";\r\n' \
  '          document.getElementById(wpt.id + "time").value = "";\r\n' \
  '          point_edit(false, true, false, true);\r\n' \
  '        } else {\r\n' \
  '          point_insert("a", coord);\r\n' \
  '          document.getElementById(focused + "name").value = "#### 3D ####";\r\n' \
  '          point_edit(false, false, false, false);\r\n' \
  '          wpt = document.getElementById(focused);\r\n' \
  '          wpt.checked = ! wpt.checked;\r\n' \
  '          point_checkbox(wpt);\r\n' \
  '        }\r\n' \
  '        save_old();\r\n' \
  '        scroll_to_dot(document.getElementById(focused.replace("point", "dot")), true);\r\n' \
  '        window.alert("3D");\r\n' \
  '      }\r\n' \
  '      function segment_calc(seg, fpan=0, ind=null, mmls=null, teahs=null) {\r\n' \
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
  '        if (fpan <= 1 || (fpan == 2 && gpucomp == 0) || gpu_part) {\r\n' \
  '          let spans = seg.getElementsByTagName("span");\r\n' + HTML_SEGCALC_1_TEMPLATE + \
  '          for (let p=0; p<spans.length; p++) {\r\n' \
  '            if (point_stat[parseInt(spans[p].id.slice(5, -5))] == null) {continue;}\r\n' \
  '            let p_c = spans[p].children;\r\n' \
  '            let ea = [parseFloat(p_c[7].value), parseFloat(p_c[10].value)];\r\n' \
  '            for (let v=0; v<2; v++) {\r\n' \
  '              if (! isNaN(ea[v]) && isNaN(ea_p[v])) {\r\n' \
  '                ea_p[v] = ea[v];\r\n' \
  '                ea_r[v] = ea_b[v] = ea[v];\r\n' \
  '                ea_s[v] = ea_p[v];\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            if (fpan == 0 || fpan == 2 || (gpucomp >= 1 && fpan != 1)) {\r\n' \
  '              let t = Date.parse(p_c[13].value);\r\n' \
  '              lat = parseFloat(p_c[1].value);\r\n' \
  '              lon = parseFloat(p_c[4].value);\r\n'  + HTML_SEGCALC_2_TEMPLATE + \
  '            if (gpucomp == 0 && (fpan == 0 || fpan == 2)) {\r\n' \
  '              stat[4] = isNaN(ea[0])?ea_p[0]:ea[0];\r\n' \
  '              stat[5] = isNaN(ea[1])?ea_p[1]:ea[1];\r\n' \
  '              stat[6] = isNaN(el_p)?el_p:el;\r\n' \
  '            }\r\n' \
  '            if (p_p == null) {\r\n' \
  '              if (gpucomp >= 1 && fpan != 1) {\r\n' \
  '                mmls.set([0, 0, lat], 3 * ind);\r\n' \
  '                teahs.set([stat[0], isNaN(ea[0])?ea_p[0]:ea[0], isNaN(ea[1])?ea_p[1]:ea[1], el_p], 4 * ind);\r\n' \
  '                ind++;\r\n' \
  '              }\r\n' \
  '            } else {\r\n' \
  '              if (gpucomp <= 1 && fpan <= 1) {\r\n' \
  '                stat[2] = stat_p[2] + ((isNaN(ea_p[0])||isNaN(ea[0]))?0:Math.max(0,ea[0]-ea_b[0]));\r\n' \
  '                stat[3] = stat_p[3] + ((isNaN(ea_p[1])||isNaN(ea[1]))?0:Math.max(0,ea[1]-ea_b[1]));\r\n' \
  '              }\r\n' \
  '              if (gpucomp == 0) {\r\n' \
  '                if (fpan == 0) {\r\n' \
  '                  stat[1] = stat_p[1] + distance(lat_p, lon_p, null, lat, lon, null);\r\n' \
  '                }\r\n' \
  '              } else if (fpan != 1) {\r\n' \
  '                mmls.set([lat - lat_p,  lon - lon_p , lat], 3 * ind);\r\n' \
  '                teahs.set([stat[0], isNaN(ea[0])?ea_p[0]:ea[0], isNaN(ea[1])?ea_p[1]:ea[1], isNaN(el_p)?el_p:el], 4 * ind);\r\n' \
  '                ind++;\r\n' \
  '              }\r\n' \
  '            }\r\n' + HTML_SEGCALC_3_TEMPLATE + \
  '          } else if (gpucomp != 0 && (fpan == 0 || gpu_part) && fpan != 1) {\r\n' \
  '            for (let i=ind-stat_i; i<ind; i++) {\r\n' \
  '              if (isNaN(teahs[4 * i + 1])) {teahs[4 * i + 1] = ea_s[0];} else {break;}\r\n' \
  '            }\r\n' \
  '            for (let i=ind-stat_i; i<ind; i++) {\r\n' \
  '              if (isNaN(teahs[4 * i + 2])) {teahs[4 * i + 2] = ea_s[1];} else {break;}\r\n' \
  '            }\r\n' \
  '            for (let i=ind-stat_i; i<ind; i++) {\r\n' \
  '              if (isNaN(teahs[4 * i + 3])) {teahs[4 * i + 3] = el_s;} else {break;}\r\n' \
  '            }\r\n' \
  '          }\r\n' + HTML_SEGCALC_4_TEMPLATE + \
  '          if (fpan == 0) {\r\n' \
  '            let dur_c = "--h--mn--s";\r\n' \
  '            if (t_s != null) {\r\n' \
  '              let dur_s = stat_p[0] % 60;\r\n' \
  '              let dur_m = ((stat_p[0] - dur_s) / 60) % 60;\r\n' \
  '              let dur_h = (stat_p[0] - dur_m * 60 - dur_s) / 3600;\r\n' \
  '              dur_c = dur_h.toFixed(0) + "h" + dur_m.toFixed(0).padStart(2, "0") + "mn" + dur_s.toFixed(0).padStart(2, "0") + "s";\r\n' \
  '            }\r\n' \
  '            let dist_c = "-km";\r\n' \
  '            if (gpucomp == 0) {dist_c = (stat_p[6] / 1000).toFixed(2) + "km";}\r\n' \
  '            let ele_c = "-m";\r\n' \
  '            if (! isNaN(ea_p[0])) {ele_c = (gpucomp<=1?stat_p[2].toFixed(0):"[eg]") + "m";}\r\n' \
  '            let alt_c = "-m";\r\n' \
  '            if (! isNaN(ea_p[1])) {alt_c = (gpucomp<=1?stat_p[3].toFixed(0):"[ag]") + "m";}\r\n' \
  '            seg_desc.innerHTML = "&ndash;" + seg_desc.innerHTML.slice(6, -6) + "(" + dur_c + "|" + dist_c + "|" + ele_c + "|" + alt_c + ") &ndash;";\r\n' \
  '          } else if (fpan == 1) {\r\n' \
  '            seg_desc.innerHTML = seg_desc.innerHTML.replace(/\\d+m\\|/, stat_p[2].toFixed(0) + "m|").replace(/\\d+m\\)/, stat_p[3].toFixed(0) + "m)");\r\n' \
  '          } else if (fpan == 2 && gpucomp == 0) {\r\n' \
  '            seg_desc.innerHTML = seg_desc.innerHTML.replace(/\\|.*?km\\|/, "|" + (stat_p[6] / 1000).toFixed(2) + "km|");\r\n' \
  '          }\r\n' \
  '        }\r\n' + HTML_SEGCALC_5_TEMPLATE + \
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
  '          dist = dist==null?stat[6]:dist+stat[6];\r\n' \
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
  '        let mmls = null;\r\n' \
  '        let teahs = null;\r\n' \
  '        if (fpan <= 1 || gpucomp == 0 || gpu_part) {\r\n' \
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
  '            mmls = new Float32Array(GPUStats.pad(starts[starts.length - 1]) * 3);\r\n' \
  '            teahs = new Float32Array(GPUStats.pad(starts[starts.length - 1]) * 4);\r\n' \
  '          }\r\n' \
  '          let ind = 0;\r\n' \
  '          for (let s=0; s<segs.length; s++) {\r\n' \
  '            segment_calc(segs[s], fpan, ind, mmls, teahs);\r\n' \
  '            ind += stats[parseInt(segs[s].id.slice(7, -4))].length;\r\n' \
  '          }\r\n' \
  '          if (starts[starts.length - 1] == 0) {\r\n' \
  '            gpu_part = gpucomp >= 1;\r\n' \
  '            whole_calc();\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '          if (gpucomp >= 1 && (fpan == 0 || gpu_part) && fpan != 1) {\r\n' \
  '            gpustats.starts = starts;\r\n' \
  '            gpustats.mmls = mmls;\r\n' \
  '            gpustats.teahs = teahs;\r\n' \
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
  '          gpustats.drange = Math.max(0.01, parseFloat(document.getElementById("sldist").innerHTML)) / 2;\r\n' \
  '          gpustats.slmax = parseFloat(document.getElementById("slmax").innerHTML) / 100;\r\n' \
  '          gpustats.calc("tweaker");\r\n' \
  '          let gs = gpustats.gs;\r\n' \
  '          let ssss = gpustats.ssss;\r\n' \
  '          let ss = gpustats.ss;\r\n' \
  '          let i = 0;\r\n' \
  '          for (let s=0; s<segs.length; s++) {\r\n' \
  '            let seg_ind = parseInt(segs[s].id.slice(7, -4));\r\n' \
  '            for (let p=0; p<stats[seg_ind].length; p++) {\r\n' \
  '              let stat = stats[seg_ind][p];\r\n' \
  '              if (fpan == 0) {stat[1] = stats[seg_ind][p>0?p-1:0][1] + gs[i];}\r\n' \
  '              stat[7] = ss[i];\r\n' \
  '              stat[4] = ssss[3 * i];\r\n' \
  '              stat[5] = ssss[3 * i + 1];\r\n' \
  '              stat[6] = p==0?0:(stats[seg_ind][p-1][6] + ssss[3 * i - 1]);\r\n' \
  '              if (gpucomp == 2 && fpan <= 2) {\r\n' \
  '                if (p == 0) {\r\n' \
  '                  stat[2] = 0;\r\n' \
  '                  stat[3] = 0;\r\n' \
  '                } else {\r\n' \
  '                  stat[2] = stats[seg_ind][p - 1][2] + Math.max(0, ssss[3 * i - 3]) * gs[i];\r\n' \
  '                  stat[3] = stats[seg_ind][p - 1][3] + Math.max(0, ssss[3 * i - 2]) * gs[i];\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              i++;\r\n' \
  '            }\r\n' \
  '            if (stats[seg_ind].length > 0) {\r\n' \
  '              let seg_desc = segs[s].firstElementChild.nextElementSibling;\r\n' \
  '              let stat = stats[seg_ind][stats[seg_ind].length - 1];\r\n' \
  '              if (gpucomp == 2 && fpan == 2) {\r\n' \
  '                seg_desc.innerHTML = seg_desc.innerHTML.replace(/\\d+m\\|/, "[eg]m|").replace(/\\d+m\\)/, "[ag]m)");\r\n' \
  '              }\r\n' \
  '              seg_desc.innerHTML = seg_desc.innerHTML.replace(/\\|.*?km\\|/, "|" + (stat[6] / 1000).toFixed(2) + "km|").replace("[eg]", stat[2].toFixed(0)).replace("[ag]", stat[3].toFixed(0));\r\n' \
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
  '          let spans = Array.from(seg.getElementsByTagName("span"));\r\n' \
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
  '        if (scrollmode > 0) {scroll_to_dot(document.getElementById(pt_foc.id.slice(0, -4).replace("point", "dot")), scrollmode == 2);}\r\n' \
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
  '        if (scrollmode > 0) {scroll_to_track(document.getElementById("track" + seg_foc.id.slice(7, -4)), scrollmode == 2);}\r\n' \
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
  '        let spans_foc = Array.from(seg_foc.getElementsByTagName("span"));\r\n' \
  '        let spans = Array.from(seg.getElementsByTagName("span"));\r\n' \
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
  '          if (scrollmode > 0) {scroll_to_track();}\r\n' \
  '          segs = pts.children;\r\n' \
  '        } else if (focused.substring(0, 3) == "seg") {\r\n' \
  '          let seg_foc = document.getElementById(focused + "cont");\r\n' \
  '          seg_foc.scrollIntoView({block:"start"});\r\n' \
  '          segs = [seg_foc];\r\n' \
  '          if (scrollmode >0) {scroll_to_track(document.getElementById("track" + seg_foc.id.slice(7, -4)), scrollmode == 2);}\r\n' \
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
  '      function segment_filter() {\r\n' \
  '        let drange = parseFloat(document.getElementById("dfdist").innerHTML);\r\n' \
  '        let seg_foc = null;\r\n' \
  '        let segs = [];\r\n' \
  '        if (focused == "") {\r\n' \
  '          if (! window.confirm("{#jfconfirm#}")) {return;}\r\n' \
  '          let segms = document.getElementById("pointsform").children;\r\n' \
  '          for (let s=0; s<segms.length; s++) {\r\n' \
  '            if (document.getElementById(segms[s].id.slice(0, -4)).checked) {segs.push(segms[s]);}\r\n' \
  '          }\r\n' \
  '          if (segs.length == 0) {return;}\r\n' \
  '          if (scrollmode > 0) {scroll_to_track();}\r\n' \
  '        } else if (focused.substring(0, 3) == "seg") {\r\n' \
  '          seg_foc = document.getElementById(focused + "cont");\r\n' \
  '          if (! seg_foc.firstElementChild.checked) {return;}\r\n' \
  '          seg_foc.scrollIntoView({block:"start"});\r\n' \
  '          segs.push(seg_foc);\r\n' \
  '          if (scrollmode > 0) {scroll_to_track(document.getElementById("track" + seg_foc.id.slice(7, -4)), scrollmode == 2);}\r\n' \
  '        } else {return;}\r\n' \
  '        let batch = ++hist_b;\r\n' \
  '        let nmod = 0;\r\n' \
  '        for (let s=0; s<segs.length; s++) {\r\n' \
  '          let spans = Array.from(segs[s].getElementsByTagName("span"));\r\n' \
  '          let positions = [];\r\n' \
  '          for (let p=0; p<spans.length; p++) {\r\n' \
  '            let pt = document.getElementById(spans[p].id.slice(0, -5));\r\n' \
  '            if (! pt.checked || pt.value == "error") {\r\n' \
  '              positions.push(null);\r\n' \
  '            } else {\r\n' \
  '              let c = spans[p].children;\r\n' \
  '              positions.push(WGS84toWebMercator(parseFloat(c[1].value), parseFloat(c[4].value)));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          let track = document.getElementById("track" + segs[s].id.slice(7, -4));\r\n' \
  '          let tl = prop_to_wmvalue(track.style.left) + htopx;\r\n' \
  '          let tt = htopy - prop_to_wmvalue(track.style.top);\r\n' \
  '          let sdrange = drange * (Math.exp(tt / 6378137) + Math.exp(- tt / 6378137)) / 2;\r\n' \
  '          let path = document.getElementById("path" + segs[s].id.slice(7, -4));\r\n' \
  '          let d = path.getAttribute("d");\r\n' \
  '          let dots = d.match(/[LMm] *\\d+([.]\\d*)? +\\d+([.]\\d*)?/g).slice(1);\r\n' \
  '          let d_f = "M0 0";\r\n' \
  '          let dir = null;\r\n' \
  '          let pp = null;\r\n' \
  '          for (let p=0; p<positions.length; p++) {\r\n' \
  '            let foc = spans[p].id.slice(0, -5);\r\n' \
  '            for (let i=hist[1].length - 1; i>=0 ;i--) {\r\n' \
  '              if (hist[1][i][0] == foc) {hist[1].splice(i, 1);}\r\n' \
  '            }\r\n' \
  '            if (positions[p] == null) {\r\n' \
  '              d_f = d_f + " " + dots[p];\r\n' \
  '              continue;\r\n' \
  '            }\r\n' \
  '            if (pp == null) {\r\n' \
  '              pp = p;\r\n' \
  '              d_f = d_f + " " + dots[p];\r\n' \
  '              continue;\r\n' \
  '            }\r\n' \
  '            let ndir = [0, 0];\r\n' \
  '            let dist = 0;\r\n' \
  '            let pr = pp;\r\n' \
  '            for (let pn=p; pn<positions.length; pn++) {\r\n' \
  '              if (positions[pn] == null) {continue;}\r\n' \
  '              dist += Math.sqrt((positions[pn][0] - positions[pr][0]) ** 2 + (positions[pn][1] - positions[pr][1]) ** 2);\r\n' \
  '              pr = pn;\r\n' \
  '              if (dist > sdrange) {break;}\r\n' \
  '              ndir[0] += positions[pn][0] - positions[pp][0];\r\n' \
  '              ndir[1] += positions[pn][1] - positions[pp][1];\r\n' \
  '            }\r\n' \
  '            let ndirl = Math.sqrt(ndir[0] ** 2 + ndir[1] ** 2);\r\n' \
  '            if (ndirl > 0) {\r\n' \
  '              ndir[0] /= ndirl;\r\n' \
  '              ndir[1] /= ndirl;\r\n' \
  '              if (dir == null) {dir = ndir;}\r\n' \
  '              let pdir = [positions[p][0] - positions[pp][0], positions[p][1] - positions[pp][1]];\r\n' \
  '              let pdirl = Math.sqrt(pdir[0]**2 + pdir[1]**2);\r\n' \
  '              if (pdirl > 0) {\r\n' \
  '                let pmod = false;\r\n' \
  '                pdir[0] /= pdirl;\r\n' \
  '                pdir[1] /= pdirl;\r\n' \
  '                let nsin = dir[0] * ndir[1] - dir[1] * ndir[0];\r\n' \
  '                let ncos = dir[0] * ndir[0] + dir[1] * ndir[1];\r\n' \
  '                let psin = dir[0] * pdir[1] - dir[1] * pdir[0];\r\n' \
  '                let pcos = dir[0] * pdir[0] + dir[1] * pdir[1];\r\n' \
  '                if (nsin * psin < 0) {\r\n' \
  '                  if (pcos < 0) {\r\n' \
  '                    if (ncos < 0) {\r\n' \
  '                      pdirl = Math.min(-pdirl * pcos, -ndirl * ncos);\r\n' \
  '                      dir[0] = -dir[0];\r\n' \
  '                      dir[1] = -dir[1];\r\n' \
  '                    } else {\r\n' \
  '                      pdirl = 0;\r\n' \
  '                    }\r\n' \
  '                  }\r\n' \
  '                  positions[p][0] = positions[pp][0] + pdirl * dir[0];\r\n' \
  '                  positions[p][1] = positions[pp][1] + pdirl * dir[1];\r\n' \
  '                  pmod = true;\r\n' \
  '                } else if (ncos > pcos) {\r\n' \
  '                  pdirl = Math.max(0, pdirl * (pdir[0] * ndir[0] + pdir[1] * ndir[1]));\r\n' \
  '                  positions[p][0] = positions[pp][0] + pdirl * ndir[0];\r\n' \
  '                  positions[p][1] = positions[pp][1] + pdirl * ndir[1];\r\n' \
  '                  pmod = true;\r\n' \
  '                  dir = ndir;\r\n' \
  '                } else {\r\n' \
  '                  dir = pdir;\r\n' \
  '                }\r\n' \
  '                if (pmod) {\r\n' \
  '                  focused = foc;\r\n' \
  '                  save_old();\r\n' \
  '                  [spans[p].children[1].value, spans[p].children[4].value] = WebMercatortoWGS84(...positions[p]).map((l) => l.toFixed(6));\r\n' \
  '                  hist[0].push([focused, foc_old, batch]);\r\n' \
  '                  save_old();\r\n' \
  '                  point_edit(false, false, false, false);\r\n' \
  '                  let dot = document.getElementById(focused.replace("point", "dot"));\r\n' \
  '                  dot.style.left = wmvalue_to_prop(positions[p][0] - htopx, 3.5);\r\n' \
  '                  dot.style.top = wmvalue_to_prop(htopy - positions[p][1], 3.5);\r\n' \
  '                  d_f = d_f + " L" + (positions[p][0] - tl).toFixed(1) + " " + (tt - positions[p][1]).toFixed(1);\r\n' \
  '                  nmod++;\r\n' \
  '                } else {\r\n' \
  '                  d_f = d_f + " " + dots[p];\r\n' \
  '                }\r\n' \
  '              } else {\r\n' \
  '                d_f = d_f + " " + dots[p];\r\n' \
  '              }\r\n' \
  '            } else {\r\n' \
  '              d_f = d_f + " " + dots[p];\r\n' \
  '            }\r\n' \
  '            pp = p;\r\n' \
  '          }\r\n' \
  '          if (d_f.substring(1).indexOf("M") < 0) {d_f = d_f.replace("L", "M");}\r\n' \
  '          path.setAttribute("d", d_f);\r\n' \
  '        }\r\n' \
  '        if (seg_foc != null) {focused = seg_foc.id.slice(0, -4);} else {focused = "";}\r\n' \
  '        segments_calc(...segs);\r\n' \
  '        show_msg((seg_foc!=null?"{#jmsegmentfilter1#}":"{#jmsegmentfilter2#}").replace("%s", nmod.toString()), 2);\r\n' \
  '      }\r\n' \
  '      function error_ecb() {\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        document.getElementById("eset").disabled = false;\r\n' \
  '        document.getElementById("eset").style.pointerEvents = "";\r\n' \
  '      }\r\n' \
  '      function load_ecb(t, pts) {\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        document.getElementById("eset").disabled = false;\r\n' \
  '        document.getElementById("eset").style.pointerEvents = "";\r\n' \
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
  '                    }\r\n' \
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
  '        if (! fromalt && (eset < 0 || document.getElementById("eset").disabled)) {show_msg("{#jmelevationsno#}", 10); return;}\r\n' \
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
  '          }\r\n' \
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
  '            show_msg("{#jmelevations6#}", 10, msgn);\r\n' \
  '          }\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        document.getElementById("eset").disabled = true;\r\n' \
  '        document.getElementById("eset").style.pointerEvents = "none";\r\n' \
  '        let xhre = new XMLHttpRequest();\r\n' \
  '        xhre.onload = (e) => {let np = load_ecb(e.target, pts); np?show_msg(msg.replace("%s", np.toString()).replace("%s", pts.length.toString()), 4, msgn):show_msg("{#jmelevations6#}", 10, msgn);};\r\n' \
  '        xhre.onerror = (e) => {error_ecb(); show_msg("{#jmelevations6#}", 10, msgn);};\r\n' \
  '        xhre.open("POST", "/ele");\r\n' \
  '        xhre.setRequestHeader("Content-Type", "application/octet-stream");\r\n' \
  '        xhre.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhr_ongoing++;\r\n' \
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
  '            spans = Array.from(document.getElementById(ex_foc + "cont").getElementsByTagName("span"));\r\n' \
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
  '          spans = Array.from(document.getElementById("points").getElementsByTagName("span"));\r\n' \
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
  '        let spans = Array.from(seg_foc.getElementsByTagName("span"));\r\n' \
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
  '      function datetime_interpolate(remove=false) {\r\n' \
  '        let segs = [];\r\n' \
  '        let seg_foc = null;\r\n' \
  '        let pt_foc = null;\r\n' \
  '        if (focused == "") {\r\n' \
  '          let segms = document.getElementById("pointsform").children;\r\n' \
  '          for (let s=0; s<segms.length; s++) {\r\n' \
  '            if (document.getElementById(segms[s].id.slice(0, -4)).checked) {segs.push(segms[s]);}\r\n' \
  '          }\r\n' \
  '          if (segs.length == 0) {return;}\r\n' \
  '          if (scrollmode > 0) {scroll_to_track();}\r\n' \
  '        } else if (focused.substring(0, 3) == "seg") {\r\n' \
  '          if (! document.getElementById(focused).checked) {return;}\r\n' \
  '          seg_foc = document.getElementById(focused + "cont");\r\n' \
  '          seg_foc.scrollIntoView({block:"start"});\r\n' \
  '          segs = [seg_foc];\r\n' \
  '          if (scrollmode > 0) {scroll_to_track(document.getElementById("track" + seg_foc.id.slice(7, -4)), scrollmode == 2);}\r\n' \
  '        } else if (focused.substring(0, 5) == "point") {\r\n' \
  '          if (! document.getElementById(focused).checked || document.getElementById(focused).value == "error") {return;}\r\n' \
  '          pt_foc = focused;\r\n' \
  '          document.getElementById(pt_foc + "cont").scrollIntoView({block:"nearest"});\r\n' \
  '          seg_foc = document.getElementById(pt_foc + "cont").parentNode;\r\n' \
  '          segs = [seg_foc];\r\n' \
  '          if (scrollmode > 0) {scroll_to_dot(document.getElementById(pt_foc.replace("point", "dot")), scrollmode == 2);}\r\n' \
  '        } else {\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let batch = ++hist_b;\r\n' \
  '        if (remove) {\r\n' \
  '          let msg = null;\r\n' \
  '          for (let s=0; s<segs.length; s++) {\r\n' \
  '            let spans = pt_foc==null?Array.from(segs[s].getElementsByTagName("span")):[document.getElementById(pt_foc + "focus")];\r\n' \
  '            for (let p=0; p<spans.length; p++) {\r\n' \
  '              pt = spans[p].id.slice(0, -5);\r\n' \
  '              if ((pt_foc == null && document.getElementById(pt).checked && document.getElementById(pt).value != "error") || pt_foc == pt) {\r\n' \
  '                if (document.getElementById(pt + "time").value != "") {\r\n' \
  '                  msg = "";\r\n' \
  '                  focused = pt;\r\n' \
  '                  save_old();\r\n' \
  '                  hist[0].push([focused, foc_old, batch]);\r\n' \
  '                  document.getElementById(pt + "time").value = "";\r\n' \
  '                  for (let j=hist[1].length - 1; j>=0 ;j--) {\r\n' \
  '                    if (hist[1][j][0] == focused) {hist[1].splice(j, 1);}\r\n' \
  '                  }\r\n' \
  '                  point_edit(false, false, false, false);\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (msg != null) {\r\n' \
  '            msg = pt_foc!=null?"{#jmdatetime4#}":(seg_foc!=null?"{#jmdatetime5#}":"{#jmdatetime6#}");\r\n' \
  '            if (pt_foc == null && seg_foc != null && focused.substring(0, 3) != "seg") {focused = seg_foc.id.slice(0, -4);}\r\n' \
  '            if (pt_foc == null && seg_foc == null && focused != "") {focused = "";}\r\n' \
  '            segments_calc(...segs);\r\n' \
  '            show_msg(msg, 2);\r\n' \
  '          }\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        for (let s=0; s<segs.length; s++) {\r\n' \
  '          let spans = Array.from(segs[s].getElementsByTagName("span"));\r\n' \
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
  '                  document.getElementById(spans[pm[i][0]].id.replace("focus", "time")).value = (new Date(Math.round((stime + inv_vit * pm[i][1]) / 1000) * 1000)).toISOString().replace(/\\.[0-9]*/,"");\r\n' \
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
  '                    document.getElementById(spans[pm_b[i][0]].id.replace("focus", "time")).value = (new Date(Math.round((dist_b==0?btime:(btime + inv_vit * (pm_b[i][1] - dist_b))) / 1000) * 1000)).toISOString().replace(/\\.[0-9]*/,"");\r\n' \
  '                    for (let j=hist[1].length - 1; j>=0 ;j--) {\r\n' \
  '                      if (hist[1][j][0] == focused) {hist[1].splice(j, 1);}\r\n' \
  '                    }\r\n' \
  '                    point_edit(false, false, false, false);\r\n' \
  '                  }\r\n' \
  '                  if (pt_foc != null && pm_b.length > 0) {\r\n' \
  '                    save_old();\r\n' \
  '                    segments_calc(segs[s]);\r\n' \
  '                    show_msg("{#jmdatetime1#}", 2);\r\n' \
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
  '        let msg = focused.indexOf("point")<0?null:(seg_foc!=null?"{#jmdatetime2#}":"{#jmdatetime3#}");\r\n' \
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
  '      }\r\n' + HTML_GRAPH1_TEMPLATE + \
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
  '            let ea = null;\r\n' \
  '            if (gy_ind == 1 || gy_ind == 2) {ea = parseFloat(document.getElementById(spans[p].id.replace("focus", gy_ind==1?"ele":"alt")).value);}\r\n' + HTML_GRAPH2_TEMPLATE + \
  '              graph_ip.push(parseInt(spans[p].id.slice(5, -5)));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          dur += stat[0];\r\n' \
  '          dist += stat[6];\r\n' \
  '          ele += stat[2];\r\n' \
  '          alt += stat[3];\r\n' \
  '        }\r\n' \
  '        if (gx.length < 2) {\r\n' \
  '          graph_point();\r\n' \
  '          return;\r\n' \
  '        }\r\n' + HTML_GRAPH3_TEMPLATE + \
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
  '      function graph_point(bx) {\r\n' \
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
  '        if (bx == null) {\r\n' \
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
  '              let dist_s = stats[segf_ind][point_stat[foc_ind]][6];\r\n' \
  '              let dist = dist_s;\r\n' \
  '              for (let s=0; s<segs.length; s++) {\r\n' \
  '                if (! segs[s].firstElementChild.checked) {continue;}\r\n' \
  '                let seg_ind = parseInt(segs[s].id.slice(7, -4));\r\n' \
  '                if (seg_ind == segf_ind) {break;}\r\n' \
  '                if (stats[seg_ind].length == 0) {continue;}\r\n' \
  '                dist += stats[seg_ind][stats[seg_ind].length - 1][6];\r\n' \
  '              }\r\n' \
  '              graphpx.innerHTML = (dist / 1000).toFixed(2) + "km<br>" + (dist_s / 1000).toFixed(2) + "km";\r\n' \
  '            }\r\n' \
  '            let yi = document.getElementById("graphy").selectedIndex;\r\n' \
  '            switch (yi) {\r\n' \
  '              case 0:\r\n' \
  '                let dist_s = stats[segf_ind][point_stat[foc_ind]][6];\r\n' \
  '                let dist = dist_s;\r\n' \
  '                for (let s=0; s<segs.length; s++) {\r\n' \
  '                  if (! segs[s].firstElementChild.checked) {continue;}\r\n' \
  '                  let seg_ind = parseInt(segs[s].id.slice(7, -4));\r\n' \
  '                  if (seg_ind == segf_ind) {break;}\r\n' \
  '                  if (stats[seg_ind].length == 0) {continue;}\r\n' \
  '                  dist += stats[seg_ind][stats[seg_ind].length - 1][6];\r\n' \
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
  '                graphpy.innerHTML = (stats[segf_ind][point_stat[foc_ind]][7] * 3.6 ).toFixed(1) + "km/h";\r\n' \
  '                break\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          let x = Math.max(Math.min(bx + 1, xr), xl);\r\n' \
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
  '          } else {\r\n' \
  '            gbar.style.display = "";\r\n' \
  '            graphpx.innerHTML = gpx;\r\n' \
  '            graphpy.innerHTML = gpy;\r\n' \
  '          }\r\n' \
  '          if (scrollmode_ex > 0) {scroll_to_dot(document.getElementById("dot" + graph_ip[ind1].toString()), scrollmode_ex == 2);}\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function error_pcb() {\r\n' \
  '        xhr_ongoing--;\r\n' \
  '      }\r\n' \
  '      function load_pcb(t, foc) {\r\n' \
  '        xhr_ongoing--;\r\n' \
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
  '                    if (point[0] != "m") {\r\n' \
  '                      let [px, py] = point.match(/\\d+([.]\\d*)?/g);\r\n' \
  '                      d_ = d_ + " " + point[0] + (parseFloat(px) + c[0]).toFixed(1) + " " + (parseFloat(py) + c[1]).toFixed(1);\r\n' \
  '                    } else {\r\n' \
  '                      d_ = d_ + " " + point;\r\n' \
  '                    }\r\n' \
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
  '      }\r\n' \
  '      function build_path() {\r\n' \
  '        if (iset < 0) {show_msg("{#jmpathno#}", 10); return;}\r\n' \
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
  '        xhr_ongoing++;\r\n' \
  '        xhrp.send(b);\r\n' \
  '      }\r\n' \
  '      function open_3D(mode3d="p") {\r\n' \
  '        if (eset < 0) {show_msg("{#jmelevationsno#}", 10); return;}\r\n' \
  '        if (mode != "map") {\r\n' \
  '          if (tlayers.has(tset) || jmaps.length > 0) {show_msg("{#jm3dviewer4#}", 10); return;}\r\n' \
  '        }\r\n' \
  '        track_save(mode3d);\r\n' \
  '      }\r\n' + HTML_MAP_TEMPLATE.replace('if (! focused) {return;}', 'if (! focused) {scroll_to_track();return;}') + \
  '      function load_ipcb(t) {\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        if (t.status != 204) {\r\n' \
  '          document.getElementById("iset").selectedIndex = iset;\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        iset = document.getElementById("iset").selectedIndex;\r\n' \
  '      }\r\n' \
  '      function error_ipcb() {\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        document.getElementById("iset").selectedIndex = iset;\r\n' \
  '      }\r\n' \
  '      function switch_itineraries(iset) {\r\n' \
  '        let q = "iset=" + encodeURIComponent(iset.toString());\r\n' \
  '        xhrip.onload = (e) => {load_ipcb(e.target)};\r\n' \
  '        xhrip.open("GET", "/itinerariesproviders/switch?" + q);\r\n' \
  '        xhrip.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhr_ongoing++;\r\n' \
  '        xhrip.send();\r\n' \
  '      }\r\n' \
  '      function load_cb(t, mode3d=null) {\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        document.getElementById("save_icon").style.fontSize = "inherit";\r\n' \
  '        document.getElementById("save").disabled = false;\r\n' \
  '        document.getElementById("save").style.pointerEvents = "";\r\n' \
  '        if (t.status != 204) {\r\n' \
  '          if (t.responseURL.indexOf("?") < 0) {window.alert("{#jserror#}" + t.status.toString() + " " + t.statusText);}\r\n' \
  '          return false;\r\n'\
  '        } else if (mode3d) {\r\n' \
  '          window.open("http://" + host + location.port + "/3D/viewer.html?3d=" + mode3d + document.getElementById(`v3d${mode3d}dist`).innerHTML);\r\n' \
  '        }\r\n' \
  '        return true;\r\n'\
  '      }\r\n' \
  '      function error_cb(t) {\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        document.getElementById("save_icon").style.fontSize = "inherit";\r\n' \
  '        document.getElementById("save").disabled = false;\r\n' \
  '        document.getElementById("save").style.pointerEvents = "";\r\n' \
  '        if (t.responseURL.indexOf("?") < 0) {window.alert("{#jserror#}");}\r\n' \
  '      }\r\n' \
  '      function track_save(mode3d=null) {\r\n' \
  '        if (document.getElementById("save").disabled) {return;}\r\n' \
  '        if (! mode3d) {document.getElementById("save_icon").style.fontSize = "10%";}\r\n' \
  '        document.getElementById("save").disabled = true;\r\n' \
  '        document.getElementById("save").style.pointerEvents = "none";\r\n' \
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
  '        if (mode3d) {\r\n' \
  '          let msgn = show_msg("{#jm3dviewer1#}", 0);\r\n' \
  '           xhr.onload = (e) => {load_cb(e.target, mode3d)?show_msg("{#jm3dviewer2#}", 2, msgn):show_msg("{#jm3dviewer3#}", 10, msgn);};\r\n' \
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
  '        xhr_ongoing++;\r\n' \
  '        xhr.send(body);\r\n' \
  '      }\r\n' \
  '      function track_change(e) {\r\n' \
  '        e.stopPropagation();\r\n' \
  '        let elt = e.target;\r\n' \
  '        if (! elt) {return;}\r\n' \
  '        let eid = elt.id.match(/(^.*[0-9]+)(.*)$/);\r\n' \
  '        if (! eid) {return;}\r\n' \
  '        switch (eid[2]) {\r\n' \
  '          case "":\r\n' \
  '            if (eid[1].substring(0, 7) == "segment") {segment_checkbox(elt);} else {point_checkbox(elt);}\r\n' \
  '            break\r\n' \
  '          case "lat":\r\n' \
  '          case "lon":\r\n' \
  '            point_edit_oc(eid[1], true, true);\r\n' \
  '            break\r\n' \
  '          case "ele":\r\n' \
  '          case "alt":\r\n' \
  '          case "time":\r\n' \
  '            point_edit_oc(eid[1], true, false);\r\n' \
  '            break\r\n' \
  '          case "name":\r\n' \
  '            point_edit_oc(eid[1], false, false);\r\n' \
  '            break\r\n' \
  '        }\r\n' \
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
  '  <body style="background-color:rgb(40,45,50);color:rgb(225,225,225);margin-top:2px;margin-bottom:0;">\r\n' \
  '    <table style="width:98vw;">\r\n' \
  '      <colgroup>\r\n' \
  '        <col style="width:21em;">\r\n' \
  '        <col style="width:calc(98vw - 21em);">\r\n' \
  '      </colgroup>\r\n' \
  '      <thead>\r\n' \
  '        <tr>\r\n' \
  '          <th colspan="2" style="text-align:left;font-size:120%;width:100%;border-bottom:1px darkgray solid;">\r\n' \
  '           <input type="text" id="name_track" name="name_track" autocomplete="off" value="##NAME##">\r\n' \
  '           <span style="display:inline-block;position:absolute;right:2vw;width:55em;overflow:hidden;text-align:right;font-size:80%;user-select:none;" oncontextmenu="event.preventDefault();"><button title="{#jundo#}" onclick="undo(false, ! event.altKey)">&cularr;</button><button title="{#jredo#}" style="margin-left:0.25em;" onclick="undo(true, ! event.altKey)">&curarr;</button><button title="{#jinsertb#}" style="margin-left:0.75em;" onclick="point_insert(\'b\')">&boxdR;</button><button title="{#jinserta#}" style="margin-left:0.25em;" onclick="point_insert(\'a\')">&boxuR;</button><button title="{#jpath#}" style="margin-left:0.25em;" onclick="build_path()">&rarrc;</button><button title="{#jelementup#}" style="margin-left:0.75em;" onclick="element_up()">&UpTeeArrow;</button><button title="{#jelementdown#}" style="margin-left:0.25em;" onclick="element_down()">&DownTeeArrow;</button><button title="{#jsegmentcut#}" style="margin-left:0.25em;" onclick="segment_cut()">&latail;</button><button title="{#jsegmentabsorb#}" style="margin-left:0.25em;"onclick="segment_absorb()">&ratail;</button><button title="{#jsegmentreverse#}" style="margin-left:0.25em;"onclick="segment_reverse()">&rlarr;</button><button title="{#jelevationsadd#}" style="margin-left:0.75em;" onclick="ele_adds(false, event.altKey)">&plusacir;</button><button title="{#jelevationsreplace#}" style="margin-left:0.25em;" onclick="event.shiftKey?ele_alt_switch():ele_adds(true, event.altKey)"><span style="vertical-align:0.2em;line-height:0.8em;">&wedgeq;</span></button><button title="{#jaltitudesjoin#}" style="margin-left:0.25em;" onclick="alt_join()">&apacir;</button><button title="{#jdatetime#}" style="margin-left:0.25em;" onclick="datetime_interpolate(event.shiftKey?true:false)">&#9201;</button><button title="{#jsave#}" id="save" style="margin-left:1.25em;" onclick="track_save()"><span id="save_icon" style="line-height:1em;font-size:inherit">&#128190;</span></button><button title="{#jswitchpoints#}" style="margin-left:1.25em;" onclick="event.ctrlKey?switch_dfpanel():(event.shiftKey?segment_filter():switch_dots())">&EmptySmallSquare;</button><button title="{#jgraph#}" style="margin-left:0.25em;" onclick="(event.shiftKey||event.ctrlKey||event.altKey)?switch_filterpanel(event.shiftKey?1:(event.ctrlKey?2:3)):refresh_graph(true)">&angrt;</button><button title="{#j3dviewer#}" style="margin-left:0.25em;" onclick="event.ctrlKey?switch_3Dpanel():open_3D(event.altKey?\'s\':\'p\')">3D</button><select id="tset" name="tset" title="{#jtset#}" autocomplete="off" style="margin-left:0.75em;" onmousedown="switch_sel(event, this)" onchange="switch_tiles(this.selectedIndex, -1)">##TSETS##</select><select id="eset" name="eset" title="{#jeset#}" autocomplete="off" style="display:none;margin-left:0.75em;" onmousedown="switch_sel(event, this)" onchange="switch_elevations(this.selectedIndex)">##ESETS##</select><select id="iset" name="iset" title="{#jiset#}" autocomplete="off" style="display:none;margin-left:0.75em;" onmousedown="switch_sel(event, this)" onchange="switch_itineraries(this.selectedIndex)">##ISETS##</select><button title="{#jminus#}" style="margin-left:0.25em;" onclick="event.ctrlKey?map_adjust(\'-\', \'a\'):(event.shiftKey?map_adjust(\'-\', \'e\'):zoom_dec())">-</button><span id="matrix" style="display:none;width:1.5em;">--</span><button id="tlock" title="{#jlock#}" style="display:none;width:1em" onclick="switch_tlock()">&#128275;&#xfe0e;</button><span id="zoom" style="display:inline-block;width:2em;text-align:center;">1</span><button title="{#jplus#}" style="" onclick="event.ctrlKey?map_adjust(\'+\', \'a\'):(event.shiftKey?map_adjust(\'+\', \'e\'):zoom_inc())">+</button></span>\r\n' + HTML_ATTENUATE_TEMPLATE + HTML_OPACITYPANEL_TEMPLATE + HTML_DFMTPANEL_TEMPLATE + HTML_FILTERPANEL_TEMPLATE + HTML_3DPANEL_TEMPLATE + \
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
  '                <form id="waypointsform" autocomplete="off" onchange="track_change(event);" onsubmit="return(false);">\r\n                  #<#WAYPOINTS#>#\r\n' \
  '                </form>\r\n' \
  '              </div>\r\n' \
  '              <div id="points" style="overflow-y:scroll;overflow-x:hidden;height:88%;font-size:80%">\r\n' \
  '                {#jpoints#}&nbsp;<svg width="7" height="7" stroke="green" stroke-width="1.5" fill="none"><rect x="1" y="1" width="5" height="5"/></svg><br>\r\n' \
  '                <form id="pointsform" autocomplete="off" onchange="track_change(event);" onsubmit="return(false);">\r\n                  #<#POINTS#>#\r\n' \
  '                </form>\r\n' \
  '              </div>\r\n' \
  '            </div>\r\n' \
  '          </td>\r\n' \
  '          <td style="display:table-cell;vertical-align:top;position:relative;">\r\n' \
  '            <div id="view" style="overflow:hidden;position:absolute;width:100%;height:calc(99vh - 2.4em - 16px);line-height:0;user-select:none;" onmousedown="mouse_down(event)" onclick="mouse_click(event)" onwheel="mouse_wheel(event)" onpointerdown="pointer_down(event)">\r\n' \
  '              <div id="background" style="position:absolute;top:0px;left:0px;width:100%;height:100%;backdrop-filter:var(--filter);pointer-events:none;"></div>\r\n' \
  '              <div id="handle" style="position:relative;top:0px;left:0px;width:100px;height:100px;pointer-events:none;">#<#PATHES#>#\r\n#<#WAYDOTS#>##<#DOTS#>#' \
  '              </div>\r\n' \
  '              <div id="scrollbox" style="left:0.1em;line-height:1em;">\r\n' \
  '                <span id="scrollcross" title="{#jscrollcross#}" onclick="event.shiftKey?switch_tiles(null, null):scrollcross(event.ctrlKey);event.stopPropagation()" onmousedown="event.stopPropagation()" onpointerdown="event.stopPropagation()" oncontextmenu="event.stopPropagation();event.preventDefault();" style="vertical-align:middle;color:rgb(90,90,90);cursor:pointer;">&#10012;</span>\r\n' \
  '              </div>\r\n' + HTML_SSB_GRAPH_TEMPLATE + \
  '    <script>\r\n' \
  '      var mousex = null;\r\n' \
  '      var mousey = null;\r\n' \
  '      var viewpane = document.getElementById("view");\r\n' \
  '      var handle = document.getElementById("handle");\r\n' \
  '      var hand = null;\r\n' \
  '      var hand_m = false;\r\n' \
  '      var mouse_out = null;\r\n' \
  '      var pointer_e = null;\r\n' \
  '      var mouse_ocm = null;\r\n' \
  '      function pointer_down(e) {\r\n' \
  '        pointer_e = e.pointerId;\r\n' \
  '      }\r\n' \
  '      function mouse_down(e) {\r\n' \
  '        if (e.button != 0 && e.button != 2) {return;}\r\n' \
  '        mousex = e.pageX;\r\n' \
  '        mousey = e.pageY;\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '        document.onmousemove = mouse_move;\r\n' \
  '        document.onmouseup = mouse_up;\r\n' \
  '        if (e.button == 2) {\r\n' \
  '          if (mouse_ocm) {clearTimeout(mouse_ocm); mouse_ocm=null;}\r\n' \
  '          document.oncontextmenu = mouse_click;\r\n' \
  '        }\r\n' \
  '        scrollmode_ex = scrollmode;\r\n' \
  '        scrollmode = 0;\r\n' \
  '        let elt = e.target;\r\n' \
  '        if (! elt) {return;}\r\n' \
  '        if (document.activeElement) {\r\n' \
  '          if (document.activeElement.nodeName != "BODY" && (e.button == 2 || elt.id.indexOf("dot") < 0 || (document.activeElement.id || "").slice(0, -2) != elt.id.replace("dot", "point") + "l")) {document.activeElement.blur();}\r\n' \
  '        }\r\n' \
  '        if (e.button == 0) {\r\n' \
  '          if (elt.id == "view") {\r\n' \
  '            hand = elt;\r\n' \
  '            viewpane.style.cursor = "all-scroll";\r\n' \
  '            viewpane.setPointerCapture(pointer_e);\r\n' \
  '          } else if (elt.id.indexOf("dot") >= 0) {\r\n' \
  '            let pt = document.getElementById(elt.id.replace("dot", "point") + "desc");\r\n' \
  '            if (pt.htmlFor != focused) {\r\n' \
  '              element_click(null, pt);\r\n' \
  '              if (! dots_visible) {return;}\r\n' \
  '            }\r\n' \
  '            hand = elt;\r\n' \
  '            hand_m = false;\r\n' \
  '            viewpane.style.cursor = "crosshair";\r\n' \
  '            hand.style.cursor = "crosshair";\r\n' \
  '            viewpane.setPointerCapture(pointer_e);\r\n' \
  '          } else if (elt.id == "gbarc") {\r\n' \
  '            hand = elt;\r\n' \
  '            graph_point(parseFloat(document.getElementById("gbarc").style.left));\r\n' \
  '            hand.setAttribute("stroke", "darkgray");\r\n' \
  '            hand.setPointerCapture(pointer_e);\r\n' \
  '          } else if (elt.id == "graphc") {\r\n' \
  '            hand = document.getElementById("gbarc");\r\n' \
  '            hand.setAttribute("stroke", "darkgray");\r\n' \
  '            graph_point(document.getElementById("graphc").offsetLeft + e.offsetX);\r\n' \
  '            hand.setPointerCapture(pointer_e);\r\n' \
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
  '            viewpane.setPointerCapture(pointer_e);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_up(e) {\r\n' \
  '        mousex = null;\r\n' \
  '        mousey = null;\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '        document.onmousemove = null;\r\n' \
  '        document.onmouseup = null;\r\n' \
  '        scrollmode = scrollmode_ex;\r\n' \
  '        if (hand) {\r\n' \
  '          if (mouse_out != null) {\r\n' \
  '            window.clearInterval(mouse_out);\r\n' \
  '            mouse_out = null;\r\n' \
  '          }\r\n' \
  '          if (hand.id.indexOf("dot") >= 0) {\r\n' \
  '            viewpane.style.cursor = "";\r\n' \
  '            viewpane.releasePointerCapture(pointer_e);\r\n' \
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
  '            hand.releasePointerCapture(pointer_e);\r\n' \
  '            hand.setAttribute("stroke", "none");\r\n' \
  '            graph_point();\r\n' \
  '          } else {\r\n' \
  '            viewpane.style.cursor = "";\r\n' \
  '            viewpane.releasePointerCapture(pointer_e);\r\n' \
  '          }\r\n' \
  '          hand = null;\r\n' \
  '          pointer_e = null;\r\n' \
  '          if (e.button == 2) {\r\n' \
  '            mouse_ocm = setTimeout(function() {if (mouse_ocm) {document.oncontextmenu=null; mouse_ocm=null;};}, 100);\r\n' \
  '          }\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let elt = e.target;\r\n' \
  '        if (! (elt?elt.id:elt)) {\r\n' \
  '          mouse_ocm = setTimeout(function() {if (mouse_ocm) {document.oncontextmenu=null; mouse_ocm=null;};}, 100);\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (e.button == 2) {\r\n' \
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
  '          mouse_ocm = setTimeout(function() {if (mouse_ocm) {document.oncontextmenu=null; mouse_ocm=null;};}, 100);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_click(e) {\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '        document.oncontextmenu = null;\r\n' \
  '        if (mouse_ocm) {clearTimeout(mouse_ocm); mouse_ocm=null;}\r\n' \
  '        mouse_ocm = null;\r\n' \
  '        let elt = e.target;\r\n' \
  '        if (! elt) {return;}\r\n' \
  '        if (e.button == 0 && elt.id.substring(0, 4) == "path") {\r\n' \
  '          let seg = document.getElementById(elt.id.replace("path", "segment") + "desc");\r\n' \
  '          element_click(null, seg);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_outside() {\r\n' \
  '        if (mouse_out == null) {return;}\r\n' \
  '        let dx = 0;\r\n' \
  '        let dy = 0;\r\n' \
  '        let p = viewpane.parentNode;\r\n' \
  '        let pl = p.offsetLeft;\r\n' \
  '        let pr = pl + p.offsetWidth;\r\n' \
  '        let pt = p.offsetTop;\r\n' \
  '        let pb = pt + p.offsetHeight;\r\n' \
  '        if (mousex < pl) {\r\n' \
  '          dx = -Math.max(1, p.offsetWidth / 20);\r\n' \
  '        } else if (mousex > pr) {\r\n' \
  '          dx = Math.max(1, p.offsetWidth / 20);\r\n' \
  '        }\r\n' \
  '        if (mousey < pt) {\r\n' \
  '          dy = -Math.max(1, p.offsetHeight / 20);\r\n' \
  '        } else if (mousey > pb) {\r\n' \
  '          dy = Math.max(1, p.offsetHeight / 20);\r\n' \
  '        }\r\n' \
  '        if (dx || dy) {\r\n' \
  '          if (hand.id == "view") {\r\n' \
  '            scroll_dview(dx, dy);\r\n' \
  '          } else {\r\n' \
  '            scroll_dview(-dx, -dy);\r\n' \
  '            drag_dot(Math.min(Math.max(mousex, pl), pr) - pl, Math.min(Math.max(mousey, pt), pb) - pt);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_move(e) {\r\n' \
  '        if (mousex != null && mousey != null && hand != null) {\r\n' \
  '          if (hand.id == "gbarc") {\r\n' \
  '            graph_point(e.pageX - document.getElementById("graph").offsetLeft);\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '          let p = viewpane.parentNode;\r\n' \
  '          let pl = p.offsetLeft;\r\n' \
  '          let pr = pl + p.offsetWidth;\r\n' \
  '          let pt = p.offsetTop;\r\n' \
  '          let pb = pt + p.offsetHeight;\r\n' \
  '          let mx = e.pageX;\r\n' \
  '          let my = e.pageY;\r\n' \
  '          if (hand.id == "view") {\r\n' \
  '            cpx = cpy = null;\r\n' \
  '            scroll_dview(Math.min(Math.max(mx, pl), pr) - Math.min(Math.max(mousex, pl), pr), Math.min(Math.max(my, pt), pb) - Math.min(Math.max(mousey, pt), pb));\r\n' \
  '          } else if (hand.id.indexOf("dot") >= 0) {\r\n' \
  '            hand_m = true;\r\n' \
  '            drag_dot(Math.min(Math.max(mx, pl), pr) - pl, Math.min(Math.max(my, pt), pb) - pt);\r\n' \
  '          } else {return;}\r\n' \
  '          if (mx >= pl && mx <= pr && my >= pt && my <= pb) {\r\n' \
  '            if (mouse_out != null) {\r\n' \
  '              window.clearInterval(mouse_out);\r\n' \
  '              mouse_out = null;\r\n' \
  '            }\r\n' \
  '          } else if (mouse_out == null) {\r\n' \
  '            mouse_out = window.setInterval(mouse_outside, 100);\r\n' \
  '          }\r\n' \
  '          mousex = mx;\r\n' \
  '          mousey = my;\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_wheel(e) {\r\n' \
  '        e.preventDefault();\r\n' \
  '        if (e.ctrlKey) {\r\n' \
  '          let p = viewpane.parentNode;\r\n' \
  '          (e.deltaY<0?zoom_inc:zoom_dec)(e.pageX - p.offsetLeft, e.pageY - p.offsetTop);\r\n' \
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
  '          if (scrollmode > 0) {scroll_to_dot(dt, scrollmode == 2);}\r\n' \
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
  '          if (scrollmode > 0) {scroll_to_track(document.getElementById(seg.id.slice(0, -4).replace("segment", "track")), scrollmode == 2);}\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function page_unload() {\r\n' + HTML_PAGE_UNLOAD_TEMPLATE + \
  '        return "{#junload#}";\r\n' \
  '      }\r\n' \
  '      function page_load() {\r\n' \
  '        if (navigator.userAgent.toLowerCase().indexOf("firefox") > 0) {\r\n' \
  '          if (! document.getElementById("waypoint0cont")) {\r\n' \
  '            document.getElementById("waypoints").style.overflowY = "auto";\r\n' \
  '            document.getElementById("waypoints").style.borderRight = "solid rgb(34,37,42) 17px";\r\n' \
  '          }\r\n' \
  '        }\r\n' + HTML_PAGE_LOAD_TEMPLATE + \
  '        if (prev_state != null) {\r\n' \
  '          if (prev_state[4] == "true") {switch_dots();}\r\n' \
  '        }\r\n' \
  '        point_desc();\r\n' \
  '        window.onresize = (e) => {document.getElementById("points").style.height = "calc(100% - " + document.getElementById("waypoints").offsetHeight.toString() + "px)";rescale();refresh_graph()};\r\n' \
  '        document.getElementById("waypoints").style.maxHeight = "10vh";\r\n' \
  '        document.getElementById("waypoints").style.height = "";\r\n' \
  '        document.getElementById("points").style.height = "calc(100% - " + document.getElementById("waypoints").offsetHeight.toString() + "px)";\r\n' \
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
  '//      document.addEventListener("DOMContentLoaded", function () {window.history.replaceState({}, "", "/GPXTweaker.html");});\r\n' \
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
  '      var htopy = ##HTOPY##;\r\n' \
  '      var tholdsize = ##THOLDSIZE##;\r\n' \
  '      var tlayers = new Map([##TLAYERS##]);\r\n' \
  '      var tmaplibre = ##TMAPLIBRE##;'
  HTML_WAYPOINT_TEMPLATE = \
  '<div id="waypoint%scont">\r\n' \
  '                    <input type="checkbox" id="waypoint%s" checked name="waypoint%s" value="initial" onmouseover="point_over(this)" onmouseout="point_outside(this)">\r\n' \
  '                    <label for="waypoint%s" id="waypoint%sdesc" onclick="element_click(event, this)" onmouseover="point_over(this)" onmouseout="point_outside(this)"><br></label><br>\r\n' \
  '                    <span id="waypoint%sfocus">\r\n' \
  '                      <label for="waypoint%slat">{jlat}</label>\r\n' \
  '                      <input type="text" id="waypoint%slat" name="waypoint%slat" required pattern="[\\+\\-]?([0-9]+([.][0-9]*)?|[.][0-9]+)" value="%f"><br>\r\n' \
  '                      <label for="waypoint%slon">{jlon}</label>\r\n' \
  '                      <input type="text" id="waypoint%slon" name="waypoint%slon" required pattern="[\\+\\-]?([0-9]+([.][0-9]*)?|[.][0-9]+)" value="%f"><br>\r\n' \
  '                      <label for="waypoint%sele">{jele}</label>\r\n' \
  '                      <input type="text" id="waypoint%sele" name="waypoint%sele" pattern="([\\+\\-]?([0-9]+([.][0-9]*)?|[.][0-9]+))|" value="%s"><br>\r\n' \
  '                      <label for="waypoint%stime">{jhor}</label>\r\n' \
  '                      <input type="text" id="waypoint%stime" name="waypoint%stime" pattern="(([0-9]{{4}}-((01|03|05|07|08|10|12)-(0[1-9]|[12][0-9]|3[01])|(04|06|09|11)-(0[1-9]|[12][0-9]|30)|02-(0[1-9]|1[0-9]|2[0-8]))|(([02468][048]|[13579][26])00|[0-9][0-9](0[48]|[2468][048]|[13579][26]))-02-29).([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\\.[0-9]{{3}})?([Zz]|[\\+\\-]([01][0-9]|2[0-3]):[0-5][0-9])?)|" value="%s"><br>\r\n' \
  '                      <label for="waypoint%sname">{jname}</label>\r\n' \
  '                      <input type="text" id="waypoint%sname" name="waypoint%sname" value="%s"><br>\r\n' \
  '                    </span>\r\n' \
  '                  </div>'
  HTML_WAYPOINT_TEMPLATE = HTML_WAYPOINT_TEMPLATE.format_map(LSTRINGS['interface'])
  HTML_POINT_TEMPLATE = \
  '<div id="point%scont">\r\n' \
  '                    <input type="checkbox" id="point%s" checked name="point%s" value="initial" onmouseover="point_over(this)" onmouseout="point_outside(this)">\r\n' \
  '                    <label for="point%s" id="point%sdesc" onclick="element_click(event, this)"  onmouseover="point_over(this)" onmouseout="point_outside(this)"></label><br>\r\n' \
  '                    <span id="point%sfocus">\r\n' \
  '                      <label for="point%slat">{jlat}</label>\r\n' \
  '                      <input type="text" id="point%slat" name="point%slat" required pattern="[\\+\\-]?([0-9]+([.][0-9]*)?|[.][0-9]+)" value ="%f" ><br>\r\n' \
  '                      <label for="point%slon">{jlon}</label>\r\n' \
  '                      <input type="text" id="point%slon" name="point%slon" required pattern="[\\+\\-]?([0-9]+([.][0-9]*)?|[.][0-9]+)" value="%f"><br>\r\n' \
  '                      <label for="point%sele">{jele}</label>\r\n' \
  '                      <input type="text" id="point%sele" name="point%sele" pattern="([\\+\\-]?([0-9]+([.][0-9]*)?|[.][0-9]+))|" value="%s"><br>\r\n' \
  '                      <label for="point%salt">{jalt}</label>\r\n' \
  '                      <input type="text" id="point%salt" name="point%salt" pattern="([\\+\\-]?([0-9]+([.][0-9]*)?|[.][0-9]+))|" value="%s"><br>\r\n' \
  '                      <label for="point%stime">{jhor}</label>\r\n' \
  '                      <input type="text" id="point%stime" name="point%stime" pattern="(([0-9]{{4}}-((01|03|05|07|08|10|12)-(0[1-9]|[12][0-9]|3[01])|(04|06|09|11)-(0[1-9]|[12][0-9]|30)|02-(0[1-9]|1[0-9]|2[0-8]))|(([02468][048]|[13579][26])00|[0-9][0-9](0[48]|[2468][048]|[13579][26]))-02-29).([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\\.[0-9]{{3}})?([Zz]|[\\+\\-]([01][0-9]|2[0-3]):[0-5][0-9])?)|" value="%s"><br>\r\n' \
  '                    </span>\r\n' \
  '                  </div>'
  HTML_POINT_TEMPLATE = HTML_POINT_TEMPLATE.format_map(LSTRINGS['interface'])
  HTML_SEGMENT_TEMPLATE = \
  '<div id="segment%scont">\r\n' \
  '                    <input type="checkbox" id="segment%s" checked name="segment%s" value="segment">\r\n' \
  '                    <label for="segment%s" id="segment%sdesc" style="text-decoration:inherit;" onclick="element_click(event, this, false)">&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&nbsp;{jsegment} %s&nbsp;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;</label>\r\n' \
  '                    <br>'
  HTML_SEGMENT_TEMPLATE = HTML_SEGMENT_TEMPLATE.format_map(LSTRINGS['interface'])
  HTML_PATH_TEMPLATE = \
  '\r\n' \
  '              <svg id="track%s" viewbox="##VIEWBOX##" style="width:##WIDTH##;height:##HEIGHT##;top:##TOP##;left:##LEFT##;">\r\n' \
  '                <path id="path%s" d="%s"/>\r\n' \
  '                <text dy="0.25em">\r\n' \
  '                  <textPath href="#path%s">##ARROWS##</textPath>\r\n' \
  '                </text>\r\n' \
  '              </svg>'
  HTML_WAYDOT_TEMPLATE = \
  '              <svg id="waydot%s" width="8" height="8" style="left:calc(%.1fpx / var(--scale) - 4px);top:calc(%.1fpx / var(--scale) - 4px);">\r\n' \
  '                <circle cx="4" cy="4" r="3" />\r\n' \
  '              </svg>\r\n'
  HTML_DOT_TEMPLATE = \
  '              <svg id="dot%s" width="7" height="7" style="left:calc(%.1fpx / var(--scale) - 3.5px);top:calc(%.1fpx / var(--scale) - 3.5px);display:none;">\r\n' \
  '                <rect x="1" y="1" width="5" height="5"/>\r\n' \
  '              </svg>\r\n'
  HTML_3D_STYLES_TEMPLATE = \
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
  '        vertical-align:top;\r\n' \
  '        color:inherit;\r\n' \
  '        font-size:inherit;\r\n' \
  '      }\r\n' \
  '      button:enabled {\r\n' \
  '        cursor:pointer;\r\n' \
  '      }\r\n' \
  '      input {\r\n' \
  '        background-color:rgb(30,30,35);\r\n' \
  '        color:inherit;\r\n' \
  '        font-size:inherit;\r\n' \
  '        margin-left:0.7em;\r\n' \
  '      }\r\n' \
  '      input:enabled {\r\n' \
  '        cursor:pointer;\r\n' \
  '      }\r\n' \
  '      input[type=range] {\r\n' \
  '        width:9em;\r\n' \
  '      }\r\n' \
  '      span {\r\n' \
  '        display:inline-block;\r\n' \
  '        text-align:center;\r\n' \
  '      }\r\n' \
  '      br+span {\r\n' \
  '        width:1.4em;\r\n' \
  '      }\r\n' \
  '      br+span+span {\r\n' \
  '        width:6em;\r\n' \
  '        margin-left:0.8em;\r\n' \
  '      }\r\n' \
  '      input:focus+br+span+span, input:focus+button+br+span+span, input:focus+input+br+span+span  {\r\n' \
  '        color:rgb(200,250,240);\r\n' \
  '      }\r\n' \
  '      br+span+span+span {\r\n' \
  '        width:3em;\r\n' \
  '      }\r\n' \
  '      input[type=radio] {\r\n' \
  '        vertical-align:middle;\r\n' \
  '        margin-bottom:0.4em;\r\n' \
  '      }\r\n' \
  '      input[type=checkbox] {\r\n' \
  '        appearance:none;\r\n' \
  '        position:absolute;\r\n' \
  '        left:10.5em;\r\n' \
  '        vertical-align:top;\r\n' \
  '        width:1.2em;\r\n' \
  '        height:1.2em;\r\n' \
  '        margin-left:0.1em;\r\n' \
  '      }\r\n' \
  '      input[type=checkbox]:checked::before {\r\n' \
  '        content:"\\2714";\r\n' \
  '        display:inline-block;\r\n' \
  '        text-align:center;\r\n' \
  '        width:100%;\r\n' \
  '        font-size:90%;\r\n' \
  '        font-weight:bold;\r\n' \
  '      }\r\n' \
  '      input[id$=_info] {\r\n' \
  '        position:absolute;\r\n' \
  '        left:1.5em;\r\n' \
  '        width:calc(100vw - 10vh - 20em);\r\n' \
  '        margin:0;\r\n' \
  '        opacity:inherit;\r\n' \
  '        background-color:inherit;\r\n' \
  '        border:none;\r\n' \
  '        outline:none;\r\n' \
  '        cursor:initial;\r\n' \
  '      }\r\n' \
  '      label[for$=_info] {\r\n' \
  '        position:absolute;\r\n' \
  '        left:2px;\r\n' \
  '        width:1em;\r\n' \
  '        text-align:center;\r\n' \
  '      }\r\n' \
  '    </style>\r\n'
  HTML_3D_FORM1_TEMPLATE = \
  '            <br><br>\r\n' \
  '            <p><label for="cursor_rangle">{#jrotation#}</label></p>\r\n' \
  '            <input type="range" id="cursor_rangle" min="0" max="360" step="any" value="0" disabled oninput="set_param(\'r\')">&nbsp;&nbsp;<button id="button_rangle" disabled onclick="toggle_rotation()">&#9199;</button>\r\n' \
  '            <br><span>0</span><span id="cursorv_rangle">0</span><span>360</span>\r\n' \
  '            <br><br>\r\n'
  HTML_3D_FORM2_TEMPLATE = \
  '            <br><br>\r\n' \
  '            <p>{#jtexture#}</p>\r\n' \
  '            <input type="radio" id="radio_yiso" name="texture" checked disabled onclick="toggle_filling(0)"><label for="radio_yiso">{#jtextureyiso#}</label><br>\r\n' \
  '            <input type="radio" id="radio_ziso" name="texture" disabled onclick="toggle_filling(1)"><label for="radio_ziso">{#jtextureziso#}</label><br>\r\n' \
  '            <input type="radio" id="radio_map" name="texture" disabled onclick="toggle_filling(2)"><label for="radio_map">{#jtexturemap#}</label>\r\n' \
  '            <br><br>\r\n' \
  '            <p>{#jdimming#}</p>\r\n' \
  '            <input type="radio" id="radio_dimn" name="dimming" disabled onclick="toggle_dimming(0)"><label for="radio_dimn">{#jdimmingnone#}</label><br>\r\n' \
  '            <input type="radio" id="radio_dimz" name="dimming" disabled onclick="toggle_dimming(1)"><label for="radio_dimz">{#jdimmingz#}</label><br>\r\n'
  HTML_3D_FORM3_TEMPLATE = \
  '            <br><br>\r\n' \
  '            <p><label for="cursor_ltangle">{#jltilt#}</label></p>\r\n' \
  '            <input type="range" id="cursor_ltangle" min="0" max="90" step="any" value ="0" disabled oninput="set_param(\'lt\')">\r\n' \
  '            <br><span>0</span><span id="cursorv_ltangle">0</span><span>90</span>\r\n' \
  '            <br><br>\r\n' \
  '            <p><label for="cursor_lrangle">{#jlrotation#}</label></p>\r\n' \
  '            <input type="range" id="cursor_lrangle" min="0" max="360" step="any" value ="0" disabled oninput="set_param(\'lr\')">&nbsp;&nbsp;<button id="button_lrangle" disabled onclick="toggle_lrotation()">&#9199;</button>\r\n' \
  '            <br><span>0</span><span id="cursorv_lrangle">0</span><span>360</span>\r\n'
  HTML_3D_GLOBALVARS_TEMPLATE = \
  '      const host = location.hostname + ":";\r\n' \
  '      var canvas = document.getElementById("canvas");\r\n' \
  '      var gl = canvas.getContext("webgl2", {preserveDrawingBuffer: true});\r\n' \
  '      canvas.addEventListener("webglcontextlost", function(event) {event.preventDefault();gl_programs=new Map();}, false);\r\n' \
  '      canvas.addEventListener("webglcontextrestored", function(event) {gl=canvas.getContext("webgl2", {preserveDrawingBuffer:true});canvas_init();canvas_redraw();}, false);\r\n' \
  '      var c_tangle = document.getElementById("cursor_tangle");\r\n' \
  '      var cv_tangle = document.getElementById("cursorv_tangle");\r\n' \
  '      var c_rangle = document.getElementById("cursor_rangle");\r\n' \
  '      var cv_rangle = document.getElementById("cursorv_rangle");\r\n' \
  '      var b_rangle = document.getElementById("button_rangle");\r\n' \
  '      var r_yiso = document.getElementById("radio_yiso");\r\n' \
  '      var r_ziso = document.getElementById("radio_ziso");\r\n' \
  '      var r_map = document.getElementById("radio_map");\r\n' \
  '      var r_dimn = document.getElementById("radio_dimn");\r\n' \
  '      var r_dimz = document.getElementById("radio_dimz");\r\n' \
  '      var r_dims = document.getElementById("radio_dims");\r\n' \
  '      var c_ltangle = document.getElementById("cursor_ltangle");\r\n' \
  '      var cv_ltangle = document.getElementById("cursorv_ltangle");\r\n' \
  '      var c_lrangle = document.getElementById("cursor_lrangle");\r\n' \
  '      var cv_lrangle = document.getElementById("cursorv_lrangle");\r\n' \
  '      var b_lrangle = document.getElementById("button_lrangle");\r\n' \
  '      var lvx = null;\r\n' \
  '      var lvy = null;\r\n' \
  '      var vpositions = null;\r\n' \
  '      var vnormals = null;\r\n' \
  '      var trpositions = null;\r\n' \
  '      var tvposition = null;\r\n' \
  '      var tvnormal = null;\r\n' \
  '      var ldirection = null;\r\n' \
  '      var vmatrix = null\r\n' \
  '      var lmatrix = null;\r\n' \
  '      const max_size = gl.getParameter(gl.MAX_TEXTURE_SIZE);\r\n' \
  '      var mtex = 0;\r\n' \
  '      var trtex = 1;\r\n' \
  '      var dtex = 2;\r\n' \
  '      var map_texture = null;\r\n' \
  '      var tr_texture = null;\r\n' \
  '      var d_texture = null;\r\n' \
  '      var sfrbuf = null;\r\n' \
  '      var fillmode = 0;\r\n' \
  '      var pmode = 0;\r\n' \
  '      var dmode = 2;\r\n' \
  '      var ylmag = 1;\r\n' \
  '      var ctangle = null;\r\n' \
  '      var stangle = null;\r\n' \
  '      var crangle = null;\r\n' \
  '      var srangle = null;\r\n' \
  '      var nrot = 0;\r\n' \
  '      var nlrot = 0;\r\n' \
  '      var rep_rot = null;\r\n' \
  '      var rep_lrot = null;\r\n' \
  '      var ltangle_rotmax = null;\r\n' \
  '      var cltangle = null;\r\n' \
  '      var sltangle = null;\r\n' \
  '      var clrangle = null;\r\n' \
  '      var slrangle = null;\r\n' \
  '      var gl_programs = new Map();\r\n' \
  '      var cur_prog = null;\r\n'
  HTML_3D_MAT_TEMPLATE = \
  '      function mat4_mult(p, m) {\r\n' \
  '        let q = m.slice();\r\n' \
  '        for (let r=0; r<4; r++) {\r\n' \
  '          for (let c=0; c<4; c++) {\r\n' \
  '            let v = 0;\r\n' \
  '            for (let i=0; i<4; i++) {v += p[4 * r + i] * q[4 * i + c];}\r\n' \
  '            m[4 * r + c] = v;\r\n' \
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
  '      }\r\n'
  HTML_3D_UTIL_TEMPLATE = \
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
  '            gl.vertexAttribPointer(gl_programs.get(cur_prog).get(n), ts[1], gl.FLOAT, false, ts.length>2?ts[2]:0, ts.length>3?ts[3]:0);\r\n' \
  '            if (ts.length > 4) {gl.vertexAttribDivisor(gl_programs.get(cur_prog).get(n), ts[4]);}\r\n' \
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
  '              case "vec2":\r\n' \
  '                gl.uniform2fv(gl_programs.get(cur_prog).get(n), window[n]);\r\n' \
  '                break;\r\n' \
  '              case "vec3":\r\n' \
  '                gl.uniform3fv(gl_programs.get(cur_prog).get(n), window[n]);\r\n' \
  '                break;\r\n' \
  '              case "vec4":\r\n' \
  '                gl.uniform4fv(gl_programs.get(cur_prog).get(n), window[n]);\r\n' \
  '                break;\r\n' \
  '              case "mat4":\r\n' \
  '                gl.uniformMatrix4fv(gl_programs.get(cur_prog).get(n), true, window[n]);\r\n' \
  '                break;\r\n' \
  '              case "sampler2D":\r\n' \
  '              case "sampler2DShadow":\r\n' \
  '              case "int":\r\n' \
  '                gl.uniform1i(gl_programs.get(cur_prog).get(n), window[n]);\r\n' \
  '                break;\r\n' \
  '              default:\r\n' \
  '                gl.uniform1f(gl_programs.get(cur_prog).get(n), window[n]);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function buffer_load(src) {\r\n' \
  '        let gl_buffer = gl.createBuffer();\r\n' \
  '        gl.bindBuffer(gl.ARRAY_BUFFER, gl_buffer);\r\n' \
  '        gl.bufferData(gl.ARRAY_BUFFER, src, gl.STATIC_DRAW);\r\n' \
  '        gl.bindBuffer(gl.ARRAY_BUFFER, null);\r\n' \
  '        return gl_buffer;\r\n' \
  '      }\r\n' \
  '      function texture_load(unit, src, rgb=true) {\r\n' \
  '        let gl_texture = gl.createTexture();\r\n' \
  '        gl.activeTexture(unit);\r\n' \
  '        gl.bindTexture(gl.TEXTURE_2D, gl_texture);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, rgb?gl.LINEAR_MIPMAP_LINEAR:gl.LINEAR);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);\r\n' \
  '        if (Array.isArray(src)) {\r\n' \
  '          gl.texImage2D(gl.TEXTURE_2D, 0, rgb?gl.RGB:gl.R8, 1, 1, 0, rgb?gl.RGB:gl.RED, gl.UNSIGNED_BYTE, new Uint8Array(src))\r\n' \
  '        } else {\r\n' \
  '          gl.texImage2D(gl.TEXTURE_2D, 0, rgb?gl.RGB:gl.R8, rgb?gl.RGB:gl.RED, gl.UNSIGNED_BYTE, src);\r\n' \
  '        }\r\n' \
  '        if (rgb) {gl.generateMipmap(gl.TEXTURE_2D);}\r\n' \
  '        return gl_texture;\r\n' \
  '      }\r\n' \
  '      function texture_attach(unit) {\r\n' \
  '        let gl_texture = gl.createTexture();\r\n' \
  '        gl.activeTexture(unit);\r\n' \
  '        gl.bindTexture(gl.TEXTURE_2D, gl_texture);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_COMPARE_MODE, gl.COMPARE_REF_TO_TEXTURE);\r\n' \
  '        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_COMPARE_FUNC, gl.LESS);\r\n' \
  '        gl.texImage2D(gl.TEXTURE_2D, 0, gl.DEPTH_COMPONENT16, d_size, d_size, 0, gl.DEPTH_COMPONENT, gl.UNSIGNED_SHORT, null);\r\n' \
  '        gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.TEXTURE_2D, gl_texture, 0);\r\n' \
  '        return gl_texture;\r\n' \
  '      }\r\n'
  HTML_3D_MAP_TEMPLATE = \
  '        function create_map() {\r\n' \
  '          r_map.nextElementSibling.innerHTML = "{#jtexturemaploading#}".replace("%s", "0");\r\n' \
  '          let nrow = tmaxrow + 1 - tminrow;\r\n' \
  '          let ncol = tmaxcol + 1 - tmincol;\r\n' \
  '          let mheight = m_size * nrow / Math.max(nrow, ncol);\r\n' \
  '          let mwidth = m_size * ncol / Math.max(nrow, ncol);\r\n' \
  '          let ntiles = nrow * ncol;\r\n' \
  '          let ltiles = 0;\r\n' \
  '          let ltp = "0%";\r\n' \
  '          let cnv2d = document.createElement("canvas");\r\n' \
  '          let ctx = cnv2d.getContext("2d", {alpha: false});\r\n' \
  '          cnv2d.height = mheight;\r\n' \
  '          mheight = cnv2d.height;\r\n' \
  '          cnv2d.width = mwidth;\r\n' \
  '          mwidth = cnv2d.width;\r\n' \
  '          ctx.fillStyle = "RGB(0,127,0)";\r\n' \
  '          ctx.fillRect(0, 0, mwidth, mheight);\r\n' \
  '          function map_complete() {\r\n' \
  '            gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);\r\n' \
  '            map_texture = texture_load(gl.TEXTURE0, cnv2d);\r\n' \
  '            gl.flush();\r\n' \
  '            gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);\r\n' \
  '            r_map.nextElementSibling.innerHTML = "{#jtexturemap#}";\r\n' \
  '            r_map.disabled = false;\r\n' \
  '          }\r\n' \
  '          let crow = tminrow;\r\n' \
  '          let prom_res = null;\r\n' \
  '          function terr_cb() {\r\n' \
  '            ltiles++;\r\n' \
  '            let ltpn = Math.floor(100 * ltiles / ntiles).toString();\r\n' \
  '            if (ltpn != ltp) {\r\n' \
  '              ltp = ltpn;\r\n' \
  '              r_map.nextElementSibling.innerHTML = "{#jtexturemaploading#}".replace("%s", ltp);\r\n' \
  '            }\r\n' \
  '            if (ltiles == ntiles) {map_complete();}\r\n' \
  '            if (prom_res && (crow - tminrow) * ncol <= ltiles + ##TILEMAXPENDING##) {\r\n' \
  '              prom_res();\r\n' \
  '              prom_res = null;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          function tload_cb(tile, row, col) {\r\n' \
  '            ctx.drawImage(tile, Math.round((col - tmincol) / ncol * mwidth), Math.round((row - tminrow) / nrow * mheight), Math.round((col + 1 - tmincol) / ncol * mwidth) - Math.round((col - tmincol) / ncol * mwidth), Math.round((row + 1 - tminrow) / nrow * mheight) - Math.round((row - tminrow) / nrow * mheight));\r\n' \
  '            terr_cb();\r\n' \
  '          }\r\n' \
  '          async function add_row_tile() {\r\n' \
  '            let row = crow;\r\n' \
  '            if ((row - tminrow) * ncol > ltiles + ##TILEMAXPENDING##) {\r\n' \
  '              let prom = new Promise(function(resolve, reject) {prom_res = resolve;});\r\n' \
  '              await prom;\r\n' \
  '            }\r\n' \
  '            for (let col=tmincol; col<=tmaxcol; col++) {\r\n' \
  '              let tile = new Image();\r\n' \
  '              tile.crossOrigin = "anonymous";\r\n' \
  '              tile.onload = (e) => {tload_cb(e.target, row, col);};\r\n' \
  '              tile.onerror = (e) => {terr_cb();};\r\n' \
  '              tile.src = "http://" + host + (portmin + (row + col) % (portmax + 1 - portmin)).toString() + ##TILEPATH##;\r\n' \
  '            }\r\n' \
  '            if (crow < tmaxrow) {\r\n' \
  '              crow++;\r\n' \
  '              add_row_tile();\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          setTimeout(add_row_tile, 1);\r\n' \
  '        }\r\n'
  HTML_3D_ROT_TEMPLATE = \
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
  '        if (lrangle >= 270) {\r\n' \
  '          nlrot ++;\r\n' \
  '          lrangle -= 180;\r\n' \
  '        }\r\n' \
  '        set_param("lr", lrangle);\r\n' \
  '        set_param("lt", Math.sin((lrangle - 90) * Math.PI / 180) * ltangle_rotmax);\r\n' \
  '        canvas_redraw();\r\n' \
  '      }\r\n'
  HTML_3D_LOAD_TEMPLATE = \
  '      function data_load() {\r\n' \
  '        function derror_cb(t) {\r\n' \
  '        }\r\n' \
  '        function dload_cb(t) {\r\n' \
  '          if (t.status != 200) {derror_cb(); return;}\r\n' \
  '          lvx = (new Uint32Array(t.response, 0, 1))[0];\r\n' \
  '          let vx = new Float32Array(t.response, 4, lvx);\r\n' \
  '          lvy = (new Uint32Array(t.response, 4 * (1 + lvx), 1))[0];\r\n' \
  '          let vy = new Float32Array(t.response, 4 * (2 + lvx) , lvy);\r\n' \
  '          let lvz = (new Uint32Array(t.response, 4 * (2 + lvx + lvy), 1))[0];\r\n' \
  '          let vz = new Float32Array(t.response, 4 * (3 + lvx + lvy), lvz);\r\n' \
  '          vpositions = new Float32Array((lvy - 1) * (lvx + 1) * 6);\r\n' \
  '          vnormals = new Float32Array((lvy - 1) * (lvx + 1) * 6);\r\n' \
  '          let i = 0;\r\n' \
  '          let n = 0;\r\n' \
  '          for (let iy=0; iy<lvy-1; iy++) {\r\n' \
  '            for (let ix=0; ix<lvx; ix++) {\r\n' \
  '              vpositions[i] = vx[ix];\r\n' \
  '              vpositions[i + 1] = vy[iy];\r\n' \
  '              vpositions[i + 2] = vz[iy * lvx + ix];\r\n' \
  '              vpositions[i + 3] = vx[ix];\r\n' \
  '              vpositions[i + 4] = vy[iy + 1];\r\n' \
  '              vpositions[i + 5] = vz[(iy + 1) * lvx + ix];\r\n' \
  '              if (iy == 0) {\r\n' \
  '                vnormals[i] = (vz[iy * lvx + Math.min(ix + 1, lvx - 1)] - vz[iy * lvx + Math.max(ix - 1, 0)]) / (vx[Math.min(ix + 1, lvx - 1)] - vx[Math.max(ix - 1, 0)]);\r\n' \
  '                vnormals[i + 1] = (vz[(iy + 1) * lvx + ix] - vz[Math.max(iy - 1, 0) * lvx + ix]) / (vy[iy + 1] - vy[Math.max(iy - 1, 0)]);\r\n' \
  '                vnormals[i + 2] = 1;\r\n' \
  '                n = Math.sqrt(vnormals[i]**2 + vnormals[i + 1]**2 + 1);\r\n' \
  '                vnormals[i] /= -n;\r\n' \
  '                vnormals[i + 1] /= -n;\r\n' \
  '                vnormals[i + 2] /= n;\r\n' \
  '              } else {\r\n' \
  '                vnormals[i] = vnormals[i + 3 - 6 * (lvx + 1)];\r\n' \
  '                vnormals[i + 1] = vnormals[i + 4 - 6 * (lvx + 1)];\r\n' \
  '                vnormals[i + 2] = vnormals[i + 5 - 6 * (lvx + 1)];\r\n' \
  '              }\r\n' \
  '              vnormals[i + 3] = (vz[(iy + 1) * lvx + Math.min(ix + 1, lvx - 1)] - vz[(iy + 1) * lvx + Math.max(ix - 1, 0)]) / (vx[Math.min(ix + 1, lvx - 1)] - vx[Math.max(ix - 1, 0)]);\r\n' \
  '              vnormals[i + 4] = (vz[Math.min(iy + 2, lvy - 1) * lvx + ix] - vz[iy * lvx + ix]) / (vy[Math.min(iy + 2, lvy - 1)] - vy[iy]);\r\n' \
  '              vnormals[i + 5] = 1;\r\n' \
  '              n = Math.sqrt(vnormals[i + 3]**2 + vnormals[i + 4]**2 + 1);\r\n' \
  '              vnormals[i + 3] /= -n;\r\n' \
  '              vnormals[i + 4] /= -n;\r\n' \
  '              vnormals[i + 5] /= n;\r\n' \
  '              i += 6;\r\n' \
  '            }\r\n' \
  '            vpositions[i] = vx[lvx - 1];\r\n' \
  '            vpositions[i + 1] = vy[iy + 1];\r\n' \
  '            vpositions[i + 2] = vz[(iy + 1) * lvx + lvx - 1];\r\n' \
  '            vpositions[i + 3] = vx[0];\r\n' \
  '            vpositions[i + 4] = vy[iy + 1];\r\n' \
  '            vpositions[i + 5] = vz[(iy + 1) * lvx];\r\n' \
  '            vnormals[i] = vnormals[i - 3];\r\n' \
  '            vnormals[i + 1] = vnormals[i - 2];\r\n' \
  '            vnormals[i + 2] = vnormals[i - 1];\r\n' \
  '            vnormals[i + 3] = vnormals[i + 3 - 6 * lvx];\r\n' \
  '            vnormals[i + 4] = vnormals[i + 4 - 6 * lvx];\r\n' \
  '            vnormals[i + 5] = vnormals[i + 5 - 6 * lvx];\r\n' \
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
  '          canvas_init();\r\n'
  HTML_3D_TOGGLE_TEMPLATE = \
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
  '          set_param("lt", ltangle_rotmax);\r\n' \
  '          canvas_redraw();\r\n' \
  '          c_lrangle.disabled = false;\r\n' \
  '          c_ltangle.disabled = false;\r\n' \
  '        } else {\r\n' \
  '          c_lrangle.disabled = true;\r\n' \
  '          c_ltangle.disabled = true;\r\n' \
  '          ltangle_rotmax = parseFloat(c_ltangle.value);\r\n' \
  '          set_param("lt", 0);\r\n' \
  '          set_param("lr", 90);\r\n' \
  '          nlrot = 0;\r\n' \
  '          rep_lrot = window.setInterval(function() {canvas_lrotate(number);}, 100);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function toggle_filling(mode) {\r\n' \
  '        if (mode == fillmode) {return;};\r\n' \
  '        fillmode = mode;\r\n' \
  '        canvas_redraw();\r\n' \
  '      }\r\n'
  HTML_3DP_TEMPLATE = \
  '<!DOCTYPE html>\r\n' \
  '<html lang="fr-FR">\r\n' \
  '  <head>\r\n' \
  '    <meta charset="utf-8">\r\n' \
  '    <title>GPXTweaker 3DViewer Panoramic</title>\r\n' + HTML_3D_STYLES_TEMPLATE + \
  '  </head>\r\n' \
  '  <body style="margin:0;background-color:rgb(40,45,50);color:rgb(225,225,225);user-select:none;">\r\n' \
  '    <table>\r\n' \
  '      <colgroup>\r\n' \
  '        <col style="width:calc(100vw - 14em);">\r\n' \
  '        <col style="width:14em;">\r\n' \
  '      </colgroup>\r\n' \
  '      <tbody>\r\n' \
  '        <tr style="display:table-row;">\r\n' \
  '        <td style="display:table-cell;position:relative;vertical-align:top;height:100vh;">\r\n' \
  '          <div style="position:absolute;top:0;left:0;width:100%;height:100%;overflow:auto;">\r\n' \
  '            <canvas id="canvas" width="100" height="100" style="position:absolute;top:0;left:0;"></canvas>\r\n' \
  '          </div>\r\n' \
  '          <div style="position:absolute;top:4px;right:calc(1.5em + 24px);width:calc(4.5em + 2px);height:calc(1.5em + 6px);overflow:hidden;transform:rotate(-90deg);transform-origin:top right;background-color:rgba(40,45,50,0.5)">\r\n' \
  '            <label for="cursor_zoom" style="font-size:120%;cursor:all-scroll;">&#128270;&#xfe0e;</label>\r\n' \
  '            <input type="range" id="cursor_zoom" min="0" max="4" step="1" value="0" disabled style="position:absolute;top:0;right:0;width:3em;height:1.5em;" oninput="set_param(\'zo\')">\r\n' \
  '          </div>\r\n' \
  '        </td>\r\n' \
  '        <td style="display:table-cell;vertical-align:top;border-left:2px solid dimgray;">\r\n' \
  '          <form autocomplete="off" onsubmit="return(false)" style="overflow:auto;max-height:100vh;padding-left:0.3em;">\r\n' \
  '            <p><label for="cursor_tangle">{#jtilt#}</label></p>\r\n' \
  '            <input type="range" id="cursor_tangle" min="0" max="90" step="any" value="0" disabled oninput="set_param(\'t\')">\r\n' \
  '            <br><span>0</span><span id="cursorv_tangle">0</span><span>90</span>\r\n' + HTML_3D_FORM1_TEMPLATE + \
  '            <p><label for="cursor_zfact">{#jzscale#}</label></p>\r\n' \
  '            <input type="range" id="cursor_zfact" min="1" max="1" step="any" value="1" disabled oninput="set_param(\'zs\')">\r\n' \
  '            <br><span>{#jzscaleiso#}</span><span id="cursorv_zfact"></span><span>{#jzscalemax#}</span>\r\n' + HTML_3D_FORM2_TEMPLATE + \
  '            <input type="radio" id="radio_dimd" name="dimming" checked disabled onclick="toggle_dimming(2)"><label for="radio_dimd">{#jdimmingdeclivity#}</label><br>\r\n' \
  '            <input type="radio" id="radio_dims" name="dimming" disabled onclick="toggle_dimming(3)"><label for="radio_dims">{#jdimmingshadow#}</label>\r\n' + HTML_3D_FORM3_TEMPLATE + \
  '          </form>\r\n' \
  '        </td>\r\n' \
  '      </tbody>\r\n' \
  '    </table>\r\n' \
  '    <script>\r\n' + HTML_3D_GLOBALVARS_TEMPLATE + \
  '      var gl_attributes = new Map([["tvposition", ["vec4", 3]], ["tvnormal", ["vec3", 3]], ["lvposition1", ["vec4", 3, 24, 0, 1]], ["lvposition2", ["vec4", 3, 24, 12, 1]], ["lvoffset", ["vec2", 2]]]);\r\n' \
  '      var gl_static_uniforms = new Map([["zfactmax", "float"], ["mpos", "vec4"], ["mtex", "sampler2D"], ["trtex", "sampler2D"], ["dtex", "sampler2DShadow"]]);\r\n' \
  '      var gl_dynamic_uniforms = new Map([["vmatrix", "mat4"], ["lmatrix", "mat4"], ["ldirection", "vec3"], ["dmode", "int"], ["pmode", "int"], ["ltype", "int"], ["hwidth", "float"]]);\r\n' \
  '      var zfact = 1;\r\n' \
  '      var r_dimd = document.getElementById("radio_dimd");\r\n' \
  '      var c_zfact = document.getElementById("cursor_zfact");\r\n' \
  '      var c_zoom = document.getElementById("cursor_zoom");\r\n' \
  '      var lvposition1 = null;\r\n' \
  '      var lvposition2 = null;\r\n' \
  '      var lvoffset = null;\r\n' \
  '      var ltype = null;\r\n' \
  '      var hwidth = null;;\r\n' \
  '      var ldirection = null;\r\n' \
  '      var zoom = 1;\r\n' \
  '      const ssampling = 2;\r\n' \
  '      const c_msize = Math.min(4096, max_size);\r\n' \
  '      const m_size = Math.min(2048, max_size);\r\n' \
  '      const tr_size = Math.min(2048, max_size);\r\n' \
  '      const d_size = Math.min(2048, max_size);\r\n' \
  '      function set_param(p, v=null) {\r\n' \
  '        if (p == "zs") {\r\n' \
  '          if (v != null) {c_zfact.value = v.toString();}\r\n' \
  '          zfact = parseFloat(c_zfact.value);\r\n' \
  '          cv_tangle.innerHTML = Math.round(90 - 180 / Math.PI * Math.atan(stangle / ctangle * zfact)).toString();\r\n' \
  '          let angle = Math.atan(slt0angle / clt0angle / zfact);\r\n' \
  '          cltangle = Math.cos(angle);\r\n' \
  '          sltangle = Math.sin(angle);\r\n' \
  '        } else if (p == "zo") {\r\n' \
  '          if (v != null) {c_zoom.value = (v<=2?((v-1)*2):v).toString();}\r\n' \
  '          zoom = parseFloat(c_zoom.value);\r\n' \
  '          zoom = zoom<=1?(1+zoom/2):zoom;\r\n' \
  '          if (v == null) {canvas_resize();}\r\n' \
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
  '              if (dmode == 2) {lmatrix = null;}\r\n' \
  '              break;\r\n' \
  '            case "lt":\r\n' \
  '              if (v != null) {c_ltangle.value = v.toString();}\r\n' \
  '              angle0 = (parseFloat(c_ltangle.value) - 90) * Math.PI / 180;\r\n' \
  '              clt0angle = Math.cos(angle0);\r\n' \
  '              slt0angle = Math.sin(angle0);\r\n' \
  '              angle = Math.atan(slt0angle / clt0angle / zfact);\r\n' \
  '              lmatrix = null;\r\n' \
  '              break;\r\n' \
  '            case "lr":\r\n' \
  '              if (v != null) {c_lrangle.value = v.toString();}\r\n' \
  '              angle = - parseFloat(c_lrangle.value) * Math.PI / 180;\r\n' \
  '              lmatrix = null;\r\n' \
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
  '        }\r\n' \
  '        if (v == null) {canvas_redraw();}\r\n' \
  '      }\r\n' \
  '      var clt0angle = null;\r\n' \
  '      var slt0angle = null;\r\n' \
  '      set_param("t", 30);\r\n' \
  '      set_param("r", 0);\r\n' \
  '      set_param("lt", 35);\r\n' \
  '      set_param("lr", 315);\r\n' \
  '      set_param("zs", 1);\r\n' \
  '      set_param("zo", 1);\r\n##DECLARATIONS##\r\n' + HTML_3D_MAT_TEMPLATE + \
  '      function canvas_resize() {\r\n' \
  '        let cpn = canvas.parentNode;\r\n' \
  '        let size = Math.floor(Math.min(cpn.offsetWidth, cpn.offsetHeight) * zoom);\r\n' \
  '        canvas.style.width = size.toString() + "px";\r\n' \
  '        canvas.style.height = size.toString() + "px";\r\n' \
  '        hwidth = 2.5 / size;\r\n' \
  '        size = size * Math.max(Math.floor(Math.min(c_msize / size, ssampling)), 1.0);\r\n' \
  '        canvas.setAttribute("width", size.toString());\r\n' \
  '        canvas.setAttribute("height", size.toString());\r\n' \
  '        gl.viewport(0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight);\r\n' \
  '        cpn.scrollTo((cpn.scrollWidth - cpn.clientWidth) / 2, (cpn.scrollHeight * (1 + (1 - zfact / zfactmax) * stangle / 1.733) - cpn.clientHeight) / 2);\r\n' \
  '      }\r\n' + HTML_3D_UTIL_TEMPLATE + \
  '      function canvas_init() {\r\n' \
  '        gl.enable(gl.DEPTH_TEST);\r\n' \
  '        canvas_resize();\r\n' \
  '        let vertex_tcshader_s = `#version 300 es\r\n' \
  '          in vec4 tvposition;\r\n' \
  '          in vec3 tvnormal;\r\n' \
  '          uniform float zfactmax;\r\n' \
  '          uniform mat4 vmatrix;\r\n' \
  '          uniform mat4 lmatrix;\r\n' \
  '          uniform vec3 ldirection;\r\n' \
  '          uniform int pmode;\r\n' \
  '          uniform int dmode;\r\n' \
  '          out vec2 pcoord;\r\n' \
  '          out float dim;\r\n' \
  '          out vec4 lposition;\r\n' \
  '          out float cinc;\r\n' \
  '          out float isov;\r\n' \
  '          void main() {\r\n' \
  '            float nz = zfactmax * (tvposition.z + 1.0) - 1.0;\r\n' \
  '            gl_Position = vmatrix * tvposition;\r\n' \
  '            pcoord = (tvposition.xy + 1.0) / 2.0;\r\n' \
  '            dim = dmode == 1 ? pow(0.5 * nz + 0.5, 0.7) : 0.7;\r\n' \
  '            lposition = dmode >= 2 ? lmatrix * tvposition : vec4(vec3(0), 1);\r\n' \
  '            cinc = dmode >= 2 ? dot(tvnormal, ldirection) : 0.0;\r\n' \
  '            isov = pmode == 0 ? pcoord.y * 100.0 : (1.0 + nz) * 25.0;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let vertex_ttshader_s = `#version 300 es\r\n' \
  '          in vec4 tvposition;\r\n' \
  '          in vec3 tvnormal;\r\n' \
  '          uniform float zfactmax;\r\n' \
  '          uniform mat4 vmatrix;\r\n' \
  '          uniform mat4 lmatrix;\r\n' \
  '          uniform vec3 ldirection;\r\n' \
  '          uniform int dmode;\r\n' \
  '          uniform vec4 mpos;\r\n' \
  '          out vec4 pcoord;\r\n' \
  '          out float dim;\r\n' \
  '          out vec4 lposition;\r\n' \
  '          out float cinc;\r\n' \
  '          void main() {\r\n' \
  '            gl_Position = vmatrix * tvposition;\r\n' \
  '            pcoord = vec4(vec2(0.5), mpos.st) * vec4(tvposition.xy, tvposition.xy) + vec4(vec2(0.5), mpos.pq);\r\n' \
  '            dim = dmode == 1 ? pow(0.5 * zfactmax * (tvposition.z + 1.0), 0.7) : 1.0;\r\n' \
  '            lposition = dmode >= 2 ? lmatrix * tvposition : vec4(vec3(0), 1);\r\n' \
  '            cinc = dmode >= 2 ? dot(tvnormal, ldirection) : 0.0;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let vertex_lshader_s = `#version 300 es\r\n' \
  '          in vec4 lvposition1;\r\n' \
  '          in vec4 lvposition2;\r\n' \
  '          in vec2 lvoffset;\r\n' \
  '          uniform mat4 vmatrix;\r\n' \
  '          uniform int ltype;\r\n' \
  '          uniform float hwidth;\\r\n' \
  '          out vec4 color;\r\n' \
  '          void main() {\r\n' \
  '            vec4 lpos1 = vmatrix * lvposition1;\r\n' \
  '            vec4 lpos2 = vmatrix * lvposition2;\r\n' \
  '            gl_Position = gl_InstanceID < ltype * 5 ? vec4(2) : (gl_VertexID <= 2 ? lpos1 : lpos2) + vec4(mat2(lvoffset.s, -lvoffset.t, lvoffset.t, lvoffset.s) * normalize(lpos2.xy - lpos1.xy) * hwidth, 0, 0);\r\n' \
  '            color = ltype == 0 ? vec4(vec3(0.35 * (gl_VertexID <= 2 ? lvposition1.z : lvposition2.z) + 0.65), 1) : vec4(1, 1, 0, 1);\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let vertex_sshader_s = `#version 300 es\r\n' \
  '          in vec4 tvposition;\r\n' \
  '          uniform mat4 lmatrix;\r\n' \
  '          void main() {\r\n' \
  '            gl_Position = lmatrix * tvposition;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let fragment_cshader_s = `#version 300 es\r\n' \
  '          precision highp float;\r\n' \
  '          precision highp int;\r\n' \
  '          precision highp sampler2D;\r\n' \
  '          precision highp sampler2DShadow;\r\n' \
  '          in vec2 pcoord;\r\n' \
  '          in float dim;\r\n' \
  '          in vec4 lposition;\r\n' \
  '          in float cinc;\r\n' \
  '          in float isov;\r\n' \
  '          uniform sampler2D trtex;\r\n' \
  '          uniform sampler2DShadow dtex;\r\n' \
  '          uniform int dmode;\r\n' \
  '          out vec4 pcolor;\r\n' \
  '          void main() {\r\n' \
  '            float color = fract(isov) <= 0.15 ? 0.0 : 1.0;\r\n' \
  '            vec3 pos = (lposition.xyz / lposition.w + vec3(1.0, 1.0, 0.996 + 0.003 * abs(cinc))) / 2.0;\r\n' \
  '            float pdim = dmode < 2 ? dim : dmode == 2 ? mix(0.7 + 0.3 * clamp(mix(1.5, 4.0, cinc <= 0.57) * (cinc - 0.57) + 0.8, 0.0, 1.0), 0.3, gl_FrontFacing) : ((cinc <= 0.0) ^^ gl_FrontFacing) ? 0.2 : mix(0.2 , 0.2 + 0.8 * abs(cinc), texture(dtex, pos));\r\n' \
  '            pcolor = gl_FrontFacing ? mix(vec4(0, 0, pdim, 1), vec4(pdim * vec3(0.47, 0.42, 0.35), 1), color) : mix(mix(vec4(0, 0, pdim, 1), vec4(pdim * vec3(0.82, 1, 0.74), 1), color), vec4(pdim, 0, 0, 1), texture(trtex, pcoord).r);\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let fragment_tshader_s = `#version 300 es\r\n' \
  '          precision highp float;\r\n' \
  '          precision highp int;\r\n' \
  '          precision highp sampler2D;\r\n' \
  '          precision highp sampler2DShadow;\r\n' \
  '          in vec4 pcoord;\r\n' \
  '          in float dim;\r\n' \
  '          in vec4 lposition;\r\n' \
  '          in float cinc;\r\n' \
  '          uniform sampler2D mtex;\r\n' \
  '          uniform sampler2D trtex;\r\n' \
  '          uniform sampler2DShadow dtex;\r\n' \
  '          uniform int dmode;\r\n' \
  '          out vec4 pcolor;\r\n' \
  '          void main() {\r\n' \
  '            vec3 pos = (lposition.xyz / lposition.w + vec3(1.0, 1.0, 0.996 + 0.003 * abs(cinc))) / 2.0;\r\n' \
  '            float pdim = dmode < 2 ? dim : dmode == 2 ? mix(0.7 + 0.3 * clamp(mix(1.5, 4.0, cinc <= 0.57) * (cinc - 0.57) + 0.8, 0.0, 1.0), 0.3, gl_FrontFacing) : ((cinc <= 0.0) ^^ gl_FrontFacing) ? 0.2 : mix(0.2 , 0.2 + 0.8 * abs(cinc), texture(dtex, pos));\r\n' \
  '            pcolor = gl_FrontFacing ? vec4(pdim * vec3(0.47, 0.42, 0.35), 1) : mix(texture(mtex, pcoord.pq) * vec4(vec3(pdim), 1.0), vec4(pdim, 0, 0, 1), texture(trtex, pcoord.st).r);\r\n' \
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
  '          void main() {\r\n' \
  '          }\r\n' \
  '        `;\r\n' + HTML_3D_MAP_TEMPLATE + \
  '        function create_track() {\r\n' \
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
  '          let ctx = cnv2d.getContext("2d", {alpha: false});\r\n' \
  '          cnv2d.height = tr_size;\r\n' \
  '          cnv2d.width = tr_size;\r\n' \
  '          ctx.strokeStyle = "red";\r\n' \
  '          ctx.lineWidth = Math.max(1, tr_size / 256);\r\n' \
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
  '                py = trpositions[s][ind + 1];\r\n' \
  '                ctx.beginPath();\r\n' \
  '                ctx.arc(tr_size * (px + 1) / 2, tr_size * (py + 1) / 2, 10 * tr_size / 2048, 0, 2 * Math.PI);\r\n' \
  '                ctx.stroke()\r\n' \
  '                ctx.fill();\r\n' \
  '                ctx.beginPath();\r\n' \
  '                move_to(px, py, false);\r\n' \
  '                ind += 2;\r\n' \
  '              } else {\r\n' \
  '                tdx = trpositions[s][ind] - px;\r\n' \
  '                tdy = trpositions[s][ind + 1] - py;\r\n' \
  '                td = Math.sqrt(tdx * tdx + tdy * tdy);\r\n' \
  '                if (td > 0) {\r\n' \
  '                  tx = tdx / td;\r\n' \
  '                  ty = tdy / td;\r\n' \
  '                  dist += td;\r\n' \
  '                }\r\n' \
  '                if (dist < ar_d) {\r\n' \
  '                  px = trpositions[s][ind];\r\n' \
  '                  py = trpositions[s][ind + 1];\r\n' \
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
  '                  py = trpositions[s][ind + 1] - (dist - ar_d) * ty;\r\n' \
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
  '          tr_texture = texture_load(gl.TEXTURE1, cnv2d, false);\r\n' \
  '        }\r\n' \
  '        program_create("tcprogram", vertex_tcshader_s, fragment_cshader_s);\r\n' \
  '        program_create("ttprogram", vertex_ttshader_s, fragment_tshader_s);\r\n' \
  '        program_create("lprogram", vertex_lshader_s, fragment_lshader_s);\r\n' \
  '        program_create("sprogram", vertex_sshader_s, fragment_sshader_s);\r\n' \
  '        texture_load(gl.TEXTURE0, [0, 127, 0]);\r\n' \
  '        texture_load(gl.TEXTURE1, [0], false);\r\n' \
  '        create_track();\r\n' \
  '        create_map();\r\n' \
  '        tvposition = buffer_load(vpositions);\r\n' \
  '        tvnormal = buffer_load(vnormals);\r\n' \
  '        lvposition1 = buffer_load(new Float32Array([\r\n' \
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
  '        ]));\r\n' \
  '        lvposition2 = lvposition1;\r\n' \
  '        lvoffset = buffer_load(new Float32Array([\r\n' \
  '          0.5, 0,\r\n' \
  '          0, -1,\r\n' \
  '          0, 1,\r\n' \
  '          0, -1,\r\n' \
  '          0, 1,\r\n' \
  '          0.5, 0\r\n' \
  '        ]));\r\n' \
  '        for (let n of gl_programs.keys()) {\r\n' \
  '          program_use(n);\r\n' \
  '          program_attributes();\r\n' \
  '          program_uniforms("static");\r\n' \
  '        }\r\n' \
  '        sfrbuf = gl.createFramebuffer();\r\n' \
  '        gl.bindFramebuffer(gl.FRAMEBUFFER, sfrbuf);\r\n' \
  '        d_texture = texture_attach(gl.TEXTURE2);\r\n' \
  '        gl.bindFramebuffer(gl.FRAMEBUFFER, null);\r\n' \
  '      }\r\n' \
  '      function canvas_redraw() {\r\n' \
  '        if (! lmatrix) {\r\n' \
  '          lmatrix = mat4_zscale(1);\r\n' \
  '          ldirection = new Float32Array([0, 0, 0]);\r\n' \
  '          if (dmode >= 2) {\r\n' \
  '            mat4_mult(mat4_scale(1.733), lmatrix);\r\n' \
  '            if (dmode == 2) {mat4_mult(mat4_rotation(crangle, srangle), lmatrix);}\r\n' \
  '            mat4_mult(mat4_rotation(clrangle, slrangle), lmatrix);\r\n' \
  '            mat4_mult(mat4_tilt(clt0angle, slt0angle), lmatrix);\r\n' \
  '            ldirection.set([-lmatrix[8], -lmatrix[9], -lmatrix[10]]);\r\n' \
  '            if (dmode == 2) {\r\n' \
  '              ylmag = 1;\r\n' \
  '            } else {\r\n' \
  '              ylmag = 1.732 / (1.415 * clt0angle - slt0angle / zfactmax);\r\n' \
  '              mat4_mult(mat4_yscale(ylmag, 1.415 * clt0angle - slt0angle), lmatrix);\r\n' \
  '              gl.bindFramebuffer(gl.FRAMEBUFFER, sfrbuf);\r\n' \
  '              gl.viewport(0, 0, d_size, d_size);\r\n' \
  '              gl.clearColor(0, 0, 0, 0);\r\n' \
  '              gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);\r\n' \
  '              program_use("sprogram");\r\n' \
  '              program_uniforms();\r\n' \
  '              gl.drawArrays(gl.TRIANGLE_STRIP, 0, vpositions.length / 3);\r\n' \
  '              gl.bindFramebuffer(gl.FRAMEBUFFER, null);\r\n' \
  '              gl.viewport(0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight);\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        gl.clearColor(0, 0, 0, 0);\r\n' \
  '        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);\r\n' \
  '        program_use(fillmode<2?"tcprogram":"ttprogram");\r\n' \
  '        pmode = fillmode==1?1:0;\r\n' \
  '        vmatrix = mat4_zscale(zfact);\r\n' \
  '        mat4_mult(mat4_scale(1.733), vmatrix);\r\n' \
  '        mat4_mult(mat4_rotation(crangle, srangle), vmatrix);\r\n' \
  '        mat4_mult(mat4_tilt(ctangle, stangle), vmatrix);\r\n' \
  '        program_uniforms();\r\n' \
  '        gl.drawArrays(gl.TRIANGLE_STRIP, 0, vpositions.length / 3);\r\n' \
  '        program_use("lprogram");\r\n' \
  '        vmatrix = mat4_zscale(1);\r\n' \
  '        mat4_mult(mat4_scale(1.733), vmatrix);\r\n' \
  '        mat4_mult(mat4_rotation(crangle, srangle), vmatrix);\r\n' \
  '        mat4_mult(mat4_tilt(ctangle, stangle), vmatrix);\r\n' \
  '        ltype = 0;\r\n' \
  '        program_uniforms();\r\n' \
  '        gl.drawArraysInstanced(gl.TRIANGLE_STRIP, 0, 6, 5);\r\n' \
  '        if (dmode >= 2) {\r\n' \
  '          ltype = 1;\r\n' \
  '          vmatrix = mat4_zscale(1);\r\n' \
  '          mat4_mult(mat4_scale(1.733), vmatrix);\r\n' \
  '          mat4_mult(mat4_tilt(clt0angle, -slt0angle), vmatrix);\r\n' \
  '          if (dmode == 3) {mat4_mult(mat4_rotation(crangle, srangle), vmatrix);}\r\n' \
  '          mat4_mult(mat4_rotation(clrangle, -slrangle), vmatrix);\r\n' \
  '          mat4_mult(mat4_tilt(ctangle, stangle), vmatrix);\r\n' \
  '          program_uniforms();\r\n' \
  '          gl.drawArraysInstanced(gl.TRIANGLE_STRIP, 0, 6, 14);\r\n' \
  '        }\r\n' \
  '        if (dmode == 3) {\r\n' \
  '          vmatrix = mat4_zscale(1);\r\n' \
  '          mat4_mult(mat4_scale(1.733), vmatrix);\r\n' \
  '          mat4_mult(mat4_tilt(cltangle, -sltangle), vmatrix);\r\n' \
  '          mat4_mult(mat4_rotation(crangle, srangle), vmatrix);\r\n' \
  '          mat4_mult(mat4_rotation(clrangle, -slrangle), vmatrix);\r\n' \
  '          mat4_mult(mat4_tilt(ctangle, stangle), vmatrix);\r\n' \
  '          program_uniforms();\r\n' \
  '          gl.drawArraysInstanced(gl.TRIANGLE_STRIP, 0, 6, 14);\r\n' \
  '        }\r\n' \
  '      }\r\n' + HTML_3D_ROT_TEMPLATE + HTML_3D_LOAD_TEMPLATE + \
  '          canvas_redraw();\r\n' \
  '          window.onresize = (e) => {canvas_resize(); canvas_redraw();};\r\n' \
  '          c_tangle.disabled = false;\r\n' \
  '          c_rangle.disabled = false;\r\n' \
  '          b_rangle.disabled = false;\r\n' \
  '          if (zfactmax > 1) {\r\n' \
  '            c_zfact.max = zfactmax.toString();\r\n' \
  '            c_zfact.disabled = false;\r\n' \
  '          }\r\n' \
  '          c_zoom.disabled = false;\r\n' \
  '          c_zoom.previousElementSibling.onclick = function () {set_param("zo");}\r\n' \
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
  '      data_load();\r\n' + HTML_3D_TOGGLE_TEMPLATE + \
  '      function toggle_dimming(mode) {\r\n' \
  '        if (mode == dmode) {return;};\r\n' \
  '        if (dmode == 3 && c_lrangle.disabled) {toggle_lrotation();}\r\n' \
  '        dmode = mode;\r\n' \
  '        if (dmode == 3) {\r\n' \
  '          c_ltangle.disabled = false;\r\n' \
  '          c_lrangle.disabled = false;\r\n' \
  '          b_lrangle.disabled = false;\r\n' \
  '          lmatrix = null;\r\n' \
  '        } else {\r\n' \
  '          c_ltangle.disabled = true;\r\n' \
  '          c_lrangle.disabled = true;\r\n' \
  '          b_lrangle.disabled = true;\r\n' \
  '          if (dmode == 2) {\r\n' \
  '            set_param("lt", 35);\r\n' \
  '            set_param("lr", 315);\r\n' \
  '            lmatrix = null;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        canvas_redraw();\r\n' \
  '      }\r\n' \
  '    </script>\r\n' \
  '  </body>\r\n' \
  '</html>'
  HTML_3DP_TEMPLATE = HTML_3DP_TEMPLATE.replace('{', '{{').replace('}', '}}').replace('{{#', '{').replace('#}}', '}').format_map(LSTRINGS['interface']).replace('{{', '{').replace('}}', '}')
  HTML_3DP_DECLARATIONS_TEMPLATE = \
  '      var portmin = ##PORTMIN##;\r\n' \
  '      var portmax = ##PORTMAX##;\r\n' \
  '      var zfactmax = ##ZFACTMAX##;\r\n' \
  '      var mpos = [##MPOS##];\r\n' \
  '      var tminrow = ##TMINROW##;\r\n' \
  '      var tmincol = ##TMINCOL##;\r\n' \
  '      var tmaxrow = ##TMAXROW##;\r\n' \
  '      var tmaxcol = ##TMAXCOL##;'
  HTML_3DS_TEMPLATE = \
  '<!DOCTYPE html>\r\n' \
  '<html lang="fr-FR">\r\n' \
  '  <head>\r\n' \
  '    <meta charset="utf-8">\r\n' \
  '    <title>GPXTweaker 3DViewer Subjective</title>\r\n' + HTML_3D_STYLES_TEMPLATE + \
  '  </head>\r\n' \
  '  <body style="margin:0;background-color:rgb(40,45,50);color:rgb(225,225,225);user-select:none;">\r\n' \
  '    <table>\r\n' \
  '      <colgroup>\r\n' \
  '        <col style="width:calc(100vw - 14em);">\r\n' \
  '        <col style="width:14em;">\r\n' \
  '      </colgroup>\r\n' \
  '      <tbody>\r\n' \
  '        <tr style="display:table-row;">\r\n' \
  '        <td style="display:table-cell;position:relative;vertical-align:top;height:100vh;overflow:hidden;user-select:none;" oncontextmenu="if (event.target.id == \'mini_map\') {event.ctrlKey?toggle_reversegeocodingswitch():toggle_infos();}; event.preventDefault();event.stopPropagation();" onwheel="mouse_wheel(event)">\r\n' \
  '          <canvas id="canvas" width="100" height="100" style="position:absolute;top:0;left:0;" tabindex="0" onkeydown="process_key(event)" ondblclick="process_key({key:\'enter\'})" onmousedown="mouse_down(event)" oncontextmenu="show_infos?update_infos(event):event.preventDefault()"></canvas>\r\n' \
  '          <div id="panel_infos" style="display:none;position:absolute;top:5px;left:5px;width:calc(100vw - 10vh - 18em);height:3em;font-size:90%;color:black;background-color:rgba(210,210,210,0.85);">\r\n' \
  '            <form autocomplete="off" onsubmit="return(false)" style="position:relative;overflow:hidden;height:3em;">\r\n' \
  '              <label for="eye_info" style="top:2px;" onclick="event.altKey?complete_infos(event):update_waypoint(event)">&#128065;</label><input type="text" id="eye_info" name="eye_info" readOnly style="top:2px;"><br>\r\n' \
  '              <label for="target_info" style="bottom:2px;" onclick="event.altKey?complete_infos(event):update_waypoint(event)">&target;</label><input type="text" id="target_info" name="target_info" readOnly style="bottom:2px;">\r\n' \
  '            </form>\r\n' \
  '          </div>\r\n' \
  '          <svg id="target_mark" viewbox="-1 -1 2 2" pointer-events="none" stroke-width="1" style="display:none;position:absolute;top:0%;left:0%;width:2vh;height:2vh;" fill="none">\r\n' \
  '            <circle cx="0" cy="0" r="0.5" vector-effect="non-scaling-stroke" stroke-width="3" stroke="lightgray"/>\r\n' \
  '            <circle cx="0" cy="0" r="0.5" vector-effect="non-scaling-stroke" stroke-width="1.5" stroke="black""/>\r\n' \
  '            <line x1="-0.9" y1="0" x2="0.9" y2 ="0" vector-effect="non-scaling-stroke" stroke-width="3" stroke="lightgray"/>\r\n' \
  '            <line x1="-0.9" y1="0" x2="0.9" y2 ="0" vector-effect="non-scaling-stroke" stroke-width="1.5" stroke="black"/>\r\n' \
  '            <line x1="0" y1="-0.9" x2="0" y2 ="0.9" vector-effect="non-scaling-stroke" stroke-width="3" stroke="lightgray"/>\r\n' \
  '            <line x1="0" y1="-0.9" x2="0" y2 ="0.9" vector-effect="non-scaling-stroke" stroke-width="1.5" stroke="black"/>\r\n' \
  '          </svg>\r\n' \
  '          <svg id="mini_map" viewbox="-1 -1 2 2" stroke="red" fill="red" stroke-width="1" stroke-linecap="round" stroke-linejoin="roundstyle" style="position:absolute;top:2px;right:2px;width:10vh;height:10vh;cursor:zoom-in;" onclick="toggle_minimap_magnification()">\r\n' \
  '            <path id="track" pointer-events="none" vector-effect="non-scaling-stroke" fill="none" d="M0 0" />\r\n' \
  '            <text pointer-events="none" dy="0.25em" style="font-size:2.5%;word-spacing:1.5em;" >\r\n' \
  '              <textPath pointer-events="none" href="#track" stroke="none">&rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; &rsaquo; </textPath>\r\n' \
  '            </text>\r\n' \
  '            <path pointer-events="none" id="eye" vector-effect="non-scaling-stroke" stroke="slategray" fill="darkslategray" fill-opacity="1" transform="scale(1) rotate(0) translate(0)" d="M0 -0.2 l-0.15 0.4 l0.15 -0.1 l0.15 0.1 l-0.15 -0.4"/>\r\n' \
  '          <title>{#jminimap#}</title>\r\n' \
  '          </svg>\r\n' \
  '          <div id="panel_rg" style="display:none;position:absolute;top:10vh;right:2px;width:11.7em;height:1.9em;font-size:80%;">\r\n' \
  '            <select id="select_rg" name="select_rg" autocomplete="off" style="width:11.5em;height:1.7em;background-color:lightgray;" onchange="rgset=this.selectedIndex">##RGSETS##</select>\r\n' \
  '          </div>\r\n' \
  '        </td>\r\n' \
  '        <td style="display:table-cell;vertical-align:top;border-left:2px solid dimgray;">\r\n' \
  '          <div title="{#jhelp3d#}" style="position:absolute;z-index:10;right:20px;top:1px;width:1.4em;height:1.2em;display:inline-block;text-align:center;background-color:lightgray;color:black;font-weight:bold;cursor:help;">?</div>\r\n' \
  '          <form autocomplete="off" onsubmit="return(false)" style="position:relative;overflow:auto;max-height:100vh;padding-left:0.3em;">\r\n' \
  '            <p><label for="cursor_tangle">{#jtilt#}</label></p>\r\n' \
  '            <input type="range" id="cursor_tangle" min="-90" max="90" step="any" value="0" disabled oninput="set_param(\'t\')">\r\n' \
  '            <br><span>-90</span><span id="cursorv_tangle">0</span><span>90</span>\r\n' + HTML_3D_FORM1_TEMPLATE + \
  '            <p><label for="cursor_pace">{#jpace#}</label><label for="checkbox_pace" style="position:absolute;left:8.15em;padding-top:0.4em;font-size:130%;">&orarr;</label></p>\r\n' \
  '            <input type="range" id="cursor_pace" min="0" max="0" step="1" value="0" disabled oninput="set_param(\'p\')">&nbsp;&nbsp;<input type="checkbox" id="checkbox_pace" checked disabled onclick="toggle_auto_rotation()">\r\n' \
  '            <br><span>0</span><span id="cursorv_pace">0</span><span>0</span>\r\n' + HTML_3D_FORM2_TEMPLATE + \
  '            <input type="radio" id="radio_dims" name="dimming" checked disabled onclick="toggle_dimming(2)"><label for="radio_dims">{#jdimmingshadow#}</label>\r\n' + HTML_3D_FORM3_TEMPLATE + \
  '            <br><br>\r\n' \
  '            <p><label for="cursor_vfov">{#jvfov#}</label></p>\r\n' \
  '            <input type="range" id="cursor_vfov" min="10" max="150" step="any" value="55" disabled oninput="set_param(\'f\')">\r\n' \
  '            <br><span>10</span><span id="cursorv_vfov">55</span><span>150</span>\r\n' \
  '            <br><br>\r\n' \
  '            <p><label for="cursor_height">{#jheight#}</label></p>\r\n' \
  '            <input type="range" id="cursor_height" min="0" max="100" step="any" value="4" disabled oninput="set_param(\'h\')">\r\n' \
  '            <br><span>0.2</span><span id="cursorv_height">2</span><span>1000</span>\r\n' \
  '          </form>\r\n' \
  '        </td>\r\n' \
  '      </tbody>\r\n' \
  '    </table>\r\n' \
  '    <script>\r\n' + HTML_3D_GLOBALVARS_TEMPLATE + \
  '      var gl_attributes = new Map([["tvposition", ["vec4", 3]], ["tvnormal", ["vec3", 3]], ["rvposition", ["vec3", 3]]]);\r\n' \
  '      var gl_static_uniforms = new Map([["zfactmax", "float"], ["scale", "float"], ["radius", "float"], ["mpos", "vec4"], ["mtex", "sampler2D"], ["trpos", "vec4"], ["trtex", "sampler2D"], ["dtex", "sampler2DShadow"]]);\r\n' \
  '      var gl_dynamic_uniforms = new Map([["eposition", "vec2"], ["vmatrix", "mat4"], ["lmatrix", "mat4"], ["ldirection", "vec3"], ["dmode", "int"], ["pmode", "int"]]);\r\n' \
  '      var track = document.getElementById("track");\r\n' \
  '      var eye = document.getElementById("eye");\r\n' \
  '      var c_pace = document.getElementById("cursor_pace");\r\n' \
  '      var cv_pace = document.getElementById("cursorv_pace");\r\n' \
  '      var cb_pace = document.getElementById("checkbox_pace");\r\n' \
  '      var c_vfov = document.getElementById("cursor_vfov");\r\n' \
  '      var cv_vfov = document.getElementById("cursorv_vfov");\r\n' \
  '      var c_height = document.getElementById("cursor_height");\r\n' \
  '      var cv_height = document.getElementById("cursorv_height");\r\n' \
  '      var p_infos = document.getElementById("panel_infos");\r\n' \
  '      var e_info = document.getElementById("eye_info");\r\n' \
  '      var t_info = document.getElementById("target_info");\r\n' \
  '      var t_mark = document.getElementById("target_mark");\r\n' \
  '      var p_rg = document.getElementById("panel_rg");\r\n' \
  '      var s_rg = document.getElementById("select_rg");\r\n' \
  '      var minimap = document.getElementById("mini_map");\r\n' \
  '      var trpaces = null;\r\n' \
  '      var trscale = null;\r\n' \
  '      var rpositions = null;\r\n' \
  '      var rvposition = null;\r\n' \
  '      var eposition = null;\r\n' \
  '      const ssampling = 2;\r\n' \
  '      const m_size = Math.min(11008, max_size);\r\n' \
  '      const tr_size = Math.min(8192, max_size / 2);\r\n' \
  '      const d_size = max_size;\r\n' \
  '      const rnt = 36;\r\n' \
  '      var p_texture = null;\r\n' \
  '      var pd_texture = null;\r\n' \
  '      var pfrbuf = null;\r\n' \
  '      var predraw = false;\r\n' \
  '      var mzoom = 1;\r\n' \
  '      var show_infos = false;\r\n' \
  '      var rgset = (s_rg.options.length > 0)?s_rg.selectedIndex:-1;\r\n' \
  '      var click_r = null;\r\n' \
  '      var click_t = null;\r\n' \
  '      var click_cr = null;\r\n' \
  '      var click_ct = null;\r\n' \
  '      var click_id = 0.0;\r\n' \
  '      function set_param(p, v=null) {\r\n' \
  '        if (p == "p") {\r\n' \
  '          if (v != null) {c_pace.value = v.toString();}\r\n' \
  '          cv_pace.innerHTML = c_pace.value;\r\n' \
  '          pace = parseInt(c_pace.value);\r\n' \
  '          eposition.set([trpaces[pace][0], trpaces[pace][1]]);\r\n' \
  '          if (cb_pace.checked) {\r\n' \
  '            if (c_rangle.disabled) {toggle_rotation();}\r\n' \
  '            set_param("r", (450 - trpaces[pace][3] / Math.PI * 180) % 360);\r\n' \
  '          } else if (eposition != null) {\r\n' \
  '            eye.setAttribute("transform", `translate(${eposition[0]} ${-eposition[1]}) rotate(${parseFloat(c_rangle.value)}) scale(${trscale / mzoom})`);\r\n' \
  '          }\r\n' \
  '          if (show_infos) {update_infos();}\r\n' \
  '        } else if (p == "f") {\r\n' \
  '          if (v != null) {c_vfov.value = v.toString();}\r\n' \
  '          cv_vfov.innerHTML = Math.round(parseFloat(c_vfov.value)).toString();\r\n' \
  '          vfov = 1 / Math.tan(parseFloat(c_vfov.value) / 360 * Math.PI);\r\n' \
  '          if (show_infos) {clear_tinfos(true);}\r\n' \
  '        } else if (p == "h") {\r\n' \
  '          if (v != null) {\r\n' \
  '            c_height.value = (Math.min(v, 10) * 2 + Math.min(Math.max(v - 10, 0), 40) / 2 + Math.min(Math.max(v - 50, 0), 150) / 7.5 + Math.min(Math.max(v - 200, 0), 300) / 15 + Math.max(v - 500, 0) / 25).toString();\r\n' \
  '            cv_height.innerHTML = (v >= 10 ? Math.round(v) : Math.round(v * 10) / 10).toString();\r\n' \
  '            zoff = v / scale;\r\n' \
  '          } else {\r\n' \
  '            let hv = parseFloat(c_height.value);\r\n' \
  '            let height = Math.max(Math.min(hv, 20) / 2, 0.2) + Math.min(Math.max(hv - 20, 0), 20) * 2 + Math.min(Math.max(hv - 40, 0), 20) * 7.5 + Math.min(Math.max(hv - 60, 0), 20) * 15 + Math.max(hv - 80, 0) * 25;\r\n' \
  '            cv_height.innerHTML = (height >= 10 ? Math.round(height) : Math.round(height * 10) / 10).toString();\r\n' \
  '            zoff = height / scale;\r\n' \
  '          }\r\n' \
  '          if (show_infos) {update_infos();}\r\n' \
  '        } else {\r\n' \
  '          let angle = null;\r\n' \
  '          switch (p) {\r\n' \
  '            case "t":\r\n' \
  '              if (v != null) {c_tangle.value = v.toString();}\r\n' \
  '              angle = (90 + parseFloat(c_tangle.value)) * Math.PI / 180;\r\n' \
  '              if (show_infos) {clear_tinfos(true);}\r\n' \
  '              break;\r\n' \
  '            case "r":\r\n' \
  '              if (v != null) {c_rangle.value = v.toString();}\r\n' \
  '              angle =  parseFloat(c_rangle.value) * Math.PI / -180;\r\n' \
  '              if (eposition != null) {eye.setAttribute("transform", `translate(${eposition[0]} ${-eposition[1]}) rotate(${parseFloat(c_rangle.value)}) scale(${trscale / mzoom})`);}\r\n' \
  '              if (show_infos) {clear_tinfos(true);}\r\n' \
  '              break;\r\n' \
  '            case "lt":\r\n' \
  '              if (v != null) {c_ltangle.value = v.toString();}\r\n' \
  '              angle = (parseFloat(c_ltangle.value) - 90) * Math.PI / 180;\r\n' \
  '              lmatrix = null;\r\n' \
  '              break;\r\n' \
  '            case "lr":\r\n' \
  '              if (v != null) {c_lrangle.value = v.toString();}\r\n' \
  '              angle = - parseFloat(c_lrangle.value) * Math.PI / 180;\r\n' \
  '              lmatrix = null;\r\n' \
  '              break;\r\n' \
  '          }\r\n' \
  '          window["c" + p + "angle"] = Math.cos(angle);\r\n' \
  '          window["s" + p + "angle"] = Math.sin(angle);\r\n' \
  '          window["cv_" + p + "angle"].innerHTML = Math.round(parseFloat(window["c_" + p + "angle"].value)).toString();\r\n' \
  '        }\r\n' \
  '        if (v == null) {canvas_redraw();}\r\n' \
  '      }\r\n' \
  '      set_param("t", 0);\r\n' \
  '      set_param("r", 0);\r\n' \
  '      set_param("lt", 25);\r\n' \
  '      set_param("lr", 90);\r\n' \
  '      var pace = 0;\r\n' \
  '      var vfov = null;\r\n' \
  '      set_param("f", 55);\r\n##DECLARATIONS##\r\n' + \
  '      var trpos = new Float32Array(4);\r\n' \
  '      var radius = 6378137 / scale;\r\n' \
  '      var pace_length = 10 / scale;\r\n' \
  '      var zoff = null;\r\n' \
  '      set_param("h", 2);\r\n' + HTML_3D_MAT_TEMPLATE + \
  '      function mat4_translation(xt, yt, zt) {\r\n' \
  '        return new Float32Array([\r\n' \
  '          1, 0, 0, xt,\r\n' \
  '          0, 1, 0, yt,\r\n' \
  '          0, 0, 1, zt,\r\n' \
  '          0, 0, 0, 1\r\n' \
  '        ]);\r\n' \
  '      }\r\n' \
  '      function mat4_perspective() {\r\n' \
  '        return new Float32Array([\r\n' \
  '          vfov / 4 / canvas.clientWidth * canvas.clientHeight, 0, 0, 0,\r\n' \
  '          0, vfov / 4, 0, 0,\r\n' \
  '          0, 0, 1/2, -1,\r\n' \
  '          0, 0, 1/4, 0,\r\n' \
  '        ]);\r\n' \
  '      }\r\n' \
  '      function canvas_resize() {\r\n' \
  '        canvas.setAttribute("width", (canvas.parentNode.offsetWidth * ssampling).toString());\r\n' \
  '        canvas.setAttribute("height", (canvas.parentNode.offsetHeight * ssampling).toString());\r\n' \
  '        canvas.style.width = canvas.parentNode.offsetWidth.toString() + "px";;\r\n' \
  '        canvas.style.height = canvas.parentNode.offsetHeight.toString() + "px";\r\n' \
  '        gl.viewport(0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight);\r\n' \
  '        if (show_infos) {clear_tinfos(true);}\r\n' \
  '        gl.bindBuffer(gl.ARRAY_BUFFER, rvposition);\r\n' \
  '        let rr = canvas.clientHeight / canvas.clientWidth;\r\n' \
  '        let ra = 2 * Math.PI / rnt;\r\n' \
  '        for (let i=0; i<=rnt;i++) {rpositions.set([0.01 * rr * Math.cos(i * ra), 0.01 * Math.sin(i * ra), 0], 3 + 3 * i);}\r\n' \
  '        gl.bufferData(gl.ARRAY_BUFFER, rpositions, gl.DYNAMIC_DRAW);\r\n' \
  '        if (pfrbuf) {\r\n' \
  '          gl.bindFramebuffer(gl.FRAMEBUFFER, pfrbuf);\r\n' \
  '          ptexture_attach(gl.TEXTURE3);\r\n' \
  '          gl.bindFramebuffer(gl.FRAMEBUFFER, null);\r\n' \
  '        }\r\n' \
  '      }\r\n' + HTML_3D_UTIL_TEMPLATE + \
  '      function ptexture_attach(unit) {\r\n' \
  '        gl.activeTexture(unit);\r\n' \
  '        for (let ttype of ["p", "pd"]){\r\n' \
  '          let gl_texture = window[ttype + "_texture"];\r\n' \
  '          if (gl_texture == null) {\r\n' \
  '            gl_texture = gl.createTexture();\r\n' \
  '            window[ttype + "_texture"] = gl_texture;\r\n' \
  '            gl.bindTexture(gl.TEXTURE_2D, gl_texture);\r\n' \
  '            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);\r\n' \
  '            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);\r\n' \
  '            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);\r\n' \
  '            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);\r\n' \
  '          } else {\r\n' \
  '            gl.bindTexture(gl.TEXTURE_2D, gl_texture);\r\n' \
  '          }\r\n' \
  '          gl.texImage2D(gl.TEXTURE_2D, 0, ttype=="p"?gl.RG16I:gl.DEPTH_COMPONENT16, gl.drawingBufferWidth / ssampling, gl.drawingBufferHeight / ssampling, 0, ttype=="p"?gl.RG_INTEGER:gl.DEPTH_COMPONENT, ttype=="p"?gl.SHORT:gl.UNSIGNED_SHORT, null);\r\n' \
  '          gl.framebufferTexture2D(gl.FRAMEBUFFER, ttype!="p"?gl.DEPTH_ATTACHMENT:gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, gl_texture, 0);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function get_pz(px, py) {\r\n' \
  '        let ix = 0;\r\n' \
  '        let iy = 0;\r\n' \
  '        while (ix < lvx - 1 && vpositions[ix * 6] <= px) {ix++;}\r\n' \
  '        while (iy < lvy - 1 && vpositions[(iy * (lvx + 1)) * 6 + 4] <= py) {iy++;}\r\n' \
  '        let cx = (px - vpositions[(ix - 1) * 6]) / (vpositions[ix * 6] - vpositions[(ix - 1) * 6]);\r\n' \
  '        let cy = (py - vpositions[(iy * (lvx + 1)) * 6 + 1]) / (vpositions[(iy * (lvx + 1)) * 6 + 4] - vpositions[(iy * (lvx + 1)) * 6 + 1]);\r\n' \
  '        return cx + cy <= 1 ? (1 - cx - cy) * vpositions[(ix - 1 + iy * (lvx + 1)) * 6 + 2] + cx * vpositions[(ix + iy * (lvx + 1)) * 6 + 2] + cy  * vpositions[(ix - 1 + iy * (lvx + 1)) * 6 + 5] : (1 - cy) * vpositions[(ix + iy * (lvx + 1)) * 6 + 2] + (1 - cx) * vpositions[(ix - 1 + iy * (lvx + 1)) * 6 + 5] + (cx + cy - 1) * vpositions[(ix + iy * (lvx + 1)) * 6 + 5];\r\n' \
  '      }\r\n' \
  '      function canvas_init() {\r\n' \
  '        gl.enable(gl.DEPTH_TEST);\r\n' \
  '        rpositions = new Float32Array(6 + 3 * rnt);\r\n' \
  '        rpositions.set([0, 0, 0]);\r\n' \
  '        rvposition = gl.createBuffer();\r\n' \
  '        canvas_resize();\r\n' \
  '        let vertex_tcshader_s = `#version 300 es\r\n' \
  '          in vec4 tvposition;\r\n' \
  '          in vec3 tvnormal;\r\n' \
  '          uniform float zfactmax;\r\n' \
  '          uniform float scale;\r\n' \
  '          uniform vec2 eposition;\r\n' \
  '          uniform float radius;\r\n' \
  '          uniform mat4 vmatrix;\r\n' \
  '          uniform mat4 lmatrix;\r\n' \
  '          uniform vec3 ldirection;\r\n' \
  '          uniform int pmode;\r\n' \
  '          uniform int dmode;\r\n' \
  '          uniform vec4 trpos;\r\n' \
  '          out vec2 pcoord;\r\n' \
  '          out float dim;\r\n' \
  '          out vec4 lposition;\r\n' \
  '          out float cinc;\r\n' \
  '          out float isov;\r\n' \
  '          void main() {\r\n' \
  '            float zcor = - pow(distance(eposition, tvposition.xy) / radius, 2.0) / 2.0;\r\n' \
  '            gl_Position = vmatrix * (tvposition + vec4(0.0, 0.0, zcor * radius, 0.0));\r\n' \
  '            gl_Position.z *= gl_Position.w;\r\n' \
  '            pcoord = trpos.st * tvposition.xy + trpos.pq;\r\n' \
  '            dim = dmode == 1 ? pow(0.5 * zfactmax * (tvposition.z + 1.0), 0.7) : 0.7;\r\n' \
  '            lposition = dmode == 2 ? lmatrix * tvposition : vec4(vec3(0), 1);\r\n' \
  '            cinc = dmode == 2 ? dot(tvnormal, ldirection) : 0.0;\r\n' \
  '            isov = ((pmode == 0 ? tvposition.y : tvposition.z) + 1.0) * scale / 50.0;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let vertex_ttshader_s = `#version 300 es\r\n' \
  '          in vec4 tvposition;\r\n' \
  '          in vec3 tvnormal;\r\n' \
  '          uniform float zfactmax;\r\n' \
  '          uniform vec2 eposition;\r\n' \
  '          uniform float radius;\r\n' \
  '          uniform mat4 vmatrix;\r\n' \
  '          uniform mat4 lmatrix;\r\n' \
  '          uniform vec3 ldirection;\r\n' \
  '          uniform int dmode;\r\n' \
  '          uniform vec4 trpos;\r\n' \
  '          uniform vec4 mpos;\r\n' \
  '          out vec4 pcoord;\r\n' \
  '          out float dim;\r\n' \
  '          out vec4 lposition;\r\n' \
  '          out float cinc;\r\n' \
  '          void main() {\r\n' \
  '            float zcor = - pow(distance(eposition, tvposition.xy) / radius, 2.0) / 2.0;\r\n' \
  '            gl_Position = vmatrix * (tvposition + vec4(0.0, 0.0, zcor * radius, 0.0));\r\n' \
  '            gl_Position.z *= gl_Position.w;\r\n' \
  '            pcoord = vec4(trpos.st, mpos.st) * vec4(tvposition.xy, tvposition.xy) + vec4(trpos.pq, mpos.pq);\r\n' \
  '            dim = dmode == 1 ? pow(0.5 * zfactmax * (tvposition.z + 1.0), 0.7) : 1.0;\r\n' \
  '            lposition = dmode == 2 ? lmatrix * tvposition : vec4(vec3(0), 1);\r\n' \
  '            cinc = dmode == 2 ? dot(tvnormal, ldirection) : 0.0;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let vertex_sshader_s = `#version 300 es\r\n' \
  '          in vec4 tvposition;\r\n' \
  '          uniform mat4 lmatrix;\r\n' \
  '          void main() {\r\n' \
  '            gl_Position = lmatrix * tvposition;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let vertex_rshader_s = `#version 300 es\r\n' \
  '          in vec3 rvposition;\r\n' \
  '          uniform mat4 vmatrix;\r\n' \
  '          void main() {\r\n' \
  '            gl_Position = vmatrix * vec4(0, 0, 1, 1) + vec4(rvposition, 0);\r\n' \
  '            gl_Position.z *= gl_Position.w;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let vertex_pshader_s = `#version 300 es\r\n' \
  '          in vec4 tvposition;\r\n' \
  '          uniform vec2 eposition;\r\n' \
  '          uniform float radius;\r\n' \
  '          uniform mat4 vmatrix;\r\n' \
  '          out vec2 pcoord;\r\n' \
  '          void main() {\r\n' \
  '            float zcor = - pow(distance(eposition, tvposition.xy) / radius, 2.0) / 2.0;\r\n' \
  '            gl_Position = vmatrix * (tvposition + vec4(0.0, 0.0, zcor * (tvposition.z + radius), 0.0));\r\n' \
  '            gl_Position.z *= gl_Position.w;\r\n' \
  '            pcoord = tvposition.xy;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let fragment_cshader_s = `#version 300 es\r\n' \
  '          precision highp float;\r\n' \
  '          precision highp int;\r\n' \
  '          precision highp sampler2D;\r\n' \
  '          precision highp sampler2DShadow;\r\n' \
  '          in vec2 pcoord;\r\n' \
  '          in float dim;\r\n' \
  '          in vec4 lposition;\r\n' \
  '          in float cinc;\r\n' \
  '          in float isov;\r\n' \
  '          uniform sampler2D trtex;\r\n' \
  '          uniform sampler2DShadow dtex;\r\n' \
  '          uniform int dmode;\r\n' \
  '          out vec4 pcolor;\r\n' \
  '          void main() {\r\n' \
  '            float color = fract(isov) <= 0.15 ? 0.0 : 1.0;\r\n' \
  '            vec3 pos = (lposition.xyz / lposition.w + vec3(1.0, 1.0, 0.996 + 0.003 * cinc)) / 2.0;\r\n' \
  '            float pdim = dmode < 2 ? dim : cinc <= 0.0 ? 0.2 : mix(0.2 , 0.2 + 0.8 * cinc, texture(dtex, pos));\r\n' \
  '            pcolor = texture(trtex, pcoord.st).r < 0.3 ? mix(vec4(0, 0, pdim, 1), vec4(pdim * vec3(0.82, 1, 0.74), 1), color) : vec4(1, 0, 0, 1);\r\n' \
  '            gl_FragDepth = 1.0 / gl_FragCoord.w;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let fragment_tshader_s = `#version 300 es\r\n' \
  '          precision highp float;\r\n' \
  '          precision highp int;\r\n' \
  '          precision highp sampler2D;\r\n' \
  '          precision highp sampler2DShadow;\r\n' \
  '          in vec4 pcoord;\r\n' \
  '          in float dim;\r\n' \
  '          in vec4 lposition;\r\n' \
  '          in float cinc;\r\n' \
  '          uniform sampler2D mtex;\r\n' \
  '          uniform sampler2D trtex;\r\n' \
  '          uniform sampler2DShadow dtex;\r\n' \
  '          uniform int dmode;\r\n' \
  '          out vec4 pcolor;\r\n' \
  '          void main() {\r\n' \
  '            vec3 pos = (lposition.xyz / lposition.w + vec3(1.0, 1.0, 0.996 + 0.003 * cinc)) / 2.0;\r\n' \
  '            float pdim = dmode < 2 ? dim : cinc <= 0.0 ? 0.2 : mix(0.2 , 0.2 + 0.8 * cinc, texture(dtex, pos));\r\n' \
  '            pcolor = texture(trtex, pcoord.st).r < 0.3 ? texture(mtex, pcoord.pq) * vec4(vec3(pdim), 1.0) : vec4(1, 0, 0, 1);\r\n' \
  '            gl_FragDepth = 1.0 / gl_FragCoord.w;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let fragment_sshader_s = `#version 300 es\r\n' \
  '          precision highp float;\r\n' \
  '          void main() {\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '        let fragment_rshader_s = `#version 300 es\r\n' \
  '          precision highp float;\r\n' \
  '          out vec4 pcolor;\r\n' \
  '          void main() {\r\n' \
  '            pcolor = vec4(1, 1, 0, 1);\r\n' \
  '            gl_FragDepth = 1.0;\r\n' \
  '          }\r\n' \
  '        `;\r\n' \
  '       let fragment_pshader_s = `#version 300 es\r\n' \
  '          precision highp float;\r\n' \
  '          precision highp int;\r\n' \
  '          in vec2 pcoord;\r\n' \
  '          out ivec2 pcolor;\r\n' \
  '          void main() {\r\n' \
  '            pcolor = ivec2(round(32767.0 * pcoord));\r\n' \
  '            gl_FragDepth = 1.0 / gl_FragCoord.w;\r\n' \
  '          }\r\n' \
  '        `;\r\n' + HTML_3D_MAP_TEMPLATE + \
  '        function create_track() {\r\n' \
  '          function move_to(x, y, d=true) {\r\n' \
  '            if (d) {\r\n' \
  '              ctx.lineTo(tr_size * (trpos[0] * x + trpos[2]), tr_size * (trpos[1] * y + trpos[3]));\r\n' \
  '            } else {\r\n' \
  '              ctx.moveTo(tr_size * (trpos[0] * x + trpos[2]), tr_size * (trpos[1] * y + trpos[3]));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          let cnv2d = document.createElement("canvas");\r\n' \
  '          let ctx = cnv2d.getContext("2d", {alpha: false});\r\n' \
  '          cnv2d.height = tr_size;\r\n' \
  '          cnv2d.width = tr_size;\r\n' \
  '          ctx.strokeStyle = "red";\r\n' \
  '          let trb = trpositions.reduce(function (p, c) {return c.reduce(function (p, c, i) {return (i%2==0?[Math.min(p[0], c), Math.max(p[1], c), p[2], p[3]]:[p[0], p[1], Math.min(p[2], c), Math.max(p[3], c)])}, p)}, [1, -1, 1, -1]);\r\n' \
  '          trscale = Math.min(2, Math.max(trb[1] - trb[0], trb[3] - trb[2], 0.00001) * 1.3) / 2;\r\n' \
  '          trpos.set([0.5 / trscale, 0.5 / trscale, 0.5 - (trb[0] + trb[1]) / (4 * trscale), 0.5 - (trb[2] + trb[3]) / (4 * trscale)]);\r\n' \
  '          ctx.lineWidth = Math.max(0.5, tr_size / 2 / scale / trscale);\r\n' \
  '          ctx.lineJoin = "round";\r\n' \
  '          ctx.lineCap = "round";\r\n' \
  '          ctx.fillStyle = "red";\r\n' \
  '          trpaces = [];\r\n' \
  '          for (let s=0; s<trpositions.length; s++) {\r\n' \
  '            let ind = 0;\r\n' \
  '            let dr = false;\r\n' \
  '            let dist = 0;\r\n' \
  '            let px = null;\r\n' \
  '            let py = null;\r\n' \
  '            let tx = null;\r\n' \
  '            let ty = null;\r\n' \
  '            let td = null;\r\n' \
  '            let tdx = null;\r\n' \
  '            let tdy = null;\r\n' \
  '            let ptg = false;\r\n' \
  '            let pac = true;\r\n' \
  '            while (ind < trpositions[s].length - 1) {\r\n' \
  '              if (! dr) {\r\n' \
  '                px = trpositions[s][ind];\r\n' \
  '                py = trpositions[s][ind + 1];\r\n' \
  '                ctx.beginPath();\r\n' \
  '                ctx.arc(tr_size * (trpos[0] * px + trpos[2]), tr_size * (trpos[1] * py + trpos[3]), tr_size / scale / trscale, 0, 2 * Math.PI);\r\n' \
  '                ctx.stroke()\r\n' \
  '                ctx.fill();\r\n' \
  '                ctx.beginPath();\r\n' \
  '                move_to(px, py, false);\r\n' \
  '                ind += 2;\r\n' \
  '              } else {\r\n' \
  '                tdx = trpositions[s][ind] - px;\r\n' \
  '                tdy = trpositions[s][ind + 1] - py;\r\n' \
  '                td = Math.sqrt(tdx * tdx + tdy * tdy);\r\n' \
  '                if (td > 0) {\r\n' \
  '                  tx = tdx / td;\r\n' \
  '                  ty = tdy / td;\r\n' \
  '                  dist += td;\r\n' \
  '                  if (! ptg) {\r\n' \
  '                    ptg = true;\r\n' \
  '                    trpaces[trpaces.length - 1][3] = Math.atan2(ty, tx);\r\n' \
  '                  }\r\n' \
  '                }\r\n' \
  '                if (dist < pace_length) {\r\n' \
  '                  px = trpositions[s][ind];\r\n' \
  '                  py = trpositions[s][ind + 1];\r\n' \
  '                  pac = false;\r\n' \
  '                  ind += 2;\r\n' \
  '                  if (ind >= trpositions[s].length - 1) {pac = true;}\r\n' \
  '                  move_to(px, py);\r\n' \
  '                } else {\r\n' \
  '                  pac = true;\r\n' \
  '                  px = trpositions[s][ind] - (dist - pace_length) * tx;\r\n' \
  '                  py = trpositions[s][ind + 1] - (dist - pace_length) * ty;\r\n' \
  '                  dist = 0;\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              dr = true;\r\n' \
  '              if (pac) {\r\n' \
  '                let pz = get_pz(px, py);\r\n' \
  '                trpaces.push([px, py, pz, ((tx==null || ty ==null)?0:Math.atan2(ty, tx))]);\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            ctx.stroke();\r\n' \
  '          }\r\n' \
  '          track.setAttribute("d", trpositions.reduce(function (p, c) {return p + c.reduce(function (p, c, i) {return p + (i%2==0?(" L" + c.toFixed(5)):(" " + (-c).toFixed(5)))}, "").replace("L", "M")}, "").trim());\r\n' \
  '          eye.setAttribute("transform", `scale(${trscale})`);\r\n' \
  '          track.parentNode.setAttribute("viewBox", [(trb[0] + trb[1]) / 2 - trscale, -(trb[2] + trb[3]) / 2 - trscale, 2 * trscale, 2 * trscale].map(String).join(" "));\r\n' \
  '          track.nextElementSibling.style.fontSize=`${2.5 * trscale}%`;\r\n' \
  '          tr_texture = texture_load(gl.TEXTURE1, cnv2d, false);\r\n' \
  '        }\r\n' \
  '        program_create("tcprogram", vertex_tcshader_s, fragment_cshader_s);\r\n' \
  '        program_create("ttprogram", vertex_ttshader_s, fragment_tshader_s);\r\n' \
  '        program_create("sprogram", vertex_sshader_s, fragment_sshader_s);\r\n' \
  '        program_create("rprogram", vertex_rshader_s, fragment_rshader_s);\r\n' \
  '        program_create("pprogram", vertex_pshader_s, fragment_pshader_s);\r\n' \
  '        texture_load(gl.TEXTURE0, [0, 127, 0]);\r\n' \
  '        texture_load(gl.TEXTURE1, [0], false);\r\n' \
  '        create_track();\r\n' \
  '        create_map();\r\n' \
  '        tvposition = buffer_load(vpositions);\r\n' \
  '        tvnormal = buffer_load(vnormals);\r\n' \
  '        for (let n of gl_programs.keys()) {\r\n' \
  '          program_use(n);\r\n' \
  '          program_attributes();\r\n' \
  '          program_uniforms("static");\r\n' \
  '        }\r\n' \
  '        sfrbuf = gl.createFramebuffer();\r\n' \
  '        gl.bindFramebuffer(gl.FRAMEBUFFER, sfrbuf);\r\n' \
  '        d_texture = texture_attach(gl.TEXTURE2);\r\n' \
  '        gl.bindFramebuffer(gl.FRAMEBUFFER, null);\r\n' \
  '      }\r\n' \
  '      function canvas_redraw() {\r\n' \
  '        if (! lmatrix) {\r\n' \
  '          lmatrix = mat4_zscale(1);\r\n' \
  '          ldirection = new Float32Array([0, 0, 0]);\r\n' \
  '          if (dmode == 2) {\r\n' \
  '            mat4_mult(mat4_scale(1.733), lmatrix);\r\n' \
  '            mat4_mult(mat4_rotation(clrangle, slrangle), lmatrix);\r\n' \
  '            mat4_mult(mat4_tilt(cltangle, sltangle), lmatrix);\r\n' \
  '            ldirection.set([-lmatrix[8], -lmatrix[9], -lmatrix[10]]);\r\n' \
  '            ylmag = 1.732 / (1.415 * cltangle - sltangle / zfactmax);\r\n' \
  '            mat4_mult(mat4_yscale(ylmag, 1.415 * cltangle - sltangle), lmatrix);\r\n' \
  '            gl.bindFramebuffer(gl.FRAMEBUFFER, sfrbuf);\r\n' \
  '            gl.viewport(0, 0, d_size, d_size);\r\n' \
  '            gl.clearColor(0, 0, 0, 0);\r\n' \
  '            gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);\r\n' \
  '            program_use("sprogram");\r\n' \
  '            program_uniforms();\r\n' \
  '            gl.drawArrays(gl.TRIANGLE_STRIP, 0, vpositions.length / 3);\r\n' \
  '            gl.bindFramebuffer(gl.FRAMEBUFFER, null);\r\n' \
  '            gl.viewport(0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        gl.clearColor(0.46, 0.68, 0.95, 1);\r\n' \
  '        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);\r\n' \
  '        program_use(fillmode<2?"tcprogram":"ttprogram");\r\n' \
  '        pmode = fillmode==1?1:0;\r\n' \
  '        vmatrix = mat4_zscale(1);\r\n' \
  '        mat4_mult(mat4_translation(-eposition[0], -eposition[1], trpaces[pace][2] + zoff), vmatrix);\r\n' \
  '        mat4_mult(mat4_rotation(crangle, srangle), vmatrix);\r\n' \
  '        mat4_mult(mat4_tilt(ctangle, stangle), vmatrix);\r\n' \
  '        mat4_mult(mat4_perspective(), vmatrix);\r\n' \
  '        program_uniforms();\r\n' \
  '        gl.drawArrays(gl.TRIANGLE_STRIP, 0, vpositions.length / 3);\r\n' \
  '        if (predraw) {\r\n' \
  '          predraw = false;\r\n' \
  '          gl.bindFramebuffer(gl.FRAMEBUFFER, pfrbuf);\r\n' \
  '          gl.viewport(0, 0, gl.drawingBufferWidth / ssampling, gl.drawingBufferHeight / ssampling);\r\n' \
  '          gl.clearBufferiv(gl.COLOR, 0, new Int16Array([-32768, -32768, 0, 0]));\r\n' \
  '          gl.clearBufferfv(gl.DEPTH, 0, new Float32Array([1.0]));\r\n' \
  '          program_use("pprogram");\r\n' \
  '          program_uniforms();\r\n' \
  '          gl.drawArrays(gl.TRIANGLE_STRIP, 0, vpositions.length / 3);\r\n' \
  '          gl.bindFramebuffer(gl.FRAMEBUFFER, null);\r\n' \
  '          gl.viewport(0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight);\r\n' \
  '        }\r\n' \
  '        if (dmode == 2) {\r\n' \
  '          program_use("rprogram");\r\n' \
  '          vmatrix = mat4_zscale(1);\r\n' \
  '          mat4_mult(mat4_tilt(cltangle, -sltangle), vmatrix);\r\n' \
  '          mat4_mult(mat4_rotation(crangle, srangle), vmatrix);\r\n' \
  '          mat4_mult(mat4_rotation(clrangle, -slrangle), vmatrix);\r\n' \
  '          mat4_mult(mat4_tilt(ctangle, stangle), vmatrix);\r\n' \
  '          mat4_mult(mat4_perspective(), vmatrix);\r\n' \
  '          program_uniforms();\r\n' \
  '          gl.depthFunc(gl.LEQUAL)\r\n' \
  '          gl.drawArrays(gl.TRIANGLE_FAN, 0, rnt + 2);\r\n' \
  '          gl.depthFunc(gl.LESS)\r\n' \
  '        }\r\n' \
  '      }\r\n' + HTML_3D_ROT_TEMPLATE + HTML_3D_LOAD_TEMPLATE + \
  '          eposition = new Float32Array(2);\r\n' \
  '          set_param("p", 0);\r\n' \
  '          canvas_redraw();\r\n' \
  '          window.onresize = (e) => {canvas_resize(); canvas_redraw();};\r\n' \
  '          c_tangle.disabled = false;\r\n' \
  '          c_rangle.disabled = false;\r\n' \
  '          b_rangle.disabled = false;\r\n' \
  '          c_pace.max = (trpaces.length - 1).toString();\r\n' \
  '          cv_pace.nextElementSibling.innerHTML = (trpaces.length - 1).toString();\r\n' \
  '          c_pace.disabled = false;\r\n' \
  '          cb_pace.disabled = false\r\n' \
  '          r_yiso.disabled = false;\r\n' \
  '          r_ziso.disabled = false;\r\n' \
  '          r_dimn.disabled = false;\r\n' \
  '          r_dimz.disabled = false\r\n' \
  '          r_dims.disabled = false;\r\n' \
  '          c_ltangle.disabled = false;\r\n' \
  '          c_lrangle.disabled = false;\r\n' \
  '          b_lrangle.disabled = false;\r\n' \
  '          c_vfov.disabled = false;\r\n' \
  '          c_height.disabled = false;\r\n' \
  '          canvas.focus();\r\n' \
  '          canvas.style.outline="none";\r\n' \
  '        }\r\n' \
  '        let xhr = new XMLHttpRequest();\r\n' \
  '        xhr.onerror = (e) => derror_cb(e.target);\r\n' \
  '        xhr.onload = (e) => dload_cb(e.target);\r\n' \
  '        xhr.open("GET", "/3D/data");\r\n' \
  '        xhr.responseType = "arraybuffer";\r\n' \
  '        xhr.send();\r\n' \
  '      }\r\n' \
  '      data_load();\r\n' + HTML_3D_TOGGLE_TEMPLATE + \
  '      function toggle_auto_rotation() {\r\n' \
  '        if (cb_pace.checked) {\r\n' \
  '          if (c_rangle.disabled) {toggle_rotation();}\r\n' \
  '          set_param("p")\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function toggle_dimming(mode) {\r\n' \
  '        if (mode == dmode) {return;};\r\n' \
  '        if (dmode == 2 && c_lrangle.disabled) {toggle_lrotation();}\r\n' \
  '        dmode = mode;\r\n' \
  '        if (dmode == 2) {\r\n' \
  '          c_ltangle.disabled = false;\r\n' \
  '          c_lrangle.disabled = false;\r\n' \
  '          b_lrangle.disabled = false;\r\n' \
  '          lmatrix = null;\r\n' \
  '        } else {\r\n' \
  '          c_ltangle.disabled = true;\r\n' \
  '          c_lrangle.disabled = true;\r\n' \
  '          b_lrangle.disabled = true;\r\n' \
  '        }\r\n' \
  '        canvas_redraw();\r\n' \
  '      }\r\n' \
  '      function process_key(e) {\r\n' \
  '        let rd = false;\r\n' \
  '        let alt = false;\r\n' \
  '        switch (e.key.toLowerCase()) {\r\n' \
  '          case "end":\r\n' \
  '            alt = true;\r\n' \
  '          case "arrowup":\r\n' \
  '            if (pace < parseInt(c_pace.max)) {\r\n' \
  '              set_param("p", alt?parseInt(c_pace.max):Math.min(pace+(e.shiftKey?10:(e.repeat?2:1)),parseInt(c_pace.max)));\r\n' \
  '              rd = true;\r\n' \
  '            } else {return;}\r\n' \
  '            break;\r\n' \
  '          case "home":\r\n' \
  '            alt = true;\r\n' \
  '          case "arrowdown":\r\n' \
  '            if (pace > 0) {\r\n' \
  '              set_param("p", alt?0:Math.max(pace-(e.shiftKey?10:(e.repeat?2:1)),0));\r\n' \
  '              rd = true;\r\n' \
  '            } else {return;}\r\n' \
  '            break;\r\n' \
  '          case "arrowleft":\r\n' \
  '            set_param("r", (parseFloat(c_rangle.value) + (e.shiftKey?350:(e.repeat?358:359))) % 360);\r\n' \
  '            rd = true;\r\n' \
  '            break;\r\n' \
  '          case "arrowright":\r\n' \
  '            set_param("r", (parseFloat(c_rangle.value) + (e.shiftKey?10:(e.repeat?2:1))) % 360);\r\n' \
  '            rd = true;\r\n' \
  '            break;\r\n' \
  '          case "pageup":\r\n' \
  '            set_param("t", Math.min(parseFloat(c_tangle.value) + (e.shiftKey?5:(e.repeat?2:1)), 90));\r\n' \
  '            rd = true;\r\n' \
  '            break;\r\n' \
  '          case "pagedown":\r\n' \
  '            set_param("t", Math.max(parseFloat(c_tangle.value) - (e.shiftKey?5:(e.repeat?2:1)), -90));\r\n' \
  '            rd = true;\r\n' \
  '            break;\r\n' \
  '          case "delete":\r\n' \
  '            cb_pace.checked = ! cb_pace.checked;\r\n' \
  '            toggle_auto_rotation();\r\n' \
  '            break;\r\n' \
  '          case "insert":\r\n' \
  '            set_param("t", 0);\r\n' \
  '            rd = true;\r\n' \
  '            break;\r\n' \
  '          case "-":\r\n' \
  '            c_height.value = Math.max(parseFloat(c_height.value) - 1, 0).toString();\r\n' \
  '            set_param("h");\r\n' \
  '            break;\r\n' \
  '          case "+":\r\n' \
  '            c_height.value = Math.min(parseFloat(c_height.value) + 1, 100).toString();\r\n' \
  '            set_param("h");\r\n' \
  '            break;\r\n' \
  '          case "enter":\r\n' \
  '            if (document.fullscreenElement) {document.exitFullscreen();} else {canvas.parentNode.requestFullscreen();}\r\n' \
  '            break;\r\n' \
  '          default:\r\n' \
  '            return;\r\n' \
  '        }\r\n' \
  '        if (e instanceof KeyboardEvent) {\r\n' \
  '          e.stopPropagation();\r\n' \
  '          e.preventDefault();\r\n' \
  '        }\r\n' \
  '        if (rd) {canvas_redraw();}\r\n' \
  '      }\r\n' \
  '      function toggle_minimap_magnification() {\r\n' \
  '        mzoom = (mzoom==1)?5:1;\r\n' \
  '        mini_map.style.width = (mzoom * 10).toString() + "vh";\r\n' \
  '        mini_map.style.height = (mzoom * 10).toString() + "vh";\r\n' \
  '        eye.setAttribute("transform", `translate(${eposition[0]} ${-eposition[1]}) rotate(${parseFloat(c_rangle.value)}) scale(${trscale / mzoom})`);\r\n' \
  '        eye.setAttribute("fill-opacity", `${1.075 - 0.075 * mzoom}`);\r\n' \
  '        track.nextElementSibling.style.fontSize=`${2.5 * trscale / (0.5 * mzoom + 0.5)}%`;\r\n' \
  '        track.nextElementSibling.style.wordSpacing=`${1.5 * mzoom}em`;\r\n' \
  '        mini_map.style.cursor = (mzoom==1)?"zoom-in":"zoom-out";\r\n' \
  '      }\r\n' \
  '      function toggle_infos() {\r\n' \
  '        if (show_infos) {\r\n' \
  '          show_infos = false;\r\n' \
  '          p_infos.style.display = "none";\r\n' \
  '          e_info.value = "";\r\n' \
  '          clear_tinfos();\r\n' \
  '          predraw = false;\r\n' \
  '        } else {\r\n' \
  '          show_infos = true;\r\n' \
  '          p_infos.style.display = "block";\r\n' \
  '          if (pfrbuf == null) {\r\n' \
  '            pfrbuf = gl.createFramebuffer();\r\n' \
  '            gl.bindFramebuffer(gl.FRAMEBUFFER, pfrbuf);\r\n' \
  '            ptexture_attach(gl.TEXTURE3);\r\n' \
  '            gl.bindFramebuffer(gl.FRAMEBUFFER, null);\r\n' \
  '          }\r\n' \
  '          predraw = true;\r\n' \
  '          canvas_redraw();\r\n' \
  '          update_infos();\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function clear_tinfos(prd=false) {\r\n' \
  '        t_info.value = "";\r\n' \
  '        t_mark.style.display = "none";\r\n' \
  '        t_mark.style.left = "0%";\r\n' \
  '        t_mark.style.top = "0%";\r\n' \
  '        if (prd) {predraw = true;}\r\n' \
  '      }\r\n' \
  '      function update_infos(e=null) {\r\n' \
  '        if (e) {\r\n' \
  '          e.preventDefault();\r\n' \
  '          e.stopPropagation();\r\n' \
  '          gl.bindFramebuffer(gl.FRAMEBUFFER, pfrbuf);\r\n' \
  '          let pxy = new Int16Array(2)\r\n' \
  '          gl.readPixels(Math.round(e.offsetX / canvas.parentNode.offsetWidth * gl.drawingBufferWidth / ssampling), Math.round((canvas.parentNode.offsetHeight - e.offsetY - 1) / canvas.parentNode.offsetHeight * gl.drawingBufferHeight / ssampling), 1, 1, gl.RG_INTEGER, gl.SHORT, pxy);\r\n' \
  '          gl.bindFramebuffer(gl.FRAMEBUFFER, null);\r\n' \
  '          if (pxy[0] != -32768 && pxy[1] != -32768) {\r\n' \
  '            let px = pxy[0] / 32767;\r\n' \
  '            let py = pxy[1] / 32767;\r\n' \
  '            let pz = get_pz(px, py);\r\n' \
  '            let plat = (2 * Math.atan(Math.exp((py * ppos[0] + ppos[2]) / 6378137)) - Math.PI / 2) * 180 / Math.PI;\r\n' \
  '            let plon = (px * ppos[0] + ppos[1]) * 180 / Math.PI / 6378137;\r\n' \
  '            let pele = (pz + 1) * ppos[0] / ppos[4] + ppos[3];\r\n' \
  '            let pdist = ppos[0] / ppos[4] * Math.sqrt((px - eposition[0]) ** 2 + (py - eposition[1]) ** 2);\r\n' \
  '            t_info.value = "{#jplat#} " + plat.toFixed(6) + "° {#jplon#} " + plon.toFixed(6) + "° {#jpele#} " + pele.toFixed(1) + "m {#jpdist#} " + pdist.toFixed(0) + "m";\r\n' \
  '            t_mark.style.left = `calc(${e.offsetX * 100 / canvas.parentNode.offsetWidth}% - 1vh)`;\r\n' \
  '            t_mark.style.top = `calc(${e.offsetY * 100 / canvas.parentNode.offsetHeight}% - 1vh)`;\r\n' \
  '            t_mark.style.display = "block";\r\n' \
  '            if (e.altKey) {complete_infos();}\r\n' \
  '          } else {\r\n' \
  '            clear_tinfos();\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          let plat = (2 * Math.atan(Math.exp((eposition[1] * ppos[0] + ppos[2]) / 6378137)) - Math.PI / 2) * 180 / Math.PI;\r\n' \
  '          let plon = (eposition[0] * ppos[0] + ppos[1]) * 180 / Math.PI / 6378137;\r\n' \
  '          let pele = (trpaces[pace][2] + zoff + 1) * ppos[0] / ppos[4] + ppos[3];\r\n' \
  '          e_info.value = "{#jplat#} " + plat.toFixed(6) + "° {#jplon#} " + plon.toFixed(6) + "° {#jpele#} " + pele.toFixed(1) + "m";\r\n' \
  '          clear_tinfos();\r\n '\
  '          predraw = true;\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function update_waypoint(e) {\r\n' \
  '        e.preventDefault();\r\n' \
  '        e.stopPropagation();\r\n' \
  '        if (! window.opener) {return;}\r\n' \
  '        if (! window.opener.hasOwnProperty("pointed_waypoint")) {return;}\r\n' \
  '        let c = null;\r\n' \
  '        if (e.target.htmlFor == "eye_info") {\r\n' \
  '          c = e_info.value.match(/lat: ([0-9\\.]*?)° lon: ([0-9\\.]*?)° /);\r\n' \
  '        } else if (e.target.htmlFor == "target_info") {\r\n' \
  '          c = t_info.value.match(/lat: ([0-9\\.]*?)° lon: ([0-9\\.]*?)° /);\r\n' \
  '        }\r\n' \
  '        if (c) {\r\n' \
  '          if (c.length == 3) {\r\n' \
  '            let plat = parseFloat(c[1]);\r\n' \
  '            let plon = parseFloat(c[2]);\r\n' \
  '            window.opener.pointed_waypoint([plat, plon]);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function toggle_reversegeocodingswitch() {\r\n' \
  '        if (s_rg.options.length > 0) {\r\n' \
  '          if (p_rg.style.display == "none") {\r\n' \
  '            p_rg.style.display = "block";\r\n' \
  '          } else {\r\n' \
  '            p_rg.style.display = "none";\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function load_rgcb(t, f, c) {\r\n' \
  '        if (t.status != 200) {\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let c_ = f.value.match(/lat: ([0-9\\.]*?)° lon: ([0-9\\.]*?)° /);\r\n' \
  '        if (! c_) {return;}\r\n' \
  '        if (c_.length != 3) {return;}\r\n' \
  '        if (c_[1] != c[0] || c_[2] != c[1]) {return;}\r\n' \
  '        let dpos = f.value.indexOf(" | ");\r\n' \
  '        if (dpos > 0) {f.value = f.value.substring(0, dpos);}\r\n' \
  '        f.value = f.value + " | " + t.response;\r\n' \
  '      }\r\n' \
  '      function error_rgcb() {\r\n' \
  '      }\r\n' \
  '      function complete_infos(e=null) {\r\n' \
  '        let f = null;\r\n' \
  '        if (e) {\r\n' \
  '          e.preventDefault();\r\n' \
  '          e.stopPropagation();\r\n' \
  '          if (e.target.htmlFor != "eye_info" && e.target.htmlFor != "target_info") {return;}\r\n' \
  '          f = e.target.nextElementSibling;\r\n' \
  '        } else {\r\n' \
  '          f = t_info;\r\n' \
  '        }\r\n' \
  '        if (rgset < 0) {return;}\r\n' \
  '        let c = null;\r\n' \
  '        let dpos = f.value.indexOf(" | ");\r\n' \
  '        if (dpos > 0) {f.value = f.value.substring(0, dpos);}\r\n' \
  '        c = f.value.match(/lat: ([0-9\\.]*?)° lon: ([0-9\\.]*?)° /);\r\n' \
  '        if (c) {\r\n' \
  '          if (c.length == 3) {\r\n' \
  '            let plat = parseFloat(c[1]);\r\n' \
  '            let plon = parseFloat(c[2]);\r\n' \
  '            let xhrrg = new XMLHttpRequest();\r\n' \
  '            xhrrg.onerror = error_rgcb;\r\n' \
  '            xhrrg.onload = (e_) => {load_rgcb(e_.target, f, [plat, plon])};\r\n' \
  '            xhrrg.open("POST", "/reversegeocoding?rgset=" + rgset.toString());\r\n' \
  '            xhrrg.setRequestHeader("Content-Type", "application/octet-stream");\r\n' \
  '            xhrrg.send(plat.toString() + "," + plon.toString());\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '       function mouse_down(e) {\r\n' \
  '        if (e.button == 1) {process_key({key:"delete"});return;} else if (e.button != 0) {return;}\r\n' \
  '        canvas.parentNode.onmousemove = mouse_move;\r\n' \
  '        document.onmouseup = mouse_up;\r\n' \
  '        mini_map.setAttribute("pointer-events", "none");\r\n' \
  '        p_infos.style.pointerEvents = "none";\r\n' \
  '        canvas.parentNode.style.cursor = "all-scroll";\r\n' \
  '        click_r = Math.atan((e.offsetX - (canvas.parentNode.offsetWidth - 1) / 2) * 2 / (canvas.parentNode.offsetHeight - 1) / vfov);\r\n' \
  '        click_t = Math.atan(((canvas.parentNode.offsetHeight - 1) / 2 - e.offsetY) * 2 / (canvas.parentNode.offsetHeight - 1) / vfov);\r\n' \
  '        click_cr = parseFloat(c_rangle.value);\r\n' \
  '        click_ct = parseFloat(c_tangle.value);\r\n' \
  '        var click_c = 0;\r\n' \
  '        click_id += 0.5;\r\n' \
  '        var click_lid = click_id;\r\n' \
  '        function loop_redraw(c) {\r\n' \
  '          if (click_lid == click_id) {click_c = c;} else if (click_id - click_lid > 0.6) {return;}\r\n' \
  '          if (c - click_c < 2000) {window.requestAnimationFrame(loop_redraw);}\r\n' \
  '          canvas_redraw();\r\n' \
  '        }\r\n' \
  '        window.requestAnimationFrame(loop_redraw);\r\n' \
  '      }\r\n' \
  '      function mouse_up(e) {\r\n' \
  '        click_id += 0.5;\r\n' \
  '        canvas.parentNode.onmousemove = null;\r\n' \
  '        document.onmouseup = null;\r\n' \
  '        mini_map.removeAttribute("pointer-events");\r\n' \
  '        canvas.parentNode.style.cursor = "";\r\n' \
  '        p_infos.style.pointerEvents = "";\r\n' \
  '      }\r\n' \
  '      function mouse_move(e) {\r\n' \
  '        set_param("r", (360 + click_cr - (Math.atan((e.offsetX - (canvas.parentNode.offsetWidth - 1) / 2) * 2 / (canvas.parentNode.offsetHeight - 1) / vfov) - click_r) * 180 / Math.PI) % 360);\r\n' \
  '        set_param("t", Math.max(Math.min(click_ct - (Math.atan(((canvas.parentNode.offsetHeight - 1) / 2 - e.offsetY) * 2 / (canvas.parentNode.offsetHeight - 1) / vfov) - click_t) * 180 / Math.PI, 90), -90));\r\n' \
  '      }\r\n' \
  '      function mouse_wheel(e) {\r\n' \
  '        if (e.deltaY > 0) {;\r\n' \
  '          if (pace < parseInt(c_pace.max)) {\r\n' \
  '            set_param("p", Math.min(pace + (e.shiftKey?10:1), parseInt(c_pace.max)));\r\n' \
  '            canvas_redraw();\r\n' \
  '          }\r\n' \
  '        } else if (e.deltaY < 0) {;\r\n' \
  '          if (pace > 0) {\r\n' \
  '            set_param("p", Math.max(pace - (e.shiftKey?10:1), 0));\r\n' \
  '            canvas_redraw();\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '    </script>\r\n' \
  '  </body>\r\n' \
  '</html>'
  HTML_3DS_TEMPLATE = HTML_3DS_TEMPLATE.replace('{', '{{').replace('}', '}}').replace('{{#', '{').replace('#}}', '}').format_map(LSTRINGS['interface']).replace('{{', '{').replace('}}', '}')
  HTML_3DS_DECLARATIONS_TEMPLATE = HTML_3DP_DECLARATIONS_TEMPLATE + '\r\n' + \
  '      var scale = ##SCALE##;\r\n' \
  '      var ppos = [##PPOS##];'
  HTMLExp_TEMPLATE = \
  '<!DOCTYPE html>\r\n' \
  '<html lang="fr-FR">\r\n' \
  '  <head>\r\n' \
  '    <meta charset="utf-8">\r\n' \
  '    <title>GPXExplorer</title>\r\n' + HTML_STYLES_TEMPLATE + \
  '      div[id$=cont] {\r\n' \
  '        position:relative;\r\n' \
  '      }\r\n' \
  '      input[type=text]:invalid {\r\n' \
  '        color:rgb(250,220,200);\r\n' \
  '      }\r\n' \
  '      input[id=tracksfilter] {\r\n' \
  '        max-width:calc(98vw - 62em);\r\n' \
  '        width:25em;\r\n' \
  '        font-size:70%;\r\n' \
  '      }\r\n' \
  '      form[id^=track] {\r\n' \
  '        overflow:hidden;\r\n' \
  '        margin-right: 4px;\r\n' \
  '      }\r\n' \
  '      input[id$=visible] {\r\n' \
  '        margin-left:0.3%;\r\n' \
  '        margin-right:2.2%;\r\n' \
  '        margin-top:0;\r\n' \
  '        margin-bottom:0.3em;\r\n' \
  '        width:5.2%;\r\n' \
  '      }\r\n' \
  '      label[id$=desc] {\r\n' \
  '        cursor:cell;\r\n' \
  '        display:inline-block;\r\n' \
  '        margin-bottom:0.3em;\r\n' \
  '        width:92.3%;\r\n' \
  '        vertical-align:middle;\r\n' \
  '        white-space:nowrap;\r\n' \
  '        line-height:1.15em;\r\n' \
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
  '      span[id$=focus] {\r\n' \
  '        display:none;\r\n' \
  '      }\r\n' \
  '      svg[id^=track] text {\r\n' \
  '        display:none;\r\n' \
  '      }\r\n' \
  '      label[for^=folder] {\r\n' \
  '        display:inline-block;\r\n' \
  '        vertical-align:middle;\r\n' \
  '        white-space:nowrap;\r\n' \
  '      }\r\n' \
  '      svg[id*=waydots] {\r\n' \
  '        stroke:white;\r\n' \
  '        stroke-width:calc(2px * var(--scale) * (var(--magnify) + 1) / 2);\r\n' \
  '        paint-order:stroke;\r\n' \
  '      }\r\n' \
  '      svg circle {\r\n' \
  '        r:calc(3px * var(--scale) * (var(--magnify) + 1) / 2);\r\n' \
  '        pointer-events:all;\r\n' \
  '      }\r\n' \
  '      div [id=geomedia] {\r\n' \
  '        position:absolute;\r\n' \
  '        pointer-events:none;\r\n' \
  '      }\r\n' \
  '      div[id=geomedia] * {\r\n' \
  '        background:darkgray;\r\n' \
  '        cursor:zoom-in;\r\n' \
  '        pointer-events:initial;\r\n' \
  '      }\r\n' \
  '      div[id=geomedia] img {\r\n' \
  '        image-orientation:from-image;\r\n' \
  '      }\r\n' \
  '      div[id=geomedia] *[id*=","] {\r\n' \
  '        outline-offset:-3px;\r\n' \
  '        outline:outset 3px lightgray;\r\n' \
  '      }\r\n' \
  '      @supports not (selector(*::-moz-color-swatch)) {\r\n' \
  '        div[id=geomedia]>img::before{\r\n' \
  '          content:"";\r\n' \
  '          position:absolute;\r\n' \
  '          left:3px;\r\n' \
  '          top:3px;\r\n' \
  '          background:darkgray;\r\n' \
  '          width:calc(100% - 6px);\r\n' \
  '          height:calc(100% - 6px);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      div[id^=media] {\r\n' \
  '        width:100%;\r\n' \
  '        background:rgb(30,30,35);\r\n' \
  '        overflow-x:auto;\r\n' \
  '        overflow-y:hidden;\r\n' \
  '        white-space:nowrap;\r\n' \
  '        line-height:0;\r\n' \
  '        text-align:center;\r\n' \
  '        user-select:none;\r\n' \
  '      }\r\n' \
  '      div[id=mediapreview] {\r\n' \
  '        position:relative;\r\n' \
  '        height:25vh;\r\n' \
  '        border-top:1px darkgray solid;\r\n' \
  '      }\r\n' \
  '      div[id=mediaview] {\r\n' \
  '        position:absolute;\r\n' \
  '        z-index:10;\r\n' \
  '        height:100%;\r\n' \
  '        bottom:0;\r\n' \
  '        left:0;\r\n' \
  '      }\r\n' \
  '      div[id^=media]::before {\r\n' \
  '        content:"";\r\n' \
  '        display:inline-block;\r\n' \
  '        vertical-align:middle;\r\n' \
  '        height:100%;\r\n' \
  '      }\r\n' \
  '      div[id^=media] * {\r\n' \
  '        display:inline-block;\r\n' \
  '        max-height:100%;\r\n' \
  '        max-width:100%;\r\n' \
  '        vertical-align:middle;\r\n' \
  '        object-fit:scale-down;\r\n' \
  '      }\r\n' \
  '      div[id^=media] img {\r\n' \
  '        image-orientation:from-image;\r\n' \
  '        cursor:nesw-resize;\r\n' \
  '        font-size:0;\r\n' \
  '      }\r\n' \
  '      div[id^=media] *:not(:last-child) {\r\n' \
  '        margin-right:14px;\r\n' \
  '      }\r\n' \
  '    </style>\r\n' \
  '    <script>\r\n' + HTML_GLOBALVARS_TEMPLATE + \
  '      var mportmin = ##MPORTMIN##;\r\n' \
  '      var mportmax = ##MPORTMAX##;\r\n' \
  '      var str_comp = new Intl.Collator().compare;\r\n' \
  '      var no_sort = null;\r\n' \
  '      var magnify = 1;\r\n' \
  '      var smoothed = ##SMENABLED##;\r\n' \
  '      var tracks_pts = [];\r\n' \
  '      var tracks_xys = null;\r\n' \
  '      var tracks_pts_smoothed = null;\r\n' \
  '      var tracks_xys_smoothed = null;\r\n' \
  '      var tracks_stats = [];\r\n' \
  '      var tracks_props = [];\r\n' + HTML_GPUSTATS_TEMPLATE + \
  '      if (gpucomp > 0) {var gpustats = new GPUStats("explorer");}\r\n' \
  '      var media_visible = false;\r\n' \
  '      var media_ex_visible = false;\r\n' \
  '      var media_gps_ar = null;\r\n' \
  '      var media_uri_dt = null;\r\n' \
  '      var media_isvid = null;\r\n' \
  '      var media_corners = null;\r\n' \
  '      var media_corners_updated = true;\r\n' \
  '      var media_sides = null;\r\n' \
  '      var media_div = null;\r\n' \
  '      var media_hold = null;\r\n' \
  '      var media_fs = false;\r\n' + HTML_MSG_TEMPLATE + \
  '      function switch_tiles(nset, nlevel, kzoom=false) {\r\n' \
  '        let b = 0;\r\n' \
  '        if (nset == null && nlevel == null) {\r\n' \
  '          switch (kzoom) {\r\n' \
  '            case 1:\r\n' \
  '              if (focused) {\r\n' \
  '                b = track_boundaries(document.getElementById(focused));\r\n' \
  '              } else {\r\n' \
  '                b = null;\r\n' \
  '              }\r\n' \
  '              break\r\n' \
  '            case 2:\r\n' \
  '              let tracks = [];\r\n' \
  '              let trks = document.getElementById("tracksform").children;\r\n' \
  '              for (let t=0; t<trks.length; t++) {\r\n' \
  '                if (trks[t].firstElementChild.checked && trks[t].style.display != "none") {\r\n' \
  '                  tracks.push(document.getElementById(trks[t].id.slice(0, -4)));\r\n' \
  '                 }\r\n' \
  '              }\r\n' \
  '              b = track_boundaries(tracks);\r\n' \
  '              break;\r\n' \
  '            default:\r\n' \
  '              b = track_boundaries();\r\n' \
  '          }\r\n' \
  '          if (mode == "map") {\r\n' \
  '            if (b == null) {return;}\r\n' \
  '            let r = Math.max((b[1] - b[0]) / viewpane.offsetWidth, (b[3] - b[2]) / viewpane.offsetHeight);\r\n' \
  '            let z = eval(zooms.slice(-1)[0]);\r\n' \
  '            if (r > 0) {z = 1 / r / Math.min((viewpane.offsetWidth - 2) / (vmaxx - vminx), (viewpane.offsetHeight - 4) / (vmaxy - vminy));}\r\n' \
  '            let zoom_s_ex = zoom_s;\r\n' \
  '            zoom_s = "1";\r\n' \
  '            for (let i=1; i<zooms.length; i++) {\r\n' \
  '              if (eval(zooms[i]) <= z) {zoom_s = zooms[i];} else {break;}\r\n' \
  '            }\r\n' \
  '            if (zoom_s != zoom_s_ex) {rescale();}\r\n' \
  '            scroll_to_track(null, true, b);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (mode == "map") {return;}\r\n' \
  '        document.getElementById("tset").disabled = true;\r\n' \
  '        document.getElementById("tset").style.pointerEvents = "none";\r\n' \
  '        let q = "";\r\n' \
  '        let sta = false;\r\n' \
  '        if (nset != null) {\r\n' \
  '          document.getElementById("opanel").style.display="none";\r\n' \
  '          if (nset == -1) {\r\n' \
  '            nset = 0;\r\n' \
  '            q = "set=" + encodeURIComponent(document.getElementById("tset").selectedIndex);\r\n' \
  '          } else {\r\n' \
  '            q = "set=" + encodeURIComponent(nset);\r\n' \
  '          }\r\n' \
  '        } else if (nlevel != null) {\r\n' \
  '          q = "matrix=" + encodeURIComponent(tlevels[nlevel][0].toString());\r\n' \
  '          sta = twidth == 0 && focused == "";\r\n' \
  '        } else {\r\n' \
  '          sta = true;\r\n' \
  '          if (b == null) {\r\n' \
  '            if (twidth || kzoom != true) {\r\n' \
  '              document.getElementById("tset").disabled = false;\r\n' \
  '              document.getElementById("tset").style.pointerEvents = "";\r\n' \
  '              return;\r\n' \
  '            }\r\n' \
  '            nlevel = tlevels[0];\r\n' \
  '            q = "matrix=" + encodeURIComponent(tlevels[nlevel][0].toString());\r\n' \
  '          } else {\r\n' \
  '            q = "auto=" + encodeURIComponent(Math.max((b[1] - b[0]) / viewpane.offsetWidth, (b[3] - b[2]) / viewpane.offsetHeight).toString());\r\n' \
  '          }\r\n' \
  '          kzoom = false;\r\n' \
  '        }\r\n' \
  '        if (xhr_ongoing == 0) {window.stop();}\r\n' \
  '        xhrt.onload = (e) => {load_tcb(e.target, nset, nlevel, kzoom); if(sta) {scroll_to_track(null, true, b);};};\r\n' \
  '        xhrt.open("GET", "/tiles/switch?" + q);\r\n' \
  '        xhrt.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhrt.send();\r\n' \
  '      }\r\n' + HTML_TILES_TEMPLATE.rsplit('update_tiles();\r\n', 1)[0] + 'let mvis = media_visible;\r\n' \
  '        hide_media("m");\r\n' \
  '        update_tiles();\r\n' \
  '        if (mvis) {show_media();}\r\n' \
  '        if (document.getElementById("oset").selectedIndex == 8) {tracks_sort();}\r\n' \
  '      }\r\n' + HTML_UTIL_TEMPLATE + \
  '      function track_boundaries(tracks=null) {\r\n' \
  '        if (tracks == null) {\r\n' \
  '          tracks = [];\r\n' \
  '          let trks = document.getElementById("tracksform").children;\r\n' \
  '          for (let t=0; t<trks.length; t++) {\r\n' \
  '            if (trks[t].firstElementChild.checked) {\r\n' \
  '              tracks.push(document.getElementById(trks[t].id.slice(0, -4)));\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        } else if (! Array.isArray(tracks)) {\r\n' \
  '          tracks = [tracks];\r\n' \
  '        }\r\n' \
  '        let gminx = null;\r\n' \
  '        let gminy = null;\r\n' \
  '        let gmaxx = null;\r\n' \
  '        let gmaxy = null;\r\n' \
  '        for (let t=0; t<tracks.length; t++) {\r\n' \
  '          let trind = parseInt(tracks[t].id.substring(5));\r\n' \
  '          let empt = document.getElementById("waydots" + trind.toString()).childElementCount == 0;\r\n' \
  '          if (empt) {\r\n' \
  '            for (let s=0; s<tracks_pts[trind].length; s++) {\r\n' \
  '              if (tracks_pts[trind][s].length > 0) {empt = false; break;}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (empt) {continue;}\r\n' \
  '          let minx = prop_to_wmvalue(tracks[t].style.left);\r\n' \
  '          let miny = prop_to_wmvalue(tracks[t].style.top);\r\n' \
  '          let maxx = minx + prop_to_wmvalue(tracks[t].style.width);\r\n' \
  '          let maxy = miny + prop_to_wmvalue(tracks[t].style.height);\r\n' \
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
  '      }\r\n' + HTML_SCROLL_TEMPLATE + \
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
  '            if (scrollmode > 0) {scroll_to_track(document.getElementById(focused), scrollmode == 2)};\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        refresh_graph();\r\n' \
  '      }\r\n' \
  '      function track_over(trk) {\r\n' \
  '        let foc = trk.id.indexOf("color")<0?((trk.id.indexOf("desc")<0?trk.id:trk.htmlFor).slice(0, -7)):trk.id.slice(0, -5);\r\n' \
  '        document.getElementById(foc.replace("track", "waydots")).style.zIndex = "2";\r\n' \
  '        document.getElementById(foc).style.zIndex = "2";\r\n' \
  '        document.getElementById(foc.replace("track", "patharrows")).style.display = "inline";\r\n' \
  '        if ((document.getElementById(foc + "visible").checked || foc == focused) && document.getElementById("oset").selectedIndex != 8) {\r\n' \
  '          if (scrollmode == 2) {scroll_to_track(document.getElementById(foc), false);}\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function track_outside(trk) {\r\n' \
  '        let foc = trk.id.indexOf("color")<0?((trk.id.indexOf("desc")<0?trk.id:trk.htmlFor).slice(0, -7)):trk.id.slice(0, -5);\r\n' \
  '        document.getElementById(foc.replace("track", "waydots")).style.zIndex = foc==focused?"1":"";\r\n' \
  '        document.getElementById(foc).style.zIndex = foc==focused?"1":"";\r\n' \
  '        document.getElementById(foc.replace("track", "patharrows")).style.display = foc==focused?"inline":"";\r\n' \
  '      }\r\n' \
  '      function segment_calc(seg, seg_smoothed, smoothed_ch, seg_ind, stats, fpan=0, ind=null, teahs=null) {\r\n' \
  '        if (fpan == 0) {\r\n' \
  '          while (stats.length <= seg_ind) {stats.push([]);}\r\n' \
  '          stats[seg_ind] = [];\r\n' \
  '        }\r\n' \
  '        let seg_c = seg_smoothed?seg_smoothed:seg;\r\n' \
  '        if (fpan <= 1 || (fpan == 2 && gpucomp == 0)) {\r\n' + HTML_SEGCALC_1_TEMPLATE + \
  '          for (let p=0; p<seg.length; p++) {\r\n' \
  '            let pt = seg[p];\r\n' \
  '            let ea = [parseFloat(pt[2]), parseFloat(pt[3])];\r\n' \
  '            for (let v=0; v<2; v++) {\r\n' \
  '              if (! isNaN(ea[v]) && isNaN(ea_p[v])) {\r\n' \
  '                ea_p[v] = ea[v];\r\n' \
  '                ea_r[v] = ea_b[v] = ea[v];\r\n' \
  '                ea_s[v] = ea_p[v];\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            if (fpan == 0 || fpan == 2) {\r\n' \
  '              let t = Date.parse(pt[4]);\r\n' + HTML_SEGCALC_2_TEMPLATE + \
  '            if (gpucomp == 0 && (fpan == 0 || fpan == 2)) {\r\n' \
  '              stat[4] = isNaN(ea[0])?ea_p[0]:ea[0];\r\n' \
  '              stat[5] = isNaN(ea[1])?ea_p[1]:ea[1];\r\n' \
  '              stat[6] = isNaN(el_p)?el_p:el;\r\n' \
  '            }\r\n' \
  '            if (p_p == null) {\r\n' \
  '              if (gpucomp == 0) {\r\n' \
  '                if (fpan == 0 || smoothed_ch) {\r\n' \
  '                  lat = parseFloat(seg_c[p][0]);\r\n' \
  '                  lon = parseFloat(seg_c[p][1]);\r\n' \
  '                }\r\n' \
  '              } else if (fpan == 0) {\r\n' \
  '                teahs.set([stat[0], isNaN(ea[0])?ea_p[0]:ea[0], isNaN(ea[1])?ea_p[1]:ea[1], el_p], 4 * ind);\r\n' \
  '                ind++;\r\n' \
  '              }\r\n' \
  '            } else {\r\n' \
  '              if (gpucomp <= 1 && fpan <= 1) {\r\n' \
  '                stat[2] = stat_p[2] + ((isNaN(ea_p[0])||isNaN(ea[0]))?0:Math.max(0,ea[0]-ea_b[0]));\r\n' \
  '                stat[3] = stat_p[3] + ((isNaN(ea_p[1])||isNaN(ea[1]))?0:Math.max(0,ea[1]-ea_b[1]));\r\n' \
  '              }\r\n' \
  '              if (gpucomp == 0) {\r\n' \
  '                if (fpan == 0 || smoothed_ch) {\r\n' \
  '                  lat = parseFloat(seg_c[p][0]);\r\n' \
  '                  lon = parseFloat(seg_c[p][1]);\r\n' \
  '                  stat[1] = stat_p[1] + distance(lat_p, lon_p, null, lat, lon, null);\r\n' \
  '                  if (fpan != 0) {stats[seg_ind][stat_i][1] = stat[1];}\r\n' \
  '                }\r\n' \
  '              } else if (fpan == 0) {\r\n' \
  '                teahs.set([stat[0], isNaN(ea[0])?ea_p[0]:ea[0], isNaN(ea[1])?ea_p[1]:ea[1], isNaN(el_p)?el_p:el], 4 * ind);\r\n' \
  '                ind++;\r\n' \
  '              }\r\n' \
  '            }\r\n' + HTML_SEGCALC_3_TEMPLATE + \
  '          } else if (gpucomp != 0 && fpan == 0) {\r\n' \
  '            for (let i=ind-stat_i; i<ind; i++) {\r\n' \
  '              if (isNaN(teahs[4 * i + 1])) {teahs[4 * i + 1] = ea_s[0];} else {break;}\r\n' \
  '            }\r\n' \
  '            for (let i=ind-stat_i; i<ind; i++) {\r\n' \
  '              if (isNaN(teahs[4 * i + 2])) {teahs[4 * i + 2] = ea_s[1];} else {break;}\r\n' \
  '            }\r\n' \
  '            for (let i=ind-stat_i; i<ind; i++) {\r\n' \
  '              if (isNaN(teahs[4 * i + 3])) {teahs[4 * i + 3] = el_s;} else {break;}\r\n' \
  '            }\r\n' \
  '          }\r\n' + HTML_SEGCALC_4_TEMPLATE + \
  '        }\r\n' + HTML_SEGCALC_5_TEMPLATE + \
  '      }\r\n' \
  '      function tracks_calc(fpan=0) {\r\n' \
  '        let starts = null;\r\n' \
  '        let tls = null;\r\n' \
  '        let lls = null;\r\n' \
  '        let teahs = null;\r\n' \
  '        let nbtracks = tracks_pts.length;\r\n' \
  '        if (fpan == 0) {\r\n' \
  '          let nbpt = tracks_pts.reduce((p,c) => p + c.reduce((p,c) => p + c.length, 0), 0);\r\n' \
  '          tracks_xys = new Float32Array(GPUStats.pad(nbpt) * 2);\r\n' \
  '          tracks_pts_smoothed = null;\r\n' \
  '          tracks_xys_smoothed = null;\r\n' \
  '          tracks_stats = [];\r\n' \
  '          tracks_props = [];\r\n' \
  '          tls = [];\r\n' \
  '          if (gpucomp >= 1) {\r\n' \
  '            starts = [0];\r\n' \
  '            lls = new Float32Array(GPUStats.pad(nbpt) * 2);\r\n' \
  '            teahs = new Float32Array(GPUStats.pad(nbpt) * 4);\r\n' \
  '          }\r\n' \
  '          let ind = 0;\r\n' \
  '          for (let t=0; t<nbtracks; t++) {\r\n' \
  '            let segs = tracks_pts[t];\r\n' \
  '            tracks_stats.push([]);\r\n' \
  '            tracks_props.push([NaN, NaN, NaN, NaN, NaN, [NaN, NaN]]);\r\n' \
  '            for (const seg of segs) {\r\n' \
  '              let nbp = seg.length;\r\n' \
  '              if (nbp != 0) {\r\n' \
  '                if (gpucomp == 0) {\r\n' \
  '                  let tl = [htopy - prop_to_wmvalue(document.getElementById("track" + t.toString()).style.top), htopx + prop_to_wmvalue(document.getElementById("track" + t.toString()).style.left)];\r\n' \
  '                  let g = [];\r\n' \
  '                  seg.forEach((c) => {let [x, y] = WGS84toWebMercator(parseFloat(c[0]), parseFloat(c[1])); g.push(x - tl[1], tl[0] - y)});\r\n' \
  '                  tracks_xys.set(g, 2 * ind);\r\n' \
  '                } else {\r\n' \
  '                  starts.push(starts[starts.length - 1] + nbp);\r\n' \
  '                  let tl = WebMercatortoWGS84(htopx + prop_to_wmvalue(document.getElementById("track" + t.toString()).style.left), htopy - prop_to_wmvalue(document.getElementById("track" + t.toString()).style.top));\r\n' \
  '                  tls.push(tl);\r\n' \
  '                  let g = [];\r\n' \
  '                  seg.forEach((c) => g.push(tl[0] - parseFloat(c[0]), parseFloat(c[1]) - tl[1]));\r\n' \
  '                  lls.set(g, 2 * ind);\r\n' \
  '                }\r\n' \
  '                ind += nbp;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (gpucomp >=1) {\r\n' \
  '            gpustats.starts = starts;\r\n' \
  '            if (nbpt == 0) {return;}\r\n' \
  '            gpustats.rlats = tls;\r\n' \
  '            gpustats.lls = lls;\r\n' \
  '            gpustats.calc("pos");\r\n' \
  '            tracks_xys.set(gpustats.xys);\r\n' \
  '          }\r\n' \
  '          if (smoothed) {tracks_smooth();}\r\n' \
  '        }\r\n' \
  '        if (tracks_stats.length == 0) {\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let smoothed_ch = false;\r\n' \
  '        if (smoothed && tracks_pts_smoothed == null) {\r\n' \
  '          tracks_pts_smoothed = [];\r\n' \
  '          smoothed_ch = true;\r\n' \
  '          if (gpucomp == 0) {\r\n' \
  '            let ind = 0;\r\n' \
  '            for (let t=0; t<nbtracks; t++) {\r\n' \
  '              let segs = tracks_pts[t];\r\n' \
  '              let nbsegs = segs.length;\r\n' \
  '              let track_pts_smoothed = [];\r\n' \
  '              tracks_pts_smoothed.push(track_pts_smoothed);\r\n' \
  '              let tl = [htopy - prop_to_wmvalue(document.getElementById("track" + t.toString()).style.top), htopx + prop_to_wmvalue(document.getElementById("track" + t.toString()).style.left)];\r\n' \
  '              for (const seg of segs) {\r\n' \
  '                let nbp = seg.length;\r\n' \
  '                if (nbp != 0) {\r\n' \
  '                  let nind = ind + nbp;\r\n' \
  '                  let seg_pts_smoothed = [];\r\n' \
  '                  track_pts_smoothed.push(seg_pts_smoothed);\r\n' \
  '                  for (let p=ind; p<nind; p++) {\r\n' \
  '                    seg_pts_smoothed.push(WebMercatortoWGS84(tracks_xys_smoothed[2 * p] + tl[1], tl[0] - tracks_xys_smoothed[2 * p + 1]));\r\n' \
  '                  }\r\n' \
  '                  ind = nind;\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            gpustats.xys = tracks_xys_smoothed;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (! smoothed && tracks_pts_smoothed != null) {\r\n' \
  '          tracks_pts_smoothed = null;\r\n' \
  '          smoothed_ch = true;\r\n' \
  '          if (gpucomp >=1) {gpustats.lls = gpustats.lls;}\r\n' \
  '        }\r\n' \
  '        if (fpan <= 1 || gpucomp == 0) {\r\n' \
  '          let ind = 0;\r\n' \
  '          for (let t=0; t<nbtracks; t++) {\r\n' \
  '            let segs = tracks_pts[t];\r\n' \
  '            for (let s=0; s<segs.length; s++) {\r\n' \
  '              segment_calc(segs[s], (smoothed && gpucomp==0)?tracks_pts_smoothed[t][s]:null, smoothed_ch, s, tracks_stats[t], fpan, ind, teahs);\r\n' \
  '              let nbp = segs[s].length;\r\n' \
  '              ind += nbp;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (fpan == 0 && gpucomp >= 1) {\r\n' \
  '          gpustats.teahs = teahs;\r\n' \
  '        }\r\n' \
  '        if (gpucomp >= 1 && fpan != 1) {\r\n' \
  '          if (gpustats.starts[gpustats.starts.length - 1] == 0) {\r\n' \
  '            return;\r\n' \
  '          }\r\n' \
  '          gpustats.trange = parseFloat(document.getElementById("sptime").innerHTML) / 2;\r\n' \
  '          gpustats.spmax = parseFloat(document.getElementById("spmax").innerHTML) / 3.6;\r\n' \
  '          gpustats.drange = Math.max(0.01, parseFloat(document.getElementById("sldist").innerHTML)) / 2;\r\n' \
  '          gpustats.slmax = parseFloat(document.getElementById("slmax").innerHTML) / 100;\r\n' \
  '          gpustats.calc((fpan==0 || smoothed_ch)?(smoothed?"gwmdist":"gdist"):"");\r\n' \
  '          let gs = gpustats.gs;\r\n' \
  '          let ssss = gpustats.ssss;\r\n' \
  '          let ss = gpustats.ss;\r\n' \
  '          let i = 0;\r\n' \
  '          for (let t=0; t<nbtracks; t++) {\r\n' \
  '            let segs = tracks_pts[t];\r\n' \
  '            let stats = tracks_stats[t];\r\n' \
  '            for (let s=0; s<segs.length; s++) {\r\n' \
  '              for (let p=0; p<segs[s].length; p++) {\r\n' \
  '                let stat = stats[s][p];\r\n' \
  '                if (fpan == 0 || smoothed_ch) {stat[1] = stats[s][p>0?p-1:0][1] + gs[i];}\r\n' \
  '                stat[7] = ss[i];\r\n' \
  '                stat[4] = ssss[3 * i];\r\n' \
  '                stat[5] = ssss[3 * i + 1];\r\n' \
  '                stat[6] = p==0?0:(stats[s][p-1][6] + ssss[3 * i - 1]);\r\n' \
  '                if (gpucomp == 2 && fpan != 3) {\r\n' \
  '                  if (p == 0) {\r\n' \
  '                    stat[2] = 0;\r\n' \
  '                    stat[3] = 0;\r\n' \
  '                  } else {\r\n' \
  '                    stat[2] = stats[s][p - 1][2] + Math.max(0, ssss[3 * i - 3]) * gs[i];\r\n' \
  '                    stat[3] = stats[s][p - 1][3] + Math.max(0, ssss[3 * i - 2]) * gs[i];\r\n' \
  '                  }\r\n' \
  '                }\r\n' \
  '                i++;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (fpan == 0 || smoothed_ch) {\r\n' \
  '          let xys = smoothed?tracks_xys_smoothed:tracks_xys;\r\n' \
  '          let ind = 0;\r\n' \
  '          for (let t=0; t<nbtracks; t++) {\r\n' \
  '            let segs = tracks_pts[t];\r\n' \
  '            let d = "M0 0";\r\n' \
  '            for (let s=0; s<segs.length; s++) {\r\n' \
  '              for (let p=0; p<segs[s].length; p++) {\r\n' \
  '                d += (p==0?" M":" L") + xys[2 * ind].toFixed(1) + " " + xys[2 * ind + 1].toFixed(1);\r\n' \
  '                ind++;\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            document.getElementById("path" + t.toString()).setAttribute("d", d);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (fpan != 3) {\r\n' \
  '          for (let t=0; t<nbtracks; t++) {\r\n' \
  '            let dur = null;\r\n' \
  '            let dist = null;\r\n' \
  '            let ele = null;\r\n' \
  '            let alt = null;\r\n' \
  '            let stats = tracks_stats[t];\r\n' \
  '            for (let s=0; s<stats.length; s++) {\r\n' \
  '              if (stats[s].length == 0) {continue;}\r\n' \
  '              let stat = stats[s][stats[s].length - 1];\r\n' \
  '              dur = dur==null?stat[0]:dur+stat[0];\r\n' \
  '              dist = dist==null?stat[6]:dist+stat[6];\r\n' \
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
  '                }\r\n' \
  '              }\r\n' \
  '              for (let s=0; s<segs.length; s++) {\r\n' \
  '                for (let p=0; p<segs[s].length; p++) {\r\n' \
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
  '                  if (! noe && ! noa && slat != null) {break;}\r\n' \
  '                }\r\n' \
  '                if (! noe && ! noa && slat != null) {break;}\r\n' \
  '              }\r\n' \
  '              tracks_props[t] = [ts==null?NaN:dur, dist==null?NaN:dist, noe?NaN:ele, noa?NaN:alt, ts==null?NaN:ts, slat==null?[NaN, NaN]:[slat, slon]];\r\n' \
  '              if (ts != null) {\r\n' \
  '                document.getElementById("track" + t.toString() + "period").value = time_conv.format(ts)  + " " + date_conv.format(ts) + " - " + time_conv.format(te)  + " " + date_conv.format(te);\r\n' \
  '              }\r\n' \
  '            } else {\r\n' \
  '              if (! isNaN(tracks_props[t][1])) {\r\n' \
  '                tracks_props[t][1] = dist;\r\n' \
  '                noe = false;\r\n' \
  '              }\r\n' \
  '              if (! isNaN(tracks_props[t][2])) {\r\n' \
  '                tracks_props[t][2] = ele;\r\n' \
  '                noe = false;\r\n' \
  '              }\r\n' \
  '              if (! isNaN(tracks_props[t][3])) {\r\n' \
  '                tracks_props[t][3] = alt;\r\n' \
  '                noa = false;\r\n' \
  '              }\r\n' \
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
  '        if ([4, 5, 6].includes(document.getElementById("oset").selectedIndex) && (fpan == 1 || fpan == 2)) {tracks_sort();}\r\n' \
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
  '      }\r\n' + HTML_GRAPH1_TEMPLATE + \
  '        if (focused == "") {return;}\r\n' \
  '        let stats = tracks_stats[parseInt(focused.substring(5))];\r\n' \
  '        for (let s=0; s<stats.length; s++) {\r\n' \
  '          if (stats[s].length == 0) {continue;}\r\n' \
  '          let stat = null;\r\n' \
  '          gc.push(gx.length);\r\n' \
  '          for (let p=0; p<stats[s].length; p++) {\r\n' \
  '            stat = stats[s][p];\r\n' \
  '            let pt = tracks_pts[parseInt(focused.substring(5))][s][p];\r\n' \
  '            let ea = null;\r\n' \
  '            if (gy_ind == 1 || gy_ind == 2) {ea = parseFloat(pt[gy_ind + 1]);}\r\n' + HTML_GRAPH2_TEMPLATE + \
  '            }\r\n' \
  '          }\r\n' \
  '          dur += stat[0];\r\n' \
  '          dist += stat[6];\r\n' \
  '          ele += stat[2];\r\n' \
  '          alt += stat[3];\r\n' \
  '        }\r\n' \
  '        if (gx.length < 2) {return;}\r\n' + HTML_GRAPH3_TEMPLATE + \
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
  '      function open_3D(mode3d="p") {\r\n' \
  '        if (eset < 0) {show_msg("{#jmelevationsno#}", 10); return;}\r\n' \
  '        if (mode != "map") {\r\n' \
  '          if (tlayers.has(tset) || jmaps.length > 0) {show_msg("{#jm3dviewer4#}", 10); return;}\r\n' \
  '        }\r\n' \
  '        if (document.getElementById("edit").disabled) {return;}\r\n' \
  '        if (focused == "") {return;}\r\n' \
  '        window.open("http://" + host + location.port + "/3D/viewer.html?3d=" + mode3d + document.getElementById(`v3d${mode3d}dist`).innerHTML + "," + focused.substring(5));\r\n' \
  '      }\r\n' + HTML_MAP_TEMPLATE.replace('function rescale(tscale_ex=tscale) {\r\n', 'function rescale(tscale_ex=tscale) {\r\n        media_sides = null;\r\n') + \
  '      function magnify_dec() {\r\n' \
  '        if (magnify > 1) {\r\n' \
  '          magnify--;\r\n' \
  '          document.documentElement.style.setProperty("--magnify", magnify.toString());\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function magnify_inc() {\r\n' \
  '        if (magnify < 3) {\r\n' \
  '          magnify++;\r\n' \
  '          document.documentElement.style.setProperty("--magnify", magnify.toString());\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function tracks_filter() {\r\n' \
  '        let filt = document.getElementById("tracksfilter").value.toLowerCase();\r\n' \
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
  '      function tracks_filter_history() {\r\n' \
  '        let filt = document.getElementById("tracksfilter").value;\r\n' \
  '        if (! filt) {return;}\r\n' \
  '        let fhist = document.getElementById("tracksfilterhistory");\r\n' \
  '        let fopts = fhist.getElementsByTagName("option");\r\n' \
  '        let opt = null;\r\n' \
  '        for (let o=0; o<fopts.length; o++) {\r\n' \
  '          if (fopts[o].value.toLowerCase() == filt.toLowerCase()) {\r\n' \
  '            opt = fhist.removeChild(fopts[o]);\r\n' \
  '            break;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (opt == null) {opt = document.createElement("option");}\r\n' \
  '        opt.value = filt;\r\n' \
  '        fhist.insertBefore(opt, fhist.firstElementChild);\r\n' \
  '      }\r\n' \
  '      function tracks_sort() {\r\n' \
  '        let crit = document.getElementById("oset").selectedIndex;\r\n' \
  '        let asc = document.getElementById("sortup").style.display != "none";\r\n' \
  '        let trks = Array.from({length:tracks_pts.length}).map((v,k)=>k);\r\n' \
  '        let n = function (a, b) {return no_sort[a] - no_sort[b]};\r\n' \
  '        let c = n;\r\n' \
  '        let vals = [];\r\n' \
  '        function comp_flt(a, b) {\r\n' \
  '          if (a == b || (isNaN(a) && isNaN(b))) {return 0;}\r\n' \
  '          if (isNaN(a)) {return 1;}\r\n' \
  '          if (isNaN(b)) {return -1;}\r\n' \
  '          return asc?a-b:b-a;\r\n' \
  '        }\r\n' \
  '        function comp_name(a, b) {\r\n' \
  '          if (a == b) {return 0;}\r\n' \
  '          let a_s = a.match(/(.*?)(?:(\\d+)|(?:\\((\\d+)\\)))?$/);\r\n' \
  '          let b_s = b.match(/(.*?)(?:(\\d+)|(?:\\((\\d+)\\)))?$/);\r\n' \
  '          return (asc?1:-1) * (str_comp(a_s[1], b_s[1]) || ((a_s[2]==undefined?-1:parseInt(a_s[2])) - (b_s[2]==undefined?-1:parseInt(b_s[2]))) || ((a_s[3]==undefined?-1:parseInt(a_s[3])) - (b_s[3]==undefined?-1:parseInt(b_s[3]))));\r\n' \
  '        }\r\n' \
  '        function comp_filepath(a, b) {\r\n' \
  '          if (a == b) {return 0;}\r\n' \
  '          let a_s = a.match(/(.*(?=\\\\)|)\\\\?(.*?)(?:\\.gpx)?$/i);\r\n' \
  '          let b_s = b.match(/(.*(?=\\\\)|)\\\\?(.*?)(?:\\.gpx)?$/i);\r\n' \
  '          return (comp_name(a_s[1], b_s[1]) || comp_name(a_s[2], b_s[2]));\r\n' \
  '        }\r\n' \
  '        switch (crit) {\r\n' \
  '          case 0:\r\n' \
  '            break;\r\n' \
  '          case 1:\r\n' \
  '            vals = trks.map(function (t) {return document.getElementById("track" + t.toString() + "name").value;});\r\n' \
  '            c = function (a, b) {return comp_name(vals[a], vals[b]) || n(a, b);};\r\n' \
  '            break;\r\n' \
  '          case 2:\r\n' \
  '            vals = trks.map(function (t) {return document.getElementById("track" + t.toString() + "visible").value;});\r\n' \
  '            c = function (a, b) {return comp_filepath(vals[a], vals[b]) || n(a, b);};\r\n' \
  '            break;\r\n' \
  '          case 3:\r\n' \
  '          case 4:\r\n' \
  '          case 5:\r\n' \
  '          case 6:\r\n' \
  '          case 7:\r\n' \
  '            c = function (a, b) {return comp_flt(tracks_props[a][crit - 3], tracks_props[b][crit - 3]) || n(a, b);};\r\n' \
  '            break;\r\n' \
  '          case 8:\r\n' \
  '            let [clat, clon] = WebMercatortoWGS84(htopx + (viewpane.offsetWidth / 2 - hpx) * tscale / zoom, htopy + (hpy - viewpane.offsetHeight / 2) * tscale / zoom);\r\n' \
  '            vals = trks.map(function (t) {return (tracks_props[t][5][0]==null || tracks_props[t][5][1]==null)?NaN:distance(clat, clon, 0, tracks_props[t][5][0], tracks_props[t][5][1], 0);});\r\n' \
  '            c = function (a, b) {return comp_flt(vals[a], vals[b]) || n(a, b);};\r\n' \
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
  '        for (let f=0; f<folders.length; f++) {\r\n' \
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
  '          if (document.getElementById(focused + "cont").style.display == "none") {\r\n' \
  '            track_click(null, document.getElementById(focused + "desc"));\r\n' \
  '          } else {\r\n' \
  '            document.getElementById(focused + "desc").scrollIntoView({block:"nearest"});\r\n' \
  '            document.getElementById(focused + "focus").scrollIntoView({block:"nearest"});\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function folders_whole(tick) {\r\n' \
  '       let folders = document.getElementById("foldersform").getElementsByTagName("input");\r\n' \
  '       for (let f=0; f<folders.length; f++) {\r\n' \
  '         folders[f].checked = tick;\r\n' \
  '       }\r\n' \
  '       folders_select();\r\n' \
  '      }\r\n' \
  '      function tracks_smooth(recalc=false) {\r\n' \
  '        let drange = parseFloat(document.getElementById("dfdist").innerHTML);\r\n' \
  '        tracks_pts_smoothed = null;\r\n' \
  '        tracks_xys_smoothed = tracks_xys.slice();\r\n' \
  '        let ind = 0;\r\n' \
  '        for (let t=0; t<tracks_pts.length; t++) {\r\n' \
  '          let segs = tracks_pts[t];\r\n' \
  '          let tt = htopy - prop_to_wmvalue(document.getElementById("track" + t.toString()).style.top);\r\n' \
  '          let tdrange = drange * (Math.exp(tt / 6378137) + Math.exp(- tt / 6378137)) / 2;\r\n' \
  '          for (const seg of segs) {\r\n' \
  '            let nind = ind + seg.length;\r\n' \
  '            let dirx = null;\r\n' \
  '            let diry = null;\r\n' \
  '            let pp = null;\r\n' \
  '            for (let p=2*ind; p<2*nind; p+=2) {\r\n' \
  '              if (pp == null) {\r\n' \
  '                pp = p;\r\n' \
  '                continue;\r\n' \
  '              }\r\n' \
  '              let ndirx = 0;\r\n' \
  '              let ndiry = 0;\r\n' \
  '              let dist = 0;\r\n' \
  '              let pr = pp;\r\n' \
  '              for (let pn=p; pn<2*nind; pn+=2) {\r\n' \
  '                dist += Math.sqrt((tracks_xys_smoothed[pn] - tracks_xys_smoothed[pr]) ** 2 + (tracks_xys_smoothed[pn + 1] - tracks_xys_smoothed[pr + 1]) ** 2);\r\n' \
  '                pr = pn;\r\n' \
  '                if (dist > tdrange) {break;}\r\n' \
  '                ndirx += tracks_xys_smoothed[pn] - tracks_xys_smoothed[pp];\r\n' \
  '                ndiry += tracks_xys_smoothed[pn + 1] - tracks_xys_smoothed[pp + 1];\r\n' \
  '              }\r\n' \
  '              let ndirl = Math.sqrt(ndirx ** 2 + ndiry ** 2);\r\n' \
  '              if (ndirl > 0) {\r\n' \
  '                ndirx /= ndirl;\r\n' \
  '                ndiry /= ndirl;\r\n' \
  '                if (dirx == null) {\r\n' \
  '                  dirx = ndirx;\r\n' \
  '                  diry = ndiry;\r\n' \
  '                }\r\n' \
  '                let pdirx = tracks_xys_smoothed[p] - tracks_xys_smoothed[pp];\r\n' \
  '                let pdiry = tracks_xys_smoothed[p + 1] - tracks_xys_smoothed[pp + 1];\r\n' \
  '                let pdirl = Math.sqrt(pdirx ** 2 + pdiry ** 2);\r\n' \
  '                if (pdirl > 0) {\r\n' \
  '                  let pmod = false;\r\n' \
  '                  pdirx /= pdirl;\r\n' \
  '                  pdiry /= pdirl;\r\n' \
  '                  let nsin = dirx * ndiry - diry * ndirx;\r\n' \
  '                  let ncos = dirx * ndirx + diry * ndiry;\r\n' \
  '                  let psin = dirx * pdiry - diry * pdirx;\r\n' \
  '                  let pcos = dirx * pdirx + diry * pdiry;\r\n' \
  '                  if (nsin * psin < 0) {\r\n' \
  '                    if (pcos < 0) {\r\n' \
  '                      if (ncos < 0) {\r\n' \
  '                        pdirl = Math.min(-pdirl * pcos, -ndirl * ncos);\r\n' \
  '                        dirx = -dirx;\r\n' \
  '                        diry = -diry;\r\n' \
  '                      } else {\r\n' \
  '                        pdirl = 0;\r\n' \
  '                      }\r\n' \
  '                    }\r\n' \
  '                    tracks_xys_smoothed[p] = tracks_xys_smoothed[pp] + pdirl * dirx;\r\n' \
  '                    tracks_xys_smoothed[p + 1] = tracks_xys_smoothed[pp + 1] + pdirl * diry;\r\n' \
  '                    pmod = true;\r\n' \
  '                  } else if (ncos > pcos) {\r\n' \
  '                    pdirl = Math.max(0, pdirl * (pdirx * ndirx + pdiry * ndiry));\r\n' \
  '                    tracks_xys_smoothed[p] = tracks_xys_smoothed[pp] + pdirl * ndirx;\r\n' \
  '                    tracks_xys_smoothed[p + 1] = tracks_xys_smoothed[pp + 1] + pdirl * ndiry;\r\n' \
  '                    pmod = true;\r\n' \
  '                    dirx = ndirx;\r\n' \
  '                    diry = ndiry;\r\n' \
  '                  } else {\r\n' \
  '                    dirx = pdirx;\r\n' \
  '                    diry = pdiry;\r\n' \
  '                  }\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              pp = p;\r\n' \
  '            }\r\n' \
  '            ind = nind;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (recalc) {tracks_calc(2);}\r\n' \
  '      }\r\n' \
  '      function switch_smooth() {\r\n' \
  '        if (smoothed) {\r\n' \
  '          smoothed = false;\r\n' \
  '          document.getElementById("swsm").innerHTML = "&homtht;&homtht;"\r\n' \
  '        } else {\r\n' \
  '          smoothed = true;\r\n' \
  '          document.getElementById("swsm").innerHTML = "&divide;&divide;"\r\n' \
  '          tracks_smooth();\r\n' \
  '        }\r\n' \
  '        tracks_calc(2);\r\n' \
  '      }\r\n' \
  '      function error_trcb() {\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        document.getElementById("edit").disabled = false;\r\n' \
  '        document.getElementById("edit").style.pointerEvents = "";\r\n' \
  '        return false;\r\n' \
  '      }\r\n' \
  '      function load_tdcb(t, trk) {\r\n' \
  '        if (t.status != 200) {return error_trcb();}\r\n' \
  '        if (t.response == "") {return error_trcb();}\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        document.getElementById(trk + "file").value = t.response;\r\n' \
  '        let uri = document.getElementById(trk + "visible").value;\r\n' \
  '        document.getElementById(trk + "visible").value = uri.replace(/(.*)(\\\\.*?)$/, "$1\\\\" + t.response);\r\n' \
  '        let ind = parseInt(trk.substring(5));\r\n' \
  '        let npos = no_sort[ind];\r\n' \
  '        for (let i=0; i<tracks_pts.length; i++) {\r\n' \
  '          if (document.getElementById("track" + i.toString() + "visible").value == uri) {\r\n' \
  '            if (no_sort[i] > no_sort[ind]) {\r\n' \
  '              if (npos < no_sort[i]) {npos = no_sort[i];}\r\n' \
  '              no_sort[i]--;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        no_sort[ind] = npos;\r\n' \
  '        document.getElementById("edit").disabled = false;\r\n' \
  '        document.getElementById("edit").style.pointerEvents = "";\r\n' \
  '        tracks_sort();\r\n' \
  '        return true;\r\n' \
  '      }\r\n' \
  '      function track_detach() {\r\n' \
  '        if (document.getElementById("edit").disabled) {return;}\r\n' \
  '        let foc = focused;\r\n' \
  '        if (foc == "") {return;}\r\n' \
  '        let ind = parseInt(foc.substring(5));\r\n' \
  '        let uri = document.getElementById("track" + ind.toString() + "visible").value;\r\n' \
  '        let mt = false;\r\n' \
  '        for (let i=0; i<tracks_pts.length; i++) {\r\n' \
  '          if (i != ind && document.getElementById("track" + i.toString() + "visible").value == uri) {mt = true; break;}\r\n' \
  '        }\r\n' \
  '        if (! mt) {show_msg("{#jmdetach4#}", 10); return;}\r\n' \
  '        document.getElementById("edit").disabled = true;\r\n' \
  '        document.getElementById("edit").style.pointerEvents = "none";\r\n' \
  '        let msgn = show_msg("{#jmdetach1#}", 0);\r\n' \
  '        xhrtr.onload = (e) => {load_tdcb(e.target, foc)?show_msg("{#jmdetach2#}", 5, msgn):show_msg("{#jmdetach3#}", 10, msgn);};\r\n' \
  '        xhrtr.onerror = (e) => {error_trcb(); show_msg("{#jmdetach3#}", 10, msgn);};\r\n' \
  '        xhrtr.open("GET", "/detach?" + foc.substring(5));\r\n' \
  '        xhrtr.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhr_ongoing++;\r\n' \
  '        xhrtr.send();\r\n' \
  '      }\r\n' \
  '      function load_ticb(t, ind1, ind2) {\r\n' \
  '        if (t.status != 200) {return error_trcb();}\r\n' \
  '        if (t.response == "") {return error_trcb();}\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        let foc = focused;\r\n' \
  '        if (focused) {track_click(null, document.getElementById(focused + "desc"));}\r\n' \
  '        let msg = JSON.parse(t.response);\r\n' \
  '        for (let n in msg) {\r\n' \
  '          let ch = null;\r\n' \
  '          if (n.indexOf("cont") >= 0) {\r\n' \
  '            ch = document.getElementById(n.replace("cont", "visible")).checked;\r\n' \
  '          } else {\r\n' \
  '            ch = document.getElementById(n).style.display;\r\n' \
  '          }\r\n' \
  '          document.getElementById(n).outerHTML = msg[n];\r\n' \
  '          if (n.indexOf("cont") >= 0) {\r\n' \
  '            document.getElementById(n.replace("cont", "visible")).checked = ch;\r\n' \
  '          } else {\r\n' \
  '            document.getElementById(n).style.display = ch;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (t.responseURL.indexOf("incorporate") >= 0) {\r\n' \
  '          tracks_pts[ind1] = tracks_pts[ind1].concat(tracks_pts[ind2]);\r\n' \
  '        } else {\r\n' \
  '          for (let i=0; i<tracks_pts.length; i++) {\r\n' \
  '            if (no_sort[i] > no_sort[ind1] && no_sort[i] < no_sort[ind2]) {no_sort[i]++;}\r\n' \
  '            if (no_sort[i] < no_sort[ind1] && no_sort[i] > no_sort[ind2]) {no_sort[i]--;}\r\n' \
  '          }\r\n' \
  '          if (t.responseURL.indexOf("before") >= 0) {\r\n' \
  '            if (no_sort[ind2] < no_sort[ind1]) {\r\n' \
  '              no_sort[ind2] = no_sort[ind1] - 1;\r\n' \
  '            } else {\r\n' \
  '              no_sort[ind2] = no_sort[ind1];\r\n' \
  '              no_sort[ind1]++;\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            if (no_sort[ind2] < no_sort[ind1]) {\r\n' \
  '              no_sort[ind2] = no_sort[ind1];\r\n' \
  '              no_sort[ind1]--;\r\n' \
  '            } else {\r\n' \
  '              no_sort[ind2] = no_sort[ind1] + 1;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        track_click(null, document.getElementById("track" + ind1.toString() + "desc"));\r\n' \
  '        tracks_calc(0);\r\n' \
  '        document.getElementById("edit").disabled = false;\r\n' \
  '        document.getElementById("edit").style.pointerEvents = "";\r\n' \
  '        tracks_sort();\r\n' \
  '        return true;\r\n' \
  '      }\r\n' \
  '      function track_incorporate_integrate(after=null) {\r\n' \
  '        if (document.getElementById("edit").disabled) {return;}\r\n' \
  '        let foc = focused;\r\n' \
  '        if (foc == "") {return;}\r\n' \
  '        let ind1 = parseInt(foc.substring(5));\r\n' \
  '        let ind2 = null;\r\n' \
  '        let trks = document.getElementById("tracksform").children;\r\n' \
  '        for (let t=0; t<trks.length; t++) {\r\n' \
  '          if (t == ind1) {continue;}\r\n' \
  '          let tr = document.getElementById("track" + t.toString() + "cont");\r\n' \
  '          if (! tr.firstElementChild.checked || tr.style.display == "none") {continue;}\r\n' \
  '          if (ind2 != null) {show_msg(after==null?"{#jmincorporate4#}":"{#jmintegrate4#}", 10); return;}\r\n' \
  '          ind2 = t;\r\n' \
  '        }\r\n' \
  '        if (ind2 == null) {show_msg(after==null?"{#jmincorporate4#}":"{#jmintegrate4#}", 10); return;}\r\n' \
  '        if (after != null) {\r\n' \
  '          let uri = document.getElementById("track" + ind2.toString() + "visible").value;\r\n' \
  '          for (let i=0; i<tracks_pts.length; i++) {\r\n' \
  '            if (i != ind2 && document.getElementById("track" + i.toString() + "visible").value == uri) {show_msg("{#jmintegrate5#}", 10); return;}\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        document.getElementById("edit").disabled = true;\r\n' \
  '        document.getElementById("edit").style.pointerEvents = "none";\r\n' \
  '        let msgn = show_msg(after==null?"{#jmincorporate1#}":"{#jmintegrate1#}", 0);\r\n' \
  '        xhrtr.onload = (e) => {load_ticb(e.target, ind1, ind2)?show_msg(after==null?"{#jmincorporate2#}":"{#jmintegrate2#}", 5, msgn):show_msg(after==null?"{#jmincorporate3#}":"{#jmintegrate3#}", 10, msgn);};\r\n' \
  '        xhrtr.onerror = (e) => {error_trcb(); show_msg(after==null?"{#jmincorporate3#}":"{#jmintegrate3#}", 10, msgn);};\r\n' \
  '        xhrtr.open("GET", (after==null?"/incorporate?":("/integrate" + (after?"after?":"before?"))) + ind1.toString() + "," + ind2.toString());\r\n' \
  '        xhrtr.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhr_ongoing++;\r\n' \
  '        xhrtr.send();\r\n' \
  '      }\r\n' \
  '      function load_tncb(t) {\r\n' \
  '        if (t.status != 200) {return error_trcb();}\r\n' \
  '        if (t.response == "") {return error_trcb();}\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        if (focused) {track_click(null, document.getElementById(focused + "desc"));}\r\n' \
  '        let msg = JSON.parse(t.response);\r\n' \
  '        for (let n in msg) {\r\n' \
  '          if (n.indexOf("cont") >= 0) {\r\n' \
  '            let e = document.createElement("span");\r\n' \
  '            document.getElementById("tracksform").appendChild(e);\r\n' \
  '            e.outerHTML = msg[n];\r\n' \
  '          } else if (n.indexOf("track") >= 0) {\r\n' \
  '            let e = document.createElementNS("http://www.w3.org/2000/svg", "svg");\r\n' \
  '            let w = document.getElementById("waydots0");\r\n' \
  '            document.getElementById("handle").insertBefore(e, w);\r\n' \
  '            e.outerHTML = w==null?msg[n]:(msg[n].substring(2)+"  ");\r\n' \
  '          } else {\r\n' \
  '            let e = document.createElementNS("http://www.w3.org/2000/svg", "svg");\r\n' \
  '            document.getElementById("handle").appendChild(e);\r\n' \
  '            e.outerHTML = msg[n];\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        document.getElementById("tracks").firstChild.textContent = document.getElementById("tracks").firstChild.textContent.replace(/\\d+/, (tracks_pts.length + 1).toString());\r\n' \
  '        no_sort.push(tracks_pts.length);\r\n' \
  '        tracks_pts.push([]);\r\n' \
  '        tracks_stats.push([]);\r\n' \
  '        tracks_props.push([NaN, NaN, NaN, NaN, NaN, [NaN, NaN]]);\r\n' \
  '        document.getElementById("edit").disabled = false;\r\n' \
  '        document.getElementById("edit").style.pointerEvents = "";\r\n' \
  '        document.getElementById("tracksfilter").value = "";\r\n' \
  '        tracks_sort();\r\n' \
  '        tracks_filter();\r\n' \
  '        track_click(null, document.getElementById("track" + (tracks_pts.length - 1).toString() + "desc"));\r\n' \
  '        return true;\r\n' \
  '      }\r\n' \
  '      function track_new() {\r\n' \
  '        if (document.getElementById("edit").disabled) {return;}\r\n' \
  '        let folders = document.getElementById("foldersform").getElementsByTagName("input");\r\n' \
  '        let t = 0;\r\n' \
  '        let f_ind = null;\r\n' \
  '        for (let f=0; f<folders.length; f++) {\r\n' \
  '          if (folders[f].checked) {\r\n' \
  '            f_ind = f;\r\n' \
  '            break;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (f_ind == null) {return;}\r\n' \
  '        document.getElementById("edit").disabled = true;\r\n' \
  '        document.getElementById("edit").style.pointerEvents = "none";\r\n' \
  '        let msgn = show_msg("{#jmnew1#}", 0);\r\n' \
  '        xhrtr.onload = (e) => {load_tncb(e.target)?show_msg("{#jmnew2#}", 5, msgn):show_msg("{#jmdetach3#}", 10, msgn);};\r\n' \
  '        xhrtr.onerror = (e) => {error_trcb(); show_msg("{#jmnew3#}", 10, msgn);};\r\n' \
  '        xhrtr.open("GET", "/new?" + f_ind.toString());\r\n' \
  '        xhrtr.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhr_ongoing++;\r\n' \
  '        xhrtr.send();\r\n' \
  '      }\r\n' \
  '      function track_edit() {\r\n' \
  '        if (focused == "") {return;}\r\n' \
  '        window.location.assign(window.location.href.replace("/GPXExplorer.html", "/edit?" + focused.substring(5) + "," + ((viewpane.offsetWidth / 2 - hpx) * tscale / zoom + htopx).toString() + "|" + (htopy - (viewpane.offsetHeight / 2 - hpy) * tscale / zoom).toString()));\r\n' \
  '      }\r\n' \
  '      function open_webmapping() {\r\n' \
  '        let wmsel = document.getElementById("iset");\r\n' \
  '        if (focused == "" || wmsel.options.length == 0 || wmsel.selectedIndex < 0) {return;}\r\n' \
  '        let c = tracks_props[parseInt(focused.substring(5))][5];\r\n' \
  '        if (isNaN(c[0]) || isNaN(c[1])) {return;}\r\n' \
  '        window.open(wmsel.options[wmsel.selectedIndex].value.replace("{lat}", c[0].toString()).replace("{lon}", c[1].toString()));\r\n' \
  '      }\r\n' \
  '      function switch_mtpanel() {\r\n' \
  '        if (document.getElementById("mtpanel").style.display != "initial") {\r\n' \
  '          document.getElementById("mtpanel").style.display = "initial";\r\n' \
  '        } else {\r\n' \
  '          document.getElementById("mtpanel").style.display = "none";\r\n' \
  '        }\r\n' \
  '        for (let fp of [document.getElementById("filterpanel1"), document.getElementById("filterpanel2"), document.getElementById("filterpanel3")]) {fp.style.display = "none";}\r\n' \
  '        document.getElementById("v3Dpanel").style.display = "none";\r\n' \
  '      }\r\n' \
  '      function error_mcb() {\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        if (document.getElementById("mediapreview").style.display != "none") {switch_mediapreview();}\r\n' \
  '        return false;\r\n' \
  '      }\r\n' \
  '      function load_mcb(t) {\r\n' \
  '        if (t.status != 200) {return error_mcb();}\r\n' \
  '        if (t.response == "") {return error_mcb();}\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        if (t.responseURL.indexOf("gps_ar") > 0) {\r\n' \
  '          media_gps_ar = new Float64Array(t.response);\r\n' \
  '          media_corners = new Float64Array(media_gps_ar.length / 3 * 4);\r\n' \
  '        } else {\r\n' \
  '          media_uri_dt = t.response.split("|");\r\n' \
  '          let rv = RegExp(/\\.mp4($|\\r)/, "i");\r\n' \
  '          media_isvid = media_uri_dt.map((s) => rv.test(s));\r\n' \
  '        }\r\n' \
  '        show_media();\r\n' \
  '        return true;\r\n' \
  '      }\r\n' \
  '      function media_process() {\r\n' \
  '        let nm = media_gps_ar.length / 3;\r\n' \
  '        media_sides = [];\r\n' \
  '        let zf = zoom / tscale;\r\n' \
  '        let ts = parseFloat(document.getElementById("mtsize").innerHTML) / 2;\r\n' \
  '        for (let m=0; m<nm; m++) {\r\n' \
  '          let mx = (media_gps_ar[3 * m] - htopx) * zf;\r\n' \
  '          let my = (htopy - media_gps_ar[3 * m + 1]) * zf;\r\n' \
  '          let mr = media_gps_ar[3 * m + 2];\r\n' \
  '          if (mr >= 1) {\r\n' \
  '            media_corners.set([mx - ts, my - ts / mr, mx + ts, my + ts / mr], 4 * m);\r\n' \
  '          } else {\r\n' \
  '            media_corners.set([mx - ts * mr, my - ts, mx + ts * mr, my + ts], 4 * m);\r\n' \
  '          }\r\n' \
  '          media_sides.push({"o":0, "m":m}, {"o":2, "m":m});\r\n' \
  '        }\r\n' \
  '        media_sides.sort((a, b) => (media_corners[4 * a.m + a.o] - media_corners[4 * b.m + b.o]) || (b.o - a.o) || (media_corners[4 * a.m + 1] - media_corners[4 * b.m + 1]) || (media_corners[4 * a.m + 3] - media_corners[4 * b.m + 3]));\r\n' \
  '        media_corners_updated = true;\r\n' \
  '      }\r\n' \
  '      function media_gen() {\r\n' \
  '        media_div = document.createElement("div");\r\n' \
  '        media_div.id = "geomedia";\r\n' \
  '        media_div.setAttribute("onmousedown", "event.stopPropagation();event.preventDefault();");\r\n' \
  '        media_div.setAttribute("onclick", "event.stopPropagation();event.preventDefault();enlarge_media(event.target.id.substring(6));");\r\n' \
  '        media_div.setAttribute("oncontextmenu", "event.stopPropagation();event.preventDefault();");\r\n' \
  '        let nm = media_corners.length / 4;\r\n' \
  '        let md = Array(nm);\r\n' \
  '        md.fill([]);\r\n' \
  '        let cs = [];\r\n' \
  '        let xl = -hpx;\r\n' \
  '        let xr = xl + viewpane.offsetWidth;\r\n' \
  '        let yt = -hpy;\r\n' \
  '        let yb = yt + viewpane.offsetHeight;\r\n' \
  '        for (let l of media_sides) {\r\n' \
  '          let m = l.m;\r\n' \
  '          if (md[m] == null) {continue;}\r\n' \
  '          if (md[m].length == 0 && (media_corners[4 * m] >= xr || media_corners[4 * m + 2] <= xl || media_corners[4 * m + 1] >= yb || media_corners[4 * m + 3] <= yt)) {\r\n' \
  '            md[m] = null;\r\n' \
  '            continue;\r\n' \
  '          }\r\n' \
  '          let s1 = 0;\r\n' \
  '          let s2 = cs.length - 1;\r\n' \
  '          if (s2 < 0) {\r\n' \
  '            md[m] = [m];\r\n' \
  '            cs.push(m);\r\n' \
  '            continue;\r\n' \
  '          }\r\n' \
  '          let mb = media_corners[4 * m + 3];\r\n' \
  '          if (mb <= media_corners[4 * cs[0] + 1]) {\r\n' \
  '            md[m] = [m];\r\n' \
  '            cs.splice(0, 0, m);\r\n' \
  '            continue;\r\n' \
  '          }\r\n' \
  '          let s0 = s2;\r\n' \
  '          if (mb <= media_corners[4 * cs[s2] + 1]) {\r\n' \
  '            while (true) {\r\n' \
  '              s0 = Math.floor((s1 + s2) / 2);\r\n' \
  '              if (s0 == s1) {break}\r\n' \
  '              if (mb <= media_corners[4 * cs[s0] + 1]) {s2 = s0} else {s1 = s0}\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (md[m].length > 0) {\r\n' \
  '            cs.splice(s0, 1);\r\n' \
  '            continue;\r\n' \
  '          }\r\n' \
  '          if (media_corners[4 * m + 1] >= media_corners[4 * cs[s0] + 3]) {\r\n' \
  '            md[m] = [m];\r\n' \
  '            cs.splice(s0 + 1, 0, m);\r\n' \
  '          } else {\r\n' \
  '            md[m] = null;\r\n' \
  '            md[cs[s0]].push(m);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        let media_ex_hold = media_hold;\r\n' \
  '        media_hold = new Object;\r\n' \
  '        [xl, xr] = [2 * xl - xr, 2 * xr - xl];\r\n' \
  '        [yt, yb] = [2 * yt - yb, 2 * yb - yt];\r\n' \
  '        if (media_ex_hold) {\r\n' \
  '          for (const m in media_ex_hold) {\r\n' \
  '            if (md[m] || (media_corners[4 * m] < xr && media_corners[4 * m + 2] > xl && media_corners[4 * m + 1] < yb && media_corners[4 * m + 3] > yt)) {\r\n' \
  '              let med = media_ex_hold[m];\r\n' \
  '              if (! (media_isvid[m]?med.videoWidth:med.naturalWidth)) {continue;}\r\n' \
  '              if (media_corners_updated) {\r\n' \
  '                med.style.width = (media_corners[4 * m + 2] - media_corners[4 * m]).toString() + "px";\r\n' \
  '                med.style.height = (media_corners[4 * m + 3] - media_corners[4 * m + 1]).toString() + "px";\r\n' \
  '                med.style.left = media_corners[4 * m].toString() + "px";\r\n' \
  '                med.style.top = media_corners[4 * m + 1].toString() + "px";\r\n' \
  '              }\r\n' \
  '              media_hold[m] = med;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        for (let m=0; m<nm; m++) {\r\n' \
  '          if (md[m] == null) {continue;}\r\n' \
  '          let med = media_hold[m];\r\n' \
  '          if (! med) {\r\n' \
  '            med = document.createElement(media_isvid[m]?"video":"img");\r\n' \
  '            let port = mportmin + m % (mportmax + 1 - mportmin);\r\n' \
  '            if (media_isvid[m]) {med.preload = "metadata"};\r\n' \
  '            med.src = "http://" + host + port.toString() + "/media?" + m.toString();\r\n' \
  '            med.alt = "";\r\n' \
  '            med.style.position = "absolute";\r\n' \
  '            med.style.width = (media_corners[4 * m + 2] - media_corners[4 * m]).toString() + "px";\r\n' \
  '            med.style.height = (media_corners[4 * m + 3] - media_corners[4 * m + 1]).toString() + "px";\r\n' \
  '            med.style.left = media_corners[4 * m].toString() + "px";\r\n' \
  '            med.style.top = media_corners[4 * m + 1].toString() + "px";\r\n' \
  '            media_hold[m] = med;\r\n' \
  '          }\r\n' \
  '          med.id = "media-" + md[m].toString();\r\n' \
  '          med.title = media_uri_dt[m] + ((md[m].length > 1)?("\\r\\n\\r\\n+ " + (md[m].length - 1).toString() + " …"):"");\r\n' \
  '          media_div.appendChild(med);\r\n' \
  '        }\r\n' \
  '        media_corners_updated = false;\r\n' \
  '      }\r\n' \
  '      function show_media() {\r\n' \
  '        document.getElementById("switchmedia").disabled = true;\r\n' \
  '        document.getElementById("switchmedia").style.pointerEvents = "none";\r\n' \
  '        if (media_gps_ar == null) {\r\n' \
  '          media_gps_ar = [];\r\n' \
  '          let xhrp = new XMLHttpRequest();\r\n' \
  '          let msgn = show_msg("{#jmmedia1#}", 0);\r\n' \
  '          xhrp.onload = (e) => {load_mcb(e.target)?show_msg("{#jmmedia1#}", 0.1, msgn):show_msg("{#jmmedia3#}", 10, msgn);};\r\n' \
  '          xhrp.onerror = (e) => {error_mcb(); show_msg("{#jmmedia3#}", 10, msgn);};\r\n' \
  '          xhrp.open("GET", "/media/gps_ar");\r\n' \
  '          xhrp.responseType = "arraybuffer";\r\n' \
  '          xhrp.setRequestHeader("If-Match", sessionid);\r\n' \
  '          xhr_ongoing++;\r\n' \
  '          xhrp.send();\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (media_gps_ar.length == 0) {return;}\r\n' \
  '        if (media_uri_dt == null) {\r\n' \
  '          media_uri_dt = [];\r\n' \
  '          let xhrp = new XMLHttpRequest();\r\n' \
  '          let msgn = show_msg("{#jmmedia1#}", 0);\r\n' \
  '          xhrp.onload = (e) => {load_mcb(e.target)?show_msg("{#jmmedia2#}", 2, msgn):show_msg("{#jmmedia3#}", 10, msgn);};\r\n' \
  '          xhrp.onerror = (e) => {error_mcb(); show_msg("{#jmmedia3#}", 10, msgn);};\r\n' \
  '          xhrp.open("GET", "/media/uri_dt");\r\n' \
  '          xhrp.setRequestHeader("If-Match", sessionid);\r\n' \
  '          xhr_ongoing++;\r\n' \
  '          xhrp.send();\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        if (media_sides == null) {media_process();}\r\n' \
  '        if (media_div == null) {media_gen();}\r\n' \
  '        let svgs = document.getElementById("handle").getElementsByTagName("svg");\r\n' \
  '        let ref = null;\r\n' \
  '        if (svgs.length > 0) {ref = svgs[0];}\r\n' \
  '        svgs = null;\r\n' \
  '        document.getElementById("handle").insertBefore(media_div, ref);\r\n' \
  '        media_visible = true;\r\n' \
  '        document.getElementById("switchmedia").disabled = false;\r\n' \
  '        document.getElementById("switchmedia").style.pointerEvents = "";\r\n' \
  '      }\r\n' \
  '      function hide_media(reset="") {\r\n' \
  '        if (reset) {media_div = null;}\r\n' \
  '        if (reset == "s") {media_sides = null;}\r\n' \
  '        if (! media_visible) {\r\n' \
  '          if (! media_ex_visible) {media_hold = null;}\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        let mdiv = document.getElementById("geomedia");\r\n' \
  '        if (mdiv != null) {document.getElementById("handle").removeChild(mdiv);}\r\n' \
  '        if (reset) {document.getElementById("mediapreview").innerHTML = "";}\r\n' \
  '        media_visible = false;\r\n' \
  '      }\r\n' \
  '      function update_media() {\r\n' \
  '        let mvis = media_visible;\r\n' \
  '        hide_media("s");\r\n' \
  '        if (mvis) {show_media();}\r\n' \
  '      }\r\n' \
  '      function show_hide_media() {\r\n' \
  '        if (media_visible) {\r\n' \
  '          hide_media();\r\n' \
  '          if (document.getElementById("mediapreview").style.display != "none") {switch_mediapreview();}\r\n' \
  '        } else {\r\n' \
  '          show_media();\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function enlarge_media(mids) {\r\n' \
  '        let mview = document.getElementById("mediapreview");\r\n' \
  '        if (mview.style.display == "none") {\r\n' \
  '          mview = document.getElementById("mediaview");\r\n' \
  '          mview.style.display = "block";\r\n' \
  '        }\r\n' \
  '        mview.innerHTML = "";\r\n' \
  '        mview.dataset.sl = "0";\r\n' \
  '        for (let m of mids.split(",")) {\r\n' \
  '          let med = document.createElement(media_isvid[m]?"video":"img");\r\n' \
  '          let port = mportmin + m % (mportmax + 1 - mportmin);\r\n' \
  '          if (media_isvid[m]) {\r\n' \
  '            med.preload = "metadata";\r\n' \
  '            med.controls = true;\r\n' \
  '            med.loop = true;\r\n' \
  '            med.playsinline = true;\r\n' \
  '          } else {\r\n' \
  '            med.setAttribute("onclick", "photo_fs(this)");\r\n' \
  '          }\r\n' \
  '          med.src = "http://" + host + port.toString() + "/media?" + m.toString();\r\n' \
  '          med.title = media_uri_dt[m];\r\n' \
  '          mview.appendChild(med);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function photo_fs(p) {\r\n' \
  '        if (document.fullscreenElement) {document.exitFullscreen();} else {p.requestFullscreen();}\r\n' \
  '      }\r\n' \
  '      function switch_mediapreview(graph=false) {\r\n' \
  '        let mpview = document.getElementById("mediapreview");\r\n' \
  '        if (mpview.style.display == "none") {\r\n' \
  '          if (graph) {return;}\r\n' \
  '          document.getElementById("graph").style.display = "none";\r\n' \
  '          document.getElementById("content").style.height = "calc(74vh - 2.4em - 18px)";\r\n' \
  '          viewpane.style.height = "calc(74vh - 2.4em - 18px)";\r\n' \
  '          mpview.dataset.sl = "0";\r\n' \
  '          mpview.style.display = "block";\r\n' \
  '          rescale();\r\n' \
  '          if (! media_visible) {show_media();}\r\n' \
  '        } else {\r\n' \
  '          mpview.innerHTML = "";\r\n' \
  '          mpview.style.display = "none";\r\n' \
  '          mpview.dataset.sl = "0";\r\n' \
  '          if (! graph) {\r\n' \
  '            document.getElementById("content").style.height = "calc(99vh - 2.4em - 16px)";\r\n' \
  '            viewpane.style.height = "calc(99vh - 2.4em - 16px)";\r\n' \
  '            rescale();\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function close_mediaview(e) {\r\n' \
  '        if (document.fullscreenElement) {\r\n' \
  '          window.onresize = (e) => {document.getElementById("mediaview").innerHTML = ""; window.onresize = window_resize; window_resize();};\r\n' \
  '          document.exitFullscreen();\r\n' \
  '        } else {\r\n' \
  '          document.getElementById("mediaview").innerHTML = "";\r\n' \
  '        }\r\n' \
  '        document.getElementById("mediaview").style.display = "none";\r\n' \
  '        document.getElementById("mediaview").dataset.sl = "0";\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '      }\r\n' \
  '      async function download_map() {\r\n' \
  '        if (document.getElementById("tset").disabled || document.getElementById("edit").disabled) {return;}\r\n' \
  '        let b = track_boundaries();\r\n' \
  '        if (b == null) {return;}\r\n' \
  '        let cwidth = Math.ceil((b[1] - b[0]) / tscale * zoom);\r\n' \
  '        let cheight = Math.ceil((b[3] - b[2]) / tscale * zoom);\r\n' \
  '        if (cwidth > 11000 || cheight > 11000) {\r\n' \
  '          show_msg("{#jmdownmap7#}", 10);\r\n' \
  '          return;\r\n' \
  '        }\r\n' \
  '        document.getElementById("tset").disabled = true;\r\n' \
  '        document.getElementById("tset").style.pointerEvents = "none";\r\n' \
  '        let msgn = show_msg("{#jmdownmap1#}", 0);\r\n' \
  '        let mcnv2d = document.createElement("canvas");\r\n' \
  '        let ctx = mcnv2d.getContext("2d");\r\n' \
  '        mcnv2d.width = cwidth;\r\n' \
  '        mcnv2d.height = cheight;\r\n' \
  '        ctx.globalCompositeOperation = "source-over";\r\n' \
  '        ctx.fillStyle = "rgb(40,45,50)";\r\n' \
  '        ctx.fillRect(0, 0, mcnv2d.width, mcnv2d.height);\r\n' \
  '        let prom_res = null;\r\n' \
  '        let prom = null;\r\n' \
  '        let prom_c = null;\r\n' \
  '        if (mode == "map") {\r\n' \
  '          let vleft = (b[0] + htopx - ttopx) / tscale;\r\n' \
  '          let vtop = (ttopy - htopy + b[2]) / tscale;\r\n' \
  '          let vright = (b[1] + htopx - ttopx) / tscale;\r\n' \
  '          let vbottom = (ttopy - htopy + b[3]) / tscale;\r\n' \
  '          let rleft = parseInt(vleft / twidth);\r\n' \
  '          let rright = parseInt(vright / twidth);\r\n' \
  '          let rtop = parseInt(vtop / theight);\r\n' \
  '          let rbottom = parseInt(vbottom / theight);\r\n' \
  '          prom = new Promise(function(resolve, reject) {prom_res = resolve;});\r\n' \
  '          prom_c = (rbottom - rtop + 1) * (rright - rleft + 1);\r\n' \
  '          let tile = new Image();\r\n' \
  '          tile.onload = function (e) {ctx.drawImage(tile, Math.round(- vleft * zoom), Math.round(- vtop * zoom), Math.round((twidth - vleft) * zoom) - Math.round(- vleft * zoom), Math.round((theight - vtop) * zoom) - Math.round(- vtop * zoom)); prom_res();};\r\n' \
  '          tile.onerror = function (e) {prom_res();};\r\n' \
  '          tile.src = "/map/map" + text;\r\n' \
  '          await prom;\r\n' \
  '        } else {\r\n' \
  '          for (let l=0; l<layers.length; l++) {\r\n' \
  '            let layer = layers[l];\r\n' \
  '            tmatrix = layer.matrix;\r\n' \
  '            ttopx = layer.topx;\r\n' \
  '            ttopy = layer.topy;\r\n' \
  '            twidth = layer.width;\r\n' \
  '            theight = layer.height;\r\n' \
  '            text = layer.ext;\r\n' \
  '            if (twidth == 0 || theight == 0) {continue;}\r\n' \
  '            let vleft = (b[0] + htopx - ttopx) / tscale;\r\n' \
  '            let vtop = (ttopy - htopy + b[2]) / tscale;\r\n' \
  '            let vright = (b[1] + htopx - ttopx) / tscale;\r\n' \
  '            let vbottom = (ttopy - htopy + b[3]) / tscale;\r\n' \
  '            let rleft = parseInt(vleft / twidth);\r\n' \
  '            let rright = parseInt(vright / twidth);\r\n' \
  '            let rtop = parseInt(vtop / theight);\r\n' \
  '            let rbottom = parseInt(vbottom / theight);\r\n' \
  '            if (tlayers.has(tset)) {\r\n' \
  '              ctx.globalAlpha = parseFloat(opacities.get(tset)[l]);\r\n' \
  '              if (tlayers.get(tset)[l][1].indexOf("x") >= 0) {\r\n' \
  '                ctx.globalCompositeOperation = "multiply";\r\n' \
  '              } else {\r\n' \
  '                ctx.globalCompositeOperation = "source-over";\r\n' \
  '              }\r\n' \
  '            }\r\n' \
  '            prom = new Promise(function(resolve, reject) {prom_res = resolve;});\r\n' \
  '            if (text == ".json") {\r\n' \
  '              if (tmaplibre != true) {continue;}\r\n' \
  '              let cjdiv = document.createElement("div");\r\n' \
  '              cjdiv.style.visibility = "hidden";\r\n' \
  '              cjdiv.style.position = "absolute";\r\n' \
  '              cjdiv.style.top = "0px";\r\n' \
  '              cjdiv.style.left = "0px";\r\n' \
  '              cjdiv.style.maxHeight = "10px";\r\n' \
  '              cjdiv.style.maxWidth = "10px";\r\n' \
  '              cjdiv.style.overflow = "hidden";\r\n' \
  '              let jdiv = document.createElement("div");\r\n' \
  '              cjdiv.appendChild(jdiv);\r\n' \
  '              document.body.append(cjdiv);\r\n' \
  '              jdiv.style.width = (cwidth / zoom).toString() + "px";\r\n' \
  '              jdiv.style.height = (cheight / zoom).toString() + "px";\r\n' \
  '              jdiv.backgroundColor = "rgba(0,0,0,0)";\r\n' \
  '              let [lat, lon] = WebMercatortoWGS84((b[0] + b[1]) / 2 + htopx, -(b[2] + b[3]) / 2 + htopy);\r\n' \
  '              let jmap = null;\r\n' \
  '              try {\r\n' \
  '                jmap = new maplibregl.Map({container: jdiv, interactive: false, attributionControl: false, trackResize: false, renderWorldCopies: false, preserveDrawingBuffer: true, pixelRatio: zoom, style: "jsontiles/style/" + (tlayers.has(tset)?tlayers.get(tset)[l][0]:tset).toString() + "/style.json", center: [lon, lat], zoom: parseInt(document.getElementById("matrix").innerHTML) - 1});\r\n' \
  '              } catch(error) {\r\n' \
  '                continue;\r\n' \
  '              }\r\n' \
  '              jmap.once("load", (e) => {ctx.drawImage(jmap.getCanvas(), 0, 0, cwidth, cheight); prom_res();});\r\n' \
  '              await prom;\r\n' \
  '              prom = new Promise(function(resolve, reject) {prom_res = resolve;});\r\n' \
  '              jmap.once("idle", (e) => {ctx.drawImage(jmap.getCanvas(), 0, 0, cwidth, cheight); prom_res();});\r\n' \
  '              await prom;\r\n' \
  '              jmap.remove();\r\n' \
  '              document.body.removeChild(cjdiv);\r\n' \
  '            } else {\r\n' \
  '              prom_c = (rbottom - rtop + 1) * (rright - rleft + 1);\r\n' \
  '              let tsuf = text + "?" + (tlayers.has(tset)?tlayers.get(tset)[l][0]:document.getElementById("tset").selectedIndex).toString() + "," + tmatrix;\r\n' \
  '              for (let row=rtop; row<=rbottom; row++) {\r\n' \
  '                for (let col=rleft; col<=rright; col++) {\r\n' \
  '                  let tile = new Image();\r\n' \
  '                  tile.onload = function (e) {ctx.drawImage(tile, Math.round((col * twidth - vleft) * zoom), Math.round((row * theight - vtop) * zoom), Math.round(((col + 1) * twidth - vleft) * zoom) - Math.round((col * twidth - vleft) * zoom), Math.round(((row + 1) * theight - vtop) * zoom) - Math.round((row * theight - vtop) * zoom)); prom_c--; if (prom_c == 0) {prom_res();};};\r\n' \
  '                  tile.onerror = function (e) {prom_c--; if (prom_c == 0) {prom_res();};};\r\n' \
  '                  tile.crossOrigin = "anonymous";\r\n' \
  '                  tile.src = "http://" + host + (portmin + (row + col) % (portmax + 1 - portmin)).toString() + "/tiles/tile-" + row.toString() + "-" + col.toString() + tsuf;\r\n' \
  '                }\r\n' \
  '              }\r\n' \
  '              await prom;\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (tlayers.has(tset)) {ctx.globalAlpha = 1;}\r\n' \
  '        }\r\n' \
  '        msgn = show_msg("{#jmdownmap2#}", 0, msgn);\r\n' \
  '        let xs = new XMLSerializer;\r\n' \
  '        let trks = document.getElementById("tracksform").children;\r\n' \
  '        let trdata = [];\r\n' \
  '        for (let t=0; t<trks.length; t++) {\r\n' \
  '          if (trks[t].firstElementChild.checked) {\r\n' \
  '            let trkid = trks[t].id.slice(5,-4);\r\n' \
  '            let trck = document.getElementById("track" + trkid);\r\n' \
  '            let wpt = document.getElementById("waydots" + trkid);\r\n' \
  '            let tcs = getComputedStyle(trck);\r\n' \
  '            let pcs = getComputedStyle(document.getElementById("path" + trkid));\r\n' \
  '            let acs = getComputedStyle(document.getElementById("patharrows" + trkid));\r\n' \
  '            let wcs = getComputedStyle(wpt);\r\n' \
  '            trdata.push([Math.round((prop_to_wmvalue(trck.style.left) - b[0]) * zoom / tscale), Math.round((prop_to_wmvalue(trck.style.top) - b[2]) * zoom / tscale), URL.createObjectURL(new Blob([xs.serializeToString(trck).replace(/^(.*?)style=".*?"(.*?path id=.*?) (d=.*?<text id=.*?) (dy=.*?<textPath) (href=)/is, "$1width=\\"" + tcs["width"].replace("px", "") + "\\" height=\\"" + tcs["height"].replace("px", "") + "\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\"$2 fill=\\"none\\" vector-effect=\\"non-scaling-stroke\\" stroke-width=\\"" + pcs["stroke-width"].replace("px", "") + "\\" $3 stroke-width=\\"" + acs["stroke-width"].replace("px", "") + "\\" font-size=\\"" + acs["font-size"].replace("px", "") + "\\" word-spacing=\\"" + acs["word-spacing"].replace("px", "") + "\\" $4 vector-effect=\\"non-scaling-stroke\\" $5")], {type: "image/svg+xml"})), Math.round((prop_to_wmvalue(wpt.style.left) - b[0]) * zoom / tscale), Math.round((prop_to_wmvalue(wpt.style.top) - b[2]) * zoom / tscale), URL.createObjectURL(new Blob([xs.serializeToString(wpt).replace(/^(.*?)style=".*?"/is, "$1width=\\"" + tcs["width"].replace("px", "") + "\\" height=\\"" + tcs["height"].replace("px", "") + "\\" stroke=\\"none\\"").replaceAll("<circle", "<circle r=\\"" + (parseFloat(wcs["stroke-width"].replace("px", "")) * 1.5).toString() + "\\"")], {type: "image/svg+xml"})), URL.createObjectURL(new Blob([xs.serializeToString(wpt).replace(/^(.*?)fill=".*?"/is, "$1width=\\"" + tcs["width"].replace("px", "") + "\\" height=\\"" + tcs["height"].replace("px", "") + "\\" fill=\\"black\\" stroke=\\"white\\" stroke-width=\\"" + wcs["stroke-width"].replace("px", "") + "\\" paint-order=\\"stroke\\"").replaceAll("<circle", "<circle r=\\"" + (parseFloat(wcs["stroke-width"].replace("px", "")) * 1.5).toString() + "\\"")], {type: "image/svg+xml"}))]);\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        let cnv2d = document.createElement("canvas");\r\n' \
  '        ctx = cnv2d.getContext("2d");\r\n' \
  '        cnv2d.width = cwidth;\r\n' \
  '        cnv2d.height = cheight;\r\n' \
  '        ctx.globalCompositeOperation = "darken";\r\n' \
  '        prom_c = trdata.length;\r\n' \
  '        prom = new Promise(function(resolve, reject) {prom_res = resolve;});\r\n' \
  '        for (const tdata of trdata) {\r\n' \
  '          let trck = new Image();\r\n' \
  '          trck.onload = function (e) {URL.revokeObjectURL(tdata[2]); ctx.drawImage(trck, tdata[0], tdata[1]); prom_c--; if (prom_c == 0) {prom_res();};};\r\n' \
  '          trck.onerror = function (e) {URL.revokeObjectURL(tdata[2]);prom_c--; if (prom_c == 0) {prom_res();};};\r\n' \
  '          trck.src = tdata[2];\r\n' \
  '        }\r\n' \
  '        await prom;\r\n' \
  '        prom_c = trdata.length;\r\n' \
  '        prom = new Promise(function(resolve, reject) {prom_res = resolve;});\r\n' \
  '        for (const tdata of trdata) {\r\n' \
  '          let waypt = new Image();\r\n' \
  '          waypt.onload = function (e) {URL.revokeObjectURL(tdata[5]); ctx.drawImage(waypt, tdata[3], tdata[4]); prom_c--; if (prom_c == 0) {prom_res();};};\r\n' \
  '          waypt.onerror = function (e) {URL.revokeObjectURL(tdata[5]);prom_c--; if (prom_c == 0) {prom_res();};};\r\n' \
  '          waypt.src = tdata[5];\r\n' \
  '        }\r\n' \
  '        await prom;\r\n' \
  '        ctx.globalCompositeOperation = "lighten";\r\n' \
  '        prom_c = trdata.length;\r\n' \
  '        prom = new Promise(function(resolve, reject) {prom_res = resolve;});\r\n' \
  '        for (const tdata of trdata) {\r\n' \
  '          let waypt = new Image();\r\n' \
  '          waypt.onload = function (e) {URL.revokeObjectURL(tdata[6]); ctx.drawImage(waypt, tdata[3], tdata[4]); prom_c--; if (prom_c == 0) {prom_res();};};\r\n' \
  '          waypt.onerror = function (e) {URL.revokeObjectURL(tdata[6]);prom_c--; if (prom_c == 0) {prom_res();};};\r\n' \
  '          waypt.src = tdata[6];\r\n' \
  '        }\r\n' \
  '        await prom;\r\n' \
  '        document.getElementById("tset").disabled = false;\r\n' \
  '        document.getElementById("tset").style.pointerEvents = "";\r\n' \
  '        msgn = show_msg("{#jmdownmap3#}", 0, msgn);\r\n' \
  '        ctx.globalCompositeOperation = "destination-over";\r\n' \
  '        ctx.filter = document.documentElement.style.getPropertyValue("--filter") || "none";\r\n' \
  '        ctx.drawImage(mcnv2d, 0, 0);\r\n' \
  '        mcnv2d.width = mcnv2d.height = 1;\r\n' \
  '        msgn = show_msg("{#jmdownmap4#}", 0, msgn);\r\n' \
  '        let url = null;\r\n' \
  '        prom = new Promise(function(resolve, reject) {prom_res = resolve;});\r\n' \
  '        cnv2d.toBlob(function (blob) {url = URL.createObjectURL(blob); prom_res();});\r\n' \
  '        await prom;\r\n' \
  '        if (url) {\r\n' \
  '          let a = document.createElement("a");\r\n' \
  '          a.href = url;\r\n' \
  '          a.download = "map";\r\n' \
  '          show_msg("{#jmdownmap5#}".replace("%s", trdata.length.toString()).replace("%s", cnv2d.width.toString()).replace("%s", cnv2d.height.toString()), 5, msgn);\r\n' \
  '          a.click();\r\n' \
  '          URL.revokeObjectURL(url);\r\n' \
  '        } else {;\r\n' \
  '          show_msg("{#jmdownmap6#}", 10, msgn);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function download_tracklist(waypoints=false) {\r\n' \
  '        if (document.getElementById("edit").disabled) {return;}\r\n' \
  '        let b = track_boundaries();\r\n' \
  '        if (b == null) {return;}\r\n' \
  '        let tracklist = document.createElementNS("http://www.w3.org/2000/svg", "svg");\r\n' \
  '        tracklist.setAttribute("width", "0");\r\n' \
  '        tracklist.setAttribute("height", "0");\r\n' \
  '        let txt = document.createElementNS("http://www.w3.org/2000/svg", "text");\r\n' \
  '        txt.setAttribute("font-family", "Calibri, sans-serif");\r\n' \
  '        tracklist.appendChild(txt);\r\n' \
  '        let trks = document.getElementById("tracksform").children;\r\n' \
  '        for (let t=0; t<trks.length; t++) {\r\n' \
  '          if (trks[t].firstElementChild.checked) {\r\n' \
  '            let trkid = trks[t].id.slice(5,-4);\r\n' \
  '            let name = document.getElementById("track" + trkid + "desc").textContent.match(/^(.*)\\((?!.*\\()(.*)\\)$/);\r\n' \
  '            let color = document.getElementById("track" + trkid + "color").value;\r\n' \
  '            let tsp = document.createElementNS("http://www.w3.org/2000/svg", "tspan");\r\n' \
  '            tsp.setAttribute("x", "10");\r\n' \
  '            tsp.setAttribute("dy", "28");\r\n' \
  '            tsp.setAttribute("fill", color);\r\n' \
  '            tsp.setAttribute("font-size", 22);\r\n' \
  '            tsp.setAttribute("font-family", "sans-serif");\r\n' \
  '            tsp.appendChild(document.createTextNode("█"));\r\n' \
  '            txt.appendChild(tsp);\r\n' \
  '            for (let p=0; p<2; p++) {\r\n' \
  '              tsp = document.createElementNS("http://www.w3.org/2000/svg", "tspan");\r\n' \
  '              tsp.setAttribute("x", "30");\r\n' \
  '              tsp.setAttribute("dy", p?"14":"-9");\r\n' \
  '              tsp.setAttribute("font-size", p?"14":"16");\r\n' \
  '              tsp.setAttribute("font-weight", p?"normal":"bold");\r\n' \
  '              tsp.appendChild(document.createTextNode(name[p+1]));\r\n' \
  '              txt.appendChild(tsp);\r\n' \
  '            }\r\n' \
  '            if (waypoints) {\r\n' \
  '              let wpt = document.getElementById("waydots" + trkid).getElementsByTagName("title");\r\n' \
  '                for (let w=0; w<wpt.length; w++) {\r\n' \
  '                  tsp = document.createElementNS("http://www.w3.org/2000/svg", "tspan");\r\n' \
  '                  tsp.setAttribute("x", "40");\r\n' \
  '                  tsp.setAttribute("dy", "14");\r\n' \
  '                  tsp.setAttribute("font-size", "14");\r\n' \
  '                  tsp.appendChild(document.createTextNode("● " + wpt[w].textContent));\r\n' \
  '                  txt.appendChild(tsp);\r\n' \
  '               }\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        let div = document.createElement("div");\r\n' \
  '        div.setAttribute("style", "z-index:-1;position:absolute;visibility:hidden;width:0;height:0");\r\n' \
  '        div.appendChild(tracklist);\r\n' \
  '        document.body.appendChild(div);\r\n' \
  '        b = txt.getBBox();\r\n' \
  '        document.body.removeChild(div);\r\n' \
  '        let w = Math.ceil(2 * b.x + b.width);\r\n' \
  '        let h = Math.ceil(2.5 * b.y + b.height);\r\n' \
  '        tracklist.setAttribute("viewBox", "0 0 " + w.toString() + " " + h.toString());\r\n' \
  '        tracklist.setAttribute("width", w.toString());\r\n' \
  '        tracklist.setAttribute("height", h.toString());\r\n' \
  '        let xs = new XMLSerializer;\r\n' \
  '        let url = URL.createObjectURL(new Blob([xs.serializeToString(tracklist)], {type: "image/svg+xml"}));\r\n' \
  '        if (url) {\r\n' \
  '          let a = document.createElement("a");\r\n' \
  '          a.href = url;\r\n' \
  '          a.download = "tracklist";\r\n' \
  '          a.click();\r\n' \
  '          URL.revokeObjectURL(url);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      async function download_graph() {\r\n' \
  '        if (document.getElementById("edit").disabled || document.getElementById("graph").style.display == "none" || focused == "") {return;}\r\n' \
  '        let graphc = document.getElementById("graphc");\r\n' \
  '        let cnv2d = document.createElement("canvas");\r\n' \
  '        let ctx = cnv2d.getContext("2d");\r\n' \
  '        let ts = 2 * parseFloat(ctx.font);\r\n' \
  '        cnv2d.width = graphc.width + ts + 5;\r\n' \
  '        cnv2d.height = graphc.height + ts;\r\n' \
  '        ctx.filter = "invert(100%) hue-rotate(180deg) saturate(1000%)";\r\n' \
  '        ctx.drawImage(graphc, ts, 0, cnv2d.width - ts - 5, cnv2d.height - ts);\r\n' \
  '        ctx.fillStyle = "rgb(225,225,255)";\r\n' \
  '        ctx.font = "10px sans-serif";\r\n' \
  '        ctx.textAlign = "center";\r\n' \
  '        ctx.textBaseline = "bottom";\r\n' \
  '        ctx.fillText(document.getElementById("graphx").options[document.getElementById("graphx").selectedIndex].textContent, (cnv2d.width + 40) / 2, cnv2d.height - 5);\r\n' \
  '        ctx.textBaseline = "top";\r\n' \
  '        ctx.rotate(1.5 * Math.PI);\r\n' \
  '        ctx.fillText(document.getElementById("graphy").options[document.getElementById("graphy").selectedIndex].textContent, -(cnv2d.height - 25) / 2 , 5);\r\n' \
  '        let prom_res = null;\r\n' \
  '        let prom = new Promise(function(resolve, reject) {prom_res = resolve;});\r\n' \
  '        let url = null;\r\n' \
  '        cnv2d.toBlob(function (blob) {url = URL.createObjectURL(blob); prom_res();});\r\n' \
  '        await prom;\r\n' \
  '        if (url) {\r\n' \
  '          let a = document.createElement("a");\r\n' \
  '          a.href = url;\r\n' \
  '          a.download = "graph";\r\n' \
  '          a.click();\r\n' \
  '          URL.revokeObjectURL(url);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function open_explorer(target) {\r\n' \
  '        if (target.slice(0, 6) == "folder") {\r\n' \
  '          xhrex.open("GET", "/explorer?folder-" + target.substring(6));\r\n' \
  '        } else if (target.slice(-4) == "file") {\r\n' \
  '          if (window.getSelection) {window.getSelection().removeAllRanges();}\r\n' \
  '          xhrex.open("GET", "/explorer?file-" + target.slice(5, -4));\r\n' \
  '        } else {return;}\r\n' \
  '        xhrex.setRequestHeader("If-Match", sessionid);\r\n' \
  '        xhrex.send();\r\n' \
  '      }\r\n' \
  '      function load_cb(t, prop) {\r\n' \
  '        if (t.status != 204) {\r\n' \
  '          window.alert("{#jserror#}" + t.status.toString() + " " + t.statusText);\r\n' \
  '          error_cb(null, prop);\r\n' \
  '          document.getElementById("edit").disabled = false;\r\n' \
  '          document.getElementById("edit").style.pointerEvents = "";\r\n' \
  '          return false;\r\n'\
  '        }\r\n' \
  '        xhr_ongoing--;\r\n' \
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
  '          if (document.getElementById("oset").selectedIndex == 2) {tracks_sort();}\r\n' \
  '        } else if (prop.id.slice(-4) == "name") {\r\n' \
  '          document.getElementById(prop.id.replace("name", "desc")).innerHTML = document.getElementById(prop.id.replace("name", "desc")).innerHTML.replace(/.*(<br>.*)/, escape(prop.value) + "$1");\r\n' \
  '          document.getElementById(prop.id.replace("name", "desc")).title = prop.value;\r\n' \
  '          document.getElementById(prop.id.slice(0, -4).replace("track", "path")).firstElementChild.innerHTML = escape(prop.value);\r\n' \
  '          if (document.getElementById("oset").selectedIndex == 1) {tracks_sort();}\r\n' \
  '          tracks_filter();\r\n' \
  '        } else if (prop.id.slice(-5) == "color") {\r\n' \
  '          let trk = prop.id.slice(0, -5);\r\n' \
  '          let col = prop.value.toUpperCase();\r\n' \
  '          document.getElementById(trk).setAttribute("stroke", col);\r\n' \
  '          document.getElementById(trk).setAttribute("fill", col);\r\n' \
  '          document.getElementById(trk.replace("track", "waydots")).setAttribute("fill", col);\r\n' \
  '        }\r\n' \
  '        document.getElementById("edit").disabled = false;\r\n' \
  '        document.getElementById("edit").style.pointerEvents = "";\r\n' \
  '        return true;\r\n'\
  '      }\r\n' \
  '      function error_cb(t, prop) {\r\n' \
  '        xhr_ongoing--;\r\n' \
  '        if (t != null) {window.alert("{#jserror#}");}\r\n' \
  '        if (prop.id.slice(-4) == "file") {\r\n' \
  '          prop.value = document.getElementById(prop.id.replace("file", "visible")).value.split("\\\\").slice(-1)[0];\r\n' \
  '        } else if (prop.id.slice(-4) == "name") {\r\n' \
  '          prop.value = document.getElementById(prop.id.replace("name", "desc")).title;\r\n' \
  '        } else if (prop.id.slice(-5) == "color") {\r\n' \
  '          prop.value = document.getElementById(prop.id.slice(0, -5)).getAttribute("stroke");\r\n' \
  '        }\r\n' \
  '        if (t != null) {\r\n' \
  '          document.getElementById("edit").disabled = false;\r\n' \
  '          document.getElementById("edit").style.pointerEvents = "";\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function track_save(prop) {\r\n' \
  '        if (document.getElementById("edit").disabled) {error_cb(null, prop);return;}\r\n' \
  '        document.getElementById("edit").disabled = true;\r\n' \
  '        document.getElementById("edit").style.pointerEvents = "none";\r\n' \
  '        if (prop.id.slice(-4) == "file") {\r\n' \
  '          if (! prop.checkValidity()) {\r\n' \
  '            prop.value = document.getElementById(prop.id.replace("file", "visible")).value.split("\\\\").slice(-1)[0];\r\n' \
  '            document.getElementById("edit").disabled = false;\r\n' \
  '            document.getElementById("edit").style.pointerEvents = "";\r\n' \
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
  '        xhr_ongoing++;\r\n' \
  '        xhr.send(body);\r\n' \
  '      }\r\n' \
  '      function track_change(e) {\r\n' \
  '        e.stopPropagation();\r\n' \
  '        let elt = e.target;\r\n' \
  '        if (! elt) {return;}\r\n' \
  '        let fld = elt.id.match(/[0-9]+(.*)$/);\r\n' \
  '        if (! fld) {return;}\r\n' \
  '        switch (fld[1]) {\r\n' \
  '          case "visible":\r\n' \
  '            track_checkbox(elt);\r\n' \
  '            break\r\n' \
  '          case "color":\r\n' \
  '            track_color(elt);\r\n' \
  '            break\r\n' \
  '          case "name":\r\n' \
  '          case "file":\r\n' \
  '            track_save(elt);\r\n' \
  '            break\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      var xhr = new XMLHttpRequest();\r\n' \
  '      var xhrt = new XMLHttpRequest();\r\n' \
  '      xhrt.addEventListener("error", error_tcb);\r\n' \
  '      var xhrep = new XMLHttpRequest();\r\n' \
  '      xhrep.addEventListener("error", error_epcb);\r\n' \
  '      var xhrtr = new XMLHttpRequest();\r\n' \
  '      var xhrex = new XMLHttpRequest();\r\n' \
  '    </script>\r\n' \
  '  </head>\r\n' \
  '  <body style="background-color:rgb(40,45,50);color:rgb(225,225,225);margin-top:2px;margin-bottom:0;">\r\n' \
  '    <table style="width:98vw;">\r\n' \
  '      <colgroup>\r\n' \
  '        <col style="width:21em;">\r\n' \
  '        <col style="width:calc(98vw - 21em);">\r\n' \
  '      </colgroup>\r\n' \
  '      <thead>\r\n' \
  '        <tr>\r\n' \
  '          <th colspan="2" style="text-align:left;font-size:120%;width:100%;border-bottom:1px darkgray solid;user-select:none;">\r\n' \
  '           <form style="display:inline-block;" onsubmit="this.firstElementChild.blur();return false;">\r\n' \
  '             <input type="text" id="tracksfilter" name="tracksfilter" autocomplete="off" list="tracksfilterhistory" value="" oninput="tracks_filter()" onchange="tracks_filter_history()">\r\n' \
  '             <datalist id="tracksfilterhistory"></datalist>\r\n' \
  '             <button style="font-size:80%;">&#128269;&#xfe0e;</button>\r\n' \
  '           </form>\r\n' \
  '           <span style="display:inline-block;position:absolute;right:2vw;width:63.4em;overflow:hidden;text-align:right;font-size:80%;" oncontextmenu="event.preventDefault();"><button title="{#jdescending#}" id="sortup" style="margin-left:0em;" onclick="switch_sortorder()">&#9699;</button><button title="{#jascending#}" id="sortdown" style="margin-left:0em;display:none;" onclick="switch_sortorder()">&#9700</button><select id="oset" name="oset" title="{#joset#}" autocomplete="off" style="width:12em;margin-left:0.25em;" onchange="tracks_sort()"><option value="none">{#jsortnone#}</option><option value="name">{#jsortname#}</option><option value="file path">{#jsortfilepath#}</option><option value="duration">{#jsortduration#}</option><option value="distance">{#jsortdistance#}</option><option value="elevation gain">{#jsortelegain#}</option><option value="altitude gain">{#jsortaltgain#}</option><option value="date">{#jsortdate#}</option><option value="proximity">{#jsortproximity#}</option><</select><button title="{#jfolders#}" style="margin-left:0.75em;" onclick="switch_folderspanel()">&#128193;&#xfe0e;</button><button title="{#jhidetracks#}" style="margin-left:0.75em;" onclick="show_hide_tracks(false, event.altKey)">&EmptySmallSquare;</button><button title="{#jshowtracks#}" style="margin-left:0.25em;" onclick="show_hide_tracks(true, event.altKey)">&FilledSmallSquare;</button><button title="{#jdownloadmap#}" style="margin-left:1em;" onclick="(event.shiftKey||event.altKey)?download_tracklist(event.altKey):(event.ctrlKey?download_graph():download_map())">&#9113;</button><button title="{#jswitchmedia#}" id="switchmedia" style="margin-left:1em;" onclick="event.ctrlKey?switch_mtpanel():(event.altKey?switch_mediapreview():show_hide_media())">&#128247;&#xfe0e;</button><button title="{#jtrackdetach#}" style="margin-left:1em;" onclick="track_detach()">&#128228;&#xfe0e;</button><button title="{#jtrackintegrate#}" style="margin-left:0.25em;" onclick="track_incorporate_integrate(event.altKey)">&#128229;&#xfe0e;</button><button title="{#jtrackincorporate#}" style="margin-left:0.25em;" onclick="track_incorporate_integrate()">&LeftTeeArrow;</button><button title="{#jtracknew#}" style="margin-left:0.75em;" onclick="track_new()">+</button><button title="{#jtrackedit#}" id="edit" style="margin-left:1em;" onclick="track_edit()">&#9998;</button><button title="{#jwebmapping#}" style="margin-left:1em;" onclick="open_webmapping()">&#10146;</button><button title="{#jzoomall#}" style="margin-left:0.75em;" onclick="document.getElementById(\'tset\').disabled?null:switch_tiles(null, null, event.altKey?2:(event.shiftKey?1:0))">&target;</button><button id="swsm" title="{#jswitchsmooth#}" style="margin-left:0.25em;letter-spacing:-0.2em" onclick="event.ctrlKey?switch_dfpanel():switch_smooth()">&homtht;&homtht;</button><button title="{#jgraph#}" style="margin-left:0.25em;" onclick="if (event.shiftKey || event.ctrlKey || event.altKey) {switch_filterpanel(event.shiftKey?1:(event.ctrlKey?2:3))} else {switch_mediapreview(true);refresh_graph(true);}">&angrt;</button><button title="{#j3dviewer#}" style="margin-left:0.25em;" onclick="event.ctrlKey?switch_3Dpanel():open_3D(event.altKey?\'s\':\'p\')">3D</button><select id="tset" name="tset" title="{#jexptset#}" autocomplete="off" style="margin-left:0.75em;" onmousedown="switch_sel(event, this)" onchange="switch_tiles(this.selectedIndex, -1)">##TSETS##</select><select id="eset" name="eset" title="{#jexpeset#}" autocomplete="off" style="display:none;margin-left:0.75em;" onmousedown="switch_sel(event, this)" onchange="switch_elevations(this.selectedIndex)">##ESETS##</select><select id="iset" name="wmset" title="{#jexpiset#}" autocomplete="off" style="display:none;margin-left:0.75em;" onmousedown="switch_sel(event, this)">##WMSETS##</select><button title="{#jexpminus#}" style="margin-left:0.25em;" onclick="event.ctrlKey?map_adjust(\'-\', \'a\'):(event.shiftKey?map_adjust(\'-\', \'e\'):(event.altKey?magnify_dec():zoom_dec()))">-</button><span id="matrix" style="display:none;width:1.5em;">--</span><button id="tlock" title="{#jlock#}" style="display:none;width:1em" onclick="switch_tlock()">&#128275;&#xfe0e;</button><span id="zoom" style="display:inline-block;width:2em;text-align:center;">1</span><button title="{#jexpplus#}" style="" onclick="event.ctrlKey?map_adjust(\'+\', \'a\'):(event.shiftKey?map_adjust(\'+\', \'e\'):(event.altKey?magnify_inc():zoom_inc()))">+</button></span>\r\n' \
  '            <div id="folderspanel" style="display:none;position:absolute;top:calc(1.6em + 10px);left:25em;box-sizing:border-box;max-width:calc(98vw - 25.1em);max-height:calc(99vh - 3.2em - 25px);padding:10px;overflow:auto;white-space:nowrap;background-color:rgb(40,45,50);z-index:20;font-size:80%;font-weight:normal;">\r\n' \
  '              <form id="foldersform" autocomplete="off" onsubmit="return(false);" onchange="folders_select()">\r\n' \
  '                <button style="margin-left:0.75em;" onclick="folders_whole(false)">&EmptySmallSquare;</button><button style="margin-left:0.25em;" onclick="folders_whole(true)">&FilledSmallSquare;</button>\r\n' \
  '                <span style="font-weight:bold;">{#jfoldersw#}</span><br>\r\n' \
  '##FOLDERS##' \
  '              </form>\r\n' \
  '            </div>\r\n' + HTML_ATTENUATE_TEMPLATE + HTML_OPACITYPANEL_TEMPLATE + HTML_DFMTPANEL_TEMPLATE + HTML_FILTERPANEL_TEMPLATE.replace('segments_calc', 'tracks_calc') + HTML_3DPANEL_TEMPLATE + \
  '          </th>\r\n' \
  '        </tr>\r\n' \
  '      </thead>\r\n' \
  '      <tbody>\r\n' \
  '        <tr style="display:table-row;">\r\n' \
  '          <td style="display:table-cell;vertical-align:top;">\r\n' \
  '            <div id="content" style="height:calc(99vh - 2.4em - 16px);width: calc(21em - 2px);">\r\n' \
  '              <div id="tracks" style="overflow-y:scroll;overflow-x:hidden;height:100%;font-size:80%">\r\n' \
  '                {#jtracks#} (##NBTRACKS##)<br>\r\n' \
  '                <form id="tracksform" autocomplete="off" onchange="track_change(event)" onsubmit="return(false);">\r\n                  #<#TRACKS#>#\r\n' \
  '                </form>\r\n' \
  '              </div>\r\n' \
  '            </div>\r\n' \
  '          </td>\r\n' \
  '          <td style="display:table-cell;vertical-align:top;position:relative;">\r\n' \
  '            <div id="view" style="overflow:hidden;position:absolute;width:100%;height:calc(99vh - 2.4em - 16px);line-height:0;user-select:none;" onmousedown="mouse_down(event)" onclick="mouse_click(event)" onwheel="mouse_wheel(event)" onpointerdown="pointer_down(event)">\r\n' \
  '              <div id="background" style="position:absolute;top:0px;left:0px;width:100%;height:100%;backdrop-filter:var(--filter);pointer-events:none;"></div>\r\n' \
  '              <div id="handle" style="position:relative;top:0px;left:0px;width:100px;height:100px;pointer-events:none;">\r\n' \
  '              #<#PATHES#>##<#WAYDOTS#>#</div>\r\n' \
  '              <div id="scrollbox" style="left:0.1em;line-height:1em;">\r\n' \
  '                <span id="scrollcross" title="{#jexpscrollcross#}" onclick="scrollcross(event.ctrlKey);event.stopPropagation()" onmousedown="event.stopPropagation()" onpointerdown="event.stopPropagation()" oncontextmenu="event.stopPropagation();event.preventDefault();" style="vertical-align:middle;color:rgb(90,90,90);cursor:pointer;">&#10012;</span>\r\n' \
  '              </div>\r\n' + HTML_SSB_GRAPH_TEMPLATE.replace('{#jhelp#}', '{#jexphelp#}') + \
  '    <div id="mediapreview" style="display:none" onscroll="if (! document.fullscreen) {this.dataset.sl=this.scrollLeft.toString();}" oncontextmenu="event.stopPropagation();event.preventDefault();">\r\n' \
  '    </div>\r\n' \
  '    <div id="mediaview" style="display:none;" onscroll="if (! document.fullscreen) {this.dataset.sl=this.scrollLeft.toString();}" oncontextmenu="close_mediaview(event);" >\r\n' \
  '    </div>\r\n' \
  '    <script>\r\n' \
  '      var mousex = null;\r\n' \
  '      var mousey = null;\r\n' \
  '      var viewpane = document.getElementById("view");\r\n' \
  '      var handle = document.getElementById("handle");\r\n' \
  '      var hand = null;\r\n' \
  '      var mouse_out = null;\r\n' \
  '      var pointer_e = null;\r\n' \
  '      var mouse_ocm = null;\r\n' \
  '      function pointer_down(e) {\r\n' \
  '        pointer_e = e.pointerId;\r\n' \
  '      }\r\n' \
  '      function mouse_down(e) {\r\n' \
  '        if (e.button != 0 && e.button != 2) {return;}\r\n' \
  '        document.getElementById("tracksfilter").blur();\r\n' \
  '        mousex = e.pageX;\r\n' \
  '        mousey = e.pageY;\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '        document.onmousemove = mouse_move;\r\n' \
  '        document.onmouseup = mouse_up;\r\n' \
  '        if (document.activeElement) {\r\n' \
  '          if (document.activeElement.nodeName != "BODY") {document.activeElement.blur();}\r\n' \
  '        }\r\n' \
  '        if (e.button == 2) {\r\n' \
  '          if (mouse_ocm) {clearTimeout(mouse_ocm); mouse_ocm=null;}\r\n' \
  '          document.oncontextmenu = mouse_click;\r\n' \
  '        }\r\n' \
  '        scrollmode_ex = scrollmode;\r\n' \
  '        scrollmode = 0;\r\n' \
  '        if (e.target && e.button == 0) {\r\n' \
  '          if (e.target.id == "view") {\r\n' \
  '            hand = e.target;\r\n' \
  '            viewpane.style.cursor = "all-scroll";\r\n' \
  '            viewpane.setPointerCapture(pointer_e);\r\n' \
  '            media_ex_visible = media_visible;\r\n' \
  '            hide_media("m");\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_up(e) {\r\n' \
  '        mousex = null;\r\n' \
  '        mousey = null;\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '        document.onmousemove = null;\r\n' \
  '        document.onmouseup = null;\r\n' \
  '        scrollmode = scrollmode_ex;\r\n' \
  '        if (hand) {\r\n' \
  '          if (mouse_out != null) {\r\n' \
  '            window.clearInterval(mouse_out);\r\n' \
  '            mouse_out = null;\r\n' \
  '          }\r\n' \
  '          hand = null;\r\n' \
  '          viewpane.style.cursor = "";\r\n' \
  '          viewpane.releasePointerCapture(pointer_e);\r\n' \
  '          pointer_e = null;\r\n' \
  '          if (media_ex_visible) {\r\n' \
  '            show_media();\r\n' \
  '            media_ex_visible = false;\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '        if (e.button == 2) {\r\n' \
  '          mouse_ocm = setTimeout(function() {if (mouse_ocm) {document.oncontextmenu=null; mouse_ocm=null;};}, 100);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_click(e) {\r\n' \
  '        e.stopPropagation();\r\n' \
  '        e.preventDefault();\r\n' \
  '        document.oncontextmenu = null;\r\n' \
  '        if (mouse_ocm) {clearTimeout(mouse_ocm); mouse_ocm=null;}\r\n' \
  '        let elt = e.target;\r\n' \
  '        if (! elt) {return;}\r\n' \
  '        if (e.button == 2) {\r\n' \
  '          if (elt.id.substring(0, 4) == "path") {\r\n' \
  '            let cb = document.getElementById(elt.id.replace("path", "track") + "visible");\r\n' \
  '            cb.checked = false;\r\n' \
  '            track_checkbox(cb);\r\n' \
  '            if (document.getElementById(elt.id.replace("path", "track") + "cont").style.display != "none") {\r\n' \
  '              cb.scrollIntoView({block:"nearest"});\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '        } else {\r\n' \
  '          let trk = null;\r\n' \
  '          if (elt.id.substring(0, 4) == "path") {\r\n' \
  '            if (document.getElementById(elt.id.replace("path", "track") + "cont").style.display != "none") {\r\n' \
  '              trk = document.getElementById(elt.id.replace("path", "track") + "desc");\r\n' \
  '            }\r\n' \
  '          } else if (elt.parentNode.id.substring(0, 7) == "waydots") {\r\n' \
  '            if (document.getElementById(elt.parentNode.id.replace("waydots", "track") + "cont").style.display != "none") {\r\n' \
  '              trk = document.getElementById(elt.parentNode.id.replace("waydots", "track") + "desc");\r\n' \
  '            }\r\n' \
  '          }\r\n' \
  '          if (trk) {track_click(null, trk, false);}\r\n' \
  '          if (trk && focused) {\r\n' \
  '            trk.scrollIntoView({block:"nearest"});\r\n' \
  '            document.getElementById(focused + "focus").scrollIntoView({block:"nearest"});\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_outside() {\r\n' \
  '        if (mouse_out == null) {return;}\r\n' \
  '        let dx = 0;\r\n' \
  '        let dy = 0;\r\n' \
  '        let p = viewpane.parentNode;\r\n' \
  '        let pl = p.offsetLeft;\r\n' \
  '        let pr = pl + p.offsetWidth;\r\n' \
  '        let pt = p.offsetTop;\r\n' \
  '        let pb = pt + p.offsetHeight;\r\n' \
  '        if (mousex < pl) {\r\n' \
  '          dx = -Math.max(1, p.offsetWidth / 20);\r\n' \
  '        } else if (mousex > pr) {\r\n' \
  '          dx = Math.max(1, p.offsetWidth / 20);\r\n' \
  '        }\r\n' \
  '        if (mousey < pt) {\r\n' \
  '          dy = -Math.max(1, p.offsetHeight / 20);\r\n' \
  '        } else if (mousey > pb) {\r\n' \
  '          dy = Math.max(1, p.offsetHeight / 20);\r\n' \
  '        }\r\n' \
  '        if (dx || dy) {\r\n' \
  '          scroll_dview(dx, dy);\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_move(e) {\r\n' \
  '        if (mousex != null && mousey != null && hand != null) {\r\n' \
  '          let p = viewpane.parentNode;\r\n' \
  '          let pl = p.offsetLeft;\r\n' \
  '          let pr = pl + p.offsetWidth;\r\n' \
  '          let pt = p.offsetTop;\r\n' \
  '          let pb = pt + p.offsetHeight;\r\n' \
  '          let mx = e.pageX;\r\n' \
  '          let my = e.pageY;\r\n' \
  '          if (hand.id == "view") {\r\n' \
  '            cpx = cpy = null;\r\n' \
  '            scroll_dview(Math.min(Math.max(mx, pl), pr) - Math.min(Math.max(mousex, pl), pr), Math.min(Math.max(my, pt), pb) - Math.min(Math.max(mousey, pt), pb));\r\n' \
  '          } else {return;}\r\n' \
  '          if (mx >= pl && mx <= pr && my >= pt && my <= pb) {\r\n' \
  '            if (mouse_out != null) {\r\n' \
  '              window.clearInterval(mouse_out);\r\n' \
  '              mouse_out = null;\r\n' \
  '            }\r\n' \
  '          } else if (mouse_out == null) {\r\n' \
  '            mouse_out = window.setInterval(mouse_outside, 100);\r\n' \
  '          }\r\n' \
  '          mousex = mx;\r\n' \
  '          mousey = my;\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function mouse_wheel(e) {\r\n' \
  '        e.preventDefault();\r\n' \
  '        if (e.ctrlKey) {\r\n' \
  '          let p = viewpane.parentNode;\r\n' \
  '          (e.deltaY<0?zoom_inc:zoom_dec)(e.pageX - p.offsetLeft, e.pageY - p.offsetTop);\r\n' \
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
  '      function window_resize() {\r\n' \
  '        if (document.fullscreen) {\r\n' \
  '          media_fs = true;\r\n' \
  '        } else {\r\n' \
  '          if (media_fs) {\r\n' \
  '            media_fs = false;\r\n' \
  '            if (media_visible) {\r\n' \
  '              document.getElementById("mediaview").scrollLeft = parseFloat(document.getElementById("mediaview").dataset.sl);\r\n' \
  '              document.getElementById("mediapreview").scrollLeft = parseFloat(document.getElementById("mediapreview").dataset.sl);\r\n' \
  '            }\r\n' \
  '          } else {\r\n' \
  '            rescale();\r\n' \
  '            refresh_graph();\r\n' \
  '          }\r\n' \
  '        }\r\n' \
  '      }\r\n' \
  '      function page_unload() {\r\n' + HTML_PAGE_UNLOAD_TEMPLATE + \
  '        sessionStorage.setItem("state_exp", document.getElementById("tracksfilter").value.replace(/&/g, "&amp;").replace(/\\|/g, "&;") + "|" + no_sort.join("-") + "|" + (document.getElementById("sortup").style.display == "").toString() + "|" + document.getElementById("oset").selectedIndex.toString() + "|" + Array.from(document.getElementById("foldersform").getElementsByTagName("input"), f => f.checked?"t":"f").join("-") + "|" + Array.from({length:document.getElementById("tracksform").children.length}, (v, k) => document.getElementById("track" + k.toString() + "visible").checked?"t":"f").join("-") + "|" + document.getElementById("iset").selectedIndex.toString() + "|" + document.getElementById("mtsize").innerHTML + "|" + media_visible.toString() + "|" + smoothed.toString() + "|" + magnify.toString());\r\n' \
  '      }\r\n' \
  '      function error_dcb() {\r\n' \
  '        window.alert("{#jexpfail#}");\r\n' \
  '        document.body.innerHTML = "";\r\n' \
  '        document.head.innerHTML = "";\r\n' \
  '        window.close();\r\n' \
  '        throw "{#jexpfail#}";\r\n' \
  '      }\r\n' \
  '      function load_dcb(t) {\r\n' \
  '        if (t.status != 200) {error_dcb();return;}\r\n' \
  '        tracks_pts = JSON.parse(t.response);\r\n' \
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
  '        }\r\n' + HTML_PAGE_LOAD_TEMPLATE.replace('switch_tiles(-1, 0)', 'switch_tiles(-1, null)') + \
  '        if (prev_state != null) {\r\n' \
  '          dots_visible = prev_state[4] == "true";\r\n' \
  '        }\r\n' \
  '        prev_state = sessionStorage.getItem("state_exp");\r\n' \
  '        if (prev_state != null) {\r\n' \
  '          prev_state = prev_state.split("|");\r\n' \
  '          document.getElementById("tracksfilter").value = prev_state[0].replace(/\\&;/g, "|").replace(/&amp;/g, "&");\r\n' \
  '          tracks_filter_history();\r\n' \
  '          no_sort = prev_state[1].split("-").map(Number);\r\n' \
  '          document.getElementById("sortup").style.display = prev_state[2]=="true"?"":"none";\r\n' \
  '          document.getElementById("sortdown").style.display = prev_state[2]=="true"?"none":"";\r\n' \
  '          document.getElementById("oset").selectedIndex = parseInt(prev_state[3]);\r\n' \
  '          let folders = document.getElementById("foldersform").getElementsByTagName("input");\r\n' \
  '          let st = prev_state[4].split("-");\r\n' \
  '          for (let f=0; f<folders.length; f++) {folders[f].checked = st[f]=="t";}\r\n' \
  '          st = prev_state[5].split("-");\r\n' \
  '          for (let t=0; t<st.length; t++) {\r\n' \
  '            document.getElementById("track" + t.toString() + "visible").checked = st[t]=="t";\r\n' \
  '            track_checkbox(document.getElementById("track" + t.toString() + "visible"));\r\n' \
  '          }\r\n' \
  '          let wmset = parseInt(prev_state[6]);\r\n' \
  '          if (document.getElementById("iset").options.length > wmset) {document.getElementById("iset").selectedIndex = wmset;}\r\n' \
  '          document.getElementById("mtsize").innerHTML = prev_state[7];\r\n' \
  '          document.getElementById("mthumb").value = parseFloat(prev_state[7]);\r\n' \
  '          if (prev_state[8] == "true") {show_media();}\r\n' \
  '          smoothed = prev_state[9] == "true";\r\n' \
  '          magnify = parseInt(prev_state[10]);\r\n' \
  '          document.documentElement.style.setProperty("--magnify", prev_state[10]);\r\n' \
  '        } else {\r\n' \
  '          no_sort = Array.from({length:tracks_pts.length}).map((v,k)=>k);\r\n' \
  '          magnify_inc();\r\n' \
  '        }\r\n' \
  '        if (smoothed) {document.getElementById("swsm").innerHTML = "&divide;&divide;"};\r\n' \
  '        tracks_calc();\r\n' \
  '        tracks_sort();\r\n' \
  '        tracks_filter();\r\n' \
  '        folders_select();\r\n' \
  '        document.getElementById("mediaview").dataset.sl = "0";\r\n' \
  '        document.getElementById("mediapreview").dataset.sl = "0";\r\n' \
  '        window.onresize = window_resize;\r\n' \
  '        window.onbeforeunload = page_unload;\r\n' \
  '        if (focused != "") {\r\n' \
  '          foc = focused;\r\n' \
  '          focused = "";\r\n' \
  '          track_click(null, document.getElementById(foc + "desc"));\r\n' \
  '          scroll_to_track(document.getElementById(foc), true);\r\n' \
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
  '                <label for="folder%s" title="{jexplorer}" ondblclick="open_explorer(this.htmlFor)">%s</label><br>\r\n'
  HTMLExp_FOLDER_TEMPLATE = HTMLExp_FOLDER_TEMPLATE.format_map(LSTRINGS['interface'])
  HTMLExp_TRACK_TEMPLATE = \
  '<div id="track%scont">\r\n' \
  '                    <input type="checkbox" id="track%svisible" checked name="track%svisible" value="%s" onmouseover="track_over(this)" onmouseout="track_outside(this)">' \
  '<label for="track%svisible" id="track%sdesc" title="%s" onclick="track_click(event, this)" onmouseover="track_over(this)" onmouseout="track_outside(this)">%s<br>(--h--mn--s | -km | -m | -m)</label>\r\n' \
  '                    <input type="color" id="track%scolor" value="%s" onmouseover="track_over(this)" onmouseout="track_outside(this)">\r\n' \
  '                    <span id="track%sfocus">\r\n' \
  '                      <label for="track%sname">{jname}</label>\r\n' \
  '                      <input type="text" id="track%sname" name="track%sname" value="%s"><br>\r\n' \
  '                      <label for="track%sfile" title="{jexplorer}" ondblclick="open_explorer(this.htmlFor)">{jfile}</label>\r\n' \
  '                      <input type="text" id="track%sfile" name="track%sfile" required pattern="[^\\\\\\/\\?\\*:<>&quot;\\|]*(?<!\\s-\\s(original|backup)(\\.[Gg][Pp][Xx])?)" value="%s"><br>\r\n' \
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
  '  <svg id="track%s" viewbox="##VIEWBOX##" stroke="%s" fill="%s" style="width:##WIDTH##;height:##HEIGHT##;top:##TOP##;left:##LEFT##;">\r\n' \
  '                  <path id="path%s" d="M0 0">\r\n' \
  '                   <title>%s</title>;\r\n' \
  '                  </path>\r\n' \
  '                  <text id="patharrows%s" dy="0.25em">\r\n' \
  '                    <textPath href="#path%s">##ARROWS##</textPath>\r\n' \
  '                  </text>\r\n' \
  '                </svg>\r\n              '
  HTMLExp_WAYDOT_TEMPLATE = \
  '                  <circle cx="%s" cy="%s"><title>%s</title></circle>\r\n'
  HTMLExp_WAYDOTS_TEMPLATE = \
  '  <svg id="waydots%s" viewbox="##VIEWBOX##" fill="%s" style="width:##WIDTH##;height:##HEIGHT##;top:##TOP##;left:##LEFT##;">\r\n%s' \
  '                </svg>\r\n              '

  @staticmethod
  def cpu_pcores_count():
    try:
      kernel32 = ctypes.WinDLL('kernel32',  use_last_error=True)
      byref = ctypes.byref
      sizeof = ctypes.sizeof
      DWORD = ctypes.wintypes.DWORD
      WORD = ctypes.wintypes.WORD
      BYTE = ctypes.wintypes.BYTE
      ULONG_PTR = ctypes.c_size_t
      ULONGLONG = ctypes.c_ulonglong
      INT = ctypes.c_int
      STRUCTURE = ctypes.Structure
      UNION = ctypes.Union
      class PROCESSOR_CORE(STRUCTURE):
        _fields_ = [('Flags', BYTE)]
      class NUMA_NODE(STRUCTURE):
        _fields_ = [('NodeNumber', DWORD)]
      class CACHE_DESCRIPTOR(STRUCTURE):
        _fields_ = [('Level', BYTE), ('Associativity', BYTE), ('LineSize', WORD), ('Size', DWORD), ('Type',INT)]
      class DUMMYUNIONNAME(UNION):
        _fields_ = [('ProcessorCore', PROCESSOR_CORE), ('NumaNode', NUMA_NODE), ('Cache', CACHE_DESCRIPTOR), ('Reserved', ULONGLONG * 2)]
      class SYSTEM_LOGICAL_PROCESSOR_INFORMATION(STRUCTURE):
        _anonymous_ = ('DUMMYUNIONNAME',)
        _fields_ = [('ProcessorMask', ULONG_PTR), ('Relationship', INT), ('DUMMYUNIONNAME', DUMMYUNIONNAME)]
      b = ctypes.create_string_buffer(0)
      s = DWORD(0)
      kernel32.GetLogicalProcessorInformation(b, byref(s))
      if kernel32.GetLastError() != 122:
        return None
      b = (SYSTEM_LOGICAL_PROCESSOR_INFORMATION * (s.value // sizeof(SYSTEM_LOGICAL_PROCESSOR_INFORMATION)))()
      if not kernel32.GetLogicalProcessorInformation(b, byref(s)):
        return None
      npcores = 0
      for i in b:
        if not i.Relationship:
          npcores += 1
      return npcores
    except:
      return None

  def _load_config(self, uri=os.path.dirname(os.path.abspath(__file__)) + r'\GPXTweaker.cfg'):
    try:
      f = open(uri, 'rt', encoding='utf-8')
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
          self.TilesSets.append([hcur[9:].strip(), {}, {}, {}, [1, ]])
          s = self.TilesSets[-1]
        elif hcur[:18].lower() == 'maptilescomposite ':
          hcur = hcur[:18].lower() + hcur[18:]
          self.TilesSets.append([hcur[18:].strip(), [], [1, ]])
          s = self.TilesSets[-1]
        elif hcur[:4].lower() == 'map ':
          hcur = hcur[:4].lower() + hcur[4:]
          self.MapSets.append([hcur[4:].strip(), {}, {}, {}])
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
        elif hcur[:20].lower() == 'reversegeocodingapi ':
          hcur = hcur[:20].lower() + hcur[20:]
          self.ReverseGeocodingsProviders.append([hcur[20:].strip(), {}, {}])
          s = self.ReverseGeocodingsProviders[-1]
        elif hcur.lower() in ('global', 'explorer'):
          hcur = hcur.lower()
        else:
          self.log(0, 'cerror', hcur)
          return False
        continue
      if l[0] == '[' and l[-1] == ']':
        scur = l[1:-1].lower()
        if hcur == 'global':
          if not scur in ('interfaceserver', 'proxy', 'jsontiles', 'tilesbuffer', 'boundaries', 'statistics', '3dviewer'):
            self.log(0, 'cerror', hcur + ' - ' + scur)
            return False
        elif hcur == 'explorer':
          if not scur in ('loading', 'folders', 'statistics', 'media') and scur[:11] != 'webmapping ':
            self.log(0, 'cerror', hcur + ' - ' + scur)
            return False
          if scur[:11] == 'webmapping ':
            self.WebMappingServices.append([l[12:-1].strip(), {}])
            s = self.WebMappingServices[-1]
        elif hcur[:9] == 'maptiles ':
          if not scur in ('infos', 'handling', 'legend', 'display'):
            self.log(0, 'cerror', hcur + ' - ' + scur)
            return False
        elif hcur[:18] == 'maptilescomposite ':
          if scur == 'layer':
            s[1].append([len(self.TilesSets) - 1, '1.00', {}])
          elif scur not in ('layers', 'display'):
            self.log(0, 'cerror', hcur + ' - ' + scur)
            return False
        elif hcur[:4] == 'map ' or hcur[:15] == 'elevationtiles ' or hcur[:13] in ('elevationmap ', 'elevationapi ', 'itineraryapi ') or hcur[:20] == 'reversegeocodingapi ':
          if not scur in ('infos', 'handling') and (hcur[:4] != 'map ' or scur != 'legend'):
            self.log(0, 'cerror', hcur + ' - ' + scur)
            return False
        else:
          self.log(0, 'cerror', hcur + ' - ' + scur)
          return False
        continue
      if not (hcur[:8] == 'maptiles' and scur == 'display') and not (hcur == 'explorer' and scur == 'folders'):
        if ':' in l:
          field, value = l.split(':', 1)
          if scur == 'legend':
            field = field.strip()
          else:
            field = field.lower().strip()
          value = value.lstrip()
          if value.lower() == 'true':
            value = True
          elif value.lower() == 'false':
            value = False
          elif value.lower() == 'none':
            value = None
          elif value.lower() == '':
            value = None if scur in ('boundaries', 'statistics', '3dviewer', 'handling') else ''
        else:
          self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
          return False
      if hcur == 'global':
        if scur == 'interfaceserver':
          if field == 'ip':
            self.Ip = value or self.Ip
          elif field == 'port':
            if value:
              if '-' in value:
                self.Ports = value.split('-', 1)
              else:
                self.Ports = (value, value)
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
        elif scur == 'proxy':
          if field == 'ip':
            if value:
              self.Proxy['ip'] = value
          elif field == 'port':
            if value:
              if not value.isdecimal():
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              self.Proxy['port'] = int(value)
          elif field == '"user_colon_password"':
            if value:
              if len(value) < 2 or value[:1] != '"' or value [-1:] != '"':
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              self.Proxy['auth'] = value[1:-1]
          elif field == 'secure':
            self.Proxy['secure'] = value is True or value.lower() == 'yes'
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'jsontiles':
          if field == 'enable':
            self.JSONTiles = value
          elif field in ('maplibrejs', 'maplibrecss'):
            if '://' in value:
              value = urllib.parse.urlsplit(value, allow_fragments=False)
              if value.scheme.lower() not in ('http', 'https'):
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              value = (value.scheme + '://' + value.netloc, value.path.lstrip('/') + ('?' + value.query if value.query else ''))
            else:
              value = os.path.split(os.path.abspath(os.path.expandvars(value)))
            if field == 'maplibrejs':
              self.JSONTilesJS = value
            else:
              self.JSONTilesCSS = value
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'tilesbuffer':
          if field == 'size':
            self.TilesBufferSize = None if value is None else int(value)
          elif field == 'threads':
            self.TilesBufferThreads = None if value is None else int(value)
          elif field == 'chromium_hold':
            self.TilesHoldSize = 0 if value is None else int(value)
          elif field == 'elevation_size':
            self.ElevationTilesBufferSize = None if value is None else int(value)
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'boundaries':
          if field == 'min_lat':
            if value is None:
              self.VMinLat = None
            else:
              self.VMinLat = float(value)
              if self.VMinLat < -math.degrees(2 * math.atan(math.exp(math.pi)) - math.pi / 2):
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              if self.VMaxLat is not None:
                if self.VMinLat >= self.VMaxLat:
                  self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                  return False
          elif field == 'max_lat':
            if value is None:
              self.VMaxLat = None
            else:
              self.VMaxLat = float(value)
              if self.VMaxLat > math.degrees(2 * math.atan(math.exp(math.pi)) - math.pi / 2):
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              if self.VMinLat is not None:
                if self.VMinLat >= self.VMaxLat:
                  self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                  return False
          elif field == 'min_lon':
            if value is None:
              self.VMinLon = None
            else:
              self.VMinLon = float(value)
              if self.VMinLon < -180:
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              if self.VMaxLon is not None:
                if self.VMinLon >= self.VMaxLon:
                  self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                  return False
          elif field == 'max_lon':
            if value is None:
              self.VMaxLon = None
            else:
              self.VMaxLon = float(value)
              if self.VMaxLon > 180:
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              if self.VMinLon is not None:
                if self.VMinLon >= self.VMaxLon:
                  self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                  return False
          elif field == 'def_lat':
            self.DefLat = None if value is None else float(value)
          elif field == 'def_lon':
            self.DefLon = None if value is None else float(value)
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
        elif scur == 'statistics':
          if field == 'gpu_comp':
            self.GpuComp = 0 if value is None else value
          elif field == 'ele_gain_threshold':
            if value is not None:
              self.EleGainThreshold = int(value)
          elif field == 'alt_gain_threshold':
            if value is not None:
              self.AltGainThreshold = int(value)
          elif field == 'slope_range':
            if value is not None:
              self.SlopeRange = int(value)
          elif field == 'slope_max':
            if value is not None:
              self.SlopeMax = int(value)
          elif field == 'speed_range':
            if value is not None:
              self.SpeedRange = int(value)
          elif field == 'speed_max':
            if value is not None:
              self.SpeedMax = int(value)
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == '3dviewer':
          if field == 'pano_margin':
            if value is not None:
              self.V3DPanoMargin = round(2 * float(value)) / 2
          elif field == 'subj_margin':
            if value is not None:
              self.V3DSubjMargin = round(2 * float(value)) / 2
          elif field == 'min_valid_ele':
            if value is None:
              self.V3DMinValidEle = - 5000000
            else:
              self.V3DMinValidEle = float(value)
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        else:
          self.log(0, 'cerror', hcur + ' - ' + scur)
          return False
      elif hcur == 'explorer':
        if scur == 'loading':
          if field == 'workers':
            if value in ('*', 'auto', True):
              npcores = self.cpu_pcores_count()
              self.ExplorerLoadingWorkers = 1 if npcores is None else max(1, npcores)
            elif value in (None, False):
              self.ExplorerLoadingWorkers = 1
            else:
              self.ExplorerLoadingWorkers = max(1, int(value))
          elif field == 'repatriation':
            self.ExplorerLoadingRepatriation = bool(value)
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'folders':
          fold = os.path.abspath(os.path.expandvars(l.lstrip()))
          if os.path.isdir(fold):
            self.Folders.append(fold)
        elif scur == 'statistics':
          if field == 'smooth_tracks':
            self.SmoothTracks = bool(value)
          elif field == 'smooth_range':
            if value is not None:
              self.SmoothRange = int(value)
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur[:11] == 'webmapping ':
          if field == 'alias':
            s[1] = WebMapping.WMAlias(value)
            if not s[1]:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          elif field == 'source':
            s[1][field] = value
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'media':
          if field == 'port':
            port = value or ''
            if port:
              if '-' in port:
                self.MediaPorts = port.split('-', 1)
              else:
                self.MediaPorts = (port, port)
              if not self.MediaPorts[0].isdecimal() or not self.MediaPorts[1].isdecimal():
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              self.MediaPorts = (int(self.MediaPorts[0]), int(self.MediaPorts[1]))
              if self.MediaPorts[0] > self.MediaPorts[1]:
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
          elif field == 'album':
            fold = os.path.abspath(os.path.expandvars(value))
            if os.path.isdir(fold):
              self.MediaFolders.append(fold)
          elif field == 'photos':
            self.MediaPhotos = value
          elif field == 'videos':
            self.MediaVideos = value
          elif field == 'size':
            try:
              self.MediaThumbSize = max(min(int(value), 512), 16)
            except:
              pass
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        else:
          self.log(0, 'cerror', hcur + ' - ' + scur)
          return False
      elif hcur[:9] == 'maptiles ' or hcur[:15] == 'elevationtiles ':
        if scur == 'infos':
          if field == 'alias':
            if hcur[:9] == 'maptiles ':
              s[1] = WebMercatorMap.TSAlias(value)
              s[3] = MapLegend.TLAlias(value) or {}
            else:
              s[1] = WGS84Elevation.TSAlias(value)
            if not s[1]:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          elif field in ('source', 'layer', 'matrixset', 'style', 'format') or (hcur[:15] == 'elevationtiles ' and field in ('matrix', 'nodata')):
            s[1][field] = value
            if field == 'nodata':
              try:
                s[1][field] = float(value) if '.' in value else int(value)
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
          elif field in ('overwrite_schemes', 'overwrite_names', 'slash_url') and hcur[:9] == 'maptiles ':
            s[1][field] = value
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'handling':
          if field in ('key', 'referer', 'user_agent', 'local_pattern', 'local_store', 'only_local'):
            s[2][field] = value
          elif field == 'local_expiration':
            try:
              s[2][field] = float(value)
            except:
              pass
          elif field == '"user_colon_password"':
            if value:
              if len(value) < 2 or value[:1] != '"' or value [-1:] != '"':
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              s[2]['basic_auth'] = value[1:-1]
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif hcur[:9] == 'maptiles ' and scur == 'legend':
          value = value.rstrip()
          if value:
            s[3][field] = value
          else:
            s[3].pop(field, None)
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
            s[-1][0] = len(s[-1])
          try:
            z = zoom.partition('/')
            float(z[0] or '1') / float(z[2] or '1')
          except:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
          s[-1].append([matrix, zoom])
      elif hcur[:18] == 'maptilescomposite ':
        if scur == 'layers':
          if field == 'alias':
            try:
              s[1].extend([next(i for i in range(len(self.TilesSets) - 1) if isinstance(self.TilesSets[i][1], dict) and self.TilesSets[i][1].get('alias') == layer[0]), ('x%.2f' if layer[1].startswith(('x', 'X')) else '%.2f') % max(0, min(1, (float(layer[1].lstrip('xX')[:-1]) / 100 if layer[1].endswith('%') else float(layer[1].lstrip('xX'))))), layer[2] if len(layer) >= 3 else {}] for layer in WebMercatorMap.TCAlias(value))
            except:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'layer':
          value = value.rstrip()
          if field == 'alias':
            try:
              s[1][-1][0] = next(i for i in range(len(self.TilesSets) - 1) if self.TilesSets[i][1].get('alias') == value)
              if not isinstance(self.TilesSets[s[1][-1][0]][1], dict):
                raise
            except:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          elif field == 'name':
            try:
              s[1][-1][0] = next(i for i in range(len(self.TilesSets) - 1) if self.TilesSets[i][0] == value)
              if not isinstance(self.TilesSets[s[1][-1][0]][1], dict):
                raise
            except:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          elif field == 'opacity':
            try:
              s[1][-1][1] = ('x%.2f' if value.startswith(('x', 'X')) else '%.2f') % max(0, min(1, (float(value[:-1].lstrip('xX')) / 100 if value.endswith('%') else float(value.ltrip('xX')))))
            except:
              pass
          elif field == 'substitution':
            try:
              s[1][-1][2].update((tuple(map(str.strip, value.split('='))),))
            except:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'display':
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
            if all(str(matrix) in la[2] for la in s[1]):
              raise
          except:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
          zoom = zoom.strip()
          if zoom[-1] == '*':
            zoom = zoom[:-1].strip()
            s[-1][0] = len(s[-1])
          try:
            z = zoom.partition('/')
            float(z[0] or '1') / float(z[2] or '1')
          except:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
          s[-1].append([matrix, zoom])
      elif hcur[:4] == 'map ' or hcur[:13] == 'elevationmap ':
        if scur == 'infos':
          if field == 'alias':
            if hcur[:4] == 'map ':
              s[1] = WebMercatorMap.MSAlias(value)
              s[3] = MapLegend.MLAlias(value) or {}
            else:
              s[1] = WGS84Elevation.MSAlias(value)
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
          elif field == '"user_colon_password"':
            if value:
              if len(value) < 2 or value[:1] != '"' or value [-1:] != '"':
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              s[2]['basic_auth'] = value[1:-1]
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif hcur[:4] == 'map ' and scur == 'legend':
          try:
            if field != '*':
              field = tuple(field.split(','))
          except:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
          value = value.rstrip()
          if value:
            s[3][field] = value
          else:
            s[3].pop(field, None)
        else:
          self.log(0, 'cerror', hcur + ' - ' + scur)
          return False
      elif hcur[:13] in ('elevationapi ', 'itineraryapi ') or hcur[:20] == 'reversegeocodingapi ':
        if scur == 'infos':
          if field == 'alias':
            if hcur[:13] == 'elevationapi ':
              s[1] = WGS84Elevation.ASAlias(value)
            elif hcur[:13] == 'itineraryapi ':
              s[1] = WGS84Itinerary.ASAlias(value)
            else:
              s[1] = WGS84ReverseGeocoding.ASAlias(value)
            if not s[1]:
              self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
              return False
          elif field == 'json_key':
            s[1]['key'] = tuple(map(str.strip, value.split(',')))
          elif field == 'html_regex' and hcur[:20] == 'reversegeocodingapi ':
            s[1]['regex'] = value
          elif field == 'source' or (field in ('separator', 'limit', 'parallel', 'nodata') and hcur[:13] == 'elevationapi '):
            s[1][field] = value
            if field == 'nodata':
              try:
                s[1][field] = float(value)
              except:
                pass
            elif field == 'limit':
              try:
                s[1][field] = int(value)
              except:
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
        elif scur == 'handling':
          if field in ('key', 'referer', 'user_agent'):
            s[2][field] = value
          elif field == '"user_colon_password"':
            if value:
              if len(value) < 2 or value[:1] != '"' or value [-1:] != '"':
                self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
                return False
              s[2]['basic_auth'] = value[1:-1]
          else:
            self.log(0, 'cerror', hcur + ' - ' + scur + ' - ' + l)
            return False
      else:
        self.log(0, 'cerror', hcur)
        return False
    if not self.MediaPorts:
      self.MediaPorts = self.Ports
    self.log(1, 'cloaded')
    return True

  def __new__(cls, uri=None, trk=None, bmap=None, emap=None, map_minlat=None, map_maxlat=None, map_minlon=None, map_maxlon=None, map_resolution=None, map_maxheight=2000, map_maxwidth=4000, map_dpi=None, record_map=None, cfg=os.path.dirname(os.path.abspath(__file__)) + r'\GPXTweaker.cfg', launch=None, stop=(lambda:False)):
    self = object.__new__(cls)
    self.SessionStoreValue = str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time())))
    self.SessionId = None
    self.PSessionId = None
    self.Ip = '127.0.0.1'
    self.Ports = (8000, 8000)
    self.Proxy = {'ip': '', 'port': 8080, 'auth': '', 'secure': False}
    self.JSONTiles = False
    self.JSONTilesJS = ('https://unpkg.com', 'maplibre-gl@latest/dist/maplibre-gl.js')
    self.JSONTilesCSS = ('https://unpkg.com', 'maplibre-gl@latest/dist/maplibre-gl.css')
    self.JSONTilesLib = {}
    self.TilesBufferSize = None
    self.TilesBufferThreads = None
    self.TilesHoldSize = 0
    self.ElevationTilesBufferSize = None
    self.VMinLat = - math.degrees(2 * math.atan(math.exp(math.pi)) - math.pi / 2)
    self.VMaxLat = - self.VMinLat
    self.VMinLon = -180
    self.VMaxLon = 180
    self.DefLat = None
    self.DefLon = None
    self.ExplorerLoadingWorkers = 1
    self.ExplorerLoadingRepatriation = True
    self.Folders = []
    self.MediaPorts = ''
    self.MediaFolders = []
    self.MediaPhotos = True
    self.MediaVideos = True
    self.MediaThumbSize = 64
    self.GpuComp = 0
    self.EleGainThreshold = 10
    self.AltGainThreshold = 5
    self.SlopeRange = 80
    self.SlopeMax = 50
    self.SpeedRange = 60
    self.SpeedMax = 8
    self.V3DPanoMargin = 0.5
    self.V3DSubjMargin = 2
    self.V3DMinValidEle = -100
    self.SmoothTracks = False
    self.SmoothRange = 15
    self.Mode = None
    self.EMode = None
    self.TilesSets = []
    self.MapSets = []
    self.ElevationsProviders = []
    self.ElevationMapSets = []
    self.ItinerariesProviders = []
    self.ReverseGeocodingsProviders = []
    self.Tracks = []
    self.Uri = None
    self.Track = None
    self.TrackInd = None
    self.TilesSet = None
    self.MapSet = None
    self.ElevationMapSet = None
    self.ElevationProviderSel = None
    self.ItineraryProviderSel = None
    self.ReverseGeocodingProviderSel = None
    self.WebMappingServices = []
    self.GPXTweakerInterfaceServerInstances = []
    self.HTML = None
    self.HTML3D = None
    self.HTML3DData = None
    self.HTML3DElevationProvider = None
    self.HTMLExp = None
    self.TracksBoundaries = []
    self.VMinx = None
    self.VMaxx = None
    self.VMiny = None
    self.VMaxy = None
    self.Minx = None
    self.Maxx = None
    self.Miny = None
    self.Maxy = None
    self.MTopx = None
    self.MTopy = None
    self.SLock = threading.Lock()
    self.TLock = threading.Lock()
    self.Builder = ExpatGPXBuilder()
    self.GPXLoader = None
    self.Media = None
    self.log = partial(log, 'interface')
    self.log(1, 'conf')
    try:
      if not self._load_config(cfg):
        return None
    except:
      self.log(0, 'cerror', cfg)
      return None
    if self.JSONTiles:
      print(LSTRINGS['interface']['maplibre'] % (urllib.parse.urljoin(*self.JSONTilesJS, allow_fragments=False) if self.JSONTilesJS[0][:4].lower() == 'http' else os.path.join(*self.JSONTilesJS)))
      print('')
    self.GPXTweakerInterfaceServerInstances = list(range(self.Ports[0], self.Ports[1] + 1))
    self.GPXTweakerInterfaceServerInstances.extend(range(self.MediaPorts[0], min(self.Ports[0], self.MediaPorts[1] + 1)))
    self.GPXTweakerInterfaceServerInstances.extend(range(max(self.Ports[1] + 1, self.MediaPorts[0]), self.MediaPorts[1] + 1))
    if self.Proxy['ip']:
      gen_HTTPRequest(self.Proxy)
    else:
      gen_HTTPRequest()
    err = False
    if map_minlat is not None:
      if map_minlat < self.VMinLat:
        err = True
      if bmap:
        self.VMinLat = map_minlat
    if map_maxlat is not None:
      if map_maxlat > self.VMaxLat:
        err = True
      if bmap:
        self.VMaxLat = map_maxlat
    if map_minlon is not None:
      if map_minlon < self.VMinLon:
        err = True
      if bmap:
        self.VMinLon = map_minlon
    if map_maxlat is not None:
      if map_maxlat > self.VMaxLat:
        err = True
      if bmap:
        self.VMaxLon = map_maxlon
    if err:
      self.log(0, 'berror2')
      return None
    self.DefLat = self.DefLat if self.DefLat is not None else (self.VMinLat + self.VMaxLat) / 2
    self.DefLon = self.DefLon if self.DefLon is not None else (self.VMinLon + self.VMaxLon) / 2
    if len(self.Folders) == 0:
      self.Folders.append(os.path.abspath(''))
    if uri is not None:
      u = os.path.abspath(uri)
    else:
      f1 = 0
      while f1 < len(self.Folders):
        f2 = f1 + 1
        while f2 < len(self.Folders):
          if os.path.commonpath((self.Folders[f1], self.Folders[f2])) == self.Folders[f1]:
            del self.Folders[f2]
          elif os.path.commonpath((self.Folders[f1], self.Folders[f2])) == self.Folders[f2]:
            del self.Folders[f1]
            f2 = f1 + 1
          else:
            f2 += 1
        f1 += 1
      k = lambda f: f[2].lower() == 'gpx' and not f[0].lower().endswith(' - original') and not f[0].lower().endswith(' - backup')
      uris = (os.path.join(e[0], f) for folder in self.Folders for e in os.walk(folder) for f in e[2] if k(f.rpartition('.')))
      trk = 0
      nbtrk = None
    ti = time.time()
    GCMan.disable()
    garb = []
    dminlat = self.DefLat if (not bmap or map_minlat is None) else map_minlat
    dmaxlat = self.DefLat if (not bmap or map_maxlat is None) else map_maxlat
    dminlon = self.DefLon if (not bmap or map_minlon is None) else map_minlon
    dmaxlon = self.DefLon if (not bmap or map_maxlon is None) else map_maxlon
    try:
      if uri or self.ExplorerLoadingWorkers == 1:
        trck = None
        tskipped = 0
        taborted = 0
        gaborted = 0
        if uri is None:
          u = next(uris, None)
        while u is not None:
          if stop():
            raise Interrupted()
          track = WGS84Track(self.SLock)
          trck = trck or track
          if not track.LoadGPX(u, trk, trck, self.Builder):
            if uri is None:
              if trck.Pts is None:
                if trck.Track is None:
                  gaborted += 1
                else:
                  for trk in range(1, len(trck.Track.documentElement.getChildren('trk'))):
                    trck.log(0, 'lerror', u + (' <%s>' % trk))
                  taborted += trk + 1
                  trk = 0
                  garb.append(trck)
                trck = None
                u = next(uris, None)
                continue
              else:
                taborted += 1
            else:
              if trck.Track is not None:
                garb.append(trck)
              return None
          else:
            minlat = min((p[1][0] for seg in (*track.Pts, track.Wpts) for p in seg), default=dminlat)
            maxlat = max((p[1][0] for seg in (*track.Pts, track.Wpts) for p in seg), default=dmaxlat)
            minlon = min((p[1][1] for seg in (*track.Pts, track.Wpts) for p in seg), default=dminlon)
            maxlon = max((p[1][1] for seg in (*track.Pts, track.Wpts) for p in seg), default=dmaxlon)
            if minlat < self.VMinLat or maxlat > self.VMaxLat or minlon < self.VMinLon or maxlon > self.VMaxLon:
              if uri is None:
                tskipped += 1
                self.log(0, 'berror6', color=31)
              else:
                self.log(0, 'berror4')
                garb.append(track)
                return None
            else:
              self.Tracks.append([u, track])
              self.TracksBoundaries.append((minlat, maxlat, minlon, maxlon))
          if uri is None:
            if nbtrk is None:
              nbtrk = len(track.Track.documentElement.getChildren('trk'))
            trk += 1
            if trk >= nbtrk:
              trk = 0
              nbtrk = None
              if (self.Tracks[-1][0] if self.Tracks else None) != u:
                garb.append(trck)
              trck = None
              u = next(uris, None)
          else:
            self.Uri, self.Track = self.Tracks[0]
            self.TrackInd = 0
            break
      else:
        self.GPXLoader = GPXLoader(self.ExplorerLoadingWorkers, self.ExplorerLoadingRepatriation, self.SLock)
        self.Tracks, self.TracksBoundaries, tskipped, taborted, gaborted = self.GPXLoader.Load(tuple(uris), (dminlat, dmaxlat, dminlon, dmaxlon), (self.VMinLat, self.VMaxLat, self.VMinLon, self.VMaxLon), stop)
      if tskipped or taborted or gaborted:
        self.log(0, 'bloaded2', len(self.Tracks), time.time() - ti, tskipped, taborted, gaborted, color=31)
      else:
        self.log(0, 'bloaded1', len(self.Tracks), time.time() - ti, color=32)
      minlat = min((b[0] for b in self.TracksBoundaries), default=(self.DefLat if (not bmap or map_minlat is None) else map_minlat))
      maxlat = max((b[1] for b in self.TracksBoundaries), default=(self.DefLat if (not bmap or map_maxlat is None) else map_maxlat))
      minlon = min((b[2] for b in self.TracksBoundaries), default=(self.DefLon if (not bmap or map_minlon is None) else map_minlon))
      maxlon = max((b[3] for b in self.TracksBoundaries), default=(self.DefLon if (not bmap or map_maxlon is None) else map_maxlon))
      if minlat < self.VMinLat or maxlat > self.VMaxLat or minlon < self.VMinLon or maxlon > self.VMaxLon:
        self.log(0, 'berror4')
        return None
      clamp_lat = lambda v: min(self.VMaxLat, max(self.VMinLat, v))
      clamp_lon = lambda v: min(self.VMaxLon, max(self.VMinLon, v))
      if stop():
        raise Interrupted()
      if bmap:
        self.Mode = 'map'
        self.Map = WebMercatorMap()
        rec = False
        if '://' in bmap or ':\\' in bmap:
          if not self.Map.LoadMap(bmap, *(WGS84WebMercator.WGS84toWebMercator(map_minlat, map_minlon) if not None in (map_minlat, map_minlon) else (None, None)), *(WGS84WebMercator.WGS84toWebMercator(map_maxlat, map_maxlon) if not None in (map_maxlat, map_maxlon) else (None, None)), resolution=map_resolution):
            self.log(0, 'berror')
            return None
          self.TilesSets = [['Map']]
        else:
          for i in range(len(self.MapSets)):
            if self.MapSets[i][0].lower() == bmap.lower() or bmap == ' ':
              self.MapSet = i
              break
          if self.MapSet is None:
            self.log(0, 'berror3', bmap)
            return None
          if not self.Map.FetchMap(self.MapSets[self.MapSet][1], clamp_lat(minlat - 0.014 if map_minlat is None else map_minlat), clamp_lat(maxlat + 0.014 if map_maxlat is None else map_maxlat), clamp_lon(minlon - 0.019 if map_minlon is None else map_minlon), clamp_lon(maxlon + 0.019 if map_maxlon is None else map_maxlon), map_maxheight, map_maxwidth, dpi=map_dpi, **self.MapSets[self.MapSet][2]):
            self.log(0, 'berror')
            return None
          self.TilesSets = [[self.MapSets[self.MapSet][0]]]
          rec = record_map is not None
        if not hasattr(self.Map, 'WMS_BBOX'):
          bbox = dict(zip(('{minx}', '{miny}', '{maxx}', '{maxy}'), self.Map.MapInfos['bbox'].split(',')))
        else:
          bbox = dict(zip(self.Map.WMS_BBOX.split(','), self.Map.MapInfos['bbox'].split(',')))
        self.VMinx, self.VMiny, self.VMaxx, self.VMaxy = [float(bbox[k]) for k in ('{minx}', '{miny}', '{maxx}', '{maxy}')]
        self.MTopx = self.VMinx
        self.MTopy = self.VMaxy
        map_minlat, map_minlon = WGS84WebMercator.WebMercatortoWGS84(self.VMinx, self.VMiny)
        map_maxlat, map_maxlon = WGS84WebMercator.WebMercatortoWGS84(self.VMaxx, self.VMaxy)
        if rec:
          self.Map.SaveMap(os.path.join(record_map.rstrip('\\') + '\\', 'Map[%s][%.4f,%.4f,%.4f,%.4f][%dx%d](%.0f).%s' % (self.MapSets[self.MapSet][0], map_minlat, map_minlon, map_maxlat, map_maxlon, self.Map.MapInfos['width'], self.Map.MapInfos['height'], time.time(), WebMercatorMap.MIME_EXT.get(self.Map.MapInfos['format'], 'img'))))
        if next((p[1][0] for uri, track in self.Tracks for seg in (*track.Pts, track.Wpts) for p in seg), None) is not None:
          if minlat < map_minlat or maxlat > map_maxlat or minlon < map_minlon or maxlon > map_maxlon:
            self.log(0, 'berror4')
            return None
        self.VMinLat = max(self.VMinLat, map_minlat)
        self.VMaxLat = min(self.VMaxLat, map_maxlat)
        self.VMinLon = max(self.VMinLon, map_minlon)
        self.VMaxLon = min(self.VMaxLon, map_maxlon)
        if self.VMinLat >= self.VMaxLat or self.VMinLon >= self.VMaxLon:
          self.log(0, 'berror2')
          return None
        self.VMinx, self.VMiny = WGS84WebMercator.WGS84toWebMercator(self.VMinLat, self.VMinLon)
        self.VMaxx, self.VMaxy = WGS84WebMercator.WGS84toWebMercator(self.VMaxLat, self.VMaxLon)
        self.DefLat = (self.VMinLat + self.VMaxLat) / 2
        self.DefLon = (self.VMinLon + self.VMaxLon) / 2
      else:
        if len(self.TilesSets) == 0 or not self.TilesBufferSize or not self.TilesBufferThreads:
          self.log(0, 'berror5')
          return None
        self.Mode = 'tiles'
        self.Map = WebMercatorMap(self.TilesBufferSize, self.TilesBufferThreads)
        self.TilesSet = 0
        self.VMinx, self.VMiny = WGS84WebMercator.WGS84toWebMercator(self.VMinLat, self.VMinLon)
        self.VMaxx, self.VMaxy = WGS84WebMercator.WGS84toWebMercator(self.VMaxLat, self.VMaxLon)
        self.MTopx = self.VMinx
        self.MTopy = self.VMaxy
      if self.VMaxx - self.VMinx <= 5 or self.VMaxy - self.VMiny <= 5:
        self.log(0, 'berror')
        return None
      self.Minx, self.Miny = WGS84WebMercator.WGS84toWebMercator(clamp_lat(minlat - 0.008), clamp_lon(minlon - 0.011))
      self.Maxx, self.Maxy = WGS84WebMercator.WGS84toWebMercator(clamp_lat(maxlat + 0.008), clamp_lon(maxlon + 0.011))
      for t in range(len(self.TracksBoundaries)):
        self.TracksBoundaries[t] = tuple(b[i] for i in (0,1) for b in (WGS84WebMercator.WGS84toWebMercator(clamp_lat(self.TracksBoundaries[t][0] - 0.008), clamp_lon(self.TracksBoundaries[t][2] - 0.011)), WGS84WebMercator.WGS84toWebMercator(clamp_lat(self.TracksBoundaries[t][1] + 0.008), clamp_lon(self.TracksBoundaries[t][3] + 0.011))))
      if stop():
        raise Interrupted()
      if emap:
        self.Elevation = WGS84Elevation()
        self.ElevationsProviders = []
        if '://' in emap or ':\\' in emap:
          if self.Elevation.LoadMap(emap):
            self.EMode = 'map'
            self.ElevationProvider = partial(self.Elevation.WGS84toElevation, infos=None)
            self.ElevationsProviders = [['Map']]
            self.log(1, 'elevation', emap)
          else:
            self.ElevationProvider = None
            self.log(0, 'eerror', emap)
        else:
          for i in range(len(self.ElevationMapSets)):
            if self.ElevationMapSets[i][0].lower() == emap.lower() or emap == ' ':
              self.ElevationMapSet = i
              break
          if self.ElevationMapSet is None:
            self.log(0, 'eerror', emap)
          else:
            if self.Elevation.FetchMap(self.ElevationMapSets[self.ElevationMapSet][1], clamp_lat(minlat - 0.014 if map_minlat is None else map_minlat), clamp_lat(maxlat + 0.014 if map_maxlat is None else map_maxlat), clamp_lon(minlon - 0.019 if map_minlon is None else map_minlon), clamp_lon(maxlon + 0.019 if map_maxlon is None else map_maxlon), map_maxheight, map_maxwidth, dpi=map_dpi, **self.ElevationMapSets[self.ElevationMapSet][2]):
              self.EMode = 'map'
              self.ElevationProvider = partial(self.Elevation.WGS84toElevation, infos=None)
              self.ElevationsProviders = [[self.ElevationMapSets[self.ElevationMapSet][0]]]
              self.log(1, 'elevation', self.ElevationMapSets[self.ElevationMapSet][0])
              if record_map is not None:
                self.Elevation.SaveMap(os.path.join(record_map.rstrip('\\') + '\\', 'ElevationMap[%s][%.4f,%.4f,%.4f,%.4f][%dx%d](%.0f).%s' % (self.ElevationMapSets[self.ElevationMapSet][0], *map(float, self.Elevation.MapInfos['bbox'].split(',')), self.Elevation.MapInfos['width'], self.Elevation.MapInfos['height'], time.time(), {'image/x-bil;bits=32': 'bil.xz', 'image/hgt': 'hgt.xz'}.get(self.Elevation.MapInfos['format'], 'img'))))
            else:
              self.ElevationProvider = None
              self.log(0, 'eerror', emap)
      elif len(self.ElevationsProviders) > 0:
        self.ElevationProviderSel = 0
        self.Elevation = WGS84Elevation(self.ElevationTilesBufferSize, self.TilesBufferThreads)
        if 'layer' in self.ElevationsProviders[0][1]:
          self.EMode = 'tiles'
          self.Elevation.SetTilesProvider((0, self.ElevationsProviders[0][1].get('matrix')), self.ElevationsProviders[0][1], self.ElevationsProviders[0][1].get('matrix'), **self.ElevationsProviders[0][2])
          self.ElevationProvider = partial(self.Elevation.WGS84toElevation, infos=self.ElevationsProviders[0][1], matrix=self.ElevationsProviders[0][1].get('matrix'), **self.ElevationsProviders[0][2])
          self.log(1, 'elevation', self.ElevationsProviders[0][0])
        else:
          self.EMode = 'api'
          self.ElevationProvider = partial(self.Elevation.RequestElevation, self.ElevationsProviders[0][1], **self.ElevationsProviders[0][2])
          self.log(1, 'elevation', self.ElevationsProviders[0][0])
      else:
        self.log(0, 'eerror', '-')
        self.ElevationProvider = None
      if stop():
        raise Interrupted()
      self.Itinerary = WGS84Itinerary()
      if len(self.ItinerariesProviders) > 0:
        self.ItineraryProviderSel = 0
        self.ItineraryProviderConnection = [[None]]
        def ItineraryProvider(points):
          psel = self.ItineraryProviderSel
          try:
            pcon = self.ItineraryProviderConnection.pop()
          except:
            pcon = None
          iti = self.Itinerary.RequestItinerary(self.ItinerariesProviders[psel][1], points, **self.ItinerariesProviders[psel][2], pconnection=pcon)
          if pcon:
            self.ItineraryProviderConnection.append(pcon)
          return iti
        self.ItineraryProvider = ItineraryProvider
        self.log(1, 'itinerary', self.ItinerariesProviders[0][0])
      else:
        self.ItineraryProvider = None
      self.ReverseGeocoding = WGS84ReverseGeocoding()
      if len(self.ReverseGeocodingsProviders) > 0:
        self.ReverseGeocodingProviderSel = 0
        self.ReverseGeocodingProviderConnection = [[None]]
        def ReverseGeocodingProvider(point):
          psel = self.ReverseGeocodingProviderSel
          try:
            pcon = self.ReverseGeocodingProviderConnection.pop()
          except:
            pcon = None
          desc = self.ReverseGeocoding.RequestDescription(self.ReverseGeocodingsProviders[psel][1], point, **self.ReverseGeocodingsProviders[psel][2], pconnection=pcon)
          if pcon:
            self.ReverseGeocodingProviderConnection.append(pcon)
          return desc
        self.ReverseGeocodingProvider = ReverseGeocodingProvider
        self.log(1, 'reversegeocoding', self.ReverseGeocodingsProviders[0][0])
      else:
        self.ReverseGeocodingProvider = None
      self.Media = GeotaggedMedia(self.MediaFolders, self.MediaPhotos, self.MediaVideos, (self.VMinx, self.VMiny, self.VMaxx, self.VMaxy))
      self.Legend = MapLegend()
      self.Map.LinkLegend(self.Legend)
      if self.JSONTiles:
        self.JSONTiles = JSONTiles(len(self.TilesSets))
        self.Map.LinkJSONTiles(self.JSONTiles)
      if stop():
        raise Interrupted()
      if uri is not None:
        self.HTML = ''
      else:
        self.HTMLExp = ''
      if launch is not None:
        if not self.run():
          self.HTML = self.HTMLExp = None
          self.log(0, 'berror')
          return None
        add = 'http://%s:%s/GPX%s.html' % (self.Ip, self.Ports[0], ('Tweaker' if uri is not None else 'Explorer'))
        print('')
        if launch:
          webbrowser.open(add)
        else:
          try:
            if subprocess.run('echo %s| clip' % add, shell=True).returncode != 0:
              raise
            print(LSTRINGS['parser']['openc'] % add)
          except:
            print(LSTRINGS['parser']['open'] % add)
      return self
    except Interrupted:
      self.log(0, 'berrori')
      return None
    except:
      self.log(0, 'berror')
      return None
    finally:
      def _unlink():
        for trcks in (garb, (tr[1] for tr in self.Tracks)) if (self.HTML is None and self.HTMLExp is None) else (garb, ):
          for trck in trcks:
            if not isinstance(trck, WGS84TrackProxy):
              trck.ULock = None
              trck.OTrack = trck.STrack = None
              del trck.Track
      if self.GPXLoader and (self.HTML is None and self.HTMLExp is None):
        self.GPXLoader.Close()
      u_thread = threading.Thread(target=_unlink)
      u_thread.start()
      GCMan.restore()

  def _build_pathes(self):
    def _coord_to_vb(x, y):
      return '%.1f %.1f' % (x - self.Minx, self.Maxy - y)
    pathes = ''
    pathes = ''.join(GPXTweakerWebInterfaceServer.HTML_PATH_TEMPLATE.replace('##WIDTH##', 'calc(%.1fpx / var(--scale))' % (self.Maxx - self.Minx)).replace('##HEIGHT##', 'calc(%.1fpx / var(--scale))' % (self.Maxy - self.Miny)).replace('##LEFT##', 'calc(0px / var(--scale))').replace('##TOP##', 'calc(0px / var(--scale))').replace('##VIEWBOX##', '%.1f %.1f %.1f %.1f' % (0, 0, self.Maxx - self.Minx, self.Maxy - self.Miny)).replace('##ARROWS##', '&rsaquo; ' * 500) % (s, s, 'M0 0' + ''.join(' M' + _coord_to_vb(*pt[1]) for pt in self.Track.WebMercatorPts[s][0:1]) + ''.join(' L' + _coord_to_vb(*pt[1]) for pt in self.Track.WebMercatorPts[s][1:]), s) for s in range(len(self.Track.WebMercatorPts)))
    return pathes

  def _build_waypoints(self):
    return ''.join((GPXTweakerWebInterfaceServer.HTML_WAYPOINT_TEMPLATE % (*([pt[0]] * 6), *(a for b in zip(*([[pt[0]] * 5] * 3), (*pt[1][0:3], escape(pt[1][3]), escape(pt[1][4]))) for a in b))) for pt in self.Track.Wpts)

  def _build_points(self):
    return ''.join(GPXTweakerWebInterfaceServer.HTML_SEGMENT_TEMPLATE % (*([s] * 5), s + 1) + ''.join(GPXTweakerWebInterfaceServer.HTML_POINT_TEMPLATE % (*([pt[0]] * 6), *(a for b in zip(*([[pt[0]] * 5] * 3), (*pt[1][0:4], escape(pt[1][4]))) for a in b)) for pt in self.Track.Pts[s]) + '</div>' for s in range(len(self.Track.Pts)))

  def _build_waydots(self):
    return ''.join(GPXTweakerWebInterfaceServer.HTML_WAYDOT_TEMPLATE % (pt[0], *(lambda x, y: (x - self.Minx, self.Maxy - y))(*pt[1])) for pt in self.Track.WebMercatorWpts)

  def _build_dots(self):
    return ''.join(GPXTweakerWebInterfaceServer.HTML_DOT_TEMPLATE % (pt[0], *(lambda x, y: (x - self.Minx, self.Maxy - y))(*pt[1])) for s in range(len(self.Track.WebMercatorPts)) for pt in self.Track.WebMercatorPts[s])

  def _build_tsets(self):
    return ''.join('<option %svalue="%s">%s</option>' % (('' if (len(tset[-1]) > 1 and (self.JSONTiles or ((tset[1].get('format') != 'application/json') if isinstance(tset[1], dict) else all(self.TilesSets[tsos[0]][1].get('format') != 'application/json' for tsos in tset[1])))) else 'style="display:none;"'), *([escape(tset[0])] * 2)) for tset in self.TilesSets)

  def _build_esets(self):
    return ''.join('<option value="%s">%s</option>' % (*([escape(epro[0])] * 2),) for epro in self.ElevationsProviders)

  def _build_isets(self):
    return ''.join('<option value="%s">%s</option>' % (*([escape(ipro[0])] * 2),) for ipro in self.ItinerariesProviders)

  def _build_tlayers(self):
    return ', '.join('[%s, [%s]]' % (i, ', '.join('[%s, "%s"]' % (to[0], to[1]) for to in t[1])) for i, t in enumerate(self.TilesSets) if len(t) >= 2 and isinstance(t[1], list))

  def BuildHTML(self, defx=None, defy=None):
    if self.HTML is None:
      return False
    if defx is None or defy is None:
      defx, defy = WGS84WebMercator.WGS84toWebMercator(self.DefLat, self.DefLon)
    declarations = GPXTweakerWebInterfaceServer.HTML_DECLARATIONS_TEMPLATE.replace('##PORTMIN##', str(self.Ports[0])).replace('##PORTMAX##', str(self.Ports[1])).replace('##GPUCOMP##', str(self.GpuComp)).replace('##MODE##', self.Mode).replace('##VMINX##', str(self.VMinx)).replace('##VMAXX##', str(self.VMaxx)).replace('##VMINY##', str(self.VMiny)).replace('##VMAXY##', str(self.VMaxy)).replace('##DEFX##', str(defx)).replace('##DEFY##', str(defy)).replace('##TTOPX##', str(self.MTopx)).replace('##TTOPY##', str(self.MTopy)).replace('##TWIDTH##', '0' if self.Mode == 'tiles' else str(self.Map.MapInfos['width'])).replace('##THEIGHT##', '0' if self.Mode == 'tiles' else str(self.Map.MapInfos['height'])).replace('##TEXT##', '' if self.Mode == 'tiles' else (WebMercatorMap.MIME_DOTEXT.get(self.Map.MapInfos.get('format'), '.img'))).replace('##TSCALE##', '1' if self.Mode =='tiles' else str(self.Map.MapResolution)).replace('##HTOPX##', str(self.Minx)).replace('##HTOPY##', str(self.Maxy)).replace('##THOLDSIZE##', str(self.TilesHoldSize)).replace('##TLAYERS##', self._build_tlayers()).replace('##TMAPLIBRE##', 'false' if self.JSONTiles else 'null')
    pathes = self._build_pathes()
    waydots = self._build_waydots()
    dots = self._build_dots()
    waypoints = self._build_waypoints()
    points = self._build_points()
    tsets = self._build_tsets()
    esets = self._build_esets()
    isets = self._build_isets()
    self.HTML = GPXTweakerWebInterfaceServer.HTML_TEMPLATE
    if self.HTMLExp is not None:
      self.HTML = self.HTML.replace('//        window.onunload', '        window.onunload').replace('//      document.addEventListener("DOMContentLoaded"', '      document.addEventListener("DOMContentLoaded"')
    self.HTML = self.HTML.replace('##DECLARATIONS##', declarations).replace('##TMAPLIBREJS##', self.JSONTilesJS[1].replace('"', r'\"') if self.JSONTiles else '').replace('##TMAPLIBRECSS##', self.JSONTilesCSS[1].replace('"', r'\"') if self.JSONTiles else '').replace('##TSETS##', tsets).replace('##ESETS##', esets).replace('##ISETS##', isets).replace('##EGTHRESHOLD##', str(self.EleGainThreshold)).replace('##AGTHRESHOLD##', str(self.AltGainThreshold)).replace('##SLRANGE##', str(self.SlopeRange)).replace('##SLMAX##', str(self.SlopeMax)).replace('##SPRANGE##', str(self.SpeedRange)).replace('##SPMAX##', str(self.SpeedMax)).replace('##SMRANGE##', str(self.SmoothRange)).replace('##V3DPMARGIN##', str(self.V3DPanoMargin)).replace('##V3DSMARGIN##', str(self.V3DSubjMargin)).replace('##NAME##', escape(self.Track.Name)).replace('##WAYPOINTTEMPLATE##', GPXTweakerWebInterfaceServer.HTML_WAYPOINT_TEMPLATE.replace('checked', '')).replace('##POINTTEMPLATE##',  GPXTweakerWebInterfaceServer.HTML_POINT_TEMPLATE.replace('checked', '')).replace('##WAYDOTTEMPLATE##',  GPXTweakerWebInterfaceServer.HTML_WAYDOT_TEMPLATE).replace('##DOTTEMPLATE##',  GPXTweakerWebInterfaceServer.HTML_DOT_TEMPLATE).replace('#<#WAYPOINTS#>#', waypoints).replace('#<#WAYDOTS#>#', waydots).replace('#<#PATHES#>#', pathes).replace('#<#DOTS#>#', dots).replace('#<#POINTS#>#', points)
    self.log(2, 'built')
    return True

  def Build3DHTML(self, mode3d, margin=0.5):
    self.HTML3D = None
    self.HTML3DData = None
    if next((p for seg in self.Track.Pts for p in seg), None) is None:
      return False
    self.log(1, '3dbuild')
    clamp_lat = lambda v: min(self.VMaxLat, max(self.VMinLat, v))
    clamp_lon = lambda v: min(self.VMaxLon, max(self.VMinLon, v))
    marginlat = margin * 180000 / (WGS84WebMercator.R * math.pi)
    minlat = clamp_lat(min(p[1][0] for seg in self.Track.Pts for p in seg) - marginlat)
    maxlat = clamp_lat(max(p[1][0] for seg in self.Track.Pts for p in seg) + marginlat)
    marginlon = marginlat / math.cos ((minlat + maxlat) / 360 * math.pi)
    minlon = clamp_lon(min(p[1][1] for seg in self.Track.Pts for p in seg) - marginlon)
    maxlon = clamp_lon(max(p[1][1] for seg in self.Track.Pts for p in seg) + marginlon)
    if self.Elevation.Map and self.HTML3DElevationProvider == self.ElevationProviderSel:
      tminlat, tminlon, tmaxlat, tmaxlon = list(map(float, self.Elevation.MapInfos['bbox'].split(',')))
      if tminlat > minlat or tminlon > minlon or tmaxlat < maxlat or tmaxlon < maxlon:
        if self.EMode == 'map':
          self.log(0, '3derror1')
          return False
        else:
          self.Elevation.Map = None
          self.Elevation.MapInfos = {}
          self.Elevation.MapResolution = None
    else:
      self.Elevation.Map = None
      self.Elevation.MapInfos = {}
      self.Elevation.MapResolution = None
    if not self.Elevation.Map:
      try:
        if self.EMode == 'tiles':
          infos = {**self.ElevationsProviders[self.ElevationProviderSel][1]}
          if not self.Elevation.AssembleMap(infos, self.ElevationsProviders[self.ElevationProviderSel][1].get('matrix'), minlat, maxlat, minlon, maxlon, **self.ElevationsProviders[self.ElevationProviderSel][2], threads=(self.TilesBufferThreads or 10), tiles_cache=self.Elevation.Tiles):
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
      tminlat, tminlon, tmaxlat, tmaxlon = list(map(float, self.Elevation.MapInfos['bbox'].split(',')))
      self.HTML3DElevationProvider = self.ElevationProviderSel
    if self.Elevation.MapInfos.get('format') not in ('image/x-bil;bits=32', 'image/hgt'):
      self.log(0, '3derror1')
      return False
    scale = self.Elevation.MapResolution
    width = self.Elevation.MapInfos['width']
    height = self.Elevation.MapInfos['height']
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
      if mode3d != 's':
        step = math.sqrt((maxpx - minpx + 1) * (maxpy - minpy + 1) / 262144)
      else:
        step = max(min(15 / (WGS84Map.CRS_MPU * scale), max(10 / (WGS84Map.CRS_MPU * scale), math.sqrt((maxpx - minpx + 1) * (maxpy - minpy + 1) / 262144))), math.sqrt((maxpx - minpx + 1) * (maxpy - minpy + 1) / 4194304))
      c = math.sqrt(math.cos((minlat + maxlat) / 2))
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
    ef = lambda e, no_data=self.Elevation.MapInfos.get('nodata'), min_valid_ele=self.V3DMinValidEle: e if e != no_data and e >= min_valid_ele else 0
    accel = ctypes.sizeof(ctypes.c_float if e_f[1] == 'f' else ctypes.c_short) == e_s
    if accel:
      if sys.byteorder == ('little' if e_f[0] == '<' else 'big'):
        _e_m = memoryview(self.Elevation.Map).cast(e_f[1])
      else:
        _e_m = array.array(e_f[1], self.Elevation.Map)
        _e_m.byteswap()
      eles = tuple(ef(_e_m[py + px]) for _lpy in (map(width.__mul__,lpy),) for py in _lpy for px in lpx)
      minele = min(eles)
      maxele = max(max(eles), minele + 1)
    else:
      _e_f = e_f[0] + str(ncol) + e_f[1]
      _e_m_ = self.Elevation.Map
      eles = tuple(tuple(map(ef, struct.unpack(_e_f, b''.join(_e_m_[_py_0 + _px: _py_1 + _px] for _px in _lpx)))) for _lpx in (tuple(map(e_s.__mul__, lpx)),) for _py_0 in map((e_s * width).__mul__,lpy) for _py_1 in (e_s + _py_0,))
      minele = min(min(eles[row]) for row in range(nrow))
      maxele = max(max(max(eles[row]) for row in range(nrow)), minele + 1)
    minx, miny = WGS84WebMercator.WGS84toWebMercator(minlat, minlon)
    maxx, maxy = WGS84WebMercator.WGS84toWebMercator(maxlat, maxlon)
    xy_den = max(maxx - minx, maxy - miny) / 2
    moyx = (minx + maxx) / 2
    moyy = (miny + maxy) / 2
    cor = math.cosh(moyy / WGS84WebMercator.R)
    z_den = (maxele - minele) / 2 * cor
    if xy_den > z_den:
      den = xy_den
      zfactor = xy_den / z_den
    else:
      den = z_den
      zfactor = 1
    _cor = cor / den
    _minele =  minele * _cor + 1
    if accel:
      self.HTML3DData = b''.join((struct.pack('=L', ncol), struct.pack('=%df' % ncol, *((WGS84WebMercator.WGS84toWebMercator(tmaxlat, tminlon + (px + 0.5) * scale)[0] - moyx) / den for px in lpx)), struct.pack('=L', nrow), struct.pack('=%df' % nrow, *((WGS84WebMercator.WGS84toWebMercator(tmaxlat - (py + 0.5) * scale, tminlon)[1] - moyy) / den for py in lpy)), struct.pack('=L', ncol * nrow), struct.pack('=%df' % (nrow * ncol), *(ele * _cor - _minele for ele in eles)), struct.pack('=L', len(self.Track.WebMercatorPts)), b''.join((struct.pack('=L%df' % (2 * len(self.Track.WebMercatorPts[s])), len(self.Track.WebMercatorPts[s]), *(v for pt in self.Track.WebMercatorPts[s] for v in ((pt[1][0] - moyx) / den, (pt[1][1] - moyy) / den)))) for s in range(len(self.Track.WebMercatorPts)))))
    else:
      self.HTML3DData = b''.join((struct.pack('=L', ncol), struct.pack('=%df' % ncol, *((WGS84WebMercator.WGS84toWebMercator(tmaxlat, tminlon + (px + 0.5) * scale)[0] - moyx) / den for px in lpx)), struct.pack('=L', nrow), struct.pack('=%df' % nrow, *((WGS84WebMercator.WGS84toWebMercator(tmaxlat - (py + 0.5) * scale, tminlon)[1] - moyy) / den for py in lpy)), struct.pack('=L', ncol * nrow), struct.pack('=%df' % (nrow * ncol), *(eles[r][c] * _cor - _minele for r in range(nrow) for c in range(ncol))), struct.pack('=L', len(self.Track.WebMercatorPts)), b''.join((struct.pack('=L%df' % (2 * len(self.Track.WebMercatorPts[s])), len(self.Track.WebMercatorPts[s]), *(v for pt in self.Track.WebMercatorPts[s] for v in ((pt[1][0] - moyx) / den, (pt[1][1] - moyy) / den)))) for s in range(len(self.Track.WebMercatorPts)))))
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
    ax = den / (tmaxx - tminx)
    bx = (moyx - tminx) / (tmaxx - tminx)
    ay = den / (tmaxy - tminy)
    by = (moyy - tminy) / (tmaxy - tminy)
    declarations = (GPXTweakerWebInterfaceServer.HTML_3DP_DECLARATIONS_TEMPLATE if mode3d != 's' else GPXTweakerWebInterfaceServer.HTML_3DS_DECLARATIONS_TEMPLATE).replace('##PORTMIN##', str(self.Ports[0])).replace('##PORTMAX##', str(self.Ports[1])).replace('##ZFACTMAX##', str(zfactor)).replace('##MPOS##', '%f, %f, %f, %f' % (ax, ay, bx, by)).replace('##TMINROW##', str(minrow)).replace('##TMINCOL##', str(mincol)).replace('##TMAXROW##', str(maxrow)).replace('##TMAXCOL##', str(maxcol)).replace('##SCALE##', str(den / cor)).replace('##PPOS##', '%f, %f, %f, %f, %f' % (den, moyx, moyy, minele, cor))
    self.HTML3D = (GPXTweakerWebInterfaceServer.HTML_3DP_TEMPLATE if mode3d != 's' else GPXTweakerWebInterfaceServer.HTML_3DS_TEMPLATE).replace('##DECLARATIONS##', declarations).replace('##TILEPATH##', tpath).replace('##TILEMAXPENDING##', str((self.TilesBufferThreads or 10) * 2)).replace('##RGSETS##', '' if mode3d != 's' else ''.join('<option value="%s">%s</option>' % (*([escape(rgpro[0])] * 2),) for rgpro in self.ReverseGeocodingsProviders))
    self.log(0, '3dbuilt')
    return True

  def _build_folders_exp(self):
    return ''.join(GPXTweakerWebInterfaceServer.HTMLExp_FOLDER_TEMPLATE % (f, *([f, escape(self.Folders[f])] * 2)) for f in range(len(self.Folders)))

  def _build_path_exp(self, t):
    return GPXTweakerWebInterfaceServer.HTMLExp_PATH_TEMPLATE.replace('##WIDTH##', 'calc(%.1fpx / var(--scale))' % (self.TracksBoundaries[t][1] - self.TracksBoundaries[t][0])).replace('##HEIGHT##', 'calc(%.1fpx / var(--scale))' % (self.TracksBoundaries[t][3] - self.TracksBoundaries[t][2])).replace('##LEFT##', 'calc(%.1fpx / var(--scale))' % (self.TracksBoundaries[t][0] - self.Minx)).replace('##TOP##', 'calc(%.1fpx / var(--scale))' % (self.Maxy - self.TracksBoundaries[t][3])).replace('##VIEWBOX##', '%.1f %.1f %.1f %.1f' % (0, 0, self.TracksBoundaries[t][1] - self.TracksBoundaries[t][0], self.TracksBoundaries[t][3] - self.TracksBoundaries[t][2])).replace('##ARROWS##', '&rsaquo; ' * 500) % (t, *([self.Tracks[t][1].Color or '#000000'] * 2), t, escape(self.Tracks[t][1].Name or ''), t, t)

  def _build_pathes_exp(self):
    return ''.join(self._build_path_exp(t) for t in range(len(self.Tracks)))

  def _build_track_exp(self, t):
    return GPXTweakerWebInterfaceServer.HTMLExp_TRACK_TEMPLATE % (*([t] * 3), escape(self.Tracks[t][0]), *([t] * 2), *([escape(self.Tracks[t][1].Name or '')] * 2), t, self.Tracks[t][1].Color or '#000000', t, *(a for b in zip(*([[t] * 5] * 3), map(escape, (self.Tracks[t][1].Name or '', *self.Tracks[t][0].rpartition('\\')[::-2], '', '{jtrackcontent}'.format_map(LSTRINGS['interface']) % (len(self.Tracks[t][1].Pts) , sum(len(s) for s in self.Tracks[t][1].Pts), len(self.Tracks[t][1].Wpts))))) for a in b))

  def _build_tracks_exp(self):
    return ''.join(self._build_track_exp(t) for t in range(len(self.Tracks)))

  def _build_waydots_exp(self, t):
    def _coord_to_vb(x, y):
      return '%.1f' % (x - self.TracksBoundaries[t][0]), '%.1f' % (self.TracksBoundaries[t][3] - y)
    return GPXTweakerWebInterfaceServer.HTMLExp_WAYDOTS_TEMPLATE.replace('##WIDTH##', 'calc(%.1fpx / var(--scale))' % (self.TracksBoundaries[t][1] - self.TracksBoundaries[t][0])).replace('##HEIGHT##', 'calc(%.1fpx / var(--scale))' % (self.TracksBoundaries[t][3] - self.TracksBoundaries[t][2])).replace('##LEFT##', 'calc(%.1fpx / var(--scale))' % (self.TracksBoundaries[t][0] - self.Minx)).replace('##TOP##', 'calc(%.1fpx / var(--scale))' % (self.Maxy - self.TracksBoundaries[t][3])).replace('##VIEWBOX##', '%.1f %.1f %.1f %.1f' % (0, 0, self.TracksBoundaries[t][1] - self.TracksBoundaries[t][0], self.TracksBoundaries[t][3] - self.TracksBoundaries[t][2])) % (t, (self.Tracks[t][1].Color or '#000000'), ''.join(GPXTweakerWebInterfaceServer.HTMLExp_WAYDOT_TEMPLATE % (*_coord_to_vb(*WGS84Track.WGS84toWebMercator(*pt[1][0:2])), escape(pt[1][4] or '')) for pt in self.Tracks[t][1].Wpts))

  def _build_waydotss_exp(self):
    return ''.join(self._build_waydots_exp(t) for t in range(len(self.Tracks)))

  def _build_wmsets(self):
    return ''.join('<option value="%s">%s</option>' % (escape(wmpro[1].get('source', '')), escape(wmpro[0])) for wmpro in self.WebMappingServices)

  def BuildHTMLExp(self):
    if self.HTMLExp is None:
      return False
    defx, defy = WGS84WebMercator.WGS84toWebMercator(self.DefLat, self.DefLon)
    declarations = GPXTweakerWebInterfaceServer.HTML_DECLARATIONS_TEMPLATE.replace('##PORTMIN##', str(self.Ports[0])).replace('##PORTMAX##', str(self.Ports[1])).replace('##GPUCOMP##', str(self.GpuComp)).replace('##MODE##', self.Mode).replace('##VMINX##', str(self.VMinx)).replace('##VMAXX##', str(self.VMaxx)).replace('##VMINY##', str(self.VMiny)).replace('##VMAXY##', str(self.VMaxy)).replace('##DEFX##', str(defx)).replace('##DEFY##', str(defy)).replace('##TTOPX##', str(self.MTopx)).replace('##TTOPY##', str(self.MTopy)).replace('##TWIDTH##', '0' if self.Mode == 'tiles' else str(self.Map.MapInfos['width'])).replace('##THEIGHT##', '0' if self.Mode == 'tiles' else str(self.Map.MapInfos['height'])).replace('##TEXT##', '' if self.Mode == 'tiles' else (WebMercatorMap.MIME_DOTEXT.get(self.Map.MapInfos.get('format'), '.img'))).replace('##TSCALE##', '1' if self.Mode =='tiles' else str(self.Map.MapResolution)).replace('##HTOPX##', str(self.Minx)).replace('##HTOPY##', str(self.Maxy)).replace('##THOLDSIZE##', str(self.TilesHoldSize)).replace('##TLAYERS##', self._build_tlayers()).replace('##TMAPLIBRE##', 'false' if self.JSONTiles else 'null')
    folders = self._build_folders_exp()
    pathes = self._build_pathes_exp()
    waydots = self._build_waydotss_exp()
    tracks = self._build_tracks_exp()
    tsets = self._build_tsets()
    esets = self._build_esets()
    wmsets = self._build_wmsets()
    self.HTMLExp = GPXTweakerWebInterfaceServer.HTMLExp_TEMPLATE.replace('##DECLARATIONS##', declarations).replace('##TMAPLIBREJS##', self.JSONTilesJS[1].replace('"', r'\"') if self.JSONTiles else '').replace('##TMAPLIBRECSS##', self.JSONTilesCSS[1].replace('"', r'\"') if self.JSONTiles else '').replace('##MPORTMIN##', str(self.MediaPorts[0])).replace('##MPORTMAX##', str(self.MediaPorts[1])).replace('##TSETS##', tsets).replace('##ESETS##', esets).replace('##FOLDERS##', folders).replace('##WMSETS##', wmsets).replace('##THUMBSIZE##', str(self.MediaThumbSize)).replace('##EGTHRESHOLD##', str(self.EleGainThreshold)).replace('##AGTHRESHOLD##', str(self.AltGainThreshold)).replace('##SLRANGE##', str(self.SlopeRange)).replace('##SLMAX##', str(self.SlopeMax)).replace('##SPRANGE##', str(self.SpeedRange)).replace('##SPMAX##', str(self.SpeedMax)).replace('##SMENABLED##', str(self.SmoothTracks).lower()).replace('##SMRANGE##', str(self.SmoothRange)).replace('##V3DPMARGIN##', str(self.V3DPanoMargin)).replace('##V3DSMARGIN##', str(self.V3DSubjMargin)).replace('##NBTRACKS##', str(len(self.Tracks))).replace('#<#WAYDOTS#>#', waydots).replace('#<#TRACKS#>#', tracks).replace('#<#PATHES#>#', pathes)
    self.log(2, 'builtexp')
    return True

  def UpdateTrackBoundaries(self, t):
    tr = self.Tracks[t]
    minlat = min((p[1][0] for seg in (*tr[1].Pts, tr[1].Wpts) for p in seg), default=self.DefLat)
    maxlat = max((p[1][0] for seg in (*tr[1].Pts, tr[1].Wpts) for p in seg), default=self.DefLat)
    minlon = min((p[1][1] for seg in (*tr[1].Pts, tr[1].Wpts) for p in seg), default=self.DefLon)
    maxlon = max((p[1][1] for seg in (*tr[1].Pts, tr[1].Wpts) for p in seg), default=self.DefLon)
    clamp_lat = lambda v: min(self.VMaxLat, max(self.VMinLat, v))
    clamp_lon = lambda v: min(self.VMaxLon, max(self.VMinLon, v))
    self.TracksBoundaries[t] = tuple(b[i] for i in (0,1) for b in (WGS84WebMercator.WGS84toWebMercator(clamp_lat(minlat - 0.008), clamp_lon(minlon - 0.011)), WGS84WebMercator.WGS84toWebMercator(clamp_lat(maxlat + 0.008), clamp_lon(maxlon + 0.011))))

  def UpdateHTMLExp(self, t, elts, retrieve=None):
    if self.HTMLExp is None:
      return False
    if 't' in elts:
      pos = self.HTMLExp.find('<div id="track%dcont"' % t)
      n = self._build_track_exp(t)
      if pos >= 0:
        n = n.strip('\r\n ')
        self.HTMLExp = self.HTMLExp[:pos] + n + self.HTMLExp[self.HTMLExp.find('</div>', pos) + 6:]
      else:
        pos = self.HTMLExp.find('\r\n                </form>', self.HTMLExp.find('<form id="tracksform"'))
        self.HTMLExp = self.HTMLExp[:pos] + n + self.HTMLExp[pos:]
        pos = self.HTMLExp.find('<br>', self.HTMLExp.find('<div id="tracks"'))
        self.HTMLExp = self.HTMLExp[:self.HTMLExp.rfind('(', 0, pos)] + '(%d)' % len(self.Tracks) + self.HTMLExp[pos:]
      if retrieve is not None:
        retrieve['track%dcont' % t] = n
    if 'p' in elts:
      pos = self.HTMLExp.find('<svg id="track%d"' % t)
      n = self._build_path_exp(t)
      if pos >= 0:
        n = n.strip('\r\n ')
        self.HTMLExp = self.HTMLExp[:pos] + n + self.HTMLExp[self.HTMLExp.find('</svg>', pos) + 6:]
      else:
        pos = self.HTMLExp.find('  <svg id="waydots')
        if pos < 0:
          pos = self.HTMLExp.find('</div>\r\n              <div id="scalebox"')
        self.HTMLExp = self.HTMLExp[:pos] + n + self.HTMLExp[pos:]
      if retrieve is not None:
        retrieve['track%d' % t] = n
    if 'w' in elts:
      pos = self.HTMLExp.find('<svg id="waydots%d"' % t)
      n = self._build_waydots_exp(t)
      if pos >= 0:
        n = n.strip('\r\n ')
        self.HTMLExp = self.HTMLExp[:pos] + n + self.HTMLExp[self.HTMLExp.find('</svg>', pos) + 6:]
      else:
        pos = self.HTMLExp.find('</div>\r\n              <div id="scalebox"')
        self.HTMLExp = self.HTMLExp[:pos] + n + self.HTMLExp[pos:]
      if retrieve is not None:
        retrieve['waydots%d' % t] = n
    return True

  def EditMode(self, defx=None, defy=None):
    if self.HTML is None:
      return False
    if self.HTML != '':
      self.UpdateTrackBoundaries(self.TrackInd)
    self.Minx, self.Maxx, self.Miny, self.Maxy = self.TracksBoundaries[self.TrackInd]
    self.HTML = ''
    self.log(1, 'build')
    if not self.Track.BuildWebMercator():
      self.log(0, 'berror1')
      return False
    if self.BuildHTML(defx, defy):
      self.log(1, 'built')
      return True
    else:
      return False

  def ExploreMode(self):
    if self.HTMLExp is None:
      return False
    self.HTML = None
    self.HTMLExp = ''
    if self.Track is not None:
      if self.Track.Track is not self.Track.STrack:
        del self.Track.Track
        self.Track.Track = self.Track.STrack
        self.Track.ProcessGPX('a')
      del self.Track.OTrack
      self.Track.OTrack = self.Track.STrack
      self.Track.WebMercatorWpts = None
      self.Track.WebMercatorPts = None
      for t_ind in range(len(self.Tracks)):
        track = self.Tracks[t_ind]
        if track[0] == self.Uri:
          if track[1] is not self.Track:
            track[1].ProcessGPX('w')
          self.UpdateTrackBoundaries(t_ind)
      self.Minx = min((b[0] for b in self.TracksBoundaries), default=self.Minx)
      self.Maxx = max((b[1] for b in self.TracksBoundaries), default=self.Maxx)
      self.Miny = min((b[2] for b in self.TracksBoundaries), default=self.Miny)
      self.Maxy = max((b[3] for b in self.TracksBoundaries), default=self.Maxy)
    self.log(1, 'buildexp')
    try:
      if self.BuildHTMLExp():
        if self.TrackInd is not None:
          self.HTMLExp = self.HTMLExp.replace('var focused = ""', 'var focused = "track' + str(self.TrackInd) + '"')
          self.Track = None
          self.Uri = None
          self.TrackInd = None
        self.log(1, 'builtexp')
        return True
      else:
        return False
    except:
      return False

  def _start_webserver(self, ind):
    with ThreadedDualStackServer((self.Ip, self.GPXTweakerInterfaceServerInstances[ind]), GPXTweakerRequestHandler) as self.GPXTweakerInterfaceServerInstances[ind]:
      self.GPXTweakerInterfaceServerInstances[ind].Interface = self
      self.GPXTweakerInterfaceServerInstances[ind].serve_forever()

  def _stop_webserver(self, ind):
    try:
      self.GPXTweakerInterfaceServerInstances[ind].shutdown()
    except:
      pass

  def run(self):
    try:
      if not (self.EditMode() if self.Uri is not None else self.ExploreMode()):
        return False
    except:
      return False
    self.log(0, 'start')
    for ind in range(len(self.GPXTweakerInterfaceServerInstances)):
      webserver_thread = threading.Thread(target=self._start_webserver, args=(ind,))
      webserver_thread.start()
    return True

  def shutdown(self):
    self.log(0, 'close')
    for ind in range(len(self.GPXTweakerInterfaceServerInstances)):
      webserver_thread = threading.Thread(target=self._stop_webserver, args=(ind,))
      webserver_thread.start()
    self.Map.Close()
    self.Elevation.Close()
    with self.SLock:
      if self.GPXLoader:
        self.GPXLoader.Close()
      for tr in self.Tracks:
        trck = tr[1]
        if not isinstance(trck, WGS84TrackProxy):
          trck.ULock = None
          trck.OTrack = trck.STrack = None
          del trck.Track
      self.HTML = self.HTMLExp = self.HTML3D = self.HTML3DData = None
    with self.Media.DLock:
      self.Media.Data = None


if __name__ == '__main__':
  print('GPXTweaker v1.16.0 (https://github.com/PCigales/GPXTweaker)    Copyright © 2022 PCigales')
  print(LSTRINGS['parser']['license'])
  print('')
  formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=119)
  CustomArgumentParser = partial(argparse.ArgumentParser, formatter_class=formatter, add_help=False)
  parser = CustomArgumentParser()
  parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help=LSTRINGS['parser']['help'])
  parser.add_argument('uri', metavar='URI', help=LSTRINGS['parser']['uri'], nargs='?', default=None)
  parser.add_argument('--conf', '-c', metavar='CONF', help=LSTRINGS['parser']['conf'], default='')
  parser.add_argument('--trk', '-t', metavar='TRK', help=LSTRINGS['parser']['trk'], type=int, default=None)
  parser.add_argument('--map', '-m', metavar='MAP', help=LSTRINGS['parser']['map'], nargs ='?', const=' ', default='')
  parser.add_argument('--emap', '-e', metavar='EMAP', help=LSTRINGS['parser']['emap'], nargs ='?', const=' ', default='')
  parser.add_argument('--box', '-b', metavar='BOX', help=LSTRINGS['parser']['box'], type=(lambda b: ([(p,q,r,s) for [p,q,r,s] in (map(float, map(str.strip, b.split(','))),)][0]) if b != '' else (None, ) * 4), default='')
  parser.add_argument('--size', '-s', metavar='SIZE', help=LSTRINGS['parser']['size'], type=(lambda s: ([(p,q) for [p,q] in (map(int, map(str.strip, s.split(','))),)][0]) if s != '' else (None, ) * 2), default='')
  parser.add_argument('--dpi', '-d', metavar='DPI', help=LSTRINGS['parser']['dpi'], type=(lambda d: (int(d) if not '.' in d else float(d)) if d != '' else None), default='')
  parser.add_argument('--record', '-r', metavar='RECORD', help=LSTRINGS['parser']['record'], default=None)
  parser.add_argument('--noopen', '-n', help=LSTRINGS['parser']['noopen'], action='store_true')
  parser.add_argument('--verbosity', '-v', metavar='VERBOSITY', help=LSTRINGS['parser']['verbosity'], type=int, choices=[0,1,2], default=0)
  args = parser.parse_args()
  if args.uri is not None:
    if args.uri.rpartition('.')[2] != 'gpx':
      parser.error(LSTRINGS['parser']['gpx'])
  VERBOSITY = args.verbosity
  print(LSTRINGS['parser']['keyboard'])
  print('')
  cfg = os.path.expandvars(args.conf).rstrip('\\')
  if not os.path.isfile(cfg):
    cfg = os.path.join(cfg or os.path.dirname(os.path.abspath(__file__)), 'GPXTweaker.cfg')
  GPXTweakerInterface = GPXTweakerWebInterfaceServer(uri=args.uri, trk=args.trk if args.uri is not None else None, bmap=(args.map or None), emap=(args.emap or None), map_minlat=args.box[0], map_maxlat=args.box[1], map_minlon=args.box[2], map_maxlon=args.box[3], map_maxheight=(args.size[0] or 2000), map_maxwidth=(args.size[1] or 4000), map_resolution=((WGS84WebMercator.WGS84toWebMercator(args.box[1], args.box[3])[0] - WGS84WebMercator.WGS84toWebMercator(args.box[0], args.box[2])[0]) / args.size[0] if not (None in args.box or None in args.size) else None), map_dpi=args.dpi, record_map=args.record, cfg=cfg, launch=(not args.noopen), stop=(stop := (lambda: bool(msvcrt.kbhit() and ((c := msvcrt.getch().upper()) == b'S' or (c == b'\xe0' and msvcrt.getch() and False) or stop())))))
  if GPXTweakerInterface is None:
    exit()
  print(LSTRINGS['parser']['keyboard'])
  while True:
    k = msvcrt.getch()
    if k == b'\xe0':
      k = msvcrt.getch()
      k = b''
    if k.upper() == b'S':
        break
  GPXTweakerInterface.shutdown()
else:
  gen_HTTPRequest()