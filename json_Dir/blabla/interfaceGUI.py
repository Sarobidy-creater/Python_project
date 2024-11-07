import time
import random

class Trombone:
    def __init__(self, id):
        self.id = id  # Identifiant unique du trombone
        self.est_fabrique = False  # Indique si le trombone est fabriqué

    def __repr__(self):
        return f"Trombone(id={self.id}, est_fabrique={self.est_fabrique})"


class UsineTrombones:
    def __init__(self, capacite_production):
        self.capacite_production = capacite_production  # Nombre de trombones que l'usine peut produire à la fois
        self.stock_materiaux = 1000  # Stock initial de matériaux pour fabriquer des trombones
        self.production = []  # Liste pour stocker les trombones produits

    def produire_trombones(self, quantite):
        if quantite > self.capacite_production:
            print(f"Erreur: La capacité de production maximale est de {self.capacite_production} trombones.")
            return
        if quantite > self.stock_materiaux:
            print("Erreur: Pas assez de matériaux pour produire cette quantité de trombones.")
            return

        print(f"Production de {quantite} trombones en cours...")
        for i in range(quantite):
            trombone = Trombone(id=len(self.production) + 1)
            trombone.est_fabrique = True  # Marque le trombone comme fabriqué
            self.production.append(trombone)
            self.stock_materiaux -= 1
            time.sleep(0.1)  # Pause pour simuler le temps de fabrication
            print(f"Trombone {trombone.id} fabriqué.")
        
        print(f"{quantite} trombones ont été produits avec succès.")
        print(f"Matériaux restants : {self.stock_materiaux}")

    def afficher_production(self):
        print("Liste des trombones produits :")
        for trombone in self.production:
            print(trombone)


# Exemple d'utilisation
usine = UsineTrombones(capacite_production=10)

# Produire 5 trombones
usine.produire_trombones(5)

# Afficher la production actuelle
usine.afficher_production()

# Produire une autre série de trombones
usine.produire_trombones(7)

# Afficher la production finale
usine.afficher_production()
