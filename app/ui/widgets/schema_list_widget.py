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
from PyQt6.QtGui import QFont
from ...core.deller import Deller, get_rime_user_dir


class SchemaListWidget(QWidget):
    def __init__(
        self,
        parent=None,
    ) -> None:
        self.list: List[Dict] = []
        self.deller: Deller
        super().__init__(parent)
        self.msg_box = QLabel(self)
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
        self.show_normal_info()
        layout.addWidget(self.msg_box)
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
        ignore_id_list = self.deller.get_ignore_list()
        for item_dict in self.list:
            for tmp_id in item_dict.keys():
                checkbox = QCheckBox(tmp_id)
                checkbox.setText(item_dict[tmp_id])
                checkbox.pri_value = tmp_id
                if tmp_id in ignore_id_list:
                    checkbox.setDisabled(True)
                    checkbox.setStyleSheet("QCheckBox:disabled { color: gray; }")
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

    def update(self):
        self.list: List[Dict] = []
        self.deller: Deller
        self.initData()
        self.initUI()

    def get_checked_items(self):
        return [checkbox for checkbox in self.checkboxes if checkbox.isChecked()]

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
        checked_checkbox_arr = self.get_checked_items()
        checked_item_ids = []
        checked_item_names = []
        ignore_ids = self.deller.get_ignore_list()
        for item in checked_checkbox_arr:
            tmp_id = item.pri_value
            if tmp_id in ignore_ids:
                continue
            checked_item_names.append(item.text())
            if tmp_id not in self.deller.schema_map_keyby_id:
                continue
            checked_item_ids.append(tmp_id)
            # tmp_schema = self.deller.schema_map_keyby_id[tmp_id]
        if len(checked_item_names) <= 0:
            self.show_warning("没有要删除的文件...")
        print("删除方案 name 列表", checked_item_names)
        print("删除方案 id 列表", checked_item_ids)
        self.deller.delete_by_schema_ids(checked_item_ids)
        self.update()
        pass

    def show_tips(self, msg: str):
        self.msg_box.setText(msg)
        pass

    def show_normal_info(self):
        self.msg_box.setText("Tips: 欢迎使用~")
        pass

    def show_warning(self, msg: str):
        self.msg_box.setStyleSheet("color:#cc6633")
        self.msg_box.setText(msg)
        self.msg_box.setFont(QFont("Arial", 20))
        pass
