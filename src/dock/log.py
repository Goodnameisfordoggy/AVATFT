'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-10-03 00:01:07
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\src\dock\log.py
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
import typing
from PySide6.QtWidgets import (
    QWidget, QDockWidget, QVBoxLayout, QLineEdit, QTextEdit
	)
from PySide6.QtCore import Signal


class LogDock(QDockWidget):
    
    # 自定义信号
    closeSignal = Signal(str)  
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        self.setWindowTitle('日志')
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.setObjectName('NEUTRAL')
        self.__initUI()
        
    def __initUI(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        center_widget_layout = QVBoxLayout(self.center_widget)
        
        # 搜索框
        # self.search_box = QLineEdit(self)
        # self.search_box.setObjectName('NEUTRAL') 
        # self.search_box.setPlaceholderText("请输入搜索项，按Enter搜索")
        # # self.search_box.textChanged.connect()
        # center_widget_layout.addWidget(self.search_box)

        # 日志区
        self.logTextWidget = QTextEdit(self)
        center_widget_layout.addWidget(self.logTextWidget)
    
    @typing.override
    def closeEvent(self, event) -> None:
        self.closeSignal.emit('close')
        return super().closeEvent(event)

