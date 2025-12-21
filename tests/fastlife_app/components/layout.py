from xcomponent import Catalog, XNode

from fastlife.adapters.xcomponent.registry import x_component

layout_catalog = Catalog()


@x_component(namespace="layout")
def Head():
    return """
    <head>
        <meta charset="utf-8" />
        <title>test - Fastlife</title>
        <script src="/static/scripts/htmx.2.0.1.min.js" crossorigin="anonymous">{""}</script>
        <link href="/static/css/main.css" rel="stylesheet" />
    </head>
    """


@x_component(namespace="layout")
def Body():
    return """
    <body>
        {/* <script>
        htmx.logAll();
        </script> */}
        <div id="maincontent" hx-target="this" hx-swap="innerHTML">
        {children}
        </div>
    </body>
    """


@x_component()
def Layout(children: XNode):
    return """
    <>
    <!DOCTYPE html>
    <html>
    <layout.Head />
    <layout.Body>{children}</layout.Body>
    </html>
    </>
    """
