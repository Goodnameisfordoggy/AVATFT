'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-08-31 16:14:42
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\treeWidgetItem.py
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
import json
import yaml
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class TreeWidgetItem(QTreeWidgetItem):
    """
    Data(tuple):
        0----type
        1----path
        2----draggable
        3----AcceptDrops
    """
    def __init__(self, parent, text: list, data: tuple = (), icon_path: str = '', editable: bool = False):
        super().__init__(parent, text)
        self.__data = data
        # 添加数据
        if self.__data:
            for i in range(len(self.__data)):
                if self.__data[i]:
                    self.setData(i, Qt.UserRole, self.__data[i])
        # 添加图标
        icon = QIcon(icon_path)
        self.setIcon(0, icon)  # 在第一列添加图标
        
        # 只设置整个 item 可编辑，这会影响到所有列
        if editable:
            self.setFlags(self.flags() | Qt.ItemIsEditable)


class ActionItem(TreeWidgetItem):
    """ 在编辑区使用的行为关键字项 """
    def __init__(self, parent, text: list = [], data: tuple = (), icon_path: str = '', editable: bool = False):
        super().__init__(parent, text, data, icon_path, editable)
        self.action_path = self.data(1, Qt.UserRole)
        # 读取 YAML 文件
        with open(self.action_path, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)
        self.setFirstColumnSpanned(True)  # 合并所有列
        self.setText(0, self.config[0]['describe'])
        
        self.create_childItem()

    def create_childItem(self):
        # 创建子项
        try:
            parameterItemsText = [[self.config[0]['params_describe'][key], key, value] for key, value in self.config[0]['params'].items()]
        except KeyError as err:
            print(f'文件参数缺失：{err}--{self.action_path}')
            return
            
        for parameterItemText in parameterItemsText:
            parameterItem = TreeWidgetItem(self, parameterItemText)

class ModuleItem(TreeWidgetItem):
    """ 在编辑区使用的模块项 """
    def __init__(self, parent, text: list = [], data: tuple = (), icon_path: str = '', editable: bool = False):
        super().__init__(parent, text, data, icon_path, editable)
        self.parent = parent
        self.module_path = self.data(1, Qt.UserRole)
        # 读取 YAML 文件
        with open(self.module_path, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)
            print(json.dumps(self.config, indent=4, ensure_ascii=False))
        self.setFirstColumnSpanned(True)
        self.create_childItem()

    def create_childItem(self):
        # 固定的action子项
        rootAction1 = TreeWidgetItem(self, ['用例信息'])
        rootAction1.setFirstColumnSpanned(True)
        root1Child1 = TreeWidgetItem(rootAction1, ['测试用例描述', 'describe', str(self.config['info']['describe'])], ('param'), editable=True)
        root1Child2 = TreeWidgetItem(rootAction1, ['测试用例编号', 'id', str(self.config['info']['id'])], ('param'), editable=True)
        root1Child3 = TreeWidgetItem(rootAction1, ['测试用例标题', 'title', str(self.config['info']['title'])], ('param'), editable=True)

        rootAction2 = TreeWidgetItem(self, ['运行设置'])
        rootAction2.setFirstColumnSpanned(True)
        root2Child1 = TreeWidgetItem(rootAction2, [str(self.config['config'][0]['describe'])])
        child1Action1 = TreeWidgetItem(root2Child1, ['是否启用此配置', 'flag', str(self.config['config'][0]['params']['flag'])], ('param'), editable=True)
        child1Action2 = TreeWidgetItem(root2Child1, ['用例跳过原因', 'reason', str(self.config['config'][0]['params']['reason'])], ('param'), editable=True)
        root2Child2 = TreeWidgetItem(rootAction2, [str(self.config['config'][1]['describe'])])
        child2Action1 = TreeWidgetItem(root2Child2, ['是否启用此配置', 'flag', str(self.config['config'][1]['params']['flag'])], ('param'), editable=True)
        child2Action2 = TreeWidgetItem(root2Child2, ['用例标签名称', 'markname', str(self.config['config'][1]['params']['markname'])], ('param'), editable=True)
        root2Child3 = TreeWidgetItem(rootAction2, [str(self.config['config'][2]['describe'])])
        child3Action1 = TreeWidgetItem(root2Child3, ['是否启用此配置', 'flag', str(self.config['config'][2]['params']['flag'])], ('param'), editable=True)
        child3Action2 = TreeWidgetItem(root2Child3, ['前后置函数名称', 'fixtures', str(self.config['config'][2]['params']['fixtures'])], ('param'), editable=True)
        root2Child4 = TreeWidgetItem(rootAction2, [str(self.config['config'][3]['describe'])])
        child4Action1 = TreeWidgetItem(root2Child4, ['是否启用此配置', 'flag', str(self.config['config'][3]['params']['flag'])], ('param'), editable=True)
        child4Action2 = TreeWidgetItem(root2Child4, ['数据驱动文件名称', 'filename', str(self.config['config'][3]['params']['filename'])], ('param'), editable=True)
        child4Action3 = TreeWidgetItem(root2Child4, ['数据驱动文件Sheet', 'sheetname', str(self.config['config'][3]['params']['sheetname'])], ('param'), editable=True)
        
        rootAction3 = TreeWidgetItem(self, ['测试步骤'], (None,None,True,True))
        rootAction3.setFirstColumnSpanned(True)
        # 创建action子项
        for action in self.config['step']:
            actionItem = TreeWidgetItem(rootAction3, [action['describe']]) # 配置文件(yaml)有列表结构
            actionItem.setFirstColumnSpanned(True)  # 合并三列
            try:
                parameterItemsText = [[action['params_describe'][key], key, value] for key, value in action['params'].items()]
            except KeyError as err:
                print(f'文件缺失参数 {err}')
                return
                
            for parameterItemText in parameterItemsText:
                parameterItem = TreeWidgetItem(actionItem, parameterItemText, ('param'), editable=True)
        
        # 展开子项
        self.setExpanded(True)
        rootAction1.setExpanded(True)
        rootAction2.setExpanded(True)
        rootAction3.setExpanded(True)