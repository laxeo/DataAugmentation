from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from azure.cognitiveservices.vision.customvision.training.models import CustomVisionErrorException
import os
import requests
import json


class CustomVisionManager:
    def __init__(self, trainer, predictor):
        self.trainer = trainer
        self.predictor = predictor
        self.target_images = []

    def get_project_by_name(self, project_name):
        print("Getting Project Info")
        projects = self.trainer.get_projects()
        project = next(p for p in projects if p.name == project_name)
        return project

    def get_or_create_tag(self, project_id, image_regions):
        print("Checking Tags...")

        # Get the set of tag names from the image_regions JSON
        tag_names = set()
        for regions in image_regions.values():
            for region in regions:
                tag_name = region[-1]
                tag_names.add(tag_name)

        # Get the set of existing tag names
        existing_tags = self.trainer.get_tags(project_id)
        existing_tag_names = {t.name for t in existing_tags}

        for tag_name in tag_names:
            if tag_name in existing_tag_names:
                print("Tag: " + tag_name + " exists")
            else:
                img_tag = self.trainer.create_tag(project_id, tag_name)
                print("Tag: " + tag_name + " created")

        return tag_names

    def read_image_regions(self, input_folder):
        print("Reading Region Info")
        json_file_path = os.path.join(input_folder, "image_regions.json")
        with open(json_file_path, "r") as json_file:
            image_regions = json.load(json_file)
        return image_regions
    
    def get_all_tagged_images(self, project_id):
        print("Getting Tagged Images Info")

        skip = 0
        take = 256  # Maximum number of images per request

        while True:
            batch_images = self.trainer.get_tagged_images(
                project_id, skip=skip, take=take, with_regions=True)
            
            if len(batch_images) == 0:
                break  # No more images to fetch

            self.target_images.extend(batch_images)
            skip += take  # Skip the images we've already fetched
    
    def get_all_untagged_images(self, project_id):
        print("Getting Untagged Images Info")

        skip = 0
        take = 256  # Maximum number of images per request
        
        while True:
            batch_images = self.trainer.get_untagged_images(
                project_id, skip=skip, take=take)
            
            if len(batch_images) == 0:
                break
            
            self.target_images.extend(batch_images)
            skip += take
            print(f"Total images fetched: {len(self.target_images)}")
            
    def add_images_with_regions(self, project_id, image_regions, input_folder, have_tag=None, only_tag=None):
        if not have_tag and only_tag:
            have_tag = only_tag

        base_image_location = os.path.abspath(input_folder)
        existing_tags = self.trainer.get_tags(project_id)
        tagged_images_with_regions = []

        print("Adding images...")

        index = 0
        for file_name in image_regions.keys():
            regions = []
            tags = set()
            for x, y, w, h, tag in image_regions[file_name]:
                tags.add(tag)
                if only_tag and only_tag != tag:
                    continue
                tag_id = next(
                    (t.id for t in existing_tags if t.name == tag), None)
                if tag_id is None:
                    raise ValueError(
                        f"Tag: '{tag}' not found in exisiting tags")
                regions.append(Region(tag_id=tag_id, left=x,
                            top=y, width=w, height=h))

            if have_tag and have_tag not in tags:
                continue

            try:
                with open(os.path.join(base_image_location, file_name + ".jpg"), mode="rb") as image_contents:
                    tagged_images_with_regions.append(ImageFileCreateEntry(
                        name=file_name, contents=image_contents.read(), regions=regions))
            except FileNotFoundError:
                print(
                    f"File not found: {os.path.join(base_image_location, file_name + '.jpg')}")
                continue

            index += 1
        print(f"Total Images to upload {index}...")

        # uploading images in chunks of 64 images per batch (maximum 64)
        for i in range(0, len(tagged_images_with_regions), 64):
            chunk = tagged_images_with_regions[i:i+64]
            try:
                upload_result = self.trainer.create_images_from_files(
                    project_id, ImageFileCreateBatch(images=chunk))
            except CustomVisionErrorException:
                print(f"Error: No File uploaded for chunk starting at index {i}")
                exit(-1)

            sorted_images = sorted(upload_result.images,
                                key=lambda image: image.source_url)

            sorted_images = sorted(
                upload_result.images,
                key=lambda image: (
                    image.source_url.rsplit('_', 1)[0],
                    int(image.source_url.rsplit('_', 1)[1])
                )
            )

            for image in sorted_images:
                print(f"Image file: {image.source_url} | Status: {image.status}")

    def download_images_and_regions(self, project_id, output_folder, have_tag=None, only_tag=None):
        if not have_tag and only_tag:
            have_tag = only_tag

        output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

        if have_tag:
            self.target_images = [img for img in self.target_images if any(
                region.tag_name == have_tag for region in img.regions)]

        image_regions = {}
        # Added dictionary to keep track of indices for each tag_name combination
        file_name_map = {}

        print("Downloading images...")

        index = -1
        for index, image in enumerate(self.target_images, start=0):

            image_url = image.original_image_uri

            if only_tag:
                file_name = only_tag
            else:
                tag_names = sorted(
                    list(set([region.tag_name for region in image.regions])))
                file_name = "_".join(tag_names)

            if file_name not in file_name_map:
                file_name_map[file_name] = 0

            File_Name = f"{file_name}_{file_name_map[file_name]}"

            # Increment the index for the current tag_name combination
            file_name_map[file_name] += 1

            image_filename = os.path.join(output_folder, f"{File_Name}.jpg")

            # Download and save the image
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                with open(image_filename, "wb") as img_file:
                    img_file.write(response.content)
            except requests.exceptions.RequestException as e:
                print(
                    f"Error downloading image from URL: {image_url}, Error: {e}")
                continue

            # Collect region info for the current image
            img_regions = []
            for region in image.regions:
                if only_tag and only_tag != region.tag_name:
                    continue
                region_info = (region.left, region.top,
                               region.width, region.height, region.tag_name)
                img_regions.append(region_info)

            # Store region info in the image_regions dictionary
            image_regions[File_Name] = img_regions

        print(f"Downloaded {index+1} images")

        # Save the image_regions dictionary to a JSON file

        # Sort the image_regions dictionary by keys
        sorted_image_regions = {
            k: image_regions[k] for k in sorted(
                image_regions,
                key=lambda x: (
                    x.rsplit('_', 1)[0],
                    int(x.rsplit('_', 1)[1])
                )
            )
        }

        print("Saving Region Info...")
        with open(os.path.join(output_folder, "image_regions.json"), "w") as json_file:
            json.dump(sorted_image_regions, json_file)

        print("Completed")

        return image_regions
    
    def delete_images(self, project_id, have_tag=None):
        print("Deleting Images...")
        images_to_delete = self.target_images
        if have_tag:
            images_to_delete = [img for img in self.target_images if any(
                region.tag_name == have_tag for region in img.regions)]
        
        # Batch operation for deletion since a request can handle a max of 256 images
        DELETE_BATCH_SIZE = 200
        for i in range(0, len(images_to_delete), DELETE_BATCH_SIZE):
            batch = images_to_delete[i:i + DELETE_BATCH_SIZE]
            batch_ids = [img.id for img in batch]
            
            try:
                # Using the trainer's delete method
                self.trainer.delete_images(project_id, image_ids=batch_ids)
            except CustomVisionErrorException as e:
                print(f"Error deleting images in batch starting at index {i}: {e}")
                continue  # Continue with the next batch even if the current batch fails

