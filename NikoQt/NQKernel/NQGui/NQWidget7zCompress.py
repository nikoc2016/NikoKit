import multiprocessing
import os

from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt import NQApplication
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetInput import NQWidgetInput
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetUrlSelector import NQWidgetUrlSelector
from NikoKit.NikoStd.NKPrint import eprint


# Simple Guide, use generate_7z_command_list() to get current setting or hook to the signal
class NQWidget7zCompress(NQWidget):
    COMP_SRC = "7Z_COMP_SRC"
    COMP_7Z_URL = "7Z_COMP_TGT"
    slot_compress = Signal(object)  # When Button clicked, this emits 7z command list.

    def __init__(self,
                 disable_source_url=False,  # Hide Widget, replace 7z command with NQWidget7zCompress.COMP_SRC
                 disable_out_url=False,  # Hide Widget, replace 7z command with NQWidget7zCompress.COMP_7Z_URL
                 disable_compress_btn=False,  # Hide Btn
                 disable_delete_src=False):  # Hide Checkbox, you can still set value.
        self.disable_source_url = disable_source_url
        self.disable_out_url = disable_out_url
        self.lang = NQApplication.Runtime.Service.NKLang.tran  # a function to convert tag to selected language
        self.layout = QVBoxLayout()
        self.user_in_source_url = NQWidgetUrlSelector(title=self.lang("7z_compress_src"),
                                                      mode=NQWidgetUrlSelector.MODE_DIR)
        self.user_in_out_7z_dir = NQWidgetUrlSelector(title=self.lang("7z_out_dir"),
                                                      mode=NQWidgetUrlSelector.MODE_DIR)
        self.user_in_out_7z_filename = NQWidgetInput(prompt=self.lang("7z_out_filename"),
                                                     mode=NQWidgetInput.MODE_TEXT,
                                                     default_value="new.7z",
                                                     stretch_in_the_end=True)
        self.user_in_compression_level_box = QComboBox()
        self.user_in_compression_level_box.addItems(
            ['0 - Store', '1 - Fastest', '3 - Fast', '5 - Normal', '7 - Maximum', '9 - Ultra'])
        self.user_in_dictionary_size_box = QComboBox()
        self.user_in_dictionary_size_box.addItems(
            ['64KB', '256KB', '1MB', '2MB', '3MB', '4MB', '6MB', '8MB', '12MB', '16MB', '24MB', '32MB',
             '48MB', '64MB', '96MB', '128MB', '192MB', '256MB', '384MB', '512MB', '768MB', '1024MB',
             '1536MB', '2048MB', '3072MB', '3840MB'])
        self.user_in_word_size_box = QComboBox()
        self.user_in_word_size_box.addItems(
            ['8', '12', '16', '24', '32', '48', '64', '96', '128', '192', '256', '273']
        )
        self.user_in_solid_block_size_box = QComboBox()
        self.user_in_solid_block_size_box.addItems(
            ['Non-solid', '1MB', '2MB', '4MB', '8MB', '16MB', '32MB', '64MB', '128MB', '256MB', '512MB',
             '1GB', '2GB', '4GB', '8GB', '16GB', '32GB', '64GB', 'Solid']
        )
        self.user_in_cpu_threads_box = QComboBox()
        self.user_in_cpu_threads_box.addItems(
            [str(i) for i in range(1, 41)]
        )

        self.user_in_split_to_volumes_mb = NQWidgetInput(prompt=self.lang("7z_split_to_volumes_mb"),
                                                         mode=NQWidgetInput.MODE_INT,
                                                         default_value=-1,
                                                         stretch_in_the_end=True)
        self.user_in_delete_files_after_compression_box = QCheckBox(self.lang("7z_remove_src"))
        self.compress_btn = QPushButton(self.lang("compress"))

        self.compression_level_label = QLabel(self.lang("7z_compress_level"))
        self.dictionary_size_label = QLabel(self.lang("7z_dictionary_size"))
        self.word_size_label = QLabel(self.lang("7z_word_size"))
        self.solid_block_size_label = QLabel(self.lang("7z_solid_block_size"))
        self.cpu_threads_label = QLabel(self.lang("7z_cpu_threads") % multiprocessing.cpu_count())
        self.memory_usage_label = QLabel(self.lang("7z_memory_usage"))

        super().__init__()

        self.setLayout(self.layout)

        if not disable_source_url:
            self.layout.addWidget(self.user_in_source_url)
        if not disable_out_url:
            self.layout.addWidget(self.user_in_out_7z_dir)
            self.layout.addWidget(self.user_in_out_7z_filename)
        self.layout.addWidget(self.user_in_split_to_volumes_mb)
        self.layout.addWidget(self.compression_level_label)
        self.layout.addWidget(self.user_in_compression_level_box)
        self.layout.addWidget(self.dictionary_size_label)
        self.layout.addWidget(self.user_in_dictionary_size_box)
        self.layout.addWidget(self.word_size_label)
        self.layout.addWidget(self.user_in_word_size_box)
        self.layout.addWidget(self.solid_block_size_label)
        self.layout.addWidget(self.user_in_solid_block_size_box)
        self.layout.addWidget(self.cpu_threads_label)
        self.layout.addWidget(self.user_in_cpu_threads_box)
        if not disable_delete_src:
            self.layout.addWidget(self.user_in_delete_files_after_compression_box)
        if not disable_compress_btn:
            self.layout.addWidget(self.compress_btn)

        self.set_default_values()

    def connect_signals(self):
        self.user_in_compression_level_box.currentIndexChanged.connect(self.slot_compression_level_changed)
        self.compress_btn.clicked.connect(self.slot_compress_btn_clicked)

    def set_default_values(self):
        self.user_in_compression_level_box.setCurrentText("5 - Normal")
        self.user_in_cpu_threads_box.setCurrentText(str(multiprocessing.cpu_count()))

    def disable_compress_params(self):
        self.user_in_dictionary_size_box.setEnabled(False)
        self.user_in_word_size_box.setEnabled(False)
        self.user_in_solid_block_size_box.setEnabled(False)
        self.user_in_dictionary_size_box.setCurrentIndex(-1)
        self.user_in_word_size_box.setCurrentIndex(-1)
        self.user_in_solid_block_size_box.setCurrentIndex(-1)

    def enable_compress_params(self):
        self.user_in_dictionary_size_box.setEnabled(True)
        self.user_in_word_size_box.setEnabled(True)
        self.user_in_solid_block_size_box.setEnabled(True)
        self.user_in_dictionary_size_box.setCurrentIndex(-1)
        self.user_in_word_size_box.setCurrentIndex(-1)
        self.user_in_solid_block_size_box.setCurrentIndex(-1)

    def extract_all_params_to_dict(self):
        params_dict = {
            "source_url": self.user_in_source_url.get_url(),
            "out_7z_dir": self.user_in_out_7z_dir.get_url(),
            "out_7z_filename": self.user_in_out_7z_filename.get_value(),
            "compression_level": self.user_in_compression_level_box.currentText(),
            "dictionary_size": self.user_in_dictionary_size_box.currentText(),
            "word_size": self.user_in_word_size_box.currentText(),
            "solid_block_size": self.user_in_solid_block_size_box.currentText(),
            "cpu_threads": self.user_in_cpu_threads_box.currentText(),
            "split_to_volumes_mb": self.user_in_split_to_volumes_mb.get_value(),
            "delete_files_after_compression": self.user_in_delete_files_after_compression_box.isChecked(),
        }
        return params_dict

    def restore_all_params_from_dict(self, params_dict):
        self.user_in_source_url.set_url(params_dict["source_url"])
        self.user_in_out_7z_dir.set_url(params_dict["out_7z_dir"])
        self.user_in_out_7z_filename.set_value(params_dict["out_7z_filename"])
        self.user_in_compression_level_box.setCurrentText(params_dict["compression_level"])
        self.user_in_dictionary_size_box.setCurrentText(params_dict["dictionary_size"])
        self.user_in_word_size_box.setCurrentText(params_dict["word_size"])
        self.user_in_solid_block_size_box.setCurrentText(params_dict["solid_block_size"])
        self.user_in_cpu_threads_box.setCurrentText(params_dict["cpu_threads"])
        self.user_in_split_to_volumes_mb.set_value(params_dict["split_to_volumes_mb"])
        self.user_in_delete_files_after_compression_box.setChecked(params_dict["delete_files_after_compression"])

    def slot_compress_btn_clicked(self):
        self.slot_compress.emit(self.generate_7z_command_list())

    def slot_compression_level_changed(self):
        compression_level = self.user_in_compression_level_box.currentText()

        if compression_level.startswith("0"):
            self.disable_compress_params()
        elif compression_level.startswith("1"):
            self.enable_compress_params()
            self.user_in_dictionary_size_box.setCurrentText("256KB")
            self.user_in_word_size_box.setCurrentText("32")
            self.user_in_solid_block_size_box.setCurrentText("Solid")
        elif compression_level.startswith("3"):
            self.enable_compress_params()
            self.user_in_dictionary_size_box.setCurrentText("4MB")
            self.user_in_word_size_box.setCurrentText("32")
            self.user_in_solid_block_size_box.setCurrentText("Solid")
        elif compression_level.startswith("5"):
            self.enable_compress_params()
            self.user_in_dictionary_size_box.setCurrentText("16MB")
            self.user_in_word_size_box.setCurrentText("32")
            self.user_in_solid_block_size_box.setCurrentText("Solid")
        elif compression_level.startswith("7"):
            self.enable_compress_params()
            self.user_in_dictionary_size_box.setCurrentText("32MB")
            self.user_in_word_size_box.setCurrentText("64")
            self.user_in_solid_block_size_box.setCurrentText("Solid")
        elif compression_level.startswith("9"):
            self.enable_compress_params()
            self.user_in_dictionary_size_box.setCurrentText("64MB")
            self.user_in_word_size_box.setCurrentText("64")
            self.user_in_solid_block_size_box.setCurrentText("Solid")
        else:
            eprint(f"Unknown compression level {compression_level}")

    def generate_7z_command_list(self):
        gui_settings = self.extract_all_params_to_dict()

        # Extract the values from the gui_settings dictionary
        source_url = gui_settings['source_url']
        out_7z_dir = gui_settings['out_7z_dir']
        out_7z_filename = gui_settings['out_7z_filename']
        compression_level = gui_settings['compression_level'][0]  # Extract the numeric part from '5 - Normal', etc.
        dictionary_size = gui_settings['dictionary_size'].replace("GB", "g").replace("MB", "m").replace("KB", "k")
        word_size = gui_settings['word_size']
        solid_block_size = gui_settings['solid_block_size'].replace("GB", "g").replace("MB", "m").replace("KB", "k")
        cpu_threads = gui_settings['cpu_threads']
        split_to_volumes_mb = gui_settings['split_to_volumes_mb']
        delete_files_after_compression = '-sdel' if gui_settings['delete_files_after_compression'] else ''

        # If solid_block_size is 'Solid' or 'Non-solid', set it to special command
        if solid_block_size.lower() == 'solid':
            solid_block_size = 'on'
        elif solid_block_size.lower() == 'non-solid':
            solid_block_size = 'off'

        command = [
            "a",
            "-t7z",  # output type is 7z
            "-m0=lzma2",  # lzma2 method
            f"-mx={compression_level}",  # compression level
            f"-ms={solid_block_size}" if solid_block_size else "",  # solid block size
            f"-md={dictionary_size}" if dictionary_size else "",  # dictionary size
            f"-mfb={word_size}" if word_size else "",  # word size
            f"-mmt={cpu_threads}",  # threads
            delete_files_after_compression,  # delete files after compression
            "-v{}m".format(split_to_volumes_mb) if int(split_to_volumes_mb) > 0 else "",  # volume size
            os.path.join(out_7z_dir, out_7z_filename) if not self.disable_out_url else self.COMP_7Z_URL,
            source_url if not self.disable_source_url else self.COMP_SRC,  # what to compress
        ]

        # filter out empty elements
        command = [c for c in command if c]

        return command
