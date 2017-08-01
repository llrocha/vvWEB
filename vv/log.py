import logging


#logging.basicConfig(filename='log.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='[%Y-%m-%d %H:%M:%S]')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#create file handler
handler = logging.FileHandler('log.log')
handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
#formatter.datefmt = '[%Y-%m-%d %H:%M:%S]'
handler.setFormatter(formatter)

logger.addHandler(handler)

#TEST
logger.debug('debug - Watch out!')  # will print a message to the console
logger.info('info - I told you so')  # will not print anything
logger.warning('warning - Watch out!')  # will print a message to the console
logger.error('error - I told you so')  # will not print anything
logger.critical('critical - Watch out!')  # will print a message to the console
a = 1
b = 0
a / b