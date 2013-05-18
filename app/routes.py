# third-party imports
from webapp2 import Route


ROUTES = [

    Route(r'/', 'app.handlers.hb_example', name='index'),
    Route(r'/hb/', 'app.handlers.hb_example', name='index-hb'),
    Route(r'/j2/', 'app.handlers.j2_example', name='index-j2'),
    Route(r'/json/', 'app.handlers.json_example', name='index-json'),

]
