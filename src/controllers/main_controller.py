import os
import sys
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Signal, Slot

from src.views import Main_Window
from src.modules import load_file_content, save_file_content
from src.views import ReconfirmDialogBox
from src.modules.logger import LOG
from src import ICON_DIR, CONFIG_DIR

class MainController:
    def __init__(self, main_window: Main_Window):
        self.main_window = main_window
        self.__init_connections()
        self.__connect_signals()

    def __init_connections(self):
        self.main_window.actionDockAction.triggered.connect(self.__viewMenu_clicked)
        self.main_window.editDockAction.triggered.connect(self.__viewMenu_clicked)
        self.main_window.projectDockAction.triggered.connect(self.__viewMenu_clicked)
        self.main_window.logDockAction.triggered.connect(self.__viewMenu_clicked)
        self.main_window.zh_CN_Action.triggered.connect(self.__switch_language)
        self.main_window.en_US_Action.triggered.connect(self.__switch_language)

    def __connect_signals(self): # QwQ: sender.signal.connect(receiver.func)
        """ 信号连接 """
        self.main_window.newProjectSignal.connect(self.main_window.project_dock.new_project)
        self.main_window.loadProjectSignal.connect(lambda: self.main_window.project_dock.load_project(self.main_window.project_dock.select_project()))
        self.main_window.action_dock.closeSignal.connect(lambda: self.main_window.actionDockAction.setIcon(QIcon()))
        self.main_window.action_dock.itemDoubleClickedSignal.connect(self.main_window.edit_dock.display_action_details)
        self.main_window.project_dock.closeSignal.connect(lambda: self.main_window.projectDockAction.setIcon(QIcon()))
        self.main_window.project_dock.operateResponseSignal.connect(self.main_window.edit_dock.operate)
        self.main_window.project_dock.itemDoubleClickedSignal.connect(self.main_window.edit_dock.display_module_details)
        self.main_window.project_dock.loadProjectSignal.connect(lambda: self.main_window.project_dock.load_project(self.main_window.project_dock.select_project()))
        self.main_window.edit_dock.closeSignal.connect(lambda: self.main_window.editDockAction.setIcon(QIcon()))
        self.main_window.edit_dock.operateSignal.connect(lambda: self.main_window.log_dock.setVisible(True))
        self.main_window.edit_dock.operateSignal.connect(self.main_window.project_dock.get_checked_modules)
        self.main_window.edit_dock.isLockEditDockCheckBoxSignal.connect(lambda is_lock: self.main_window.edit_dock.ui.check_box.setEnabled(not is_lock))
        self.main_window.edit_dock.isLockEditDockCheckBoxSignal.connect(lambda is_lock: self.main_window.edit_dock.ui.check_box2.setEnabled(not is_lock))
        self.main_window.log_dock.closeSignal.connect(lambda: self.main_window.logDockAction.setIcon(QIcon()))

    def __viewMenu_clicked(self):
        """ 视图菜单下子项的单击事件 """
        print(self.main_window)
        sender: QAction = self.main_window.sender()  # 获取信号发送者
        print(sender)
        actionText = sender.text()
        dock = None
        if actionText == self.tr('自动化测试关键字窗口', 'view_keyword_window'):
            dock = self.main_window.action_dock
        elif actionText == self.tr('自动化测试编辑窗口', 'view_edit_window'): 
            dock = self.main_window.edit_dock
        elif actionText == self.tr('自动化测试项目窗口', 'view_project_window'): 
            dock = self.main_window.project_dock
        elif actionText == self.tr('自动化测试日志窗口', 'view_log_window'): 
            dock = self.main_window.log_dock
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
        sender: QAction = self.main_window.sender()  # 获取信号发送者
        language = sender.text()
        workspace_settings = load_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), LOG, translater=True)
        history_user_language = workspace_settings['settings']['user_language']
        if language != history_user_language: # 语言发生变化时才进行保存
            workspace_settings['settings']['user_language'] = language
            save_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), workspace_settings, LOG, translater=True)
            if ReconfirmDialogBox(self.main_window, self.tr("切换语言设置", "dialog_title"), self.tr("需要重启以启用新设置", "dialog_text"), self.tr("立即重启", "dialog_ok"), self.tr("稍后重启", "dialog_cancel")).exec():
                os.execl(sys.executable, *([sys.executable] + sys.argv))