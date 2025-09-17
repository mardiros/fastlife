from typing import Literal

from fastlife.adapters.xcomponent.catalog import catalog
from tests.fastlife_app.models import Person


@catalog.component
def HelloWorld(
    person: Person,
    method: Literal["get", "post"] = "post",
):
    # lang JSX
    return """
        <Layout>
        <H1>Hello { person and person.nick or "World" }!</H1>
        <Form method={method}>
            <Input name="person.nick" label="Name" aria_label="First name and last name, or surname" />
            <Button aria_label="submit">Submit</Button>
        </Form>
        </Layout>
    """
