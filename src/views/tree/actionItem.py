'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-04 09:44:59
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\views\tree\actionItem.py
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
from PySide6.QtCore import Qt, QObject

from src.views.tree.TreeWidgetItem import TreeWidgetItem
from src.modules.logger import get_global_logger
LOG = get_global_logger()

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