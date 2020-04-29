from PIL import Image

##defines var as Image.open() object
apple = Image.open("C:/git/applebottomgenius/images/apple.jpg")
orange = Image.open("C:/git/applebottomgenius/images/orange.jpg")
smile = Image.open("C:/git/applebottomgenius/images/smile.jpg")

##merges two images into a horizontal concatenation
def concatenateWide(image1, image2):
    dst = Image.new('RGB', (image1.width + image2.width, image1.height))
    dst.paste(image1, (0, 0))
    dst.paste(image2, (image1.width, 0))
    return dst

##merges two images into a vertical concatenation
def concatenateTall(image1, image2):
    dst = Image.new('RGB', (image1.width, image1.height + image2.height))
    dst.paste(image1, (0, 0))
    dst.paste(image2, (0, image1.height))
    return dst

##example of the .save function
#concatenateTall(apple, orange).save('concatenateTall.jpg')

##function that resizes the image1 parameter to image2 and then blends the two together
##Blendfactor operates on a scale from 0-1, 0 = 100% image1 and 1 = 100% image2
def imageBlend(image1, image2, BlendFactor):

    bFactor = BlendFactor
    image1_resize = image1.resize(image2.size)

    print("Resized apple.jpg to fit orange.jpg: ", image1_resize.size)

    compare_images = concatenateTall(image1_resize, image2)
    compare_images.show()

    GodGasped = Image.blend(image1_resize, image2, bFactor)

    GodGasped.show()

imageBlend(apple, smile, 0.2)
