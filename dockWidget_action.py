'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-08-27 00:11:51
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\dockWidget_action.py
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
from PySide6.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLabel, QMainWindow, QDockWidget, QVBoxLayout, QLineEdit
    )
from PySide6.QtGui import QScreen
from PySide6.QtCore import Qt

class ActionDock(QDockWidget):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        self.setWindowTitle('行为关键字')
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.resize(400, 300)
        self.initUI()
    
    def initUI(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        center_widget_layout = QVBoxLayout(self.center_widget)
        

        # 搜索框
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("请输入搜索项，按Enter搜索")
        # self.search_box.textChanged.connect()
        center_widget_layout.addWidget(self.search_box)
