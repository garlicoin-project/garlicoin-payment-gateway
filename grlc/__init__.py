import json
from pyramid.config import Configurator
from grlc.services.garlicoin import Garlicoin


def main(_, **settings):
    config = Configurator(settings=settings)
    config.include('.services.log_service')
    config.include('.services.database')
    config.include('.routes')
    Garlicoin.global_init(credentials=json.load(open('credentials.json')))
    return config.make_wsgi_app()
