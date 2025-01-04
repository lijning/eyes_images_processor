import cv2
from mtcnn import MTCNN
import numpy as np

from typing import Optional, Tuple


def detect_face_eyes_mtcnn(image: np.ndarray) -> Tuple[Optional[np.ndarray], int]:
    """
    该函数使用 MTCNN 算法检测人脸和眼睛，并根据眼睛位置裁剪图像。

    参数:
    image (np.ndarray): 输入的图像数据，以 numpy 数组形式表示。

    返回:
    Tuple[Optional[np.ndarray], int]: 一个元组，第一个元素是裁剪后的图像，如果未检测到人脸或眼睛则为 None；
                                第二个元素是状态码，0 表示成功，-1 表示未检测到人脸或眼睛。
    """
    # 初始化 MTCNN 检测器
    detector = MTCNN()
    # 使用 MTCNN 检测人脸
    result = detector.detect_faces(image)
    if result:
        for face in result:
            # 获取人脸关键点信息
            keypoints = face['keypoints']
            # 获取左眼和右眼的关键点
            left_eye = keypoints['left_eye']
            right_eye = keypoints['right_eye']

            cv2.circle(image, left_eye, 2, (0, 255, 0), 2)
            cv2.circle(image, right_eye, 2, (0, 255, 0), 2)

            # 计算左右眼的中点
            mid_point = ((left_eye[0] + right_eye[0])//2,
                         (left_eye[1] + right_eye[1])//2)
            # 计算左右眼之间的距离（曼哈顿距离）
            distance = abs(left_eye[1] - right_eye[1]) + \
                abs(left_eye[0] - right_eye[0])

            # 计算裁剪区域的边界
            x1, x2 = mid_point[0] - distance, mid_point[0] + distance
            y1, y2 = mid_point[1] - distance//2, mid_point[1] + distance//2

            # 裁剪图像
            croped = image[y1:y2, x1:x2]
            return croped, 0

    return None, -1


if __name__ == "__main__":
    # 调用函数

    image = cv2.imread('test.jpg')
    croped, _ = detect_face_eyes_mtcnn(image)

    result = cv2.resize(croped, (200, 100))

    cv2.imshow('Image', result)
    # 等待用户按键，0 表示无限等待，直到用户按下按键
    cv2.waitKey(0)
    # 销毁所有创建的窗口
    cv2.destroyAllWindows()
