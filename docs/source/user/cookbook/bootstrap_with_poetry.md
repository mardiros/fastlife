# Bootstrap with poetry


## Boostrap the repository

```bash
poetry new --src myapp
cd myapp
poetry add fastlifeweb


cat << 'EOF' >  src/myapp/views.py
from fastlife import view_config, Response

@view_config("hello_world", "/",  template="HelloWorld.jinja")
def hello_world() -> dict[str, str]:
    return {}
EOF

mkdir src/myapp/templates
cat << 'EOF' > src/myapp/templates/HelloWorld.jinja
<html>
    <body>
        <h1>Hello world!</h1>
    </body>
<html>
EOF

cat << 'EOF' > src/myapp/entrypoint.py
from fastlife import Configurator, Settings

def build_app():
    config = Configurator(Settings())
    config.add_template_search_path("myapp:templates")
    config.include("myapp.views")
    return config.build_asgi_app()

app = build_app()

EOF

poetry run fastapi dev
```
