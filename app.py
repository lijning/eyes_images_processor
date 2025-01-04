from flask_cors import CORS
from flask import Flask, request, send_file, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from algorithms import detect_face_eyes_mtcnn


app = Flask(__name__)
cors = CORS(app)


def process_image(image_path, target_size=(200, 100)):
    app.logger.info(image_path)
    app.logger.info(type(image_path))
    image = cv2.imread(image_path)
    croped, flag = detect_face_eyes_mtcnn(image)

    if flag >= 0:
        # 缩放图片到目标大小
        result = cv2.resize(croped, target_size)
        return result
    else:
        # 缩放原始图片到目标大小
        image = cv2.resize(image, target_size)
        return image


def combine_images(images):
    # 简单的拼接，假设所有图像大小相同
    rows = []
    for i in range(0, len(images), 3):
        row = np.hstack(images[i:i+3])
        rows.append(row)
    combined_image = np.vstack(rows)
    return combined_image


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/process_images', methods=['POST'])
def process_images():
    uploaded_files = request.files
    processed_images = []
    for _, file in enumerate(uploaded_files.values()):
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        # file_path = 'uploads/' + filename
        file.save(file_path)
        processed_image = process_image(file_path)
        processed_images.append(processed_image)
        os.remove(file_path)
    combined_image = combine_images(processed_images)
    preocessed_image_path = os.path.join('outputs', 'processed_image.jpg')
    cv2.imwrite(preocessed_image_path, combined_image)
    return send_file(preocessed_image_path, mimetype='image/jpeg')


if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    app.run(debug=True)
