import csv
import requests
import os
import logging

logging.basicConfig(level=logging.INFO)

# Function to download an image
def download_image(url, directory, filename):
    # Check if the directory exists and if not, create it
    os.makedirs(directory, exist_ok=True)

    # Try to download the image
    try:
        # Send a GET request to the image URL, stream the response
        response = requests.get(url, stream=True)

        # Raise an error if the request failed
        response.raise_for_status()

        # Open the destination file and write the image data into it in chunks
        with open(os.path.join(directory, filename), 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): 
                f.write(chunk)
    except Exception as e:
        # Log any errors encountered
        logging.error(f'Error downloading image {url}: {e}')
        return False

    return True

# Function to download a number of images specified in a CSV file
def download_images_from_csv(csv_filename, directory, num_images, url_column_name='image_url'):
    # Open the CSV file
    with open(csv_filename, 'r', encoding='UTF-8') as csvFile:
        reader = csv.reader(csvFile)
        url_column = -1
        count = 0

        # Process each row in the CSV file
        for row in reader:
            # Find the column with the URLs
            if reader.line_num == 1:
                url_column = row.index(url_column_name)
                continue

            # Stop after downloading the specified number of images
            if count >= num_images:
                break

            # Get the image URL
            url = row[url_column]

            # Construct the destination filename
            filename = f'image{reader.line_num-1}.jpeg'

            # Download the image
            if download_image(url, directory, filename):
                count += 1
