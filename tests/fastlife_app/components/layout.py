from xcomponent import XNode

from fastlife.adapters.xcomponent.catalog import catalog


@catalog.component
def Layout(children: XNode):
    return """
    <>
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>test - Fastlife</title>
        <script src="/static/scripts/htmx.2.0.1.min.js" crossorigin="anonymous">{""}</script>
        <link href="/static/css/main.css" rel="stylesheet" />
    </head>
    <body>
        {/* <script>
        htmx.logAll();
        </script> */}
        <div id="maincontent" hx-target="this" hx-swap="innerHTML">
        { children }
        </div>
    </body>
    </html>
    </>
    """
