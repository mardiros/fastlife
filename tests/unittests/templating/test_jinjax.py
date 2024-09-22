from fastlife.templates.renderer.jinjax import AbstractTemplateRenderer


def test_render_template(renderer: AbstractTemplateRenderer):
    res = renderer.render_template("Page.jinja")
    assert (
        res
        == """\
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8" />
  <title>Fastlife</title>
</head>

<body><div>Hello World</div></body>

</html>\
"""
    )
