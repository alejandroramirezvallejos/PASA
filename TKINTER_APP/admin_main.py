import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk 
from tkinter import messagebox, font
from tkcalendar import Calendar
from datetime import date
from PIL import Image, ImageTk
from customtkinter import CTkComboBox, CTkButton, CTkEntry, set_appearance_mode, set_default_color_theme
from ADMIN_APP import admin_welcome as aw, admin_functions_query as afq, admin_frame_options as afq, admin_fetch_frame as aff, admin_conection as acc, admin_action_navegation as aan
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

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

"""Funcion Principal"""
def main():
    global window, all_frames, start_frame, register_frame, login_frame, action_bar, terms_frame
    global current_frame, loading_frame, add_frame, update_frame, delete_frame, fetch_frame, navigation_bar
    # Configuración de la ventana
    set_appearance_mode("#09090A")
    set_default_color_theme("blue")
    window = tk.Tk()
    window.title("Pasa")
    window.geometry("380x750+120+10")
    window.resizable(False, False)
    window.configure(bg="#09090A")
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
    all_frames = [
        loading_frame, start_frame, register_frame,
        login_frame, fetch_frame, terms_frame,
        add_frame, update_frame, delete_frame
    ]
    # Mostrar pantalla de carga
    current_frame = loading_frame
    show_frame(loading_frame)
    window.after(1500, lambda: show_frame(start_frame))
    window.mainloop()

if __name__ == "__main__":
    main()