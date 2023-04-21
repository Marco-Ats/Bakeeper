from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QCoreApplication, Qt
import login, ctypes, os
import cryptography.fernet

def abrir_login():
    app = QApplication([])
    window = login.Login()
    window.show()
    app.exec_()

def abrir_registro():
    app = QApplication([])
    window = Registro()
    window.show()
    app.exec_()

class Registro(QMainWindow):
    def __init__(self):
        super(Registro, self).__init__()

        # Cargar la interfaz de usuario desde el archivo .ui
        loadUi("resources/registro.ui", self)

        self.setWindowTitle("Registro")  # Título de la ventana
         # Botones de la ventana
        self.closeApp.clicked.connect(self.cerrar_app)
        self.minApp.clicked.connect(self.minimizar_app)
        # Sombreado del boton de login
        self.pushButton = self.findChild(QtWidgets.QPushButton, "continueB")
        self.pushButton.pressed.connect(lambda: self.pushButton.setStyleSheet("QPushButton { background-color: rgb(125, 125, 125); font: 30pt 'Brush Script MT';}"))
        self.pushButton.released.connect(lambda: self.pushButton.setStyleSheet("background-color: rgb(170, 170, 255);font: 30pt 'Brush Script MT';"))
        self.continueB.clicked.connect(self.guardar_texto)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ver_1.clicked.connect(self.contrasena_visible_1)
        self.ver_2.clicked.connect(self.contrasena_visible_2)

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
    
    def abrir_login(self):
        self.hide()  # Ocultar ventana registro
        self.ventana_dos = login.Login()
        self.ventana_dos.show()

    def guardar_texto(self):
        if self.lineEdit_2.text() == self.lineEdit_3.text():

            nombre = self.lineEdit.text()
            contrasena = self.lineEdit_2.text()
            if nombre and contrasena:
                self.carpeta_oculta()
                self.encriptar(nombre + '|' + contrasena + '\n')
                self.lineEdit.clear()
                self.lineEdit.setFocus()
                self.lineEdit_2.clear()
                self.lineEdit_2.setFocus()

                login.Login.mostrarMensaje(self,"Registro exitoso","Se ha registrado con exito!")
                self.abrir_login()
        else:
            login.Login.mostrarMensaje(self,"Error","Las contrasenas no coinciden")

    def contrasena_visible_1(self):
        if self.lineEdit_2.echoMode() == QtWidgets.QLineEdit.Password:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.ver_1.setIcon(login.QIcon('resources/hide.png'))
        else:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ver_1.setIcon(login.QIcon('resources/show.png'))

    def contrasena_visible_2(self):
        if self.lineEdit_3.echoMode() == QtWidgets.QLineEdit.Password:
            self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.ver_2.setIcon(login.QIcon('resources/hide.png'))
        else:
            self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ver_2.setIcon(login.QIcon('resources/show.png'))

    def carpeta_oculta(self):
        ruta = "./data"

        # Comprobar si la carpeta no existe
        if not os.path.exists(ruta):
            # Crear la carpeta
            os.makedirs(ruta)

            # Cambiar los atributos de la carpeta para que sea oculta en Windows
            if os.name == 'nt':  # Windows
                try:
                    attrs = ctypes.windll.kernel32.GetFileAttributesW(ruta)
                    attrs |= 0x02  # Atributo de archivo oculto
                    ctypes.windll.kernel32.SetFileAttributesW(ruta, attrs)
                except Exception as e:
                    print("No se pudo establecer el atributo oculto en la carpeta:", e)
        else:
            print("La carpeta 'data' ya existe.")

    def encriptar(self,data):
        # Generar una clave aleatoria para el cifrado
        clave = cryptography.fernet.Fernet.generate_key()

        # Crear un objeto Fernet con la clave generada
        fernet = cryptography.fernet.Fernet(clave)

        contenido = data
        contenido_bytes = contenido.encode()  # Convertir a bytes

        # Encriptar los datos en formato de bytes
        contenido_cifrado = fernet.encrypt(contenido_bytes)

        # Escribir el contenido cifrado en un nuevo archivo
        ruta_archivo_cifrado = 'data/guardado.txt'
        with open(ruta_archivo_cifrado, 'wb') as archivo_cifrado:
            archivo_cifrado.write(contenido_cifrado)

        # Guardar la clave en un archivo
        ruta_clave = 'data/key.key'
        with open(ruta_clave, 'wb') as archivo_clave:
            archivo_clave.write(clave)
    

if __name__ == "__main__":
    filename = "data/guardado.txt"

    if os.path.isfile(filename):
        if os.path.getsize(filename) > 0:
            abrir_login()
        else:
            os.remove('data/guardado.txt')
            abrir_registro()

    else:
        print("El archivo no existe.")
        abrir_registro()
