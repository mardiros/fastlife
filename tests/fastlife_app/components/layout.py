from xcomponent import Catalog, XNode

from fastlife.adapters.xcomponent.registry import x_component

layout_catalog = Catalog()


@layout_catalog.component
def Head():
    return """
    <head>
        <meta charset="utf-8" />
        <title>test - Fastlife</title>
        <script src="/static/scripts/htmx.2.0.1.min.js" crossorigin="anonymous">{""}</script>
        <link href="/static/css/main.css" rel="stylesheet" />
    </head>
    """


@layout_catalog.component
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


@x_component(use={"layout": layout_catalog})
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
