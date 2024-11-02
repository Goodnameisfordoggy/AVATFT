'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-02 22:43:28
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\views\mainWindow.py
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
import typing
from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QTextEdit, QToolBar
from PySide6.QtGui import QAction, QIcon, QTextCursor
from PySide6.QtCore import Qt, Signal

from src.views import ActionDock, EditDock, LogDock, ProjectDock, ReconfirmDialogBox
from src.controllers import ProjectController
from src import ICON_DIR

class Main_Window(QMainWindow):
    
    def __init__(self, app):
        super().__init__()
        self.__app = app
        self.setWindowTitle(self.tr("行为可视化自动测试平台"))

        # 获取主屏幕的大小
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.screen_width = screen_size.width()
        self.screen_height = screen_size.height()
        self.resize(self.screen_width - 100, self.screen_height - 100)
        self.setWindowIcon(QIcon(os.path.join(ICON_DIR, 'app.svg')))
        
        self.__build_menu()
        self.__create_dock_widgets()
        self.__initialize_layout()
        self.showMaximized()  # 将窗口设置为最大化    
        
        # 重定向标准输出和标准错误到自定义输出类
        # sys.stdout = ConsoleOutput(self.log_dock.ui.logTextWidget)
        # sys.stderr = ConsoleOutput(self.log_dock.ui.logTextWidget)
        # # 将日志输出到自定义输出类
        # textEditLogger = QTextEditLogger(self.log_dock.ui.logTextWidget)
    
    def __build_menu(self):
        # 创建菜单栏
        self.menuBar = self.menuBar()

        # 创建菜单
        self.fileMenu = QMenu(self.tr("文件"), self)        
        self.viewMenu = QMenu(self.tr("视图"), self)
        self.languageMenu = QMenu(self.tr("语言"), self)
        self.helpMenu = QMenu(self.tr("帮助"), self)

        # fileMenu动作
        self.newProjectAction = QAction(self.tr("新建工程"), self)
        self.newProjectAction.setIcon(QIcon(os.path.join(ICON_DIR, 'folder-plus.svg')))
        
        self.openProjectAction = QAction(self.tr("打开工程"), self)
        self.openProjectAction.setIcon(QIcon(os.path.join(ICON_DIR, 'folder-search.svg')))
        self.exitAction = QAction(self.tr("退出"), self)
        self.exitAction.setIcon(QIcon(os.path.join(ICON_DIR, 'window-close.svg')))
        self.exitAction.triggered.connect(self.close)  # 连接退出动作到窗口的关闭功能

        self.fileMenu.addAction(self.newProjectAction)
        self.fileMenu.addAction(self.openProjectAction)
        self.fileMenu.addSeparator()  # 分隔符
        self.fileMenu.addAction(self.exitAction)
        
        # viewMenu 动作
        self.actionDockAction = QAction(QIcon(os.path.join(ICON_DIR, 'view-dashboard-variant.svg')), self.tr("自动化测试关键字窗口", "view_keyword_window"), self)
        self.editDockAction = QAction(QIcon(os.path.join(ICON_DIR, 'view-dashboard-variant.svg')), self.tr("自动化测试编辑窗口", "view_edit_window"), self)
        self.projectDockAction = QAction(QIcon(os.path.join(ICON_DIR, 'view-dashboard-variant.svg')), self.tr("自动化测试项目窗口", "view_project_window"), self)
        self.logDockAction = QAction(self.tr("自动化测试日志窗口", "view_log_window"), self)

        self.viewMenu.addAction(self.actionDockAction)
        self.viewMenu.addSeparator()  # 分隔符
        self.viewMenu.addAction(self.editDockAction)
        self.viewMenu.addSeparator()  # 分隔符
        self.viewMenu.addAction(self.projectDockAction)
        self.viewMenu.addSeparator()  # 分隔符
        self.viewMenu.addAction(self.logDockAction)

        # languageMenu 动作
        self.zh_CN_Action = QAction('zh_CN', self)
        self.en_US_Action = QAction('en_US', self)
        self.languageMenu.addAction(self.zh_CN_Action)
        self.languageMenu.addAction(self.en_US_Action)

        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.viewMenu)
        self.menuBar.addMenu(self.languageMenu)
        self.menuBar.addMenu(self.helpMenu)
    
    def __create_dock_widgets(self):
        # 关键词区域
        self.action_dock = ActionDock('', self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.action_dock)

        # 正在编辑用例区域
        self.edit_dock = EditDock('', self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.edit_dock)

        # 工程区域
        self.project_dock = ProjectDock('', self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.project_dock)

        # 日志区域
        self.log_dock = LogDock('', self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.log_dock)
        self.log_dock.setVisible(False)
    
    def __initialize_layout(self):
        
        # 分割 Horizontal Vertical
        self.splitDockWidget(self.action_dock, self.edit_dock, Qt.Horizontal)
        self.splitDockWidget(self.edit_dock, self.project_dock, Qt.Horizontal)
        self.resizeDocks([self.action_dock, self.edit_dock, self.project_dock], [250, 500, 250], Qt.Horizontal)
    
    @typing.override
    def contextMenuEvent(self, event):
        # 阻止右键菜单的弹出
        event.ignore()
    
    @typing.override
    def closeEvent(self, event):
        # 恢复标准输出和标准错误，保持良好的编程习惯Qwq。
        # 程序结束时，操作系统会自动释放所有资源，包括标准输出和标准错误的重定向。
        # 因此，这种重定向不会影响其他正在运行的程序，也不会影响外部的终端或控制台。
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        super().closeEvent(event)

class ConsoleOutput:
    """ 用于重定向控制台输出 """
    def __init__(self, outputWidget: QTextEdit):
        self.outputWidget = outputWidget

    def write(self, message):
        # 不做任何处理，直接输出到控制台
        sys.__stdout__.write(message)
        sys.__stdout__.flush()

        # 确保 message 是字符串类型
        if isinstance(message, bytes):
            message = message.decode('utf-8')  # 将 bytes 转换为 str
        # 去除前后空白字符
        message = message.strip().translate(str.maketrans('', '', '^~'))
        # 只在 message 非空时才追加到 QTextEdit
        if message:
            self.outputWidget.append(message + '\n')
    
    def flush(self):
        """ 清空缓冲区 """
        # 需要实现这个方法以避免报错
        sys.__stdout__.flush()


# class QTextEditLogger:
#     """ 使用 QTextEdit 作为日志记录器 """
#     def __init__(self, outputWidget: QTextEdit):
#         self.outputWidget = outputWidget
#         LOG.add(self.log_to_widget, level="TRACE")

#     def log_to_widget(self, message):
#         log_level = message.record["level"].name
#         background = None
#         # 根据日志级别设置颜色
#         if log_level == "CRITICAL":
#             color = "white"
#             background = "#de747e"
#         elif log_level == "ERROR":
#             color = "red"
#         elif log_level == "WARNING":
#             color = "orange"
#         elif log_level == "SUCCESS":
#             color = "green"
#         elif log_level == "DEBUG":
#             color = "blue"
#         elif log_level == "TRACE":
#             color = "skyblue"
#         else:
#             color = "black"
#         # 构建 HTML 格式的日志消息
#         html_message = f"""
#             <div>
#                 <span style='color:gray; '>{message.record["time"].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}</span> | 
#                 <span style='color:{color}; background-color: {background}; font-weight: bold; '>{message.record["level"].name}</span> | 
#                 <span style='color:{color}; background-color: {background}; '>{message.record["message"]}</span> 
#                 <br>
#             </div>
#             """
#         cursor = self.outputWidget.textCursor()  # 获取当前光标
#         cursor.movePosition(QTextCursor.End)  # 将光标移动到末尾
#         self.outputWidget.setTextCursor(cursor)  # 更新 QTextEdit 的光标
#         # 在主线程中将日志插入到 QTextEdit 中
#         self.outputWidget.insertHtml(html_message)

#     def write(self, message):
#         # 保持兼容性，write 方法处理一般的文本输出
#         self.outputWidget.append(message)

#     def flush(self):
#         pass  # 不需要特殊的 flush 处理