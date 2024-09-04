'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-09-02 08:55:49
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\mainWindow.py
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
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QDockWidget, QMenuBar, QMenu, QSplitter
from PySide6.QtGui import QScreen, QAction
from PySide6.QtCore import Qt, Signal

from dockWidget_edit import EditDock
from dockWidget_action import ActionDock 
from dockWidget_log import LogDock
from dockWidget_project import ProjectDock

class MainWindow(QMainWindow):
    
    # 自定义信号
    new_project_signal = Signal(str)
    load_project_signal = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("可视化自动测试框架工具")

        # 获取主屏幕的大小
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.screen_width = screen_size.width()
        self.screen_height = screen_size.height()
        self.resize(self.screen_width - 100, self.screen_height - 100)
        # self.maximumSize()        

        self.build_menu()
        self.create_dock_widgets()
        self.initialize_layout()
        self.connect_signal()

    def build_menu(self):
        # 创建菜单栏
        self.menuBar = self.menuBar()

        # 创建菜单
        self.fileMenu = QMenu("文件", self)
        self.viewMenu = QMenu("视图", self)
        self.helpMenu = QMenu("帮助", self)

        # fileMenu动作
        self.newAction = QAction("新建工程", self)
        # self.newAction.triggered.connect(self.project_dock.)
        self.openAction = QAction("打开工程", self)
        self.openAction.triggered.connect(lambda: self.load_project_signal.emit('load_project'))
        # self.saveAction = QAction("保存", self)
        self.exitAction = QAction("退出", self)
        self.exitAction.triggered.connect(self.close)  # 连接退出动作到窗口的关闭功能

        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.openAction)
        # self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addSeparator()  # 分隔符
        self.fileMenu.addAction(self.exitAction)
        
        # viewMenu 动作
        self.actionDockAction = QAction("自动化测试关键字窗口", self)
        self.actionDockAction.setCheckable(True)  # 设置菜单项可勾选
        self.actionDockAction.setChecked(True) # 初始勾选
        self.actionDockAction.triggered.connect(self.viewMenu_clicked)
        self.editDockAction = QAction("自动化测试编辑窗口", self)
        self.editDockAction.setCheckable(True)
        self.editDockAction.setChecked(True)
        self.editDockAction.triggered.connect(self.viewMenu_clicked)
        self.projectDockAction = QAction("自动化测试项目窗口", self)
        self.projectDockAction.setCheckable(True)
        self.projectDockAction.setChecked(True)
        self.projectDockAction.triggered.connect(self.viewMenu_clicked)
        self.logDockAction = QAction("自动化测试日志窗口", self)
        self.logDockAction.setCheckable(True)
        self.logDockAction.triggered.connect(self.viewMenu_clicked)

        self.viewMenu.addAction(self.actionDockAction)
        self.viewMenu.addAction(self.editDockAction)
        self.viewMenu.addAction(self.projectDockAction)
        self.viewMenu.addAction(self.logDockAction)

        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.viewMenu)
        self.menuBar.addMenu(self.helpMenu)

    def create_dock_widgets(self):
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

    
    def initialize_layout(self):
        
        # 分割 Horizontal Vertical
        self.splitDockWidget(self.action_dock, self.edit_dock, Qt.Horizontal)
        self.splitDockWidget(self.edit_dock, self.project_dock, Qt.Horizontal)

    def connect_signal(self): # QwQ: sender.signal.connect(receiver.func)
        """ 信号连接 """
        self.action_dock.item_double_clicked_signal.connect(self.edit_dock.display_action_details)
        self.project_dock.item_double_clicked_signal.connect(self.edit_dock.display_module_details)
        self.load_project_signal.connect(self.project_dock.load_project)
        self.edit_dock.operate_signal.connect(lambda: self.log_dock.setVisible(True))

    def viewMenu_clicked(self, checked):
        """ 视图菜单下子项的单击事件 """
        sender = self.sender()  # 获取信号发送者
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
        if checked:
            dock.setVisible(True)
        else:
            dock.setVisible(False)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
