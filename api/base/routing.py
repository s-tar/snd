def init(app):
    from endpoints import auth
    from endpoints import users
    from endpoints import persons
    from endpoints import military_unit

    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(users.router, prefix="/user", tags=["User"])
    app.include_router(persons.router, prefix="/person", tags=["Person"])
    app.include_router(
        military_unit.router, prefix="/unit", tags=["Military Unit"]
    )

