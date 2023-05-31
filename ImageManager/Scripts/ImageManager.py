from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from CustomVisionManager import CustomVisionManager
import argparse

# Replace with valid values
ENDPOINT =
training_key =  # key1
prediction_key =  # key2
prediction_resource_id = 

print("Creating Credentials")
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(
    in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# Initialize CustomVision Manager
manager = CustomVisionManager(trainer, predictor)

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-upload", action="store_true",
                    help="Upload images to Custom Vision")
parser.add_argument("-export", action="store_true",
                    help="Download images from specific project")
parser.add_argument("-project", type=str, help="Project Name")
parser.add_argument("-have_tag", type=str,
                    help="Specify an unique Tag name that the images must include in")
parser.add_argument("-only_tag", type=str,
                    help="Specify an unique Tag name that you are interested in for the images")
parser.add_argument("-folder", type=str,
                    help="Path to the folder containing the images")

args = parser.parse_args()

if args.upload:
    project_name = args.project
    have_tag = args.have_tag
    only_tag = args.only_tag
    input_folder = args.folder

    project = manager.get_project_by_name(project_name)
    image_regions = manager.read_image_regions(input_folder)
    img_tags = manager.get_or_create_tag(project.id, image_regions)
    manager.add_images_with_regions(
        project.id, image_regions, input_folder, have_tag=have_tag, only_tag=only_tag)

if args.export:
    project_name = args.project
    output_folder = args.folder
    have_tag = args.have_tag
    only_tag = args.only_tag

    project = manager.get_project_by_name(project_name)
    
    manager.get_all_tagged_images(project.id)

    manager.download_images_and_regions(
        project.id, output_folder, have_tag=have_tag, only_tag=only_tag)
