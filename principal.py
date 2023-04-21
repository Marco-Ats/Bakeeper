import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt, QPropertyAnimation
from PyQt5.QtCore import Qt, QCoreApplication, QPropertyAnimation, QEasingCurve

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt

class Principal(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('resources/principal.ui', self)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.maximizar.clicked.connect(self.maximizeWindow)
        self.minimizar.clicked.connect(self.minimizar_app)
        self.cerrar.clicked.connect(self.cerrar_app)
        self.menuBtn.clicked.connect(self.mover_menu)
        self.ingredientes.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page1))
        self.recetas.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page2))
        self.tableWidget.setColumnCount(5)  # Establecer la cantidad de columnas en la tabla
        self.tableWidget.setHorizontalHeaderLabels(["Nombre", "Descripción", "Cantidad (g)", "Precio/Kg", "ID"])
        self.tableWidget.setStyleSheet("background-color: pink")  # Establecer el color de fondo de la tabla

        self.searchLineEdit.textChanged.connect(self.search_ingrediente)
        self.printButton.clicked.connect(self.imprimir_producto)
        self.mostrar_todos_ingredientes()

    def mostrar_todos_ingredientes(self):
        self.tableWidget.setRowCount(0)

        with open("ingredientes.txt", "r", encoding="utf-8") as file:
            for line in file:
                fields = line.strip().split("|")
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                for i, field in enumerate(fields):
                    self.tableWidget.setItem(row_position, i, QTableWidgetItem(field))

        if self.tableWidget.rowCount() == 0:
            self.printButton.setEnabled(False)
        else:
            self.printButton.setEnabled(True)

    def search_ingrediente(self):
        search_text = self.searchLineEdit.text().lower()
        self.tableWidget.setRowCount(0)  # Limpiar la tabla antes de agregar nuevos resultados

        with open("ingredientes.txt", "r", encoding='utf-8') as file:
            for line in file:
                fields = line.strip().split("|")
                nombre = fields[0].lower()
                if search_text in nombre:  # Buscar coincidencias por nombre
                    row_position = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_position)
                    for i, field in enumerate(fields):
                        self.tableWidget.setItem(row_position, i, QTableWidgetItem(field))

        if self.tableWidget.rowCount() == 0:
            self.tableWidget.hide()
            self.printButton.setEnabled(False)
        else:
            self.tableWidget.show()
            self.printButton.setEnabled(True)

    def imprimir_producto(self):
        selected_rows = self.tableWidget.selectedItems()
        if len(selected_rows) == 0:
            print("¡No has seleccionado ningún producto!")
        else:
            producto = [selected_rows[i].text() for i in range(5)]
            print("Producto seleccionado:", producto)

    def mousePressEvent(self, event):
        # Guardar la posición del ratón en la ventana
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        # Obtener la posición actual del ratón y mover la ventana
        x = event.globalX()
        y = event.globalY()
        self.move(x - self.offset.x(), y - self.offset.y())

    def maximizeWindow(self):
        if self.isMaximized():
            self.maximizar.setIcon(QIcon('resources/maximizar.png'))
            self.showNormal()
        else:
            self.maximizar.setIcon(QIcon('resources/squares.png'))
            self.showMaximized()
    def minimizar_app(self):
        # Minimizar la ventana principal
        self.showMinimized()
    def cerrar_app(self):
        # Mediante este metodo cerramos la aplicacion
        QCoreApplication.quit()

    def mover_menu(self):
        ancho= self.menu_barra.width()
        
        if ancho == 0:
            extender = 250
        else:
            extender = 0
        self.animacion = QPropertyAnimation(self.menu_barra, b'minimumWidth')
        self.animacion.setDuration(300)
        self.animacion.setStartValue(ancho)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve(QEasingCurve.InOutQuart)
        self.animacion.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Principal()
    window.show()
    sys.exit(app.exec_())