import logging
def add(x,y):
    return x+ y

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
logger = logging.getLogger(__name__)


a = add(3,5)
logger.info(a)
print(a)