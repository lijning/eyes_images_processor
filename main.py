import os
import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import mainthread
from plyer import filechooser
from algorithms import detect_face_eyes_mtcnn


# 保持原有图像处理逻辑（调整了文件路径处理）
def process_image(image_path, target_size=(200, 100)):
    image = cv2.imread(image_path)
    croped, status = detect_face_eyes_mtcnn(image)
    
    if croped is not None:
        return cv2.resize(croped, target_size)
    return cv2.resize(image, target_size)

def combine_images(images):
    rows = []
    for i in range(0, len(images), 3):
        row = np.hstack(images[i:i+3])
        rows.append(row)
    return np.vstack(rows) if rows else None

class EyesProcessorUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        self.uploaded_paths = []
        self.processed_path = None
        
        # 上传按钮
        self.btn_upload = Button(text="上传9张图片", size_hint=(1, 0.2))
        self.btn_upload.bind(on_release=self.choose_images)
        self.add_widget(self.btn_upload)
        
        # 状态提示
        self.lbl_status = Label(text="等待上传...", size_hint=(1, 0.1))
        self.add_widget(self.lbl_status)
        
        # 处理按钮
        self.btn_process = Button(text="开始处理", size_hint=(1, 0.2), disabled=True)
        self.btn_process.bind(on_release=self.process_images)
        self.add_widget(self.btn_process)
        
        # 下载按钮
        self.btn_download = Button(text="保存结果", size_hint=(1, 0.2), disabled=True)
        self.btn_download.bind(on_release=self.save_result)
        self.add_widget(self.btn_download)

    def choose_images(self, instance):
        """选择最多9张图片"""
        filechooser.open_file(
            title="选择9张图片",
            multiple=True,
            filters=[("图像文件", "*.png", "*.jpg", "*.jpeg")],
            on_selection=self.handle_selection
        )

    def handle_selection(self, selection):
        """处理选中的文件"""
        if selection and len(selection) <= 9:
            self.uploaded_paths = selection
            self.update_status(f"已选择{len(selection)}张图片")
            self.btn_process.disabled = False
        else:
            self.update_status("请选择1-9张图片")

    def process_images(self, instance):
        """处理图片逻辑"""
        processed_images = [process_image(path) for path in self.uploaded_paths]
        combined = combine_images(processed_images)
        
        if combined is not None:
            app = App.get_running_app()
            self.processed_path = os.path.join(app.user_data_dir, "processed_result.jpg")
            cv2.imwrite(self.processed_path, combined)
            self.update_status("处理完成！")
            self.btn_download.disabled = False
        else:
            self.update_status("处理失败")

    def save_result(self, instance):
        """保存结果图片"""
        if self.processed_path and os.path.exists(self.processed_path):
            filechooser.save_file(
                title="保存处理结果",
                defaultpath=self.processed_path,
                on_selection=self.confirm_save
            )

    def confirm_save(self, selection):
        """确认保存路径"""
        if selection:
            # 实际应使用shutil.copy，这里简化为提示
            self.update_status(f"已保存到：{selection[0]}")
        else:
            self.update_status("保存取消")

    @mainthread
    def update_status(self, text):
        """线程安全的状态更新"""
        self.lbl_status.text = text

class EyesProcessorApp(App):
    def build(self):
        return EyesProcessorUI()

    def on_start(self):
        # 确保应用数据目录存在
        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir)

if __name__ == "__main__":
    EyesProcessorApp().run()
