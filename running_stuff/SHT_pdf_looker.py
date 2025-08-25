import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import fitz  # PyMuPDF
import matplotlib.pyplot as plt
from PIL import Image
import io

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']


def extract_maps(doc, direc, fn):
    for page_number in range(len(doc)):
        page = doc[page_number]
        image_list = page.get_images(full=True)

        # print(f"Page {page_number + 1} has {len(image_list)} images")

        def get_img_data(img_list_item):
            xref = img_list_item[0]
            pix = fitz.Pixmap(doc, xref)

            # Export pixmap as PNG bytes
            png_bytes = pix.tobytes("png")
            img_data = Image.open(io.BytesIO(png_bytes))
            return img_data

        def trim_whitespace(arr):
            ih = int(arr.shape[0] / 2)  # index for horizontal cut
            iv = int(arr.shape[1] / 2)  # index for vertical

            # get border rgb value
            bi = arr[ih, :50, :3]  # look at first 50 pts along horizontal cut
            bv = min(np.sum(bi, axis=1))

            horiz, vert = arr[ih, :, :], arr[:, iv, :]
            ih0, ih1, iv0, iv1 = 0, horiz.shape[0] - 1, 0, vert.shape[0] - 1
            while np.sum(horiz[ih0, :3]) >= 1.5 * bv:
                ih0 += 1
            while np.sum(horiz[ih1, :3]) >= 1.5 * bv:
                ih1 -= 1
            while np.sum(vert[iv0, :3]) >= 1.5 * bv:
                iv0 += 1
            while np.sum(vert[iv1, :3]) >= 1.5 * bv:
                iv1 -= 1

            # add padding to include width of border
            ih0, iv0 = max([0, ih0 - 2]), max([0, iv0 - 2])
            ih1, iv1 = min([horiz.shape[0] - 1, ih1 + 2]), min([vert.shape[0] - 1, iv1 + 2])

            return arr[iv0:iv1, ih0:ih1, :]

        yellow = get_img_data(image_list[1])
        map = get_img_data(image_list[2])
        yellow = yellow.resize(map.size)
        y, m = yellow.convert('RGBA'), map.convert('RGBA')
        comb = Image.alpha_composite(y, m)
        half = int(comb.width / 2)

        img_arr = np.array(comb)
        left_arr = img_arr[:, :half, :]  # [height pix, width pix, rgba]
        right_arr = img_arr[:, half:, :]

        # trim whitespace
        left_trim = trim_whitespace(left_arr)
        right_trim = trim_whitespace(right_arr)

        # copy legend from right to left
        if 'Map1' in fn:
            left_trim[-110:-22, 22:22 + 238, :] = right_trim[-110:-22, -260:-22, :]
        elif 'Map4' in fn:
            left_trim[-220:-132, -273:-22, :] = right_trim[-110:-22, -273:-22, :]
        else:
            left_trim[-140:-22, -275:-22, :] = right_trim[-140:-22, -275:-22, :]

        l, r = Image.fromarray(left_trim), Image.fromarray(right_trim)
        l, r = l.convert('RGB'), r.convert('RGB')

        fnl = ''.join([fn[:4], 'a', fn[4:]])
        fnr = ''.join([fn[:4], 'b', fn[4:]])
        l.save(f'{direc}extracted/{fnl}')
        print(f'saved extracted/{fnl}')
        r.save(f'{direc}extracted/{fnr}')
        print(f'saved extracted/{fnr}')

        # optional plotting for debugging
        # fig, (ax1, ax2) = plt.subplots(ncols=2)
        # ax1.imshow(l)
        # ax1.axis("off")
        # # ax1.title(f"Left")
        # ax2.imshow(r)
        # ax2.axis("off")
        # # ax2.title(f"Right")
        # plt.show()


direc = 'C:/Users/willi/Dropbox/running_stuff/2025_Superior100/'
fns = os.listdir(direc)
for fn in fns:
    if fn.endswith('.pdf'):
        doc = fitz.open(f'{direc}/{fn}')
        extract_maps(doc, direc, fn)

if __name__ == '__main__':
    pass
