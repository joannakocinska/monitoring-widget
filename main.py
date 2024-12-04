import tkinter as tk
from tkinter import ttk
import psutil
import time
from datetime import datetime
from py3nvml.py3nvml import (
    nvmlInit,
    nvmlShutdown,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetUtilizationRates,
    nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetTemperature
)

# Inicjalizacja NVML
nvmlInit()

def get_gpu_stats():
    try:
        handle = nvmlDeviceGetHandleByIndex(0)  # Pierwsza karta graficzna
        utilization = nvmlDeviceGetUtilizationRates(handle)
        memory = nvmlDeviceGetMemoryInfo(handle)
        gpu_temperature = nvmlDeviceGetTemperature(handle, 0)  # Temperatura GPU
        gpu_usage = utilization.gpu
        gpu_memory = memory.used / memory.total * 100
        return gpu_usage, gpu_memory, gpu_temperature
    except Exception:
        return "N/A", "N/A", "N/A"

# Funkcja do aktualizacji statystyk
def update_stats():
    if root.winfo_exists():
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        uptime = time.time() - psutil.boot_time()
        uptime_str = str(datetime.utcfromtimestamp(uptime).strftime("%H:%M:%S"))
        current_time = datetime.now().strftime("%H:%M:%S")

        gpu_usage, gpu_memory, gpu_temp = get_gpu_stats()

        # Aktualizacja danych
        time_label.config(text=f"{current_time}")
        uptime_label.config(text=f"{uptime_str}")
        cpu_label.config(text=f"CPU: {cpu_usage}%")
        ram_label.config(text=f"RAM: {ram_usage}%")
        gpu_label.config(text=f"GPU: {gpu_usage}% | VRAM: {gpu_memory:.1f}% | Temp: {gpu_temp}°C")

        root.after(1000, update_stats)

# Funkcja do zamknięcia aplikacji
def on_close(event=None):
    nvmlShutdown()
    root.destroy()

# Tworzenie głównego okna
root = tk.Tk()
root.title("System Monitor Widget")
root.attributes("-topmost", True)
root.attributes("-alpha", 0.8)
root.geometry("250x80")
root.configure(bg="lightgray")

# Układ tabeli
time_label = ttk.Label(root, text="Time", anchor="w", font=("Arial", 10), background="lightgray")
uptime_label = ttk.Label(root, text="Uptime", anchor="w", font=("Arial", 10), background="lightgray")
cpu_label = ttk.Label(root, text="CPU: ", anchor="w", font=("Arial", 10), background="lightgray")
ram_label = ttk.Label(root, text="RAM: ", anchor="w", font=("Arial", 10), background="lightgray")
gpu_label = ttk.Label(root, text="GPU: ", anchor="w", font=("Arial", 10), background="lightgray")

# Dodawanie do siatki
time_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
uptime_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)
cpu_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
ram_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)
gpu_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)

# Obsługa zamknięcia okna
root.protocol("WM_DELETE_WINDOW", on_close)

# Uruchomienie pętli aktualizacji
update_stats()

# Start głównej pętli aplikacji
root.mainloop()
