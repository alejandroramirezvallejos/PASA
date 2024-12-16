import sys
import os
import tkinter as tk 
from tkinter import messagebox, font
from tkcalendar import Calendar
from datetime import date
from PIL import Image, ImageTk
from customtkinter import CTkComboBox, CTkButton, CTkEntry, set_appearance_mode, set_default_color_theme
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from USER_APP import user_content as uc, user_show_frames as shf, user_signup_login as usl, welcome as w, action_bar as a, connection as con, search_bus as sh

"""Pantalla de Carga"""
def make_loading_screen(window):
    # Creando Frame
    loading_frame = tk.Frame(window, bg="#7732FF") 
    loading_frame.name = "loading" 
    loading_frame.pack(fill="both", expand=True)
    # Agregando Icono
    try:
        pasa_iso = "../ASSETS/color_negative.png"
        image = Image.open(pasa_iso)
        image = image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        iso_label = tk.Label(loading_frame, image=photo, bg="#7732FF")  
        iso_label.image = photo  
        iso_label.pack(expand=True)
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Tiempo de Espera
    def delayed_show_start_frame():
        window.configure(bg="#F1F2F6")
        shf.show_frame(start_frame)
    window.after(1500, delayed_show_start_frame)
    return loading_frame

"""Frame Inicial"""
def make_start_frame(window):
    # Creacion del Frame
    start_frame = tk.Frame(window, bg="#F1F2F6")
    start_frame.name = "start"
    # Agregando Icono
    try:
        pasa_iso = "../ASSETS/color_positive.png"
        image = Image.open(pasa_iso)
        image = image.resize((170, 170), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        iso_label = tk.Label(start_frame, image=photo, bg="#F1F2F6")  
        iso_label.image = photo  
        iso_label.pack(expand=True)
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Texto
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        start_frame,
        text="¡Viajar nunca fue mas sencillo!",
        font=title_font,
        bg="#F1F2F6",
        fg="black",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=50)
    # Boton de Inicio de Sesion
    login_button = CTkButton(
        start_frame,
        text="Iniciar Sesion",
        corner_radius=32,
        fg_color="#7732FF",
        text_color="white",
        hover_color="#5A23CC",
        command=lambda: show_frame(login_frame),
    )
    login_button.pack(pady=10)
    # Boton de Creacion de Cuenta
    signup_button = CTkButton(
        start_frame,
        text="Crear cuenta",
        corner_radius=32,
        fg_color="#7732FF",
        text_color="white",
        hover_color="#5A23CC",
        command=lambda: show_frame(register_frame),
    )
    signup_button.pack(pady=10)
    # Texto de Términos y Condiciones
    terms_label = tk.Label(
        start_frame,
        text="Al crear una cuenta, confirmo que he leído y acepto los ",
        font=("Arial", 10),
        bg="#F1F2F6",
        fg="black",
    )
    terms_label.pack(pady=(30, 5), side="top", anchor="center")
    # Crear enlace para "Términos y condiciones"
    terms_link = tk.Label(
        start_frame,
        text="Terminos y Condiciones de Uso",
        font=("Arial", 10, "underline"),
        bg="#F1F2F6",
        fg="#7732FF",
        cursor="hand2",
    )
    terms_link.pack(side="top", anchor="center")
    # Vincular el clic al enlace
    terms_link.bind("<Button-1>", lambda e: shf.show_frame(w.terms_frame))
    return start_frame

"""Frame para ver los Terminos y Condiciones de Uso"""
def make_terms_frame(window):
    # Crear el frame de términos y condiciones
    terms_frame = tk.Frame(window, bg="#F1F2F6")
    terms_frame.name = "terms"
    # Título principal
    title_label = tk.Label(
        terms_frame,
        text="Términos y Condiciones de Uso",
        font=("Arial", 16, "bold"),
        bg="#F1F2F6",
        fg="black",
    )
    title_label.pack(pady=20)
    # Crear un Scrollbar
    scrollbar = tk.Scrollbar(terms_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas = tk.Canvas(terms_frame, bg="#F1F2F6", yscrollcommand=scrollbar.set, bd=0, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.config(command=canvas.yview)
    # Agregando el Contenido
    content_text_frame = tk.Frame(canvas, bg="#F1F2F6")
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
        section_frame = tk.Frame(content_text_frame, bg="#F1F2F6")
        section_frame.pack(fill="x", padx=20, pady=10)
        # Título en negrita
        title_label = tk.Label(
            section_frame,
            text=title,
            font=("Arial", 12, "bold"),
            bg="#F1F2F6",
            fg="black",
            anchor="w",
        )
        title_label.pack(fill="x")
        # Contenido justificado
        content_text_label = tk.Label(
            section_frame,
            text=content,
            font=("Arial", 10),
            bg="#F1F2F6",
            fg="black",
            anchor="w",
            justify="left",
            wraplength=335,
        )
        content_text_label.pack(fill="x")
    # Botón para regresar
    a.show_back_button(terms_frame)
    return terms_frame