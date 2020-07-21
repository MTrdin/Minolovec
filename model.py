import random

MINA = "*"
ZASTAVICA = "#"
ODKRITO_POLJE = "-"
NAPAKA = "N" 

ZMAGA = "W"
PORAZ = "L"

ZAČETEK = "S"


class Celica:
    def __init__(self, mina, vrstica, stolpec, odkrita=False, z_zastavico=False):
        self.mina = mina
        self.odkrita = odkrita
        self.z_zastavico = z_zastavico
        #koordinate
        self.vrstica = vrstica
        self.stolpec = stolpec
        
        
    def odkrij_celico(self):
        self.odkrita = True

    def postavi_zastavico(self):
        self.z_zastavico = not self.z_zastavico

    def je_mina(self):
        self.mina = True


class Polje(tuple):
    def __init__(self, polja=[]):
        self.polja = polja
        #polja bodo seznam seznamov po vrsticah
        #super().__init__()

        #celica = polja[vrstica][stolpec]

    def st_min_v_okolici(self, vrstica, stolpec):
        st = 0
        for celica in sosedi_celice(self, vrstica, stolpec):
            if celica.mina:
                st += 1
        return st

    def sosedi_celice(self, vr, st):
        st_vrstic = len(polja)
        st_stolpcev = len(polja[0])
        sez = [[vr - 1, st - 1], [vr - 1, st], [vr - 1, st + 1], [vr, st - 1], [vr, st + 1],[vr + 1, st - 1], [vr + 1, st],[vr + 1, st + 1]]
        nov_sez = []
        for celica in sez:
            i = celica[0]
            j = celica[1]
            if legalna_celica(self, i, j):
                nov_sez.append(celica)
        return nov_sez

    #pogleda, da ni slucajno cez rob
    def legalna_celica(self, vrstica, stolpec):
        st_vrstic = len(polja)
        st_stolpcev = len(polja[0])
        if vrstica >= 0 and vrstica < st_vrstic:
            if stolpec >= 0 and stolpec < st_stolpcev:
                return True
            else:
                return False
        else:
            return False

 
    #mogoče gre to raje v tekstovni vmesnik
    #def je_mina(self, x0, y0):
    #    self[x0][y0].je_mina()
    ##ta tudi
    #def postavi_zastavico(self, x0, y0):
    #    if not self[x0][y0].odkrita:
    #        self[x0][y0].postavi_zastavico()
    #    else:
    #        print("Celica je že vidna. Zastavice ne moreš postaviti.")


    def postavi_zastavico(self, vrstica, stolpec):
        celica = polja[vrstica][stolpec]
        if not celica.odkrita:
            celica.postavi_zastavico()
        else:
            return #ne naredi nic

    #se treba dodat, da prvi klik ni mina, ampka prazno polje
    def odkrij_celico(self, vrstica, stolpec):
        celica = polja[vrstica][stolpec]
        if not celica.odkrita:
            celica.odkrij_celico()
            #za celice, ki nimajo min v okolici, odkrije tudi druge celice
            if self.st_min_v_okolici(vrstica, stolpec) == 0:
                for cel in self.sosedi_celice(vrstica, stolpec):
                    cel.odkrij_celico()
                    

    #brezvezna fuja
    def polje_brez_min(self, x0, y0):
        st = st_min_v_okolici(self, x0, y0, mine)
        if st == 0:
            return True
        else:
            return False

    #ko odkriješ vsa polja, kjer ni min
    def zmaga(self):
        for vrstica in self.polja:
            for celica in vrstica:
                if not celica.odkrita and not celica.je_mina:
                    return False
        return True
        
    #odkriješ polje z mino
    def poraz(self):
        for vrstica in self.polja:
            for celica in vrstica:
                if celica.odkrita and celica.je_mina:
                    return True
        return False
        


    #spremeni stanje igre glede na uporabnikovo ugibanje
    def ugibaj(self, vrstica, stolpec):
        #se dodat zastavico najbrs
        #kaj se zgodi če vnešeni podatki niso ustrezni
        if not vrstica.isdigit() or not stolpec.isdigit():
            return NAPAKA
        
        vr = int(vrstica)
        st = int(stolpec)
        if not legalna_celica(vr, st):
            return NAPAKA

        celica = self.polje[vr][st]
        #stanje po ugibu
        if celica.je_mina(): #self.poraz()
            return PORAZ
        
        elif self.zmaga():
            return ZMAGA
        
        else:
            return ODKRITO_POLJE

    #ta funkcija se ni v redu
    def pokazi_vse_mine(self):
        for vrstica in polja:
            for celica in vrstica:
                if celica.mina:
                    if not celica.odkrij_celico():
                        celica.odkrita == True
                    else:
                        return celica.odkrita == False

    def postavljene_zastavice(self):
        st = 0
        for vrstica in self.polja:
            for celica in vrstica:
                if celica.z_zastavico:
                    st += 1
        return st
    
    def ostanek_min(self):
        ostanek = 0
        for vrstica in self.polja:
            for celica in vrstica:
                if celica.je_mina():
                    ostanek += 1
                elif celica.z_zastavico:
                    ostanek -= 1
        return ostanek


def zgradi_polje(st_vrstic, st_stolpcev, st_min):
    sez_celic = []
    for i in range(st_vrstic):
        vrstica = []
        for j in range(st_stolpcev):
            vrstica.append(Celica(i, j, False))
    sez_celic.append(vrstica)

    #še postavitev bomb
    prosta_mesta = []
    for i in range(st_vrstic):
        for j in range(st_stolpcev):
            prosta_mesta.append([i, j])

    for l in range(st_min):
        izbira = random.choice(prosta_mesta)
        prosta_mesta.remove(izbira)
        i = izbira[0]
        j = izbira[1]
        sez_celic[i][j].je_mina()
    return sez_celic
    
def nova_igra(st_vrstic, st_stolpcev, st_min):
    novo_polje = zgradi_polje(st_vrstic, st_stolpcev, st_min)
    return Polje(novo_polje)