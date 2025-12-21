from xcomponent import XNode

from fastlife import XTemplate, x_component


@x_component(namespace="login")
def Layout(children: XNode):
    return """
    <>
    <!DOCTYPE html>
    <html>
    <layout.Head />
    <layout.Body>
        <div style="background: #ee0000">
        {children}
        </div>
    </layout.Body>
    </html>
    </>
    """


class XSigninTemplate(XTemplate):
    namespace = "login"
