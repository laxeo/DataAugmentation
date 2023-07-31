import albumentations as A
import cv2
import json
import os


class ImageTransformer:

    def __init__(self, imamge, image_region, image_name):
        self.image = imamge
        self.bboxes = image_region
        self.image_name = image_name
        self.index = 0
        self.transform = self.transform_pipeline()
        self.new_image_regions = {}
        self.transformed_image = None
        self.transformed_bboxes = None

    def bboxes_preprocessing(self):
        for bbox in self.bboxes:
            bbox[2] = bbox[0] + bbox[2]
            bbox[3] = bbox[1] + bbox[3]

    def bboxes_postprocessing(self):
        new_image_regions = {}
        for key, bboxes in self.new_image_regions.items():
            new_bboxes = []
            for bbox in bboxes:
                new_bbox = (bbox[0], bbox[1], bbox[2] -
                            bbox[0], bbox[3] - bbox[1], bbox[4])
                new_bboxes.append(new_bbox)
            new_image_regions[key] = new_bboxes
        return new_image_regions

    def transform_pipeline(self):
        return A.Compose([
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.5),
            A.RandomRotate90(p=0.5),
            A.ShiftScaleRotate(
                shift_limit=0.05, scale_limit=0.3, rotate_limit=15, p=0.5),
            A.RandomBrightnessContrast(p=0.5),
            A.HueSaturationValue(
                hue_shift_limit=0.2, sat_shift_limit=0.2, val_shift_limit=0.2, p=0.5),
            A.GaussNoise(p=0.5),
            A.MotionBlur(p=0.5),
            A.CLAHE(p=0.5),
        ], bbox_params=A.BboxParams(format='albumentations'))

    def transform_image(self):
        # covert image to RGB
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        # apply transformations
        transformed = self.transform(image=image, bboxes=self.bboxes)

        # convert back to BGR
        self.transformed_image = cv2.cvtColor(
            transformed['image'], cv2.COLOR_RGB2BGR)

        self.transformed_bboxes = transformed['bboxes']

    def save_image(self, output_folder):
        
        file_name = f"{self.image_name}_t_{self.index}"

        print("Saving Image: " + file_name)

        # save image
        os.makedirs(output_folder, exist_ok=True)

        image_path = os.path.join(output_folder, file_name + ".jpg")

        cv2.imwrite(image_path, self.transformed_image)

        # save image region
        self.new_image_regions[file_name] = self.transformed_bboxes

        self.index += 1

    def save_image_regions(self):
        print(f"Saving Region Info for {self.image_name}")

        # convert bboxes back to customvision.ai format
        image_regions = self.bboxes_postprocessing()

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
        
        return sorted_image_regions