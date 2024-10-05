from fastlife.config.resources import resource, resource_view


@resource(name="working", path="/working")
class Bar:
    @resource_view()
    def get(self): ...
