from typing import Literal

from fastlife.adapters.xcomponent.registry import x_component
from tests.fastlife_app.models import Person


@x_component()
def HelloWorld(
    person: Person | None,
    method: Literal["get", "post"] = "post",
):
    # lang JSX
    return """
        <Layout>
        <H1>Hello {
            if person {
                if person.nick {
                    <>{person.nick}</>
                }
                else {
                    <>World</>
                }
            }
            else {
                <>World</>
            }
        }!</H1>
        <Form method={method}>
            <Input name="person.nick" label="Name" aria_label="First name and last name, or surname" />
            <Button aria_label="submit">Submit</Button>
        </Form>
        </Layout>
    """
