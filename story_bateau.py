from bateau import Bateau

b1 = Bateau(2, 3, longueur=3) 
b2 = Bateau(2, 4, longueur=2) 

chevauchent = False
for pos in b2.positions:
    if pos in b1.positions:
        chevauchent = True
        break

print("Cas chevauchement :")
print(f"Bateau 1 positions : {b1.positions}")
print(f"Bateau 2 positions : {b2.positions}")
print("Chevauchent ?" , chevauchent)
print()

b3 = Bateau(0, 0, longueur=3)          
b4 = Bateau(2, 0, longueur=2, vertical=True)  

chevauchent2 = False
for pos in b3.positions:
    if pos in b4.positions:
        chevauchent = True
        break

print("Cas sans chevauchement :")
print(f"Bateau 3 positions : {b3.positions}")
print(f"Bateau 4 positions : {b4.positions}")
print("Chevauchent ?" , chevauchent2)