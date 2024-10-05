from fastlife.config.resources import resource, resource_view


@resource(name="foo")  # missing path
class Foo:
    @resource_view()
    def collection_get(self): ...
