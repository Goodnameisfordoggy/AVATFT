'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-09-04 23:19:14
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\main.py
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
from PySide6.QtWidgets import QApplication
from src.mainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow(app)
    window.show()
    app.exec()
