'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-09-26 23:32:05
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\src\mainWindow.py
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
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QTextEdit 
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, Signal, Slot

from utils import logger
from src.dock.edit import EditDock
from src.dock.action import ActionDock 
from src.dock.log import LogDock
from src.dock.project import ProjectDock
from src.dialogBox.input import NameInputDialogBox
from src import PROJECTS_DIR, ICON_DIR
LOG = logger.get_logger()


class ConsoleOutput:
    """ 用于重定向控制台输出 """
    def __init__(self, outputWidget: QTextEdit):
        self.outputWidget = outputWidget

    def write(self, message):
        # 将信息追加到 QTextEdit 中
        self.outputWidget.append(message)
        # 输出到控制台
        sys.__stdout__.write(message)
        sys.__stdout__.flush()

    def flush(self):
        """ 清空缓冲区 """
        # 需要实现这个方法以避免报错
        sys.__stdout__.flush()


class QTextEditLogger:
    """ 用于将日志输出到 QTextEdit """
    def __init__(self, outputWidget):
        self.outputWidget = outputWidget
        LOG.add(self, level="TRACE")
		
    def write(self, message):
        # 将日志输出到 QTextEdit
        self.outputWidget.append(message)

    def flush(self):
        pass  # 不需要特殊的 flush 处理
    

class MainWindow(QMainWindow):
    
    # 自定义信号
    new_project_signal = Signal(str)
    loadProjectSignal = Signal(str)
    
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("可视化自动测试框架工具")

        # 获取主屏幕的大小
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.screen_width = screen_size.width()
        self.screen_height = screen_size.height()
        self.resize(self.screen_width, self.screen_height)
        # self.maximumSize()        

        self.__build_menu()
        self.__create_dock_widgets()
        self.__initialize_layout()
        self.__connect_signals()

        # 重定向标准输出和标准错误到自定义输出类
        sys.stdout = ConsoleOutput(self.log_dock.logTextWidget)
        sys.stderr = ConsoleOutput(self.log_dock.logTextWidget)
        # 将日志输出到自定义输出类
        textEditLogger = QTextEditLogger(self.log_dock.logTextWidget)
    
    def __build_menu(self):
        # 创建菜单栏
        self.menuBar = self.menuBar()

        # 创建菜单
        self.fileMenu = QMenu("文件", self)
        self.viewMenu = QMenu("视图", self)
        self.helpMenu = QMenu("帮助", self)

        # fileMenu动作
        self.newProjectAction = QAction("新建工程", self)
        self.newProjectAction.setIcon(QIcon(os.path.join(ICON_DIR, 'folder-plus.svg')))
        self.newProjectAction.triggered.connect(self.__new_project)
        self.openProjectAction = QAction("打开工程", self)
        self.openProjectAction.setIcon(QIcon(os.path.join(ICON_DIR, 'folder-search.svg')))
        self.openProjectAction.triggered.connect(lambda: self.loadProjectSignal.emit('load_project'))
        self.exitAction = QAction("退出", self)
        self.exitAction.setIcon(QIcon(os.path.join(ICON_DIR, 'window-close.svg')))
        self.exitAction.triggered.connect(self.close)  # 连接退出动作到窗口的关闭功能

        self.fileMenu.addAction(self.newProjectAction)
        self.fileMenu.addAction(self.openProjectAction)
        self.fileMenu.addSeparator()  # 分隔符
        self.fileMenu.addAction(self.exitAction)
        
        # viewMenu 动作
        self.actionDockAction = QAction(QIcon(os.path.join(ICON_DIR, 'view-dashboard-variant.svg')), "自动化测试关键字窗口", self)
        self.actionDockAction.triggered.connect(self.__viewMenu_clicked)
        self.editDockAction = QAction(QIcon(os.path.join(ICON_DIR, 'view-dashboard-variant.svg')), "自动化测试编辑窗口", self)
        self.editDockAction.triggered.connect(self.__viewMenu_clicked)
        self.projectDockAction = QAction(QIcon(os.path.join(ICON_DIR, 'view-dashboard-variant.svg')), "自动化测试项目窗口", self)
        self.projectDockAction.triggered.connect(self.__viewMenu_clicked)
        self.logDockAction = QAction("自动化测试日志窗口", self)
        self.logDockAction.triggered.connect(self.__viewMenu_clicked)

        self.viewMenu.addAction(self.actionDockAction)
        self.viewMenu.addSeparator()  # 分隔符
        self.viewMenu.addAction(self.editDockAction)
        self.viewMenu.addSeparator()  # 分隔符
        self.viewMenu.addAction(self.projectDockAction)
        self.viewMenu.addSeparator()  # 分隔符
        self.viewMenu.addAction(self.logDockAction)

        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.viewMenu)
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

    
    def __connect_signals(self): # QwQ: sender.signal.connect(receiver.func)
        """ 信号连接 """
        self.loadProjectSignal.connect(lambda: self.project_dock.load_project(self.project_dock.select_project()))
        self.action_dock.closeSignal.connect(lambda: self.actionDockAction.setIcon(QIcon()))
        self.action_dock.itemDoubleClickedSignal.connect(self.edit_dock.tree.display_action_details)
        self.project_dock.closeSignal.connect(lambda: self.projectDockAction.setIcon(QIcon()))
        self.project_dock.operateResponseSignal.connect(self.edit_dock.operate)
        self.project_dock.tree.itemDoubleClickedSignal.connect(self.edit_dock.tree.display_module_details)
        self.edit_dock.closeSignal.connect(lambda: self.editDockAction.setIcon(QIcon()))
        self.edit_dock.operateSignal.connect(lambda: self.log_dock.setVisible(True))
        self.edit_dock.operateSignal.connect(self.project_dock.get_checked_modules)
        self.log_dock.closeSignal.connect(lambda: self.logDockAction.setIcon(QIcon()))
    
    def __new_project(self):
        """ 创建新工程目录，菜单操作"""
        nameInputDialogBox = NameInputDialogBox(self, '新建工程', '请输入新工程的名称：')
        if nameInputDialogBox.exec():
            projectName = nameInputDialogBox.nameInput() # 要创建的顶级目录名称
            projectPath = os.path.join(PROJECTS_DIR, projectName)
            try:
                # 创建完整的目录结构
                os.makedirs(f"{projectPath}/business")
                os.makedirs(f"{projectPath}/config")
                os.makedirs(f"{projectPath}/data")
                os.makedirs(f"{projectPath}/log")
                LOG.success(f'Project {projectName} create successfully')
            except Exception as err:
                LOG.debug(f'Exception: {err}')
    
    @typing.override
    def closeEvent(self, event):
        # 恢复标准输出和标准错误，保持良好的编程习惯Qwq。
        # 程序结束时，操作系统会自动释放所有资源，包括标准输出和标准错误的重定向。
        # 因此，这种重定向不会影响其他正在运行的程序，也不会影响外部的终端或控制台。
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        super().closeEvent(event)
    
    @Slot(bool)
    def __viewMenu_clicked(self, checked: bool):
        """ 视图菜单下子项的单击事件 """
        sender: QAction = self.sender()  # 获取信号发送者
        actionText = sender.text()
        dock = None
        if actionText == '自动化测试关键字窗口':
            dock = self.action_dock
        elif actionText == '自动化测试编辑窗口': 
            dock = self.edit_dock
        elif actionText == '自动化测试项目窗口': 
            dock = self.project_dock
        elif actionText == '自动化测试日志窗口': 
            dock = self.log_dock
        else:
            return
        # 判断菜单项的勾选状态
        if sender.icon().isNull():
            dock.setVisible(True)
            sender.setIcon(QIcon(os.path.join(ICON_DIR, 'view-dashboard-variant.svg')))
        else:
            dock.setVisible(False)
            sender.setIcon(QIcon())
    


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
