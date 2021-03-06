import bottle
import model

SECRET = "Ena skrivnost"

minolovec = model.Minolovec()

@bottle.get("/")
def zacetna_stran():
    return bottle.template("zacetna_stran.html")

@bottle.post("/nova_igra/")
def nova_igra():
    tezavnost = bottle.request.forms.getunicode("tezavnost")

    if tezavnost == "lahko":
        velikost_polja = 8
        st_min = 10

    elif tezavnost == "srednje":
        velikost_polja = 16
        st_min = 40

    elif tezavnost == "tezko":
        velikost_polja = 19
        st_min = 98

    elif tezavnost == None:
        return bottle.template("zacetna_stran.html")

    #na koncu igre da te preusmiri na zacetno stran
    elif tezavnost == "hocem_novo_igro":
        return bottle.template("zacetna_stran.html")

    else:
        if veljaven_vnos_zacetek(tezavnost):
            podatki = tezavnost.split(" ")
            velikost_polja = int(podatki[0])
            st_min = int(podatki[1])
        else:
            return bottle.template("zacetna_stran.html")

    id_igre = minolovec.nova_igra(velikost_polja, st_min)
    bottle.response.set_cookie("id_igre", id_igre, path='/', secret=SECRET)
    bottle.redirect("/igra/")

#pomozna fuja za zacetek igre
def veljaven_vnos_zacetek(tezavnost):
    podatki = tezavnost.split(" ")
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

@bottle.get("/igra/")
def pokazi_igro():
    id_igre = bottle.request.get_cookie("id_igre", secret=SECRET)
    [igra, velikost_polja, st_min, stanje] = minolovec.igre[id_igre]
    return bottle.template("igra.html", igra=igra, stanje=stanje, id_igre=id_igre, ZMAGA=model.ZMAGA, PORAZ=model.PORAZ, st_min=st_min, velikost_polja=velikost_polja)

@bottle.post("/igra/")
def ugibaj():
    id_igre = bottle.request.get_cookie("id_igre", secret=SECRET)
    poskus = bottle.request.forms.getunicode("poskus")
    #podatke poslane prek POST preberes iz request.forms iz igra.html
    if not veljaven_vnos(id_igre, poskus):
        novo_stanje = model.NAPAKA
        [igra, velikost_polja, st_min, stanje] = minolovec.igre[id_igre]
        minolovec.igre[id_igre] = [igra, velikost_polja, st_min, novo_stanje]
        bottle.redirect('/igra/')

    vnseseni_podatki = poskus.split(" ")
    vrstica = int(vnseseni_podatki[0])
    stolpec = int(vnseseni_podatki[1])

    minolovec.ugibaj(id_igre, vrstica, stolpec, vnseseni_podatki[- 1] == "f")

    bottle.redirect('/igra/')

#pomozna za ugibaj
def veljaven_vnos(id_igre, poskus):
    vnseseni_podatki = poskus.split(" ")
    st = len(vnseseni_podatki)
    moja_igra = minolovec.igre[id_igre][0]

    if st == 2:
        prvi = vnseseni_podatki[0]
        drugi = vnseseni_podatki[1]
        if prvi.isdigit() and drugi.isdigit():
            if 0 <= int(prvi) < (len(moja_igra.polja)) and 0 <= int(drugi) < (len(moja_igra.polja)):
                return True
        else:
            return False
    elif st == 3:
        prvi = vnseseni_podatki[0]
        drugi = vnseseni_podatki[1]
        if prvi.isdigit() and drugi.isdigit():
            if 0 <= int(prvi) < (len(moja_igra.polja)) and 0 <= int(drugi) < (len(moja_igra.polja)):
                if vnseseni_podatki[2] == "f":
                    return True
        else:
            return False
    else:
        return False


bottle.run(reloader=True, debug=True)