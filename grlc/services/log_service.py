import logging
from logging.handlers import SysLogHandler, SYSLOG_UDP_PORT


class LogService:
    logger = None

    @classmethod
    def setup_logging(cls, name: str, level: str):
        if cls.logger is not None:
            return

        formatter = logging.Formatter('[%(asctime)s] %(levelname)-3.3s: %(name)s: %(message)s')
        handler = SysLogHandler(address=('localhost', SYSLOG_UDP_PORT), facility=SysLogHandler.LOG_LOCAL0)
        handler.setLevel(level=level)
        handler.setFormatter(fmt=formatter)

        cls.logger = logging.getLogger(name=name)
        cls.logger.setLevel(level=level)
        cls.logger.addHandler(hdlr=handler)


def includeme(config):
    settings = config.get_settings()
    LogService.setup_logging(name='grlc', level=settings.get('log_level'))
