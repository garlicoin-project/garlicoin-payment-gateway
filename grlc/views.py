from pyramid.view import view_defaults
from pyramid.response import Response


@view_defaults(route_name='home')
class HomeView(object):
    def __init__(self, request):
        self.request = request

    def home(self):
        return Response(status=418)


@view_defaults(route_name='gateway')
class GatewayView(object):
    def __init__(self, request):
        self.request = request

    def get(self):
        transaction_id = self.request.matchdict.get('i')

        # TODO: Validate ID / get transaction
        status = 'testing'

        return Response(json_body={
            'status': status,
            'uuid': transaction_id})

    def post(self):
        gateway_user_id = self.request.matchdict.get('g')
        garlic_amount = self.request.matchdict.get('a')
        client_user_id = self.request.matchdict.get('u', '')
        client_order_id = self.request.matchdict.get('o', '')

        # TODO: Validate user (gateway_user_id)

        # TODO: Validate GRLC amount (number greater than zero)

        # TODO: Generate receiving address for transaction
        payment_address = 'Garlic1234'

        # TODO: Create transaction record
        transaction_id = 'uuid-transaction-id'

        return Response(json_body={
            'uuid': transaction_id,
            'grlc_amt_str': 'exactly 12.345 GRLC',
            'pmt_address': payment_address},
            status=201,
            location=f'/gateway?i={transaction_id}',
        )
