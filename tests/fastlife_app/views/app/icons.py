from fastlife import Request, XTemplate, view_config


class IconsWall(XTemplate):
    template = """
    <Layout>
    <Icon name="academic-cap" />
    <Icon name="adjustments-horizontal" />
    <Icon name="adjustments-vertical" />
    </Layout>
    """


@view_config("icons", "/icons", methods=["GET"])
async def icons(request: Request) -> IconsWall:
    return IconsWall()
