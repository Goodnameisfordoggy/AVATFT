from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit

class Ui_LogDock(object):
    def setupUi(self, parent):
        self.center_widget = QWidget(parent)
        parent.setWidget(self.center_widget)
        self.center_widget_layout = QVBoxLayout(self.center_widget)
        
        # ������
        # self.search_box = QLineEdit(separentlf)
        # self.search_box.setObjectName('NEUTRAL') 
        # self.search_box.setPlaceholderText("�������������Enter����")
        # self.search_box.textChanged.connect()
        # center_widget_layout.addWidget(self.search_box)

        # ��־��
        self.logTextWidget = QTextEdit(parent)
        self.center_widget_layout.addWidget(self.logTextWidget)