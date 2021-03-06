import random

MINA = "*"
ZASTAVICA = "#"
ODKRITO_POLJE = "-"
NAPAKA = "N"

ZMAGA = "W"
PORAZ = "L"

PRVI_UGIB = "A"
ZACETEK = "S"


class Celica:
    def __init__(self, vrstica, stolpec, mina, odkrita=False, z_zastavico=False):
        self.mina = mina
        self.odkrita = odkrita
        self.z_zastavico = z_zastavico
        self.vrstica = vrstica
        self.stolpec = stolpec


    def odkrij_celico(self):
        self.odkrita = True

    def postavi_zastavico(self):
        self.z_zastavico = not self.z_zastavico

    def je_mina(self):
        self.mina = True


class Polje:
    def __init__(self, polja=None):
        if polja is None:
            self.polja = []
        else:
            self.polja = polja

        #celica = self.polja[vrstica][stolpec]

    def __len__(self):
        return len(self.polja)

    def st_min_v_okolici(self, vrstica, stolpec):
        st = 0
        for [i, j] in self.sosedi_celice(vrstica, stolpec):
            celica = self.polja[i][j]
            if celica.mina == True:
                st += 1
        return st

    def sosedi_celice(self, vr, st):
        st_vrstic = len(self.polja)
        st_stolpcev = len(self.polja[0])
        sez = [[vr - 1, st - 1], [vr - 1, st], [vr - 1, st + 1], [vr, st - 1], [vr, st + 1],[vr + 1, st - 1], [vr + 1, st],[vr + 1, st + 1]]
        nov_sez = []
        for celica in sez:
            i = celica[0]
            j = celica[1]
            if self.legalna_celica(i, j):
                nov_sez.append(celica)
        return nov_sez

    #pogleda, da ni slucajno cez rob
    def legalna_celica(self, vrstica, stolpec):
        st_vrstic = len(self.polja)
        st_stolpcev = len(self.polja[0])
        if vrstica >= 0 and vrstica < st_vrstic:
            if stolpec >= 0 and stolpec < st_stolpcev:
                return True
            else:
                return False
        else:
            return False

    def postavi_zastavico(self, vrstica, stolpec):
        celica = self.polja[vrstica][stolpec]
        if not celica.odkrita:
            celica.postavi_zastavico()
        else:
            return

    def odkrij_celico(self, vrstica, stolpec):
        celica = self.polja[vrstica][stolpec]
        if not celica.odkrita:
            celica.odkrij_celico()
            #za celice, ki nimajo min v okolici, odkrije tudi druge celice
            if self.st_min_v_okolici(vrstica, stolpec) == 0:
                for [i, j] in self.sosedi_celice(vrstica, stolpec):
                    self.odkrij_celico(i, j)

    #ko odkriješ vsa polja, kjer ni min
    def zmaga(self):
        for vrstica in self.polja:
            for celica in vrstica:
                if not celica.odkrita and not celica.mina:
                    return False
        return True

    #odkriješ polje z mino
    def poraz(self):
        for vrstica in self.polja:
            for celica in vrstica:
                if celica.odkrita == True  and celica.mina == True:
                    return True
        return False



    #spremeni stanje igre glede na uporabnikovo ugibanje
    def ugibaj(self, vr, st, zastavica):
        #zastavica je true ali false
        if not self.legalna_celica(vr, st):
            return NAPAKA

        celica = self.polja[vr][st]

        #pogledat če prvi vnos
        if self.brez_odkritih_celic():
            #ce je slucajno celica mina je treba dat mino drugam
            if celica.mina == True:

                sez_koordinat = []
                for i in range(len(self.polja)):
                    for j in range(len(self.polja)):
                        sez_koordinat.append([i, j])

                mesta_brez_bomb = []
                for [i, j] in sez_koordinat:
                    celica_x = self.polja[i][j]
                    if celica_x.mina == False:
                        mesta_brez_bomb.append([i, j])

                izbira = random.choice(mesta_brez_bomb)
                self.polja[izbira[0]][izbira[1]].je_mina()
                celica.mina = False
                self.odkrij_celico(vr, st)
                return PRVI_UGIB

            else:
                self.odkrij_celico(vr, st)
                return PRVI_UGIB

        if celica.odkrita == True:
            return NAPAKA


        elif zastavica == False:
            self.odkrij_celico(vr, st)
            if self.poraz():
                return PORAZ
            elif self.zmaga():
                return ZMAGA
            else:
                return ODKRITO_POLJE

        elif zastavica == True:
            self.postavi_zastavico(vr, st)
            return ZASTAVICA

        else:
            return ODKRITO_POLJE

    #pomozna fuja
    def brez_odkritih_celic(self):
        for vrsta in self.polja:
            for celica in vrsta:
                if celica.odkrita == True:
                    return False
        return True

    def pokazi_vse_mine(self):
        for vrstica in self.polja:
            for celica in vrstica:
                if celica.mina == True:
                    if not celica.odkrita:
                        celica.odkrij_celico()
                    else:
                        return

    def postavljene_zastavice(self):
        st = 0
        for vrstica in self.polja:
            for celica in vrstica:
                if celica.z_zastavico == True:
                    st += 1
        return st

    def ostanek_min(self):
        ostanek = 0
        for vrstica in self.polja:
            for celica in vrstica:
                if celica.mina == True:
                    ostanek += 1
                elif celica.z_zastavico == True:
                    ostanek -= 1
        return ostanek




def zgradi_polje(velikost, st_min):
    sez_celic = []
    for i in range(velikost):
        vrstica = []
        for j in range(velikost):
            vrstica.append(Celica(i, j, False))
        sez_celic.append(vrstica)

    #še postavitev bomb
    prosta_mesta = []
    for i in range(velikost):
        for j in range(velikost):
            prosta_mesta.append([i, j])

    for l in range(st_min):
        izbira = random.choice(prosta_mesta)
        prosta_mesta.remove(izbira)
        i = izbira[0]
        j = izbira[1]
        sez_celic[i][j].je_mina()
    return sez_celic


def nova_igra(velikost_polja, st_min):
    novo_polje = zgradi_polje(velikost_polja, st_min)
    return Polje(novo_polje)


#za celico prikazano v spletnem vmesniku
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


class Minolovec:
    def __init__(self):
        self.igre = {}

    def prost_id_igre(self):
        if self.igre.keys():
            return max(self.igre.keys()) + 1
        else:
            return 0

    def nova_igra(self, velikost_polja, st_min):
        id_igre = self.prost_id_igre()

        polje = zgradi_polje(velikost_polja, st_min)
        igra = Polje(polje)
        self.igre[id_igre] = [igra, velikost_polja, st_min, ZACETEK]

        return id_igre

    def ugibaj(self, id_igre, vrstica, stolpec, zastavica):
        [igra, velikost_polja, st_min, stanje] = self.igre[id_igre]
        novo_stanje = igra.ugibaj(vrstica, stolpec, zastavica)
        self.igre[id_igre] = [igra, velikost_polja, st_min, novo_stanje]
