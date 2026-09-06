#!/usr/bin/env python
# Copyright 2026 Hin-Tak Leung

# Smaller and simpler version of extract-all-mask.py, converting only page 4.
# To look at the 1.25.1->1.25.2 regression.

import sys
import os

import fitz

import subprocess

fname = sys.argv[1] if len(sys.argv) == 2 else None
if not fname:
    raise SystemExit()

doc = fitz.open(fname)

page_count = doc.page_count
print(page_count)

pages =  doc.pages()
il = doc.get_page_images(4)
for img in il:
    xref = img[1]
    print(xref)
    if (xref > 0):
        c = doc.extract_image(xref)["image"]
        raw_data = doc.xref_stream_raw(xref)
        print("ext=", doc.extract_image(xref)['ext'],
              "colorspace=", doc.extract_image(xref)['colorspace'],
              "cs-name=", doc.extract_image(xref)['cs-name'],
              "size=", doc.extract_image(xref)['size'],
              )
        print(doc.extract_image(xref).keys())
#        print(doc.extract_image(xref))
        fout = open('tmp-jbig-%03d-%d' % (5, xref), "wb")
        fout.write(raw_data)
        fout.close()
        subprocess.call('jbig2dec -e -o alt-page%03d-%d.png tmp-jbig-%03d-%d' % (5, xref, 5, xref), shell=True)
        #os.remove('tmp-jbig-%03d-%d' % (5, xref))
