import argparse
from DataAugmentationManager import ImageTransformer
import os
import json
import cv2
import argparse


def read_image_regions(input_folder):
    print("Reading Region Info")
    json_file_path = os.path.join(input_folder, "image_regions.json")
    with open(json_file_path, "r") as json_file:
        image_regions = json.load(json_file)
    return image_regions


def process_image(input_folder, output_folder, num):

    image_regions = read_image_regions(input_folder)

    for image_name, image_region in image_regions.items():

        image = cv2.imread(os.path.join(input_folder, image_name + ".jpg"))
        if image is None:
            print(f"Image: '{image_name}.jpg' not found")
            continue

        imagetransformer = ImageTransformer(image, image_region, image_name)
        imagetransformer.bboxes_preprocessing()

        for i in range(num):
            imagetransformer.transform_image()

            # Visualize the transformed image
            # p = multiprocessing.Process(target=Visualization.visualize_and_wait, args=(
            #     transformed_image, transformed_bboxes, f'{image_name}_t{i}'))
            # p.start()

            # Save the image and regions info
            imagetransformer.save_image(output_folder)

    try:
        imagetransformer.save_image_regions(output_folder)
    except NameError as e:
        print("No matching image found")
        exit(-1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some images.')
    parser.add_argument('-input', type=str, help='Input folder name')
    parser.add_argument('-output', type=str, help='Output folder name')
    parser.add_argument('-num', type=int, help='Number of iterations')

    args = parser.parse_args()

    process_image(args.input, args.output, args.num)
