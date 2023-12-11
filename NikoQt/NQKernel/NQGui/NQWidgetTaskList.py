from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout


class NQWidgetTaskList(QListWidget):
    task_clicked = Signal(int, object)  # Signal to emit when a task is clicked

    def __init__(self, parent=None):
        super(NQWidgetTaskList, self).__init__(parent)
        self.task_widgets = []
        self.itemClicked.connect(self._on_task_clicked)

        self.setStyleSheet(
            '''
            QListWidget::item {
                border: none;
            }
            QListWidget::item:hover {
                background-color: #24323e;
            }
            QListWidget::item:selected {
                background-color: #214283;
                border: 1px dotted white;
            }
            #TaskWidgetOriginal {
                background-color: #424242;
            }
            '''
        )

    def _on_task_clicked(self, item):
        index = self.row(item)
        widget = self.task_widgets[index]
        self.task_clicked.emit(index, widget)

    def _wrap_task_widget(self, task_widget: QWidget):
        wrapper = QWidget()
        layout = QVBoxLayout(wrapper)
        layout.setContentsMargins(10, 5, 10, 5)  # Add 5px margin to all sides
        layout.addWidget(task_widget)
        task_widget.setObjectName("TaskWidgetOriginal")
        return wrapper

    def get_task_count(self):
        return len(self.task_widgets)

    def add_task(self, task_widget):
        if task_widget not in self.task_widgets:
            self.task_widgets.append(task_widget)
            wrapped_task_widget = self._wrap_task_widget(task_widget)
            item = QListWidgetItem(self)
            self.setItemWidget(item, wrapped_task_widget)
            item.setSizeHint(wrapped_task_widget.sizeHint())

    def insert_task(self, task_widget, index):
        if task_widget not in self.task_widgets:
            self.task_widgets.insert(index, task_widget)
            wrapped_task_widget = self._wrap_task_widget(task_widget)
            item = QListWidgetItem()
            self.insertItem(index, item)
            self.setItemWidget(item, wrapped_task_widget)
            item.setSizeHint(wrapped_task_widget.sizeHint())

    def remove_task(self, task_widget):
        if task_widget in self.task_widgets:
            index = self.task_widgets.index(task_widget)
            self.remove_task_by_index(index)

    def remove_task_by_index(self, index):
        item = self.takeItem(index)
        del self.task_widgets[index]
        del item

    def select_task(self, task_widget):
        if task_widget in self.task_widgets:
            index = self.task_widgets.index(task_widget)
            self.select_task_by_index(index)

    def select_task_by_index(self, index):
        item = self.item(index)
        self.setCurrentItem(item)

    def get_selected_task(self):
        item = self.currentItem()
        index = self.row(item)
        if index != -1:
            return self.task_widgets[index]
        return None

    def get_selected_task_index(self):
        item = self.currentItem()
        return self.row(item)
