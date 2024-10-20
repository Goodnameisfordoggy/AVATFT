'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-10-11 21:25:51
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\treeWidgetItem.py
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
import yaml
import typing
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QIcon

from src.utils.filter import identify_input_type
from src.utils.logger import get_logger
from src import BASE_DIR, ICON_DIR
LOG = get_logger()


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


class ActionItem(TreeWidgetItem, QObject):
    """ 在编辑区使用的行为关键字项 """
    def __init__(self, parent, text: list = [], data: tuple = (), icon_path: str = '', editable: bool = False, param_editable: bool = False):
        super().__init__(parent, text, data, icon_path, editable, checkbox=False)
        self.action_path = self.data(1, Qt.UserRole)
        self.param_editable = param_editable
        # 读取 YAML 文件
        try:
            with open(self.action_path, 'r', encoding='utf-8') as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError:
            LOG.critical(self.tr("请检查文件 {} 是否存在", "Log_msg").format(self.action_path))

        try:
            self.setText(0, self.config[0]['describe'])
        except KeyError as err:
            LOG.critical(self.tr("请检查文件 {} 中是否存在键：{}", "Log_msg").format(self.action_path, err))
        self.setFirstColumnSpanned(True)  # 合并所有列
        self.__create_childItem()

    def __create_childItem(self):
        # 创建子项
        try:
            parameterItemsText = [[str(self.config[0]['params_describe'][key]), str(key), str(value)] for key, value in self.config[0]['params'].items()]
        except KeyError as err:
            LOG.critical(self.tr("请检查文件 {} 中是否存在键：{}", "Log_msg").format(self.action_path, err))
            return
            
        for parameterItemText in parameterItemsText:
            if self.param_editable:
                parameterItem = TreeWidgetItem(self, parameterItemText, editable=True)
            else:
                parameterItem = TreeWidgetItem(self, parameterItemText)
            

class ModuleItem(TreeWidgetItem, QObject):
    """ 在编辑区使用的模块项 """
    def __init__(self, parent: QTreeWidget, text: list = [], data: tuple = (), icon_path: str = '', editable: bool = False):
        super().__init__(parent, text, data, icon_path, editable, checkbox=False)
        self.__parent = parent
        self.module_path = self.data(1, Qt.UserRole)
        # 读取 YAML 文件
        try: 
            with open(self.module_path, 'r', encoding='utf-8') as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError:
            LOG.critical(self.tr("请检查文件 {} 是否存在", "Log_msg").format(self.module_path))
        self.setFirstColumnSpanned(True)
        self.setText(0, os.path.splitext(os.path.basename(self.module_path))[0])
        self.__create_childItem()
        self.__parent.itemChanged.connect(self.__parent.on_item_changed) # 连接父组件（QTreeWidget）的子项编辑事件，该操作必须位于ModuleItem所有子项初始化之后，以防初始化时触发该事件
    
    def __del__(self):
        self.__parent.itemChanged.disconnect(self.__parent.on_item_changed) # 析构时取消连接

    def __create_childItem(self):
        try:
            # 固定的action子项
            rootAction1 = TreeWidgetItem(self, [self.tr("用例信息")])
            rootAction1.setFirstColumnSpanned(True)
            root1Child1 = TreeWidgetItem(rootAction1, [self.tr("测试用例描述"), 'describe', str(self.config['info']['describe'])], ('param', ), icon_path=os.path.join(ICON_DIR, 'information-slab-circle.svg'), editable=True)
            root1Child2 = TreeWidgetItem(rootAction1, [self.tr("测试用例编号"), 'id', str(self.config['info']['id'])], ('param', ), icon_path=os.path.join(ICON_DIR, 'information-slab-circle.svg'), editable=True)
            root1Child3 = TreeWidgetItem(rootAction1, [self.tr("测试用例标题"), 'title', str(self.config['info']['title'])], ('param', ), icon_path=os.path.join(ICON_DIR, 'information-slab-circle.svg'), editable=True)

            rootAction2 = TreeWidgetItem(self, [self.tr("运行设置")])
            rootAction2.setFirstColumnSpanned(True)
            root2Child1 = TreeWidgetItem(rootAction2, [self.tr("跳过此用例")], icon_path=os.path.join(ICON_DIR, 'cogs.svg'))
            root2Child1.setFirstColumnSpanned(True)
            child1Action1 = TreeWidgetItem(root2Child1, [self.tr("是否启用此配置"), 'flag', str(self.config['config'][0]['params']['flag'])], ('param', ), editable=True)
            child1Action2 = TreeWidgetItem(root2Child1, [self.tr("用例跳过原因"), 'reason', str(self.config['config'][0]['params']['reason'])], ('param', ), editable=True)
            root2Child2 = TreeWidgetItem(rootAction2, [self.tr("给用例打标签")], icon_path=os.path.join(ICON_DIR, 'cogs.svg'))
            root2Child2.setFirstColumnSpanned(True)
            child2Action1 = TreeWidgetItem(root2Child2, [self.tr("是否启用此配置"), 'flag', str(self.config['config'][1]['params']['flag'])], ('param', ), editable=True)
            child2Action2 = TreeWidgetItem(root2Child2, [self.tr("用例标签名称"), 'markname', str(self.config['config'][1]['params']['markname'])], ('param', ), editable=True)
            root2Child3 = TreeWidgetItem(rootAction2, [self.tr("使用前置后置")], icon_path=os.path.join(ICON_DIR, 'cogs.svg'))
            root2Child3.setFirstColumnSpanned(True)
            child3Action1 = TreeWidgetItem(root2Child3, [self.tr("是否启用此配置"), 'flag', str(self.config['config'][2]['params']['flag'])], ('param', ), editable=True)
            child3Action2 = TreeWidgetItem(root2Child3, [self.tr("前后置函数名称"), 'fixtures', str(self.config['config'][2]['params']['fixtures'])], ('param', ), editable=True)
            root2Child4 = TreeWidgetItem(rootAction2, [self.tr("数据驱动")], icon_path=os.path.join(ICON_DIR, 'cogs.svg'))
            root2Child4.setFirstColumnSpanned(True)
            child4Action1 = TreeWidgetItem(root2Child4, [self.tr("是否启用此配置"), 'flag', str(self.config['config'][3]['params']['flag'])], ('param', ), editable=True)
            child4Action2 = TreeWidgetItem(root2Child4, [self.tr("数据驱动文件名称"), 'filename', str(self.config['config'][3]['params']['filename'])], ('param', ), editable=True)
            child4Action3 = TreeWidgetItem(root2Child4, [self.tr("数据驱动文件Sheet"), 'sheetname', str(self.config['config'][3]['params']['sheetname'])], ('param', ), editable=True)
            
            rootAction3 = TreeWidgetItem(self, [self.tr("测试步骤")], (None,None,True,True))
            rootAction3.setFirstColumnSpanned(True)
            # 创建action子项
            if self.config['step']:
                for action in self.config['step']:
                    actionItem = TreeWidgetItem(rootAction3, [str(action['describe'])], ('action', os.path.join(BASE_DIR, action['action_RP']), False, True)) 
                    actionItem.setFirstColumnSpanned(True)  # 合并三列
                    parameterItemsText = [[str(action['params_describe'][key]), str(key), str(value)] for key, value in action['params'].items()]
                    for parameterItemText in parameterItemsText:
                        parameterItem = TreeWidgetItem(actionItem, parameterItemText, ('param', ), editable=True)
        except KeyError as err:
            LOG.critical(self.tr("请检查文件 {} 中是否存在键：{}", "Log_msg").format(self.module_path, err))
            return
        # 展开子项
        self.setExpanded(True)
        rootAction1.setExpanded(True)
        rootAction2.setExpanded(True)
        rootAction3.setExpanded(True)