import tkinter as tk
from tkinter import messagebox
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
import principal
from cryptography.fernet import Fernet
from PyQt5.QtCore import QRect


from PyQt5.QtCore import QCoreApplication, Qt, QPropertyAnimation
from PyQt5.QtCore import Qt, QCoreApplication, QPropertyAnimation, QEasingCurve

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()

        # Cargar la interfaz de usuario desde el archivo .ui
        loadUi("resources/login.ui", self)
        self.closeApp.clicked.connect(self.cerrar_app)
        self.minApp.clicked.connect(self.minimizar_app)
        self.ver.clicked.connect(self.contrasena_visible)
        
        self.setWindowTitle("Registro")  # Título de la ventana
        #Quitar los bordes por defecto de la ventana
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.continueB.clicked.connect(lambda: self.validar(self.passEdit.text()))

    # Métodos de la ventana
    def minimizar_app(self):
        # Minimizar la ventana principal
        self.showMinimized()
    def cerrar_app(self):
        # Mediante este metodo cerramos la aplicacion
        QCoreApplication.quit()

    def mousePressEvent(self, event):
        # Guardar la posición del ratón en la ventana
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        # Obtener la posición actual del ratón y mover la ventana
        x = event.globalX()
        y = event.globalY()
        self.move(x - self.offset.x(), y - self.offset.y())
    
    def contrasena_visible(self):
        if self.passEdit.echoMode() == QtWidgets.QLineEdit.Password:
            self.passEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.ver.setIcon(QIcon('resources/hide.png'))
        else:
            self.passEdit.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ver.setIcon(QIcon('resources/show.png'))
    def mostrarMensaje(self,titulo,mensaje):
        # Configurar la ventana
        ventana = tk.Tk()
        ventana.withdraw()
        # Mostrar el cuadro de mensaje
        messagebox.showinfo(title=titulo, message=mensaje)

    def obtenerContrasena(self):
        line = self.desencriptar()

        campos = line.strip().split("|")
        if len(campos) == 2:
            _, contrasena = campos

        return contrasena
    
    def validar(self,contrasenaInput):
        contrasena=self.obtenerContrasena()

        if contrasenaInput==contrasena:
            #self.mostrarMensaje("Bienvenido","Contrasena correcta!")
            self.abrir_principal()
        else:
            self.mostrarMensaje("Error","Contrasena incorrecta!")
    
    def abrir_principal(self):
        self.hide()  # Ocultar ventana registro
        self.ventana_dos = principal.Principal()
        self.ventana_dos.show()

    def desplegar_menu(self):
        ancho = self.inside.width()
        
        if ancho == 0:
            extender = 300
        else:
            extender = 0
        self.animacion = QPropertyAnimation(self.inside, b'minimumWidth')
        self.animacion.setDuration(900)
        self.animacion.setStartValue(ancho)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve(QEasingCurve.InOutQuart)
        self.animacion.finished.connect(self.desplegar_botones)
        self.animacion.start()

    def desplegar_botones(self):
        alto1 = self.tab1.height()
        if alto1 == 0:
            extender1 = 50
        else:
            extender1 = 0
        self.animacion1 = QPropertyAnimation(self.tab1, b'minimumHeight')
        self.animacion1.setDuration(900)
        self.animacion1.setStartValue(alto1)
        self.animacion1.setEndValue(extender1)
        self.animacion1.setEasingCurve(QEasingCurve.InOutQuart)
        self.animacion1.start()

        extender1 = 30  # Altura final deseada
        self.animacion2 = QPropertyAnimation(self.tab1, b'geometry')
        self.animacion2.setDuration(900)
        self.animacion2.setStartValue(self.tab1.geometry())
        end_geometry1 = QRect(self.tab1.geometry().x(), extender1, self.tab1.geometry().width(), self.tab1.geometry().height())
        self.animacion2.setEndValue(end_geometry1)
        self.animacion2.setEasingCurve(QEasingCurve.InOutQuart)
        self.animacion2.start()

        alto2 = self.tab2.height()
        if alto2 == 0:
            extender2 = 50
        else:
            extender2 = 0
        self.animacion3 = QPropertyAnimation(self.tab2, b'minimumHeight')
        self.animacion3.setDuration(900)
        self.animacion3.setStartValue(alto2)
        self.animacion3.setEndValue(extender2)
        self.animacion3.setEasingCurve(QEasingCurve.InOutQuart)
        self.animacion3.start()

        extender2 = 30  # Altura final deseada
        self.animacion4 = QPropertyAnimation(self.tab2, b'geometry')
        self.animacion4.setDuration(900)
        self.animacion4.setStartValue(self.tab2.geometry())
        end_geometry2 = QRect(self.tab2.geometry().x(), extender2, self.tab2.geometry().width(), self.tab2.geometry().height())
        self.animacion4.setEndValue(end_geometry2)
        self.animacion4.setEasingCurve(QEasingCurve.InOutQuart)
        self.animacion4.start()
        
    def showEvent(self, event):
        self.desplegar_menu()
    
    def desencriptar(self):
        # Obtener la clave generada
        with open("data/key.key", "rb") as file:
            key = file.read()

        # Crear una instancia de la clase Fernet
        f = Fernet(key)

        ruta_archivo = 'data/guardado.txt'
        with open(ruta_archivo, 'rb') as archivo:
            contenido = archivo.read()
            contenido_desencriptado = f.decrypt(contenido)
            contenido_string = contenido_desencriptado.decode()  # Convertir a string
            return(contenido_string)
       
    

if __name__ == "__main__":
    app = QApplication([])
    window = Login()
    window.show()
    app.exec_()