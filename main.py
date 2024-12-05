import os
import tkinter as tk

from tkinter import filedialog, simpledialog, messagebox
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class ImageAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Анализ изображений и видео")
        self.master.geometry("400x300")

        # Кнопки
        self.btn_image_analysis = tk.Button(master, text="Анализ изображения", command=self.open_image_analysis)
        self.btn_image_analysis.pack(pady=10)

        self.btn_video_analysis = tk.Button(master, text="Анализ видео", command=self.open_video_analysis)
        self.btn_video_analysis.pack(pady=10)

        self.btn_ip_camera_analysis = tk.Button(master, text="Анализ видеоопотока с IP-камеры", command=self.open_ip_camera_analysis)
        self.btn_ip_camera_analysis.pack(pady=10)

        self.btn_webcam_analysis = tk.Button(master, text="Анализ с веб-камеры", command=self.open_webcam_analysis)
        self.btn_webcam_analysis.pack(pady=10)

    def open_image_analysis(self):
        window = tk.Toplevel(self.master)
        window.title("Анализ изображения")
        window.geometry('240x240')

        tk.Label(window, text="Выберите изображение:").pack(pady=5)
        tk.Button(window, text="Выбрать файл", command=lambda: self.select_file(window)).pack(pady=5)

        tk.Label(window, text="Процент точности:").pack(pady=5)
        accuracy_input = tk.Entry(window)
        accuracy_input.pack(pady=5)

        # tk.Label(window, text="Размер:").pack(pady=5)
        # size_input = tk.Entry(window)
        # size_input.pack(pady=5)

        tk.Button(window, text="Сканировать", command=lambda: self.scan_image(accuracy_input.get())).pack(pady=10)

    def open_video_analysis(self):
        window = tk.Toplevel(self.master)
        window.title("Анализ видео")
        window.geometry('240x240')

        tk.Label(window, text="Выберите видео:").pack(pady=5)
        tk.Button(window, text="Выбрать файл", command=lambda: self.select_file(window)).pack(pady=5)

        tk.Label(window, text="Процент точности:").pack(pady=5)
        accuracy_input = tk.Entry(window)
        accuracy_input.pack(pady=5)

        tk.Label(window, text="Размер:").pack(pady=5)
        size_input = tk.Entry(window)
        size_input.pack(pady=5)

        tk.Button(window, text="Сканировать", command=lambda: self.scan_video(accuracy_input.get(), size_input.get())).pack(pady=10)

    def open_ip_camera_analysis(self):
        window = tk.Toplevel(self.master)
        window.title("Анализ видеоопотока с IP-камеры")
        window.geometry('520x240')

        tk.Label(window, text="URL IP-камеры:").pack(pady=5)
        ip_input = tk.Entry(window, width=420)
        ip_input.pack(pady=5)

        tk.Label(window, text="Процент точности:").pack(pady=5)
        accuracy_input = tk.Entry(window)
        accuracy_input.pack(pady=5)

        tk.Label(window, text="Размер:").pack(pady=5)
        size_input = tk.Entry(window)
        size_input.pack(pady=5)

        tk.Button(window, text="Сканировать", command=lambda: self.scan_ip_camera(ip_input.get(), accuracy_input.get(), size_input.get())).pack(pady=10)

    def open_webcam_analysis(self):
        window = tk.Toplevel(self.master)
        window.title("Анализ с веб-камеры")
        window.geometry('240x240')

        tk.Label(window, text="Процент точности:").pack(pady=5)
        accuracy_input = tk.Entry(window)
        accuracy_input.pack(pady=5)


        tk.Button(window, text="Сканировать", command=lambda: self.scan_webcam(accuracy_input.get())).pack(pady=10)

    def select_file(self, window):
        self.file_path = filedialog.askopenfilename()
        # if file_path:
        #     messagebox.showinfo("Выбранный файл", f"Выбрано: {file_path}")

    def scan_image(self, accuracy):
        cmd = f"python {os.path.join(ROOT_DIR,'yolov5','detect.py')} " \
               f"--weights {os.path.join(ROOT_DIR, 'myyolo.pt')} " \
               f"--source {self.file_path} " \
               f"--project {os.path.join(ROOT_DIR, 'content', 'images')} " \
               f"--name {datetime.now().date()} " \
               f"--conf-thres {accuracy} " \
               f"--exist-ok " \
               f"--view-img " \
              f"--line-thickness 1"
        os.system(cmd)
        messagebox.showinfo("Сканирование изображения", f"Сканирование изображения с точностью {accuracy}")

    def scan_video(self, accuracy, size):
        messagebox.showinfo("Сканирование видео", f"Сканирование видео с точностью {accuracy} и размером {size}")

    def scan_ip_camera(self, ip_address, accuracy, size):
        messagebox.showinfo("Сканирование IP-камеры", f"Сканирование потока с IP-камеры {ip_address} с точностью {accuracy} и размером {size}")

    def scan_webcam(self, accuracy):
        cmd = f"python {os.path.join(ROOT_DIR, 'yolov5', 'detect.py')} " \
              f"--weights {os.path.join(ROOT_DIR, 'myyolo.pt')} " \
              f"--source 0 " \
              f"--project {os.path.join(ROOT_DIR, 'content', 'video')} " \
              f"--name {datetime.now().date()} " \
              f"--conf-thres {accuracy} " \
              f"--exist-ok " \
              f"--view-img " \
              f"--line-thickness 1 " \
              f"--save-csv "
        os.system(cmd)
        messagebox.showinfo("Сканирование веб-камеры", f"Сканирование веб-камеры с точностью {accuracy}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnalyzerApp(root)
    root.mainloop()
