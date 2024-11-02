import os
import sys
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QObject


from src.modules import load_file_content, save_file_content
from src.views import ReconfirmDialogBox
from src.modules.logger import get_global_logger
LOG = get_global_logger()
from src import ICON_DIR, CONFIG_DIR

class MainController(QObject):
    
    def __init__(self, main_window):
        from src.views import Main_Window
        self.view: Main_Window = main_window
        self.__init_connections()
        # MainController 初始化是将所有子 controller 一同初始化；前提条件，MainWindow(view) 初始化时也将所有子 view 初始化
        from src.controllers import (
            ActionController, 
            ProjectController, 
            EditController, 
            LogController
        )
        self.actionController = ActionController(self.view.action_dock)
        self.projectController = ProjectController(self.view.project_dock)
        self.editController = EditController(self.view.edit_dock)
        self.logController = LogController(self.view.log_dock)
        self.__connect_custom_signals()

    def __init_connections(self):
        """ 连接内置事件信号与槽函数 """
        self.view.newProjectAction.triggered.connect(lambda: self.view.project_dock.newProjectSignal.emit("MainController:new project"))
        self.view.openProjectAction.triggered.connect(lambda: self.view.project_dock.loadProjectSignal.emit('MainController:load project'))
        self.view.actionDockAction.triggered.connect(self.__viewMenu_clicked)
        self.view.editDockAction.triggered.connect(self.__viewMenu_clicked)
        self.view.projectDockAction.triggered.connect(self.__viewMenu_clicked)
        self.view.logDockAction.triggered.connect(self.__viewMenu_clicked)
        self.view.zh_CN_Action.triggered.connect(self.__switch_language)
        self.view.en_US_Action.triggered.connect(self.__switch_language)
        

    def __connect_custom_signals(self): # QwQ: sender.signal.connect(receiver.func)
        """连接自定义信号与槽函数"""
        self.view.action_dock.closeSignal.connect(lambda: self.view.actionDockAction.setIcon(QIcon()))
        self.view.action_dock.itemDoubleClickedSignal.connect(lambda action_path: self.view.edit_dock.displayActionDetailsSignal.emit(action_path))
        self.view.project_dock.closeSignal.connect(lambda: self.view.projectDockAction.setIcon(QIcon()))
        # self.view.project_dock.operateResponseSignal.connect(self.view.edit_dock.operate)
        self.view.project_dock.itemDoubleClickedSignal.connect(lambda module_path: self.view.edit_dock.displayModuleDetailsSignal.emit(module_path))
        self.view.project_dock.loadProjectSignal.connect(lambda: self.view.project_dock.load_project(self.view.project_dock.select_project()))
        self.view.edit_dock.closeSignal.connect(lambda: self.view.editDockAction.setIcon(QIcon()))
        self.view.edit_dock.operateSignal.connect(lambda: self.view.log_dock.setVisible(True))
        # self.view.edit_dock.operateSignal.connect(self.view.project_dock.get_checked_modules)
        self.view.edit_dock.isLockEditDockCheckBoxSignal.connect(lambda is_lock: self.view.edit_dock.check_box.setEnabled(not is_lock))
        self.view.edit_dock.isLockEditDockCheckBoxSignal.connect(lambda is_lock: self.view.edit_dock.check_box2.setEnabled(not is_lock))
        self.view.log_dock.closeSignal.connect(lambda: self.view.logDockAction.setIcon(QIcon()))

    def init_APP(self):
        self.view.project_dock.loadHistoryProjectSiganl.emit()
        self.view.action_dock.updateChildrenItemSignal.emit()

    def __viewMenu_clicked(self):
        """ 视图菜单下子项的单击事件 """
        sender: QAction = self.view.sender()  # 获取信号发送者
        actionText = sender.text()
        dock = None
        if actionText == self.tr('自动化测试关键字窗口', 'view_keyword_window'):
            dock = self.view.action_dock
        elif actionText == self.tr('自动化测试编辑窗口', 'view_edit_window'): 
            dock = self.view.edit_dock
        elif actionText == self.tr('自动化测试项目窗口', 'view_project_window'): 
            dock = self.view.project_dock
        elif actionText == self.tr('自动化测试日志窗口', 'view_log_window'): 
            dock = self.view.log_dock
        else:
            return
        # 判断菜单项的勾选状态
        if sender.icon().isNull():
            dock.setVisible(True)
            sender.setIcon(QIcon(os.path.join(ICON_DIR, 'view-dashboard-variant.svg')))
        else:
            dock.setVisible(False)
            sender.setIcon(QIcon())
    
    def __switch_language(self):
        """ 切换语言设置，菜单操作"""
        sender: QAction = self.view.sender()  # 获取信号发送者
        language = sender.text()
        workspace_settings = load_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), LOG, translater=True)
        history_user_language = workspace_settings['settings']['user_language']
        if language != history_user_language: # 语言发生变化时才进行保存
            workspace_settings['settings']['user_language'] = language
            save_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), workspace_settings, LOG, translater=True)
            if ReconfirmDialogBox(self.view, self.tr("切换语言设置", "dialog_title"), self.tr("需要重启以启用新设置", "dialog_text"), self.tr("立即重启", "dialog_ok"), self.tr("稍后重启", "dialog_cancel")).exec():
                os.execl(sys.executable, *([sys.executable] + sys.argv))