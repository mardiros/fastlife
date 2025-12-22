(add-css-stylesheet)=

# Add CSS stylesheet

To add CSS stylesheet, we have many choices, and know, we can split the works in
two main parts, build CSS and serve CSS.

Building CSS is optional, or you can use the framework you want for that,
so we starts by that step, using {term}`Tailwind CSS` and actually, the
wrapped version in python directly.
Using [pytailwindcss](https://pypi.org/project/pytailwindcss/), you don't have
to manage nodejs and npm for you, this is made for you.

:::{admonition} Before you continue
The example here requires you have already bootrap an project named myapp
for the needs. The [boostrap with poetry](#bootstrap-with-poetry) recipes
has been used user.
:::

## Building the CSS

If you are using poetry, like in the tutorial
[boostrap with poetry](#bootstrap-with-poetry), you can add pytailwindcss
as a dev dependency. You can adapt with your own packaging tool.

```bash
poetry add --group dev pytailwindcss
```

Now, we need two directory, the first one is the source for our process, the input.
And the second is the compilation result of the css, the output.

```bash
mkdir -p src/myapp/assets/styles
mkdir -p src/myapp/static/css
```

Using tailwind, we don't need to write CSS, those classes
alreay exists, you use them, and tailwind will grab them
in order to right the css.

Basically, we install the tailwind css classes like below and
never look back in it.

```bash
cat << 'EOF' > src/myapp/assets/styles/main.css
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF
```

Now compile the css we can run:

```bash
poetry run tailwindcss \
  -i src/myapp/assets/styles/main.css \
  -o src/myapp/static/css/main.css
```

This command will warn you that **No utility classes were detected in your source
files**. This is correct. We dont write class yet.

It provide you a links to https://tailwindcss.com/docs/content-configuration
in order to have a spells of tailwint congiruation.

In the [boostrap with poetry](#bootstrap-with-poetry) recipe, there is a step
to ensure you create the venv inside the project in order to load the classes
of fastlife.

We will bootstrap a configuration that grab classes from our templates
and from fastlife too.

```bash
cat << 'EOF' > tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./src/myapp/templates/*.jinja",
    "./src/myapp/templates/**/*.jinja",
    ".venv/lib/python3.*/site-packages/fastlife/template_globals.py",
    ".venv/lib/python3.*/site-packages/fastlife/components/*.jinja",
    ".venv/lib/python3.*/site-packages/fastlife/components/**/*.jinja",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f0f9ff",
          100: "#e0f2fe",
          200: "#bae6fd",
          300: "#7dd3fc",
          400: "#38bdf8",
          500: "#0ea5e9",
          600: "#0284c7",
          700: "#0369a1",
          800: "#075985",
          900: "#0c4a6e",
          950: "#082f49",
        },
        danger: {
          50: "#fef2f2",
          100: "#fee2e2",
          200: "#fecaca",
          300: "#fca5a5",
          400: "#f87171",
          500: "#ef4444",
          600: "#dc2626",
          700: "#b91c1c",
          800: "#991b1b",
          900: "#7f1d1d",
          950: "#450a0a",
        },
        neutral: {
          50: "#fafaf9",
          100: "#f5f5f4",
          200: "#e7e5e4",
          300: "#d6d3d1",
          400: "#a8a29e",
          500: "#78716c",
          600: "#57534e",
          700: "#44403c",
          800: "#292524",
          900: "#1c1917",
          950: "#0c0a09",
        },
      },
    },
  },
  plugins: [],
};
EOF
```

:::{tip}
Tailwind CSS can grab class names in python file too.
All the basic X compoments classes of fastlife are
actually in
[the Constant](#fastlife.template_globals.Globals) class
that is completly replacable in the setting
[xcomponent_global_catalog_class](#fastlife.settings.Settings.xcomponent_global_catalog_class)

```python
# content of the file src/myapp/contants.py
from fastlife.templating.renderer.constants import Constant
class MyConstants(Constant):
    ...
```

and then set the settings to
`FASTLIFE_Xcomponent_GLOBAL_CATALOG_CLASS="myapp.contants:MyConstants"`
:::

Fastlife use a set of 3 colors, primary, danger and neutral. You can add
your on colors or use the Tailwind predefined colors too.

Runng tailwindcss should not warn anymore.

```bash
$ poetry run tailwindcss \
  -i src/myapp/assets/styles/main.css \
  -o src/myapp/static/css/main.css

Rebuilding...

Done in 774ms.
```

## Serving the CSS and all the assets

To server the assets, the method
{meth}`add_static_route <fastlife.config.configurator.GenericConfigurator.add_static_route>`
is used to serve the css and then we can inject it to our html in order to be loaded.

```bash
cat << 'EOF' > src/myapp/static/__init__.py
from pathlib import Path

from fastlife import Response, Configurator, configure

static_dir = Path(__file__).parent


@configure
def includeme(config: Configurator) -> None:
    config.add_static_route("/static/css", static_dir / "css", name="static")
EOF
```

:::{admonition} Why The static dir is not mounted directly ?
Yes you can, in that case to a static dir in the static dir in order
to not serve any `.py` file to avoid any security issue.
:::

To serve the css, we have to load the static route in the app, we will update
the application entrypoint.

```bash
cat << 'EOF' > src/myapp/entrypoint.py
from fastlife import Configurator, Settings

def build_app():
    config = Configurator(Settings())
    config.include(".views")
    config.include(".static")
    return config.build_asgi_app()

app = build_app()
EOF
```

Now the css ared served here.

We can adapt our HelloWorld template in order to inherits from a shared page layout.

Lets write a Layout component, that will load the CSS.

```python
@x_component()
def Layout(children: XNode, title: str = "Hello World") -> str:
    return """
    <>
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8" />
                <title>{title}</title>
                <link href="/static/css/main.css" rel="stylesheet" />
            </head>
            <body>
                {children}
            </body>
        </html>
    </>
    """
```

### Testing

We can observe that the Hello World style is applyied by running the app.

```bash
poetry run fastapi dev src/myapp/entrypoint.py
```

### Before you go

Here is a version of the static that also load a favicon.ico

Add a favicon in the static directory and replace the `__init__.py` file
to get an icon in the browser.

```python
from pathlib import Path

from fastlife import Response, Configurator, configure
from starlette.responses import FileResponse

static_dir = Path(__file__).parent
favicon_path = Path(__file__).parent / "favicon.ico"


async def favicon() -> Response:
    return FileResponse(favicon_path)


@configure
def includeme(config: Configurator) -> None:
    config.add_route("favicon", "/favicon.ico", favicon, methods=["GET"])
    config.add_static_route("/static/css", static_dir / "css", name="static")

```
