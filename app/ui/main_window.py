"""app/ui/main_window.py"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QTextEdit,
    QToolBar,
    QToolButton,
)
from PyQt6.QtGui import QIcon, QAction
from app.ui.widgets.schema_list_widget import SchemaListWidget
from ..utils.config import AppConfig
from .widgets.menubar import MenuBar
from .widgets.toolbar import ToolBar, get_separator
from .widgets.statusbar import StatusBar
from .widgets.treeview import TreeView
from ..core.deller import get_rime_user_dir


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        """
        Initialize the Main-Window.
        """
        super().__init__()
        # Window-Settings
        self.setWindowTitle(AppConfig.APP_NAME)
        self.resize(800, 600)
        self.center()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        # Create Widgets
        self.treeview = self.create_treeview()
        self.editbox = self.create_edit()

        # Add Widgets to Window
        # self.setMenuBar(MenuBar(self))
        # self.setStatusBar(StatusBar(self))
        self.top_toolbar = self.addToolBar("Open")
        self.top_toolbar_add_button()

        # layout.addWidget(get_separator(self))
        refresh_btn = QToolButton(self)
        refresh_btn.setText("刷新")
        layout.addWidget(refresh_btn)
        layout.addWidget(self.treeview)
        layout.addWidget(self.create_rime_list_view())
        # layout.addWidget(self.editbox, stretch=1)
        # layout.addWidget(self.editbox)
        refresh_btn.triggered.connect(self.refresh_filelist)

    def refresh_filelist(self):
        self.treeview.refresh()
        pass

    def top_toolbar_add_button(self):
        # 创建并添加新建操作按钮
        new_action = QAction(QIcon("new_icon.png"), "Open", self)
        new_action.setShortcut("Ctrl+O")
        new_action.setStatusTip("open dir")
        new_action.triggered.connect(self.open_file)
        self.top_toolbar.addAction(new_action)
        pass

    def create_toolbars(self) -> None:
        """
        Creates and adds the top and right toolbars to the main window.
        """
        self.set_top_bar()

    def set_top_bar(self):
        # Top Toolbar [PyQt6.QtWidgets.QToolBar]
        self.topbar = ToolBar(
            self,
            orientation=Qt.Orientation.Horizontal,
            style=Qt.ToolButtonStyle.ToolButtonTextUnderIcon,
            icon_size=(44, 44),
        )
        # Top Toolbar Buttons
        self.topbar.add_button(
            "Open", "resources/assets/icons/windows/imageres-10.ico", self.open_file
        )
        # self.topbar.add_button(
        #     "Save", "resources/assets/icons/windows/shell32-259.ico", self.save_file
        # )
        # self.topbar.add_button(
        #     "Exit", "resources/assets/icons/windows/shell32-220.ico", self.exit_app
        # )
        pass

    # しばらく、いらない
    def set_right_bar(self):
        # Right Toolbar [PyQt6.QtWidgets.QToolBar]
        self.rightbar = ToolBar(
            self,
            orientation=Qt.Orientation.Vertical,
            style=Qt.ToolButtonStyle.ToolButtonIconOnly,
            icon_size=(24, 24),
        )

        # Right Toolbar Buttons
        self.rightbar.add_separator()
        self.rightbar.add_button(
            "Privacy",
            "resources/assets/icons/windows/shell32-167.ico",
            self.privacy_window,
        )
        self.rightbar.add_button(
            "Settings",
            "resources/assets/icons/windows/shell32-315.ico",
            self.settings_window,
        )

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.topbar)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.rightbar)

    def create_treeview(self) -> TreeView:
        """
        Creates and adds the tree view widget to the main window.
        """
        return TreeView(self)

    def create_rime_list_view(self) -> QWidget:
        """
        Creates and adds the QTextEdit widget to the main window.
        """
        return SchemaListWidget()

    def create_edit(self) -> QTextEdit:
        """
        Creates and adds the QTextEdit widget to the main window.
        """
        return QTextEdit(self)

    def open_file(self) -> None:
        """
        Event handler for the "Open" button. Displays the "Open File" dialog.
        """
        print("Open")

    def save_file(self) -> None:
        """
        Event handler for the "Save" button. Displays the "Save File" dialog.
        """
        print("Save")

    def exit_app(self) -> None:
        """
        Event handler for the "Exit" button. Closes the application.
        """
        self.close()

    def settings_window(self) -> None:
        """
        Event handler for the "Settings" button. Displays the "Settings" window.
        """

    def privacy_window(self) -> None:
        """
        Event handler for the "Privacy" button. Displays the "Privacy" window.
        """
        print("privacy_window")

    def center(self):
        # 获取屏幕的尺寸
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_center = screen_geometry.center()
        # 获取窗口的尺寸
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_center)
        # 将窗口移动到屏幕中央
        self.move(window_geometry.topLeft())
        self.get_rime_user_dir()

    def get_rime_user_dir(self) -> str:
        self.rime_user_dir = get_rime_user_dir()
        pass
