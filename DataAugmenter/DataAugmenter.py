import argparse
from DataAugmentationManager import ImageTransformer
import os
import json
import cv2
import argparse
import multiprocessing
import ImageVisualization_v4 as Visualization
import ImageVisualization_v3



def read_image_regions(input_folder):
    print("Reading Region Info")
    json_file_path = os.path.join(input_folder, "image_regions.json")
    with open(json_file_path, "r") as json_file:
        image_regions = json.load(json_file)
    return image_regions


def process_image(input_folder, output_folder, num, auto_save=False):
    
    # Create an empty list to hold all the image region data
    all_image_regions = {}

    image_regions = read_image_regions(input_folder)

    for image_name, image_region in image_regions.items():

        image = cv2.imread(os.path.join(input_folder, image_name + ".jpg"))
        if image is None:
            print(f"Image: '{image_name}.jpg' not found")
            continue

        imagetransformer = ImageTransformer(image, image_region, image_name)
        imagetransformer.bboxes_preprocessing()
        
        print(f"Processing Image: {imagetransformer.image_name}")
        
        if not auto_save:
            if not Visualization.visualize_and_wait(imagetransformer.image, imagetransformer.bboxes, f'{image_name}'):
                continue
              
        for i in range(num):
            imagetransformer.transform_image()

            # Visualize the transformed image in real-time
            # If auto_save is not enabled, ask the user if they want to save
            if not auto_save:
                if Visualization.visualize_and_wait(imagetransformer.transformed_image, imagetransformer.transformed_bboxes, f'{image_name}_t{i}'):
                    # Save the image and regions info
                    imagetransformer.save_image(output_folder)
            else:
                # Save the image and regions info
                imagetransformer.save_image(output_folder)
    
        all_image_regions.update(imagetransformer.save_image_regions())

    # Save all image region data to the output directory
    try:
        with open(os.path.join(output_folder, "image_regions.json"), 'w') as json_file:
            json.dump(all_image_regions, json_file)
        print("Saving Completed")
    except NameError as e:
        print("No matching image found")
        exit(-1)
        
def view_images(output_folder):

    image_regions = read_image_regions(output_folder)
    
    print("Viewing Images...")

    for image_name, image_region in image_regions.items():

        image = cv2.imread(os.path.join(output_folder, image_name + ".jpg"))
        if image is None:
            print(f"Image: '{image_name}.jpg' not found")
            continue

        imagetransformer = ImageTransformer(image, image_region, image_name)
        imagetransformer.bboxes_preprocessing()
        
        p = multiprocessing.Process(target=ImageVisualization_v3.visualize_and_wait, args=(
            imagetransformer.image, imagetransformer.bboxes, f'{image_name}'))
        p.start()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Process some images.')
    parser.add_argument('-t', action='store_true', help='Transform images')
    parser.add_argument('-v', action='store_true', help='View images')
    parser.add_argument('-input', type=str, help='Input folder name')
    parser.add_argument('-output', type=str, help='Output folder name')
    parser.add_argument('-num', type=int, help='Number of iterations')
    parser.add_argument('-y', action='store_true', help='Automatically save all images without interactive mode')

    args = parser.parse_args()

    if args.t:
        process_image(args.input, args.output, args.num, args.y)
    elif args.v:
        view_images(args.output)
