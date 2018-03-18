from decimal import Decimal
from grlc.services.log_service import LogService
import requests

logger = LogService.logger


class Garlicoin:
    rpc_username = 'test'
    rpc_password = 'test'
    rpc_id = 0

    @classmethod
    def global_init(cls, credentials: dict):
        cls.rpc_username = credentials['username']
        cls.rpc_password = credentials['password']

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

    def listtransactions(self, address: str='', count: int=10, skip: int=0):
        """Return most recent [count] transactions skipping first [skip] for [address]

        Returns a list of dictionaries with, for example:
            {'account': '',
             'address': 'GeMo9tJxQLfipPjeY1SdBJAgkQPpXf4EZm',
             'category': 'receive',  # 'send'
             'amount': 0.01753841,  # -0.01234567 for send
             'label': '',  # not used for send
             'vout': 237,
             # 'fee': -0.0033,  # send only
             'confirmations': 24100,
             'blockhash': '10c49c32be907a7c8f4330ff8250285dafb86edfb4f35f76d5781685f02d3573',
             'blockindex': 4,
             'blocktime': 1519291852,
             'txid': '6f42f052e4bb3f521b40e4e7895d0ac1bfa4c268646616ae13eae613efaabf18',
             'walletconflicts': [],
             'time': 1519291852,
             'timereceived': 1519485123,
             'bip125-replaceable': 'no',
             # 'abandoned': False,  # send only
             },
        """
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
        response = self._post('getnewaddress', None)
        address = response['result']
        if address[0] == 'G' and len(address) == 34:
            return address
