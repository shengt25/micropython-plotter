from PySide6.QtWidgets import QToolBar
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction


class CodeToolBar(QToolBar):

    # Signals
    run_clicked = Signal()
    stop_clicked = Signal()
    save_clicked = Signal()
    # reset_clicked = Signal()  # 暂时禁用软重启功能

    def __init__(self, parent=None):
        super().__init__("Code Control", parent)

        self.run_action = QAction("Run", self)
        self.stop_action = QAction("Stop", self)
        self.save_action = QAction("Save", self)
        # self.reset_action = QAction("Soft Reset", self)  # 暂时禁用软重启功能

        self.run_action.triggered.connect(self.run_clicked.emit)
        self.stop_action.triggered.connect(self.stop_clicked.emit)
        self.save_action.triggered.connect(self.save_clicked.emit)
        # self.reset_action.triggered.connect(self.reset_clicked.emit)  # 暂时禁用软重启功能

        # 保存按钮默认禁用（只有打开文件并修改后才启用）
        self.save_action.setEnabled(False)

        self.addAction(self.run_action)
        self.addAction(self.stop_action)
        self.addSeparator()
        self.addAction(self.save_action)
        # self.addSeparator()  # 暂时禁用软重启功能
        # self.addAction(self.reset_action)  # 暂时禁用软重启功能

        self.setMovable(False)
