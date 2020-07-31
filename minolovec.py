import bottle
import model


minolovec = model.Minolovec()

#ali def index()
#se treba narest zacetno stran v html
@bottle.get("/")
def zacetna_stran():
    return bottle.template("zacetna_stran.html")

@bottle.post("/nova_igra/")
def nova_igra():
    id_igre = minolovec.nova_igra(velikost_polja, st_min)
    #se piskotek
    bottle.redirect("/igra/")

@bottle.get("/igra/")
def pokazi_igro():
    #id_igre = bottle.request.get_cookie("id_igre", secret=SECRET)
    [igra, velikost_polja, st_min, stanje] = minolovec.igre[id_igre]

    return bottle.template("igra.html", igra=igra, stanje=stanje, id_igre=id_igre, ZMAGA=model.ZMAGA, PORAZ=model.PORAZ)

#ni se v redu
@bottle.post("/igra/")
def ugibaj():
    #id_igre = bottle.request.get_cookie("id_igre", secret=SECRET)
    crka = bottle.request.forms.getunicode("crka")
    #podatke poslane prek POST preberes iz request.forms iz igra.html
    #dobit moram vr, st, zastavico

    minolovec.ugibaj(id_igre, vrstica, stolpec, zastavica)
    
    bottle.redirect('/igra/')


bottle.run(reloader=True, debug=True)