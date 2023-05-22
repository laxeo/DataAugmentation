# DataAugmentation

This repository contains two key projects for image manipulation and management, particularly useful for object detection tasks.

## DataAugmenter

The DataAugmenter performs data augmentation on images with bounding box regions. Key features include various transformations, an interactive mode for manually approving transformation results, automatic saving of transformed images and corresponding updated bounding box coordinates.

## ImageManager

ImageManager is a Python-based tool for managing Object Detection Models in Microsoft Azure's CustomVision.ai. It provides functionalities for uploading and downloading images from a specific Custom Vision project.

## Quick Start

1. Clone the repository to your local machine.
2. Install the necessary Python packages mentioned in the prerequisites section of each project's README.
3. For **DataAugmenter**, place your images and the `image_regions.json` file in the `input` directory. Then, run `DataAugmenter.py` with appropriate flags.
4. For **ImageManager**, update the `ImageManager.py` script with your Azure Custom Vision resource's details. Then, run `ImageManager.py` with the correct arguments depending on whether you want to upload or download images.

## Usage

Install the required Python packages for each project. Then, run the corresponding scripts in the command line with the appropriate flags and arguments. For detailed usage instructions, refer to the individual README files in each project's directory.
