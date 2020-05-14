from PIL import Image
import os, shutil
import sys
import numpy as np
import itertools

from skimage.metrics import structural_similarity as ssim
from skimage.color import rgb2gray
from skimage.io import imread

'''
util.py serves as a aggregation of all essential utility functions for APG

A potential future internal structure for APG could be as such:

main.py -- references inputs/outputs with utility functions found in util.py
util.py -- toolbox for APG
rcnn.py -- communicator for Matterport Mask_RCNN modified model

**Changelog**
5/13/20
-- Added combineALLImages(), compares all images in a dir to eachother with smart recursion (itertools.combination)
 - outputs a 'similarlist' that contains all images that had 70% or highier similarities with eachother

'''



#Grabs the current working directory and moves up once into the parent directory
#This allows us to write to a temp folder, later will become important, also looks cleaner
directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
directory1 = "Z:\Datasets\Apples\downloads\Applefruit\compare"
tempdirectory = (directory + "/temp/rotate_temp/")

#global color variables
white = (255,255,255)

im1 = Image.open("C:\\git\\applebottomgenius\\images\\jpg\\goodapple1.jpg")
im2 = Image.open("C:/git/applebottomgenius/images/jpg/goodapple2.jpg")


## merges two images into a horizontal concatenation
def concatenateWide(image1, image2):
    dst = Image.new('RGB', (image1.width + image2.width, image1.height))
    dst.paste(image1, (0, 0))
    dst.paste(image2, (image1.width, 0))
    return dst

## merges two images into a vertical concatenation
def concatenateTall(image1, image2):
    dst = Image.new('RGB', (image1.width, image1.height + image2.height))
    dst.paste(image1, (0, 0))
    dst.paste(image2, (0, image1.height))
    return dst

##example of the .save function
#concatenateTall(apple, orange).save('concatenateTall.jpg')



## Blendfactor operates on a scale from 0-1, 0 = 100% image1 and 1 = 100% image2
def imageBlend(image1, image2, BlendFactor):

    bFactor = BlendFactor
    image1_resize = image1.resize(image2.size)

    print("Resized apple.jpg to fit orange.jpg: ", image1_resize.size)

    compare_images = concatenateTall(image1_resize, image2)
    compare_images.show()

    GodGasped = Image.blend(image1_resize, image2, bFactor)

    GodGasped.show()


## confirms that image is JPEG and if PNG converts. Needs further error handling to avoid crashes in future
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


## takes in image, how many variations to save
# Saves image set to temp/rotate_temp
def rotateImage(image1, variations):

    #i don't know how to handle errors
    if (variations < 1 or variations > 360):
        print("Error: rotateImage(image, integer between 1 and 360)")
    else:
        # split into array on '\\' (\ is escape), return the value of the last elem
        fileName = image1.filename.split('\\').pop()

        print('image name: ' +  fileName)
        folderName = fileName.split('.')[0] + "Variations"

        try:
            os.mkdir(directory + "/temp/rotate_temp/" + folderName)
        except FileExistsError as e:  ## if failed, report it back to the user ##
            print ("Error: %s - %s." % (e.filename, e.strerror))
            pass

        variationDict = {}
        for x in range(variations):
            intervals = int(360/variations*x)
            imageName = "/" + fileName.split('.')[0] + str(intervals) + "degrees.jpg"
            print(imageName)
            #print("intervals: " + str(intervals))
            saveLocation = directory + "/temp/rotate_temp/" + folderName + imageName
            #print("save location ::  " + saveLocation)
            image1.rotate(intervals, fillcolor = white).save(saveLocation)
            variationDict.update({str(intervals): saveLocation})

        fileList = os.listdir(directory + "/temp/rotate_temp/")

        print("printed " + str(variations) + " variations of " + fileName)

    return variationDict

#vDict = rotateImage(im1, 30)
## uses SSIM to compare two images of the same size
def compareImages(image1, image2):

    image1a = np.array(image1.resize(image2.size))
    image2a = np.array(image2)

    #ssim(compare_image, base_image, data_range={What range to compare}
    structural_similarity = ssim(image1a, image2a, multichannel=True, data_range=image2a.max() - image2a.min())
    return structural_similarity

# allowing for variables to return values outside of function
# result = compareImages(im1, im2)
# print("printing compareImages function value after running it: " + str(result))

## compares all images within a directory and writes a copylist.txt with every duplicate pair
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
    with open(file_directory + "\\" + 'similarlist.txt', 'w') as filehandle:
        for similarimage in similarlist:
            filehandle.write('%s\n' % similarimage)
    return similarlist

# results = compareALLImages(directory1)
# print(results)

## Under development
def compareVariations(userinput, variationDict):
    smiledegrees = 0
    currentbest = 0

    for key in variationDict:
        print("printing key, then dictionary[key]")
        print(" ")
        print(key)
        print(variationDict[key])

        image1 = Image.open(variationDict[key])

        image1a = np.array(image1.resize(userinput.size))
        image2a = np.array(userinput)

        structural_similarity = ssim(image1a, image2a, multichannel=True, data_range=image2a.max() - image2a.min())
        if structural_similarity > currentbest:
            currentbest = structural_similarity
            smiledegrees = [key]

        print(structural_similarity)
        ssimScores = {key,structural_similarity}
        print(ssimScores)

        # if ssimScores[key] > currentbest:
        #     currentbest = ssimScores[key]

    print("degrees to rotate smile: " + str(smiledegrees))
    return smiledegrees

#compareVariations(im2, vDict)

## unsure, maybe Tempfile python module for images
def tempClean(folder_path):

    for filename in os.path.join(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. ReasonL %s' % (file_path, e))


tempClean(tempdirectory)

#def main():

# test_dictionary = {30:"image30", 60:"image60", 90:"image90"}
#
# print(test_dictionary[30])