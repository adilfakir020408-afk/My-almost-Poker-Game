import random
class Carte:
        def __init__(self, c, v):
            """ Initialise les attributs couleur (entre 1 et 4), et valeur (entre 2 et 14). """
            self.couleur = c
            self.valeur = v
            
        def get_valeur(self):
            valeurs = [None, None,'2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi', 'As']
            return valeurs[self.valeur]

        def get_couleur(self):
            couleurs = ['trèfle','carreau','coeur','pique']
            return couleurs[self.couleur - 1]       
                    
        def __repr__(self):
            return self.get_valeur() + ' de ' + self.get_couleur()
        
        def __lt__(self, other):
            if self.valeur<other.valeur:
                return True
            elif self.valeur==other.valeur:
                if self.couleur < other.couleur:
                    return True
            return False
                
                

class Paquet_de_cartes:
    def __init__(self):
        """ Initialise l'attribut contenu avec une liste des 52 objets Carte possibles rangées par valeurs croissantes en commençant par pique, puis coeur, carreau et tréfle. """
        paquet = []
        self.paquet = paquet
        for couleur in range(1, 5):
            for valeur in range(2, 15):
                self.paquet.append(Carte(couleur, valeur))
                
    def __repr__(self):
        myrepr = ''
        for i in range(len(self.paquet)):
            myrepr = myrepr + ', ' + self.paquet[i].__repr__()
        return myrepr
    
    def distribuer_carte(self, main, n=1):
        if len(self.paquet) == 0: #on regarde si le paquet n'est pas vide
            print("Le paquet est vide")
        else:
            for i in range(min(n, len(self.paquet))): #pour éviter de tirer plus de cartes qu'il en éxiste dans le paquet
                main.cartes.append(self.paquet.pop())
    
    def ajouter_carte(self, carte):
        self.paquet.append(carte)
        
    def battre(self):
        random.shuffle(self.paquet)

def echange(t, i, j):
    temp = t[i]
    t[i] = t[j]
    t[j] = temp

def indMin(iDebut, liste):
  imin = iDebut
  for i in range(iDebut, len(liste)):
    if liste[i] < liste[imin]:
      imin = i
  return imin

def triSelection(liste):
  for i in range(len(liste)):
    echange(liste,i,indMin(i, liste))
  return liste

class Main:
    
    def __init__(self, etiquette =''):
        self.cartes =[]
        self.etiquette = etiquette
        
    def tri(self):
        triSelection(self.cartes)

    def famille(self):
        listeValeurs = [carte.valeur for carte in self.cartes]
        bilan = []
        for elt in set(listeValeurs):   
            nb = listeValeurs.count(elt)     
            if nb >= 2:
                bilan.append(nb)                
        
        if bilan == [2]:
            return 1       # paire
        if bilan == [2, 2]:
            return 2      # double paire
        if bilan == [3]:
            return 3      # brelan
        if bilan == [2, 3] or bilan == [3, 2]:
            return 6       # full
        if bilan == [4]:
            return 7      # carré   
        return 0    # aucun
            
    def quinte(self):
        valeurs = [carte.valeur for carte in self.cartes]
        U = set(valeurs)      # pour avoir toutes les valeurs distinctes
        if len(U) != 5:
            return 0
        if U == {14, 2, 3, 4, 5}:   # Notre cas spécial
            return 4
        if max(U) - min(U) == 4:   #permet de vérifier si on a bien 5 entiers consécutifs (pour éviter l'utilisation de max et min, on pourrait utiliser le triSelection déjà réalise, et faire la soustraction entre la dernière valeur de la liste, et la première)
            return 4
        return 0

    def couleur(self):
        couleurs = [carte.couleur for carte in self.cartes]
        if len(set(couleurs)) == 1:
            return 5
        else:
            return 0

    def quinteFlush(self):
        # 8 points si quinte ET couleur
        if (self.quinte() and self.couleur()): #tout entier ≠ 0 est “vrai” (True) et 0 est “faux” (False), donc on regarde si les deux autres sont vrais
            return 8  
        else:
            return 0
        
    def score(self):
        return max(self.quinteFlush(), self.famille(), self.couleur(), self.quinte()) #calcule le score final d’une main en prenant le plus grand des points donnés par quinte flush, famille (paires/brelan/full/carré), couleur et quinte


def partie(main1, main2):
    score1, score2 = main1.score(), main2.score()
    if score1 > score2:
        print("Le gagnant est le joueur 1")
    elif score2 > score1:
        print("Le gagnant est le joueur 2")
    else:
        print("C'est une égalité!!")
        
        
def afficher_main(main):
    print("Main de", main.etiquette)
    for i in range(len(main.cartes)):
        print(i + 1, ":", main.cartes[i])
        

def changer_cartes(paquet, main):
    afficher_main(main)

    saisie = input("Numéros des cartes à changer (max 3, séparés par des espaces; entrée pour garder toutes les cartes: ").strip() #s'assurer que les espaces avant de rentrer les cartes ne flag pas la réponse comme vide saisie =""

    if saisie == "":
        # Le joueur garde sa main
        return

    numeros = saisie.split() #découpe une chaîne de caractères en une liste de morceaux, en séparant sur les espaces (par défaut).

    # Maximum 3 cartes
    if len(numeros) > 3:
        print("Tu ne peux changer qu'au maximum 3 cartes. Aucune carte changée.")
        return

    indices = []

    # Vérifier chaque numéro
    for nb in numeros:
        if nb.isdigit() == False:
            print("Entrée invalide. Aucune carte changée.")
            return
        n = int(nb)
        if n < 1 or n > len(main.cartes):
            print("Numéro invalide. Aucune carte changée.")
            return
        if n not in indices:   # pour pas échange 2 fois la même carte
            indices.append(n)

    # Supprimer les cartes choisies (du plus grand indice au plus petit, sécuriser la suppression des cartes choisies, sans bug d’indice.
    #ex: si je pop(1), il ne restera que 4 cartes, donc si je veux pop(4), index out of range, si je veux pop(3), ça va pop la mauvaise carte parce que décalage d'index 
    #alors que si je pop toujours les plus grands indices, pas moyen d'avoir un index trop grand après.
    indices.sort(reverse=True)
    for n in indices:
        main.cartes.pop(n - 1) #décalage entre numéro carte, et leur indice

    # Distribuer le même nombre de nouvelles cartes
    paquet.distribuer_carte(main, n=len(indices))

    print("Nouvelle main de", main.etiquette)
    afficher_main(main)
    
def jouer_un_tour():
    paquet = Paquet_de_cartes()
    paquet.battre()
    main1 = Main("Joueur 1")
    main2 = Main("Joueur 2")

    paquet.distribuer_carte(main1, 5)
    paquet.distribuer_carte(main2, 5)

    print("--- Mains initiales ---")
    afficher_main(main1)
    afficher_main(main2)

    print("--- Tour du Joueur 1 ---")
    changer_cartes(paquet, main1)

    print("--- Tour du Joueur 2 ---")
    changer_cartes(paquet, main2)

    print("--- Mains finales ---")
    afficher_main(main1)
    afficher_main(main2)

    print("--- Résultat ---")
    partie(main1, main2)

