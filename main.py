from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys
from ai_tools import CreateLLMSession, translate
from ai_tools.config import MISTRAL_API_KEY

model_config = {
    "API_KEY": MISTRAL_API_KEY,
    "model_name": "mistral",
}

#МЕСТО ДЛЯ СЛОВАРЕЙ/ЯЗЫКОВ


class Thread_Summarizator(QThread):
    signal = pyqtSignal(list)
    def __init__(self, selected_text: str, llm_session: CreateLLMSession):
        self.selected_text = selected_text
        self.llm_session = llm_session
        super(Thread_Summarizator, self).__init__()

    def run(self):
        summary = self.llm_session.summarize(self.selected_text) # Should be async!
        self.signal.emit([self.selected_text, summary])
        self.quit()


class Thread_Paraphrase(QThread):
    signal = pyqtSignal(list)
    def __init__(self, selected_text: str, llm_session: CreateLLMSession):
        self.selected_text = selected_text
        self.llm_session = llm_session
        super(Thread_Paraphrase, self).__init__()

    def run(self):
        summary = self.llm_session.paraphrase(self.selected_text) # Should be async!
        self.signal.emit([self.selected_text, summary])
        self.quit()


class Thread_Transtator(QThread):
    signal = pyqtSignal(list)
    def __init__(self, selected_text: str):
        self.selected_text = selected_text
        super(Thread_Transtator, self).__init__()

    def run(self):
        translated = ""
        for sentence in self.selected_text.split('.'):
            if sentence != '':
                translated += translate("autodetect", "ru", sentence + '.')
        self.signal.emit([self.selected_text, translated])
        self.quit()


class AminatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(AminatedButton, self).__init__(*args, **kwargs)
        self.x_shift = 0
        self.y_shift = 0
        self._animation = QPropertyAnimation(
            self, b'geometry', self, duration=200)

    def set_shift(self, x_shift: int, y_shift: int):
        self.x_shift = x_shift
        self.y_shift = y_shift
    
    def updatePos(self):
        #фиксированное значение геометрии
        self._geometry = self.geometry()
        self._rect = QRect(
            self._geometry.x() - self.x_shift,
            self._geometry.y() - self.y_shift,
            self._geometry.width(),
            self._geometry.height()
        )

    def showEvent(self, event):
        super(AminatedButton, self).showEvent(event)
        self.updatePos()

    def enterEvent(self, event):
        super(AminatedButton, self).enterEvent(event)
        self._animation.stop()
        self._animation.setStartValue(self._geometry)
        self._animation.setEndValue(self._rect)
        self._animation.start()

    def leaveEvent(self, event):
        super(AminatedButton, self).leaveEvent(event)
        self._animation.stop()               
        self._animation.setStartValue(self._rect)
        self._animation.setEndValue(self._geometry)
        self._animation.start()

    def mousePressEvent(self, event):
        self._animation.stop()  
        self._animation.setStartValue(self._geometry)
        self._animation.setEndValue(self._rect)
        self._animation.start()
        super(AminatedButton, self).mousePressEvent(event)


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        AppLang = QComboBox()
        AppLang.addItems(["English", "Russian"])
        TransLang = QComboBox()
        TransLang.addItems(["English", "Russian"])
        self.SettingsLayout = QVBoxLayout()
        self.SettingsLayout.addWidget(QLabel("App Language"))
        self.SettingsLayout.addWidget(AppLang)
        self.SettingsLayout.addWidget(QLabel("Translation Language"))
        self.SettingsLayout.addWidget(TransLang)
        self.textbox = QLineEdit(placeholderText="APIKEY?")
        self.SettingsLayout.addWidget(QLabel("API key for MistralAI"))
        self.textbox.setText(MISTRAL_API_KEY)
        self.SettingsLayout.addWidget(self.textbox)
        self.setWindowTitle("Settings")
        self.setStyleSheet("background-color: #262627; color: #FFFFFF")
        self.setGeometry(170, 600, 200, 50)
        self.setLayout(self.SettingsLayout)
        self.show()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(100, 100, 1000, 600)

        self.setStyleSheet("background-color: #262627; color: #FFFFFF")
        
        self.editor = QPlainTextEdit()
        self.editor.setStyleSheet("background-color: #1e1e1f; color: #FFFFFF; border-radius: 5%;") 

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        self.path = None
        self.is_file_manager_opened = False
        self.current_dir = QDir.currentPath()

        # FILE MENU
        file_menu = self.menuBar().addMenu("&File")
        file_menu.setStyleSheet("color: #FFFFFF;")
        self.menuBar().setStyleSheet("color: #FFFFFF;")

        open_file_action = QAction("Open file", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)

        save_file_action = QAction("Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)

        saveas_file_action = QAction("Save As", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)

        print_action = QAction("Print", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action) 
    
        # EDIT MENU
        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.setStyleSheet("color: #FFFFFF;")
        
        undo_action = QAction("Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
    
        redo_action = QAction("Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
    
        cut_action = QAction("Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.cut)
        edit_menu.addAction(cut_action)
    
        copy_action = QAction("Copy", self)
        copy_action.setStatusTip("Copy selected text")
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)
    
        paste_action = QAction("Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)

        select_action = QAction("Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        
        # AI TOOLS
        ai_tools_menu = self.menuBar().addMenu("AI Tools")
        ai_tools_menu.setStyleSheet("color: #FFFFFF;")
        
        summarize_action = QAction("Summarise", self)
        summarize_action.setStatusTip("Summarise selected")
        summarize_action.triggered.connect(self.summarise)
        ai_tools_menu.addAction(summarize_action)

        translate_action = QAction("Translate", self)
        translate_action.setStatusTip("Translate selected")
        translate_action.triggered.connect(self.translate)
        ai_tools_menu.addAction(translate_action)

        parahrase_action = QAction("Paraphrase", self)
        parahrase_action.setStatusTip("Paraphrase selected")
        parahrase_action.triggered.connect(self.paraphrase)
        ai_tools_menu.addAction(parahrase_action)

        # wrap action
        wrap_action = QAction("Wrap text to window", self)
        wrap_action.setStatusTip("Check to wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        self.update_title()
        # right mouse button menu

        self.editor.setContextMenuPolicy(Qt.ActionsContextMenu)
        context_copy_ation = QAction("Copy", self)
        context_copy_ation.triggered.connect(self.editor.copy)
        self.editor.addAction(context_copy_ation)

        context_paste_ation = QAction("Paste", self)
        context_paste_ation.triggered.connect(self.editor.paste)
        self.editor.addAction(context_paste_ation)

        context_summarise_ation = QAction("Summarise", self)
        context_summarise_ation.triggered.connect(self.summarise)
        self.editor.addAction(context_summarise_ation)

        context_translate_ation = QAction("Translate", self)
        context_translate_ation.triggered.connect(self.translate)
        self.editor.addAction(context_translate_ation)

        context_paraphrase_ation = QAction("Paraphrase", self)
        context_paraphrase_ation.triggered.connect(self.paraphrase)
        self.editor.addAction(context_paraphrase_ation)

        # LEFT PANEL
        self.icons_path = 'assets/Icons/'
        
        self.btn_file_manager = AminatedButton('', self)
        self.btn_search = AminatedButton('', self)
        self.btn_time = AminatedButton('', self)
        self.btn_calendar = AminatedButton('', self)
        self.btn_inf = AminatedButton('', self)
        self.btn_settings = AminatedButton('', self)
        
        self.buttons_css = "color: #FFFFFF; border: none"
        self.btn_file_manager.setStyleSheet(self.buttons_css)
        self.btn_search.setStyleSheet(self.buttons_css)
        self.btn_time.setStyleSheet(self.buttons_css)
        self.btn_calendar.setStyleSheet(self.buttons_css)
        self.btn_inf.setStyleSheet(self.buttons_css)
        self.btn_settings.setStyleSheet(self.buttons_css)

        self.btn_file_manager.set_shift(8, 0)
        self.btn_search.set_shift(8, 0)
        self.btn_time.set_shift(8, 0)
        self.btn_calendar.set_shift(8, 0)
        self.btn_inf.set_shift(8, 0)
        self.btn_settings.set_shift(8, 0)

        self.btn_file_manager.setIcon(QIcon(self.icons_path  + 'Circle_arrow.png'))
        self.btn_search.setIcon(QIcon(self.icons_path  + 'Search.png'))
        self.btn_time.setIcon(QIcon(self.icons_path  + 'Clock.png'))
        self.btn_calendar.setIcon(QIcon(self.icons_path  + 'Calendar.png'))
        self.btn_inf.setIcon(QIcon(self.icons_path  + 'Info.png'))
        self.btn_settings.setIcon(QIcon(self.icons_path  + 'Settings.png'))

        self.btn_file_manager.setIconSize(QSize(80, 80))
        self.btn_search.setIconSize(QSize(80, 80))
        self.btn_time.setIconSize(QSize(80, 80))
        self.btn_calendar.setIconSize(QSize(80, 80))
        self.btn_inf.setIconSize(QSize(80, 80))
        self.btn_settings.setIconSize(QSize(80, 80))

        self.btn_file_manager.setFixedSize(QSize(40, 40))
        self.btn_search.setFixedSize(QSize(40, 40))
        self.btn_time.setFixedSize(QSize(40, 40))
        self.btn_calendar.setFixedSize(QSize(40, 40))
        self.btn_inf.setFixedSize(QSize(40, 40))
        self.btn_settings.setFixedSize(QSize(40, 40))

        self.btn_file_manager.pressed.connect(self.open_file_manager)
        self.btn_inf.pressed.connect(self.show_info)
        self.btn_settings.pressed.connect(self.settings_win)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(30)
        left_layout.addWidget(self.btn_file_manager)
        left_layout.addWidget(self.btn_search)
        left_layout.addWidget(self.btn_time)
        left_layout.addWidget(self.btn_calendar)
        left_layout.addStretch(50)
        left_layout.addWidget(self.btn_inf)
        left_layout.addWidget(self.btn_settings)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        self.left_widget = left_widget

        # showing all the components
        self.main_layout = QHBoxLayout()

        self.main_layout.addWidget(left_widget)
        self.main_layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        self.show()

        self.llm_session = CreateLLMSession(model_config)


    def generate_file_manager(self):
        # File manager
        file_manager = QWidget()
        files_layout = QVBoxLayout()

        files_up_panel_layout = QHBoxLayout()
        files_manager_layout = QVBoxLayout()
        files_down_layout = QHBoxLayout()

        files_up_panel_layout.setContentsMargins(0, 0, 0, 0)
        files_down_layout.setContentsMargins(0, 0, 0, 0)

        # files_up_panel
        self.btn_translator = AminatedButton('', self)
        self.btn_chat = AminatedButton('', self)
        self.btn_book = AminatedButton('', self)
        self.btn_statistic = AminatedButton('', self)
        self.btn_tasks = AminatedButton('', self)
        self.btn_list = AminatedButton('', self)
        self.btn_up_dir = AminatedButton('', self)
        
        self.btn_translator.setStyleSheet(self.buttons_css)
        self.btn_chat.setStyleSheet(self.buttons_css)
        self.btn_book.setStyleSheet(self.buttons_css)
        self.btn_statistic.setStyleSheet(self.buttons_css)
        self.btn_tasks.setStyleSheet(self.buttons_css)
        self.btn_list.setStyleSheet(self.buttons_css)
        self.btn_up_dir.setStyleSheet(self.buttons_css)

        self.btn_translator.set_shift(0, 5)
        self.btn_chat.set_shift(0, 5)
        self.btn_book.set_shift(0, 5)
        self.btn_statistic.set_shift(0, 5)
        self.btn_tasks.set_shift(0, 5)
        self.btn_list.set_shift(0, 5)
        self.btn_up_dir.set_shift(0, 3)

        self.btn_translator.setIcon(QIcon(self.icons_path  + 'g_translate.png'))
        self.btn_chat.setIcon(QIcon(self.icons_path  + 'chat_bubble.png'))
        self.btn_book.setIcon(QIcon(self.icons_path  + 'Book.png'))
        self.btn_statistic.setIcon(QIcon(self.icons_path  + 'Trending up.png'))
        self.btn_tasks.setIcon(QIcon(self.icons_path  + 'Check square.png'))
        self.btn_list.setIcon(QIcon(self.icons_path  + 'List.png'))
        self.btn_up_dir.setIcon(QIcon(self.icons_path  + 'up_circle_arrow.png'))

        self.btn_translator.setIconSize(QSize(80, 80))
        self.btn_chat.setIconSize(QSize(80, 80))
        self.btn_book.setIconSize(QSize(80, 80))
        self.btn_statistic.setIconSize(QSize(80, 80))
        self.btn_tasks.setIconSize(QSize(80, 80))
        self.btn_list.setIconSize(QSize(80, 80))
        self.btn_up_dir.setIconSize(QSize(35, 35))

        self.btn_translator.setFixedSize(QSize(40, 40))
        self.btn_chat.setFixedSize(QSize(40, 40))
        self.btn_book.setFixedSize(QSize(40, 40))
        self.btn_statistic.setFixedSize(QSize(40, 40))
        self.btn_tasks.setFixedSize(QSize(40, 40))
        self.btn_list.setFixedSize(QSize(40, 40))
        self.btn_up_dir.setFixedSize(QSize(35, 35))

        files_up_panel_layout.addWidget(self.btn_up_dir)
        files_up_panel_layout.addWidget(self.btn_translator)
        #files_up_panel_layout.addWidget(self.btn_chat)
        files_up_panel_layout.addWidget(self.btn_book)
        files_up_panel_layout.addWidget(self.btn_statistic)
        files_up_panel_layout.addWidget(self.btn_tasks)
        #files_up_panel_layout.addWidget(self.btn_list)
        
        self.btn_translator.pressed.connect(self.translate)
        self.btn_up_dir.pressed.connect(self.file_manager_up_dir)

        # File manager
        self.file_manager_model = QFileSystemModel()
        self.file_manager_model.setRootPath(self.current_dir)

        self.file_manager_tree = QTreeView()
        self.file_manager_tree.setModel(self.file_manager_model)
        self.file_manager_tree.setRootIndex(self.file_manager_model.index(self.current_dir))
        self.file_manager_tree.doubleClicked.connect(self.file_manager_on_double_clicked)
        self.file_manager_tree.setAnimated(False)
        self.file_manager_tree.setIndentation(20)
        self.file_manager_tree.setSortingEnabled(True)
        self.file_manager_tree.setStyleSheet(self.buttons_css)

        # files_down_layout
        self.btn_mic = AminatedButton('', self)
        self.btn_photo = AminatedButton('', self)
        self.btn_attach_file = AminatedButton('', self)
        self.btn_Youtube = AminatedButton('', self)
        
        self.btn_mic.setStyleSheet(self.buttons_css)
        self.btn_photo.setStyleSheet(self.buttons_css)
        self.btn_attach_file.setStyleSheet(self.buttons_css)
        self.btn_Youtube.setStyleSheet(self.buttons_css)

        self.btn_mic.set_shift(0, 5)
        self.btn_photo.set_shift(0, 5)
        self.btn_attach_file.set_shift(0, 5)
        self.btn_Youtube.set_shift(0, 5)

        self.btn_mic.setIcon(QIcon(self.icons_path  + 'mic.png'))
        self.btn_photo.setIcon(QIcon(self.icons_path  + 'photo.png'))
        self.btn_attach_file.setIcon(QIcon(self.icons_path  + 'attach_file.png'))
        self.btn_Youtube.setIcon(QIcon(self.icons_path  + 'Youtube.png'))

        self.btn_mic.setIconSize(QSize(80, 80))
        self.btn_photo.setIconSize(QSize(80, 80))
        self.btn_attach_file.setIconSize(QSize(80, 80))
        self.btn_Youtube.setIconSize(QSize(80, 80))

        self.btn_mic.setFixedSize(QSize(40, 40))
        self.btn_photo.setFixedSize(QSize(40, 40))
        self.btn_attach_file.setFixedSize(QSize(40, 40))
        self.btn_Youtube.setFixedSize(QSize(40, 40))

        files_down_layout.addWidget(self.btn_mic)
        files_down_layout.addWidget(self.btn_photo)
        files_down_layout.addWidget(self.btn_attach_file)
        files_down_layout.addWidget(self.btn_Youtube)

        files_up_panel = QWidget()
        files_up_panel.setLayout(files_up_panel_layout)
        files_down = QWidget()
        files_down.setLayout(files_down_layout)

        files_layout.addWidget(files_up_panel)
        #files_layout.addStretch(1000)
        files_layout.addWidget(self.file_manager_tree)
        files_layout.addWidget(files_down)
        file_manager.setLayout(files_layout)

        return file_manager

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", 
                            "Text documents (*.txt);;All files (*.*)")
        if path:
            try:
                with open(path, 'r+') as f:
                    text = f.read()
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    def file_save(self):
        if self.path is None:
            return self.file_saveas()
        self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);; All files (*.*)")
        if not path:
            return
        self._save_to_path(path)

    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - ConspectPRO" %(os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0 )
    
    def open_file_manager(self):
        container = QWidget()
        right_container = QWidget()
        main_layout = QSplitter()
        right_layout = QHBoxLayout()

        if not self.is_file_manager_opened:
            self.file_manager = self.generate_file_manager()
            self.file_manager.setMaximumWidth(420)
            self.file_manager.setMinimumWidth(220)
            main_layout.addWidget(self.file_manager)
            self.btn_file_manager.setIcon(QIcon(self.icons_path  + 'Circle_arrow_down.png'))

            self.file_manager_effect = QGraphicsOpacityEffect(self.file_manager)
            self.file_manager.setGraphicsEffect(self.file_manager_effect)
            self.anim = QPropertyAnimation(self.file_manager, b"pos")
            self.anim.setStartValue(QPoint(-500, 0))
            self.anim.setEndValue(QPoint(0, 0))
            self.anim.setDuration(300)
            self.anim_2 = QPropertyAnimation(self.file_manager_effect, b"opacity")
            self.anim_2.setStartValue(0)
            self.anim_2.setEndValue(1)
            self.anim_2.setDuration(300)
            self.anim_group = QParallelAnimationGroup()
            self.anim_group.addAnimation(self.anim)
            self.anim_group.addAnimation(self.anim_2)
            self.anim_group.start()
        else:
            self.btn_file_manager.setIcon(QIcon(self.icons_path  + 'Circle_arrow.png'))

        right_layout.addWidget(self.left_widget)
        right_layout.addWidget(self.editor)
        right_container.setLayout(right_layout)
        main_layout.addWidget(right_container)
        self.setCentralWidget(main_layout)

        self.is_file_manager_opened = not(self.is_file_manager_opened)

    def get_selected_text(self):
        return self.editor.toPlainText()[self.editor.textCursor().selectionStart():self.editor.textCursor().selectionEnd()]

    def summarise(self):
        self.temp_thread = Thread_Summarizator(self.get_selected_text(), self.llm_session)
        self.temp_thread.signal.connect(self.update_text)
        self.temp_thread.start()
    
    def translate(self):
        self.temp_thread_translator = Thread_Transtator(self.get_selected_text())
        self.temp_thread_translator.signal.connect(self.update_text)
        self.temp_thread_translator.start()

    def paraphrase(self):
        self.temp_thread_paraphasor = Thread_Paraphrase(self.get_selected_text(), self.llm_session)
        self.temp_thread_paraphasor.signal.connect(self.update_text)
        self.temp_thread_paraphasor.start()

    def update_text(self, signal):
        text = self.editor.toPlainText()
        cursor = self.editor.textCursor()
        new_pos = 0
        if cursor.position() < text.find(signal[0]): # Calculating new cursor position
            new_pos = cursor.position()
        elif cursor.position() >= text.find(signal[0]) and cursor.position() <= text.find(signal[0]) + len(signal[0]):
            new_pos = text.find(signal[0]) + len(signal[1])
        elif cursor.position() > text.find(signal[0]) + len(signal[0]):
            new_pos = cursor.position() + len(signal[1]) - len(signal[0])
        text = text.replace(signal[0], signal[1])
        self.editor.setPlainText(text)
        cursor.setPosition(new_pos)
        self.editor.setTextCursor(cursor)
    
    def show_info(self):
        msg = QMessageBox()
        msg.setWindowTitle("ConspectPRO")
        msg.setText("This is a program to work with text and conspects.")
        msg.setIconPixmap(QPixmap(self.icons_path + 'mascot.png'))
        x = msg.exec_()

    def file_manager_on_double_clicked(self, index):
        file_name = self.file_manager_model.filePath(index)
        if file_name:
            try:
                with open(file_name, 'r+') as f:
                    text = f.read()
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = file_name
                self.editor.setPlainText(text)
                self.update_title()
    
    def file_manager_up_dir(self):
        self.current_dir = self.current_dir[:self.current_dir.rfind('/')]
        self.file_manager_tree.setRootIndex(self.file_manager_model.index(self.current_dir))

    def settings_win(self):
        self.settings_win = SettingsWindow()


# drivers code
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("ConspectPRO")
    app.setWindowIcon(QIcon('assets/Icons/mascot.png'))
    window = MainWindow()
    app.exec_()
