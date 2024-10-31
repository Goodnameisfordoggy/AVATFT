from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLineEdit, QTreeWidget

class Ui_ActionDock(object):
    def setupUi(self, parent):
        if not parent.objectName():
            parent.setObjectName("ActionDock")
        parent.resize(400, 300)

        self.center_widget = QWidget(parent)
        parent.setWidget(self.center_widget)
        self.center_widget_layout = QVBoxLayout(self.center_widget)
        
        self.layout = QHBoxLayout()
        self.center_widget_layout.addLayout(self.layout)
        # 复选框
        self.check_box = QCheckBox(parent)
        
        self.check_box.setObjectName('NEUTRAL')
        self.layout.addWidget(self.check_box, 1)
        # 搜索框
        self.search_box = QLineEdit(parent)
        self.search_box.setObjectName('NEUTRAL')
        self.search_box.setPlaceholderText(QCoreApplication.translate("Ui_ActionDock", "请输入搜索项，按Enter搜索", "search_box_placeholder_text"))
        self.layout.addWidget(self.search_box, 99)
        
        # 树控件
        self.tree = QTreeWidget(parent)
        self.tree.setObjectName('NEUTRAL') 
        self.center_widget_layout.addWidget(self.tree)
        self.tree.setHeaderHidden(True) # 隐藏表头
        # 拖拽功能
        self.tree.setDragEnabled(True) # 能否拖拽
        self.tree.setAcceptDrops(False) # 能否放置
        self.tree.setDropIndicatorShown(True) # 是否启用放置指示器
        self.tree.setDefaultDropAction(Qt.CopyAction) # 放置操作 (MoveAction, CopyAction, LinkAction: 创建一个链接或引用)
        # 连接右键菜单事件
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        
