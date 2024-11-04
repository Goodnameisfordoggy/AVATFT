'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-04 09:31:07
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\views\tree\moduleItem.py
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
import yaml
from PySide6.QtWidgets import QTreeWidget
from PySide6.QtCore import Qt, QObject

from src.views.tree.TreeWidgetItem import TreeWidgetItem
from src.modules.logger import get_global_logger
LOG = get_global_logger()
from src import BASE_DIR, ICON_DIR

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