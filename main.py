from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(100, 100, 600, 400)

        layout = QFormLayout()
        self.setStyleSheet("background-color: #262627;")
        
        self.editor = QPlainTextEdit()
        self.editor.setStyleSheet("background-color: #1e1e1f; color: #FFFFFF") 
         

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)


        self.path = None

        


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
        
        summ = QAction("Summarise", self)
        summ.setStatusTip("Save current page")
        summ.triggered.connect(self.summarise)
        ai_tools_menu.addAction(summ)

        # wrap action
        wrap_action = QAction("Wrap text to window", self)
        wrap_action.setStatusTip("Check to wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        # calling update title method
        self.update_title()

        self.editor.setContextMenuPolicy(Qt.ActionsContextMenu)
        quitAction = QAction("Summarise", self)
        quitAction.triggered.connect(self.summarise)
        self.editor.addAction(quitAction)

        icons_path = 'assets/Icons/'
        
        self.btn_file_manager = QPushButton('', self)
        self.btn_search = QPushButton('', self)
        self.btn_time = QPushButton('', self)
        self.btn_calendar = QPushButton('', self)
        self.btn_inf = QPushButton('', self)
        self.btn_settings = QPushButton('', self)
        self.btn_file_manager.setStyleSheet("color: #FFFFFF; border: none")
        self.btn_search.setStyleSheet("color: #FFFFFF; border: none")
        self.btn_time.setStyleSheet("color: #FFFFFF; border: none")
        self.btn_calendar.setStyleSheet("color: #FFFFFF; border: none")
        self.btn_inf.setStyleSheet("color: #FFFFFF; border: none")
        self.btn_settings.setStyleSheet("color: #FFFFFF; border: none")
        
        self.btn_file_manager.setIcon(QIcon(icons_path  + 'Info.png'))
        self.btn_search.setIcon(QIcon(icons_path  + 'Search.png'))
        self.btn_time.setIcon(QIcon(icons_path  + 'Clock.png'))
        self.btn_calendar.setIcon(QIcon(icons_path  + 'Calendar.png'))
        self.btn_inf.setIcon(QIcon(icons_path  + 'Info.png'))
        self.btn_settings.setIcon(QIcon(icons_path  + 'Settings.png'))

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_file_manager)
        left_layout.addWidget(self.btn_search)
        left_layout.addWidget(self.btn_time)
        left_layout.addWidget(self.btn_calendar)
        left_layout.addWidget(self.btn_inf)
        left_layout.addWidget(self.btn_settings)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)


        # showing all the components

        layout.addRow(left_widget, self.editor) 

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.show()


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
                with open(path, 'rU') as f:
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

    def summarise(self):
        print(self.editor.textCursor().selectedText())


# drivers code
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("ConspectPRO")
    window = MainWindow()
    app.exec_()
