'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-09-11 01:25:45
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\src\dialogBox\reconfirm.py
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
import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PySide6.QtCore import Qt

class ReconfirmDialogBox(QDialog):
    def __init__(self, parent, title: str = 'reconfirm', text: str = 'text'):
        super().__init__()
        self.setWindowTitle(title)
        self.setStyleSheet("QDialog { min-width: 200px; max-width: 200px; min-height: 100px; max-height: 100px; }")
        self.label = QLabel(text)
        self.okButton = QPushButton("确定")
        self.cancelButton = QPushButton("取消")
        # 样式
        self.label.setAlignment(Qt.AlignCenter)
        self.okButton.setStyleSheet("QPushButton { min-width: 35px; max-width: 35px; min-height: 20px; max-width: 20px; }")
        self.cancelButton.setStyleSheet("QPushButton { min-width: 35px; max-width: 35px; min-height: 20px; max-width: 20px; }")

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(QLabel(''))
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.label)
        mainLayout.addLayout(buttonLayout)
        
if __name__ == '__main__':
    # Application setup
    app = QApplication(sys.argv)
    dialog = ReconfirmDialogBox('text')
    
    # Show the dialog and wait for it to close
    if dialog.exec():
        print("Password:", dialog.lineEdit.text())
    else:
        print("Operation cancelled.")
    sys.exit(app.exec())