'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-04 09:50:40
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\views\dock\log.py
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
from PySide6.QtGui import QTextCursor

from src.modules.logger import get_global_logger
LOG = get_global_logger()

class LogDock(QDockWidget):
    
    # 自定义信号
    closeSignal = Signal(str)  
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        self.setWindowTitle(self.tr("日志", "window_title"))
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.setObjectName('NEUTRAL')
        self.setupUi()
    
    def setupUi(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        self.center_widget_layout = QVBoxLayout(self.center_widget)
        
        # 搜索框
        # self.search_box = QLineEdit(separentlf)
        # self.search_box.setObjectName('NEUTRAL') 
        # self.search_box.setPlaceholderText("请输入搜索项，按Enter搜索")
        # self.search_box.textChanged.connect()
        # center_widget_layout.addWidget(self.search_box)

        # 日志区
        self.logTextWidget = QTextEdit(self)
        self.center_widget_layout.addWidget(self.logTextWidget)
    
    @typing.override
    def closeEvent(self, event) -> None:
        self.closeSignal.emit('close')
        return super().closeEvent(event)

class QTextEditLogger:
    """ 使用 QTextEdit 作为日志记录器 """
    def __init__(self, outputWidget: QTextEdit):
        self.outputWidget = outputWidget
        LOG.add(self.log_to_widget, level="TRACE")

    def log_to_widget(self, message):
        log_level = message.record["level"].name
        background = None
        # 根据日志级别设置颜色
        if log_level == "CRITICAL":
            color = "white"
            background = "#de747e"
        elif log_level == "ERROR":
            color = "red"
        elif log_level == "WARNING":
            color = "orange"
        elif log_level == "SUCCESS":
            color = "green"
        elif log_level == "DEBUG":
            color = "blue"
        elif log_level == "TRACE":
            color = "skyblue"
        else:
            color = "black"
        # 构建 HTML 格式的日志消息
        html_message = f"""
            <div>
                <span style='color:gray; '>{message.record["time"].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}</span> | 
                <span style='color:{color}; background-color: {background}; font-weight: bold; '>{message.record["level"].name}</span> | 
                <span style='color:{color}; background-color: {background}; '>{message.record["message"]}</span> 
                <br>
            </div>
            """
        cursor = self.outputWidget.textCursor()  # 获取当前光标
        cursor.movePosition(QTextCursor.End)  # 将光标移动到末尾
        self.outputWidget.setTextCursor(cursor)  # 更新 QTextEdit 的光标
        # 在主线程中将日志插入到 QTextEdit 中
        self.outputWidget.insertHtml(html_message)

    def write(self, message):
        # 保持兼容性，write 方法处理一般的文本输出
        self.outputWidget.append(message)

    def flush(self):
        pass  # 不需要特殊的 flush 处理

