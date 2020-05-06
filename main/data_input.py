from PIL import Image
import os
import sys
import numpy as np

from skimage.metrics import structural_similarity as ssim
from skimage.color import rgb2gray
from skimage.io import imread

"""
taking 2 images
rotate second image X times
for x images compare to image 1
select highest score comparison
return degrees to rotate smile

"""


#Grabs the current working directory and moves up once into the parent directory
#This allows us to write to a temp folder, later will become important, also looks cleaner
directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

#im1 = Image.open(sys.argv[1])

print(directory) # AppleBottomGenius


#im1 = Image.open("C:/git/applebottomgenius/temp/rotate_temp/rotate180degrees.jpg")
#im = Image.open(relativePath + "/temp/rotate_temp/rotate180degrees.jpg")
im1= Image.open(directory + "/images/jpg/Honeycrisp.jpg")
#im2 = Image.open("C:/git/applebottomgenius/images/jpg/Honeycrisp.jpg")


# print(im1.size)
# print(im1.mode)

#im1_array = np.array(im1)
#print(im1_array.shape)


#global color variables
white = (255,255,255)

def cleanImage(dirty_image):

    #print(dirty_image.format)
    if dirty_image.format == "JPEG":
        print(dirty_image.format)
    elif dirty_image.format == "PNG":
        dirty_image_jpg = dirty_image.convert('RGB')
        dirty_image_jpg.save(os.path.join(directory, 'temp', "color.jpg"))
        print("converted a filthy PNG file into a glorious JPG")
    else:
        print("What the heck is this? A TIF? geez, come back with a JPG or a PNG when you are serious about this")
        return

#cleanImage(im1)


#rotates an image by 359 degrees in 1 degree intervals, saves to temp folder
##current issues: rotateDict currently organizes images assuming scales of decimals, bot literal order
def emptyTemp();

def rotateImage(image1, variations):

    if (variations < 1 or variations > 360):
        print("Error: rotateImage(image, integer between 1 and 360)")

    # split into array on '/', return the value of the last elem
    fileName = image1.filename.split('/').pop()

    print('image name: ' +  fileName)
    folderName = fileName.split('.')[0] + "Variations"

    try:
        os.mkdir(directory + "/temp/rotate_temp/" + folderName)
    except FileExistsError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))
        pass

    global rotateDict
    rotateDict = {}
    for x in range(variations):
        print(x)
        intervals = int(360/variations*x)
        imageName = "/rotate" + str(intervals) + "degrees.jpg"
        #print("intervals: " + str(intervals))
        saveLocation = directory + "/temp/rotate_temp/" + folderName + imageName
        #print("save location ::  " + saveLocation)
        image1.rotate(intervals, fillcolor = white).save(saveLocation)
        rotateDict.update({str(intervals): imageName})

    fileList = os.listdir(directory + "/temp/rotate_temp/")

    print("printed " + str(variations) + " variations of " + fileName)

rotateImage(im1, 0)
print(im1.format)
#uses SSIM to compare two images of the same size
def compareImages(image1, image2):

    #image1 = Image.open("C:/git/applebottomgenius/temp/rotate_temp/rotate1degrees.jpg")
    #image1 = Image.open("C:/git/applebottomgenius/images/jpg/apple.jpg")
    #image2 = Image.open("C:/git/applebottomgenius/images/jpg/Honeycrisp.jpg")

    # image1.save('C:/git/applebottomgenius/temp/SSIMa.jpg')
    # image2.save('C:/git/applebottomgenius/temp/SSIMb.jpg')
    #
    # image1a = Image.open('C:/git/applebottomgenius/temp/SSIMa.jpg')
    # image2a = Image.open('C:/git/applebottomgenius/temp/SSIMb.jpg')

    image1a = np.array(image1.resize(image2.size))
    image2a = np.array(image2)

    #ssim can be used with color, but it is a massively more complex process for our needs, so we convert to grayscale
    rgb2gray(image1a)
    rgb2gray(image2a)
    structural_similarity = ssim(image1a, image2a, multichannel=True, gaussian_weights=True, sigma=1.5, use_sample_covariance=False, data_range=1.0)

    print(structural_similarity)

#compareImages(im1, im2)


def compareImagesLoop(image1, image2):

    #image1 = Image.open("C:/git/applebottomgenius/temp/rotate_temp/rotate1degrees.jpg")
    #image1 = Image.open("C:/git/applebottomgenius/images/jpg/apple.jpg")
    #image2 = Image.open("C:/git/applebottomgenius/images/jpg/Honeycrisp.jpg")

    # image1.save('C:/git/applebottomgenius/temp/SSIMa.jpg')
    # image2.save('C:/git/applebottomgenius/temp/SSIMb.jpg')
    #
    # image1a = Image.open('C:/git/applebottomgenius/temp/SSIMa.jpg')
    # image2a = Image.open('C:/git/applebottomgenius/temp/SSIMb.jpg')
    i=0
    while i < len(rotateDict):
        image1a = np.array(image1.resize(image2.size))
        image2a = np.array(image2)

        #ssim can be used with color, but it is a massively more complex process for our needs, so we convert to grayscale
        rgb2gray(image1a)
        rgb2gray(image2a)
        structural_similarity = ssim(image1a, image2a, multichannel=True, gaussian_weights=True, sigma=1.5, use_sample_covariance=False, data_range=1.0)
        print(structural_similarity)
        ssimScores = {i,structural_similarity}
        print(ssimScores)

        i += 1

#compareImagesLoop(im1, im2)




#print(os.listdir("C:/git/applebottomgenius/temp/rotate_temp/"))
# fileList = os.listdir("C:/git/applebottomgenius/temp/rotate_temp/")
#
# x=0
# while x < len(fileList):
#     print(fileList[x])
#     x += 1

#next steps are to make a while loops that calculates every SSIM index value for every rotation of apple image and then writes them to a dictionary.
