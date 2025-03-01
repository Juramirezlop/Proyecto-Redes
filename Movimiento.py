import tkinter as tk
from tkinter import ttk
import random
import winsound  
import csv
import threading
from PIL import Image, ImageTk  

# Definir zonas con colores y límites de velocidad
zones = [
    {"name": "Carretera", "speed_limit": 80, "color": "gray", "x_range": (300, 450)},
    {"name": "Avenida", "speed_limit": 50, "color": "goldenrod", "x_range": (150, 299)},
    {"name": "Zona Urbana", "speed_limit": 25, "color": "forestgreen", "x_range": (0, 149)}
]

class Moto:
    def __init__(self):
        self.speed = random.randint(20, 50)
        self.location = [random.randint(50, 400), random.randint(50, 450)]
        self.speed_x = random.uniform(2, 4)  
        self.speed_y = random.uniform(2, 4)  
        self.moving = True
        self.infractions = 0  
        self.infractions_active = False  
        self.infraction_resolved = True  
        self.update_zone()

    def move(self):
        if self.moving:
            self.location[0] += self.speed_x
            self.location[1] += self.speed_y

            if self.location[0] > 430 or self.location[0] < 20:
                self.speed_x = -self.speed_x
            if self.location[1] > 480 or self.location[1] < 20:
                self.speed_y = -self.speed_y

            if not self.infractions_active:  
                self.update_zone()

    def update_zone(self):
        for zone in zones:
            if zone["x_range"][0] <= self.location[0] <= zone["x_range"][1]:
                self.current_zone = zone
                break

    def check_speed(self):
        return self.speed > self.current_zone["speed_limit"]

    def update_speed(self):
        if self.moving:
            self.speed += random.uniform(-3, 3)  
            self.speed = max(10, min(self.speed, 120))  

    def toggle_pause(self):
        if not police_active:  
            self.moving = not self.moving

    def brake(self):
        self.speed -= 10  
        if self.speed < 10:
            self.speed = 10

# Interfaz principal
root = tk.Tk()
root.title("Simulación de Moto Mejorada")
root.configure(bg="#333")

moto = Moto()

# Panel lateral
left_frame = tk.Frame(root, width=200, height=500, bg="#222", relief="ridge", bd=2)
left_frame.pack(side="left", fill="y")

phone_frame = tk.Frame(left_frame, width=140, height=200, bg="green", bd=5, relief="solid")
phone_frame.pack_propagate(False)
phone_frame.pack(pady=10)

phone_label = tk.Label(left_frame, text="Seguridad: Velocidad dentro del límite.", font=("Helvetica", 10), fg="white", bg="#222", wraplength=160)
phone_label.pack(pady=5)

speed_label = tk.Label(left_frame, text="Velocidad: 0 km/h", font=("Helvetica", 12, "bold"), fg="cyan", bg="#222")
speed_label.pack(pady=5)

# Barra de velocidad con color dinámico
speed_bar = ttk.Progressbar(left_frame, length=150, mode="determinate")
speed_bar.pack(pady=5)

zone_label = tk.Label(left_frame, text="Zona: --", font=("Helvetica", 12, "bold"), fg="yellow", bg="#222")
zone_label.pack(pady=5)

infractions_label = tk.Label(left_frame, text="Infracciones: 0", font=("Helvetica", 12, "bold"), fg="red", bg="#222")
infractions_label.pack(pady=5)

infraction_location_label = tk.Label(left_frame, text="Última infracción en: --", font=("Helvetica", 10), fg="white", bg="#222")
infraction_location_label.pack(pady=5)

pause_button = tk.Button(left_frame, text="⏸️ Pausar", font=("Helvetica", 10), command=moto.toggle_pause, bg="orange", fg="black")
pause_button.pack(pady=5)

def brake_moto():
    if not police_active:  # 🚫 No permitir frenar si la policía ya está activa
        moto.brake()
        speed_label.config(text=f"Velocidad: {moto.speed:.1f} km/h")  

        # ✅ Solo permitir que la moto vuelva a moverse si su velocidad es menor al límite de la zona
        if moto.speed <= moto.current_zone["speed_limit"]:
            moto.infractions_active = False  # 🔥 Ahora la moto puede recibir nuevas infracciones más adelante
            moto.moving = True  
            phone_frame.config(bg="green")

brake_button = tk.Button(left_frame, text="🛑 Frenar", font=("Helvetica", 10), command=brake_moto, bg="red", fg="white")
brake_button.pack(pady=5)

# Canvas para la simulación
canvas = tk.Canvas(root, width=450, height=500, bg=moto.current_zone["color"])  
canvas.pack(side="right")

# Íconos en canvas
def draw_icons():
    icon_canvas = tk.Canvas(left_frame, width=180, height=100, bg="#222", highlightthickness=0)
    icon_canvas.pack(pady=10)

    # Velocímetro
    icon_canvas.create_oval(10, 10, 50, 50, outline="white", width=2)
    icon_canvas.create_line(30, 30, 45, 15, fill="red", width=3)  

    # Alerta
    icon_canvas.create_polygon(70, 50, 90, 10, 110, 50, fill="yellow", outline="black")
    icon_canvas.create_text(90, 30, text="⚠️", font=("Helvetica", 14, "bold"))

    # Policía
    icon_canvas.create_rectangle(130, 20, 170, 40, fill="blue")
    icon_canvas.create_oval(140, 10, 160, 30, fill="red")

draw_icons()

# Moto y Policía
moto_img = Image.open("moto.png").resize((40, 40))  
moto_icon = ImageTk.PhotoImage(moto_img)

police_img = Image.open("policia.png").resize((50, 50))  
police_icon = ImageTk.PhotoImage(police_img)

police_active = False
police_x, police_y = 450, 500  

def draw_environment():
    canvas.delete("background")  # Borrar fondo anterior

    # 🚗 Dibujar las zonas con colores
    canvas.create_rectangle(0, 0, 150, 500, fill="forestgreen", outline="black", tags="background")  # Zona Urbana
    canvas.create_rectangle(150, 0, 300, 500, fill="goldenrod", outline="black", tags="background")  # Avenida
    canvas.create_rectangle(300, 0, 450, 500, fill="gray", outline="black", tags="background")  # Carretera

    # 🏁 Dibujar líneas de carretera
    for i in range(0, 500, 40):
        canvas.create_line(150, i, 150, i + 20, fill="white", width=3, tags="background")  # Línea entre Zona Urbana y Avenida
        canvas.create_line(300, i, 300, i + 20, fill="white", width=3, tags="background")  # Línea entre Avenida y Carretera

draw_environment()

def save_infraction():
    with open("infracciones.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([moto.location[0], moto.location[1], moto.speed, moto.current_zone["name"]])

def play_infraccion_sound():
    winsound.Beep(1000, 300)

def trigger_alert():
    global police_active

    if moto.infractions_active:  # 🚨 Si ya está en infracción, evitar repetir el proceso
        return

    phone_frame.config(bg="red")
    moto.infractions_active = True  # 🔥 Bloquear el movimiento hasta que frene
    moto.moving = False  

    moto.infractions += 1  
    infractions_label.config(text=f"Infracciones: {moto.infractions}")
    infraction_location_label.config(text=f"Última infracción en: ({moto.location[0]:.1f}, {moto.location[1]:.1f})")
    save_infraction()
    play_infraccion_sound()

    if moto.infractions >= 5 and not police_active:
        call_police()

def siren_sound():
    while police_active:  # La sirena suena mientras la policía esté activa
        winsound.Beep(700, 500)
        winsound.Beep(900, 500)

def call_police():
    global police_active
    if police_active:  # Si ya está activa, no la vuelvas a llamar
        return  

    police_active = True
    phone_label.config(text="🚨 ¡ALERTA! Policía en camino.", fg="white", bg="red")

    pause_button.config(state="disabled")
    brake_button.config(state="disabled")

    siren_thread = threading.Thread(target=siren_sound, daemon=True)
    siren_thread.start()

def move_police():
    global police_x, police_y, police_active

    if police_active:
        moved = False  

        if abs(police_x - moto.location[0]) > 3:  
            police_x += 2 if police_x < moto.location[0] else -2
            moved = True  

        if abs(police_y - moto.location[1]) > 3:  
            police_y += 2 if police_y < moto.location[1] else -2
            moved = True  

        if moved:  
            canvas.delete("police")
            canvas.create_image(police_x, police_y, image=police_icon, tags="police")

        if abs(police_x - moto.location[0]) > 10 or abs(police_y - moto.location[1]) > 10:
            phone_label.config(text="🚓 ¡Atención! Policía en camino...", fg="white", bg="red")

        # 🚓 Cuando la patrulla captura la moto, detener la simulación correctamente
        if abs(police_x - moto.location[0]) <= 10 and abs(police_y - moto.location[1]) <= 10:
            police_active = False  
            moto.moving = False  # 🔥 Asegurarse de que la moto se detiene completamente
            phone_label.config(text="🚓 ¡La policía ha detenido la moto!", fg="white", bg="black")

            # 🚫 DETENER COMPLETAMENTE LA SIMULACIÓN
            root.after(2000, end_simulation)

def end_simulation():
    global update_id

    phone_frame.config(bg="black")  # Mantener el color original
    phone_label.config(text="🚓 ¡La policía ha detenido la moto!", fg="white", bg="black")  # Mantener el mensaje original

    if update_id:
        root.after_cancel(update_id)

    canvas.delete("moto")
    canvas.delete("police")

    # 🚫 Mantener los botones de pausa y freno deshabilitados
    pause_button.config(state="disabled")
    brake_button.config(state="disabled")

    # 📌 Mostrar los botones de reinicio y CSV centrados
    canvas.itemconfig(restart_button_window, state="normal")
    canvas.itemconfig(show_csv_button_window, state="normal")

def restart_simulation():
    global moto, police_active, police_x, police_y, update_id

    moto = Moto()
    police_active = False
    police_x, police_y = 450, 500  

    phone_label.config(text="Seguridad: Velocidad dentro del límite.", fg="white", bg="#222")
    phone_frame.config(bg="green")
    infractions_label.config(text="Infracciones: 0")
    infraction_location_label.config(text="Última infracción en: --")
    speed_label.config(text="Velocidad: 0 km/h")
    speed_bar["value"] = 0
    zone_label.config(text="Zona: --")

    pause_button.config(state="normal")
    brake_button.config(state="normal")

    # ❌ Ocultar los botones de reinicio y CSV del canvas
    canvas.itemconfig(restart_button_window, state="hidden")
    canvas.itemconfig(show_csv_button_window, state="hidden")

    canvas.delete("moto")
    canvas.delete("police")
    canvas.config(bg=moto.current_zone["color"])

    update()

def show_csv_data():
    try:
        with open("infracciones.csv", mode="r") as file:
            reader = csv.reader(file)
            data = list(reader)

        if not data:  # Si el archivo está vacío
            data_window = tk.Toplevel(root)
            data_window.title("Datos de Infracciones")
            label = tk.Label(data_window, text="No hay infracciones registradas.", font=("Helvetica", 12))
            label.pack(padx=20, pady=20)
            return

        # 📌 Crear ventana emergente para la tabla
        data_window = tk.Toplevel(root)
        data_window.title("Historial de Infracciones")

        # 📌 Crear Treeview con columnas bien definidas
        columns = ("X Pos", "Y Pos", "Velocidad", "Zona")
        tree = ttk.Treeview(data_window, columns=columns, show="headings", height=10)

        # 📌 Definir encabezados de columna
        tree.heading("X Pos", text="X Posición", anchor="center")
        tree.heading("Y Pos", text="Y Posición", anchor="center")
        tree.heading("Velocidad", text="Velocidad (km/h)", anchor="center")
        tree.heading("Zona", text="Zona", anchor="center")

        # 📌 Ajustar tamaño de columnas
        tree.column("X Pos", width=80, anchor="center")
        tree.column("Y Pos", width=80, anchor="center")
        tree.column("Velocidad", width=100, anchor="center")
        tree.column("Zona", width=120, anchor="center")

        # 📌 Insertar los datos en la tabla
        for row in data:
            tree.insert("", "end", values=row)

        # 📌 Agregar la tabla a la ventana
        tree.pack(padx=20, pady=20)

        # 📌 Agregar un botón para cerrar la ventana
        close_button = tk.Button(data_window, text="Cerrar", command=data_window.destroy, font=("Helvetica", 10), bg="red", fg="white")
        close_button.pack(pady=10)

    except FileNotFoundError:
        data_window = tk.Toplevel(root)
        data_window.title("Datos de Infracciones")
        label = tk.Label(data_window, text="No se encontró el archivo de infracciones.", font=("Helvetica", 12))
        label.pack(padx=20, pady=20)

# Crear los botones sobre el canvas (pero ocultos al inicio)
restart_button = tk.Button(root, text="🔄 Reiniciar", font=("Helvetica", 14, "bold"), command=restart_simulation, bg="blue", fg="white")
show_csv_button = tk.Button(root, text="📜 Ver Infracciones", font=("Helvetica", 14, "bold"), command=show_csv_data, bg="purple", fg="white")

# 📌 Ubicarlos en el centro del canvas (225, 220 y 225, 270)
restart_button_window = canvas.create_window(225, 220, window=restart_button, state="hidden")  
show_csv_button_window = canvas.create_window(225, 270, window=show_csv_button, state="hidden")

update_id = None  # Almacena el identificador del after()

def update():
    global update_id

    if not police_active and not moto.infractions_active:
        moto.moving = True  # 🔥 Solo permitir movimiento si no hay infracción

    if moto.moving:  
        moto.move()
        moto.update_zone()
        moto.update_speed()

    speed_label.config(text=f"Velocidad: {moto.speed:.1f} km/h")
    speed_bar["value"] = moto.speed
    zone_label.config(text=f"Zona: {moto.current_zone['name']}")

    canvas.config(bg=moto.current_zone["color"])  

    if moto.check_speed():
        trigger_alert()  # 🔥 Ahora se llama correctamente cada vez que la moto excede el límite

    canvas.delete("moto")
    canvas.create_image(moto.location[0], moto.location[1], image=moto_icon, tags="moto")

    if police_active:
        move_police()

    update_id = root.after(50, update)

update()
root.mainloop()