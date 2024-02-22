#!/usr/bin/env python

# Copyright 2024 Hin-Tak Leung

# extract all image masks from a pdf (consisting of scans, many from LuraDocument)

import sys
import os

import fitz

import subprocess

fname = sys.argv[1] if len(sys.argv) == 2 else None
if not fname:
    raise SystemExit()

doc = fitz.open(fname)

page_count = doc.page_count

print_once = True

to_invert = False

xref_hash = {}

#for pno in range(page_count):
#    il = doc.get_page_images(pno)
for page in doc.pages():
    pno = page.number
    # page.get_text("rawdict")
    if (print_once and (len(page.get_images()) != 2)):
        print("Number of images per page:", len(page.get_images()))
    page.clean_contents() # page.clean_contents(sanitize=False) also does not # page.wrap_contents() does not correct the situation
    il = page.get_images()
    if (print_once):
        print(len(il))
    for img in il:
        xref = img[1]
        if (xref > 0):
#            a = fitz.Pixmap(doc, xref)
            c = doc.extract_image(xref)["image"]
            if (print_once):
                print(doc.extract_image(xref)['ext'], doc.extract_image(xref)['colorspace'], doc.extract_image(xref)['cs-name'])
                if (doc.extract_image(xref)['cs-name'] == 'DeviceGray'):
                    to_invert = True
                print_once = False
#            a.save("page%03d-%d.png" % (pno+1, xref))
            if (not (xref in xref_hash.keys())):
                fout = open('tmp-jbig-%03d-%d' % (pno+1, xref), "wb")
                fout.write(c)
                fout.close()
#                xref_hash[xref] = 1
#            subprocess.call('jbig2dec -e -o alt-page%03d-%d.png tmp-jbig-%03d-%d' % (pno+1, xref, pno+1, xref), shell=True)
#            os.remove('tmp-jbig-%03d-%d' % (pno+1, xref))

my_env = {}
if to_invert:
    my_env['INVERTED'] = "true"

subprocess.call('python %s/gist.github.com/kmlyvens/b532c7aec2fe2bd8214ae2b3faf8f741/raw/be7accd836fb98b2c1308ddc73f4de01e567af40/pdfsimp.py tmp-jbig-* > tmp.pdf' % (os.path.dirname(__file__)) , shell=True, env=my_env)
subprocess.call('rm -f tmp-jbig-*', shell=True)
subprocess.call('mutool clean -sg \"%s\" out.pdf 1,%d' % (fname, page_count), shell=True)
subprocess.call('qpdf --deterministic-id --pages \"%s\" 1 tmp.pdf 2-%d \"%s\" %d -- \"%s\" \"%s\"' % ("out.pdf", page_count - 1, "out.pdf", 2, fname, os.path.basename(fname)), shell=True)
subprocess.call('rm -f tmp.pdf', shell=True)
subprocess.call('rm -f out.pdf', shell=True)
