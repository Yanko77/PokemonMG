## Move les fonctions plus tard, comme je ne savais pas où les ranger, j'ai créé un fichier à part

# importation des modules
from objet import Objet
# declaration des fonction


def _get_total_rarity(list_all_object):
    total_rarety = 0
    for OBJECT in list_all_object:
        total_rarety += abs(OBJECT.rarety-100)
    return total_rarety

    
    
# fonction principale
def main():
    pass
    

# programe principale
if __name__ == '__main__':
    main()
