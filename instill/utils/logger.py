import logging
import os

home_dir = os.path.expanduser("~")


class Logger:
    Initialized = False

    @staticmethod
    def initialize(
        runlog_path=f"{home_dir}/.config/instill/sdk/python/run.log",
        errorlog_path=f"{home_dir}/.config/instill/sdk/python/error.log",
    ):
        os.makedirs(os.path.dirname(runlog_path), exist_ok=True)
        os.makedirs(os.path.dirname(errorlog_path), exist_ok=True)

        logger = logging.getLogger()

        # remove handlers added by installed package
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s"
        )
        runlog_handler = logging.FileHandler(runlog_path)
        runlog_handler.setLevel(logging.INFO)
        errorlog_handler = logging.FileHandler(errorlog_path)
        errorlog_handler.setLevel(logging.ERROR)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        runlog_handler.setFormatter(formatter)
        errorlog_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(runlog_handler)
        logger.addHandler(errorlog_handler)
        logger.addHandler(console_handler)
        Logger.Initialized = True

    @staticmethod
    def exception(message):
        assert Logger.Initialized, "Logger has not been initialized"
        logging.exception(message)

    @staticmethod
    def log(level, message):
        assert Logger.Initialized, "Logger has not been initialized"
        logging.log(level, message)

    @staticmethod
    def d(message):
        Logger.log(logging.DEBUG, message)

    @staticmethod
    def i(message):
        Logger.log(logging.INFO, message)

    @staticmethod
    def w(message):
        Logger.log(logging.WARNING, message)

    @staticmethod
    def e(message):
        Logger.log(logging.ERROR, message)
