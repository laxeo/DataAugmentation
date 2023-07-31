import random

import cv2
from matplotlib import pyplot as plt

import albumentations as A

BOX_COLOR = (255, 0, 0)  # Red
TEXT_COLOR = (255, 255, 255)  # White


def visualize_bbox(img, bbox, class_name, color=BOX_COLOR, thickness=2):
    """Visualizes a single bounding box on the image"""
    x_min, y_min, x_max, y_max = bbox
    img_size = img.shape
    img_width, img_height = img_size[1], img_size[0]

    x_min = int(x_min * img_width)
    y_min = int(y_min * img_height)
    x_max = int(x_max * img_width)
    y_max = int(y_max * img_height)

    cv2.rectangle(img, (x_min, y_min), (x_max, y_max),
                  color=color, thickness=thickness)

    ((text_width, text_height), _) = cv2.getTextSize(
        class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)),
                  (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(
        img,
        text=class_name,
        org=(x_min, y_min - int(0.3 * text_height)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=3,
        color=TEXT_COLOR,
        lineType=cv2.LINE_8,
        thickness=5
    )
    return img


def visualize_and_wait(image, bboxes, window_name='image'):
    img = image.copy()
    for bbox in bboxes:
        img = visualize_bbox(img, bbox[0:4], bbox[4])
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img)
    while True:
        key = cv2.waitKey(0) & 0xFF
        if key == ord('y'):  # if 'y' is pressed, return True
            cv2.destroyWindow(window_name)
            return True
        elif key == ord('n'):  # if 'n' is pressed, return False
            cv2.destroyWindow(window_name)
            return False
        else:  # if any other key is pressed, print message and continue
            print("Invalid input. Please press 'y' to save or 'n' to continue.")
