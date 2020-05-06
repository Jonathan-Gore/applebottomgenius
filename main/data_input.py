from PIL import Image
import os
import sys
import numpy as np

from skimage.metrics import structural_similarity as ssim
from skimage.color import rgb2gray
from skimage.io import imread


#Grabs the current working directory and moves up once into the parent directory
#This allows us to write to a temp folder, later will become important, also looks cleaner
directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

#im1 = Image.open(sys.argv[1])
#im1 = Image.open("C:/git/applebottomgenius/temp/rotate_temp/rotate180degrees.jpg")
im1 = Image.open("C:/git/applebottomgenius/temp/rotate_temp/rotate180degrees.jpg")
im2 = Image.open("C:/git/applebottomgenius/images/jpg/apple.jpg")
#im2 = Image.open("C:/git/applebottomgenius/images/jpg/Honeycrisp.jpg")

# print(im1.format)
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


#needs to updating to conform with William's pillowtest.py (much better/flexible)
def resizeImages(image1, image2):
    #print(image1.size)
    #print(image2.size)

    # makes this variable global/accessible between functions
    #global image1_resize

    image1_resize = image1.resize(image2.size)

    #print(image1_resize.size)
    #print(image2.size)

    image1_resize.show()


#resizeImages(im1, im2)


#rotates an image by 359 degrees in 1 degree intervals, saves to temp folder
##current issues: rotateDict currently organizes images assuming scales of decimals, bot literal order
def rotateImage(image1):
    #image1.show()
    #image1.rotate(45).show()
    #image1.rotate(x).save("C:/git/applebottomgenius/temp/" +degrees[x]+ image.jpg")

    degreeList = list(range(1, 360))

    i=0
    while i < len(degreeList):
        image1.rotate(i, fillcolor = white).save("C:/git/applebottomgenius/temp/rotate_temp/rotate"+str(degreeList[i])+"degrees.jpg")
        i += 1

    fileList = os.listdir("C:/git/applebottomgenius/temp/rotate_temp/")

    #x=0
    #while x < len(fileList):
    #    print(fileList[x])
    #    x += 1
    global rotateDict
    rotateDict = {fileList[i]: degreeList[i] for i in range(len(degreeList))}

    # Printing resultant dictionary
    print("Resultant dictionary is : " + str(rotateDict))
    print("rotateImage function completed")
    #y=0
    #while y < len(rotateDict):
    #    print("Resultant dictionary is : " + str(rotateDict[y]))
    #    y += 1

#rotateImage(im1)

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

compareImages(im1, im2)


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