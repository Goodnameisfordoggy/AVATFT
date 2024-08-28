'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-08-29 00:26:31
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
from PySide6.QtCore import Qt

from dockWidget_edit import EditDock
from dockWidget_action import ActionDock 
from dockWidget_log import LogDock
from dockWidget_project import ProjectDock

class MainWindow(QMainWindow):
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

        self.initUI()
        self.connect_signal()

    def initUI(self):
        self.build_menu()
        self.create_dock_widgets()
        self.initialize_layout()

    def build_menu(self):
        # 创建菜单栏
        menuBar = self.menuBar()

        # 创建菜单
        fileMenu = QMenu("文件", self)
        viewMenu = QMenu("视图", self)
        helpMenu = QMenu("帮助", self)

        # fileMenu动作
        newAction = QAction("新建", self)
        openAction = QAction("打开", self)
        saveAction = QAction("保存", self)
        exitAction = QAction("退出", self)
        exitAction.triggered.connect(self.close)  # 连接退出动作到窗口的关闭功能

        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()  # 分隔符
        fileMenu.addAction(exitAction)

        menuBar.addMenu(fileMenu)
        menuBar.addMenu(viewMenu)
        menuBar.addMenu(helpMenu)

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

    
    def initialize_layout(self):
        
        # 分割 Horizontal Vertical
        self.splitDockWidget(self.action_dock, self.edit_dock, Qt.Horizontal)
        self.splitDockWidget(self.edit_dock, self.project_dock, Qt.Horizontal)

    def connect_signal(self): # QwQ: sender.signal.connect(receiver.func)
        self.action_dock.item_double_clicked_signal.connect(self.edit_dock.display_action_details)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
