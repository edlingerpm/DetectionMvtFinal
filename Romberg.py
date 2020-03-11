# -*- coding: utf-8 -*-
"""
Created on Mon MAR 11 2020

@author: Pierre-Marie EDLINGER
ROMBERG TEST
"""
import cv2
import operator
import RutaipCommonFunctions as Rtp
from datetime import datetime
import numpy as np

TEMPSDUTEST = 3 # en secondes
DIFFSIGNIFICATIVETAILLEVISAGE=5
DIFFSIGNIFICATIVEAXEVISAGE=25

tailleInitiale = 0
tailleFinale = 0
differenceTailleVisage = 0
axeVisageInitial = 0
axeVisageFinal = 0

#création d'un répertoire + nommage du fichier final
Rtp.creationRepertoireImage()    
nom = './Images/images_Romberg.jpg'

#Ouverture de la camera
cap = Rtp.choixCamera()

# choix du fichier haarcascade

face_cascade=cv2.CascadeClassifier("./Haarcascade/haarcascade_frontalface_alt2.xml")

largeurFenetre = int(cap.get(3))
hauteurFenetre = int(cap.get(4))
marge=70
centreVertical = largeurFenetre/2
centreHorizontal = hauteurFenetre/2

now = datetime.now()

decompteFait = False
MerciFait = False
SecondesFait = False

# =============================================================================
# on demande de tendre les bras et de fermer les yeux
# on regarde ce qu'il s'est passé au bout de 5 secondes
# on affiche le résultat
# =============================================================================

while True:
    ret, frame=cap.read()
    
    later = datetime.now()
    difference = (later - now).total_seconds()
    
    # création d'un tableau
    tab_face=[]
    
    #########################################################################
    #    Gestion de l'IA qui rempli un tableau 
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face=face_cascade.detectMultiScale(gray, 1.3, 5)
    for x, y, w, h in face:
        tab_face.append([x, y, x+w, y+h])

    tab_face=sorted(tab_face, key=operator.itemgetter(0, 1))
    index=0
    #########################################################################
    
    # affichage du texte qui dit quoi faire    
    if (difference>=8)&(difference<=10):         
        Rtp.afficheTexte(frame, "Fermez les yeux")
    else:
        if difference <= 10 :
            Rtp.afficheTexte(frame, "Start in "+ str(10-int(difference)) +" seconds")

        
    if (difference>=5)&(decompteFait==False):
        Rtp.joueSon("./Sons/Test3Secondes.mp3")
        decompteFait = True  
        
    if (difference>=8)&(decompteFait==True)&(SecondesFait==False):
        Rtp.joueSon("./Sons/CloseEyes.mp3")
        SecondesFait = True
        
        for x, y, x2, y2 in tab_face:
            tailleInitiale=x2-x
            axeVisageInitial = x+(x2-x)/2
        print("Enregistrement paramètres initiaux")
    
    
    
        
    if (difference>=10+TEMPSDUTEST)&(MerciFait==False):
        Rtp.joueSon("./Sons/ThankYou.mp3")
        MerciFait = True  
        for x, y, x2, y2 in tab_face:
            # calcule la taille du visage
            tailleFinale=x2-x
            axeVisageFinal = x+(x2-x)/2
            
            #détermination de la position du visage par rapport au centre de l'image
            if abs(axeVisageFinal-axeVisageInitial)>= DIFFSIGNIFICATIVEAXEVISAGE:
                if axeVisageFinal>centreVertical :
                    print("à gauche ")
                else :
                    print("à droite")
        
        differenceTailleVisage = abs(tailleFinale - tailleInitiale)
        
        if differenceTailleVisage >= DIFFSIGNIFICATIVETAILLEVISAGE:
            if tailleInitiale<tailleFinale:
                
                print("en avant ")
            else:
                print("en arrière ")
            
    for x, y, x2, y2 in tab_face:
        cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)

    cv2.imshow('video', frame)
    

    # for x, y, x2, y2 in tab_face:
    #     print("x="+str(x))
    
    # taper "q" pour quitter le programme
    if cv2.waitKey(1)&0xFF==ord('q'):
        #print("quitter")
        #continuation = False
        break
    
    # taper "e" pour faire une image
    if cv2.waitKey(1)&0xFF==ord('e'):
        #enregistrement de l'image
        print("Enregistrement de l'image")
        break
        
cap.release()
cv2.destroyAllWindows()

