# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1044, 753)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_2.setHorizontalSpacing(7)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1044, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menubar)
        self.menu_5.setObjectName("menu_5")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionFAO = QtWidgets.QAction(MainWindow)
        self.actionFAO.setObjectName("actionFAO")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.actionCreateProject = QtWidgets.QAction(MainWindow)
        self.actionCreateProject.setObjectName("actionCreateProject")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAddConstant = QtWidgets.QAction(MainWindow)
        self.actionAddConstant.setObjectName("actionAddConstant")
        self.actionAddBeginValue = QtWidgets.QAction(MainWindow)
        self.actionAddBeginValue.setObjectName("actionAddBeginValue")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.actionOpenProjFolder = QtWidgets.QAction(MainWindow)
        self.actionOpenProjFolder.setObjectName("actionOpenProjFolder")
        self.actionOpenProject = QtWidgets.QAction(MainWindow)
        self.actionOpenProject.setObjectName("actionOpenProject")
        self.actionSaveChangesProject = QtWidgets.QAction(MainWindow)
        self.actionSaveChangesProject.setObjectName("actionSaveChangesProject")
        self.actionConsole = QtWidgets.QAction(MainWindow)
        self.actionConsole.setCheckable(True)
        self.actionConsole.setObjectName("actionConsole")
        self.actionEditfvSchemes = QtWidgets.QAction(MainWindow)
        self.actionEditfvSchemes.setObjectName("actionEditfvSchemes")
        self.actionEditfvSolution = QtWidgets.QAction(MainWindow)
        self.actionEditfvSolution.setObjectName("actionEditfvSolution")
        self.actionResiduals = QtWidgets.QAction(MainWindow)
        self.actionResiduals.setObjectName("actionResiduals")
        self.actionParaView = QtWidgets.QAction(MainWindow)
        self.actionParaView.setObjectName("actionParaView")
        self.menu.addAction(self.actionOpenProject)
        self.menu.addAction(self.actionCreateProject)
        self.menu.addSeparator()
        self.menu.addAction(self.actionSaveChangesProject)
        self.menu.addSeparator()
        self.menu.addAction(self.actionQuit)
        self.menu_2.addAction(self.actionParaView)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.actionResiduals)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.actionOpenProjFolder)
        self.menu_3.addAction(self.actionFAO)
        self.menu_4.addAction(self.actionConsole)
        self.menu_5.addAction(self.actionEditfvSchemes)
        self.menu_5.addAction(self.actionEditfvSolution)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GUI openFoam"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Tab 1"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.menu_2.setTitle(_translate("MainWindow", "Инструменты"))
        self.menu_3.setTitle(_translate("MainWindow", "Справка"))
        self.menu_4.setTitle(_translate("MainWindow", "Вид"))
        self.menu_5.setTitle(_translate("MainWindow", "Редактирование"))
        self.actionFAO.setText(_translate("MainWindow", "О программе"))
        self.action_2.setText(_translate("MainWindow", "Открыть проект"))
        self.actionCreateProject.setText(_translate("MainWindow", "Новый проект"))
        self.actionCreateProject.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionQuit.setText(_translate("MainWindow", "Выйти"))
        self.actionAddConstant.setText(_translate("MainWindow", "Добавить константу"))
        self.actionAddBeginValue.setText(_translate("MainWindow", "Добавить начальное значение"))
        self.action_4.setText(_translate("MainWindow", "Открыть папку с проектом"))
        self.actionOpenProjFolder.setText(_translate("MainWindow", "Открыть папку с проектом в проводнике"))
        self.actionOpenProject.setText(_translate("MainWindow", "Открыть проект"))
        self.actionOpenProject.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSaveChangesProject.setText(_translate("MainWindow", "Сохранить изменения"))
        self.actionSaveChangesProject.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionConsole.setText(_translate("MainWindow", "Консоль"))
        self.actionEditfvSchemes.setText(_translate("MainWindow", "Файл fvSchemes"))
        self.actionEditfvSolution.setText(_translate("MainWindow", "Файл fvSolution"))
        self.actionResiduals.setText(_translate("MainWindow", "Графики остатков моделирования"))
        self.actionParaView.setText(_translate("MainWindow", "Открыть модель в ParaView"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
