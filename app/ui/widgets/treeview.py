"""app/ui/widgets/treeview.py"""

from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir


class TreeView(QTreeView):
    """
    Initialize the TreeView widget.

    Args:
        parent (QWidget, optional): Parent widget of the TreeView. Defaults to None.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.file_system_model: QFileSystemModel = QFileSystemModel()
        default_dir = QDir.currentPath()
        if parent.rime_user_dir != "":
            default_dir = parent.rime_user_dir
        self.file_system_model.setRootPath(default_dir)
        self.setModel(self.file_system_model)
        self.setRootIndex(self.file_system_model.index(default_dir))
        self.setFixedWidth(300)
        # 隐藏多余的列
        self.setSortingEnabled(False)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)

    def clear_view(self) -> None:
        """
        Clearing the TreeView
        """
        self.destroy(destroySubWindows=True)

    def refresh(self) -> None:
        self.update()
        pass
