def init(app):
    from endpoints import auth
    from endpoints import users
    from endpoints import persons
    from endpoints import squads

    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(users.router, prefix="/users", tags=["User"])
    app.include_router(persons.router, prefix="/persons", tags=["Person"])
    app.include_router(squads.router, prefix="/squads", tags=["Squads"])

