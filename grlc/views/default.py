from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home')
def home_view(request):
    return Response(418)


@view_config(route_name='request', renderer='json')
def request_view(request):
    return {'uuid': 'unique-id-for-transaction', 'grlc_amt_str': 'exactly 12.345 GRLC', 'pmt_address': 'Garlic1234'}


@view_config(route_name='status', renderer='json')
def status_view(request):
    return {'status': 'waiting', 'uuid': 'uuid'}
