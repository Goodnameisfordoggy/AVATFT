'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-11-04 22:43:16
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\controllers\edit_controller.py
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
import threading
from PySide6.QtWidgets import QTreeWidgetItem, QMenu
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QObject, QPoint, Slot

from src.modules import load_file_content, save_file_content
from src.views.tree import ActionItem, ModuleItem, TreeWidgetItem
from src.modules.funcs import *
from src import ICON_DIR, CONFIG_DIR
from src.modules.logger import get_global_logger
LOG = get_global_logger()

OPERATE_LOCK = threading.Lock()

class EditController(QObject):
    
    def __init__(self, edit_dock):
        # super().__init__()
        from src.views import EditDock
        self.view: EditDock = edit_dock
        self.__init_connections()
        self.__connect_custom_signals()

    def __init_connections(self):
        """连接内置事件信号与槽函数"""
        self.view.check_box.stateChanged.connect(self.__on_expand_all_checkbox_changed)
        self.view.check_box2.stateChanged.connect(self.__on_expand_step_checkbox_changed)
        self.view.search_box.textChanged.connect(lambda: self.__search_tree_items())
        self.view.search_combo_box.currentIndexChanged.connect(self.__switch_search_method)
        self.view.operation_btn.clicked.connect(self.operate)
        self.view.tree.customContextMenuRequested.connect(self.__show_context_menu)
        self.view.tree.itemChanged.connect(self.view.tree.on_item_changed)
        # 子项展开和收缩事件
        self.view.tree.itemExpanded.connect(self.__adjust_column_widths)
        self.view.tree.itemCollapsed.connect(self.__adjust_column_widths)
        

    def __connect_custom_signals(self):
        """连接自定义信号与槽函数"""
        self.view.displayActionDetailsSignal.connect(lambda action_path: self.__display_action_details(action_path))
        self.view.displayModuleDetailsSignal.connect(lambda module_path: self.__display_module_details(module_path))
        self.view.operateSignal.connect(lambda module_path_list: self.operate(module_path_list))
    
    @Slot(int)
    def __on_expand_all_checkbox_changed(self, state: int):
        """ 复选框状态变更绑定事件 """
        if state == 2:  # 复选框选中
            self.__set_all_items_expanded(self.view.tree.topLevelItem(0), True) # 展开所有项
            self.view.check_box.setIcon(QIcon(os.path.join(ICON_DIR, 'arrow-expand-vertical.svg')))
            self.view.check_box2.setChecked(True) # 状态关联
        else:
            self.__set_all_items_expanded(self.view.tree.topLevelItem(0).child(0), False)
            self.__set_all_items_expanded(self.view.tree.topLevelItem(0).child(1), False)
            self.__set_all_items_expanded(self.view.tree.topLevelItem(0).child(2), False)
            self.view.check_box.setIcon(QIcon(os.path.join(ICON_DIR, 'arrow-collapse-vertical.svg')))
            self.view.check_box2.setChecked(False) # 状态关联
    
    @Slot(int)
    def __on_expand_step_checkbox_changed(self, state: int):
        """ 复选框状态变更绑定事件 """
        item_step  = self.view.tree.topLevelItem(0).child(2)
        if state == 2:  # 复选框选中
            if item_step:
                self.__set_all_items_expanded(item_step, True)
            self.view.check_box2.setIcon(QIcon(os.path.join(ICON_DIR, 'arrow-expand-vertical.svg')))
            # try:
            #     self.view.tree.scrollToItem(self.current_item, QAbstractItemView.PositionAtTop)
            # except AttributeError:
            #     pass
        else:
            if item_step:
                # 只处理步骤项下子项的收缩
                for index in range(0, item_step.childCount()):
                    item_step.child(index).setExpanded(False)
                
            # self.current_item = self.view.tree.itemAt(0, 0)
            self.view.check_box2.setIcon(QIcon(os.path.join(ICON_DIR, 'arrow-collapse-vertical.svg')))
    
    @Slot()
    @Slot(int)
    def __search_tree_items(self, column: int = 0):
        """ 
        搜索树控件子项，搜索框绑定操作
        
        :param column: 搜索文本所在的列
        """
        search_text = self.view.search_box.text().lower() # 获取搜索框的文本，并转换为小写
        root = self.view.tree.invisibleRootItem() # 获取根项
        
        def filter_item(item: QTreeWidgetItem, column: int, search_text: str):
            """ 
            筛选符合条件的子项，遍历子项，递归搜索
            
            :param item: 根节点（项）
            """
            # 当前项处理
            item_text = item.text(column).lower()  # 获取项的文本，并转换为小写
            match = search_text in item_text  # 检查项的文本是否包含搜索内容
            if search_text == "":
                match = False
            item.setSelected(match)
            # 对所有子项进行同样的处理
            for j in range(item.childCount()):
                child_item = item.child(j)
                match = filter_item(child_item, column, search_text) or match # 如果任何一个子项匹配，那么其父项也应当被视为匹配
            
            # 根据是否匹配来设置当前项的选中状态，以及其父项的展折叠状态
            # item.setSelected(match)
            if match and item.parent():
                item.parent().setExpanded(True)
            return match
        filter_item(root, column, search_text)
    
    @Slot()
    def __switch_search_method(self):
        """ 切换查找方法，下拉列表绑定操作 """
        selected_text = self.view.search_combo_box.currentText()
        if selected_text == self.tr("匹配参数描述", "search_combo_box_item_Pdescribe"):
            self.view.search_box.textChanged.disconnect()
            self.view.search_box.textChanged.connect(lambda: self.__search_tree_items(0))
        elif selected_text == self.tr("匹配参数名称", "search_combo_box_item_Pname"):
            self.view.search_box.textChanged.disconnect()
            self.view.search_box.textChanged.connect(lambda: self.__search_tree_items(1))
        elif selected_text == self.tr("匹配参数值", "search_combo_box_item_Pvalue"):
            self.view.search_box.textChanged.disconnect()
            self.view.search_box.textChanged.connect(lambda: self.__search_tree_items(2))
    
    @Slot(list)  
    @Slot() # 也可处理不带参数的信号
    def operate(self, data: list | bool = False):
        """ 开始测试,按钮绑定操作 """
        if data is False or data is None: #  data: 按钮clicked信号触发时传递的信息
            self.view.operateRequestSignal.emit('request for module path list')
            return
        if isinstance(data, list): # data: operateResponseSignal信号触发时回带的信息
            if len(data) == 0:
                LOG.warning(self.tr("还未勾选要运行的测试用例！", "Log_msg"))
                return
            try:
                thread = threading.Thread(target=self.__operate_thread, args=(data,))
                thread.start()
            except Exception as e:
                LOG.debug(f"{e}")
    
    @Slot()
    def __adjust_column_widths(self):
        """ 调节数控件列的宽度 """
        for col in range(self.view.tree.columnCount()):
            self.view.tree.resizeColumnToContents(col)
    
    @Slot(str)
    def __display_action_details(self, action_path: str):
        """ 
        展示action的详细信息, 仅供预览 
        
        :param action_path: 由信号携带
        """
        self.view.tree.itemChanged.disconnect(self.view.tree.on_item_changed)

        # 清空树控件
        self.view.tree.clear()
        # 创建action子项
        actionItem = ActionItem(self.view.tree, data=('action', action_path)) # 配置文件(yaml)有列表结构
        # 展开子项
        actionItem.setExpanded(True)
        # 自动调整所有列的宽度
        self.view.tree.resizeColumnToContents(0)
        self.view.tree.resizeColumnToContents(1)
        self.view.tree.resizeColumnToContents(2)
        self.view.isLockEditDockCheckBoxSignal.emit(True) # 关闭交互

        self.view.tree.itemChanged.connect(self.view.tree.on_item_changed) 
    
    @Slot(str)
    def __display_module_details(self, module_path:str):
        """ 
        展示module的详细信息, 提供编辑交互UI 
        
        :param module_path: 由信号携带
        """
        self.view.tree.itemChanged.disconnect(self.view.tree.on_item_changed)

        # 清空树控件
        self.view.tree.clear()
        # 创建module子项
        moduleItem = ModuleItem(self.view.tree, data=('module', module_path))
        # 自动调整所有列的宽度
        self.view.tree.resizeColumnToContents(0)
        self.view.tree.resizeColumnToContents(1)
        self.view.tree.resizeColumnToContents(2)
        self.view.isLockEditDockCheckBoxSignal.emit(False) # 放开交互

        self.view.tree.itemChanged.connect(self.view.tree.on_item_changed) 
    
    @Slot()
    def __show_context_menu(self, pos: QPoint):
        """ 
        树控件子项右键菜单事件 
        
        :param pos: 事件位置
        """
        # 获取点击的项
        item = self.view.tree.itemAt(pos)
        if item:
            if item.type == 'action':
                # 创建上下文菜单
                context_menu = QMenu(self.view.tree)
                # 创建菜单项
                actionDelete = QAction(QIcon(os.path.join(ICON_DIR, 'trash-can-outline.svg')), self.tr("删除"), self.view.tree)
                actionMoveUp = QAction(QIcon(os.path.join(ICON_DIR, 'arrange-bring-forward.svg')), self.tr("上移"), self.view.tree)
                actionMoveDown = QAction(QIcon(os.path.join(ICON_DIR, 'arrange-send-backward.svg')), self.tr("下移"), self.view.tree)
                # 连接菜单项的触发信号
                actionDelete.triggered.connect(lambda: self.__delete_item(item))
                actionMoveUp.triggered.connect(lambda: self.__move_item_up(item))
                actionMoveDown.triggered.connect(lambda: self.__move_item_down(item))
                # 将菜单项添加到上下文菜单
                context_menu.addAction(actionDelete)
                context_menu.addAction(actionMoveUp)
                context_menu.addAction(actionMoveDown)
                # 显示上下文菜单
                context_menu.exec(self.view.tree.viewport().mapToGlobal(pos))
    
    def __add_action_to_module(self, action_file: str, module_file: str, step_index: int | None = None):
        """ 
        将action文件信息添加到module文件, 拖拽放置事件的文件处理操作
        
        :param step_index: 向module文件(step)中插入action的索引
        """
        start_index = action_file.find('action_keywords') # 查找起始位置
        action_RP = action_file[start_index:] # 提取相对路径
        action_content = load_file_content(action_file, logger=LOG, translater=True)
        module_content = load_file_content(module_file, logger=LOG, translater=True)
        action_content[0] = {'action_RP': action_RP} | action_content[0] #添加相对路径信息，'|' Operator (Python 3.9+)
        # 确保模块内容有 'step' 键
        if 'step' not in module_content:
            module_content['step'] = None
        # 向 module 文件( step 字段)中插入 action
        if module_content['step'] is None: # 不存在 action 时
            module_content['step'] = action_content
        else: # 存在 action 时
            if isinstance(step_index, int):
                module_content['step'].insert(step_index, action_content[0])
            else: # 默认插入到最后
                module_content['step'] = module_content['step'] + action_content
        # 将更新后的内容写回目标文件
        save_file_content(module_file, module_content, logger=LOG, translater=True)
        LOG.trace(f'Add action info to the "step" section of the {module_file}')
    
    def __delete_actionInfo(self, index: int):
        """ 从 module 文件(step)中删除 action 信息"""
        moduleItem = self.view.tree.topLevelItem(0)
        content = load_file_content(moduleItem.path, logger=LOG, translater=True)
        removed_action = content['step'].pop(index) # 根据子项索引在文件中删除对应位置上的信息
        save_file_content(moduleItem.path, content, logger=LOG, translater=True)
        LOG.trace(f'Action info at "step" index {index} delete successfully at {moduleItem.path}')

    def __move_actionInfo_to(self, move_index: int,  to_index: int):
        """ 向 module 文件(step)中特定索引插入 action 信息"""
        moduleItem = self.view.tree.topLevelItem(0)
        content = load_file_content(moduleItem.path, logger=LOG, translater=True)
        removed_action = content['step'].pop(move_index) # 根据子项索引在文件中删除对应位置上的信息
        content['step'].insert(to_index, removed_action)
        save_file_content(moduleItem.path, content, logger=LOG, translater=True)
        LOG.trace(f'Action info at "step" index {move_index} move to index {move_index} successfully at {moduleItem.path}')

    def __swap_actionInfo(self, index_1: int, index_2: int):
        """ 将 module 文件(step)中两个不同索引的 action 信息交换 """
        moduleItem = self.view.tree.topLevelItem(0)
        content = load_file_content(moduleItem.path, logger=LOG, translater=True)
        content['step'][index_1], content['step'][index_2] = content['step'][index_2], content['step'][index_1] # 交换值
        save_file_content(moduleItem.path, content, logger=LOG, translater=True)
        LOG.trace(f'Action info at "step" index {index_1} and {index_2} swap successfully at {moduleItem.path}')
    
    def __delete_item(self, item: TreeWidgetItem):
        """
        删除选中的项, 菜单操作
        """
        parent = item.parent() or self.view.tree.invisibleRootItem()
        index = parent.indexOfChild(item)
        parent.removeChild(item)
        self.__delete_actionInfo(index)
    
    def __move_item_up(self, item: TreeWidgetItem):
        """
        上移选中的项, 菜单操作
        """
        parent = item.parent() or self.view.tree.invisibleRootItem()
        index = parent.indexOfChild(item)
        if index > 0: # 第一项不动
            parent.takeChild(index)
            parent.insertChild(index - 1, item)
            self.view.tree.setCurrentItem(item)  # 重新选中该项
            # 保持action子项所有列合并
            if item.type == 'action':
                item.setFirstColumnSpanned(True)
            self.__swap_actionInfo(index, index - 1)
    
    def __move_item_down(self, item: TreeWidgetItem):
        """
        下移选中的项, 菜单操作
        """
        parent = item.parent() or self.view.tree.invisibleRootItem()
        index = parent.indexOfChild(item)
        if index < parent.childCount() - 1: # 最后一项不动
            parent.takeChild(index)
            parent.insertChild(index + 1, item)
            self.view.tree.setCurrentItem(item)  # 重新选中该项
            # 保持action子项所有列合并
            if item.type == 'action':
                item.setFirstColumnSpanned(True)
            self.__swap_actionInfo(index, index + 1)
    
    def __set_all_items_expanded(self, current_item: QTreeWidgetItem, state: bool):
        """ 递归设置当前项及其下子项的展开状态 """
        current_item.setExpanded(state)
        
        # 递归设置所有子项
        for i in range(current_item.childCount()):
            self.__set_all_items_expanded(current_item.child(i), state)
    
    def __operate_thread(self, data: list | bool = False):
        """ 线程任务 """
        if OPERATE_LOCK.acquire(blocking=False): # 获取锁，立即返回
            self.view.operation_btn.setEnabled(False) # 禁止交互
            try:
                LOG.info(self.tr("开始测试 》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》", "Log_msg"))
                if len(data) == 1:
                    run_module_process(data[0])
                else:
                    workspace_settings = load_file_content(os.path.join(CONFIG_DIR, 'workspace.json'), LOG, translater=True)
                    multi_module_operation_mode = workspace_settings['settings']['multi_module_operation_mode']
                    if multi_module_operation_mode == 'concurrently':
                        run_modules_processes_concurrently(get_ordered_queue(path_list=data))
                    elif multi_module_operation_mode == 'sequential':
                        run_modules_processes_sequentially(get_ordered_queue(path_list=data))
                    else:
                        LOG.critical("未知的运行模式配置！multi_module_operation_mode: {}".format(multi_module_operation_mode))

                LOG.info(self.tr("测试结束《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《 ", "Log_msg"))
            except Exception as e:
                LOG.debug(f"{e}")
            finally:
                OPERATE_LOCK.release()  # 在进程任务完成后释放锁
                self.view.operation_btn.setEnabled(True) # 允许交互
        else:
            LOG.warning(self.tr("已有操作正在进行，请稍候再试", "Log_msg"))