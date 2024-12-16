from . import action_bar as a

"""Funcion para Mostrar un Frame"""
def show_frame(frame_to_show, all_frames):
    current_frame = frame_to_show  
    # Ocultar todos los frames
    for frame in all_frames:
        frame.pack_forget()
    # Gestionar visibilidad de la barra de acción
    if hasattr(frame_to_show, "name") and frame_to_show.name in ["loading", "start"]:
        action_bar.pack_forget()
        a.hide_back_button()
        a.hide_log_out_button()
    else:
        action_bar.pack(side="top", fill="x")
        a.hide_back_button()
        a.hide_log_out_button()
        if hasattr(frame_to_show, "name"):
            if frame_to_show.name == "content":
                a.show_log_out_button()
            elif frame_to_show.name == "results":
                a.show_back_button()
                a.show_log_out_button()
            elif frame_to_show.name in ["login", "register", "terms"]:
                a.show_back_button()
    frame_to_show.pack(expand=True)