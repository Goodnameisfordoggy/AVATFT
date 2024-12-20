'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-04 21:59:21
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\AVATFT.py
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
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication

from src.modules import load_file_content
from src.views import Main_Window
from src.controllers import MainController
from static.css.stylesheet import STYLE_SHEET
from src import CONFIG_DIR, TRANSLATIONS_DIR, ICON_DIR
from src.modules.logger import get_global_logger
LOG = get_global_logger()

class AVATFT:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)  # 将 QApplication 实例作为成员变量
        
        self.app.setWindowIcon(QIcon(os.path.join(ICON_DIR, 'app.svg')))
        if STYLE_SHEET:
            self.app.setStyleSheet(STYLE_SHEET)

        # 创建 QTranslator 实例
        self.translator = QTranslator()

        # 加载编译后的翻译文件
        workspace_settings = load_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), LOG, translater=True)
        qm_file = os.path.join(TRANSLATIONS_DIR, f'{workspace_settings['settings']['user_language'] or workspace_settings['settings']['default_language']}.qm')
        if os.path.exists(qm_file):
            if self.translator.load(qm_file):
                self.app.installTranslator(self.translator)

        # 重定向标准输出和标准错误到自定义输出类
        # sys.stdout = ConsoleOutput(self.log_dock.ui.logTextWidget)
        # sys.stderr = ConsoleOutput(self.log_dock.ui.logTextWidget)
        # # 将日志输出到自定义输出类
        # textEditLogger = QTextEditLogger(self.log_dock.ui.logTextWidget)
        
        self.main_window = Main_Window(self.app)
        main_controller = MainController(self.main_window)
        self.main_window.show()
        main_controller.init_APP()
        self.app.exec()
        

