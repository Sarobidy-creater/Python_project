import argparse  # Importe le module argparse qui permet de gérer les arguments de la ligne de commande.

# Créer un parser d'arguments
parser = argparse.ArgumentParser(description="Un exemple simple de lecture d'arguments.")
# Crée une instance d'ArgumentParser. Le paramètre 'description' fournit une brève description du programme qui s'affichera si l'utilisateur demande de l'aide.

# Ajouter des arguments
parser.add_argument('--name', type=str, help='Votre nom', required=True)
# Ajoute un argument optionnel '--name' qui attend une chaîne de caractères (type=str).
# 'help' fournit une description de cet argument qui s'affichera dans l'aide.
# 'required=True' indique que cet argument est obligatoire.

parser.add_argument('--age', type=int, help='Votre âge', required=True)
# Ajoute un autre argument optionnel '--age' qui attend un entier (type=int).
# Cet argument est également requis.

# Analyser les arguments
args = parser.parse_args()
# Utilise la méthode parse_args() pour analyser les arguments fournis par l'utilisateur via la ligne de commande.
# Les valeurs des arguments sont stockées dans un objet 'args'.

# Afficher les résultats
print(f"Bonjour, {args.name}! Vous avez {args.age} ans.")
# Affiche un message personnalisé en utilisant les valeurs des arguments 'name' et 'age'.
# f-string permet d'insérer les variables directement dans la chaîne.
