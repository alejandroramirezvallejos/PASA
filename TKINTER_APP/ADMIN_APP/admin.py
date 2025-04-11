""" pip install tk
    pip install pyodbc
    pip install tkcalendar
    pip install pillow
    pip install customtkinter
"""
import sys
import tkinter as tk
from tkinter import ttk
import pyodbc
from tkinter import messagebox, font
from tkcalendar import Calendar
from datetime import date
from PIL import Image, ImageTk
import customtkinter as ctk
from customtkinter import CTkComboBox, CTkButton, CTkEntry, set_appearance_mode, set_default_color_theme, CTkImage
import functions_query as f
import conection as c
import json
window = None
current_frame = None
add_frame = None
option_frame = None
update_frame = None
delete_frame = None
fetch_frame = None
navigation_bar = None
action_bar = None
start_frame = None
register_frame = None
login_frame = None
terms_frame = None
loading_frame = None
all_frames = []
entries = []
selected_option = ""
role_input = None
last_table_window = None
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ----------------------------------------------------ENTRADA Y SALIDA DE DATOS-----------------------------------------------------------------------------------------------

"""Guardar Datos al Crear una Cuenta"""
def create_account():
    # Entrada de Datos
    global fetch_frame, name_entry, last_name_entry, age_entry, id_card_entry, password_entry
    name = name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    age = age_entry.get().strip()
    id_card = id_card_entry.get().strip()
    password = password_entry.get().strip()
    # Manejo de Errores
    if not all([name]):
        messagebox.showerror("Error", "Debes ingresar tu Nombre")
        return
    if not all([last_name]):
        messagebox.showerror("Error", "Debes ingresar tus Apellidos")
        return
    if not all([age]):
        messagebox.showerror("Error", "Debes ingresar tu Edad")
        return
    if not age.isdigit():
        messagebox.showerror("Error", "Tu Edad debe ser un numero natural")
        return
    if not int(age) >= 18:
        messagebox.showerror("Error", "No puedes Crear una Cuenta si eres menor de edad")
        return
    if not all([id_card]):
        messagebox.showerror("Error", "Debes ingresar tu Numero de Carnet")
        return
    if not id_card.isdigit():
        messagebox.showerror("Error", "El Numero de Carnet debe ser un numero natural")
        return
    if not len(id_card) == 7:
        messagebox.showerror("Error", "El Numero de Carnet debe tener 7 digitos")
        return
    if f.validate_carnet(id_card)==True:
        messagebox.showerror("Error", "Carnet ya existente")
        return
    if not all([password]):
        messagebox.showerror("Error", "Debes crear una Contraseña")
        return
    # Borrar Datos en caso de Error
    name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    id_card_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    # Conexion con la Base de Datos
    connection = c.make_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute(f"EXEC sp_insertar_usuario {f.obtain_pk(cursor,'usuario')},'{name}', '{last_name}', {age}, {id_card}, '{password}'")
        connection.commit()
        # Cambiar al start_frame si todo sale bien
        messagebox.showinfo("Exito", f"Usuario {id_card} creado con exito")
        show_frame(start_frame)
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al registrar la cuenta: {e}")
    finally:
        connection.close()

"""Extraer Datos para Verificar el Inicio de Sesion"""
def login():
    # Entrada de Datos
    global fetch_frame, role_input
    id_card = login_id_card_entry.get().strip()
    password = login_password_entry.get().strip()
    # Verificar la correcta Entrada de Datos
    if not all([id_card]):
        messagebox.showerror("Error", "Debes ingresar tu Numero de Carnet")
        return
    if not id_card.isdigit():
        messagebox.showerror("Error", "El Numero de Carnet debe ser un numero natural")
        return
    if not len(id_card) == 7:
        messagebox.showerror("Error", "El Numero de Carnet debe tener 7 digitos")
        return
    if not all([password]):
        messagebox.showerror("Error", "Debes ingresar tu Contraseña")
        return
    if role_input == "Seleccionar":
        messagebox.showerror("Error", "Debes seleccionar un rol válido.")
        return
    if role_input.get() == "DBA":
        c.username = 'dba'
        c.password = 'dba'
    if role_input.get() == "Gerente":
        c.username = 'gerente'
        c.password = 'gerente'
    if role_input.get() == "Trabajador":
        c.username = 'vendedor'
        c.password = 'vendedor'
    # Borrar Datos en caso de Error
    login_id_card_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)
    role_input.set("Seleccionar")
    print(c.username)
    # Conexion con la Base de Datos
    connection = c.make_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute(f"sp_obtener_admin '{id_card}', '{password}'")
        usuario = cursor.fetchone()
        # Cambiar al fetch_frame si todo sale bien
        if usuario:
            show_frame(fetch_frame)
        else:
            messagebox.showerror("Error", "Datos incorrectos. Verifique su usuario y contraseña")
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al realizar la consulta: {e}")
    finally:
        connection.close()

"""Funcion para Realizar Consultas"""
def queries_option():
    global current_frame, selected_option, entries
    connection = c.make_connection()
    if not connection:
        return
    cursor = connection.cursor()
    try:
        if current_frame == add_frame:
            action = "add"
        elif current_frame == delete_frame:
            action = "delete"
        elif current_frame == update_frame:
            action = "update"
        else:
            messagebox.showerror("Error", "Operación no válida o Frame desconocido.")
            return
        if action == "add":
            if "Agregar Bus" in selected_option:
                chofer_id = int(entries[0].get())
                ruta_id = int(entries[1].get())
                fecha_sal=(entries[2].get())
                fecha_ret=(entries[3].get())
                f.add_bus(chofer_id,ruta_id,fecha_sal,fecha_ret)
                messagebox.showinfo("Éxito", "Bus agregado correctamente.")
            elif "Agregar Chofer" in selected_option:
                nombre = entries[4].get()
                edad = int(entries[5].get())
                carnet = int(entries[6].get())
                f.add_driver(nombre, edad, carnet)
                messagebox.showinfo("Éxito", "Chofer agregado correctamente")
            elif "Agregar Ruta" in selected_option:
                dep_inicio = entries[7].get()
                dep_final = entries[8].get()
                costo = float(entries[9].get())
                costo_vip = float(entries[10].get())
                f.add_route(dep_inicio, dep_final, costo, costo_vip)
                messagebox.showinfo("Éxito", "Ruta agregada correctamente")
        elif action == "delete":
            #------------------------------------------ Logica ---------------------------------------
            
            # lo que esta en comentario no se elimina son las funciones de eliminar fisica no logica . ahi van las nuevas que tiene que hacer fer
            if "Eliminar Bus Logica" in selected_option:
                try:
                # Intentar convertir a entero
                    bus_id = int(entries[0].get())
                    print(bus_id)
                    f.del_bus_logic(bus_id)
                    messagebox.showinfo("Éxito", "bus eliminado correctamente")
                except ValueError:
                    resultadobus_id = open_table_window_obtain(f.get_bus, "buses")
                    if resultadobus_id and len(resultadobus_id) > 0:
                        bus_id = int(resultadobus_id[0])
                        print(bus_id)
                        f.del_bus_logic(bus_id)
                        messagebox.showinfo("Éxito", "bus eliminado correctamente")
                    else:
                        messagebox.showwarning("Advertencia", "No se selecciono ningun bus")
           
            elif "Eliminar Chofer Logica" in selected_option:
                try:
                # Intentar convertir a entero
                    chofer_id = int(entries[1].get())
                    print(chofer_id)
                    f.del_driver_logic(chofer_id)
                    messagebox.showinfo("Éxito", "Chofer eliminado correctamente")
                except ValueError:
                    resultadoscl = open_table_window_obtain(f.get_chofer, "choferes")
                    if resultadoscl and len(resultadoscl) > 0:
                        chofer_id = int(resultadoscl[0])
                        print(chofer_id)
                        f.del_driver_logic(chofer_id)
                        messagebox.showinfo("Éxito", "Chofer eliminado correctamente")
                    else:
                        messagebox.showwarning("Advertencia", "No se selecciono ningun chofer")
                
            elif "Eliminar Ruta Logica" in selected_option:
                try:
                # Intentar convertir a entero
                    ruta_id = int(entries[2].get())
                    print(ruta_id)
                    f.del_route_logic(ruta_id)
                    messagebox.showinfo("Éxito", "Ruta eliminada correctamente")
                except ValueError:
                    resultadoruta_id = open_table_window_obtain(f.get_route, "rutas")
                    if resultadoruta_id and len(resultadoruta_id) > 0:
                        ruta_id = int(resultadoruta_id[0])
                        print(ruta_id)
                        f.del_route_logic(ruta_id)
                        messagebox.showinfo("Éxito", "Ruta eliminada correctamente")
                    else:
                        messagebox.showwarning("Advertencia", "No se selecciono ninguna ruta")



            elif "Eliminar Usuario Logica" in selected_option:
                try:
                # Intentar convertir a entero
                    usuario_id = int(entries[3].get())
                    print(usuario_id)
                    f.del_usuario_logic(usuario_id)
                    messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                except ValueError:
                    resultadosusuario_id = open_table_window_obtain(f.get_usuarios, "usuarios")
                    if resultadosusuario_id and len(resultadosusuario_id) > 0:
                        usuario_id = int(resultadosusuario_id[0])
                        print(usuario_id)
                        f.del_usuario_logic(usuario_id)
                        messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                    else:
                        messagebox.showwarning("Advertencia", "No se selecciono ningun usuario")



            #-------------------------------Fisica-------------------------------


            elif "Eliminar Bus" in selected_option:
                try:
                # Intentar convertir a entero
                    bus_id = int(entries[4].get())
                    print(bus_id)
                    f.del_bus(bus_id)
                    messagebox.showinfo("Éxito", "Bus eliminado correctamente")
                except ValueError:
                    resultadosbus_id2 = open_table_window_obtain(f.get_bus, "buses")   
                    if resultadosbus_id2 and len(resultadosbus_id2) > 0:
                        bus_id = int(resultadosbus_id2[0])
                        print(bus_id)
                        f.del_bus(bus_id)
                        messagebox.showinfo("Éxito", "Bus eliminado correctamente")
                    else:
                        messagebox.showwarning("Advertencia", "No se selecciono ningun bus")      

           
            elif "Eliminar Chofer" in selected_option:
                try:
                # Intentar convertir a entero
                    chofer_id = int(entries[5].get())
                    print(chofer_id)
                    f.del_driver(chofer_id)
                    messagebox.showinfo("Éxito", "Chofer eliminado correctamente")
                except ValueError:
                    resultadochofer_id2 = open_table_window_obtain(f.get_chofer, "choferes")
                    if resultadochofer_id2 and len(resultadochofer_id2) > 0:
                        chofer_id = int(resultadochofer_id2[0])
                        print(chofer_id)
                        f.del_driver(chofer_id)
                        messagebox.showinfo("Éxito", "Chofer eliminado correctamente")
                    else:
                        messagebox.showwarning("Advertencia", "No se selecciono ningun chofer")

            elif "Eliminar Ruta" in selected_option:
                try:
                # Intentar convertir a entero
                    ruta_id = int(entries[6].get())
                    print(ruta_id)
                    f.del_route(ruta_id)
                    messagebox.showinfo("Éxito", "Ruta eliminada correctamente")
                except ValueError:
                    resultadoruta_id2 = open_table_window_obtain(f.get_route, "rutas")
                    if resultadoruta_id2 and len(resultadoruta_id2) > 0:
                        ruta_id = int(resultadoruta_id2[0])
                        print(ruta_id)
                        f.del_route(ruta_id)
                        messagebox.showinfo("Éxito", "Ruta eliminada correctamente")
                    else:
                        messagebox.showwarning("Advertencia", "No se selecciono ninguna ruta")



            elif "Eliminar Usuario" in selected_option:
                try:
                # Intentar convertir a entero
                    usuario_id = int(entries[7].get())
                    print(usuario_id)
                    f.del_usuario(usuario_id)
                    messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                except ValueError:
                    resiltadousuario_id2 = open_table_window_obtain(f.get_usuarios, "usuarios")
                    if resiltadousuario_id2 and len(resiltadousuario_id2) > 0:
                        usuario_id = int(resiltadousuario_id2[0])
                        print(usuario_id)
                        f.del_usuario(usuario_id)
                        messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                    else:
                        messagebox.showwarning("Advertencia", "No se selecciono ningun usuario")

        elif action == "update":
            if "Actualizar Bus" in selected_option:
                try:
                    bus_id = int(entries[0].get())
                    chofer_id = int(entries[1].get())
                    ruta_id = int(entries[2].get())
                    fecha_sal=(entries[3].get())
                    fecha_ret=(entries[4].get())
                    print(bus_id, chofer_id, ruta_id, fecha_sal, fecha_ret)
                    f.update_bus(bus_id,  chofer_id, ruta_id,fecha_sal,fecha_ret)
                    messagebox.showinfo("Éxito", "Bus actualizado correctamente")
                except ValueError:
                    resultadosbus = open_table_window_obtain(f.get_bus_elimacion, "buses")
                    if resultadosbus:
                        entries[0].delete(0, tk.END)
                        entries[0].insert(0, str(resultadosbus[0]))  # ID Bus
                        entries[1].delete(0, tk.END)
                        entries[1].insert(0, str(resultadosbus[1]))  # ID Chofer
                        entries[2].delete(0, tk.END)
                        entries[2].insert(0, str(resultadosbus[4]))  # ID Ruta
                        entries[3].delete(0, tk.END)
                        entries[3].insert(0, resultadosbus[5])       # Fecha Salida
                        entries[4].delete(0, tk.END)
                        entries[4].insert(0, resultadosbus[6])       # Fecha Retorno
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar el bus: {e}")

               
            #    messagebox.showinfo("Éxito", "Bus actualizado correctamente")
            elif "Actualizar Chofer" in selected_option:
                try:
                    nombre = entries[5].get()
                    chofer_id = int(entries[6].get())
                    edad = int(entries[7].get())
                    carnet = int(entries[8].get())

                    print(nombre, chofer_id, edad, carnet)
                    f.update_driver(chofer_id, nombre, edad, carnet)
                    messagebox.showinfo("Éxito", "Chofer actualizado correctamente")
                except ValueError:
                    resultadoschofer = open_table_window_obtain(f.get_chofer, "choferes")
                    if resultadoschofer:
                        entries[5].delete(0, tk.END)
                        entries[5].insert(0, str(resultadoschofer[1]))
                        entries[6].delete(0, tk.END)
                        entries[6].insert(0, str(resultadoschofer[0]))
                        entries[7].delete(0, tk.END)
                        entries[7].insert(0, str(resultadoschofer[3]))
                        entries[8].delete(0, tk.END)
                        entries[8].insert(0, str(resultadoschofer[2]))
                   
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar el chofer: {e}")
            
            elif "Actualizar Ruta" in selected_option:
                try:
                    ruta_id = int(entries[9].get())
                    dep_inicio = entries[10].get()
                    dep_final = entries[11].get()
                    costo = int(entries[12].get())
                    costo_vip = int(entries[13].get())
                    print(ruta_id, dep_inicio, dep_final, costo, costo_vip)

                    f.update_route(ruta_id,dep_inicio,dep_final,costo,costo_vip)
                    messagebox.showinfo("Éxito", "Ruta actualizado correctamente")
                except ValueError:
                    resultadosruta = open_table_window_obtain(f.get_route, "rutas")
                    if resultadosruta:
                        entries[9].delete(0, tk.END)
                        entries[9].insert(0, str(resultadosruta[0]))
                        entries[10].delete(0, tk.END)
                        entries[10].insert(0, str(resultadosruta[1]))
                        entries[11].delete(0, tk.END)
                        entries[11].insert(0, str(resultadosruta[2]))
                        entries[12].delete(0, tk.END)
                        entries[12].insert(0, str(resultadosruta[3]))
                        entries[13].delete(0, tk.END)
                        entries[13].insert(0, str(resultadosruta[4]))
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar la ruta: {e}")

                
               
            elif "Actualizar Usuario" in selected_option:
                try:
                    usuario_id=int(entries[14].get())
                    nombre=entries[15].get()
                    apellido=entries[16].get()
                    edad=int(entries[17].get())
                    carnet=entries[18].get()
                    if(len(carnet)!=7):
                        raise ValueError("El carnet tiene que tener 7 digitos y no existir")
                    contraseña=entries[19].get()
                    if(entries[20].get()=="True"):
                        admin=1
                    elif(entries[20].get()=="False"):
                        admin=0
                    else:
                        admin=int(entries[20].get())
                    if(admin!=1 and admin!=0):
                        raise ValueError("El campo admin solo puede ser 0 (No) o 1 (Sí)")
                    
                    print(usuario_id,nombre,apellido,edad,carnet,contraseña,admin)
                    f.update_user(usuario_id,nombre,apellido,edad,carnet,contraseña,admin)
                    messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                except ValueError:
                    resultadosusuario = open_table_window_obtain(f.get_usuarios, "usuarios")
                    if resultadosusuario:
                        entries[14].delete(0, tk.END)
                        entries[14].insert(0, str(resultadosusuario[0]))
                        entries[15].delete(0, tk.END)
                        entries[15].insert(0, str(resultadosusuario[1]))
                        entries[16].delete(0, tk.END)
                        entries[16].insert(0, str(resultadosusuario[2]))
                        entries[17].delete(0, tk.END)
                        entries[17].insert(0, str(resultadosusuario[3]))
                        entries[18].delete(0, tk.END)
                        entries[18].insert(0, str(resultadosusuario[4]))
                        entries[20].delete(0, tk.END)
                        entries[20].insert(0, str(resultadosusuario[5]))
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar el usuario: {e}")


    except Exception as e:
        messagebox.showerror("Error",e)

"""Funcion para Mostrar el Boton de Historial"""
def show_history_button(target_frame=None):
    if history_button:
        history_button.place(x=25, y=9)  

"""Funcion para ocultar el Boton de Historial"""
def hide_history_button():
    if history_button:
        history_button.place_forget()

"""Funcion para ocultar Frame al apretar Boton de Historial"""
def on_history_button():
    global current_frame, fetch_frame, history_frame
    # Ocultar frame actual
    if current_frame == fetch_frame:
        fetch_frame.pack_forget()
    hide_history_button()
    history_frame = make_history_frame() 
    show_frame(history_frame)

# ------------------------------------------------------------FRAMES---------------------------------------------------------------------------------------------

"""Pantalla de Carga"""
def make_loading_screen():
    # Creando Frame
    loading_frame = tk.Frame(window, bg="#09090A")  
    loading_frame.name = "loading"
    loading_frame.pack(fill="both", expand=True)
    # Agregando Icono
    try:
        pasa_iso = "../../ASSETS/color_negative_admin.png"
        image = Image.open(pasa_iso)
        image = image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        iso_label = tk.Label(loading_frame, image=photo, bg="#09090A")  
        iso_label.image = photo  
        iso_label.pack(expand=True)
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Tiempo de Espera
    def delayed_show_start_frame():
        window.configure(bg="#09090A")
        show_frame(start_frame)
    window.after(1500, delayed_show_start_frame)
    return loading_frame

"""Frame de la Barra de Accion"""
def make_action_bar():
    # Creación del frame de la barra de acción
    action_bar = tk.Frame(window, bg="#09090A", width=380, height=40)
    action_bar.name = "action_bar"
    action_bar.pack(side="top", fill="x")
    # Agregar logo al centro
    try:
        pasa_logo = "../../ASSETS/logo_admin.png"
        logo_image = Image.open(pasa_logo).resize((56, 20), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(action_bar, image=logo_photo, bg="#09090A")
        logo_label.image = logo_photo
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Crear Boton para Regresar pero inicialmente ocultarlo
    try:
        back_image_path = "../../ASSETS/back_button_admin.png"
        back_image = Image.open(back_image_path).resize((12, 15), Image.LANCZOS)
        back_photo = ImageTk.PhotoImage(back_image)
        global back_button
        def on_back_button():
            global current_frame, login_frame, register_frame, start_frame, terms_frame, history_frame
            # Verificar desde qué frame se está presionando el Boton de Regreso
            if current_frame == login_frame:
                login_frame.pack_forget()
                hide_back_button()
                show_frame(start_frame)
            elif current_frame == register_frame:
                register_frame.pack_forget()
                hide_back_button()
                show_frame(start_frame)
            elif current_frame == terms_frame:
                terms_frame.pack_forget()
                hide_back_button()
                show_frame(start_frame)
            elif current_frame == history_frame:
                history_frame.pack_forget()
                hide_back_button()
                show_frame(fetch_frame)
        back_button = tk.Button(
            action_bar,
            image=back_photo,
            bg="#09090A",
            borderwidth=0,
            command=on_back_button
        )
        back_button.image = back_photo
        back_button.place(x=25, y=12) 
        back_button.place_forget()
    except Exception as e:
        print(f"Error al cargar el Boton Regresar: {e}")
    # Boton para Cerrar Sesion
    try:
        log_out_image_path = "../../ASSETS/log_out_button_admin.png"
        log_out_image = Image.open(log_out_image_path).resize((18, 18), Image.LANCZOS)
        log_out_photo = ImageTk.PhotoImage(log_out_image)
        global log_out_button
        def log_out_button():
            global current_frame, add_frame, fetch_frame, update_frame, delete_frame
            # Verificar desde qué frame se está presionando el Boton de Cerrar Sesion
            if current_frame == add_frame:
                add_frame.pack_forget()
                hide_log_out_button()
                show_frame(start_frame)
                hide_option()
            elif current_frame == fetch_frame:
                fetch_frame.pack_forget()
                hide_log_out_button()
                show_frame(start_frame)
                hide_option()
            elif current_frame == update_frame:
                update_frame.pack_forget()
                hide_log_out_button()
                hide_option()
                show_frame(start_frame)
                hide_option()
            elif current_frame == delete_frame:
                delete_frame.pack_forget()
                hide_log_out_button()
                hide_option()
                show_frame(start_frame)
        log_out_button = tk.Button(
            action_bar,
            image=log_out_photo,
            bg="#09090A",
            borderwidth=0,
            command=on_log_out_button
        )
        log_out_button.image = log_out_photo
        log_out_button.place(x=340, y=12)  
        log_out_button.place_forget()  
    except Exception as e:
        print(f"Error al cargar el Boton de Cerrar Sesion: {e}")
    # Crear Boton de Historial pero inicialmente ocultarlo
    try:
        history_image_path = "../../ASSETS/history_button_admin.png"
        history_image = Image.open(history_image_path).resize((17, 21), Image.LANCZOS)
        history_photo = ImageTk.PhotoImage(history_image)
        global history_button
        history_button = tk.Button(
            action_bar,
            image=history_photo,
            bg="#09090A",
            borderwidth=0,
            command=on_history_button
        )
        history_button.image = history_photo
        history_button.place(x=25, y=9) 
        history_button.place_forget()
    except Exception as e:
        print(f"Error al cargar el Boton de Historial: {e}")
    return action_bar

"""Frame de la Barra de Navegacion"""
def make_navigation_bar(window, add_frame, delete_frame, fetch_frame, update_frame):
    # Crear Frame
    navigation_bar = tk.Frame(window, bg="#09090A", height=60, width=380)
    navigation_bar.pack(side="bottom", fill="x")
    navigation_bar.pack_propagate(False)
    # Cargar Icono
    def load_icon(path, size=(24, 24)):
        try:
            image = Image.open(path)
            image = image.resize(size, Image.LANCZOS)
            return CTkImage(image, size=size)
        except Exception as e:
            print(f"Error al cargar el Icono {path}: {e}")
            return None
    # Iconos de Botones de Navegacion
    try:
        search_icon = load_icon("../../ASSETS/search_icon.png")
        add_icon = load_icon("../../ASSETS/add_icon.png")
        delete_icon = load_icon("../../ASSETS/delete_icon.png")
        update_icon = load_icon("../../ASSETS/update_icon.png")
    except Exception as e:
        print(f"Error al cargar los Iconos de la Barra de Navegacion {e}")
        add_icon = delete_icon = search_icon = update_icon = None
    # Estilo de Botones de Navegacion
    button_style = {
        'width': 80, 
        'height': 60, 
        'fg_color': "#09090A", 
        'hover_color': "#F0F0F0", 
        'text_color': "#7732FF"
    }
    # Botones de Navegacion
    fetch_button = ctk.CTkButton(
        navigation_bar, 
        text="Buscar", 
        image=search_icon, 
        command=lambda: show_frame(make_fetch_frame()),
        **button_style
    )
    fetch_button.pack(side="left", expand=True)
    add_button = ctk.CTkButton(
        navigation_bar, 
        text="Agregar", 
        image=add_icon, 
        command=lambda: show_frame(make_add_frame()),
        **button_style
    )
    add_button.pack(side="left", expand=True)
    delete_button = ctk.CTkButton(
        navigation_bar, 
        text="Eliminar", 
        image=delete_icon, 
        command=lambda: show_frame(make_delete_frame()),
        **button_style
    )
    delete_button.pack(side="left", expand=True)
    update_button = ctk.CTkButton(
        navigation_bar, 
        text="Modificar", 
        image=update_icon, 
        command=lambda: show_frame(make_update_frame()),
        **button_style
    )
    update_button.pack(side="left", expand=True)
    return navigation_bar

"""Frame Inicial"""
def make_start_frame():
    # Creacion del Frame
    start_frame = tk.Frame(window, bg="#09090A")
    start_frame.name = "start"
    # Agregando Icono
    try:
        pasa_iso = "../../ASSETS/color_positive_admin.png"
        image = Image.open(pasa_iso)
        image = image.resize((170, 170), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        iso_label = tk.Label(start_frame, image=photo, bg="#09090A")  
        iso_label.image = photo  
        iso_label.pack(expand=True)
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Texto
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        start_frame,
        text="¡Gestionar una Base de Datos nunca fue mas sencillo!",
        font=title_font,
        bg="#090906",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=50)
    # Boton de Inicio de Sesion
    login_button = CTkButton(
        start_frame,
        text="Iniciar Sesion",
        corner_radius=32,
        fg_color="#C8BCF6",
        text_color="#09090A",
        hover_color="#A79BE2",
        command=lambda: show_frame(login_frame),
    )
    login_button.pack(pady=10)
    # Boton de Creacion de Cuenta
    signup_button = CTkButton(
        start_frame,
        text="Crear cuenta",
        corner_radius=32,
        fg_color="#C8BCF6",
        text_color="#09090A",
        hover_color="#A79BE2",
        command=lambda: show_frame(register_frame),
    )
    signup_button.pack(pady=10)
    # Texto de Términos y Condiciones
    terms_label = tk.Label(
        start_frame,
        text="Al crear una cuenta, confirmo que he leído y acepto los ",
        font=("Arial", 10),
        bg="#09090A",
        fg="#C8BCF6",
    )
    terms_label.pack(pady=(30, 5), side="top", anchor="center")
    # Crear enlace para "Términos y condiciones"
    terms_link = tk.Label(
        start_frame,
        text="Terminos y Condiciones de Uso",
        font=("Arial", 10, "underline"),
        bg="#09090A",
        fg="#7732FF",
        cursor="hand2",
    )
    terms_link.pack(side="top", anchor="center")
    # Vincular el clic al enlace
    terms_link.bind("<Button-1>", lambda e: show_frame(terms_frame))
    return start_frame

"""Frame para ver los Terminos y Condiciones de Uso"""
def make_terms_frame():
    # Crear el frame de términos y condiciones
    terms_frame = tk.Frame(window, bg="#09090A")
    terms_frame.name = "terms"
    # Título principal
    title_label = tk.Label(
        terms_frame,
        text="Términos y Condiciones de Uso",
        font=("Arial", 16, "bold"),
        bg="#09090A",
        fg="#7732FF",
    )
    title_label.pack(pady=20)
    # Crear un Scrollbar
    scrollbar = tk.Scrollbar(terms_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas = tk.Canvas(terms_frame, bg="#09090A", yscrollcommand=scrollbar.set, bd=0, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.config(command=canvas.yview)
    # Agregando el Contenido
    content_text_frame = tk.Frame(canvas, bg="#09090A")
    canvas.create_window((0, 0), window=content_text_frame, anchor="nw")
    def resize_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    content_text_frame.bind("<Configure>", resize_canvas)
    # Contenido por Secciones
    sections = [
        (
            "1. Aceptación de los Términos",
            """Al crear una cuenta en nuestra plataforma, usted declara que ha leído, comprendido y aceptado en su totalidad los presentes Términos y Condiciones. Asimismo, se compromete a cumplir con todas las leyes, normativas y reglamentos aplicables, incluidos aquellos que pudieran requerir una interpretación exhaustiva."""
        ),
        (
            "2. Privacidad y Tratamiento de Datos",
            """Al aceptar, usted otorga permiso para que compartamos, distribuyamos o regalemos sus datos personales a entidades selectas. Estas pueden incluir agencias gubernamentales misteriosas, civilizaciones extraterrestres y organizaciones con nombres demasiado interesantes para ser ignorados. Nos reservamos el derecho de decidir, a nuestra entera discreción, las entidades receptoras de esta información, todo esto, por supuesto, en aras de la innovación, seguridad y el progreso."""
        ),
        (
            "3. Responsabilidades del Usuario",
            """Como usuario registrado, usted asume la obligación de colaborar con los proyectos y objetivos educativos establecidos por la plataforma. Esto incluye, pero no se limita a, garantizar un puntaje perfecto de 100 en cualquier examen final presentado por los creadores de esta aplicación."""
        ),
        (
            "4. Modificaciones a los Términos",
            """Nos reservamos el derecho de modificar estos términos en cualquier momento. No prometemos avisarle, pero contamos con su confianza ciega. La continuación en el uso de nuestra plataforma tras cualquier modificación implicará la aceptación implícita de los cambios realizados."""
        ),
        (
            "5. Limitación de Responsabilidad",
            """La plataforma no se hará responsable por cualquier consecuencia derivada del uso indebido de su tiempo, datos personales, o información sensible, incluyendo, pero no limitado a, datos bancarios o información financiera. Al aceptar estos términos, usted exonera a la plataforma de cualquier reclamación derivada de tales eventos."""
        ),
        (
            "6. Aceptación y Carácter Vinculante",
            """Al continuar con el uso de nuestros servicios, usted acepta de manera irrevocable y vinculante los presentes Términos y Condiciones, comprometiéndose a no impugnar su validez o aplicación en ningún momento."""
        ),
    ]
    # Secciones
    for title, content in sections:
        section_frame = tk.Frame(content_text_frame, bg="#09090A")
        section_frame.pack(fill="x", padx=20, pady=10)
        # Título en negrita
        title_label = tk.Label(
            section_frame,
            text=title,
            font=("Arial", 12, "bold"),
            bg="#09090A",
            fg="#7732FF",
            anchor="w",
        )
        title_label.pack(fill="x")
        # Contenido justificado
        content_text_label = tk.Label(
            section_frame,
            text=content,
            font=("Arial", 10),
            bg="#09090A",
            fg="#C8BCF6",
            anchor="w",
            justify="left",
            wraplength=335,
        )
        content_text_label.pack(fill="x")
    # Botón para regresar
    show_back_button(terms_frame)
    return terms_frame

"""Frame para Crear una Cuenta"""
def make_register_frame():
    global name_entry, last_name_entry, age_entry, id_card_entry, password_entry
    # Creando el Frame
    register_frame = tk.Frame(window, bg="#09090A")
    register_frame.name = "register"
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        register_frame,
        text="Crear Cuenta Administrativa",
        font=title_font,
        bg="#09090A",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=50)
    # Ingresando el Nombre
    name_frame = tk.Frame(register_frame, bg="#09090A")
    name_frame.pack(side="top", pady=10, fill="x", padx=10)
    name_label = tk.Label(name_frame, text="Nombre:", bg="#09090A", fg="#C8BCF6")
    name_label.pack(side="left", padx=10)
    name_entry = CTkEntry(
        name_frame,
        placeholder_text="Ingresar",
        border_color="#C8BCF6",
        corner_radius=32
    )
    name_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando los Apellidos
    last_name_frame = tk.Frame(register_frame, bg="#09090A")
    last_name_frame.pack(side="top", pady=10, fill="x", padx=10)
    last_name_label = tk.Label(last_name_frame, text="Apellidos:", bg="#09090A", fg="#C8BCF6")
    last_name_label.pack(side="left", padx=10)
    last_name_entry = CTkEntry(
        last_name_frame,
        placeholder_text="Ingresar",
        border_color="#C8BCF6",
        corner_radius=32
    )
    last_name_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando la Edad
    age_frame = tk.Frame(register_frame, bg="#09090A")
    age_frame.pack(side="top", pady=10, fill="x", padx=10)
    age_label = tk.Label(age_frame, text="Edad:", bg="#09090A", fg="#C8BCF6")
    age_label.pack(side="left", padx=10)
    age_entry = CTkEntry(
        age_frame,
        placeholder_text="Ingresar",
        border_color="#C8BCF6",
        corner_radius=32
    )
    age_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando el Carnet
    id_card_frame = tk.Frame(register_frame, bg="#09090A")
    id_card_frame.pack(side="top", pady=10, fill="x", padx=10)
    id_card_label = tk.Label(id_card_frame, text="Carnet:", bg="#09090A", fg="#C8BCF6")
    id_card_label.pack(side="left", padx=10)
    id_card_entry = CTkEntry(
        id_card_frame,
        placeholder_text="Ingresar",
        border_color="#C8BCF6",
        corner_radius=32
    )
    id_card_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando la Contraseña
    password_frame = tk.Frame(register_frame, bg="#09090A")
    password_frame.pack(side="top", pady=10, fill="x", padx=10)
    password_label = tk.Label(password_frame, text="Contraseña:", bg="#09090A", fg="#C8BCF6")
    password_label.pack(side="left", padx=10)
    password_entry = CTkEntry(
        password_frame,
        placeholder_text="Ingresar",
        show="*",
        border_color="#C8BCF6",
        corner_radius=32
    )
    password_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Boton para Crear Cuenta
    create_account_button = CTkButton(
        register_frame,
        text="Crear cuenta",
        corner_radius=32,
        fg_color="#C8BCF6",
        text_color="#09090A",
        hover_color="#A79BE2",
        command=create_account
    )
    create_account_button.pack(pady=10) 
    # Botón de Regreso
    show_back_button()
    return register_frame

"""Frame para Iniciar Sesion"""
def make_login_frame():
    global login_frame, login_id_card_entry, login_password_entry, role_input
    # Creando Frame
    login_frame = tk.Frame(window, bg="#09090A")
    login_frame.name = "login"
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        login_frame,
        text="Inicio de Sesion Administrativa",
        font=title_font,
        bg="#09090A",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=50)
    # Ingresando el Carnet
    login_id_card_frame = tk.Frame(login_frame, bg="#09090A")
    login_id_card_frame.pack(side="top", pady=10, fill="x", padx=10)
    login_id_card_label = tk.Label(login_id_card_frame, text="Carnet:", bg="#09090A", fg="#C8BCF6")
    login_id_card_label.pack(side="left", padx=10)
    login_id_card_entry = CTkEntry(
        login_id_card_frame,
        placeholder_text="Ingresar",
        border_color="#C8BCF6",
        corner_radius=32
    )
    login_id_card_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando la Contraseña
    login_password_frame = tk.Frame(login_frame, bg="#09090A")
    login_password_frame.pack(side="top", pady=10, fill="x", padx=10)
    login_password_label = tk.Label(login_password_frame, text="Contraseña:", bg="#09090A", fg="#C8BCF6")
    login_password_label.pack(side="left", padx=10)
    login_password_entry = CTkEntry(
        login_password_frame,
        placeholder_text="Ingresar",
        show="*",
        border_color="#C8BCF6",
        corner_radius=32
    )
    login_password_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Elegir Roles
    role_frame = tk.Frame(login_frame, bg="#09090A")
    role_frame.pack(side="top", pady=10, fill="x", padx=10)
    role_txt = tk.Label(role_frame, text="Rol:", bg="#09090A", fg="#C8BCF6")
    role_input = CTkComboBox(
        role_frame,
        values=["DBA", "Gerente", "Trabajador"],
        fg_color="#343638",
        button_color="#C8BCF6",
        border_color="#C8BCF6",
        corner_radius=32,
        state="readonly" 
    )
    role_input.set("Seleccionar")
    role_txt.pack(side="left", padx=10)
    role_input.pack(side="left", padx=10)
    # Boton para Iniciar Sesion
    login_button_submit = CTkButton(
        login_frame,
        text="Iniciar Sesion",
        corner_radius=32,
        fg_color="#C8BCF6",
        text_color="#09090A",
        hover_color="#A79BE2",
        command=login
    )
    login_button_submit.pack(pady=10)
    # Botón de Regreso
    show_back_button()
    return login_frame

"""Frame para el Historial de Modificaciones"""
def make_history_frame():
    global history_frame, history_date_button, modifications_container
    modifications_container = None
    # Creando Frame
    history_frame = tk.Frame(window, bg="#09090A")
    history_frame.name = "history"
    history_frame.pack(side="top", anchor="n", fill="x", expand=True)
    # Título
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        history_frame,
        text="Historial de Modificaciones",
        font=title_font,
        bg="#09090A",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=10)
    def load_modifications(selected_date):
        global modifications_container
        # Si ya existe un contenedor previo, se destruye para refrescar la información
        if modifications_container is not None:
            modifications_container.destroy()
        modifications_container = tk.Frame(history_frame, bg="#09090A")
        modifications_container.pack(fill="both", expand=True, padx=10, pady=10)
        # Crear un Scrollbar
        scrollbar = tk.Scrollbar(modifications_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas = tk.Canvas(modifications_container, bg="#09090A", yscrollcommand=scrollbar.set, bd=0, highlightthickness=0, height=500)
        canvas.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=canvas.yview)
        inner_frame = tk.Frame(canvas, bg="#09090A")
        window_id = canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        def onFrameConfigure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(window_id, width=canvas.winfo_width())
        inner_frame.bind("<Configure>", onFrameConfigure)
        # Conexión y consulta a la base de datos
        try:
            connection = c.make_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute(f"EXEC sp_obtener_modificaciones_por_dia_vista '{selected_date}'")
                modifications = cursor.fetchall()
                if modifications: 
                    for modification in modifications:
                        # Procesar modification[6] si es un JSON válido
                        try:
                            datos_json = json.loads(modification[6])
                            def format_data(data, indent=0):
                                formatted = ""
                                espacios = " " * indent
                                if isinstance(data, dict):
                                    for key, value in data.items():
                                        if key.lower() in ["contraseña", "password"]:
                                            continue # No mostrar contraseña en el JSON
                                        if isinstance(value, (dict, list)):
                                            formatted += f"{espacios}{key}:\n{format_data(value, indent + 4)}"
                                        else:
                                            formatted += f"{espacios}{key}: {value}\n"
                                elif isinstance(data, list):
                                    for item in data:
                                        if isinstance(item, (dict, list)):
                                            formatted += format_data(item, indent)
                                        else:
                                            formatted += f"{espacios}- {item}\n"
                                else:
                                    formatted += f"{espacios}{data}\n"
                                return formatted                            
                            pretty_data = format_data(datos_json)
                        except Exception as e:
                            pretty_data = modification[6]                            
                        texto_modification = (
                            f"Auditoria ID: {modification[0]}\n"
                            f"Tabla Modificada: {modification[1]}\n"
                            f"Registro Modificado: {modification[2]}\n"
                            f"Comando: {modification[3]}\n"
                            f"Rol del Modificador: {modification[5]}\n"
                            f"Datos Anteriores:\n{pretty_data}\n"
                        )
                        tk.Label(inner_frame, text=texto_modification, bg="#09090A", fg="#C8BCF6", anchor="center", justify="center").pack(fill="x", pady=2)
                else:
                    tk.Label(inner_frame, text="No se encontraron modificaciones", bg="#09090A", fg="#C8BCF6").pack(pady=10, side="top", anchor="center")
                connection.close()
            else:
                tk.Label(inner_frame, text="Error en la conexión a la base de datos", bg="#09090A", fg="#C8BCF6").pack(pady=10, side="top", anchor="center")
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener modificaciones: {e}")
    # Función para actualizar la fecha seleccionada y cargar las modificaciones
    def update_history_date(selected_date):
        history_date_button.configure(text=selected_date)
        load_modifications(selected_date)
    # Función del calendario
    def open_calendar(min_date, max_date, callback):
        calendar_window = tk.Toplevel(window)
        calendar_window.title("Selecciona la Fecha")
        calendar_window.configure(bg="#09090A")
        calendar_window.geometry("320x250+150+85")
        try:
            calendar_window.iconbitmap("../../ASSETS/icon.ico")
        except Exception:
            print(f"Error al cargar el icono: {Exception}")
        calendar_frame = tk.Frame(calendar_window, bg="#09090A", relief="flat", bd=1)
        calendar_frame.pack(padx=10, pady=10, fill="both", expand=True)
        calendar = Calendar(
            calendar_frame,
            mindate=min_date,
            maxdate=max_date,
            date_pattern="yyyy-mm-dd",
            selectmode="day",
            background="#09090A",
            foreground="#7732FF",
            headersbackground="#09090A",
            headersforeground="#7732FF",
            selectbackground="#7732FF",
            selectforeground="#09090A",
            weekendforeground="#A9A9A9",
            bordercolor="#C7BCF6",
        )
        calendar.pack(padx=10, pady=10)
        calendar.bind("<<CalendarSelected>>", lambda _: [callback(calendar.get_date()), calendar_window.destroy()])
    # Fecha de Modificaciones
    history_date_frame = tk.Frame(history_frame, bg="#09090A")
    history_date_frame.pack(side="top", pady=10, fill="x", padx=10)
    history_date_label = tk.Label(history_date_frame, text="Fecha de las Modificaciones:", bg="#09090A", fg="#C8BCF6")
    history_date_label.pack(side="left", padx=10)
    history_date_button = CTkButton(
        history_date_frame,
        text="Seleccionar",
        corner_radius=32,
        fg_color="#343638",
        text_color="#C8BCF6",
        hover_color="#5A23CC",
        border_color="#C8BCF6",
        border_width=2,
        command=lambda: open_calendar(
            date(2024, 12, 31),
            date.today(),
            update_history_date  
        )
    )
    history_date_button.pack(side="left", padx=10, fill="x", expand=True)
    return history_frame

# ------------------------------------------------------------MANEJO DE COMANDOS---------------------------------------------------------------------------------------------

def open_table_window_obtain(fetch_function, title):
    global last_table_window
    # Si hay una ventana abierta, destruirla antes de abrir una nueva
    if last_table_window is not None and last_table_window.winfo_exists():
        last_table_window.destroy()
    connection = c.make_connection()
    if not connection:
        return None
    cursor = connection.cursor()
    selected_data = None  # Almacena la fila seleccionada
    confirmed = False  # Bandera para confirmar la selección
    try:
        data = fetch_function(cursor)
        if not data:
            messagebox.showinfo("Información", f"No hay datos en la tabla {title}.")
            return None
        # Crear ventana
        table_window = tk.Toplevel(fetch_frame)
        last_table_window = table_window
        table_window.title(f"Tabla: {title}")
        # Asegurarse de que la ventana principal tenga los datos actualizados
        window.update_idletasks()
        main_width = window.winfo_width()
        main_height = window.winfo_height()
        main_x = window.winfo_x()
        main_y = window.winfo_y()
        # Definir un ancho mayor para la ventana secundaria 
        new_width = main_width + 200
        new_height = main_height
        new_x = main_x + main_width  
        new_y = main_y
        table_window.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")
        table_window.configure(bg="#09090A")
        try:
            table_window.iconbitmap("../../ASSETS/icon.ico")
        except Exception:
            print(f"Error al cargar el icono: {Exception}")
        table_window.configure(bg="#09090A")
        # Treeview para mostrar datos
        tree = ttk.Treeview(table_window, show="headings", selectmode="browse")
        tree.pack(fill="both", expand=True)
        # Configurar columnas 
        columns = [desc[0] for desc in cursor.description]
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        # Insertar datos
        all_data = []
        for row in data:
            cleaned_row = [item.strip() if isinstance(item, str) else item for item in row]
            tree.insert("", "end", values=cleaned_row)
            all_data.append(row)
        # Buscador
        logo_img = Image.open("../../ASSETS/search_logo.png")  
        logo_img = logo_img.resize((20, 20), Image.LANCZOS)
        ctk_logo = ctk.CTkImage(logo_img, size=(20, 20))
        search_frame = ctk.CTkFrame(table_window, fg_color="transparent")  
        # Crea un label que muestre el logo
        logo_label = ctk.CTkLabel(search_frame, image=ctk_logo, text="")
        logo_label.pack(side="left", padx=(5, 0)) 
        # Crea el entry para el buscador
        search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=search_var,
            corner_radius=16,
            border_color="#C8BCF6",
            fg_color="#343638",
            text_color="#C8BCF6",
            placeholder_text="Buscar",
            width=150   
        )
        search_entry.bind("<KeyRelease>", lambda event: update_treeview(tree, all_data, search_var.get()))
        search_entry.pack(side="left", padx=(5, 5), fill="x", expand=True)
        search_frame.pack(pady=5, padx=10, fill="x")
        # Función al seleccionar fila
        def on_select(event):
            nonlocal selected_data
            selected_items = tree.selection()
            if selected_items:
                selected_item = selected_items[0]
                selected_data = list(tree.item(selected_item, 'values'))
        tree.bind('<<TreeviewSelect>>', on_select)
        # Frame para botones
        button_frame = tk.Frame(table_window, bg="#09090A")
        button_frame.pack(pady=10)
        # Botón Aceptar (confirma y cierra)
        def confirm_selection():
            nonlocal confirmed
            confirmed = True
            table_window.destroy()
        accept_button = ctk.CTkButton(
            button_frame,
            text="Aceptar",
            corner_radius=16,
            fg_color="#7732FF",  
            text_color="white",  
            command=confirm_selection
        )
        accept_button.pack(side="left", padx=5)
        # Boton de cerrar sin confirmar
        close_button = ctk.CTkButton(
            button_frame,
            text="Cerrar",
            corner_radius=16,
            fg_color="#444444",
            text_color="white",
            command=table_window.destroy
        )
        close_button.pack(side="left", padx=5)
        # Esperar a que la ventana se cierre
        table_window.wait_window()
        # Retornar datos solo si se confirmó con "Aceptar"
        return selected_data if confirmed else None
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"No se pudo obtener datos: {e}")
        return None
    finally:
        connection.close()

"""Frame para Buscar Datos"""
def make_fetch_frame():
    global current_frame, navigation_bar, action_bar
    fetch_frame = tk.Frame(window, bg="#09090A")
    fetch_frame.name = "fetch"
    # Función para abrir una ventana con datos de una tabla
    def open_table_window(fetch_function, title):
        global last_table_window
        # Si hay una ventana abierta, destruirla antes de abrir una nueva
        if last_table_window is not None and last_table_window.winfo_exists():
            last_table_window.destroy()
        connection = c.make_connection()
        if not connection:
            return
        cursor = connection.cursor()
        try:
            data = fetch_function(cursor)  
            if not data:
                messagebox.showinfo("Información", f"No hay datos en la tabla {title}.")
                return
            # Crear una nueva ventana
            table_window = tk.Toplevel(fetch_frame)
            last_table_window = table_window
            table_window.title(f"Tabla: {title}")
            # Asegurarse de que la ventana principal tenga los datos actualizados
            window.update_idletasks()
            main_width = window.winfo_width()
            main_height = window.winfo_height()
            main_x = window.winfo_x()
            main_y = window.winfo_y()
            # Definir un ancho mayor para la ventana secundaria 
            new_width = main_width + 200
            new_height = main_height
            new_x = main_x + main_width  
            new_y = main_y
            table_window.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")
            table_window.configure(bg="#09090A")
            # Logo
            try:
                table_window.iconbitmap("../../ASSETS/icon.ico")
            except Exception:
                print(f"Error al cargar el icono: {Exception}")
            table_window.configure(bg="#09090A")
            # Crear un Treeview para mostrar los datos
            tree = ttk.Treeview(table_window, show="headings", selectmode="browse")
            tree.pack(fill="both", expand=True)
            # Configurar columnas según cursor.description
            columns = [desc[0] for desc in cursor.description]
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center")
            # Insertar datos en el Treeview
            all_data = []
            for row in data:
                cleaned_row = [item.strip() if isinstance(item, str) else item for item in row]
                tree.insert("", "end", values=cleaned_row)
                all_data.append(row)
            # Buscador
            logo_img = Image.open("../../ASSETS/search_logo.png")  
            logo_img = logo_img.resize((20, 20), Image.LANCZOS)
            ctk_logo = ctk.CTkImage(logo_img, size=(20, 20))
            search_frame = ctk.CTkFrame(table_window, fg_color="transparent")  
            # Crea un label que muestre el logo
            logo_label = ctk.CTkLabel(search_frame, image=ctk_logo, text="")
            logo_label.pack(side="left", padx=(5, 0)) 
            # Crea el entry para el buscador
            search_var = tk.StringVar()
            search_entry = ctk.CTkEntry(
                search_frame,
                textvariable=search_var,
                corner_radius=16,
                border_color="#C8BCF6",
                fg_color="#343638",
                text_color="#C8BCF6",
                placeholder_text="Buscar",
                width=150   
            )
            search_entry.bind("<KeyRelease>", lambda event: update_treeview(tree, all_data, search_var.get()))
            search_entry.pack(side="left", padx=(5, 5), fill="x", expand=True)
            search_frame.pack(pady=5, padx=10, fill="x")
            # Botón para cerrar la ventana
            close_button = ctk.CTkButton(
                table_window,
                text="Cerrar",
                corner_radius=16,
                fg_color="#7732FF",
                text_color="white",
                command=table_window.destroy
            )
            close_button.pack(pady=10)
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"No se pudo obtener datos: {e}")
        finally:
            connection.close()

    # Botón para mostrar la tabla de Usuarios
    usuario_button = CTkButton(
        fetch_frame,
        text="Ver Usuarios",
        corner_radius=32,
        fg_color="#7732FF",
        hover_color="#5A23CC",
        command=lambda: open_table_window(f.get_usuarios, "Usuarios")
    )
    usuario_button.pack(pady=10, padx=20, fill="x")
    # Botón para mostrar la tabla de buses
    bus_button = CTkButton(
        fetch_frame,
        text="Ver Buses",
        corner_radius=32,
        fg_color="#7732FF",
        hover_color="#5A23CC",
        command=lambda: open_table_window(f.get_bus, "Buses")
    )
    bus_button.pack(pady=10, padx=20, fill="x")
    # Botón para mostrar la tabla de choferes
    driver_button = CTkButton(
        fetch_frame,
        text="Ver Choferes",
        corner_radius=32,
        fg_color="#7732FF",
        hover_color="#5A23CC",
        command=lambda: open_table_window(f.get_driver, "Choferes")
    )
    driver_button.pack(pady=10, padx=20, fill="x")
    # Botón para mostrar la tabla de rutas
    route_button = CTkButton(
        fetch_frame,
        text="Ver Rutas",
        corner_radius=32,
        fg_color="#7732FF",
        hover_color="#5A23CC",
        command=lambda: open_table_window(f.get_route, "Rutas")
    )
    route_button.pack(pady=10, padx=20, fill="x")
    # Botón para mostrar la tabla de reservas
    booking_button = CTkButton(
        fetch_frame,
        text="Ver Reservas",
        corner_radius=32,
        fg_color="#7732FF",
        hover_color="#5A23CC",
        command=lambda: open_table_window(f.get_booking, "Reservas")
    )
    booking_button.pack(pady=10, padx=20, fill="x")
    # Botón para mostrar la tabla de Reportes_total
    reportes_button_total = CTkButton(
        fetch_frame,
        text="Ver Reportes Total",
        corner_radius=32,
        fg_color="#7732FF",
        hover_color="#5A23CC",
        command=lambda: open_table_window(f.get_reportes_total, "Reportes_total")
    )
    reportes_button_total.pack(pady=10, padx=20, fill="x")
    # Boton para mostrar la tabla reportes
    reportes_button = CTkButton(
        fetch_frame,
        text="Ver Reportes",
        corner_radius=32,
        fg_color="#7732FF",
        hover_color="#5A23CC",
        command=lambda: open_table_window(f.get_reportes, "Reportes")
    )
    reportes_button.pack(pady=10, padx=20, fill="x")
    return fetch_frame

def create_input_field(parent, label_text, placeholder, identifier_button):
    global entries
    frame = tk.Frame(parent, bg="#09090A")
    frame.pack(side="top", pady=10, fill="x", padx=10)
    if identifier_button == 1:
        label = tk.Label(frame, text=label_text, bg="#09090A", fg="#C8BCF6")
        label.pack(side="left", padx=10)
        entry = CTkEntry(
            frame,
            placeholder_text=placeholder,
            border_color="#C8BCF6",
            corner_radius=32,
        )
        entry.pack(side="left", padx=10, fill="x", expand=True)
        if entry is not None:
            entries.append(entry)  # Agregar la entrada a la lista
    elif identifier_button == 2:
        frame = tk.Frame(parent, bg="#09090A")
        frame.pack(side="top", pady=20, fill="x", padx=10)
        def on_button_click():
            global selected_option
            selected_option = label_text
            queries_option()  # Llama a la función queries_option cuando se presione el botón
        available = CTkButton(
            frame,
            text=label_text,
            corner_radius=32,
            fg_color="#7732FF",
            hover_color="#5A23CC",
            command=on_button_click,
        )
        available.pack(pady=10, fill="x")

"""Frame para Crear Botones Predeterminados"""
def make_option_frame(parent, title_name):
    option_frame = ttk.Frame(parent)
    global option, entries 
    option = ttk.Entry(option_frame)
    entries = []  # Reiniciar la lista de entradas cada vez que se crea un nuevo conjunto
    option.pack(padx=10, pady=10)
    # Scrollbar
    canvas = tk.Canvas(option_frame, bg="#09090A", highlightthickness=0, width=350, height=1300)
    scrollbar = tk.Scrollbar(option_frame, orient="vertical", command=canvas.yview,width=18)
    # Crear un marco interno dentro del canvas
    scrollable_frame = tk.Frame(canvas, bg="#09090A")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    # Vincular el marco interno con el canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=350, height=1900)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    if title_name == "Eliminar":
        # Eliminacion logica
        title_font = font.Font(family="Canva Sans", size=15, weight="bold")
        title_label = tk.Label(
            scrollable_frame,
            text=f"{title_name} logica un Bus",  
            font=title_font,
            bg="#09090A",
            fg="#7732FF",
            wraplength=350,
            justify="center",
        )
        title_label.pack(pady=20)
        create_input_field(scrollable_frame, "Bus ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Bus Logica", "Ingresar", 2)
        title_label = tk.Label(
            scrollable_frame,
            text=f"{title_name} logica un Chofer",  
            font=title_font,
            bg="#09090A",
            fg="#7732FF",
            wraplength=350,
            justify="center",
        )
        title_label.pack(pady=20)
        create_input_field(scrollable_frame, "Chofer ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Chofer Logica", "Ingresar", 2) 
        title_label = tk.Label(
            scrollable_frame,
            text=f"{title_name} logica una Ruta",  
            font=title_font,
            bg="#09090A",
            fg="#7732FF",
            wraplength=350,
            justify="center",
        )
        title_label.pack(pady=20)
        create_input_field(scrollable_frame, "Ruta ID", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Ruta Logica", "Ingresar", 2)
        title_label = tk.Label(
            scrollable_frame,
            text=f"{title_name} logica un Usuario",  
            font=title_font,
            bg="#09090A",
            fg="#7732FF",
            wraplength=350,
            justify="center",
        )
        title_label.pack(pady=20)
        create_input_field(scrollable_frame, "Usuario ID", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Usuario Logica", "Ingresar", 2)    
    # Titulo de Bus
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        scrollable_frame,
        text=f"{title_name} un Bus",  
        font=title_font,
        bg="#09090A",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=20)
    #bus
    if title_name == "Agregar":
        create_input_field(scrollable_frame, "Chofer ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Ruta ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, "fecha_salida:", "Ingresar", 1)
        create_input_field(scrollable_frame, "fecha_retorno","Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Bus", "Ingresar", 2)
    elif title_name == "Eliminar":
        create_input_field(scrollable_frame, "Bus ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Bus", "Ingresar", 2)
    elif title_name == "Actualizar":
        create_input_field(scrollable_frame, "Bus ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Chofer ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Ruta ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, "fecha_salida:", "Ingresar", 1)
        create_input_field(scrollable_frame, "fecha_retorno","Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Bus", "Ingresar", 2)
    # Titulo de Chofer
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        scrollable_frame,
        text=f"{title_name} un Chofer",  
        font=title_font,
        bg="#09090A",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=20)
    #chofer
    if title_name == "Agregar":
        create_input_field(scrollable_frame, "Nombre del Chofer:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Edad:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Carnet:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Chofer", "Ingresar", 2)
    elif title_name == "Eliminar":
        create_input_field(scrollable_frame, "Chofer ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Chofer", "Ingresar", 2)
    elif title_name == "Actualizar":
        create_input_field(scrollable_frame, "Nombre del Chofer:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Chofer ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Edad:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Carnet:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Chofer", "Ingresar", 2)
    # Titulo de RUTA
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        scrollable_frame,
        text=f"{title_name} una Ruta",  
        font=title_font,
        bg="#09090A",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=20)    
    #ruta
    if title_name == "Agregar":
        create_input_field(scrollable_frame, "Dep_inicio:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Dep_final:", "Ingresar", 1)        
        create_input_field(scrollable_frame, "Costo:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Costo VIP:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Ruta", "Ingresar", 2)
    elif title_name == "Eliminar":
        create_input_field(scrollable_frame, "Ruta ID", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Ruta", "Ingresar", 2)  
    elif title_name == "Actualizar":
        create_input_field(scrollable_frame, "Ruta ID", "Ingresar", 1)
        create_input_field(scrollable_frame, "Dep_inicio", "Ingresar", 1)
        create_input_field(scrollable_frame, "Dep_final", "Ingresar", 1)        
        create_input_field(scrollable_frame, "Costo:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Costo VIP:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Ruta", "Ingresar", 2)
    # Usuario
    if title_name == "Actualizar":
        title_font = font.Font(family="Canva Sans", size=15, weight="bold")
        title_label = tk.Label(
            scrollable_frame,
            text=f"{title_name} un Usuario",  
            font=title_font,
            bg="#09090A",
            fg="#7732FF",
            wraplength=350,
            justify="center",
        )
        title_label.pack(pady=20)   
        create_input_field(scrollable_frame, "Usuario ID", "Ingresar", 1)
        create_input_field(scrollable_frame, "Nombre", "Ingresar", 1)
        create_input_field(scrollable_frame, "Apellido", "Ingresar", 1)        
        create_input_field(scrollable_frame, "Edad:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Carnet:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Contraseña:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Admin:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Usuario", "Ingresar", 2)
    elif title_name=="Eliminar":
        title_font = font.Font(family="Canva Sans", size=15, weight="bold")
        title_label = tk.Label(
            scrollable_frame,
            text=f"{title_name} un Usuario",  
            font=title_font,
            bg="#09090A",
            fg="#7732FF",
            wraplength=350,
            justify="center",
        )
        title_label.pack(pady=20)   
        create_input_field(scrollable_frame, "Usuario ID", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Usuario", "Ingresar", 2)
    return option_frame

"""Frame para Agregar Datos"""
def make_add_frame():
    global current_frame, add_frame, option_frame
    if add_frame is None:
        add_frame = tk.Frame(window, bg="#09090A")
        add_frame.name = "add"
    if option_frame is None or option_frame.master != add_frame:
        if option_frame:
            option_frame.pack_forget() 
        option_frame = make_option_frame(add_frame, "Agregar")
        option_frame.pack(fill="both", expand=True)
    if current_frame:
        current_frame.pack_forget()
    current_frame = add_frame
    current_frame.pack(fill="both", expand=True)
    show_option(target_frame=add_frame)
    return add_frame

"""Frame para Modificar Datos"""
def make_update_frame():
    global current_frame, update_frame, option_frame
    if update_frame is None:
        update_frame = tk.Frame(window, bg="#09090A")
        update_frame.name = "update"
    if option_frame is None or option_frame.master != update_frame:
        if option_frame:
            option_frame.pack_forget()  
        option_frame = make_option_frame(update_frame, "Actualizar")
        option_frame.pack(fill="both", expand=True)
    if current_frame:
        current_frame.pack_forget()
    current_frame = update_frame
    current_frame.pack(fill="both", expand=True)
    show_option(target_frame=update_frame)
    return update_frame

"""Frame para Eliminar Datos"""
def make_delete_frame():
    global current_frame, delete_frame, option_frame
    if delete_frame is None:
        delete_frame = tk.Frame(window, bg="#09090A")
        delete_frame.name = "delete"
    if option_frame is None or option_frame.master != delete_frame:
        if option_frame:
            option_frame.pack_forget()  
        option_frame = make_option_frame(delete_frame, "Eliminar")
        option_frame.pack(fill="both", expand=True)
    if current_frame:
        current_frame.pack_forget()
    current_frame = delete_frame
    current_frame.pack(fill="both", expand=True)
    show_option(target_frame=delete_frame)
    return delete_frame

# ----------------------------------------------------------MOSTRAR Y OCULTAR FRAMES-----------------------------------------------------------------------------------------------

"""Funcion para Mostrar un Frame"""
def show_frame(frame_to_show):
    global all_frames, action_bar, back_button, log_out_button, current_frame
    # Ocultar frame actual
    if current_frame:
        current_frame.pack_forget()
    current_frame = frame_to_show  
    frame_to_show.pack(expand=True)
    # Ocultar todos los frames
    for frame in all_frames:
        frame.pack_forget()
    # Gestionar visibilidad de la barra de acción
    if hasattr(frame_to_show, "name") and frame_to_show.name in ["loading", "start"]:
        action_bar.pack_forget()
        hide_back_button()
        hide_log_out_button()
        navigation_bar.pack_forget()
    else:
        if frame_to_show.name in ["login", "register", "terms"]:
            action_bar.pack(side="top", fill="x")
            show_back_button()
            hide_log_out_button()
            navigation_bar.pack_forget()
        elif frame_to_show.name == "history":
            hide_option()
            action_bar.pack(side="top", fill="x")
            show_back_button()
            show_log_out_button()
            navigation_bar.pack(side="bottom", fill="x")
        else:
            hide_option()
            action_bar.pack(side="top", fill="x")
            hide_back_button()
            show_log_out_button()
            show_history_button()
            navigation_bar.pack(side="bottom", fill="x")
    frame_to_show.pack(expand=True)

"""Funcion para Mostrar el Boton para Regresar"""
def show_back_button(target_frame=None):
    if back_button:
        back_button.place(x=25, y=12)  

"""Funcion para ocultar el Boton para Regresar"""
def hide_back_button():
    if back_button:
        on_back_button()
        back_button.place_forget()

"""Funcion para limpiar datos al  presionar el Boton de Regresar"""
def on_back_button():
    global current_frame, login_frame, register_frame, start_frame, role_input, history_date_button, history_frame
    # Borar datos al presionar el boton de regreso
    if current_frame == login_frame:
        login_id_card_entry.delete(0, tk.END)
        login_password_entry.delete(0, tk.END)
        role_input.set("Seleccionar")
    elif current_frame == register_frame:
        name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        id_card_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    elif current_frame == history_frame:
        history_date_button.configure(text="Seleccionar") 

"""Funcion para mostrar el Boton para Cerrar Sesion"""
def show_log_out_button(target_frame=None):
    if log_out_button:
        log_out_button.place(x=340, y=12)

"""Funcion para ocultar el Boton para Cerrar Sesion"""
def hide_log_out_button():
    if log_out_button:
        log_out_button.place_forget()

"""Funcion para limpiar datos al presionar el Boton Cerrar Sesion"""
def on_log_out_button():
    global current_frame, start_frame, history_date_button
    hide_log_out_button()
    history_date_button.configure(text="Seleccionar") 
    show_frame(start_frame)

"""Función para Mostrar Option"""
def show_option(target_frame=None):
    global option
    if option and target_frame:
        option.place(relx=0.5, rely=0.5, anchor='center')

"""Función para Ocultar Option"""
def hide_option():
    if option:
        option.place_forget()

"""Actualizar el TreeView al buscar"""
def update_treeview(tree, all_data, keyword):
    # Limpiar el Treeview
    for item in tree.get_children():
        tree.delete(item)
    keyword = keyword.lower().strip()
    # Si no se ingresó texto, mostramos todos los datos
    if keyword == "":
        filtered = all_data
    else:
        filtered = [
            row for row in all_data 
            if keyword in " ".join(str(item).lower() for item in row)
        ]
    # Eliminar duplicados conservando el orden
    filtered_unique = []
    for row in filtered:
        if row not in filtered_unique:
            filtered_unique.append(row)
    # Insertar los registros filtrados sin duplicados en el Treeview
    for row in filtered_unique:
        cleaned_row = [item.strip() if isinstance(item, str) else item for item in row]
        tree.insert("", "end", values=cleaned_row)

# ----------------------------------------------------------------MAIN--------------------------------------------------------------------------------------------

"""Funcion Principal"""
def main():
    global window, all_frames, start_frame, register_frame, login_frame, action_bar, terms_frame
    global current_frame, loading_frame, add_frame, update_frame, delete_frame, fetch_frame, navigation_bar, history_frame
    # Configuración de la ventana
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    window = tk.Tk()
    window.title("Pasa")
    window.geometry("380x650+120+10")
    window.resizable(False, False)
    window.configure(bg="#09090A")
    # Agregar Icono
    try:
        window.iconbitmap("../../ASSETS/icon.ico")
    except Exception:
        print("Error al cargar el Icono")
    # Crear barras y frames
    action_bar = make_action_bar()
    action_bar.pack_forget()
    navigation_bar = make_navigation_bar(window, None, None, None, None)
    navigation_bar.pack_forget()
    # Crear Frames
    loading_frame = make_loading_screen()
    start_frame = make_start_frame()
    register_frame = make_register_frame()
    login_frame = make_login_frame()
    add_frame = make_add_frame()
    update_frame = make_update_frame()
    delete_frame = make_delete_frame()
    fetch_frame = make_fetch_frame()
    terms_frame = make_terms_frame()
    history_frame = make_history_frame()
    all_frames = [
        loading_frame, start_frame, register_frame,
        login_frame, fetch_frame, history_frame, terms_frame,
        add_frame, update_frame, delete_frame
    ]
    # Mostrar pantalla de carga
    current_frame = loading_frame
    show_frame(loading_frame)
    window.after(1500, lambda: show_frame(start_frame))
    window.mainloop()

if __name__ == "__main__":
    main()