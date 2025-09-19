(bootstrap-with-poetry)=
# Bootstrap with poetry

In this section, we build a Python package ready application.


## Create the project

Lets use the src layout, it's easier to find your code if it is at the same place
in all you projects.

```bash
poetry new --src myapp
cd myapp
```

This step is not mandatory, but, if you want are going to build some CSS with
pytailwindcss, you will need to fillout some path in a json.
You can't predict the name of you're virtualenv path, it depends on a username,
so it is better to enforce it's place before it is created.

```bash
cat << 'EOF' > poetry.toml
[virtualenvs]
path = ".venv"
EOF
```

Now we can add the `fastlifeweb` package with `jinjax` template rendering engine.

```bash
poetry add fastlifeweb[jinjax]
```


## Adding at tests

We ensure that the testings dependencies are installed and install pytest
to run our tests.

```bash
poetry add --group dev "fastlifeweb[testing]" pytes
```

Now lets write a tests.

We know that we want a page that put an hello world on its title.

```bash
cat << 'EOF' >  tests/test_views.py
from fastlife.testing import WebTestClient


def test_helloworld(client: WebTestClient) -> None:
    page = client.get("/")
    assert page.html.h1.text == "Hello World!"

EOF
```

At this point,we can see that we need a fixture to run our tests, and
we can starts by creating it in the main `conftest.py`
file of our project.

```
cat << 'EOF' >  tests/conftest.py
import pytest
from fastlife.testing import WebTestClient

from myapp.entrypoint import app


@pytest.fixture
def client() -> WebTestClient:
    return WebTestClient(app)

EOF
```

Here, we've decide to have a FastAPI app in a submodule entrypoint of our package.
At this moment you may want to run your tests to see it raising an ImportError.

### Adding the entrypoint

We will instanciate the Configurator and adding some configuration to build
the app we want.
We want a templates inside our package, the syntax `myapp:templates` is
here to says the directory templates inside the package myapp. We don't
care where myapp module is installed, so it's better than any absolute path
in any settings for our use cases.


```bash
cat << 'EOF' > src/myapp/entrypoint.py
from fastlife import Configurator, Settings

def build_app():
    config = Configurator(Settings())
    config.add_template_search_path("myapp:templates")
    config.include(".views")
    return config.build_asgi_app()

app = build_app()

EOF
```

```{tip}
Packaging an app in a package have lots of benefits,

in this situation, the template search path can be made using the package itself,
and the {meth}`config.include <fastlife.config.configurator.Configurator.include>`
can be relative from the module.
```

### Adding a view and its template.

```bash
cat << 'EOF' >  src/myapp/views.py
from fastlife import JinjaXTemplate, view_config

class HelloWorld(JinjaXTemplate):
    template = """
    <html>
        <body>
            <H1>Hello World!</H1>
        </body>
    <html>
    """

@view_config("hello_world", "/")
def hello_world() -> HelloWorld:
    return HelloWorld()
EOF
```


The view here hello_world return a template HelloWorld which is going to be
rendered by the JinjaX template engine.

The `H1` here is a component from the fastlife component library which
will render a `<h1>` in HTML. In {term}`JinjaX`, the template engined used,
by convention, `PascalCase` tag are Jinjax component and lowercase are simple HTML.


### Testing

At this time the test suite should run without errors.
```bash
poetry run pytest
```

```bash
poetry run fastapi dev src/myapp/entrypoint.py
```
