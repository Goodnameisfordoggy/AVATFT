'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-04 21:50:47
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\views\dialogBox\input.py
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
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit


class NameInputDialogBox(QDialog):
    def __init__(self, parent, title: str = 'nameInput', text: str = 'text'):
        super().__init__()
        self.setWindowTitle(title)
        self.label = QLabel(text)
        self.lineEdit = QLineEdit()
        self.okButton = QPushButton("确定")
        self.cancelButton = QPushButton("取消")
        # 样式

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(QLabel(''))
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.lineEdit)
        mainLayout.addLayout(buttonLayout)
    
    def nameInput(self):
        return self.lineEdit.text()
    
    def set_default_name(self, text: str):
        self.lineEdit.setText(text)
    
