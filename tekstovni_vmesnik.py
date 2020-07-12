import model


#ze vemo da je prislo do poraza
def izpis_poraza(igra):
    return "Sprožil/a si mino. Igre je konec."

def izpis_zmage(igra):
    return "Čestitke, odkril/a si vsa polja brez min."

def izpis_igre(igra):
    pass

def postavitev(st_vrstic, st_stolpcev, mine):
    polje = Polje(tuple([([Celica(False) for i in range(st_vrstic - 1)])
            for j in range(st_stolpcev)]))
    nezasedena_polja = list(range((st_vrstic - 1) * (st_stolpcev - 1)))
    #tuki mogoce bosl st min
    for n in range(mine):
        novo_polje = random.choice(nezasedena_polja)
        nezasedena_polja.remove(novo_polje)
        (vrstica, stolpec) = (novo_polje % 9, novo_polje // 9)
        polje.je_mina(vrstica, stolpec)
    return polje

    

def zahtevaj_vnos(igra):
    navodila = """Najprej vnesi stolpec nato vrstico. Če želiš postaviti zastavico,
    dodaj še črko f. (Na primer: 32f postavi zastavico na mesto,
    ki je v tretjem stolpcu in v drugi vrsti.
    Vnesi koordinate: """

    vnos = input("Vnesi koordinate (za navodila pritisni N): ")

    if vnos == "N":
        vnos = input(navodila)

    while not veljaven_vnos(vnos, igra):
        vnos = input("Neveljaven vnos. Vnesi koordinate (za navodila pritisni N): ")
        if vnos == "N":
            vnos = input(navodila)
    
    x0 = int(vnos[0])
    y0 = int(vnos[1])
    #tuki se ne vem kaj naj vrne, upoštevat bi mogla tut zastavico
    return (x0, y0)


def veljaven_vnos(moj_vnos, igra):
    if len(moj_vnos) not in (2, 3) or not moj_vnos[:1].isdigit() or int(moj_vnos[0]) not in range(st_stolpcev) or int(moj_vnos[1]) not in range(st_vrstic) or moj_vnos == "N":
        return False
    
    if len(moj_vnos) == 3 and moj_vnos[2] != "f":
        return False
    
    else:
        return True



def pozeni_vmesnik():
    igra = model.nova_igra()
    st_vrstic = 10
    st_stolpcev = 10
    mine = 9
    print(postavitev(st_vrstic, st_stolpcev, mine))
    while True:
        #izpisimo stanje
        print(izpis_igre(igra))
        #igralec
        korak = zahtevaj_vnos()
        if not veljaven_vnos(korak):
            continue #preskoci preostanek zanke

        igra.ugibaj(korak)
        
        #preverimo če je igre konec
        if igra.poraz():
            print(izpis_poraza(igra))
            break
        elif igra.zmaga():
            print(izpis_zmage(igra))
            break
    return

pozeni_vmesnik()
    