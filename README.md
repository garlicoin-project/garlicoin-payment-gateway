Garlicoin Payment Gateway
=========================

Client/Gateway transaction process
----------------------------------

Client requests payment destination:
`POST https://grlc.cash/gateway?g={gatewayUserID}&a={grlcAmount}&u={clientUserID}&o={clientOrderID}`

GRLC Gateway responds:
`{"uuid": "unique-id-for-transaction", "grlc_amt_str": "exactly 12.345 GRLC", "pmt_address": "Garlic1234"}`

GRLC Gateway forwards funds to user:
`amount * (1 - fee) send to wallet address from user record`

GRLC Gateway sends notice to user:
`{clientCallbackUrl}: {"user_id": {clientUserID}, "order_id": {clientOrderID}, "amount": {amountReceived}, }`

Client requests status update:
`GET https://grlc.cash/gateway?i={uuid}`
    
GRLC Gateway responds:
`{"status": "waiting/expired/received", "uuid": "{uuid}"}`


Notes:
------

- use address indexes from https://github.com/garlicoin-project/garlicore-garlicoin
- need a database to store user records and wallet transactions
- need to generate wallet addresses and monitor receipts
- need to sign and send transactions
