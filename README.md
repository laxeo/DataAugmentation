# ImageManager

ImageManager is a Python-based tool that interacts with the REST API of Microsoft Azure's CustomVision.ai to manage Object Detection Models.

## Prerequisites

Make sure you have the following setup before using ImageManager:

- <b>Python 3.6 or higher</b>
- <b>An Azure account with an active subscription</b>
- <b>An Azure Custom Vision resource created</b>
- <b>Python packages installed:</b>
  - <b>azure-cognitiveservices-vision-customvision</b>
  - <b>msrest</b>
  - <b>requests</b>
  - <b>argparse</b>

Install the required packages using the following command:

```
pip install azure-cognitiveservices-vision-customvision msrest requests argparse
```

## Configuration

Replace the placeholders in the ImageManager.py script with valid values:

- <b>ENDPOINT:</b> Your Custom Vision resource's endpoint URL
- <b>training_key:</b> Your Custom Vision resource's training key
- <b>prediction_key:</b> Your Custom Vision resource's prediction key
- <b>prediction_resource_id:</b> Your Custom Vision resource's resource ID

Find these values in the Azure portal, under your Custom Vision resource's "Keys and Endpoint" tab.

## Usage

The ImageManager.py script supports the following command line arguments:

- <b>-upload:</b> Upload images to a Custom Vision project
- <b>-export:</b> Download images from a specific Custom Vision project
- <b>-project:</b> Name of the Custom Vision project
- <b>-have_tag:</b> Specify a unique tag name that the images must include
- <b>-only_tag:</b> Specify a unique tag name that you are interested in for the images
- <b>-folder:</b> Path to the folder containing the images

### Uploading images

Upload images to a Custom Vision project:

```
python ImageManager.py -upload -project "Project Name" -folder "/path/to/input/folder" [-have_tag "tag_name"] [-only_tag "tag_name"]
```

Replace "<b>Project Name</b>" with the name of your Custom Vision project, "<b>/path/to/input/folder</b>" with the path to the folder containing the images, and "<b>tag_name</b>" with the tag name(s) you are interested in. The <b>-have_tag</b> and <b>-only_tag</b> arguments are optional.

### Downloading images

Download images from a specific Custom Vision project:

```
python ImageManager.py -export -project "Project Name" -folder "/path/to/output/folder" [-have_tag "tag_name"] [-only_tag "tag_name"]
```

Replace "<b>Project Name</b>" with the name of your Custom Vision project, "<b>/path/to/output/folder</b>" with the path to the folder where you want to save the downloaded images, and "<b>tag_name</b>" with the tag name(s) you are interested in. The <b>-have_tag</b> and <b>-only_tag</b> arguments are optional.

## Notes

- The input folder for uploading images should contain an <b>image_regions.json</b> file with the region information for the images.
- When downloading images, the output folder will be created if it does not exist. The downloaded images and their region information will be saved in this folder.
