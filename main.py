import os
import tkinter as tk

from tkinter import filedialog, simpledialog, messagebox
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class ImageAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Анализ изображений и видео")
        self.master.geometry("300x450")

        # Кнопки
        self.btn_image_analysis = tk.Button(master, text="Загрузка конфигураций", command=self.load_config)
        self.btn_image_analysis.pack(pady=10)


        self.btn_image_analysis = tk.Button(master, text="Анализ изображения", command=self.open_image_analysis)
        self.btn_image_analysis.pack(pady=10)

        self.btn_video_analysis = tk.Button(master, text="Анализ видео", command=self.open_video_analysis)
        self.btn_video_analysis.pack(pady=10)

        self.btn_ip_camera_analysis = tk.Button(master, text="Анализ видеоопотока с IP-камеры",
                                                command=self.open_ip_camera_analysis)
        self.btn_ip_camera_analysis.pack(pady=10)

        self.btn_webcam_analysis = tk.Button(master, text="Анализ с веб-камеры", command=self.open_webcam_analysis)
        self.btn_webcam_analysis.pack(pady=10)

        self.use_video_device = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(master, text="Использовать видеокарту", variable=self.use_video_device)
        self.checkbutton.pack(pady=10)

        self.show_content = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(master, text="Визуализировать", variable=self.show_content)
        self.checkbutton.pack(pady=10)

        self.save_img_object = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(master, text="Сохранять изображения объектов", variable=self.save_img_object)
        self.checkbutton.pack(pady=10)

        self.on_write_date_scv = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(master, text="Сохранять данные в формате csv", variable=self.on_write_date_scv)
        self.checkbutton.pack(pady=10)

        self.on_write_date_txt = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(master, text="Сохранять данные в формате txt", variable=self.on_write_date_txt)
        self.checkbutton.pack(pady=10)

    def fix_config(self):
        cmd = ''
        if self.on_write_date_scv.get():
            cmd += '--save-csv '
        if self.on_write_date_txt.get():
            cmd += '--save-txt '
        if self.use_video_device.get():
            cmd += "--device 0 "
        if self.save_img_object.get():
            cmd += "--save-crop "
        if self.show_content.get():
            cmd += "--view-img  "
        # else:
        #     cmd += "--device cpu "
        return cmd

    def load_config(self):
        self.config = {
            'weights': f"--weights {os.path.join(ROOT_DIR,'config','model.pt')} ",
            'data': f"--data {os.path.join(ROOT_DIR,'config','data.yaml')} ",
        }


    def open_image_analysis(self):
        window = tk.Toplevel(self.master)
        window.title("Анализ изображения")
        window.geometry('240x240')

        tk.Label(window, text="Выберите изображение:").pack(pady=5)
        tk.Button(window, text="Выбрать файл", command=lambda: self.select_file(window)).pack(pady=5)

        tk.Label(window, text="Процент точности:").pack(pady=5)
        accuracy_scale = tk.Scale(window, from_=0.5, to=1.0, resolution=0.01, orient=tk.HORIZONTAL)
        accuracy_scale.pack(pady=5)

        tk.Button(window, text="Сканировать", command=lambda: self.scan_image(accuracy_scale.get())).pack(pady=10)

    def open_video_analysis(self):
        window = tk.Toplevel(self.master)
        window.title("Анализ видео")
        window.geometry('240x240')

        tk.Label(window, text="Выберите видео:").pack(pady=5)
        tk.Button(window, text="Выбрать файл", command=lambda: self.select_file(window)).pack(pady=5)

        tk.Label(window, text="Процент точности:").pack(pady=5)
        accuracy_scale = tk.Scale(window, from_=0.5, to=1.0, resolution=0.01, orient=tk.HORIZONTAL)
        accuracy_scale.pack(pady=5)

        tk.Button(window, text="Сканировать", command=lambda: self.scan_video(accuracy_scale.get())).pack(pady=10)

    def open_ip_camera_analysis(self):
        window = tk.Toplevel(self.master)
        window.title("Анализ видеоопотока с IP-камеры")
        window.geometry('520x240')

        tk.Label(window, text="URL IP-камеры:").pack(pady=5)
        ip_input = tk.Entry(window, width=420)
        ip_input.pack(pady=5)

        tk.Label(window, text="Процент точности:").pack(pady=5)
        accuracy_scale = tk.Scale(window, from_=0.5, to=1.0, resolution=0.01, orient=tk.HORIZONTAL)
        accuracy_scale.pack(pady=5)

        tk.Button(window, text="Сканировать",
                  command=lambda: self.scan_ip_camera(ip_input.get(), accuracy_scale.get())).pack(pady=10)

    def open_webcam_analysis(self):
        window = tk.Toplevel(self.master)
        window.title("Анализ с веб-камеры")
        window.geometry('240x240')

        tk.Label(window, text="Процент точности:").pack(pady=5)
        accuracy_scale = tk.Scale(window, from_=0.5, to=1.0, resolution=0.01, orient=tk.HORIZONTAL)
        accuracy_scale.pack(pady=5)

        tk.Button(window, text="Сканировать", command=lambda: self.scan_webcam(accuracy_scale.get())).pack(pady=10)

    def select_file(self, window):
        self.file_path = filedialog.askopenfilename()
        # if file_path:
        #     messagebox.showinfo("Выбранный файл", f"Выбрано: {file_path}")

    def scan_image(self, accuracy):
        cmd = f"python {os.path.join(ROOT_DIR, 'yolov5', 'detect.py')} " \
              f"{self.config.get('weights')} " \
              f"{self.config.get('data')} " \
              f"--source {self.file_path} " \
              f"--project {os.path.join(ROOT_DIR, 'content', 'images')} " \
              f"--name {datetime.now().date()} " \
              f"--conf-thres {accuracy} " \
              f"--exist-ok " \
              f"--line-thickness 1 "\
              f"--classes 0 "
        cmd += self.fix_config()
        os.system(cmd)
        # messagebox.showinfo("Сканирование изображения", f"Сканирование изображения с точностью {accuracy}")

    def scan_video(self, accuracy):
        cmd = f"python {os.path.join(ROOT_DIR, 'yolov5', 'detect.py')} " \
              f"{self.config.get('weights')} " \
              f"{self.config.get('data')} " \
              f"--source {self.file_path} " \
              f"--project {os.path.join(ROOT_DIR, 'content', 'video')} " \
              f"--name {datetime.now().date()} " \
              f"--conf-thres {accuracy} " \
              f"--exist-ok " \
              f"--line-thickness 1 "\
              f"--classes 0 "
        cmd += self.fix_config()
        os.system(cmd)
        # messagebox.showinfo("Сканирование видео", f"Сканирование видео с точностью {accuracy} и размером {size}")

    def scan_ip_camera(self, ip_address, accuracy):
        cmd = f"python {os.path.join(ROOT_DIR, 'yolov5', 'detect.py')} " \
              f"{self.config.get('weights')} " \
              f"{self.config.get('data')} " \
              f"--source '{ip_address}' " \
              f"--project {os.path.join(ROOT_DIR, 'content', 'images')} " \
              f"--name {datetime.now().date()} " \
              f"--conf-thres {accuracy} " \
              f"--exist-ok " \
              f"--line-thickness 1 "\
              f"--classes 0 "
        cmd += self.fix_config()
        os.system(cmd)

    def scan_webcam(self, accuracy):
        cmd = f"python {os.path.join(ROOT_DIR, 'yolov5', 'detect.py')} " \
              f"{self.config.get('weights')} " \
              f"{self.config.get('data')} " \
              f"--source 0 " \
              f"--project {os.path.join(ROOT_DIR, 'content', 'video')} " \
              f"--name {datetime.now().date()} " \
              f"--conf-thres {accuracy} " \
              f"--exist-ok " \
              f"--line-thickness 1 "\
              f"--classes 0 "
        cmd += self.fix_config()
        os.system(cmd)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnalyzerApp(root)
    root.mainloop()
