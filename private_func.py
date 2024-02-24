## Move les fonctions plus tard, comme je ne savais pas où les ranger, j'ai créé un fichier à part

# importation des modules
from objet import Objet
# declaration des fonction


def _get_total_rarity(list_all_object):
    total_rarety = 0
    for OBJECT in list_all_object:
        total_rarety += abs(OBJECT.rarety-100)
    return total_rarety


def list_all_objet():# on pourait le mettre dans objet.py directement
    
    list_all_object = []
    with open('all_objets.txt') as file:
        for line in file.readlines():
            list_all_object.append(Objet(line.split()[0]))
    return list_all_object
    
    
# fonction principale
def main():
    pass
    

# programe principale
if __name__ == '__main__':
    main()
