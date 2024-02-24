## move les fonction plutard comme je savait pas ou les ranger j'ai fait un fichier a part

# importation des modules

# declaration des fonction

def _get_rarity_and_name(): # witch one who can spawn in wild
    name_rarity_quantity = []
    with open('all_objets.txt') as file:
        for line in file.readlines():
            line_ = line.split()
            if line_[0] != '#':
                name,rarity = line_[0],line_[1]
                rarity = rarity.split(":")
                if rarity[0] != 0:
                    print(rarity[1])
                    rarity[1] = abs(int(rarity[1])-100)# inversion of rarity for future calcul
                    name_rarity_quantity.append((name,rarity[1],rarity[2]))
    return tuple(name_rarity_quantity)

def _get_total_rarity(name_rarity_quantity):
    total_rarity = 0
    for i in name_rarity_quantity:
        total_rarity += i[1]
    return total_rarity
    
# fonction principale
def main():
    name_rarity_quantity = _get_rarity_and_name()
    print(name_rarity_quantity)
    print(_get_total_rarity(name_rarity_quantity))
    

# programe principale
if __name__ == '__main__':
    main()
