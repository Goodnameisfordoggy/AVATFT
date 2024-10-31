from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTreeWidget

class Ui_ProjectDock(object):
    def setupUi(self, parent):
        self.center_widget = QWidget(parent)
        parent.setWidget(self.center_widget)
        self.center_widget_layout = QVBoxLayout(self.center_widget)
        
        # 搜索框
        self.search_box = QLineEdit(parent)
        self.search_box.setObjectName('NEUTRAL')
        self.search_box.setPlaceholderText(QCoreApplication.translate("ProjectDock_ui", "请输入搜索项，按Enter搜索", "search_box_placeholder_text"))
        self.center_widget_layout.addWidget(self.search_box)

        # 树控件
        self.tree = QTreeWidget(parent)
        self.tree.setObjectName('NEUTRAL') 
        self.tree.setHeaderHidden(True) # 隐藏表头
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu) # 使用自定义菜单
        self.center_widget_layout.addWidget(self.tree)