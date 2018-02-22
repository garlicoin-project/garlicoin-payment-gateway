from pyramid.config import Configurator


def main(_, **settings):
    config = Configurator(settings=settings)
    config.include('.services.log_service')
    config.include('.services.database')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
