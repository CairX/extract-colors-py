from PIL import Image

im = Image.open('gameboy.png', 'r')
width, height = im.size
print(im.mode)
pixel_values = list(im.getdata())


pixels = len(pixel_values)
print("\n[ RESULT {}]".format(pixels))
print(width)
print(height)

counter = dict()
for i in range(pixels):
    color = pixel_values[i]

    # print(i)
    # print(color)

    if color in counter:
        counter[color] += 1
    else:
        counter[color] = 1

for key, value in sorted(counter.items(), key=lambda x: x[1], reverse=True):
    print("{0:15}:{1:>7}% ({2})".format(str(key), "{0:.2f}".format(value / pixels * 100), value))
