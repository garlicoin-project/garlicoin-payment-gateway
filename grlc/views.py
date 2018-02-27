from decimal import Decimal
from grlc.services.address import receiver
from grlc.services.database import DbSession, Transaction, User
from grlc.services.log_service import LogService
from pyramid.view import view_defaults
from pyramid.response import Response

logger = LogService.logger


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
        """Return status of transaction given a valid transaction id as {i}"""
        transaction_id = self.request.matchdict.get('i')

        if not transaction_id or len(transaction_id) != 36:
            logger.info(f'Rejected get request with transaction id {transaction_id}')
            return Response(status=400)  # bad request

        with DbSession() as s:
            transaction = s.query(Transaction).filter_by(id=transaction_id).one_or_none()
            if transaction is None:
                logger.info(f'Get request for {transaction_id} not found')
                return Response(status=404)  # not found

            return Response(json_body={
                'status': transaction.status,
                'uuid': transaction_id,
            }, status=200)  # ok

    def post(self):
        """Create a new receipt transaction and return the transaction details"""
        gateway_user_id = self.request.matchdict.get('g')
        garlic_amount = _to_decimal(self.request.matchdict.get('a'))
        client_user_id = self.request.matchdict.get('u')
        client_order_id = self.request.matchdict.get('o')

        if (
            not gateway_user_id or len(gateway_user_id) != 36 or
            not garlic_amount or garlic_amount < 0 or
            client_user_id is None or client_order_id is None
        ):
            logger.warning(f'Rejected request for {gateway_user_id};{garlic_amount};{client_user_id};{client_order_id}')
            return Response(status=400)  # bad request

        with DbSession() as s:
            user = s.query(User).filter_by(id=gateway_user_id).one_or_none()
            if user is None:
                logger.warning(f'Unauthorized request by {gateway_user_id}')
                return Response(satus=401)  # unauthorized
            user_id = user.id

            # TODO: Validate receipt watching process is running?

            try:
                payment_address = receiver()
            except Exception as exc:
                logger.error(f'Error getting payment address: {exc}')
                return Response(body=str(exc), status=500)  # internal server error

            transaction = Transaction(
                payment_address=payment_address,
                payment_amount=garlic_amount,
                payment_amount_string=f'exactly {garlic_amount:.8f} GRLC',
                user_id=user_id,
                status='waiting',
            )
            s.add(transaction)
            s.commit()

            logger.info(f'Created transaction {transaction.id} for {garlic_amount} to {payment_address}')
            return Response(json_body={
                'uuid': transaction.id,
                'grlc_amt_str': transaction.payment_amount_string,
                'pmt_address': payment_address,
            },
                status=201,  # created
                location=f'/gateway?i={transaction.id}',
            )


def _to_decimal(value: str):
    """Return a Decimal object if given a well-formed GRLC amount string, otherwise return 0"""
    try:
        d = Decimal(value)
        if d.as_tuple().exponent < -8:
            d = 0
    except (ArithmeticError, TypeError):
        d = 0
    return d
