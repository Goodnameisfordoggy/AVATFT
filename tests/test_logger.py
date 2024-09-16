import os
import sys
import pytest
from loguru import logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import get_logger

# 测试 get_logger 函数是否返回一个 loguru logger 实例
log = get_logger()
assert isinstance(logger, logger.__class__)

log.trace('trace msg')
log.debug('debug msg')
log.info('info msg')
log.success('success msg')
log.warning('warning msg')
log.error('error msg')
log.critical('critical msg')

