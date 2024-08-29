'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-08-29 22:27:26
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\dockWidget_edit.py
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
import yaml
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QDockWidget, QVBoxLayout, QWidget, QLineEdit, QTreeWidget,
    QTreeWidgetItem
    )
from PySide6.QtGui import QScreen
from PySide6.QtCore import Qt

class EditDock(QDockWidget):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __init__(self, title='', parent=None):
        super().__init__(title, parent)
        
        # QDockWidget.NoDockWidgetFeatures        禁用所有特性，停靠窗口将不能移动、浮动或关闭。
        # QDockWidget.DockWidgetMovable           允许停靠窗口在主窗口中移动（拖动）。
        # QDockWidget.DockWidgetFloatable         允许停靠窗口浮动到主窗口之外成为独立窗口。
        # QDockWidget.DockWidgetClosable          允许用户关闭停靠窗口。
        # QDockWidget.DockWidgetVerticalTitleBar  显示垂直标题栏，这个特性仅在某些平台和样式中有效。
        # QDockWidget.DockWidgetAutoHide          允许停靠窗口自动隐藏。当用户将鼠标移到窗口边缘时，停靠窗口将会自动显示出来，移开鼠标时将会自动隐藏。
        # QDockWidget.DockWidgetFloatable         允许停靠窗口浮动，使其可以脱离主窗口作为独立的浮动窗口显示。
        # QDockWidget.DockWidgetMovable           允许停靠窗口在主窗口中进行移动。
        self.setFeatures(QDockWidget.NoDockWidgetFeatures | QDockWidget.DockWidgetClosable)
        self.setTitleBarWidget(QLabel('   测试用例编辑区'))
        self.initUI()
        
    
    def initUI(self):
        self.center_widget = QWidget(self)
        self.setWidget(self.center_widget)
        center_widget_layout = QVBoxLayout(self.center_widget)
        
        # 搜索框
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("请输入搜索项，按Enter搜索")
        # self.search_box.textChanged.connect()
        center_widget_layout.addWidget(self.search_box)

        # 树状控件
        self.tree = QTreeWidget()
        center_widget_layout.addWidget(self.tree)
        self.tree.setColumnCount(3) # 列数
        self.tree.setHeaderLabels(['参数描述', '参数名称', '参数值'])
        
    
    def display_action_details(self, action_path:str):
        """ 
        展示action的详细信息 
        
        action_path: 由信号携带
        """
        # 清空树控件
        self.tree.clear()
        # 读取 YAML 文件
        with open(action_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        # 创建action子项
        actionItem = QTreeWidgetItem(self.tree, [config[0]['describe']]) # 配置文件(yaml)有列表结构
        actionItem.setFirstColumnSpanned(True)  # 合并三列
        try:
            parameterItemsText = [[config[0]['params_describe'][key], key, value] for key, value in config[0]['params'].items()]
        except KeyError:
            print(f'文件参数缺失：{action_path}')
            return
            
        for parameterItemText in parameterItemsText:
            parameterItem = QTreeWidgetItem(actionItem, parameterItemText)

        # 展开子项
        actionItem.setExpanded(True)
        # 自动调整所有列的宽度
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)
        self.tree.resizeColumnToContents(2)
    
    def display_module_details(self, module_path:str):
        print('display_module_details')
        pass

if __name__ == '__main__':
    app = QApplication([])
    window = EditDock()
    window.show()
    app.exec()