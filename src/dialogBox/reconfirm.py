'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-10-13 00:52:58
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\dialogBox\reconfirm.py
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
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from src import ICON_DIR

class ReconfirmDialogBox(QDialog):
    def __init__(self, parent, title: str = 'reconfirm', text: str = 'text', ok_text: str = "确定", cancel_text: str = "取消"):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(ICON_DIR, 'app.svg')))
        self.label = QLabel(text)
        self.okButton = QPushButton(ok_text)
        self.cancelButton = QPushButton(cancel_text)
        # 样式
        self.label.setAlignment(Qt.AlignCenter)

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(QLabel(''))
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.label)
        mainLayout.addLayout(buttonLayout)
        