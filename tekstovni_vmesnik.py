import model


#ze vemo da je prislo do poraza
def izpis_poraza(igra):
    return "Sprožil/a si mino. Igre je konec."

def izpis_zmage(igra):
    return "Čestitke, odkril/a si vsa polja brez min."

#dolocis velikost polja
def zacetek_igre(igra):
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
-->Vnesi koordinate: """

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
            if 0 <= int(prvi) <= len(igra.polja) and 0 <= int(drugi) <= len(igra.polja):
                return True
        else:
            return False
    elif st == 3:
        prvi = vnseseni_podatki[0]
        drugi = vnseseni_podatki[1]
        if prvi.isdigit() and drugi.isdigit():
            if 0 <= int(prvi) <= len(igra) and 0 <= int(drugi) <= len(igra):
                if vnseseni_podatki[2] == "f":
                    return True
        else:
            return False
    else:
        return False

velikost = 8
st_min = 5

#to moram se izboljsat
def pozeni_vmesnik():
    
    igra = model.nova_igra(velikost, st_min)
    zacetek_igre(igra)
    while True:
        #izpisimo stanje
        print(izpis_igre(igra))
        #igralec
        poteza = zahtevaj_vnos(igra)
        vrstica = poteza[0]
        stolpec = poteza[1]
        zastavica = poteza[2] #False ali True
        #celica = igra.polja[vrstica][stolpec]

        stanje = igra.ugibaj(vrstica, stolpec, zastavica)



        #if not veljaven_vnos(igra, poteza):#vnos preverja ze fuja zahtevaj_vnos
            #continue #preskoci preostanek zanke
        if stanje == model.NAPAKA:
            print("Celica je že odprta.")
            #poteza = zahtevaj_vnos(igra)

        if stanje == model.PORAZ:
            print(izpis_poraza(igra))
            break
        elif stanje == model.ZMAGA:
            print(izpis_zmage(igra))
            break
        
        
        #preverimo če je igre konec
        #if igra.poraz():
        #    print(izpis_poraza(igra))
        #    break
        #elif igra.zmaga():
        #    print(izpis_zmage(igra))
        #    break
    return

pozeni_vmesnik()
    