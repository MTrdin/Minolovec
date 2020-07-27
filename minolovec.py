import bottle
import model

@bottle.get("/")
def index():
    pass

@bottle.post("/nova_igra/")
def nova_igra():
    pass

@bottle.get("/igra/")
def pokazi_igro():
    pass


@bottle.post("/igra/")
def ugibaj():
    pass


bottle.run(reloader=True, debug=True)