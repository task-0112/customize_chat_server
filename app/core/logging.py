import logging


def init_logging():
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(module)s@%(funcName)s:%(lineno)d] %(message)s",
    )
