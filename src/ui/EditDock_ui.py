from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QCheckBox, QLineEdit, QTreeWidget, QPushButton

class Ui_EditDock(object):
    def setupUi(self, parent):
        self.center_widget = QWidget(parent)
        parent.setWidget(self.center_widget)
        self.center_widget_layout = QVBoxLayout(self.center_widget)

        self.search_layout = QHBoxLayout()
        # 复选框
        self.check_box = QCheckBox(parent)
        self.check_box.setObjectName('SECONDARY')
        self.check_box.setEnabled(False)
        self.search_layout.addWidget(self.check_box, 1)

        # 复选框
        self.check_box2 = QCheckBox(parent)
        self.check_box2.setObjectName('SECONDARY')
        self.check_box2.setEnabled(False)
        self.search_layout.addWidget(self.check_box2, 1)

        # 搜索框
        self.search_box = QLineEdit(parent)
        self.search_box.setObjectName('SECONDARY')
        self.search_box.setPlaceholderText(QCoreApplication.translate("ProjectDock_ui", "请输入搜索项，按Enter搜索", "search_box_placeholder_text"))
        self.search_layout.addWidget(self.search_box, 99)

        # 搜索方法下拉列表
        self.search_combo_box =  QComboBox()
        self.search_combo_box.addItems([QCoreApplication.translate("ProjectDock_ui", "匹配参数描述", "search_combo_box_item_Pdescribe"), 
                                        QCoreApplication.translate("ProjectDock_ui", "匹配参数名称", "search_combo_box_item_Pname"), 
                                        QCoreApplication.translate("ProjectDock_ui", "匹配参数值", "search_combo_box_item_Pvalue")]) # 添加选项
        self.search_layout.addWidget(self.search_combo_box, 1)
        self.center_widget_layout.addLayout(self.search_layout)

        # 树状控件
        self.tree = QTreeWidget(parent)
        # self.tree.setObjectName('SECONDARY')
        self.tree.setColumnCount(3) # 列数
        self.tree.setHeaderLabels([QCoreApplication.translate("ProjectDock_ui", "匹配参数描述", "search_combo_box_item_Pdescribe"), 
                            QCoreApplication.translate("ProjectDock_ui", "匹配参数名称", "search_combo_box_item_Pname"), 
                            QCoreApplication.translate("ProjectDock_ui", "匹配参数值", "search_combo_box_item_Pvalue")])
        self.tree.setDragEnabled(True) # 能否拖拽
        self.tree.setAcceptDrops(True) # 能否放置
        self.tree.setDropIndicatorShown(True) # 是否启用放置指示器
        self.tree.setDefaultDropAction(Qt.CopyAction) # 放置操作 (MoveAction, CopyAction, LinkAction: 创建一个链接或引用)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu) # 右键菜单
        self.center_widget_layout.addWidget(self.tree)

        self.button_layout = QHBoxLayout()
        # 运行按钮
        self.operation_btn = QPushButton(parent, text=QCoreApplication.translate("ProjectDock_ui", "开始测试", "operation_button_text"))
        self.operation_btn.setFocusPolicy(Qt.NoFocus)  # 禁用键盘焦点
        self.button_layout.addWidget(self.operation_btn)
        self.center_widget_layout.addLayout(self.button_layout)