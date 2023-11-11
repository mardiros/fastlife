if __name__ == "__main__":
    import uvicorn

    from fastlife import Configurator
    from fastlife.configurator.configurator import Settings

    def getapp():
        conf = Configurator(
            Settings(template_search_path="fastlife:templates,fastlife_app:templates")
        )
        conf.include("fastlife_app.views")
        return conf.get_app()

    app = getapp()

    uvicorn.run(app, host="0.0.0.0", port=8000)
