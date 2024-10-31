'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-10-31 21:43:43
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\modules\logger.py
Description: 

				*		写字楼里写字间，写字间里程序员；
				*		程序人员写程序，又拿程序换酒钱。
				*		酒醒只在网上坐，酒醉还来网下眠；
				*		酒醉酒醒日复日，网上网下年复年。
				*		但愿老死电脑间，不愿鞠躬老板前；
				*		奔驰宝马贵者趣，公交自行程序员。
				*		别人笑我忒疯癫，我笑自己命太贱；
				*		不见满街漂亮妹，哪个归得程序员？    
Copyright (c) 2024 by HDJ, All Rights Reserved. 
'''
import os
import sys
from loguru import logger
from src import LOG_DIR

logger_global = logger
logger_global.remove()

logger_global.add(sys.stdout, level="TRACE")

logger_global.add(
    os.path.join(LOG_DIR, "{time:YYYY-MM-DD}.log"),
    rotation="1 day",
    retention="1 month",
    level="TRACE",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    colorize=True
)

LOG = logger_global



