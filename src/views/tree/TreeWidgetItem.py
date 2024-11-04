'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-04 09:31:23
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\views\tree\treeWidgetItem.py
Description: 

    TreeWidgetItem: 项目中通用的树控件子项的封装
    ActionItem, ModuleItem: 特化的子项

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
import typing
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QIcon

from src.modules.logger import get_global_logger
LOG = get_global_logger()
from src import ICON_DIR


class TreeWidgetItem(QTreeWidgetItem, QObject):
    """
    Data(tuple):
        0----type
        1----path
        2----draggable
        3----acceptDrops
    """
    def __init__(self, parent, text: list, data: tuple = (None, None, None, None), icon_path: str = '', editable: bool = False, checkbox: bool = False, *args, **kwargs):
        super().__init__(parent, text, *args, **kwargs)
        self.__data = data
        # 添加数据
        if self.__data:
            for i in range(len(self.__data)):
                if self.__data[i]:
                    self.setData(i, Qt.UserRole, self.__data[i])
        self.setFirstColumnSpanned
        # 添加图标
        if icon_path:
            icon = QIcon(icon_path)
            self.setIcon(0, icon)  # 在第一列添加图标
        else:
            if self.type == 'action':
                self.setIcon(0, QIcon(os.path.join(ICON_DIR, 'sitemap.png')))
            elif self.type == 'Project:module':
                self.setIcon(0, QIcon(os.path.join(ICON_DIR, 'file-yaml.svg')))
            elif self.type == 'package':
                self.setIcon(0, QIcon(os.path.join(ICON_DIR, 'package-variant.svg')))
            elif self.type == 'Project:package':
                self.setIcon(0, QIcon(os.path.join(ICON_DIR, 'folder-open.svg')))
            elif self.type == 'Project:project':
                self.setIcon(0, QIcon(os.path.join(ICON_DIR, 'layers.svg')))
        
        
        # 只设置整个 item 可编辑，这会影响到所有列
        if editable:
            self.setFlags(self.flags() | Qt.ItemIsEditable)

        # 设置复选框
        if checkbox:
            self.setCheckState(0, Qt.Unchecked)
    
    @property
    def type(self):
        return self.data(0, Qt.UserRole)
    @type.setter
    def type(self, value):
        self.setData(0, Qt.UserRole, value)
    
    @property
    def path(self):
        return self.data(1, Qt.UserRole)
    @path.setter
    def path(self, value):
        self.setData(1, Qt.UserRole, value)

    @property
    def draggable(self):
        return self.data(2, Qt.UserRole)
    @draggable.setter
    def draggable(self, value):
        self.setData(2, Qt.UserRole, value)
    
    @property
    def acceptDrops(self):
        return self.data(3, Qt.UserRole)
    @acceptDrops.setter
    def acceptDrops(self, value):
        self.setData(3, Qt.UserRole, value)

    def change_UserData(self, column: int, value: any, role=Qt.UserRole):
        """
        修改用户数据
        :param column: 列索引
        :param value: 要设置的数据
        :param role: 数据的角色，默认是 Qt.UserRole
        """
        self.setData(column, role, value)

    @typing.override
    def clone(self):
        """
        克隆当前的 TreeWidgetItem，包括文本、数据、图标等
        """
        # 创建一个新的 TreeWidgetItem 实例，传入相同的参数
        cloned_item = TreeWidgetItem(
            parent=None,  # clone 不应该有父项
            text=[self.text(i) for i in range(self.columnCount())], 
            data=self.__data,
            icon_path='',  # icon 处理可以稍后进行
            editable=self.flags() & Qt.ItemIsEditable, # 是否可编辑
            checkbox=self.flags() & Qt.ItemIsUserCheckable # 设置复选框
        )
        
        # 如果有图标，需要手动复制
        if not self.icon(0).isNull():
            cloned_item.setIcon(0, self.icon(0))
        
        return cloned_item