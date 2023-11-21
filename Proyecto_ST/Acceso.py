from tkinter import *
from tkinter import messagebox
import sqlite3
from index import Empleados

def usuario_existe(Usuario):
    conn = sqlite3.connect("Base_de_datos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE Usuario=?", (Usuario,))
    existe = cursor.fetchone() is not None
    return existe

def registrar_usuario(Usuario, Contraseña):
    try:
        if usuario_existe(Usuario):
            messagebox.showerror("Error", "Este usuario ya existe. Por favor, elige otro.")
            return

        conn = sqlite3.connect("Base_de_datos.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios (Usuario,Password) VALUES( ?, ?)", (Usuario, Contraseña))
        conn.commit()
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar el usuario. Error: {e}")

def crear_ventana_registro(ventana_anterior):
    ventana_anterior.destroy()

    reg = Tk()
    reg.title("StaffTrack")
    reg.geometry(f"{reg.winfo_screenwidth()}x{reg.winfo_screenheight()}")
    reg.config(bg="white")

    marco = Frame(reg, height=85, bg="#d3d2d1")
    marco.pack(fill='x', expand=False)

    lm = Label(marco, text="StaffTrack", font=("Courier", 50, "bold"), fg="#404040", bg="#d3d2d1")
    lm.place(x=5, y=2)

    lm2 = Label(marco, text="Acceso", font=("Courier", 15, "bold"), fg="#404040", bg="#d3d2d1")
    lm2.place(x=1100, y=55)
    lm2.bind("<Button-1>", lambda event: crear_ventana_acceso(reg))

    lm3 = Label(marco, text="Registro", font=("Courier", 15, "bold"), fg="#404040", bg="#d3d2d1")
    lm3.place(x=1200, y=55)
    lm3.bind("<Button-1>", lambda event: crear_ventana_registro(reg))

    mr = Frame(reg, height=525, width=400)
    mr.config(bg="#404040")
    mr.place(x=450, y=150)

    lmr1 = Label(mr, text="REGISTRO", font=("Courier", 20, "bold"), fg="white", bg="#404040")
    lmr1.place(x=135, y=30)

    lmr2 = Label(mr, text="Usuario:", font=("Courier", 20, "bold"), fg="white", bg="#404040")
    lmr2.place(x=20, y=100)

    ctr1 = Entry(mr, font=("Courier", 20,))
    ctr1.place(x=35, y=150)

    lmr3 = Label(mr, text="Contraseña:", font=("Courier", 20, "bold"), fg="white", bg="#404040")
    lmr3.place(x=20, y=215)

    ctr2 = Entry(mr, font=("Courier", 20,), show="*")
    ctr2.place(x=35, y=265)

    lmr3 = Label(mr, text="Confirmar contraseña:", font=("Courier", 20, "bold"), fg="white", bg="#404040")
    lmr3.place(x=20, y=330)

    ctr3 = Entry(mr, font=("Courier", 20,), show="*")
    ctr3.place(x=35, y=380)

    def on_registrar_click():
        Usuario = ctr1.get()
        Contraseña = ctr2.get()
        confirmar_contrasena = ctr3.get()

        if Contraseña != confirmar_contrasena:
            messagebox.showerror("Error", "Las contraseñas no coinciden. Inténtalo de nuevo.")
            return

        registrar_usuario(Usuario, Contraseña)

    btn = Button(mr, text="Registrar", font=("Courier", 15, "bold"), fg="#404040", command=on_registrar_click)
    btn.place(x=130, y=470)

    reg.iconbitmap("icono.ico")

    reg.mainloop()

def crear_ventana_acceso(ventana_anterior):
    ventana_anterior.destroy()

    acc = Tk()
    acc.title("StaffTrack")
    acc.geometry(f"{acc.winfo_screenwidth()}x{acc.winfo_screenheight()}")
    acc.config(bg="white")

    marco = Frame(acc, height=85, bg="#d3d2d1")
    marco.pack(fill='x', expand=False)

    lm = Label(marco, text="StaffTrack", font=("Courier", 50, "bold"), fg="#404040", bg="#d3d2d1")
    lm.place(x=5, y=2)

    lm2 = Label(marco, text="Acceso", font=("Courier", 15, "bold"), fg="#404040", bg="#d3d2d1")
    lm2.place(x=1100, y=55)
    lm2.bind("<Button-1>", lambda event: crear_ventana_acceso(acc))

    lm3 = Label(marco, text="Registro", font=("Courier", 15, "bold"), fg="#404040", bg="#d3d2d1")
    lm3.place(x=1200, y=55)
    lm3.bind("<Button-1>", lambda event: crear_ventana_registro(acc))

    ma = Frame(acc, height=430, width=400)
    ma.config(bg="#404040")
    ma.place(x=450, y=150)

    lma1 = Label(ma, text="ACCESO", font=("Courier", 20, "bold"), fg="white", bg="#404040")
    lma1.place(x=145, y=30)

    lma2 = Label(ma, text="Usuario:", font=("Courier", 20, "bold"), fg="white", bg="#404040")
    lma2.place(x=20, y=100)

    ctr1 = Entry(ma, font=("Courier", 20,))
    ctr1.place(x=35, y=150)

    lmr3 = Label(ma, text="Contraseña:", font=("Courier", 20, "bold"), fg="white", bg="#404040")
    lmr3.place(x=20, y=215)

    ctr2 = Entry(ma, font=("Courier", 20,), show="*")
    ctr2.place(x=35, y=265)

    def on_acceder_click():
        Usuario = ctr1.get()
        Contraseña = ctr2.get()

        if not usuario_existe(Usuario):
            messagebox.showerror("Error", "Usuario no registrado. Por favor, regístrate primero.")
            return

        conn = sqlite3.connect("Base_de_datos.db")

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Usuarios WHERE Usuario=? AND Password=?", (Usuario, Contraseña))
            existe = cursor.fetchone() is not None

            if existe:
                crear_ventana_empleados(acc)  # Pasa 'acc' como el argumento 'ventana_anterior'

            else:
                messagebox.showerror("Error", "Contraseña incorrecta. Inténtalo de nuevo.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error de base de datos: {e}")
        finally:
            conn.close()


    btn = Button(ma, text="Acceder", font=("Courier", 15, "bold"), fg="#404040", command=on_acceder_click)
    btn.place(x=130, y=330)

    acc.iconbitmap("icono.ico")

    acc.mainloop()


def crear_ventana_empleados(ventana_anterior):
    ventana_anterior.destroy()
    ve = Tk()
    ve.geometry()
    va = Empleados(ve)
    ve.mainloop()

    
if __name__ == "__main__":
    ventana_principal = Tk()
    ventana_principal.geometry()
    crear_ventana_registro(ventana_principal)
