import model


def izpis_poraza(igra):
    return "Sprožil/a si mino!!! Igre je konec."

def izpis_zmage(igra):
    return "Čestitke!!! Odkril/a si vsa polja brez min!"

#dolocis velikost polja
def zacetek_igre():
    print("""=======================================
Dobrodošel v igri minolovec.
Cilj igre je odkriti vsa polja brez min.
=======================================""")


def izpis_igre(igra):
    izpis = "   "
    for id_st in range(len(igra.polja)):
        izpis += str(id_st) + "  "
    izpis += "\n\n"

    for vrstica in range(len(igra.polja)):
        niz = ""
        for stolpec in range(len(igra.polja)):
            niz += str(izpis_celice(igra, vrstica, stolpec)) + "  "
        izpis += str(vrstica) + "  " + niz + "\n"
    return izpis


def izpis_celice(igra, vrstica, stolpec):
    celica = igra.polja[vrstica][stolpec]
    if celica.mina == True and celica.odkrita == True:
        return "M"
    elif celica.mina == False and celica.odkrita == True:
        if igra.st_min_v_okolici(vrstica, stolpec) == 0:
            return " "
        else:
            return str(igra.st_min_v_okolici(vrstica, stolpec))
    elif celica.z_zastavico == True:
        return "F"
    else:
        return "X"

    
def zahtevaj_vnos(igra):
    navodila = """NAVODILA: Najprej vnesi vrstico nato stolpec. Loči ju s presledkom.
Če želiš postaviti zastavico, dodaj še črko f. 
Na primer: 3 2 f postavi zastavico na mesto, ki je v tretji vrstici in v drugem stolpcu.
--> Vnesi koordinate: """

    vnos = input("Vnesi koordinate (za navodila pritisni N): ")

    if vnos == "n":
        vnos = input(navodila)

    while not veljaven_vnos(igra, vnos):
        vnos = input("Neveljaven vnos. Vnesi koordinate (za navodila pritisni N): ")
        if vnos == "N" or vnos == "n":
            vnos = input(navodila)
    
    vnseseni_podatki = vnos.split(" ")
    vrstica = int(vnseseni_podatki[0])
    stolpec = int(vnseseni_podatki[1])
    return [vrstica, stolpec, vnseseni_podatki[- 1] == "f"]


def veljaven_vnos(igra, moj_vnos):
    vnseseni_podatki = moj_vnos.split(" ")
    st = len(vnseseni_podatki)
    if st == 2:
        prvi = vnseseni_podatki[0]
        drugi = vnseseni_podatki[1]
        if prvi.isdigit() and drugi.isdigit():
            if 0 <= int(prvi) < len(igra.polja) and 0 <= int(drugi) < len(igra.polja):
                return True
        else:
            return False
    elif st == 3:
        prvi = vnseseni_podatki[0]
        drugi = vnseseni_podatki[1]
        if prvi.isdigit() and drugi.isdigit():
            if 0 <= int(prvi) < len(igra) and 0 <= int(drugi) < len(igra):
                if vnseseni_podatki[2] == "f":
                    return True
        else:
            return False
    else:
        return False

def vnesi_velikosti():
    cifre = input("""Določi velikost polja n x n in število min.
Najprej vnesi velikost n, nato število min. Loči ju s presledkom.
(Število min mora biti manjše kot n x n)
--> Vnesi velikosti: """)

    while not veljaven_vnos_velikosti(cifre):
        cifre = input("""Neveljaven vnos! 
--> Vnesi velikost polja n in st min, ki ju ločiš s presledkom: """)

    podatki = cifre.split(" ")
    velikost_polja = int(podatki[0])
    st_min = int(podatki[1])
    return [velikost_polja, st_min]

def veljaven_vnos_velikosti(cifre):
    podatki = cifre.split(" ")
    if len(podatki) != 2:
        return False

    prvi = podatki[0]
    drugi = podatki[1]

    if prvi.isdigit() and drugi.isdigit():
        if int(drugi) < int(prvi) * int(prvi):
            return True
        else:
            return False
    else:
        return False

def podatki_o_minah(igra):
    tekst = ("""Postavljene zastavice\\st min: {zas}\\{mine}""").format(zas = igra.postavljene_zastavice(), mine = igra.ostanek_min())
    return tekst


def pozeni_vmesnik():
    zacetek_igre()

    seznam_cifer = vnesi_velikosti()
    velikost = seznam_cifer[0]
    st_min = seznam_cifer[1]

    igra = model.nova_igra(velikost, st_min)
    
    while True:
        print(izpis_igre(igra))
        print(podatki_o_minah(igra))

        poteza = zahtevaj_vnos(igra)
        vrstica = poteza[0]
        stolpec = poteza[1]
        zastavica = poteza[2] #False ali True
        
        stanje = igra.ugibaj(vrstica, stolpec, zastavica)

        if stanje == model.NAPAKA:
            print("Celica je že odprta!!!")
            
        if stanje == model.PORAZ:
            #odkrije vse mine
            igra.pokazi_vse_mine()
            print(izpis_igre(igra))
            print(izpis_poraza(igra))
            break

        elif stanje == model.ZMAGA:
            print(izpis_zmage(igra))
            break
        
    return

pozeni_vmesnik()
    