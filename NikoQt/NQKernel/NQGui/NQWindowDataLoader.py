from NikoKit.NikoLib.NKDataLoader import NKDataLoader
from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQFunctions import clear_layout
from NikoKit.NikoQt.NQKernel.NQGui.NQWindow import NQWindow
from NikoKit.NikoStd.NKTime import NKDatetime


class NQWindowDataLoader(NQWindow):
    class DataLoadWidgets(QObject):
        def __init__(self,
                     data_load_name,
                     label_label,
                     label_status,
                     label_updated_datetime,
                     label_reload_timeout,
                     checkbox_auto_load,
                     checkbox_auto_update,
                     spinbox_auto_update_time_gap,
                     btn_load,
                     btn_update,
                     btn_clear,
                     btn_apply,
                     error_text_edit,
                     ):
            super(NQWindowDataLoader.DataLoadWidgets, self).__init__()
            self.data_load_name = data_load_name
            self.label_label = label_label
            self.label_status = label_status
            self.label_updated_datetime = label_updated_datetime
            self.label_reload_timeout = label_reload_timeout
            self.checkbox_auto_load = checkbox_auto_load
            self.checkbox_auto_update = checkbox_auto_update
            self.spinbox_auto_update_time_gap = spinbox_auto_update_time_gap
            self.btn_load = btn_load
            self.btn_update = btn_update
            self.btn_clear = btn_clear
            self.btn_apply = btn_apply
            self.error_text_edit = error_text_edit

    def __init__(self,
                 data_loader,
                 w_width=1024,
                 w_height=500,
                 *args,
                 **kwargs):
        self.data_loader = data_loader
        self.data_name_to_widgets = {}
        self.errors = []

        # GUI Component
        self.main_lay = None
        self.grid_lay = None
        self.grid_lay_adapter = None
        self.btn_lay = None

        self.btn_load_all = None
        self.btn_clear_all = None
        self.btn_apply_setting = None

        self.error_lay = None
        self.error_lay_adapter = None
        self.error_text_edit_data_loader = None

        super(NQWindowDataLoader, self).__init__(w_width=w_width,
                                                 w_height=w_height,
                                                 *args,
                                                 **kwargs)

    def construct(self):
        super(NQWindowDataLoader, self).construct()
        main_lay = QVBoxLayout()
        grid_lay_adapter = QWidget()
        btn_lay = QHBoxLayout()
        error_lay_adapter = QWidget()
        error_text_edit_data_loader = QTextEdit()
        error_text_edit_data_loader.setReadOnly(True)

        btn_load_all = QPushButton(self.lang("download", "all"))
        btn_clear_all = QPushButton(self.lang("clear", "all"))
        btn_apply_setting = QPushButton(self.lang("apply", "setting"))

        main_lay.addWidget(grid_lay_adapter)
        main_lay.addWidget(error_lay_adapter)
        main_lay.addLayout(btn_lay)
        main_lay.setStretchFactor(grid_lay_adapter, 1)

        btn_lay.addStretch()
        btn_lay.addWidget(btn_load_all)
        btn_lay.addWidget(btn_clear_all)
        btn_lay.addWidget(btn_apply_setting)
        btn_lay.addStretch()

        self.main_lay = main_lay
        self.grid_lay_adapter = grid_lay_adapter
        self.btn_lay = btn_lay
        self.error_lay_adapter = error_lay_adapter
        self.error_text_edit_data_loader = error_text_edit_data_loader

        self.btn_load_all = btn_load_all
        self.btn_clear_all = btn_clear_all
        self.btn_apply_setting = btn_apply_setting

        self.setLayout(self.main_lay)

    def connect_signals(self):
        super(NQWindowDataLoader, self).connect_signals()
        self.btn_load_all.clicked.connect(self.slot_load_all)
        self.btn_clear_all.clicked.connect(self.slot_clear_all)
        self.btn_apply_setting.clicked.connect(self.slot_apply_all)

    def load_widgets(self):
        clear_layout(self.grid_lay)
        clear_layout(self.error_lay)

        grid_lay = QGridLayout()
        error_lay = QHBoxLayout()
        error_tab_widget = QTabWidget()
        error_tab_widget.addTab(self.error_text_edit_data_loader, "DataLoader")
        error_lay.addWidget(error_tab_widget)

        data_name_to_widgets = {}
        grid_lay.addWidget(QLabel(self.lang("data", "pack")), 0, 0, 1, 1)
        grid_lay.addWidget(QLabel(self.lang("status")), 0, 1, 1, 1)
        grid_lay.addWidget(QLabel(self.lang("update", "time")), 0, 2, 1, 1)
        grid_lay.addWidget(QLabel(self.lang("next_time", "auto", "update", "countdown")), 0, 3, 1, 1)
        grid_lay.addWidget(QLabel(self.lang("auto", "load")), 0, 4, 1, 1)
        grid_lay.addWidget(QLabel(self.lang("auto", "update")), 0, 5, 1, 1)
        grid_lay.addWidget(QLabel(self.lang("auto", "update", "time", "gap")), 0, 6, 1, 1)
        grid_lay.addWidget(QLabel(self.lang("available", "operation")), 0, 7, 1, 1)

        for idx, data_load_name in enumerate(self.data_loader.data_loads.keys()):
            data_load = self.data_loader.data_loads[data_load_name]
            spinbox_auto_update_time_gap = QSpinBox()
            spinbox_auto_update_time_gap.setRange(10, 86400)
            spinbox_auto_update_time_gap.setSingleStep(1)
            spinbox_auto_update_time_gap.setValue(3600)

            btn_adapter = QWidget()
            btn_lay = QHBoxLayout()
            btn_load = QPushButton(self.lang("load"))
            btn_load.data_load_name = data_load_name
            btn_update = QPushButton(self.lang("update"))
            btn_update.data_load_name = data_load_name
            btn_clear = QPushButton(self.lang("clear"))
            btn_clear.data_load_name = data_load_name
            btn_apply = QPushButton(self.lang("apply"))
            btn_apply.data_load_name = data_load_name
            btn_adapter.setLayout(btn_lay)
            btn_lay.addWidget(btn_load)
            btn_lay.addWidget(btn_update)
            btn_lay.addWidget(btn_clear)
            btn_lay.addWidget(btn_apply)

            error_text_edit = QTextEdit()
            error_text_edit.setReadOnly(True)
            error_text_edit.setLineWrapMode(QTextEdit.NoWrap)

            dl_widgets = self.DataLoadWidgets(
                data_load_name=data_load_name,
                label_label=QLabel(self.lang(data_load.label)),
                label_status=QLabel(self.lang(data_load.status)),
                label_updated_datetime=QLabel(self.lang(NKDatetime.datetime_to_str(data_load.updated_datetime))),
                label_reload_timeout=QLabel(str(data_load.auto_reload_timeout_sec - data_load.auto_reload_current_sec)),
                checkbox_auto_load=QCheckBox(),
                checkbox_auto_update=QCheckBox(),
                spinbox_auto_update_time_gap=spinbox_auto_update_time_gap,
                btn_load=btn_load,
                btn_update=btn_update,
                btn_clear=btn_clear,
                btn_apply=btn_apply,
                error_text_edit=error_text_edit,
            )

            btn_load.clicked.connect(self.slot_load)
            btn_update.clicked.connect(self.slot_reload)
            btn_clear.clicked.connect(self.slot_clear)
            btn_apply.clicked.connect(self.slot_apply)

            data_name_to_widgets[data_load.name] = dl_widgets
            grid_lay.addWidget(dl_widgets.label_label, idx + 1, 0, 1, 1)
            grid_lay.addWidget(dl_widgets.label_status, idx + 1, 1, 1, 1)
            grid_lay.addWidget(dl_widgets.label_updated_datetime, idx + 1, 2, 1, 1)
            grid_lay.addWidget(dl_widgets.label_reload_timeout, idx + 1, 3, 1, 1)
            grid_lay.addWidget(dl_widgets.checkbox_auto_load, idx + 1, 4, 1, 1)
            grid_lay.addWidget(dl_widgets.checkbox_auto_update, idx + 1, 5, 1, 1)
            grid_lay.addWidget(dl_widgets.spinbox_auto_update_time_gap, idx + 1, 6, 1, 1)
            grid_lay.addWidget(btn_adapter, idx + 1, 7, 1, 1)
            error_tab_widget.addTab(dl_widgets.error_text_edit, data_load_name)

        # grid_lay.setRowStretch(grid_lay.rowCount(), 1)
        grid_lay.setAlignment(Qt.AlignTop)

        self.grid_lay_adapter.setLayout(grid_lay)
        self.grid_lay = grid_lay
        self.error_lay_adapter.setLayout(error_lay)
        self.error_lay = error_lay
        self.data_name_to_widgets = data_name_to_widgets

    def slot_refresh(self, reset=False):
        log_str = "\n".join(self.data_loader.logs)
        if self.error_text_edit_data_loader.toPlainText() != log_str:
            self.error_text_edit_data_loader.setText(log_str)
            self.error_text_edit_data_loader.moveCursor(QTextCursor.End)

        for data_load_name in self.data_loader.data_loads.keys():
            data_load = self.data_loader.data_loads[data_load_name]
            if data_load.name not in self.data_name_to_widgets.keys():
                self.load_widgets()
                self.slot_refresh(reset=True)
            else:
                data_load_widgets = self.data_name_to_widgets[data_load.name]
                data_load_widgets.label_label.setText(self.lang(data_load.label))
                data_load_widgets.label_status.setText(self.lang(data_load.status))
                data_load_widgets.label_updated_datetime.setText(
                    self.lang(NKDatetime.datetime_to_str(data_load.updated_datetime)))
                data_load_widgets.label_reload_timeout.setText(
                    str(data_load.auto_reload_timeout_sec - data_load.auto_reload_current_sec)
                )
                if reset:
                    data_load_widgets.checkbox_auto_load.setChecked(data_load.auto_load)
                    data_load_widgets.checkbox_auto_update.setChecked(data_load.auto_reload)
                    data_load_widgets.spinbox_auto_update_time_gap.setValue(data_load.auto_reload_timeout_sec)

                if data_load.status in (NKDataLoader.UNLOAD, NKDataLoader.LOAD_ERROR):
                    data_load_widgets.btn_load.show()
                else:
                    data_load_widgets.btn_load.hide()

                if data_load.status == NKDataLoader.LOADED:
                    data_load_widgets.btn_update.show()
                else:
                    data_load_widgets.btn_update.hide()

                if data_load.status != NKDataLoader.CLEARING:
                    data_load_widgets.btn_clear.show()
                else:
                    data_load_widgets.btn_clear.hide()

                log_str = "\n".join(data_load.logs)
                if data_load_widgets.error_text_edit.toPlainText() != log_str:
                    data_load_widgets.error_text_edit.setText(log_str)
                    data_load_widgets.error_text_edit.moveCursor(QTextCursor.End)

    def slot_show(self):
        self.data_loader.load_appdata()
        self.slot_refresh(reset=True)
        self.show()

    def handle_error(self, errors):
        if errors:
            self.errors.extend(errors)
            self.error_text_edit.setText("\n".join(self.errors))

    def slot_load(self):
        self.handle_error(self.data_loader.data_loads[self.sender().data_load_name].load())

    def slot_reload(self):
        self.handle_error(self.data_loader.data_loads[self.sender().data_load_name].reload())

    def slot_clear(self):
        self.handle_error(self.data_loader.data_loads[self.sender().data_load_name].clear())

    def slot_apply(self):
        self.apply_data_load_values(self.sender().data_load_name)
        self.data_loader.save_appdata()

    def apply_data_load_values(self, data_load_name):
        dl_widgets = self.data_name_to_widgets[data_load_name]
        dl = self.data_loader.data_loads[data_load_name]

        dl.auto_load = dl_widgets.checkbox_auto_load.isChecked()
        dl.auto_reload = dl_widgets.checkbox_auto_update.isChecked()
        dl.auto_reload_timeout_sec = dl_widgets.spinbox_auto_update_time_gap.value()

    def slot_load_all(self):
        for data_load_name in self.data_loader.data_loads.keys():
            data_load = self.data_loader.data_loads[data_load_name]
            if data_load.status == NKDataLoader.LOADED:
                self.handle_error(data_load.reload())
            else:
                self.handle_error(data_load.load())

    def slot_clear_all(self):
        for data_load_name in self.data_loader.data_loads.keys():
            data_load = self.data_loader.data_loads[data_load_name]
            self.handle_error(data_load.clear())

    def slot_apply_all(self):
        for dl_name in self.data_name_to_widgets.keys():
            self.apply_data_load_values(dl_name)
        self.data_loader.save_data()

    def closeEvent(self, event):
        event.ignore()
        self.slot_hide()
