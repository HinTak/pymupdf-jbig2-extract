#!/usr/bin/env python

# Copyright 2024 Hin-Tak Leung

# convert page 2 of a pdf to png

import sys
import os

import fitz

fname = sys.argv[1] if len(sys.argv) == 2 else None
if not fname:
    raise SystemExit()

doc = fitz.open(fname)

for page in doc.pages():
    if (page.number == 1):
        a = page.get_pixmap()
        a.save("%s.png" % (os.path.basename(fname)))
        exit(0)
