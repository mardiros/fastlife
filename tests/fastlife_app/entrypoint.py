from tests.fastlife_app.config import MyConfigurator, MySettings


def build_app():
    conf = MyConfigurator(MySettings(session_secret_key="supasickret"))
    conf.include(".adapters")
    conf.include(".config")
    conf.include(".components")
    conf.include(".views", ignore=[".api", ".app.admin"])
    conf.include(".views.api", route_prefix="/api")
    conf.include(".views.app.admin", route_prefix="/admin")
    conf.include(".static")
    conf.include(".jobs")
    return conf.build_asgi_app()


app = build_app()
