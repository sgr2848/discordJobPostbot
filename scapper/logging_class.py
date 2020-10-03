import logging
from logging.handlers import RotatingFileHandler
import os


class Logger_Setup():
    def __init__(self,
                 debug_fn=None,
                 info_fn=None,
                 warning_fn=None,
                 error_fn=None,
                 crit_fn=None,
                 create_save_path=False,
                 save_path='None',
                 func_name='None',
                 silence_logs=False):

        if debug_fn is None:
            debug_fn = 'debug_log.log'
        if info_fn is None:
            info_fn = 'info_log.log'
        if warning_fn is None:
            warning_fn = 'warning_log.log'
        if error_fn is None:
            error_fn = 'error_log.log'
        if crit_fn is None:
            crit_fn = 'CRITICAL_log.log'

        self.debug_fn = debug_fn
        self.info_fn = info_fn
        self.warning_fn = warning_fn
        self.error_fn = error_fn
        self.crit_fn = crit_fn

        self.save_path = save_path
        self.func_name = func_name
        self.silence_logs = silence_logs

        if create_save_path:
            self.create_save_path_func()

        self.initialize()

        if self.silence_logs:
            self.silence_logs_func()

        logging.raiseExceptions = False

    def create_save_path_func(self):

        save_path_str = self.save_path + self.func_name + '_logs'
        if not os.path.exists(save_path_str):
            os.makedirs(save_path_str)
        self.debug_fn = save_path_str + '/' + 'debug_log.log'
        self.info_fn = save_path_str + '/' + 'info_log.log'
        self.warning_fn = save_path_str + '/' + 'warning_log.log'
        self.error_fn = save_path_str + '/' + 'error_log.log'
        self.crit_fn = save_path_str + '/' + 'CRITICAL_log.log'

    def silence_logs_func(self):

        try:
            self.logger.debug(self.func_name + ' Silencing ')
            self.logger.setLevel(logging.INFO)
        except:
            self.logger.critical(
                self.func_name + ' couldnt set logging above debug')

    def initialize(self):

        ####Initialize Logging ###
        # The different levels of logging, from highest urgency to lowest urgency, are:
        # CRITICAL
        # ERROR
        # WARNING
        # INFO
        # DEBUG

        logfile1 = self.debug_fn
        logfile2 = self.info_fn
        logfile3 = self.warning_fn
        logfile4 = self.error_fn
        logfile5 = self.crit_fn
        # log_level = logging.DEBUG
        log_level = logging.INFO
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')

        fh = RotatingFileHandler(
            logfile1, mode='w', maxBytes=20 * 1024 * 1024, backupCount=5, encoding=None, delay=0)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        fh2 = RotatingFileHandler(
            logfile2, mode='w', maxBytes=20 * 1024 * 1024, backupCount=5, encoding=None, delay=0)
        fh2.setLevel(log_level)
        fh2.setFormatter(formatter)
        self.logger.addHandler(fh2)

        fh3 = RotatingFileHandler(
            logfile3, mode='w', maxBytes=20 * 1024 * 1024, backupCount=5, encoding=None, delay=0)
        fh3.setLevel(logging.WARNING)
        fh3.setFormatter(formatter)
        self.logger.addHandler(fh3)

        fh4 = RotatingFileHandler(
            logfile4, mode='w', maxBytes=20 * 1024 * 1024, backupCount=5, encoding=None, delay=0)
        fh4.setLevel(logging.ERROR)
        fh4.setFormatter(formatter)
        self.logger.addHandler(fh4)

        fh5 = RotatingFileHandler(
            logfile5, mode='w', maxBytes=20 * 1024 * 1024, backupCount=5, encoding=None, delay=0)
        fh5.setLevel(logging.CRITICAL)
        fh5.setFormatter(formatter)
        self.logger.addHandler(fh5)

        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        self.logger.debug('Loggers are setup!')


if __name__ == "__main__":
    placeholder = 0
