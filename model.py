import random

MINA = "*"
ZASTAVICA = "#"
ODKRITO_POLJE = "-"

ZMAGA = "W"
PORAZ = "L"

ZAČETEK = "S"


class Celica(x):
    def __init__(self, mina, vrstica, stolpec):
        self.mina = mina
        self.odkrita = False
        self.z_zastavico = False
        self.vrstica = vrstica
        self.stolpec = stolpec
        # se koordinate mogoce

    def odkrij_celico(self):
        self.odkrita = not self.odkrita

    def postavi_zastavico(self):
        self.z_zastavico = not self.z_zastavico

    def je_mina(self):
        self.mina = True


class Polje():
    def __init__(self, st_vrstic, st_stolpcev, st_min, polja):
        self.st_vrstic = st_vrstic
        self.st_stolpcev = st_stolpcev
        self.st_min = st_min
        self.polja = polja
        super().__init__()


    def st_min_v_okolici(self, x0, y0, mine):
        #mine je mnozica koordinat z minami
        #tuki moram se dodat sploh notr mine
        st = 0
        for x in (x0 - 1, x0, x0 + 1):
            for y in (y0 - 1, y0, y0 + 1):
                if (x, y) in mine and (x != x0 or y != y0):
                    st += 1
        return st
    
    #mogoče gre to raje v tekstovni vmesnik
    def je_mina(self, x0, y0):
        self[x0][y0].je_mina()
    #ta tudi
    def postavi_zastavico(self, x0, y0):
        if not self[x0][y0].odkrita:
            self[x0][y0].postavi_zastavico()
        else:
            print("Celica je že vidna. Zastavice ne moreš postaviti.")



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
        if self.odkrij_celico() and self.je_mina():
            return True
        else:
            return False
        


    #ce celica nima min v okolici, odpre tudi vse sosednje celice
    def odpri_polja_v_okolici(self):
        pass
    

    #spremeni stanje igre glede na uporabnikovo ugibanje
    def ugibaj(self, vrstica, stolpec):
        celica = self[vrstica][stolpec]
        #stanje po ugibu
        if celica.je_mina():
            return PORAZ
        
        elif self.zmaga():
            return ZMAGA
        
        else:
            return ODKRITO_POLJE

    #ta funkcija se ni v redu
    def pokazi_vse_mine(self):
        for vrstica in polja:
            for celica in vrstica:
                if celica.je_mina:
                    if not celica.odkrij_celico():
                        celica.odkrita == True
                    else:
                        return celica.odkrita == False

    def ostanek_min(self):
        ostanek = 0
        for vrstica in self.polja:
            for celica in vrstica:
                if celica.je_mina():
                    ostanek += 1
                elif celica.z_zastavico:
                    ostanek -= 1
        return ostanek

    
def nova_igra():
        pass