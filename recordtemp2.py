import os
import sys
import glob
#import django
from django.apps import apps
from django.utils import timezone
from django.db import models
from thermo.models import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sensors.settings")

def lireFichier (emplacement) :
    # Ouverture du fichier contenant la temperature
    fichTemp = open(emplacement)
    # Lecture du fichier
    contenu = fichTemp.read()
    # Fermeture du fichier apres qu'il ai ete lu
    fichTemp.close()
    return contenu

def recupTemp (contenuFich) :
    # Supprimer la premiere ligne qui est inutile
    secondeLigne = contenuFich.split("\n")[1]
    temperatureData = secondeLigne.split(" ")[9]
    # Supprimer le "t="
    temperature = float(temperatureData[2:])
    # Mettre un chiffre apres la virgule
    temperature = temperature / 1000
    return temperature

contenuFich = lireFichier("/sys/bus/w1/devices/28-0417b2f8faff/w1_slave")
temperature = recupTemp (contenuFich)

print ("Temperature :", temperature)
m = Measurement(sensor="temp1", value = temperature)
m.save()

