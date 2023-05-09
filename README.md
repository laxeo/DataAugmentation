# ImageManager

ImageManager is a Python-based tool that interacts with the REST API of Microsoft Azure's CustomVision.ai to manage Object Detection Models.

## Prerequisites

Make sure you have the following setup before using ImageManager:

- Python 3.6 or higher
- An Azure account with an active subscription
- An Azure Custom Vision resource created
- Python packages installed:
  - azure-cognitiveservices-vision-customvision
  - msrest
  - requests
  - argparse

Install the required packages using the following command:

```
pip install azure-cognitiveservices-vision-customvision msrest requests argparse
```

## Configuration

Replace the placeholders in the ImageManager.py script with valid values:

- ENDPOINT: Your Custom Vision resource's endpoint URL
- training_key: Your Custom Vision resource's training key
- prediction_key: Your Custom Vision resource's prediction key
- prediction_resource_id: Your Custom Vision resource's resource ID

Find these values in the Azure portal, under your Custom Vision resource's "Keys and Endpoint" tab.

## Usage

The ImageManager.py script supports the following command line arguments:

- -upload: Upload images to a Custom Vision project
- -export: Download images from a specific Custom Vision project
- -project: Name of the Custom Vision project
- -have_tag: Specify a unique tag name that the images must include
- -only_tag: Specify a unique tag name that you are interested in for the images
- -folder: Path to the folder containing the images

### Uploading images

Upload images to a Custom Vision project:

```
python ImageManager.py -upload -project "Project Name" -folder "/path/to/input/folder" [-have_tag "tag_name"] [-only_tag "tag_name"]
```

Replace "Project Name" with the name of your Custom Vision project, "/path/to/input/folder" with the path to the folder containing the images, and "tag_name" with the tag name(s) you are interested in. The -have_tag and -only_tag arguments are optional.

### Downloading images

Download images from a specific Custom Vision project:

```
python ImageManager.py -export -project "Project Name" -folder "/path/to/output/folder" [-have_tag "tag_name"] [-only_tag "tag_name"]
```

Replace "Project Name" with the name of your Custom Vision project, "/path/to/output/folder" with the path to the folder where you want to save the downloaded images, and "tag_name" with the tag name(s) you are interested in. The -have_tag and -only_tag arguments are optional.

## Notes

- The input folder for uploading images should contain an image_regions.json file with the region information for the images.
- When downloading images, the output folder will be created if it does not exist. The downloaded images and their region information will be saved in this folder.
