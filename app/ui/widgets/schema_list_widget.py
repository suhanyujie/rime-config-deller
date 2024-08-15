from typing import Dict, List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QCheckBox,
    QSizePolicy,
    QBoxLayout,
    QFrame,
    QPushButton,
)
from ...core.deller import Deller, get_rime_user_dir


class SchemaListWidget(QWidget):
    def __init__(
        self,
        parent=None,
    ) -> None:
        self.list: List[Dict] = []
        self.deller: Deller
        super().__init__(parent)
        self.initData()
        self.initUI()

    def initData(self):
        deller = Deller(get_rime_user_dir())
        self.list = deller.get_schema_name_list()
        self.deller = deller
        pass

    def initUI(self):
        layout = QVBoxLayout()

        # 添加标题
        layout.addWidget(QLabel("输入法方案列表:"))

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
            for tmp_id in item_dict.keys():
                checkbox = QCheckBox(tmp_id)
                checkbox.setText(item_dict[tmp_id])
                container_layout.addWidget(checkbox)
                checkbox.setSizePolicy(
                    QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
                )
                self.checkboxes.append(checkbox)

        container_layout.addStretch(1)

        self.set_hr_line(container_layout)
        self.set_button(container_layout)

        container.setLayout(container_layout)
        scroll_area.setWidget(container)

        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def get_checked_items(self):
        return [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]

    def set_hr_line(self, container_layout: QVBoxLayout):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        container_layout.addWidget(line)

    def set_button(self, container_layout: QVBoxLayout):
        submit_button = QPushButton("确定删除")
        submit_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        submit_button.clicked.connect(self.submit)
        container_layout.addWidget(submit_button)

    def submit(self):
        checked_items = self.get_checked_items()
        for tmp_id in checked_items:
            if tmp_id not in self.deller.schema_map_keyby_id:
                continue
            tmp_schema = self.deller.schema_map_keyby_id[tmp_id]
            print("找到要删除的 schema: ", tmp_schema.nick_name)
        print(checked_items, "删除文件")
        pass
