import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk 
from tkinter import messagebox, font
from tkcalendar import Calendar
from datetime import date
from PIL import Image, ImageTk
from customtkinter import CTkComboBox, CTkButton, CTkEntry, set_appearance_mode, set_default_color_theme
from USER_APP import user_content as uc, user_show_frames as shf, user_signup_login as usl, welcome as w, action_bar as a, connection as con, search_bus as sh
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

"""Funcion Principal"""
def main():
    global window, all_frames, start_frame, register_frame, login_frame, action_bar, content_frame, results_frame, terms_frame, current_frame, loading_frame
    # Configuración de la ventana
    set_appearance_mode("light")
    set_default_color_theme("blue")
    window = tk.Tk()
    window.title("Pasa")
    window.geometry("380x750+120+10")
    window.resizable(False, False)
    window.configure(bg="#7732FF")
    # Agregar Icono
    try:
        window.iconbitmap("../ASSETS/icon.ico")
    except Exception:
        print("Error al cargar el Icono")
    # Creación de Frames
    loading_frame = w.make_loading_screen(window)
    action_bar = a.make_action_bar(window)
    action_bar.pack_forget()
    start_frame = w.make_start_frame(window)
    register_frame = usl.make_register_frame(window)
    login_frame = usl.make_login_frame(window)
    content_frame = uc.make_content_frame(window)
    results_frame = tk.Frame(window, bg="#F1F2F6") 
    results_frame.name = "results"
    terms_frame = w.make_terms_frame(window)
    # Lista de Frames
    all_frames = [
        loading_frame, start_frame, register_frame,
        login_frame, content_frame, results_frame, terms_frame
    ]
    # Iniciar el programa
    shf.show_frame(loading_frame, all_frames)
    window.after(1500, lambda: show_frame(start_frame, all_frames))
    window.mainloop()

if __name__ == "__main__":
    main()
