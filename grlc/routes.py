import grlc.views as v


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_view(v.HomeView, attr='home')
    
    config.add_route('gateway', '/gateway')
    config.add_view(v.GatewayView, attr='get', request_method='GET')
    config.add_view(v.GatewayView, attr='post', request_method='POST')
    config.add_view(v.GatewayView, attr='delete', request_method='DELETE')
