'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-04 09:09:12
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\controllers\log_controller.py
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
from PySide6.QtCore import QObject

class LogController(QObject):
    
    def __init__(self, log_dock):
        # super().__init__()
        from src.views import LogDock
        self.view: LogDock = log_dock
        # self.__init_connections()
        # self.__connect_custom_signals()