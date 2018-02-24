from decimal import Decimal
from grlc.services.log_service import LogService
import requests

logger = LogService.logger


class Garlicoin:
    rpc_username = 'test'
    rpc_password = 'test'
    rpc_id = 0

    def global_init(self, credentials: dict):
        self.rpc_username = credentials['username']
        self.rpc_password = credentials['password']

    def _post(self, method: str, params: list=None):
        url = f'http://{self.rpc_username}:{self.rpc_password}@localhost:42068'
        payload = {
            'method': method,
            'params': params,
            'jsonrpc': '2.0',
            'id': self.rpc_id,
        }
        response = requests.post(url=url, json=payload)
        self.rpc_id += 1
        data = response.json()
        if data['error']:
            logger.warning(f'RPC Call {data["id"]}:{method} returned error {data["error"]}')
        return data['result']

    def getblockcount(self):
        """Return highest block # in local copy of blockchain"""
        return self._post('getblockcount')

    def listtransactions(self, address: str, count: int=10, skip: int=0):
        """Return most recent [count] transactions skipping first [skip] for [address]"""
        return self._post('listtransactions', [address, count, skip])

    def gettransaction(self, txid: str):
        """Return transaction details for [txid]"""
        return self._post('gettransaction', [txid])

    def listaccounts(self):
        """Return all accounts and balances in wallet"""
        return self._post('listaccounts', None)

    def sendtoaddress(self, address: str, amount: Decimal, comment: str=''):
        """Send [amount] GRLC to [address] with optional [comment] attached"""
        return self._post('sendtoaddress', [address, amount, comment])

    def getnewaddress(self):
        """Return a new address for receiving payments"""
        return self._post('getnewaddress', None)
