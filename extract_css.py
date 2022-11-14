import datetime
import os
import discord
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv



load_dotenv(dotenv_path="config")
#############DEBUT FONCTION AFFICHE_COURS#################

def affiche_cours():

    #first_day_of_the_week
    fdow = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday() % 7)

    date_first_day_of_the_week = fdow.strftime("%m/%d/%Y")
    #print(date_first_day_of_the_week)
    

    #print(date_today)

    LINK_TO_REQUEST = 'https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=G&Tel=alex.sentes&date='+date_first_day_of_the_week
    #LINK_TO_REQUEST = 'https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=G&Tel=alex.sentes&date=11/14/2022'

    #requete page EDT beecome
    #print(LINK_TO_REQUEST)
    page = requests.get(LINK_TO_REQUEST)

    #conversion dans un format lisible par bs4
    soup = BeautifulSoup(page.content, 'html.parser')


    ###################################################################################
    ###################EXTRACTION DES COURS DE L'EDT###################################
    ###################################################################################

    #extraction de toutes les cases de l'emploi du temps
    demi_journee = soup.find_all('div', class_='Case')
    #print(len(demi_journee))
    #on supprime le dernier élément des resultats qui ne sert a rien
    
    try:
        demi_journee.pop(-1)
    except:
        pass

    #declaration dictionnaire demi journée
    dico_cours = {}


    #variable pour afficher une demi journée sur 2
    a=0
    x = 1
    for i in demi_journee:
        if a % 2 == 0:
            try:
            #cours de la demi_journee
                contenu = i.find('div', class_="BackGroundCase")
                cours = contenu.find('td', class_="TCase").get_text()
                salle = contenu.find('td', class_="TCSalle").get_text()
                titre_forma = contenu.find('br').next_sibling
                prof = contenu.find('span').next_sibling
                heure = contenu.find('td', class_="TChdeb").get_text()

                content = cours+" "+salle+" "+heure+" "+titre_forma+" "+prof
                #print(x)
                #print(content)
                #copie du contenu de la variable content ligne cours, prof, etc dans un dictionnaire
                #le format du dictionnaire est le suivant : jour_semaine = 'cours'
                dico_cours[x] = content
                print(salle)
                #variable qui sert a ajouter le contenu au dictionnaire avec comme clé le numero du jour
                x+=1
            except:
                #print("pas de cours cette semaine")
                #print("test")
                break
        #variable a
        #cette variable est incrémenté car on veut recuperer une demi journée sur 2 pour avoir que les cours du matin
        a+=1


    #print(len(dico_cours))
    #jour_de_la_semaine = fdow.weekday()
    #print(fdow.weekday())
    
    jour_semaine = datetime.datetime.today().isoweekday()
    
    print("len of dico_cours is : ")
    print(len(dico_cours))
    jours_semaine_OK = [1, 2, 3, 4, 5]
    
    if jour_semaine in jours_semaine_OK and not len(dico_cours) == 0:
        print("affiche le jour de la semaine")
        print(dico_cours[jour_semaine])
        return dico_cours[jour_semaine]
        #action a effectuer a mettre ici
    elif len(dico_cours) == 0:
        return "pas de cours cette semaine"
    elif jour_semaine not in jours_semaine_OK:
        return("cest le week end !")

affiche_cours()
