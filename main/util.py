from PIL import Image
import os
import sys
import numpy as np
import itertools

from skimage.metrics import structural_similarity as ssim
from skimage.color import rgb2gray
from skimage.io import imread


#Grabs the current working directory and moves up once into the parent directory
#This allows us to write to a temp folder, later will become important, also looks cleaner
directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
directory1 = "Z:\Datasets\Apples\downloads\Applefruit"

#im1 = Image.open(sys.argv[1])
#im1 = Image.open("C:/git/applebottomgenius/temp/rotate_temp/rotate180degrees.jpg")
im1 = Image.open("C:/git/applebottomgenius/temp/rotate_temp/rotate180degrees.jpg")
im2 = Image.open("C:/git/applebottomgenius/images/jpg/apple.jpg")
#im2 = Image.open("C:/git/applebottomgenius/images/jpg/Honeycrisp.jpg")



# im1= Image.open("Z:\\Datasets\\Apples\\downloads\\Applefruit\\compare\\green.jpg")
# im2= Image.open("Z:\\Datasets\\Apples\\downloads\\Applefruit\\compare\\red.jpg")



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

<<<<<<< Updated upstream
#rotateImage(im1)
=======
#rotateImage(im1, 11)
>>>>>>> Stashed changes

#uses SSIM to compare two images of the same size
def compareImages(image1, image2):

    image1a = np.array(image1.resize(image2.size))
    image2a = np.array(image2)

    #ssim(compare_image, base_image, data_range={What range to compare}
    structural_similarity = ssim(image1a, image2a, multichannel=True, data_range=image2a.max() - image2a.min())
    return structural_similarity

##allowing for variables to return values outside of function
# result = compareImages(im1, im2)
# print("printing compareImages function value after running it: " + str(result))

#compares all images within a directory and writes a copylist.txt with every duplicate pair
def compareALLImages(file_directory):

    files = os.listdir(file_directory)
    similarlist = []

    # concatenate directory into file list
    for i in range(len(files)):
        files[i] = str(file_directory + "\\" + files[i])

    index = range(len(files))
    for a, b in itertools.combinations(index, 2):
        image1 = Image.open(files[a])
        image2 = Image.open(files[b])

        image1a = np.array(image1.resize(image2.size))
        image2a = np.array(image2)

        print("Comparing image " + str(a) + " " + "vs image " + str(b))
        structural_similarity = ssim(image1a, image2a, multichannel=True, data_range=image2a.max() - image2a.min())

        image1.close()
        image2.close()

        if structural_similarity >= 0.7:
            print("Completed Comparison: !!WARNING!! ")
            print("Images are >= 70% similar, adding both images to similarlist.txt")
            print(" ")
            similarlist.append(files[a])
            similarlist.append(files[b])
        elif structural_similarity < 1:
            print("Completed comparison: Images are sufficiently unique")
            print(" ")

<<<<<<< Updated upstream
compareImages(im1, im2)
=======
    with open(file_directory + "\\" + 'similarlist.txt', 'w') as filehandle:
        for similarimage in similarlist:
            filehandle.write('%s\n' % similarimage)
>>>>>>> Stashed changes

    return similarlist

results = compareALLImages(directory1)
print(results)

# a_list = ("a", "b", "c", "d", "e")
#
# for a, b in itertools.combinations(a_list, 2):
#     if a == b:
#         print("a is equal to b, need to print this combination")
#     else:
#         print(a, b)

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
        structural_similarity = ssim(image1a, image2a, multichannel=True, data_range=image2a.max() - image2a.min())
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