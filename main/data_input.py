from PIL import Image
import os

#Grabs the current working directory and moves up once into the parent directory
#This allows us to write to a temp folder, later will become important, also looks cleaner
directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

#im1 = Image.open(sys.argv[1])
im1 = Image.open("C:/git/applebottomgenius/images/smile.png")


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

cleanImage(im1)


