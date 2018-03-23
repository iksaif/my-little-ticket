"""Views."""
from annoying import decorators as an_decorators


@an_decorators.render_to('index.html')
def index(request):
    """Show the list of boards."""
    return {}
