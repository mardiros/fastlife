from tests.fastlife_app.config import MyConfigurator, MySettings


def build_app():
    conf = MyConfigurator(
        MySettings(
            session_secret_key="supasickret",
            jinjax_auto_reload=True,
        )
    )
    conf.add_template_search_path("tests.fastlife_app:templates")
    conf.include(".adapters")
    conf.include(".config")
    conf.include(".components")
    conf.include(".views", ignore=[".api", ".app.admin"])
    conf.include(".views.api", route_prefix="/api")
    conf.include(".views.app.admin", route_prefix="/admin")
    conf.include(".static")
    return conf.build_asgi_app()


app = build_app()
