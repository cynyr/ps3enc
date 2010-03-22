#!/usr/bin/env python
# quitbutton.py

import sys
from PyQt4 import QtGui, QtCore


class QuitButton(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Icon')

        quit = QtGui.QPushButton('Close', self)
        quit.setGeometry(10, 10, 60, 35)

        self.connect(quit, QtCore.SIGNAL('clicked()'),
            QtGui.qApp, QtCore.SLOT('quit()'))

# messagebox.py

class MessageBox(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('message box')


    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


#status bar

class StatusBar(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(250, 150)
        self.setWindowTitle('statusbar')

        self.statusBar().showMessage('Not Ready')

class MenuBar(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(250, 150)
        self.setWindowTitle('menubar')

        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        self.statusBar().showMessage("Try out the menu")

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(350, 250)
        self.setWindowTitle('mainwindow')

        textEdit = QtGui.QTextEdit()
        self.setCentralWidget(textEdit)

        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        self.statusBar()

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit)


class BoxLayout(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle('box layout')

        ok = QtGui.QPushButton("OK")
        cancel = QtGui.QPushButton("Cancel")

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.resize(300, 150)

class GridLayout(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle('grid layout')

        names = ['Cls', 'Bck', '', 'Close', '7', '8', '9', '/',
            '4', '5', '6', '*', '1', '2', '3', '-',
            '0', '.', '=', '+']

        grid = QtGui.QGridLayout()

        j = 0
        pos = [(0, 0), (0, 1), (0, 2), (0, 3),
                (1, 0), (1, 1), (1, 2), (1, 3),
                (2, 0), (2, 1), (2, 2), (2, 3),
                (3, 0), (3, 1), (3, 2), (3, 3 ),
                (4, 0), (4, 1), (4, 2), (4, 3)]

        for i in names:
            button = QtGui.QPushButton(i)
            if j == 2:
                grid.addWidget(QtGui.QLabel(''), 0, 2)
            else: grid.addWidget(button, pos[j][0], pos[j][1])
            j = j + 1

        self.setLayout(grid)


class SigSlot(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle('signal & slot')

        lcd = QtGui.QLCDNumber(self)
        slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(slider)

        self.setLayout(vbox)
        self.connect(slider,  QtCore.SIGNAL('valueChanged(int)'), lcd, 
		QtCore.SLOT('display(int)') )

        self.resize(250, 150)

class InputDialog(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 350, 80)
        self.setWindowTitle('InputDialog')

        self.button = QtGui.QPushButton('Dialog', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)

        self.button.move(20, 20)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.showDialog)
        self.setFocus()

        self.label = QtGui.QLineEdit(self)
        self.label.move(130, 22)


    def showDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        if ok:
            self.label.setText(unicode(text))

class OpenFile(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('OpenFile')

        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()
        self.setFocus()

        exit = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        exit.setShortcut('Ctrl+O')
        exit.setStatusTip('Open new File')
        self.connect(exit, QtCore.SIGNAL('triggered()'), self.showDialog)

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)

    def showDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                    '/home')
        if filename != '':
            file=open(filename)
            data = file.read()
            self.textEdit.setText(data)
            file.close()
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class CheckBox(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Checkbox')

        self.cb = QtGui.QCheckBox('Show title', self)
        self.cb.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cb.move(10, 10)
        self.cb.toggle()
        self.connect(self.cb, QtCore.SIGNAL('stateChanged(int)'), self.changeTitle)

    def changeTitle(self, value):
        if self.cb.isChecked():
            self.setWindowTitle('Checkbox')
        else:
            self.setWindowTitle(' ')

class ProgressBar(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('ProgressBar')

        self.pbar = QtGui.QProgressBar()
        self.pbar.setGeometry(30, 40, 200, 25)

        self.button = QtGui.QPushButton('Start')
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(40, 80)

        self.reset = QtGui.QPushButton("restart")
        self.reset.setFocusPolicy(QtCore.Qt.NoFocus)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.button)
        hbox.addWidget(self.reset)
        vbox.addWidget(self.pbar)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.onStart)
        self.connect(self.reset, QtCore.SIGNAL('clicked()'), self.resetProgress)

        self.timer = QtCore.QBasicTimer()
        self.step = 0


    def resetProgress(self):
        self.step = 0
        self.pbar.setValue(self.step)

    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            return
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def onStart(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText('Start')
        else:
            self.timer.start(100, self)
            self.button.setText('Stop')


app = QtGui.QApplication(sys.argv)
qb = ProgressBar()
#qb = CheckBox()
#qb = OpenFile()
#qb = InputDialog()
#qb = SigSlot()
#qb = MessageBox()
#qb = MainWindow()
#qb = BoxLayout()
#qb = GridLayout()
#qb = MenuBar()
#qb = QuitButton()
qb.show()
sys.exit(app.exec_())
