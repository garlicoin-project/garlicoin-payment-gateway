from datetime import datetime, timedelta
from grlc.services.database import DbSession, Address
from grlc.services.garlicoin import Garlicoin
from grlc.services.log_service import LogService

REUSE_AGE = 2 * 24  # number of hours before an receiving address can be reused
logger = LogService.logger


def receiver():
    """Return an address from the wallet that is old enough to be reused or a newly generated address"""
    receiver_datetime = datetime.now()
    limit_datetime = receiver_datetime - timedelta(hours=REUSE_AGE)

    with DbSession() as s:
        next_address = s.query(Address).filter(Address.last_used < limit_datetime).first()
        if next_address is not None:
            next_address.last_used = receiver_datetime
            s.commit()
            candidate = next_address.address

            # ensure another process hasn't started to use the same address
            confirm = s.query(Address).filter_by(address=candidate).filter_by(last_used=receiver_datetime).one_or_none()
            if confirm is not None:
                logger.debug(f'Reusing address {confirm.address}')
                return confirm.address
            else:
                logger.warning(f'Lost address {candidate} after setting `last_used` to {receiver_datetime}')

        # if we get to this point, either we didn't find a usable address or someone else snagged it
        address = Garlicoin().getnewaddress()

        next_address = Address(
            address=address,
            last_used=receiver_datetime,
            balance_date=receiver_datetime,
            balance=0,
        )
        s.add(next_address)
        s.commit()
        logger.info(f'Created receiving address {address} at {receiver_datetime}')
        return address
