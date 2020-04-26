from PIL import Image

#defines var as Image.open() object
apple = Image.open("C:/git/applebottomgenius/images/apple.jpg")
smile = Image.open("C:/git/applebottomgenius/images/smile.png")
orange = Image.open("C:/git/applebottomgenius/images/orange.jpg")
#
# ##show images
# #apple.show()
# #smile.show()
#
# apple_cursed = apple.quantize(colors=2, method=None, kmeans=1, palette=None)
#
# apple_cursed.show()
#
# #print(apple_size)
#
#
# print(end)

#blackboy = Image.new('RGB', (1920,1080), color=0)

#blackboy.show()

orange_w, orange_h = orange.size

orange_basewidth = orange_w

wpercent = (orange_basewidth/float(apple.size[0]))




GodGasped = Image.blend(apple, orange, 0.5)

GodGasped.show()