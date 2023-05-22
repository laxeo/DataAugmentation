# DataAugmenter

## Overview

This Python script package is designed to perform data augmentation on images with bounding box regions, such as those used in object detection tasks. Data augmentation includes transformations such as rotation, shifting, scaling, and others, which can be applied to enhance the diversity of data in training sets, hence improving the performance of machine learning models.

The package provides the following key features:
1. Various transformations including Horizontal Flip, Vertical Flip, Random Rotation, Shift, Scale and Rotate, Random Brightness and Contrast, Hue Saturation Value Adjustment, Gaussian Noise, Motion Blur, and Contrast Limited Adaptive Histogram Equalization (CLAHE).
2. An interactive mode that allows you to view and manually approve each transformation result.
3. The ability to automatically save all transformed images without user interaction.
4. The transformed images and corresponding updated bounding box coordinates are saved in the output directory, ensuring easy use for subsequent machine learning tasks.

## Prerequisites

- **Python**: The scripts are written in Python and require a Python environment to run. Python 3.7 or later is recommended.
- **Libraries**: The scripts use the following Python libraries:
    - **albumentations**: This is used for performing the image and bounding box transformations.
    - **cv2 (OpenCV)**: This is used for reading and writing images, and also for changing image color spaces.
    - **matplotlib**: This is used for visualizing the bounding boxes on the images.
    - **multiprocessing**: This is used to manage concurrent image visualizations.
    - **argparse**: This is used for handling command-line arguments.
    - **os**: This is used for handling file and directory paths.
    - **json**: This is used for reading and writing JSON files.

You can install these libraries using pip:

```python
pip install albumentations opencv-python matplotlib multiprocessing argparse
```

## Key Scripts

1. **DataAugmentationManager.py**: This script defines the `ImageTransformer` class that handles the image and bounding box transformations.
2. **ImageVisualization.py**: This script provides functions for visualizing the bounding boxes on the images and an interactive mode for manual approval of transformations.
3. **DataAugmenter.py**: This is the main script that uses the `ImageTransformer` class and visualization functions to process the images and save the results. It can be run from the command line and offers a range of options for controlling the augmentation process.

## How to use

### Input Data

Store your images (.jpg) and image_regions.json file in the `input` directory. The image_regions.json should have the following format:

```json
{
  "image_name_1": [
    [xmin, ymin, width, height, "class_name"],
    ...
  ],
  "image_name_2": [
    [xmin, ymin, width, height, "class_name"],
    ...
  ],
  ...
}
```

## Running the Scripts

1. **Data Augmentation**: To perform data augmentation on your images, you can run the `DataAugmenter.py` script with the `-t` flag. You will also need to specify the input directory (with `-input`), output directory (with `-output`), and number of transformations per image (with `-num`). If you want to automatically save all transformed images without the interactive mode, you can add the `-y` flag. Here's an example:

```python
python DataAugmenter.py -t -input ./input -output ./output -num 5 -y
```

2. **View Images**: To view the augmented images along with their bounding boxes, you can run the `DataAugmenter.py` script with the `-v` flag and specify the directory containing the images and `image_regions.json` file (with `-output`). Here's an example:

```python
python DataAugmenter.py -v -output ./output
```
For both of the above commands, the script will look for a JSON file named `image_regions.json` in the specified directory. This JSON file should contain the bounding box coordinates and labels for each image.

## Troubleshooting

If you encounter any issues while using these scripts, try the following troubleshooting steps:

- **Image file not found**: Ensure that all image files mentioned in the `image_regions.json` file are present in the input directory. The image file names in the JSON file should not include the '.jpg' extension.
- **JSON file not found**: Ensure that the `image_regions.json` file is located in the input directory.
- **Issues with transformations**: Ensure that the bounding box coordinates in the `image_regions.json` file are in the correct format (`[xmin, ymin, width, height, "class_name"]`). The coordinates should be relative, i.e., in the range [0, 1], with the origin at the top-left corner of the image.
- **Issues with saving images or `image_regions.json`**: Ensure that the output directory exists and you have the necessary permissions to write to it. If not, you can create the directory or change its permissions using `os.makedirs` or `os.chmod`, respectively.

