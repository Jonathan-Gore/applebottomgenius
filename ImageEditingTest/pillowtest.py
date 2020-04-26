#pillowtest following tutorial https://auth0.com/blog/image-processing-in-python-with-pillow/
from PIL import Image
import sys

#inputs: background, foreground, foreground scale (between >0 and 1)
#$python pillowtest.py combineImages honeycrisp.jpg scary.png .5
def combineImages(background, foreground, fScale="1"):

    fScale=float(fScale)
    background = Image.open('images/' + background)
    foreground = Image.open('images/' + foreground)

    bg_w, bg_h = background.size

    #smile resize
    basewidth = bg_w
    wpercent = (basewidth/float(foreground.size[0]))
    hsize = int((float(foreground.size[1])*float(wpercent)))
    foreground = foreground.resize((int(basewidth*fScale),int(hsize*fScale)), Image.ANTIALIAS)

    foreground_w, foreground_h = foreground.size


    offset = ((bg_w - foreground_w) // 2, (bg_h - foreground_h) // 2)
    background.paste(foreground, offset, foreground)
    background.show()


#apple = Image.open('apple.jpg')
#smile = Image.open('face.png')
#combineImages(apple,smile)

if sys.argv[1] == 'combineImages':
    #attempting option arguments, there must be a better way
    if len(sys.argv) > 4:
        combineImages(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        combineImages(sys.argv[2], sys.argv[3])
