# pip install Pillow
# refer https://stackoverflow.com/questions/12988915/how-to-extract-bitmap-data-from-ttf-bitmap-typeface-for-a-pov-display for extract font
# 'create_char_map' calculates weight based on the font, and 'getchar' dynamically decides the charater. But the result looks too noisy, 
# therefore not making the output looks better than the hardcoded character mapping result. Mabye should not use linear calculation.

import tkinter
from tkinter import filedialog
from PIL import Image, ImageFont
#import webbrowser

def create_char_map():
    characters = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    weights = []

    font_name = "Courier_Prime/CourierPrime-Regular.ttf"
    font_size = 16 # px
    font_color = "#000000" # HEX Black
    font = ImageFont.truetype(font_name, font_size)
    max_weight = 0

    # Loop through the characters needed and save to desired location
    for character in characters:
        # Get text size of character
        width, height = font.getsize(character)
        pix = font.getmask(character)
        #print("Bitmap for %c, %d X %d" % (character, width, height))
        weight = 0
        for y in range(len(pix)//width): # the actual row might be smaller than hegith
            for x in range(width):
                #print("%03d " % pix[x+width*y], end="")
                weight += pix[x+width*y]
            #print("")
        weights.append(weight)
        if weight>max_weight: max_weight = weight
        #print("%c => %d" % (character, weight))
    # uniform the weight to 0~256*3-1
    # for revert image: char_map = {int(w*767/max_weight):ch for (w, ch) in zip(weights, characters)}
    char_map = {767-int(w*767/max_weight):ch for (w, ch) in zip(weights, characters)}
    return char_map

def get_pixmap(path):
    im = Image.open(path)
    print('Original: ' + str(im.size))
    size = 320
    if im.size[0] > size:
        resized_image = im.resize((size, int(size * im.size[1] / im.size[0])))
        pixmap = resized_image.load()
        pixmap_size = resized_image.size
        print('Resized: ' + str(pixmap_size))
    else:
        pixmap = im.load()
        pixmap_size = im.size
    return pixmap, pixmap_size

def character(rgb_sum):
    if rgb_sum > 700:     return ' '
    elif rgb_sum > 650:   return ';'
    elif rgb_sum > 600:   return '|'
    elif rgb_sum > 550:   return '/'
    elif rgb_sum > 500:   return 'L'
    elif rgb_sum > 450:   return 'L'
    elif rgb_sum > 400:   return 'L'
    elif rgb_sum > 350:   return 'L'
    elif rgb_sum > 300:   return 'Y'
    elif rgb_sum > 250:   return 'R'
    elif rgb_sum > 200:   return 'K'
    elif rgb_sum > 150:   return 'E'
    elif rgb_sum > 100:   return 'H'
    elif rgb_sum > 50:    return 'M'
    else:                 return 'N'

def getchar(rgb_sum):
    for i in range(1, len(char_keys)):
        if rgb_sum<char_keys[i]:
            if char_keys[i]+char_keys[i-1]>rgb_sum*2: i=i-1
            break
    return char_map[char_keys[i]]

def main():
    #return
    root = tkinter.Tk()
    root.withdraw()
    fin=filedialog.askopenfilename() 
    if(fin):
        pixmap, pixmap_size = get_pixmap(fin)
        file = open('output.txt', 'w')
        for y in range(0, pixmap_size[1]-1, 2):
            line_left=''
            line_right=''
            for x in range(pixmap_size[0]):
                # merge two line into one printed line to keep a better ratio
                rgb_sum = (pixmap[x, y][0] + pixmap[x, y][1] + pixmap[x, y][2] + pixmap[x, y+1][0] + pixmap[x, y+1][1] + pixmap[x, y+1][2])>>1
                line_left+=character(rgb_sum)
                line_right+=getchar(rgb_sum)
            file.write(line_left+'  '+line_right+'\n')
        file.close()
    #webbrowser.open('output.txt') => somehow it would be opened by text editor

if __name__=="__main__":
    char_map = create_char_map()
    char_keys = sorted(char_map)
    #for key in char_keys: print("%d => %c" % (key, char_map[key]))
    main()
