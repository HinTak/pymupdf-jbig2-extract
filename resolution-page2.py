#!/usr/bin/env python

# Copyright 2024 Hin-Tak Leung

# Calculate the resolution of a page image's mask, based on the 2nd page. Also flag tricky problems.

import sys
import os

import fitz

fname = sys.argv[1] if len(sys.argv) == 2 else None
if not fname:
    raise SystemExit()

doc = fitz.open(fname)

for page in doc.pages():
    if (page.number == 1):
        if (len(page.get_images()) != 2):
            print("Number of images per page:", len(page.get_images()))
        page.clean_contents()
        il = page.get_images()
        bounds = page.mediabox
        #print(page.bound())
        for img in il:
            xref = img[1]
            if (xref > 0):
                c = doc.extract_image(xref)
                #print(c['width'], c['height'],c['xres'], c['yres'])
                a = c['width'] / (bounds.x1 - bounds.x0) * 72
                b = c['height'] / (bounds.y1 - bounds.y0) * 72
                #print( c['width'] / (bounds.x1 - bounds.x0) * 72, c['height'] / (bounds.y1 - bounds.y0) * 72)
                dpi = 300
                if (c['cs-name'] == 'DeviceGray'):
                    dpi = 360
                if (abs(a - dpi) > 1) or (abs(b - dpi) > 1):
                    print("Not OK", dpi, a, b)
                else:
                    if (dpi == 300):
                        print("OK-A")
                    if (dpi == 360):
                        print("OK-B")
