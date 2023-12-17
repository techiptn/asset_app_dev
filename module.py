from PIL import Image, ImageFont, ImageDraw
import qrcode
import os
import csv

path = os.getcwd()

# Mac font
font = ImageFont.truetype('Arial.ttf', 50)
font2 = ImageFont.truetype('Arial.ttf', 50)
font3 = ImageFont.truetype('Arial.ttf', 70)

# ultiumCAM color
color1 = (0, 114, 206)
color2 = (5, 195, 221)
color3 = (20, 27, 77)

# load the logo image
# loadlogo = input("Input logo file and path:")
# logoimg = Image.open(loadlogo)
logoimg = Image.open('static/img/logo.png')
logoimg = logoimg.convert('RGBA')
logore = logoimg.resize(size=(1100, 236))


# Back ground / inch (label 4'X 2' , 2 = 600px, 4 = 1200px /
# letter size 2551 x 3295 pixels)
w1, h1 = 1200, 600
imgbg = Image.new(mode="RGB", size=(w1, h1), color=(255, 255, 255))


def qr_gen(acode, date, sn, user):
    # Generate QR code
    g_img = qrcode.make(f'{acode}, {sn}')
    g_img2 = g_img.resize(size=(250, 250))

    # Put the logo and QC code on background
    base = imgbg.copy()
    base.paste(logore, (31, 125), logore)
    base.paste(g_img2, (31, 350))
    draw = ImageDraw.Draw(base)
    draw.text((31.25, 31.25), "PROPRIÉTÉ DE / PROPERTY OF", color1, font=font)

    # asset code & date & User
    draw.text((313, 368), 'DATE :', color1, font=font2)
    draw.text((313, 431), 'CODE :', color1, font=font2)
    # draw.text((313, 493), 'NOM / NAME:', color1, font=font2)
    draw.text((313, 493), 'UTILISATEUR / USER :', color1, font=font2)
    draw.text((525, 368), f'{date}', color1, font=font2)
    draw.text((525, 431), f'{acode}', color1, font=font2)
    draw.text((313, 545), f'{user}', color1, font=font2)

    # Size adjusting
    base1 = base.resize(size=(1008, 504))
    base2 = imgbg.copy()
    base2.paste(base1, (32, 32))
    return base2
    # return base


def data_gen(datalist):
    with open(datalist, 'r') as a_list:
        reader = csv.DictReader(a_list)
        data = list(reader)

    v = len(data)
    for i in range(len(data)):
        if data[i]['AssetCode'] == '':
            v = i
            break
    data2 = data[0:v]
    return(data2)


def label_gen(b_list, path, filename, pmark):
    # Positions for label printing
    abc = []
    for i in range(len(b_list)):
        date = b_list[i]['Date']
        acode = b_list[i]['AssetCode']
        sn = b_list[i]['SN']
        name = b_list[i]['UserName']
        abc.append(qr_gen(date, acode, sn, name))

    # 300 dpi letter size (118 = 1cm)
    w2, h2 = 2551, 3295
    letter_bg = Image.new(mode="RGB", size=(w2, h2), color=(255, 255, 255))

    for i in range(len(abc)):
        letter_bg.paste(abc[i], pmark[i+1])

    letter_bg.save(f'{path}/{filename}.png')


