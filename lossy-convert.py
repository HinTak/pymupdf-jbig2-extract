#!/usr/bin/env python

# Copyright 2024 Hin-Tak Leung

# extract all image masks from a pdf (consisting of scans, many from LuraDocument)

import sys
import os

import fitz

from PIL import Image
import io

fname = sys.argv[1] if len(sys.argv) == 2 else None
if not fname:
    raise SystemExit()

doc = fitz.open(fname)

page_count = doc.page_count

for page in doc.pages():
    pno = page.number
    ImageList = page.get_images()
    # 151 [(303, 0, 1280, 1920, 8, 'DeviceRGB', '', 'Im152', 'FlateDecode')]
    if ((ImageList[0][8] == 'FlateDecode') and (ImageList[0][5] == 'DeviceRGB')):
        xref = ImageList[0][0]
        print(pno, xref)
        img = Image.open(io.BytesIO(doc.extract_image(xref)['image']))
        tmpfilename = "tmp-%d-%d.jpg" % (pno, xref)
        img.save(tmpfilename, optimize=True)
        page.replace_image(xref, filename=tmpfilename)
        os.remove(tmpfilename)
doc.save("1.pdf")
