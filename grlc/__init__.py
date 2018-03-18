import json
from pyramid.config import Configurator
from grlc.services.garlicoin import Garlicoin


def main(_, **settings):
    config = Configurator(settings=settings)
    config.include('.services.log_service')
    config.include('.services.database')
    config.include('.routes')
    try:
        credentials = json.load(open('credentials.json'))
    except FileNotFoundError:
        credentials = {'username': 'test', 'password': 'test'}
    Garlicoin.global_init(credentials=credentials)
    return config.make_wsgi_app()
