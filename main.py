from tkinter import Tk
from repositorio.database import inicializar_db

def main():
    inicializar_db()

    # La importación va acá adentro para que la DB
    # esté lista antes de que la vista arranque
    from vista.ventana_principal import VentanaPrincipal
    root = Tk()
    app = VentanaPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()