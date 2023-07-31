import argparse
import ImgDownloadManager

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='Download images specified in a CSV file.')
parser.add_argument('-csv', metavar='csv', type=str, required=True,
                    help='the CSV file to read')
parser.add_argument('-dir', metavar='dir', type=str, default='.',
                    help='the directory to save the images to')
parser.add_argument('-num', metavar='num', type=int, default=10,
                    help='the number of images to download')

# Parse the command line arguments
args = parser.parse_args()

# Call the function to download the images
ImgDownloadManager.download_images_from_csv(args.csv, args.dir, args.num)
