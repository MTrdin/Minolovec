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

    minolovec.ugibaj(id_igre, vrstica, stolpec, zastavica)
    
    bottle.redirect('/igra/')


bottle.run(reloader=True, debug=True)