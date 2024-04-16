"""!
@file
@brief Основной функционал и пользовательский интерфейс

В этом файле написан основной функционал работы с пользовательским интерфейсом, включая основное окно, дополнительные окна(к примеру окно создания проекта), а также вкладки для конкретного проекта. Также в файле находятся подключения всех необходимыч библиотек, а также создания проекта openFoam с необходимыми файлами.
"""

import os
import sys
import shutil
import psutil
import tempfile
import numpy as np
from decimal import Decimal
from stl import mesh
from subprocess import *
from functools import partial
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from Tab import *
from MainWindow import *
from ViewModel import *
from BlockMeshDict import *
from ControlDict import *
from Constant import *
from BeginValues import *
from fvObjects import *
from SnappyHexMeshDict import *


class MyMainWindow(QMainWindow):
    """!
    @brief Класс основного окна приложения

    Этот класс основного окна приложения, в который будут добавлятся вкладки с проектами, в которых будут задавться параметры, фигуры и генерироваться модель. Также здесь создаётся меню("Файл", "Инструменты", "Справка") в верхней части окна, для общего взаимодействия.
    """

    def __init__(self):
        """!
        @brief Конструктор класса.

        В конструкторе классе инициализируется дополнительные окна, меню, а также подключение сигналов виджетов и слотов для их обработки.
        """

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.tabWidget.removeTab(0)

        self.ui.actionOpenProject.triggered.connect(self.openProj)
        self.ui.actionCreateProject.triggered.connect(self.newProj)
        self.ui.actionQuit.triggered.connect(QApplication.quit)
        self.ui.actionOpenProjFolder.triggered.connect(self.openFolder)
        self.ui.actionSaveChangesProject.triggered.connect(self.saveChangesProject)
        self.ui.actionConsole.setChecked(False)
        self.ui.actionConsole.triggered.connect(self.toggleConsole)
        self.ui.actionEditfvSchemes.triggered.connect(self.showWindowChangeFvObject)
        self.ui.actionEditfvSolution.triggered.connect(self.showWindowChangeFvObject)
        self.ui.actionResiduals.triggered.connect(self.showWindowResiduals)
        self.ui.actionParaView.triggered.connect(self.runParaView)

        self.newProjDialog = QDialog(self)
        self.newProjDialog.setWindowFlags(self.newProjDialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.initDialog()

        self.widgetFAO = QWidget()
        self.initFAO()
        self.ui.actionFAO.triggered.connect(self.widgetFAO.show)

        self.ui.tabWidget.tabCloseRequested.connect(self.removeProj)
        self.ui.tabWidget.currentChanged.connect(self.changedCurrentTab)

    def runParaView(self):
        if self.ui.tabWidget.currentWidget() != None:
            self.ui.tabWidget.currentWidget().runParaView()

    def showWindowResiduals(self):
        """!
        @brief Метод, который отображает окно с графиками точности решения.

        Метод, который отображает окно с графиками точности решения.
        """

        if self.ui.tabWidget.currentWidget() != None:
            self.ui.tabWidget.currentWidget().showWindowResiduals()

    def showWindowChangeFvObject(self):
        """!
        @brief Метод, который отображает окно изменения fvObjects.

        Метод, который отображает окно изменения fvObjects.
        """

        if self.ui.tabWidget.currentWidget() != None:
            if(self.sender().text() == "Файл fvSchemes"):
                self.ui.tabWidget.currentWidget().showFvWindow("fvSchemes")
            elif(self.sender().text() == "Файл fvSolution"):
                self.ui.tabWidget.currentWidget().showFvWindow("fvSolution")

    def changedCurrentTab(self):
        """!
        @brief Метод, который вызывается при изменении выбора текущего проекта.

        Метод, который вызывается при изменении выбора текущего проекта.
        """

        if self.ui.tabWidget.currentWidget() != None:
            self.ui.actionConsole.setChecked(self.ui.tabWidget.currentWidget().currentToggleConsole())

    def toggleConsole(self, chaked):
        """!
        @brief Метод, который вызывается при нажатии на кнопку в меню ("Вид" -> "Консоль").

        Метод, который вызывается при нажатии на кнопку в меню ("Вид" -> "Консоль").
        @param chaked (bool) - вкл/выкл консоли для конкретного проекта
        """

        if self.ui.tabWidget.currentWidget() != None:
            self.ui.tabWidget.currentWidget().toggleConsole(chaked)

    def initFAO(self):
        """!
        @brief Метод инициализация окна "О программе".

        В этом методе задется краткое описание о программе.
        """

        self.widgetFAO.setWindowTitle("О программе")
        self.widgetFAO.setWindowIcon(QIcon("icons/1.png"))
        widgetLayout = QVBoxLayout()
        label = QLabel("Программа для автоматизации рещений задач в openFoam\n\nАвтор: Венгелевский Максим\nEmail: maksimuchhka@list.ru")
        fontLabel = QFont("Times", 9)
        label.setFont(fontLabel)
        widgetLayout.addWidget(label)
        self.widgetFAO.setLayout(widgetLayout)

    def saveChangesProject(self):
        """!
        @brief Метод сохранения изменений.

        Метод вызова функции сохранения изменений у объекта Project
        """

        if self.ui.tabWidget.currentWidget() != None:
            self.ui.tabWidget.currentWidget().saveChanges()

    def openFolder(self):
        """!
        @brief Метод открытия папки проекта в проводнике.

        Метод, который открывает папку в проводнике при нажатии на кнопку в меню ("Инструменты -> Открыть папку в проводнике").
        """

        if self.ui.tabWidget.currentWidget() != None:
            Popen(f"explorer {self.ui.tabWidget.currentWidget().pathProj}")

    def initDialog(self):
        """!
        @brief Метод инициализация окна создания нового проекта.

        В этом методе задаются основные настройки и свойства модального окна создания нового проекта.
        """

        autoPathEnv = "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\ESI-OpenCFD\\OpenFOAM\\"
        autoPathProj = ""
        if not os.path.exists(autoPathEnv):
            autoPathEnv = "C:\\Program Files\\ESI-OpenCFD\\OpenFOAM\\"
        for val in os.listdir(autoPathEnv):
            if os.path.isdir(autoPathEnv + val) and val.startswith("v"):
                autoPathEnv += val + "\\"
                autoPathProj = autoPathEnv
                break
        if autoPathProj == "":
            autoPathEnv = "C:\\Program Files\\ESI-OpenCFD\\OpenFOAM\\"
            for val in os.listdir(autoPathEnv):
                if os.path.isdir(autoPathEnv + val) and val.startswith("v"):
                    autoPathEnv += val + "\\"
                    autoPathProj = autoPathEnv
                    break
        for val in os.listdir(autoPathEnv):
            if os.path.isfile(autoPathEnv + val) and val.startswith("setEnvVariables") and val.endswith(".bat"):
                autoPathEnv += val
                break
        if not autoPathEnv.endswith(".bat"):
            autoPathEnv = ""

        self.newProjDialog.setWindowTitle("Создание проекта")
        self.newProjDialog.resize(400, 100)
        widgetLayout = QVBoxLayout()

        frame1 = QFrame(self.newProjDialog)
        frame1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layoutFrame1 = QGridLayout()

        layoutFrame1.addWidget(QLabel("Название проекта:"), 0, 0)
        self.nameProj = QLineEdit()
        self.nameProj.setPlaceholderText("Название проекта")
        layoutFrame1.addWidget(self.nameProj, 0, 1, 1, 2)

        layoutFrame1.addWidget(QLabel("Путь к проекту:"), 1, 0)
        self.pathProj = QLineEdit()
        self.pathProj.setPlaceholderText("C:\\")
        if (autoPathProj != ""):
            self.pathProj.setText(autoPathProj+"msys64\\home\\ofuser\\")
        else:
            self.pathProj.setText("")
        layoutFrame1.addWidget(self.pathProj, 1, 1)
        self.pushButtonPathProj = QPushButton("Обзор")
        self.pushButtonPathProj.setMinimumSize(60, 27)
        self.pushButtonPathProj.clicked.connect(self.selectFolderProj)
        layoutFrame1.addWidget(self.pushButtonPathProj, 1, 2)

        layoutFrame1.addWidget(QLabel("Cреда openFoam:"), 2, 0)
        self.pathEnv = QLineEdit()

        self.pathEnv.setText(autoPathEnv)
        self.pathEnv.setPlaceholderText("C:\\")
        layoutFrame1.addWidget(self.pathEnv, 2, 1)
        self.pushButtonPathEnv = QPushButton("Обзор")
        self.pushButtonPathEnv.setMinimumSize(60, 27)
        self.pushButtonPathEnv.clicked.connect(self.selectFileEnv)
        layoutFrame1.addWidget(self.pushButtonPathEnv, 2, 2)

        frame1.setLayout(layoutFrame1)
        widgetLayout.addWidget(frame1)

        frame2 = QFrame(self.newProjDialog)
        frame2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        frame2.setMinimumHeight(40)
        layoutFrame2 = QHBoxLayout()
        layoutFrame2.addStretch()
        buttonOk = QPushButton("Создать")
        buttonOk.setFixedSize(120, 30)
        buttonOk.clicked.connect(self.checkPaths)
        layoutFrame2.addWidget(buttonOk)
        frame2.setLayout(layoutFrame2);
        widgetLayout.addWidget(frame2)

        self.newProjDialog.setLayout(widgetLayout)

    def selectFolderProj(self):
        """!
        @brief Метод выбора папки проекта.

        Метод выбора папки для сохранения проекта.
        """

        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        folder_path = folder_path.replace("/", "\\")
        self.pathProj.setText(folder_path)

    def selectFileEnv(self):
        """!
        @brief Метод выбора файла среды.

        Метод выбора среды, т.е. файла ".bat" openFoam.
        """

        file_path, _ = QFileDialog.getOpenFileName(self, 'Select (EnvVariables).bat File', filter='Data files (*.bat)')
        file_path = file_path.replace("/", "\\")
        self.pathEnv.setText(file_path)

    def checkPaths(self):
        """!
        @brief Метод проверки корректности пути.

        Метод, который проверяет правильность написания или выбора пути (к примеру путь к проекту или путь к среде).
        """

        if not os.path.exists(self.pathProj.text()):
            QMessageBox.critical(self, "Ошибка", "Не верный формат пути к проекту")
            return
        elif os.path.exists(self.pathProj.text()+"\\"+self.nameProj.text()):
            QMessageBox.critical(self, "Ошибка", "Такой проект уже существует!")
            return

        if not os.path.exists(self.pathEnv.text()):
            QMessageBox.critical(self, "Ошибка", "Не верный формат пути к среде openFoam")
            return
        elif not self.pathEnv.text().replace("/", "\\").split("\\")[-1].endswith(".bat"):
            QMessageBox.critical(self, "Ошибка", "Не верный формат пути к среде openFoam")
            return

        self.newProjDialog.accept()

    def openProj(self):
        """!
        @brief Метод открытие существующего проекта.

        Метод, кооторый открывает существующий проект, который был создан с помощью данного приложения, при нажатии на кнопку в меню("Файл" -> "Открыть проект").
        """

        filePath, _ = QFileDialog.getOpenFileName(self, "Открыть файл .foamProj",
                                                  "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\ESI-OpenCFD\\OpenFOAM\\",
                                                  "Foam Files (*.foamProj)")
        if (len(filePath) == 0):
            return

        filePath = filePath.replace("/", "\\")
        for i in range(self.ui.tabWidget.count()):
            filePathExist = self.ui.tabWidget.widget(i).pathProj + "\\" + self.ui.tabWidget.widget(i).nameProj + ".foamProj"
            if (filePathExist == filePath):
                QMessageBox.critical(self, "Ошибка", "Проект уже открыт!")
                return

        fileFoam = open(filePath, "r")
        rawData = fileFoam.read()
        if not rawData.startswith("###\nPathEnv:"):
            QMessageBox.critical(self, "Ошибка", "Не верный формат файла")
            return
        pathEnv = rawData.split("\n")[1].split(" ")[-1]
        fileFoam.close()
        pathProj = "\\".join(filePath.replace("/", "\\").split("\\")[:-1])

        nameProj = pathProj.split("\\")[-1]
        newTab = Project(nameProj, pathProj, pathEnv, self.ui.tabWidget)
        self.ui.tabWidget.addTab(newTab, f"Проект {nameProj}")

        newTab.parseProj(pathProj + "\\" + nameProj + ".foamProj")

        self.ui.tabWidget.setCurrentWidget(newTab)

    def newProj(self):
        """!
        @brief Метод создание нового проекта.

        Метод, кооторый создает новый проект при нажатии на кнопку в меню("Файл" -> "Новый проект").
        """

        self.nameProj.clear()
        res = self.newProjDialog.exec_()
        if res == QDialog.Rejected:
            return

        pathProj = self.pathProj.text()
        if self.pathProj.text()[-1] == "\\":
            pathProj += self.nameProj.text()
        else:
            pathProj += "\\" + self.nameProj.text()

        newTab = Project(self.nameProj.text(), pathProj, self.pathEnv.text(), self.ui.tabWidget)
        self.ui.tabWidget.addTab(newTab, f"Проект {self.nameProj.text()}")

        if not os.path.exists(pathProj):
            os.makedirs(pathProj)

        pathFile = pathProj + "\\" + pathProj.split("\\")[-1] + ".foamProj"
        fileFoam = open(pathFile, "w")
        fileFoam.write(f"###\nPathEnv: {self.pathEnv.text()}\n")
        fileFoam.close()

        pathFileFoam = pathProj + "\\" + pathProj.split("\\")[-1] + ".foam"
        fileFoam = open(pathFileFoam, "w")
        fileFoam.close()

        self.ui.tabWidget.setCurrentWidget(newTab)

    def removeProj(self, id):
        """!
        @brief Метод закрытие проекта.

        Метод, который закрывает открытый проекта в программе.
        @param id (int) - id виджета в контейнере виджетов
        """

        self.ui.tabWidget.removeTab(id)

class GenerateModel(QObject):
    """!
    @brief Класс отдельного потока для выполнения моделирования

    Этот класс отдельного потока, в котором выполняется моделирование, при этом никак не мещая пользователю продолжить пользоваться программой или запуска моделирования другой модели в другом проекте.
    """

    updateProgressBar = pyqtSignal(int)
    finishedGenerate = pyqtSignal()
    damagedGenerate = pyqtSignal()
    updatePlainTextEdit = pyqtSignal(str)
    parseResiduals = pyqtSignal(str)

    def __init__(self, pathProj, pathEnv):
        """!
        @brief Конструктор класса.

        Конструктора класса принимает два параметра, которые в дальнейшем будут использоваться в функциях класса:
        @param pathProj (str) - путь к папке проекта
        @param pathEnv (str) - путь к среде openFoam
        """

        super().__init__()
        self.pathProj = pathProj
        self.pathEnv = pathEnv

        self.consoleIsActive = False

    @pyqtSlot(str, str, str)
    def setTime(self, timeStart, timeEnd, timeStep):
        """!
        @brief Слот задания времени для вычисления текущего состояния процесса моделирования в процентах.

        Слот задания времени для вычисления текущего состояния процесса моделирования и отображения значения в процентах.
        @param timeStart (str) - время начала моделирования, заданное в параметрах моделирования
        @param timeEnd (str) - время окончания моделирования, заданное в параметрах моделирования
        @param timeStep (str) - шаг по времени моделирования, заданное в параметрах моделирования
        """

        self.timeStart = float(timeStart)
        self.timeEnd = float(timeEnd)
        self.timeStep = float(timeStep)

    def updateThread(self, newThread):
        """!
        @brief Метод переноса объекта этого класса в другой поток.

        Метод, который переносит объекта этого класса в другой поток для дальнейшего моделирования, при этом никак не мешая основной программе.
        @param newThread (QThread) - время начала моделирования
        """

        self.newThread = newThread
        self.moveToThread(self.newThread)

    @pyqtSlot(bool)
    def toggleConsole(self, checked):
        """!
        @brief Слот обработки изменения окна консоли (вкл/выкл).

        Слот, который сохраняет значение состояни консоли. Необходимо для оптимизации. Когда консоль выключена накапливать результат, а после включения заполнить накопленным содержимым.
        @param checked (bool) - вкл/выкл консоль
        """

        self.consoleIsActive = checked

    @pyqtSlot(str)
    def startGenerate(self, solver):
        """!
        @brief Слот запуска моделирования.

        Слот, который запускает моделирование с помощью среды openFoam, запустив команду solver.
        @param solver (str) - команда запуска решателя (пример: icoFoam)
        """

        checkDamaged = True
        self.log = ""
        startLog = False
        stepUpdateProgressBar = 0
        skipIteration = int((self.timeEnd/self.timeStep)/100)
        blockLogForConsole = ""

        if (solver != "Не выбрано"):
            # Команда, которую вы хотите выполнить в .bat файле
            command_to_execute = "call " + self.pathEnv + " && cd " + self.pathProj + " && " + solver

            # Выполнение файла .bat с передачей команды
            p = Popen(command_to_execute, shell=True,
                      stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True,
                      universal_newlines=True)
            for line in p.stdout:
                QCoreApplication.processEvents()
                if line.startswith("Time = "):
                    startLog = True
                    if(stepUpdateProgressBar == skipIteration):
                        stepUpdateProgressBar = 0
                        timeCurrent = float(line.split()[-1])
                        proc = int(timeCurrent / (self.timeEnd - self.timeStart) * 100)
                        self.updateProgressBar.emit(proc)

                        if(self.consoleIsActive):
                            self.updatePlainTextEdit.emit(blockLogForConsole)
                            blockLogForConsole = ""
                    else:
                        stepUpdateProgressBar += 1
                elif line.startswith("End"):
                    checkDamaged = False
                    self.updatePlainTextEdit.emit(blockLogForConsole)
                    self.finishedGenerate.emit()
                    self.parseResiduals.emit(self.log)
                print(line, end='')  # Печать вывода без добавления дополнительных символов перевода строки
                blockLogForConsole += line
                if startLog:
                    self.log += line

            if (checkDamaged):
                self.damagedGenerate.emit()
        else:
            self.finishedGenerate.emit()

class ViewModel(QDialog):
    def __init__(self, pathProj, nameProj, parent=None):
        super().__init__(parent)
        self.ui = Ui_ViewModel()
        self.ui.setupUi(self)

        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.pathProj = pathProj.replace("\\", "/")
        self.nameProj = nameProj

        self.ui.comboBoxAxis.addItems(["oX", "oY", "oZ"])
        self.ui.comboBoxAxis.setCurrentIndex(0)
        self.ui.lineEditOffset.setText("0")
        self.ui.lineEditXRotation.setText("0")
        self.ui.lineEditYRotation.setText("0")
        self.ui.lineEditZRotation.setText("0")

        self.ui.pushButtonMakePNG.clicked.connect(self.makePNG)

    def setTimeStep(self, listTimeStep):
        self.ui.comboBoxTimeStep.setDisabled(False)
        self.ui.comboBoxTimeStep.addItems(listTimeStep)
        self.ui.comboBoxTimeStep.setCurrentIndex(0)

    def setVars(self, listVars):
        self.ui.comboBoxVar.setDisabled(False)
        self.ui.comboBoxVar.addItems(listVars)

    def clear(self):
        if(self.ui.graphicsView.scene() != None):
            self.ui.graphicsView.scene().clear()
        self.ui.comboBoxVar.setDisabled(True)
        self.ui.comboBoxVar.clear()
        self.ui.comboBoxTimeStep.setDisabled(True)
        self.ui.comboBoxTimeStep.clear()
        self.ui.comboBoxAxis.setCurrentIndex(0)
        self.ui.lineEditOffset.setText("0")
        self.ui.lineEditXRotation.setText("0")
        self.ui.lineEditYRotation.setText("0")
        self.ui.lineEditZRotation.setText("0")

    def makePNG(self):
        self.setDisabled(True)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QCoreApplication.processEvents()


        offset = self.ui.lineEditOffset.text()
        xRotation = self.ui.lineEditXRotation.text()
        yRotation = self.ui.lineEditYRotation.text()
        zRotation = self.ui.lineEditZRotation.text()
        nameVar = self.ui.comboBoxVar.currentText()
        timeValue = self.ui.comboBoxTimeStep.currentText()
        if(float(offset) < 0):
            offset = "-" + offset
        if (float(xRotation) < 0):
            xRotation = "-" + xRotation
        if (float(yRotation) < 0):
            yRotation = "-" + yRotation
        if (float(zRotation) < 0):
            zRotation = "-" + zRotation
        command_str = str(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
        command_to_execute = "pvpython --force-offscreen-rendering "+command_str+"/script.py " + \
                             self.pathProj + "\\" + self.nameProj + ".foam " + str(self.ui.comboBoxAxis.currentIndex()) + \
                             " " + offset + " " + xRotation + " " + yRotation + " " + zRotation + " " + nameVar + " " + \
                             timeValue
        p = Popen(command_to_execute, shell=True, close_fds=True)
        p.wait()

        temp_dir = tempfile.gettempdir()
        custom_temp_dir = os.path.join(temp_dir, 'GUIopenFoam')
        temp_file_path = os.path.join(custom_temp_dir, 'screenshot.png')
        if os.path.exists(temp_file_path):
            shutil.move(temp_file_path, self.pathProj+"/screenshot.png")
        if os.path.exists(custom_temp_dir):
            shutil.rmtree(custom_temp_dir)

        scene = QGraphicsScene(self)
        self.ui.graphicsView.setScene(scene)
        if os.path.exists(self.pathProj+"/screenshot.png"):
            pixmap = QPixmap(self.pathProj+"/screenshot.png")
            pixmap_item = QGraphicsPixmapItem(pixmap)
            pixmap_item.setScale(self.ui.graphicsView.frameSize().height() / pixmap.height() - (self.ui.graphicsView.frameSize().height() / pixmap.height())*0.01)
            scene.addItem(pixmap_item)

        self.setDisabled(False)
        QApplication.setOverrideCursor(Qt.ArrowCursor)

class Project(QWidget):
    """!
    @brief Класс проекта openFoam

    Этот класс проекта openFoam, в котором инициализируются все параметры для моделирования с помощью openFoam и создаются соответствующие файлы
    """

    signalSetTime = pyqtSignal(str, str, str)
    signalStartGenerate = pyqtSignal(str)
    signalToggleConsole = pyqtSignal(bool)

    def __init__(self, nameProj, pathProj, pathEnv, parent=None):
        """!
        @brief Конструктор класса.

        В конструкторе устанавливаются название проекта, пукть к папке проекта и среда openFoam
        @param nameProj (str) - название проекта
        @param pathProj (str) - путь к папке проекта
        @param pathEnv (str) - путь к среде openFoam (к файлу .bat)
        @param parent (str) - (необязательный параметр) указатель на объект Qt
        """

        super().__init__(parent)
        self.ui = Ui_Tab()
        self.ui.setupUi(self)

        self.ui.console.hide()

        self.ui.pushButtonBlockMesh.clicked.connect(self.runBlockMesh)
        self.ui.pushButtonImportSTL.clicked.connect(self.openSTL)
        self.ui.pushButtonResetSTL.clicked.connect(self.resetSTL)
        self.ui.pushButtonGenerateSTL.clicked.connect(self.generateSTL)
        self.ui.pushButtonGenerateSTL.setDisabled(True)

        self.nameProj = nameProj
        self.pathProj = pathProj
        self.pathEnv = pathEnv

        self.listConstants = []
        self.listBeginValues = []

        self.fvSchemes = FvSchemes()
        self.fvSolution = FvSolution()
        self.initFvWindow()

        self.initFigure()
        self.initSolver()
        self.initGenerateModel()

        self.checkedConsole = False

        self.listResiduals = []
        self.initWindowResiduals()

    def initWindowResiduals(self):
        """!
        @brief Метод инициализация окна графиков точности решения.

        В этом методе происходит инициализация окна графиков точности решения.
        """

        self.widgetResiduals = QDialog()
        self.widgetResiduals.setWindowTitle("Точность решения")
        self.widgetResiduals.setWindowFlags(self.widgetResiduals.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.widgetResiduals.setWindowIcon(QIcon("icons/1.png"))
        layoutWidgetResiduals = QHBoxLayout()
        self.figure1 = plt.figure()
        self.canvas1 = FigureCanvas(self.figure1)
        layoutWidgetResiduals.addWidget(self.canvas1)
        self.figure2 = plt.figure()
        self.canvas2 = FigureCanvas(self.figure2)
        layoutWidgetResiduals.addWidget(self.canvas2)
        self.ax1 = self.figure1.add_subplot(111)
        self.ax2 = self.figure2.add_subplot(111)
        self.ax1.set_title('Начальный остаток')
        self.ax1.set_xlabel('Время')
        self.ax1.set_ylabel('Значение')
        self.ax2.set_title('Конечный остаток')
        self.ax2.set_xlabel('Время')
        self.ax2.set_ylabel('Значение')
        self.canvas1.draw()
        self.canvas2.draw()
        self.setLayout(layoutWidgetResiduals)
        self.widgetResiduals.setLayout(layoutWidgetResiduals)

    def showWindowResiduals(self):
        """!
        @brief Метод отбражения окна с графиками точности решения.

        Метод отбражения окна с графиками точности решения.
        """

        self.widgetResiduals.exec_()

    @pyqtSlot(str)
    def parseResiduals(self, log):
        """!
        @brief Метод парсинга данных с консоли для отображения в виде графиков.

        Метод парсинга данных с консоли для отображения в виде графиков.
        """

        self.listResiduals = []
        logList = log.split("Time =")
        for block in logList:
            lineList = block.split("\n")
            listRes = []
            for line in lineList:
                nameValue = ""
                initialResiduals = float(0)
                finalResiduals = float(0)

                indexStart = line.find("Solving for ")
                if indexStart != -1:
                    nameValue = line[indexStart+len("Solving for "):line.find(",", indexStart)]

                indexStart = line.find("Initial residual = ")
                if indexStart != -1:
                    initialResiduals = float(line[indexStart+len("Initial residual = "):line.find(",", indexStart)])

                indexStart = line.find("Final residual = ")
                if indexStart != -1:
                    finalResiduals = float(line[indexStart+len("Final residual = "):line.find(",", indexStart)])

                if nameValue != "":
                    listRes.append([nameValue, [initialResiduals], [finalResiduals]])

            if len(listRes) != 0:
                if len(self.listResiduals) == 0:
                    for val in listRes:
                        self.listResiduals.append(val)
                else:
                    for i in range(len(self.listResiduals)):
                        self.listResiduals[i][1].append(listRes[i][1][0])
                        self.listResiduals[i][2].append(listRes[i][2][0])

        if len(self.listResiduals) != 0:
            self.ax1.clear()
            self.ax1.set_title('Начальный остаток')
            self.ax1.set_xlabel('Время')
            self.ax1.set_ylabel('Значение')
            self.ax2.clear()
            self.ax2.set_title('Конечный остаток')
            self.ax2.set_xlabel('Время')
            self.ax2.set_ylabel('Значение')
            time = np.linspace(float(self.ui.lineEditStartTime.text())+float(self.ui.lineEditStepTime.text()),
                               float(self.ui.lineEditEndTime.text()), len(self.listResiduals[0][1]))

            for val in self.listResiduals:
                self.ax1.plot(time, val[1], label=val[0])
                self.ax2.plot(time, val[2], label=val[0])
            self.ax1.legend()
            self.ax2.legend()
            self.canvas1.draw()
            self.canvas2.draw()

    def initFvWindow(self):
        """!
        @brief Метод инициализация окна изменения fvObjects.

        В этом методе происходит инициализация окна изменения fvObjects.
        """

        self.widgetFv = QDialog()
        self.widgetFv.setWindowFlags(self.widgetFv.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.widgetFv.resize(500,600)
        self.widgetFv.setWindowIcon(QIcon("icons/1.png"))
        layoutWidgetFv = QVBoxLayout()
        self.plainTextEditWidgetFv = QPlainTextEdit()
        saveButton = QPushButton("Применить")
        saveButton.clicked.connect(self.saveChangesFvObject)
        layoutWidgetFv.addWidget(self.plainTextEditWidgetFv)
        layoutWidgetFv.addWidget(saveButton)
        self.widgetFv.setLayout(layoutWidgetFv)

    def saveChangesFvObject(self):
        """!
        @brief Метод сохранения изменений fvObjects.

        Метод сохранения изменений fvObjects.
        """

        if self.widgetFv.windowTitle() == "fvSchemes":
            self.fvSchemes.setText(self.plainTextEditWidgetFv.toPlainText())
        elif self.widgetFv.windowTitle() == "fvSolution":
            self.fvSolution.setText(self.plainTextEditWidgetFv.toPlainText())
        self.widgetFv.hide()
        self.saveChanges(False)

    def showFvWindow(self, text):
        """!
        @brief Метод отбражения окна изменений fvObjects.

        Метод отбражения окна изменений fvObjects.
        """

        if self.ui.comboBoxSolver.currentIndex() != 0:
            self.widgetFv.setWindowTitle(text)
            if text == "fvSchemes":
                self.plainTextEditWidgetFv.setPlainText(self.fvSchemes.getText())
            elif text == "fvSolution":
                self.plainTextEditWidgetFv.setPlainText(self.fvSolution.getText())
            self.widgetFv.exec_()

    def currentToggleConsole(self):
        """!
        @brief Метод возвращения значения состояния консоли.

        Метод возвращения значения состояния консоли (вкл/выкл).
        @return checkedConsole (bool) - стостояние консоли (вкл/выкл)
        """

        return self.checkedConsole

    def toggleConsole(self, checked):
        """!
        @brief Метод отображения или скрытия консоли.

        Метод отображения или скрытия консоли для проекта в нижней части окна
        @param checked (bool) - значение переключателя
        """

        self.checkedConsole = checked
        self.signalToggleConsole.emit(checked)
        if checked:
            self.ui.console.show()
        else:
            self.ui.console.hide()

    @pyqtSlot(str)
    def updatePlainTextEdit(self, line):
        """!
        @brief Слот обновления содержимого консоли.

        Слот обновления содержимого консоли во время запущенного моделирования.
        @param line (str) - строчка вывода решателя
        """

        line.replace("\n", "")
        self.ui.console.appendPlainText(line)

    def initGenerateModel(self):
        """!
        @brief Метод инициализация объекта моделирования.

        Метод, в котором инициализируется объект моделирования и переносится другой поток, и после запускается этот новый поток.
        """

        self.generateModel = GenerateModel(self.pathProj, self.pathEnv)
        self.generateModel.updateProgressBar.connect(self.updateProgressBar)
        self.generateModel.finishedGenerate.connect(self.finishedGenerate)
        self.generateModel.damagedGenerate.connect(self.damagedGenerate)
        self.generateModel.updatePlainTextEdit.connect(self.updatePlainTextEdit)
        self.generateModel.parseResiduals.connect(self.parseResiduals)

        self.signalSetTime.connect(self.generateModel.setTime)
        self.signalStartGenerate.connect(self.generateModel.startGenerate)
        self.signalToggleConsole.connect(self.generateModel.toggleConsole)

        self.newThread = QThread()
        self.generateModel.updateThread(self.newThread)
        self.destroyed.connect(self.newThread.quit)

        self.ui.buttonGenerate.clicked.connect(self.generate)
        self.ui.buttonClearGenerate.clicked.connect(self.clearGenerate)

        self.viewModel = ViewModel(self.pathProj, self.nameProj)
        self.ui.buttonView.clicked.connect(self.showViewModel)

        self.newThread.start()

    def generate(self):
        """!
        @brief Метод запуска моделирования.

        Метод, который запускает моделирование при нажатии на кнопку "Смоделировать".
        """

        self.saveChanges(showMessage=False)

        self.ui.progressBar.setValue(0)
        self.ui.buttonView.setEnabled(False)
        self.ui.buttonGenerate.setEnabled(False)
        self.ui.buttonClearGenerate.setEnabled(False)
        self.ui.groupBox_2.setEnabled(False)
        self.ui.groupBox_3.setEnabled(False)
        self.ui.groupBox_4.setEnabled(False)
        self.signalSetTime.emit(self.ui.lineEditStartTime.text(), self.ui.lineEditEndTime.text(), self.ui.lineEditStepTime.text())
        self.signalStartGenerate.emit(self.ui.comboBoxSolver.currentText())

    def clearGenerate(self):
        """!
        @brief Метод очистки моделирования.

        Метод очистки всех созданных папок при моделировании, кроме "system", "constant", "0".
        """

        folders = [f for f in os.listdir(self.pathProj) if os.path.isdir(os.path.join(self.pathProj, f))]
        for folder in folders:
            if folder != "system" and folder != "constant" and folder != "0":
                shutil.rmtree(os.path.join(self.pathProj, folder))
        self.ui.progressBar.setValue(0)

        self.ax1.clear()
        self.ax1.set_title('Начальный остаток')
        self.ax1.set_xlabel('Время')
        self.ax1.set_ylabel('Значение')
        self.ax2.clear()
        self.ax2.set_title('Конечный остаток')
        self.ax2.set_xlabel('Время')
        self.ax2.set_ylabel('Значение')
        self.canvas1.draw()
        self.canvas2.draw()

        self.viewModel.clear()
        QMessageBox.information(self, "Информация", "Смоделированные данные успешно удалены!")

    def runParaView(self):
        """!
        @brief Метод просмотра результатов моделирования.

        Метод запуска просмотра результатов моделирования в программе ParaView.
        """

        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.setEnabled(False)
        QCoreApplication.processEvents()

        pathFile = self.pathProj + "\\" + self.pathProj.split("\\")[-1] + ".foam"
        Popen("paraview " + pathFile, shell=True,
              stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True,
              universal_newlines=True)

        timer = QElapsedTimer()
        timer.start()
        checkOpenParaView = False
        while (timer.elapsed() < 10000 and not checkOpenParaView):
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == 'paraview.exe' and proc.cmdline()[1] == (
                        self.pathProj + "\\" + self.pathProj.split("\\")[-1] + ".foam"):
                    checkOpenParaView = True
                    break
        if not checkOpenParaView:
            QMessageBox.critical(self, "Ошибка", "Не удалось открыть модель")

        QApplication.setOverrideCursor(Qt.ArrowCursor)
        self.setEnabled(True)
        QCoreApplication.processEvents()

    def showViewModel(self):
        self.viewModel.clear()

        if self.ui.comboBoxSolver.currentIndex() != 0:
            array = np.arange(Decimal(self.ui.lineEditStartTime.text()), Decimal(self.ui.lineEditEndTime.text())+Decimal(self.ui.lineEditStepTime.text()), Decimal(self.ui.lineEditStepTime.text())* 20)
            listPointTime = list(map(str, array))
            self.viewModel.setTimeStep(listPointTime)
            if self.ui.comboBoxSolver.currentIndex() == 1:
                self.viewModel.setVars(["p", "U"])
            elif self.ui.comboBoxSolver.currentIndex() == 2:
                self.viewModel.setVars(["T"])

        self.viewModel.exec_()

    @pyqtSlot(int)
    def updateProgressBar(self, proc):
        """!
        @brief Слот обновления прогресса выполнения моделирования.

        Слот обновления прогресса выполнения моделирования в нижней части программы(идикатор хода моделирования).
        @param proc (int) - значение в процентах
        """

        self.ui.progressBar.setValue(proc)

    @pyqtSlot()
    def finishedGenerate(self):
        """!
        @brief Слот заверщения процесса выполнения моделирования.

        Слот, который обрабатывает сигнал о заверщении моделирования.
        """

        self.ui.progressBar.setValue(100)
        QMessageBox.information(self, "Информация", "Моделирование выполнилось успешно!")
        self.ui.buttonView.setEnabled(True)
        self.ui.buttonGenerate.setEnabled(True)
        self.ui.buttonClearGenerate.setEnabled(True)
        self.ui.groupBox_2.setEnabled(True)
        self.ui.groupBox_3.setEnabled(True)
        self.ui.groupBox_4.setEnabled(True)

    @pyqtSlot()
    def damagedGenerate(self):
        """!
        @brief Слот обработки ошибки при моделировании.

        Данный слот будет вызван если выполнение команды в среде openFoam не закончилась на End.
        """

        QMessageBox.critical(self, "Ошибка моделирования", "Возникла ошибка при моделировании!")
        self.ui.progressBar.setValue(0)
        self.ui.buttonView.setEnabled(True)
        self.ui.buttonGenerate.setEnabled(True)
        self.ui.buttonClearGenerate.setEnabled(True)
        self.ui.groupBox_2.setEnabled(True)
        self.ui.groupBox_3.setEnabled(True)
        self.ui.groupBox_4.setEnabled(True)

    def runBlockMesh(self):
        """!
        @brief Метод запуска команды blockMesh.

        Метод запуска команды blockMesh в среде openFoam.
        """

        self.saveChanges(showMessage=False)
        self.setDisabled(True)
        QCoreApplication.processEvents()

        checkDamaged = True

        command_to_execute = "call " + self.pathEnv + " && cd " + self.pathProj + " && blockMesh"
        p = Popen(command_to_execute, shell=True,
                  stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True,
                  universal_newlines=True)
        for line in p.stdout:
            print(line, end='')  # Печать вывода без добавления дополнительных символов перевода строки
            if(line.endswith("\n")):
                line = line[:-1]
            self.ui.console.appendPlainText(line)
            QCoreApplication.processEvents()
            if line.startswith("End"):
                checkDamaged = False

        if (checkDamaged):
            QMessageBox.critical(self, "Ошибка", "Не удалось построить сетку STL")
        else:
            QMessageBox.information(self, "Информация", "Сетка успешно построена!")
        self.setDisabled(False)

    def openSTL(self):
        """!
        @brief Метод открытия STL файла.

        Метод открытия STL и перемещения его в папку с проектом.
        """

        filePath, _ = QFileDialog.getOpenFileName(self, "Открыть файл .stl",
                                                  "C:\\Users\\" + os.getlogin() + "\\Desktop",
                                                  "Foam Files (*.stl)")
        if (len(filePath) == 0):
            return

        filePath = filePath.replace("/", "\\")
        nameFileSTL = filePath.split("\\")[-1]

        pathDir = self.pathProj + "\\constant\\triSurface"
        if not os.path.exists(pathDir):
            os.makedirs(pathDir)

        pathSTL = pathDir + "\\" + nameFileSTL
        shutil.copyfile(filePath, pathSTL)

        self.loadSTL(pathSTL)

    def loadSTL(self, pathSTL):
        """!
        @brief Метод обработки STL файла.

        Метод, в котором идёт обработка STL файла. Вычисляется его Bounding Box, а также находится его центр и перемещается в начало координат, для корректного построения сетки в openFoam
        @param pathSTL (str) - Путь к файлу ".stl"
        """

        nameSTL = pathSTL.split("\\")[-1]
        self.ui.labelNameSTL.setText(nameSTL)
        your_mesh = mesh.Mesh.from_file(pathSTL)
        min_point, max_point = your_mesh.min_, your_mesh.max_
        self.widthSTL = abs(max_point[0] - min_point[0])
        self.heightSTL = abs(max_point[1] - min_point[1])
        self.lengthSTL = abs(max_point[2] - min_point[2])
        print("Ширина:", self.widthSTL)
        print("Высота:", self.heightSTL)
        print("Длина:", self.lengthSTL)

        center_x = (your_mesh.x.max() + your_mesh.x.min()) / 2
        center_y = (your_mesh.y.max() + your_mesh.y.min()) / 2
        center_z = (your_mesh.z.max() + your_mesh.z.min()) / 2
        your_mesh.x -= center_x
        your_mesh.y -= center_y
        your_mesh.z -= center_z
        self.minPointMesh = [your_mesh.x.min(), your_mesh.y.min(), your_mesh.z.min()]
        self.maxPointMesh = [your_mesh.x.max(), your_mesh.y.max(), your_mesh.z.max()]
        your_mesh.save(pathSTL)
        self.changedSolver()
        self.ui.pushButtonGenerateSTL.setDisabled(False)

        # --------------------------- Настройки в .foamProj ---------------------------
        settingsProject = f"STL {nameSTL}\n"

        file = open(self.pathProj + "\\" + self.nameProj + ".foamProj", "r")
        data = file.read()
        file.close()
        startIndex = data.find("STL")
        if startIndex == -1:
            data += settingsProject
        else:
            endIndex = data.find("\n", startIndex)
            data = data.replace(data[startIndex:endIndex + 1], settingsProject)
        file = open(self.pathProj + "\\" + self.nameProj + ".foamProj", "w")
        file.write(data)
        file.close();
        # --------------------------- Настройки в .foamProj ---------------------------

    def resetSTL(self):
        """!
        @brief Метод сброса импортированной STL.

        Метод, который удаляет скопированный и обработанный STL файл из папки проекта.
        """

        if self.ui.labelNameSTL.text() != "Не выбран":
            self.ui.labelNameSTL.setText("Не выбран")
            pathDir = self.pathProj + "\\constant\\triSurface"
            shutil.rmtree(pathDir)
            self.ui.pushButtonGenerateSTL.setDisabled(True)

            file = open(self.pathProj + "\\" + self.nameProj + ".foamProj", "r")
            data = file.read()
            file.close()
            startIndex = data.find("STL")
            if startIndex != -1:
                endIndex = data.find("\n", startIndex)
                data = data.replace(data[startIndex:endIndex + 1], "")
                file = open(self.pathProj + "\\" + self.nameProj + ".foamProj", "w")
                file.write(data)
                file.close()

    def generateSTL(self):
        """!
        @brief Метод построение сетки STL.

        Метод построение сетки STL внутри основной фигуры(параллелепипед, шар или цилиндр).
        """

        self.saveChanges(showMessage=False)
        self.setDisabled(True)
        QCoreApplication.processEvents()

        checkDamaged = True

        command_to_execute = "call " + self.pathEnv + " && cd " + self.pathProj + " && snappyHexMesh -overwrite"
        p = Popen(command_to_execute, shell=True,
                  stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True,
                  universal_newlines=True)
        for line in p.stdout:
            print(line, end='')  # Печать вывода без добавления дополнительных символов перевода строки
            if (line.endswith("\n")):
                line = line[:-1]
            self.ui.console.appendPlainText(line)
            QCoreApplication.processEvents()
            if line.startswith("End"):
                checkDamaged = False

        if (checkDamaged):
            QMessageBox.critical(self, "Ошибка", "Не удалось построить сетку STL")
        else:
            QMessageBox.information(self, "Информация", "Сетка успешно построена!")
        self.setDisabled(False)

    def saveChanges(self, showMessage=True):
        """!
        @brief Метод сохранения всех изменений в проекте.

        Метод, который сначала очищает файлы, которые могут менятся, затем создаёт необходимые файлы и сохраняет все изменения.
        @param showMessage (bool) - флаг отображения сообщения об успешном сохранении изменений (по умолчанию True)
        """

        self.clearFolderConstants()
        self.clearFolderBeginValues()

        self.createBlockMeshDict()
        self.createControlDict()
        self.createConstants()
        self.createBeginValues()
        self.createFvObjects()
        if self.ui.labelNameSTL.text() != "Не выбран":
            self.createSnappyHexMeshDict()
        if (showMessage):
            QMessageBox.information(self, "Информация", "Изменения сохранены!")

    def createBlockMeshDict(self):
        """!
        @brief Метод создания файла blockMeshDict.

        Метод генерации файла blockMeshDict в папке "system".
        """

        blockMeshDict = None
        if (self.ui.comboBoxChangeFigure.currentText() == "Параллелепипед"):
            blockMeshDictBlocks = BlockMeshDictBlocks(int(self.lineEditCellLengthFigure.text()),
                                                      int(self.lineEditCellWidthFigure.text()),
                                                      int(self.lineEditCellHeightFigure.text()))
            width = float(self.lineEditWidthFigure.text())
            height = float(self.lineEditHeightFigure.text())
            length = float(self.lineEditLengthFigure.text())
            blockMeshDictVertices = BlockMeshDictVertices([
                [-length / 2, -width / 2, -height / 2],
                [length / 2, -width / 2, -height / 2],
                [length / 2, width / 2, -height / 2],
                [-length / 2, width / 2, -height / 2],
                [-length / 2, -width / 2, height / 2],
                [length / 2, -width / 2, height / 2],
                [length / 2, width / 2, height / 2],
                [-length / 2, width / 2, height / 2]])
            blockMeshDictBoundaries = BlockMeshDictBoundaries([
                {
                    'name': 'Top',
                    'type': 'wall',
                    'faces': [[4, 5, 6, 7]]
                },
                {
                    'name': 'Bottom',
                    'type': 'wall',
                    'faces': [[0, 1, 2, 3]]
                },
                {
                    'name': 'Front',
                    'type': 'wall',
                    'faces': [[1, 2, 6, 5]]
                },
                {
                    'name': 'Back',
                    'type': 'wall',
                    'faces': [[0, 3, 7, 4]]
                },
                {
                    'name': 'Left',
                    'type': 'wall',
                    'faces': [[0, 1, 5, 4]]
                },
                {
                    'name': 'Right',
                    'type': 'wall',
                    'faces': [[3, 2, 6, 7]]
                },
            ])
            blockMeshDict = BlockMeshDict(float(self.lineEditScaleFigure.text()),
                                          blockMeshDictVertices,
                                          blockMeshDictBlocks,
                                          blockMeshDictBoundaries)
        elif (self.ui.comboBoxChangeFigure.currentText() == "Cфера"):

            vert = (float(self.lineEditRadiusFigure.text()) / 3) ** (1 / 2)

            blockMeshDictBlocks = BlockMeshDictBlocks(int(self.lineEditCellFigure.text()),
                                                      int(self.lineEditCellFigure.text()),
                                                      int(self.lineEditCellFigure.text()))
            blockMeshDictVertices = BlockMeshDictVertices(
                [[-vert, -vert, -vert],
                 [vert, -vert, -vert],
                 [vert, vert, -vert],
                 [-vert, vert, -vert],
                 [-vert, -vert, vert],
                 [vert, -vert, vert],
                 [vert, vert, vert],
                 [-vert, vert, vert]
                 ])
            blockMeshDictBoundaries = BlockMeshDictBoundaries([
                {
                    'name': 'Top',
                    'type': 'wall',
                    'faces': [[0, 0]]
                },
                {
                    'name': 'Bottom',
                    'type': 'wall',
                    'faces': [[0, 1]]
                },
                {
                    'name': 'Front',
                    'type': 'wall',
                    'faces': [[0, 2]]
                },
                {
                    'name': 'Back',
                    'type': 'wall',
                    'faces': [[0, 3]]
                },
                {
                    'name': 'Left',
                    'type': 'wall',
                    'faces': [[0, 4]]
                },
                {
                    'name': 'Right',
                    'type': 'wall',
                    'faces': [[0, 5]]
                },
            ])
            blockMeshDict = BlockMeshDict(float(self.lineEditScaleFigure.text()),
                                          blockMeshDictVertices,
                                          blockMeshDictBlocks,
                                          blockMeshDictBoundaries)
            blockMeshDict.setGeometry(BlockMeshDictGeometry([
                {
                    'name': 'sphere',
                    'type': 'sphere',
                    'origin': '(0 0 0)',
                    'radius': str(float(self.lineEditRadiusFigure.text())**(1/2)),
                },
            ]))
            blockMeshDict.setEndges(BlockMeshDictEdges([
                ["arc", 0, 1, "origin", [0, 0, 0]],
                ["arc", 2, 3, "origin", [0, 0, 0]],
                ["arc", 6, 7, "origin", [0, 0, 0]],
                ["arc", 4, 5, "origin", [0, 0, 0]],
                ["arc", 0, 3, "origin", [0, 0, 0]],
                ["arc", 1, 2, "origin", [0, 0, 0]],
                ["arc", 5, 6, "origin", [0, 0, 0]],
                ["arc", 4, 7, "origin", [0, 0, 0]],
                ["arc", 0, 4, "origin", [0, 0, 0]],
                ["arc", 1, 5, "origin", [0, 0, 0]],
                ["arc", 2, 6, "origin", [0, 0, 0]],
                ["arc", 3, 7, "origin", [0, 0, 0]],
            ]))
            blockMeshDict.setFaces(BlockMeshDictFaces([
                [[0, 0], "sphere"],
                [[0, 1], "sphere"],
                [[0, 2], "sphere"],
                [[0, 3], "sphere"],
                [[0, 4], "sphere"],
                [[0, 5], "sphere"],
            ]))
        elif (self.ui.comboBoxChangeFigure.currentText() == "Цилиндр"):

            side = 2 * float(self.lineEditRadiusFigure.text()) / (2 ** (1 / 2))
            height = float(self.lineEditHeightFigure.text())
            half = side / 2
            plus = half + float(self.lineEditRadiusFigure.text())
            minus = half - float(self.lineEditRadiusFigure.text())

            blockMeshDictBlocks = BlockMeshDictBlocks(int(self.lineEditCellHeightFigure.text()),
                                                      int(self.lineEditCellRadiusFigure.text()),
                                                      int(self.lineEditCellRadiusFigure.text()))
            blockMeshDictVertices = BlockMeshDictVertices([
                [-height/2, -side/2, -side/2],
                [height/2, -side/2, -side/2],
                [height/2, side/2, -side/2],
                [-height/2, side/2, -side/2],
                [-height/2, -side/2, side/2],
                [height/2, -side/2, side/2],
                [height/2, side/2, side/2],
                [-height/2, side/2, side/2]
            ])
            blockMeshDictBoundaries = BlockMeshDictBoundaries([
                {
                    'name': 'Top',
                    'type': 'wall',
                    'faces': [[4, 5, 6, 7]]
                },
                {
                    'name': 'Bottom',
                    'type': 'wall',
                    'faces': [[0, 1, 2, 3]]
                },
                {
                    'name': 'Front',
                    'type': 'wall',
                    'faces': [[1, 2, 6, 5]]
                },
                {
                    'name': 'Back',
                    'type': 'wall',
                    'faces': [[0, 3, 7, 4]]
                },
                {
                    'name': 'Left',
                    'type': 'wall',
                    'faces': [[0, 1, 5, 4]]
                },
                {
                    'name': 'Right',
                    'type': 'wall',
                    'faces': [[3, 2, 6, 7]]
                },
            ])
            blockMeshDict = BlockMeshDict(float(self.lineEditScaleFigure.text()),
                                          blockMeshDictVertices,
                                          blockMeshDictBlocks,
                                          blockMeshDictBoundaries)
            blockMeshDict.setEndges(BlockMeshDictEdges([
                ["arc", 1, 5, "", [height/2, minus-half, 0]],
                ["arc", 0, 4, "", [-height/2, minus-half, 0]],
                ["arc", 2, 6, "", [height/2, plus-half, 0]],
                ["arc", 5, 6, "", [height/2, 0, plus-half]],
                ["arc", 4, 7, "", [-height/2, 0, plus-half]],
                ["arc", 3, 7, "", [-height/2, plus-half, 0]],
                ["arc", 2, 1, "", [height/2, 0, minus-half]],
                ["arc", 3, 0, "", [-height/2, 0, minus-half]],
            ]))

        pathDir = self.pathProj + "\\system"
        pathFile = self.pathProj + "\\system\\blockMeshDict"
        if not os.path.exists(pathDir):
            os.makedirs(pathDir)
        fileOut = open(pathFile, "w")
        fileOut.write(str(blockMeshDict))
        fileOut.close()

        # --------------------------- Настройки в .foamProj ---------------------------
        settingsProject = ""
        if (self.ui.comboBoxChangeFigure.currentIndex() == 0):
            settingsProject = f"blockMeshDict " \
                              f"{self.ui.comboBoxChangeFigure.currentIndex()}\n"
        elif (self.ui.comboBoxChangeFigure.currentText() == "Параллелепипед"):
            settingsProject = f"blockMeshDict " \
                              f"{self.ui.comboBoxChangeFigure.currentIndex()}," \
                              f"{self.lineEditScaleFigure.text()}," \
                              f"{self.lineEditWidthFigure.text()}," \
                              f"{self.lineEditHeightFigure.text()}," \
                              f"{self.lineEditLengthFigure.text()}," \
                              f"{self.lineEditCellWidthFigure.text()}," \
                              f"{self.lineEditCellHeightFigure.text()}," \
                              f"{self.lineEditCellLengthFigure.text()}\n"
        elif (self.ui.comboBoxChangeFigure.currentText() == "Cфера"):
            settingsProject = f"blockMeshDict " \
                              f"{self.ui.comboBoxChangeFigure.currentIndex()}," \
                              f"{self.lineEditScaleFigure.text()}," \
                              f"{self.lineEditRadiusFigure.text()}," \
                              f"{self.lineEditCellFigure.text()}\n"
        elif (self.ui.comboBoxChangeFigure.currentText() == "Цилиндр"):
            settingsProject = f"blockMeshDict " \
                              f"{self.ui.comboBoxChangeFigure.currentIndex()}," \
                              f"{self.lineEditScaleFigure.text()}," \
                              f"{self.lineEditHeightFigure.text()}," \
                              f"{self.lineEditRadiusFigure.text()}," \
                              f"{self.lineEditCellHeightFigure.text()}," \
                              f"{self.lineEditCellRadiusFigure.text()}\n"

        file = open(self.pathProj + "\\" + self.nameProj + ".foamProj", "r")
        data = file.read()
        file.close()
        startIndex = data.find("blockMeshDict")
        if startIndex == -1:
            data += settingsProject
        else:
            endIndex = data.find("\n", startIndex)
            data = data.replace(data[startIndex:endIndex + 1], settingsProject)
        file = open(self.pathProj + "\\" + self.nameProj + ".foamProj", "w")
        file.write(data)
        file.close()
        # --------------------------- Настройки в .foamProj ---------------------------

    def createControlDict(self):
        """!
        @brief Метод создания файла controlDict.

        Метод генерации файла controlDict в папке "system".
        """

        pathDir = self.pathProj + "\\system"
        pathFile = self.pathProj + "\\system\\controlDict"
        if not os.path.exists(pathDir):
            os.makedirs(pathDir)

        # --------------------------- Настройки в .foamProj ---------------------------
        settingsProject = f"controlDict " \
                          f"{self.ui.comboBoxSolver.currentIndex()}," \
                          f"{self.ui.lineEditStartTime.text()}," \
                          f"{self.ui.lineEditEndTime.text()}," \
                          f"{self.ui.lineEditStepTime.text()}\n"

        file = open(self.pathProj + "\\" + self.nameProj + ".foamProj", "r")
        data = file.read()
        file.close()
        startIndex = data.find("controlDict")
        if startIndex == -1:
            data += settingsProject
        else:
            endIndex = data.find("\n", startIndex)
            data = data.replace(data[startIndex:endIndex + 1], settingsProject)
        file = open(self.pathProj + "\\" + self.nameProj + ".foamProj", "w")
        file.write(data)
        file.close();
        # --------------------------- Настройки в .foamProj ---------------------------

        controlDict = ControlDict()
        if (self.ui.comboBoxSolver.currentText() == "Не выбрано"):
            controlDict["application"] = "NULL"
        else:
            controlDict["application"] = self.ui.comboBoxSolver.currentText()
        controlDict["startFrom"] = "latestTime"
        controlDict["startTime"] = self.ui.lineEditStartTime.text()
        controlDict["stopAt"] = "endTime"
        controlDict["endTime"] = self.ui.lineEditEndTime.text()
        controlDict["deltaT"] = self.ui.lineEditStepTime.text()
        controlDict["writeControl"] = "timeStep"
        controlDict["writeInterval"] = "20"
        controlDict["purgeWrite"] = "0"
        controlDict["writeFormat"] = "ascii"
        controlDict["writePrecision"] = "7"
        controlDict["writeCompression"] = "off"
        controlDict["timeFormat"] = "general"
        controlDict["timePrecision"] = "6"
        controlDict["runTimeModifiable"] = "true"
        fileOut = open(pathFile, "w")
        fileOut.write(str(controlDict))
        fileOut.close()

    def createConstants(self):
        """!
        @brief Метод создания файлов констант.

        Метод генерации файлов констант в папке "constant".
        """

        settingsProject = "constants"
        if (len(self.listConstants) != 0):
            for val in self.listConstants:
                constant = Constant(val[0], val[1].text(), val[2], val[3])

                pathDir = self.pathProj + "\\constant"
                pathFile = self.pathProj + "\\constant\\"+val[4]
                if not os.path.exists(pathDir):
                    os.makedirs(pathDir)
                fileOut = open(pathFile, "w")
                fileOut.write(str(constant))
                fileOut.close()
                settingsProject += f" {val[4]} " + val[1].text()
        settingsProject += "\n"

        # --------------------------- Настройки в .foamProj ---------------------------
        file = open(self.pathProj + "\\" + self.nameProj + ".foamProj", "r")
        data = file.read()
        file.close()
        startIndex = data.find("constants")
        if startIndex == -1:
            data += settingsProject
        else:
            endIndex = data.find("\n", startIndex)
            data = data.replace(data[startIndex:endIndex + 1], settingsProject)
        file = open(self.pathProj + "\\" + self.nameProj + ".foamProj", "w")
        file.write(data)
        file.close();
        # --------------------------- Настройки в .foamProj ---------------------------

    def createBeginValues(self):
        """!
        @brief Метод создания файлов начальных значений.

        Метод генерации файлов начальных значений в папке "0".
        """

        for val in self.listBeginValues:
            boundaryField = [
                {
                    'name': 'Top',
                    'type': val[12].currentText(),
                    'value': val[13].text()
                },
                {
                    'name': 'Bottom',
                    'type': val[14].currentText(),
                    'value': val[15].text()
                },
                {
                    'name': 'Front',
                    'type': val[4].currentText(),
                    'value': val[5].text()
                },
                {
                    'name': 'Back',
                    'type': val[6].currentText(),
                    'value': val[7].text()
                },
                {
                    'name': 'Left',
                    'type': val[10].currentText(),
                    'value': val[11].text()
                },
                {
                    'name': 'Right',
                    'type': val[8].currentText(),
                    'value': val[9].text()
                },
            ]
            if self.ui.labelNameSTL.text() != "Не выбран":
                boundaryField.append({
                    'name': 'stl_surface',
                    'type': val[16].currentText(),
                    'value': val[17].text()
                })
            beginValue = BeginValue(val[0], val[1], val[2], val[3].text(), boundaryField)
            pathDir = self.pathProj + "\\0"
            pathFile = self.pathProj + "\\0\\" + val[0]
            if not os.path.exists(pathDir):
                os.makedirs(pathDir)
            fileOut = open(pathFile, "w")
            fileOut.write(str(beginValue))
            fileOut.close()

        # --------------------------- Настройки в .foamProj ---------------------------
        settingsProject = f"beginValues"
        for val in self.listBeginValues:
            if val[1] == "volVectorField":
                val3 = val[3].text().replace(" ", "_")
                val5 = val[5].text().replace(" ", "_")
                val7 = val[7].text().replace(" ", "_")
                val9 = val[9].text().replace(" ", "_")
                val11 = val[11].text().replace(" ", "_")
                val13 = val[13].text().replace(" ", "_")
                val15 = val[15].text().replace(" ", "_")

                settingsProject += f" {val3}," \
                                   f"{val[4].currentIndex()}," \
                                   f"{val5}," \
                                   f"{val[6].currentIndex()}," \
                                   f"{val7}," \
                                   f"{val[8].currentIndex()}," \
                                   f"{val9}," \
                                   f"{val[10].currentIndex()}," \
                                   f"{val11}," \
                                   f"{val[12].currentIndex()}," \
                                   f"{val13}," \
                                   f"{val[14].currentIndex()}," \
                                   f"{val15}"
                if len(val) > 16:
                    val17 = val[17].text().replace(" ", "_")
                    settingsProject += f",{val[16].currentIndex()}," \
                                       f"{val17}"
            else:
                settingsProject += f" {val[3].text()}," \
                                   f"{val[4].currentIndex()}," \
                                   f"{val[5].text()}," \
                                   f"{val[6].currentIndex()}," \
                                   f"{val[7].text()}," \
                                   f"{val[8].currentIndex()}," \
                                   f"{val[9].text()}," \
                                   f"{val[10].currentIndex()}," \
                                   f"{val[11].text()}," \
                                   f"{val[12].currentIndex()}," \
                                   f"{val[13].text()}," \
                                   f"{val[14].currentIndex()}," \
                                   f"{val[15].text()}"
                if len(val) > 16:
                    settingsProject += f",{val[16].currentIndex()}," \
                                       f"{val[17].text()}"
        settingsProject += "\n"

        file = open(self.pathProj + "\\" + self.nameProj + ".foamProj", "r")
        data = file.read()
        file.close()
        startIndex = data.find("beginValues")
        if startIndex == -1:
            data += settingsProject
        else:
            endIndex = data.find("\n", startIndex)
            data = data.replace(data[startIndex:endIndex + 1], settingsProject)
        file = open(self.pathProj + "\\" + self.nameProj + ".foamProj", "w")
        file.write(data)
        file.close();
        # --------------------------- Настройки в .foamProj ---------------------------

    def createFvObjects(self):
        """!
        @brief Метод создания файлов fv.

        Метод создания файлов fv в папке "system" (к примеру fvSchemes).
        """

        pathDir = self.pathProj + "\\system"
        pathFile = self.pathProj + "\\system\\fvSchemes"
        if not os.path.exists(pathDir):
            os.makedirs(pathDir)
        fileOut = open(pathFile, "w")
        fileOut.write(str(self.fvSchemes))
        fileOut.close()

        pathDir = self.pathProj + "\\system"
        pathFile = self.pathProj + "\\system\\fvSolution"
        if not os.path.exists(pathDir):
            os.makedirs(pathDir)
        fileOut = open(pathFile, "w")
        fileOut.write(str(self.fvSolution))
        fileOut.close()

    def createSnappyHexMeshDict(self):
        """!
        @brief Метод создания файлов связанных с построением сетки STL.

        Метод генерации файлов связанных с построением сетки STL в папке "system".
        """

        width = 0
        height = 0
        length = 0
        minSize = 0
        locationInMesh = ""
        if (self.ui.comboBoxChangeFigure.currentText() == "Параллелепипед"):
            scale = float(self.lineEditScaleFigure.text())
            width = float(self.lineEditWidthFigure.text())
            height = float(self.lineEditHeightFigure.text())
            length = float(self.lineEditLengthFigure.text())
            minSize = min([width, height, length])
            locationInMesh = f"{length / 2 * scale - (length / 2 * scale)*0.01} {width / 2 * scale - (width / 2 * scale)*0.01} {height / 2 * scale - (height / 2 * scale)*0.01}"
        elif (self.ui.comboBoxChangeFigure.currentText() == "Cфера"):
            scale = float(self.lineEditScaleFigure.text())
            width = float((float(self.lineEditRadiusFigure.text()) / 3) ** (1 / 2))
            height = float((float(self.lineEditRadiusFigure.text()) / 3) ** (1 / 2))
            length = float((float(self.lineEditRadiusFigure.text()) / 3) ** (1 / 2))
            minSize = min([width*2, height*2, length*2])
            locationInMesh = f"{width * scale - (width * scale)*0.01} {height * scale - (height * scale)*0.01} {length * scale - (length * scale)*0.01}"
        elif (self.ui.comboBoxChangeFigure.currentText() == "Цилиндр"):
            scale = float(self.lineEditScaleFigure.text())
            width = 2 * float(self.lineEditRadiusFigure.text()) / (2 ** (1 / 2))
            height = float(self.lineEditHeightFigure.text())
            length = 2 * float(self.lineEditRadiusFigure.text()) / (2 ** (1 / 2))
            minSize = min([width, height, length])
            locationInMesh = f"{height / 2 * scale - (height / 2 * scale)*0.01} {width / 2 * scale - (width / 2 * scale)*0.01} {length / 2 * scale - (length / 2 * scale)*0.01}"
        else:
            return

        maxSizeSTL = max([self.widthSTL, self.heightSTL, self.lengthSTL])

        scaleSTL = minSize / maxSizeSTL
        scaleSTL *= int(self.ui.lineEditScaleSTL.text()) / 100
        minPoint = f"{self.minPointMesh[0] * scaleSTL} {self.minPointMesh[1] * scaleSTL} {self.minPointMesh[2] * scaleSTL}"
        maxPoint = f"{self.maxPointMesh[0] * scaleSTL} {self.maxPointMesh[1] * scaleSTL} {self.maxPointMesh[2] * scaleSTL}"


        snappyHexMeshDict = SnappyHexMeshDict(self.ui.labelNameSTL.text(), str(scaleSTL), minPoint, maxPoint,
                                              locationInMesh)
        meshQualityDict = MeshQualityDict()

        pathDir = self.pathProj + "\\system"
        pathFile = self.pathProj + "\\system\\snappyHexMeshDict"
        if not os.path.exists(pathDir):
            os.makedirs(pathDir)
        fileOut = open(pathFile, "w")
        fileOut.write(str(snappyHexMeshDict))
        fileOut.close()

        pathFile = self.pathProj + "\\system\\meshQualityDict"
        if not os.path.exists(pathDir):
            os.makedirs(pathDir)
        fileOut = open(pathFile, "w")
        fileOut.write(str(meshQualityDict))
        fileOut.close()

    def initFigure(self):
        """!
        @brief Метод инициализации виджета выбора основной фигуры.

        Метод инициализации виджета выбора основной фигуры(параллелепипед, сфера или цилиндр).
        """

        self.ui.comboBoxChangeFigure.clear()
        self.ui.comboBoxChangeFigure.addItem("Не выбрано")
        self.ui.comboBoxChangeFigure.addItem("Параллелепипед")
        self.ui.comboBoxChangeFigure.addItem("Цилиндр")
        self.ui.comboBoxChangeFigure.addItem("Cфера")
        layoutFrameChangeShape = QGridLayout()
        self.ui.frameChangeShape.setLayout(layoutFrameChangeShape)
        self.ui.comboBoxChangeFigure.currentIndexChanged.connect(self.changedFigure)
        self.ui.comboBoxChangeFigure.currentIndexChanged.emit(0)

    def changedFigure(self):
        """!
        @brief Метод обработки изменения виджета выбора основной фигуры.

        Метод обработки сигнала изменения виджета выбора основной фигуры.
        """

        self.ui.groupBoxSTL.setDisabled(False)
        self.ui.pushButtonBlockMesh.setDisabled(False)

        if (self.ui.frameChangeShape.layout() is not None):
            for i in reversed(range(self.ui.frameChangeShape.layout().count())):
                item = self.ui.frameChangeShape.layout().itemAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.ui.frameChangeShape.layout().removeItem(item)

        if (self.ui.comboBoxChangeFigure.currentText() == "Параллелепипед"):
            labelScale = QLabel("Масштаб:")
            labelWidth = QLabel("Ширина:")
            labelHeight = QLabel("Высота:")
            labelLength = QLabel("Длина:")
            labelCellWidth = QLabel("Количество ячеек по ширине:")
            labelCellHeight = QLabel("Количество ячеек по высоте:")
            labelCellLength = QLabel("Количество ячеек по длине:")
            self.lineEditScaleFigure = QLineEdit("1")
            self.lineEditWidthFigure = QLineEdit("1")
            self.lineEditHeightFigure = QLineEdit("1")
            self.lineEditLengthFigure = QLineEdit("1")
            self.lineEditCellWidthFigure = QLineEdit("10")
            self.lineEditCellHeightFigure = QLineEdit("10")
            self.lineEditCellLengthFigure = QLineEdit("10")
            self.ui.frameChangeShape.layout().addWidget(labelScale, 0, 0)
            self.ui.frameChangeShape.layout().addWidget(labelWidth, 1, 0)
            self.ui.frameChangeShape.layout().addWidget(labelHeight, 2, 0)
            self.ui.frameChangeShape.layout().addWidget(labelLength, 3, 0)
            self.ui.frameChangeShape.layout().addWidget(labelCellWidth, 4, 0)
            self.ui.frameChangeShape.layout().addWidget(labelCellHeight, 5, 0)
            self.ui.frameChangeShape.layout().addWidget(labelCellLength, 6, 0)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditScaleFigure, 0, 1)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditWidthFigure, 1, 1)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditHeightFigure, 2, 1)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditLengthFigure, 3, 1)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditCellWidthFigure, 4, 1)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditCellHeightFigure, 5, 1)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditCellLengthFigure, 6, 1)
            self.ui.frameChangeShape.layout().setColumnStretch(2, 1)
            self.ui.frameChangeShape.layout().setRowStretch(7, 1)
        elif (self.ui.comboBoxChangeFigure.currentText() == "Cфера"):
            labelScale = QLabel("Масштаб:")
            labelRadius = QLabel("Радиус:")
            labelCell = QLabel("Количество ячеек:")
            self.lineEditScaleFigure = QLineEdit("1")
            self.lineEditRadiusFigure = QLineEdit("1")
            self.lineEditCellFigure = QLineEdit("10")
            self.ui.frameChangeShape.layout().addWidget(labelScale, 0, 0)
            self.ui.frameChangeShape.layout().addWidget(labelRadius, 1, 0)
            self.ui.frameChangeShape.layout().addWidget(labelCell, 2, 0)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditScaleFigure, 0, 1)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditRadiusFigure, 1, 1)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditCellFigure, 2, 1)
            self.ui.frameChangeShape.layout().setColumnStretch(2, 1)
            self.ui.frameChangeShape.layout().setRowStretch(3, 1)
        elif (self.ui.comboBoxChangeFigure.currentText() == "Цилиндр"):
            labelScale = QLabel("Масштаб:")
            labelHeight = QLabel("Высота:")
            labelRadius = QLabel("Радиус:")
            labelCellHeight = QLabel("Количество ячеек по высоте:")
            labelCellRadius = QLabel("Количество ячеек в окружности:")
            self.lineEditScaleFigure = QLineEdit("1")
            self.lineEditHeightFigure = QLineEdit("1")
            self.lineEditRadiusFigure = QLineEdit("1")
            self.lineEditCellHeightFigure = QLineEdit("10")
            self.lineEditCellRadiusFigure = QLineEdit("10")
            self.ui.frameChangeShape.layout().addWidget(labelScale, 0, 0)
            self.ui.frameChangeShape.layout().addWidget(labelHeight, 1, 0)
            self.ui.frameChangeShape.layout().addWidget(labelRadius, 2, 0)
            self.ui.frameChangeShape.layout().addWidget(labelCellHeight, 3, 0)
            self.ui.frameChangeShape.layout().addWidget(labelCellRadius, 4, 0)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditScaleFigure, 0, 1)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditHeightFigure, 1, 1)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditRadiusFigure, 2, 1)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditCellHeightFigure, 3, 1)
            self.ui.frameChangeShape.layout().addWidget(self.lineEditCellRadiusFigure, 4, 1)
            self.ui.frameChangeShape.layout().setColumnStretch(2, 1)
            self.ui.frameChangeShape.layout().setRowStretch(5, 1)
        else:
            self.ui.groupBoxSTL.setDisabled(True)
            self.ui.pushButtonBlockMesh.setDisabled(True)
            self.resetSTL()

    def initSolver(self):
        """!
        @brief Метод инициализации виджета выбора решателя.

        Метод инициализации виджета выбора решателя.
        """

        self.ui.comboBoxSolver.clear()
        self.ui.comboBoxSolver.addItem("Не выбрано")
        self.ui.comboBoxSolver.addItem("icoFoam")
        self.ui.comboBoxSolver.addItem("laplacianFoam")
        self.ui.comboBoxSolver.currentIndexChanged.connect(self.changedSolver)
        self.ui.comboBoxSolver.currentIndexChanged.emit(0)

    def changedSolver(self):
        """!
        @brief Метод обработки изменения виджета выбора решателя.

        Метод обработки сигнала изменения виджета выбора решателя.
        """

        if (len(self.listConstants) != 0):
            self.removeAllConstants()
            self.listConstants.clear()
        if (len(self.listBeginValues) != 0):
            self.removeAllBeginValues()
            self.listBeginValues.clear()

        if (self.ui.comboBoxSolver.currentText() == "icoFoam"):
            self.fvSolution.setSolver("icoFoam")
            self.fvSchemes.setSolver("icoFoam")
            self.addConstant("ν", "0", "м²/с", "nu", "[0 2 -1 0 0 0 0]", "transportProperties", "transportProperties")
            self.addBeginValue("p", "volScalarField", "м²/с²", "p", "[0 2 -2 0 0 0 0]")
            self.addBeginValue("U", "volVectorField", "м/с", "U", "[0 1 -1 0 0 0 0]")
        elif (self.ui.comboBoxSolver.currentText() == "laplacianFoam"):
            self.fvSolution.setSolver("laplacianFoam")
            self.fvSchemes.setSolver("laplacianFoam")
            self.addConstant("DT", "0", "м²/с", "DT", "[0 2 -1 0 0 0 0]", "transportProperties", "transportProperties")
            self.addBeginValue("T", "volScalarField", "град", "T", "[0 0 0 1 0 0 0]")
        else:
            self.fvSolution.setSolver("")
            self.fvSchemes.setSolver("")

    def addConstant(self, name, value, unit, nameFoam, unitFoam, typeValue, nameFile):
        """!
        @brief Метод добавления констант.

        Метод добавления transport properties.
        @param name (str) - название (в программе)
        @param value (str) - значение
        @param unit (str) - единицы измерения (в программе)
        @param nameFoam (str) - название (в openFoam)
        @param unitFoam (str) - единицы измерения (в openFoam)
        @param typeValue (str) - тип константы (в openFoam)
        @param nameFile (str) - название файла, в котором будет хранится константа (в openFoam)
        """

        frameProperties = QFrame()
        layoutFrameProperties = QGridLayout()
        layoutFrameProperties.setSpacing(7)
        layoutFrameProperties.setContentsMargins(3, 3, 3, 3)

        labelTypeValue = QLabel()
        fontLabelTypeValue = QFont("Times", 8, QFont.Bold)
        labelTypeValue.setFont(fontLabelTypeValue)
        if(typeValue == "transportProperties"):
            labelTypeValue.setText("Транспортное свойство")
        else:
            labelTypeValue.setText("Неизвестное свойство")
        labelName = QLabel("Название")
        labelName.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        labelValue = QLabel("Значение")
        labelValue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        labelUnits = QLabel("Ед.изм")
        labelUnits.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        labelNameTransportProperty = QLabel(name)
        lineEditValueTransportProperty = QLineEdit(value)
        labelUnitTransportProperty = QLabel(unit)
        self.listConstants.append([nameFoam, lineEditValueTransportProperty, unitFoam, typeValue, nameFile])
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layoutFrameProperties.addWidget(line, 0, 0, 1, 3)
        layoutFrameProperties.addWidget(labelTypeValue, 1, 0, 1, 3)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layoutFrameProperties.addWidget(line, 2, 0, 1, 3)
        layoutFrameProperties.addWidget(labelName, 3, 0)
        layoutFrameProperties.addWidget(labelValue, 3, 1)
        layoutFrameProperties.addWidget(labelUnits, 3, 2)
        layoutFrameProperties.addWidget(labelNameTransportProperty, 4, 0)
        layoutFrameProperties.addWidget(lineEditValueTransportProperty, 4, 1)
        layoutFrameProperties.addWidget(labelUnitTransportProperty, 4, 2)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layoutFrameProperties.addWidget(line, 5, 0, 1, 3)

        frameProperties.setLayout(layoutFrameProperties)
        self.ui.scrollAreaWidgetConstant.layout().addWidget(frameProperties,
                                                            self.ui.scrollAreaWidgetConstant.layout().rowCount(), 0)
        self.ui.scrollAreaWidgetConstant.layout().setRowStretch(self.ui.scrollAreaWidgetConstant.layout().rowCount()-1, 0)
        self.ui.scrollAreaWidgetConstant.layout().setRowStretch(self.ui.scrollAreaWidgetConstant.layout().rowCount(), 1)

    def removeAllConstants(self):
        """!
        @brief Метод очистки всех констант из программы.

        Метод очистки всех констант из программы. Для их очистки из папки проекта необходимо сохранить изменения.
        """

        if (self.ui.scrollAreaWidgetConstant.layout() is not None):
            for i in reversed(range(self.ui.scrollAreaWidgetConstant.layout().count())):
                item = self.ui.scrollAreaWidgetConstant.layout().itemAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.ui.scrollAreaWidgetConstant.layout().removeItem(item)
            for i in range(self.ui.scrollAreaWidgetConstant.layout().rowCount()):
                self.ui.scrollAreaWidgetConstant.layout().setRowStretch(i, 0)

    def clearFolderConstants(self):
        """!
        @brief Метод очистки всех констант из папки проекта.

        Метод очистки всех констант из папки проекта. Данный метод выполняется во время сохранения изменений.
        """

        pathDir = self.pathProj + "\\constant"
        if os.path.exists(pathDir):
            listDir = os.listdir(pathDir)
            for file in listDir:
                filePath = os.path.join(pathDir, file)
                if os.path.isfile(filePath):
                    os.remove(filePath)

    def changedTypeValue(self, lineEdit, index):
        """!
        @brief Метод отключения изменения значений при zeroGradient.

        Метод который деактивирует виджет изменения значений в области начальных значений.
        @param lineEdit (QLineEdit) - виджет Qt
        @param index (int) - индекс текущего типа значения
        """

        if(index == 0):
            lineEdit.setDisabled(True)
        else:
            lineEdit.setDisabled(False)

    def addBeginValue(self, name="", typeValue="", unit="-", nameFoam="", unitFoam="",
                      inner="0",
                      front="0",
                      back="0",
                      right="0",
                      left="0",
                      top="0",
                      bottom="0",
                      stl="0"):
        """!
        @brief Метод добавления начальных значений.

        Метод добавления начальных значений.
        @param name (str) - название (в программе)
        @param typeValue (str) - тип начального значения (пример: "volScalarField")
        @param unit (str) - единицы измерения (в программе)
        @param nameFoam (str) - название (в openFoam)
        @param unitFoam (str) - единицы измерения (в openFoam)
        @param inner (str) - значение внутри фигуры
        @param front (str) - значение спереди
        @param back (str) - значение сзадаи
        @param right (str) - значение справа
        @param left (str) - значение слева
        @param top (str) - значение сверху
        @param bottom (str) - значение снизу
        @param stl (str) - значение в stl (если имеется stl)
        """

        frameProperties = QFrame()
        layoutFrameProperties = QGridLayout()
        layoutFrameProperties.setVerticalSpacing(7)
        layoutFrameProperties.setHorizontalSpacing(10)
        layoutFrameProperties.setContentsMargins(0, 0, 5, 0)

        labelName = QLabel(" Название переменной")
        fontLabelName = QFont("Times", 8, QFont.Bold)
        labelName.setFont(fontLabelName)
        self.labelNameValueBeginValue = QLabel("\t" + name)
        self.labelNameValueBeginValue.setFont(fontLabelName)

        labelTypeName = QLabel(" Тип значения")
        labelTypeNameValue = QLabel()
        if typeValue == "volScalarField":
            labelTypeNameValue.setText("\tскаляр")
        elif typeValue == "volVectorField":
            labelTypeNameValue.setText("\tвектор")

        labelUnit = QLabel(" Ед.изм")
        self.labelUnitsBeginValue = QLabel(unit)

        labelInner = QLabel(" Значение внутри")

        labelFront = QLabel("\tЗначение спереди")
        labelFrontType = QLabel("\t\tТип")
        labelFrontValue = QLabel("\t\tЗначение")

        labelBack = QLabel("\tЗначение сзади")
        labelBackType = QLabel("\t\tТип")
        labelBackValue = QLabel("\t\tЗначение")

        labelRight = QLabel("\tЗначение справа")
        labelRightType = QLabel("\t\tТип")
        labelRightValue = QLabel("\t\tЗначение")

        labelLeft = QLabel("\tЗначение слева")
        labelLeftType = QLabel("\t\tТип")
        labelLeftValue = QLabel("\t\tЗначение")

        labelTop = QLabel("\tЗначение сверху")
        labelTopType = QLabel("\t\tТип")
        labelTopValue = QLabel("\t\tЗначение")

        labelBottom = QLabel("\tЗначение снизу")
        labelBottomType = QLabel("\t\tТип")
        labelBottomValue = QLabel("\t\tЗначение")

        comboBoxFrontTypeBeginValue = QComboBox()
        comboBoxFrontTypeBeginValue.addItems(["zeroGradient", "fixedValue"])
        comboBoxBackTypeBeginValue = QComboBox()
        comboBoxBackTypeBeginValue.addItems(["zeroGradient", "fixedValue"])
        comboBoxRightTypeBeginValue = QComboBox()
        comboBoxRightTypeBeginValue.addItems(["zeroGradient", "fixedValue"])
        comboBoxLeftTypeBeginValue = QComboBox()
        comboBoxLeftTypeBeginValue.addItems(["zeroGradient", "fixedValue"])
        comboBoxTopTypeBeginValue = QComboBox()
        comboBoxTopTypeBeginValue.addItems(["zeroGradient", "fixedValue"])
        comboBoxBottomTypeBeginValue = QComboBox()
        comboBoxBottomTypeBeginValue.addItems(["zeroGradient", "fixedValue"])

        if typeValue == "volVectorField":
            if inner == "0":
                inner = "(0 0 0)"
            if front == "0":
                front = "(0 0 0)"
            if back == "0":
                back = "(0 0 0)"
            if right == "0":
                right = "(0 0 0)"
            if left == "0":
                left = "(0 0 0)"
            if top == "0":
                top = "(0 0 0)"
            if bottom == "0":
                bottom = "(0 0 0)"

        lineEditInnerValueBeginValue = QLineEdit(inner)
        lineEditFrontValueBeginValue = QLineEdit(front)
        lineEditBackValueBeginValue = QLineEdit(back)
        lineEditRightValueBeginValue = QLineEdit(right)
        lineEditLeftValueBeginValue = QLineEdit(left)
        lineEditTopValueBeginValue = QLineEdit(top)
        lineEditBottomValueBeginValue = QLineEdit(bottom)

        comboBoxFrontTypeBeginValue.currentIndexChanged.connect(partial(self.changedTypeValue, lineEditFrontValueBeginValue))
        comboBoxFrontTypeBeginValue.currentIndexChanged.emit(0)
        comboBoxBackTypeBeginValue.currentIndexChanged.connect(partial(self.changedTypeValue, lineEditBackValueBeginValue))
        comboBoxBackTypeBeginValue.currentIndexChanged.emit(0)
        comboBoxRightTypeBeginValue.currentIndexChanged.connect(partial(self.changedTypeValue, lineEditRightValueBeginValue))
        comboBoxRightTypeBeginValue.currentIndexChanged.emit(0)
        comboBoxLeftTypeBeginValue.currentIndexChanged.connect(partial(self.changedTypeValue, lineEditLeftValueBeginValue))
        comboBoxLeftTypeBeginValue.currentIndexChanged.emit(0)
        comboBoxTopTypeBeginValue.currentIndexChanged.connect(partial(self.changedTypeValue, lineEditTopValueBeginValue))
        comboBoxTopTypeBeginValue.currentIndexChanged.emit(0)
        comboBoxBottomTypeBeginValue.currentIndexChanged.connect(partial(self.changedTypeValue, lineEditBottomValueBeginValue))
        comboBoxBottomTypeBeginValue.currentIndexChanged.emit(0)

        self.listBeginValues.append([nameFoam, typeValue, unitFoam,
                                     lineEditInnerValueBeginValue,
                                     comboBoxFrontTypeBeginValue,
                                     lineEditFrontValueBeginValue,
                                     comboBoxBackTypeBeginValue,
                                     lineEditBackValueBeginValue,
                                     comboBoxRightTypeBeginValue,
                                     lineEditRightValueBeginValue,
                                     comboBoxLeftTypeBeginValue,
                                     lineEditLeftValueBeginValue,
                                     comboBoxTopTypeBeginValue,
                                     lineEditTopValueBeginValue,
                                     comboBoxBottomTypeBeginValue,
                                     lineEditBottomValueBeginValue
                                     ])

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layoutFrameProperties.addWidget(line, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelName, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(self.labelNameValueBeginValue, layoutFrameProperties.rowCount() - 1, 1)
        layoutFrameProperties.addWidget(labelTypeName, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(labelTypeNameValue, layoutFrameProperties.rowCount() - 1, 1)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layoutFrameProperties.addWidget(line, layoutFrameProperties.rowCount(), 0, 1, 2)

        layoutFrameProperties.addWidget(labelUnit, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(self.labelUnitsBeginValue, layoutFrameProperties.rowCount() - 1, 1)

        layoutFrameProperties.addWidget(labelInner, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(lineEditInnerValueBeginValue, layoutFrameProperties.rowCount() - 1, 1)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layoutFrameProperties.addWidget(line, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelFront, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelFrontType, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(comboBoxFrontTypeBeginValue, layoutFrameProperties.rowCount() - 1, 1)
        layoutFrameProperties.addWidget(labelFrontValue, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(lineEditFrontValueBeginValue, layoutFrameProperties.rowCount() - 1, 1)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layoutFrameProperties.addWidget(line, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelBack, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelBackType, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(comboBoxBackTypeBeginValue, layoutFrameProperties.rowCount() - 1, 1)
        layoutFrameProperties.addWidget(labelBackValue, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(lineEditBackValueBeginValue, layoutFrameProperties.rowCount() - 1, 1)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layoutFrameProperties.addWidget(line, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelRight, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelRightType, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(comboBoxRightTypeBeginValue, layoutFrameProperties.rowCount() - 1, 1)
        layoutFrameProperties.addWidget(labelRightValue, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(lineEditRightValueBeginValue, layoutFrameProperties.rowCount() - 1, 1)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layoutFrameProperties.addWidget(line, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelLeft, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelLeftType, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(comboBoxLeftTypeBeginValue, layoutFrameProperties.rowCount() - 1, 1)
        layoutFrameProperties.addWidget(labelLeftValue, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(lineEditLeftValueBeginValue, layoutFrameProperties.rowCount() - 1, 1)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layoutFrameProperties.addWidget(line, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelTop, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelTopType, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(comboBoxTopTypeBeginValue, layoutFrameProperties.rowCount() - 1, 1)
        layoutFrameProperties.addWidget(labelTopValue, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(lineEditTopValueBeginValue, layoutFrameProperties.rowCount() - 1, 1)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layoutFrameProperties.addWidget(line, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelBottom, layoutFrameProperties.rowCount(), 0, 1, 2)
        layoutFrameProperties.addWidget(labelBottomType, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(comboBoxBottomTypeBeginValue, layoutFrameProperties.rowCount() - 1, 1)
        layoutFrameProperties.addWidget(labelBottomValue, layoutFrameProperties.rowCount(), 0)
        layoutFrameProperties.addWidget(lineEditBottomValueBeginValue, layoutFrameProperties.rowCount() - 1, 1)

        if self.ui.labelNameSTL.text() != "Не выбран":
            labelSTL = QLabel("\tЗначение STL")
            labelSTLType = QLabel("\t\tТип")
            labelSTLValue = QLabel("\t\tЗначение")
            comboBoxSTLTypeBeginValue = QComboBox()
            comboBoxSTLTypeBeginValue.addItems(["zeroGradient", "fixedValue"])
            lineEditSTLValueBeginValue = QLineEdit(stl)

            comboBoxSTLTypeBeginValue.currentIndexChanged.connect(partial(self.changedTypeValue, lineEditSTLValueBeginValue))
            comboBoxSTLTypeBeginValue.currentIndexChanged.emit(0)

            self.listBeginValues[-1].append(comboBoxSTLTypeBeginValue)
            self.listBeginValues[-1].append(lineEditSTLValueBeginValue)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            layoutFrameProperties.addWidget(line, layoutFrameProperties.rowCount(), 0, 1, 2)
            layoutFrameProperties.addWidget(labelSTL, layoutFrameProperties.rowCount(), 0, 1, 2)
            layoutFrameProperties.addWidget(labelSTLType, layoutFrameProperties.rowCount(), 0)
            layoutFrameProperties.addWidget(comboBoxSTLTypeBeginValue, layoutFrameProperties.rowCount() - 1, 1)
            layoutFrameProperties.addWidget(labelSTLValue, layoutFrameProperties.rowCount(), 0)
            layoutFrameProperties.addWidget(lineEditSTLValueBeginValue, layoutFrameProperties.rowCount() - 1, 1)

        frameProperties.setLayout(layoutFrameProperties)
        self.ui.scrollAreaWidgetBeginValues.layout().addWidget(frameProperties,
                                                               self.ui.scrollAreaWidgetBeginValues.layout().rowCount(),
                                                               0)

    def removeAllBeginValues(self):
        """!
        @brief Метод очистки всех начальных значений из программы.

        Метод очистки всех начальных значений из программы. Для их очистки из папки проекта необходимо сохранить изменения.
        """

        if (self.ui.scrollAreaWidgetBeginValues.layout() is not None):
            for i in reversed(range(self.ui.scrollAreaWidgetBeginValues.layout().count())):
                item = self.ui.scrollAreaWidgetBeginValues.layout().itemAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.ui.scrollAreaWidgetBeginValues.layout().removeItem(item)

    def clearFolderBeginValues(self):
        """!
        @brief Метод очистки всех начальных значений из папки проекта.

        Метод очистки всех начальных значений из папки проекта. Данный метод выполняется во время сохранения изменений.
        """

        pathDir = self.pathProj + "\\0"
        if os.path.exists(pathDir):
            listDir = os.listdir(pathDir)
            for file in listDir:
                filePath = os.path.join(pathDir, file)
                if os.path.isfile(filePath):
                    os.remove(filePath)

    def parseProj(self, pathBlockMeshDict):
        """!
        @brief Метод парсинга данных для открытия созданного проекта.

        Метод парсинга данных для открытия созданного проекта.
        """

        file = open(pathBlockMeshDict, "r")
        data = file.read()
        file.close()

        startIndex = data.find("blockMeshDict")
        if (startIndex != -1):
            endIndex = data.find("\n", startIndex)
            settingsBlockMeshDict = data[startIndex:endIndex].split(" ")[-1].split(",")
            self.ui.comboBoxChangeFigure.setCurrentIndex(int(settingsBlockMeshDict[0]))
            if (self.ui.comboBoxChangeFigure.currentText() == "Параллелепипед"):
                self.lineEditScaleFigure.setText(settingsBlockMeshDict[1])
                self.lineEditWidthFigure.setText(settingsBlockMeshDict[2])
                self.lineEditHeightFigure.setText(settingsBlockMeshDict[3])
                self.lineEditLengthFigure.setText(settingsBlockMeshDict[4])
                self.lineEditCellWidthFigure.setText(settingsBlockMeshDict[5])
                self.lineEditCellHeightFigure.setText(settingsBlockMeshDict[6])
                self.lineEditCellLengthFigure.setText(settingsBlockMeshDict[7])
            elif (self.ui.comboBoxChangeFigure.currentText() == "Cфера"):
                self.lineEditScaleFigure.setText(settingsBlockMeshDict[1])
                self.lineEditRadiusFigure.setText(settingsBlockMeshDict[2])
                self.lineEditCellFigure.setText(settingsBlockMeshDict[3])
            elif (self.ui.comboBoxChangeFigure.currentText() == "Цилиндр"):
                self.lineEditScaleFigure.setText(settingsBlockMeshDict[1])
                self.lineEditHeightFigure.setText(settingsBlockMeshDict[2])
                self.lineEditRadiusFigure.setText(settingsBlockMeshDict[3])
                self.lineEditCellHeightFigure.setText(settingsBlockMeshDict[4])
                self.lineEditCellRadiusFigure.setText(settingsBlockMeshDict[5])

        startIndex = data.find("controlDict")
        if (startIndex != -1):
            endIndex = data.find("\n", startIndex)
            settingsControlDict = data[startIndex:endIndex].split(" ")[-1].split(",")
            self.ui.comboBoxSolver.setCurrentIndex(int(settingsControlDict[0]))
            self.ui.lineEditStartTime.setText(settingsControlDict[1])
            self.ui.lineEditEndTime.setText(settingsControlDict[2])
            self.ui.lineEditStepTime.setText(settingsControlDict[3])

        pathFile = self.pathProj + "\\system\\fvSchemes"
        if os.path.exists(pathFile):
            fileOut = open(pathFile, "r")
            textFile = fileOut.read()
            fileOut.close()
            self.fvSchemes.setText(textFile)

        pathFile = self.pathProj + "\\system\\fvSolution"
        if os.path.exists(pathFile):
            fileOut = open(pathFile, "r")
            textFile = fileOut.read()
            fileOut.close()
            self.fvSolution.setText(textFile)

        startIndex = data.find("STL")
        if (startIndex != -1):
            endIndex = data.find("\n", startIndex)
            settingsSTL = data[startIndex:endIndex].split(" ")
            if (len(settingsSTL) > 1):
                pathDir = self.pathProj + "\\constant\\triSurface"
                if not os.path.exists(pathDir):
                    os.makedirs(pathDir)
                pathSTL = self.pathProj + "\\constant\\triSurface\\" + settingsSTL[-1]
                self.loadSTL(pathSTL)

        startIndex = data.find("constants")
        if (startIndex != -1):
            endIndex = data.find("\n", startIndex)
            settingsConstants = data[startIndex:endIndex].split(" ")
            if (len(self.listConstants) != 0 and len(settingsConstants) > 1):
                for i in range(1,len(settingsConstants),2):
                    self.listConstants[int(i/2)][1].setText(settingsConstants[i+1])

        startIndex = data.find("beginValues")
        if (startIndex != -1):
            endIndex = data.find("\n", startIndex)

            for i in range(len(self.listBeginValues)):
                val = self.listBeginValues[i]
                settingsBeginValues = data[startIndex:endIndex].split(" ")[i + 1].split(",")
                val[3].setText(settingsBeginValues[0].replace("_", " "))
                val[4].setCurrentIndex(int(settingsBeginValues[1]))
                val[5].setText(settingsBeginValues[2].replace("_", " "))
                val[6].setCurrentIndex(int(settingsBeginValues[3]))
                val[7].setText(settingsBeginValues[4].replace("_", " "))
                val[8].setCurrentIndex(int(settingsBeginValues[5]))
                val[9].setText(settingsBeginValues[6].replace("_", " "))
                val[10].setCurrentIndex(int(settingsBeginValues[7]))
                val[11].setText(settingsBeginValues[8].replace("_", " "))
                val[12].setCurrentIndex(int(settingsBeginValues[9]))
                val[13].setText(settingsBeginValues[10].replace("_", " "))
                val[14].setCurrentIndex(int(settingsBeginValues[11]))
                val[15].setText(settingsBeginValues[12].replace("_", " "))
                if len(val) > 16:
                    val[16].setCurrentIndex(int(settingsBeginValues[13]))
                    val[17].setText(settingsBeginValues[14].replace("_", " "))


if __name__ == "__main__":
    """!
    @brief Основная точка входа в приложение.

    Основная точка входа в приложение.
    """

    app = QApplication(sys.argv)
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
