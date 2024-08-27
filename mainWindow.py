'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-08-27 14:34:41
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\mainWindow.py
Description: 

				*		д��¥��д�ּ䣬д�ּ������Ա��
				*		������Աд�������ó��򻻾�Ǯ��
				*		����ֻ���������������������ߣ�
				*		��������ո��գ����������긴�ꡣ
				*		��Ը�������Լ䣬��Ը�Ϲ��ϰ�ǰ��
				*		���۱������Ȥ���������г���Ա��
				*		����Ц��߯��񲣬��Ц�Լ���̫����
				*		��������Ư���ã��ĸ���ó���Ա��    
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
        self.setWindowTitle("���ӻ��Զ����Կ�ܹ���")

        # ��ȡ����Ļ�Ĵ�С
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.screen_width = screen_size.width()
        self.screen_height = screen_size.height()
        self.resize(self.screen_width - 100, self.screen_height - 100)
        # self.maximumSize()

        self.initUI()

    def initUI(self):
        self.build_menu()
        self.create_dock_widgets()
        self.initialize_layout()

    def build_menu(self):
        # �����˵���
        menuBar = self.menuBar()

        # �����˵�
        fileMenu = QMenu("�ļ�", self)
        viewMenu = QMenu("��ͼ", self)
        helpMenu = QMenu("����", self)

        # fileMenu����
        newAction = QAction("�½�", self)
        openAction = QAction("��", self)
        saveAction = QAction("����", self)
        exitAction = QAction("�˳�", self)
        exitAction.triggered.connect(self.close)  # �����˳����������ڵĹرչ���

        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()  # �ָ���
        fileMenu.addAction(exitAction)

        menuBar.addMenu(fileMenu)
        menuBar.addMenu(viewMenu)
        menuBar.addMenu(helpMenu)

    def create_dock_widgets(self):
        # �ؼ�������
        self.action_dock = ActionDock('', self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.action_dock)

        # ���ڱ༭��������
        self.edit_dock = EditDock('', self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.edit_dock)

        # ��������
        self.project_dock = ProjectDock('', self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.project_dock)

        # ��־����
        self.log_dock = LogDock('', self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.log_dock)

    
    def initialize_layout(self):
        pass
        # # �ָ� Horizontal Vertical
        # self.splitDockWidget(self.action_dock, self.edit_dock, Qt.Horizontal)
        # self.splitDockWidget(self.edit_dock, self.project_dock, Qt.Horizontal)
        # self.splitDockWidget(self.edit_dock, self.log_dock, Qt.Vertical)
        # # # ���ùؼ�����������ڱ༭��������ķָ����
        # self.action_dock.setMinimumSize(10, 10)
        # self.edit_dock.setMinimumSize(10, 10)
        # self.action_dock.setMinimumSize(10, 10)
        # self.log_dock.setMinimumSize(10, 10)

        # # ʹ�� QTimer �ڴ�����ʾ������ָ����
        # from PySide6.QtCore import QTimer
        # QTimer.singleShot(0, self.adjust_dock_sizes)

    # def adjust_dock_sizes(self):
    #     # ������� findChild �ҵ�����һ�� QSplitter����������С
    #     for splitter in self.findChildren(QSplitter):
    #         print(1)
    #         splitter.setSizes([100, 500])  # ��������Ҫ�ı���


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
