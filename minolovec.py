import bottle
import model

SECRET = "Ena skrivnost"

minolovec = model.Minolovec()

#ali def index()
#se treba narest zacetno stran v html
@bottle.get("/")
def zacetna_stran():
    return bottle.template("zacetna_stran.html")

@bottle.post("/nova_igra/")
def nova_igra():
    tezavnost = bottle.request.forms.getunicode("tezavnost")
    if tezavnost == "lahko":
        velikost_polja = 8
        st_min = 10
    
    if tezavnost == "srednje":
        velikost_polja = 16
        st_min = 40

    else:
        velikost_polja = 22
        st_min = 99

    id_igre = minolovec.nova_igra(velikost_polja, st_min)
    bottle.response.set_cookie("id_igre", id_igre, path='/', secret=SECRET)
    bottle.redirect("/igra/")

@bottle.get("/igra/")
def pokazi_igro():
    id_igre = bottle.request.get_cookie("id_igre", secret=SECRET)
    [igra, velikost_polja, st_min, stanje] = minolovec.igre[id_igre]
    # igra = Polje()

    return bottle.template("igra.html", igra=igra, stanje=stanje, id_igre=id_igre, ZMAGA=model.ZMAGA, PORAZ=model.PORAZ, st_min=st_min, velikost_polja=velikost_polja)

#ni se v redu
@bottle.post("/igra/")
def ugibaj():
    id_igre = bottle.request.get_cookie("id_igre", secret=SECRET)
    poskus = bottle.request.forms.getunicode("poskus")
    #podatke poslane prek POST preberes iz request.forms iz igra.html
    #dobit moram vr, st, zastavico
    #najprej pogledat ce je veljaven vnos
    while not veljaven_vnos(minolovec, id_igre, poskus):
        stanje = NAPAKA #mogoce to ne bo delal ker je post?
        return bottle.template("igra.html", igra=igra, stanje=stanje)
    
    vnseseni_podatki = poskus.split(" ")
    vrstica = int(vnseseni_podatki[0])
    stolpec = int(vnseseni_podatki[1])
    
    minolovec.ugibaj(id_igre, vrstica, stolpec, vnseseni_podatki[- 1] == "f")
    
    bottle.redirect('/igra/')


def veljaven_vnos(minolovec, id_igre, poskus):
    vnseseni_podatki = poskus.split(" ")
    st = len(vnseseni_podatki)
    if st == 2:
        prvi = vnseseni_podatki[0]
        drugi = vnseseni_podatki[1]
        if prvi.isdigit() and drugi.isdigit():
            if 0 <= int(prvi) < (minolovec.igre[id_igre][1]) and 0 <= int(drugi) < (minolovec.igre[id_igre][1]):
                return True
        else:
            return False
    elif st == 3:
        prvi = vnseseni_podatki[0]
        drugi = vnseseni_podatki[1]
        if prvi.isdigit() and drugi.isdigit():
            if 0 <= int(prvi) < (minolovec.igre[id_igre][1]) and 0 <= int(drugi) < (minolovec.igre[id_igre][1]):
                if vnseseni_podatki[2] == "f":
                    return True
        else:
            return False
    else:
        return False


bottle.run(reloader=True, debug=True)