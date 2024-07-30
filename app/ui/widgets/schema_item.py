from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtCore import Qt


class SchemaItemWidget(QCheckBox):
    def __init__(self, parent=None, label: str = "", value: str = ""):
        super().__init__(label, parent)
        self.setChecked(False)
        self.value = value
        self.initUI()
        pass

    def initUI(self):
        # 添加初始化逻辑，例如设置样式或信号槽连接
        self.stateChanged.connect(self.on_state_changed)

    def on_state_changed(self, state):
        # 处理复选框状态变化的逻辑
        if state == Qt.Checked:
            print(f"{self.text()} is checked")
        else:
            print(f"{self.text()} is unchecked")

    def get_value(self) -> str:
        return self.value

    def set_value(self, value: str):
        self.value = value

    def is_checked(self):
        return self.isChecked()
