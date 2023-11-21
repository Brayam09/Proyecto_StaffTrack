from tkinter import ttk
from tkinter import *
import sqlite3

class Empleados():
    DB_NAME = "Base_de_datos.db"
    COLUMNS = ("Nombre", "Cargo", "Salario")

    def __init__(self, window):
        self.wind = window
        self.wind.title("StaffTrack")
        self.create_widgets()
        window.iconbitmap("icono.ico")
        self.get_empleados()

    def create_widgets(self):
        # Configuración de weight para que se expanda con el cambio de tamaño
        self.wind.columnconfigure(0, weight=1)
        self.wind.rowconfigure(0, weight=1)

        marco_superior = Frame(self.wind, height=85, bg="#d3d2d1")
        marco_superior.grid(row=0, column=0, columnspan=2, sticky="ew")

        lm = Label(marco_superior, text="StaffTrack", font=("Courier", 50, "bold"), fg="#404040", bg="#d3d2d1")
        lm.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        marco = LabelFrame(self.wind, text="Registrar un Empleado", background="#a3e9a4")
        marco.grid(row=1, column=0, columnspan=2, pady=20, sticky="nsew")
            
        # Ingresar un nombre
        Label(marco, text="Nombre").grid(row=1, column=0)
        self.name = Entry(marco)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # Ingresar un cargo
        Label(marco, text="Cargo").grid(row=2, column=0)
        self.cargo = Entry(marco)
        self.cargo.grid(row=2, column=1)

        # Ingresar un Salario
        Label(marco, text="Salario").grid(row=3, column=0)
        self.salario = Entry(marco)
        self.salario.grid(row=3, column=1)

        # Boton para agregar producto
        ttk.Button(marco, text="Guardar empleado", command=self.add_empleado).grid(row=4, columnspan=2, sticky=W + E)

        # Salida para mensajes
        self.mensaje = Label(self.wind, text="", fg="red")
        self.mensaje.grid(row=7, column=0, columnspan=2, sticky=W + E)

        # Barra de busqueda
        self.search_label = Label(marco, text="Buscar:")
        self.search_label.grid(row=0, column=2)

        self.search_entry = Entry(marco)
        self.search_entry.grid(row=0, column=3)

        ttk.Button(marco, text="Buscar", command=self.search_empleados).grid(row=0, column=4)

        # Tabla
        self.tree = ttk.Treeview(height=10, columns=self.COLUMNS)
        self.tree.grid(row=5, column=0, columnspan=2, sticky='nsew')
        for col in self.COLUMNS:
            self.tree.heading(col, text=col, anchor=CENTER)

        # Botones
        ttk.Button(text="Eliminar", command=self.eliminar_empleado).grid(row=6, column=0, sticky=W + E)
        ttk.Button(text="Editar", command=self.editar_empleado).grid(row=6, column=1, sticky=W + E)


    def search_empleados(self):
        search_term = self.search_entry.get()
        query = "SELECT * FROM Empleados WHERE Nombre LIKE ?"
        parameters = ('%' + search_term + '%', )
        db_rows = self.run_query(query, parameters)

        # Limpiar la tabla
        self.clear_table()

        # Mostrar mensaje si no se encontraron resultados
        if not db_rows:
            self.mensaje["text"] = f"Empleado '{search_term}' no encontrado."
        else:
            # Agregar empleados filtrados a la tabla
            for row in db_rows:
                self.tree.insert('', 0, values=(row[1], row[2], row[3]))
            self.mensaje["text"] = ""  # Limpiar mensaje si se encontraron resultados

    def clear_table(self):
        # Limpiar la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

    def run_query(self, query, parameters=()):
        try:
            with sqlite3.connect(self.DB_NAME) as conn:
                cursor = conn.cursor()
                resultado = cursor.execute(query, parameters)
                conn.commit()
                return resultado
        except sqlite3.Error as e:
            print("Error de base de datos:", e)

    def get_empleados(self):
        # Limpiando la tabla
        self.clear_table()

        # Consultando los datos
        query = "SELECT * FROM Empleados ORDER BY Nombre DESC"
        db_rows = self.run_query(query)

        # Agregando empleados a la tabla
        for row in db_rows:
            self.tree.insert('', 0, values=(row[1], row[2], row[3]))

    def validacion(self):
        return len(self.name.get()) != 0 and len(self.cargo.get()) != 0 and len(self.salario.get()) != 0

    def add_empleado(self):
        if self.validacion():
            query = "INSERT INTO Empleados (Nombre, Cargo, Salario) VALUES( ?, ?, ?)"
            parametros = (self.name.get(), self.cargo.get(), self.salario.get())
            self.run_query(query, parametros)
            nombre_empleado = self.name.get()
            self.mensaje["text"] = f"Empleado {nombre_empleado} guardado correctamente"
            self.name.delete(0, END)
            self.cargo.delete(0, END)
            self.salario.delete(0, END)
            self.get_empleados()
        else:
            self.mensaje["text"] = "Nombre, Cargo y Salario son requeridos"

    def eliminar_empleado(self):
        self.mensaje["text"] = ""
        selected_item = self.tree.selection()
        if not selected_item:
            self.mensaje["text"] = "Por favor selecciona un registro"
            return

        nombre = self.tree.item(selected_item, 'values')[0]
        query = "DELETE FROM Empleados WHERE Nombre = ?"

        try:
            self.run_query(query, (nombre,))
            self.mensaje["text"] = "El dato {} ha sido eliminado".format(nombre)
        except sqlite3.Error as e:
            self.mensaje["text"] = "Error al eliminar el dato: {}".format(str(e))
        finally:
            self.get_empleados()

    def editar_empleado(self):
        self.mensaje["text"] = ""
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                raise IndexError("Por favor selecciona un registro")

            name = self.tree.item(selected_item, 'values')[0]
            cargo = self.tree.item(selected_item, 'values')[1]
            salario = self.tree.item(selected_item, 'values')[2]

            self.edit_wind = Toplevel()
            self.edit_wind.title("Editar Empleado")

            # Nombre anterior
            Label(self.edit_wind, text="Nombre Anterior: ").grid(row=0, column=0)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name), state="readonly").grid(row=0,
                                                                                                              column=1)

            # Cargo anterior
            Label(self.edit_wind, text="Cargo Anterior: ").grid(row=1, column=0)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=cargo), state="readonly").grid(row=1,
                                                                                                              column=1)

            # Salario anterior
            Label(self.edit_wind, text="Salario Anterior: ").grid(row=2, column=0)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=salario), state="readonly").grid(row=2,
                                                                                                                column=1)

            # Nombre nuevo
            Label(self.edit_wind, text="Nuevo Nombre: ").grid(row=3, column=0)
            nuevo_nombre = Entry(self.edit_wind)
            nuevo_nombre.grid(row=3, column=1)

            # Cargo nuevo
            Label(self.edit_wind, text="Nuevo Cargo: ").grid(row=4, column=0)
            nuevo_cargo = Entry(self.edit_wind)
            nuevo_cargo.grid(row=4, column=1)

            # Salario nuevo
            Label(self.edit_wind, text="Nuevo Salario: ").grid(row=5, column=0)
            nuevo_salario = Entry(self.edit_wind)
            nuevo_salario.grid(row=5, column=1)

            # Boton para actualizar
            Button(self.edit_wind, text="Actualizar",
                   command=lambda: self.edit_records(nuevo_nombre.get(), name, nuevo_cargo.get(),
                                                     nuevo_salario.get())).grid(row=6, column=1, sticky=W)

        except IndexError as e:
            self.mensaje["text"] = str(e)

    def edit_records(self, nuevo_nombre, name, nuevo_cargo, nuevo_salario):
        query = "UPDATE Empleados SET Nombre = ?, Cargo = ?, Salario = ? WHERE Nombre = ?"
        parameters = (nuevo_nombre, nuevo_cargo, nuevo_salario, name)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.mensaje["text"] = "Registro {} actualizado correctamente".format(name)
        self.get_empleados()

if __name__ == "__main__":
    window = Tk()
    window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")

    # Configuración de weight para que se expanda con el cambio de tamaño
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    aplicacion = Empleados(window)

    window.mainloop()



