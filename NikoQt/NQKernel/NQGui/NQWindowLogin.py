from NikoKit.NikoQt.NQAdapter import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton
from NikoKit.NikoQt.NQApplication import Runtime
from NikoKit.NikoQt.NQKernel.NQGui.NQWindow import NQWindow


class NQWindowLogin(NQWindow):

    @staticmethod
    def new_appdata():
        return {
            "username": "",
            "password": "",
            "remember_me": False,
            "auto_login": False,
        }

    def __init__(self,
                 login_validator,
                 w_title="NQWindowLogin",
                 w_width=300,
                 w_height=100,
                 appdata_name="Login",
                 require_username=True,
                 require_password=True,
                 allow_remember_me=True,
                 allow_auto_login=True,
                 **kwargs):
        # Private Storage
        self.login_validator = login_validator
        self.appdata_name = appdata_name
        self.require_username = require_username
        self.require_password = require_password
        self.allow_remember_me = allow_remember_me
        self.allow_auto_login = allow_auto_login

        # GUI Component
        self.main_lay = None
        self.username_lay_adapter = None
        self.username_line_edit = None
        self.password_lay_adapter = None
        self.password_line_edit = None
        self.remember_me_checkbox = None
        self.auto_login_checkbox = None
        self.message_label = None
        self.login_button = None

        super(NQWindowLogin, self).__init__(w_title=w_title,
                                            w_width=w_width,
                                            w_height=w_height,
                                            **kwargs)

        # Initialization
        appdata = self.load_appdata()
        if appdata["auto_login"]:
            self.slot_login_button_clicked()
        self.apply_appdata(self.load_appdata())

    def construct(self):
        super(NQWindowLogin, self).construct()
        main_lay = QVBoxLayout()
        username_lay = QHBoxLayout()
        username_label = QLabel(self.lang("account"))
        username_line_edit = QLineEdit()
        password_lay = QHBoxLayout()
        password_label = QLabel(self.lang("password"))
        password_line_edit = QLineEdit()
        checkbox_lay = QHBoxLayout()
        remember_me_checkbox = QCheckBox(self.lang("remember") + self.lang("account"))
        auto_login_checkbox = QCheckBox(self.lang("auto") + self.lang("login"))
        message_lay = QHBoxLayout()
        message_label = QLabel("")
        login_button = QPushButton(self.lang("login"))

        if self.require_username:
            main_lay.addLayout(username_lay)
        if self.require_password:
            main_lay.addLayout(password_lay)
        if self.allow_remember_me or self.allow_auto_login:
            main_lay.addLayout(checkbox_lay)
        main_lay.addLayout(message_lay)
        main_lay.addWidget(login_button)

        username_lay.addWidget(username_label)
        username_lay.addWidget(username_line_edit)

        password_lay.addWidget(password_label)
        password_lay.addWidget(password_line_edit)

        checkbox_lay.addStretch()
        if self.allow_remember_me:
            checkbox_lay.addWidget(remember_me_checkbox)
            if self.allow_auto_login:
                checkbox_lay.addWidget(auto_login_checkbox)
        checkbox_lay.addStretch()

        message_lay.addStretch()
        message_lay.addWidget(message_label)
        message_lay.addStretch()

        self.main_lay = main_lay
        self.username_line_edit = username_line_edit
        self.password_line_edit = password_line_edit
        self.remember_me_checkbox = remember_me_checkbox
        self.auto_login_checkbox = auto_login_checkbox
        self.message_label = message_label
        self.login_button = login_button

        self.setLayout(self.main_lay)

    def connect_signals(self):
        super(NQWindowLogin, self).connect_signals()
        self.login_button.clicked.connect(self.slot_login_button_clicked)

    def slot_login_button_clicked(self):
        username, password = self.get_username_password()
        try:
            if self.login_validator(username, password):
                self.save_appdata(self.extract_appdata())
                self.signal_done.emit(self.w_id, (username, password))
            else:
                self.message_label.setText(self.lang("username")
                                           + self.lang("or")
                                           + self.lang("password")
                                           + self.lang("incorrect"))
        except Exception as e:
            self.message_label.setText("validator failure:" + str(e))

    def get_username_password(self):
        return self.username_line_edit.text(), self.password_line_edit.text()

    def load_appdata(self):
        local_appdata = Runtime.Service.AppDataMgr.get(self.appdata_name)
        appdata = self.new_appdata()
        if local_appdata:
            appdata.update(local_appdata)
        return appdata

    def save_appdata(self, appdata):
        Runtime.Service.AppDataMgr.set(self.appdata_name, appdata)
        Runtime.Service.AppDataMgr.save(self.appdata_name)

    def extract_appdata(self):
        appdata = self.new_appdata()
        username, password = self.get_username_password()

        if self.allow_remember_me and self.remember_me_checkbox.isChecked():
            appdata["username"] = username
            appdata["password"] = password
            appdata["remember_me"] = True
            if self.allow_auto_login and self.auto_login_checkbox.isChecked():
                appdata["auto_login"] = True

        return appdata

    def apply_appdata(self, appdata):
        if self.require_username:
            self.username_line_edit.setText(appdata["username"])
        else:
            self.username_line_edit.setText("")

        if self.require_password:
            self.password_line_edit.setText(appdata["password"])
        else:
            self.password_line_edit.setText("")

        if self.allow_remember_me:
            self.remember_me_checkbox.setChecked(appdata["remember_me"])
        else:
            self.remember_me_checkbox.setChecked(False)

        if self.allow_auto_login:
            self.auto_login_checkbox.setChecked(appdata["auto_login"])
        else:
            self.auto_login_checkbox.setChecked(False)
