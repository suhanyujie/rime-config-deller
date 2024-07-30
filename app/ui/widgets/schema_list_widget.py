from typing import Dict, List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QCheckBox,
    QSizePolicy,
    QBoxLayout,
)
from ...core.deller import Deller, get_rime_user_dir


class SchemaListWidget(QWidget):
    def __init__(
        self,
        parent=None,
    ) -> None:
        self.list: List[Dict] = []
        super().__init__(parent)
        self.initData()
        self.initUI()

    def initData(self):
        deller = Deller(get_rime_user_dir())
        self.list = deller.get_schema_name_list()
        pass

    def initUI(self):
        layout = QVBoxLayout()

        # 添加标题
        layout.addWidget(QLabel("方案列表:"))

        # 创建一个滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # 创建一个容器窗口，放置复选框
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(1)
        container_layout.setDirection(QBoxLayout.Direction.TopToBottom)
        # 创建复选框并添加到容器布局中
        self.checkboxes = []
        for item_dict in self.list:
            for key in item_dict.keys():
                checkbox = QCheckBox(key)
                container_layout.addWidget(checkbox)
                checkbox.setSizePolicy(
                    QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
                )
                self.checkboxes.append(checkbox)

        container_layout.addStretch(1)
        container.setLayout(container_layout)
        scroll_area.setWidget(container)

        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def get_checked_items(self):
        return [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
