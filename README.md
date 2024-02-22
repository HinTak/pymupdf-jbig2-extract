Some pdf's (those from the Internet Archive, apparently) consist of mostly
scans. Structurally, every page is a background image with a mask, occasionally with
an invisible OCR text layer, and sometimes a lower-res preview/thumbnail image.

This is mostly a script trying to convert the mask into an image losslessly.
The background image (often just yellowing paper) makes the document less-readable.
Smaller pdf with single image per page (without requiring compositing) also loads faster, too.

Out of about 400 such pdf's:

* There is one (also apparently the oldest by its creation/modification date)
which has this strange problem (indented and spaced for readability from original)
of every page of 308 refering to every image and mask. Hence the `page.clean_contents()` line
and `mutool clean -sg ...`.

```
4668 0 obj
<< /Type /Page
   /Parent 924 0 R
   ...
   /Resources<<...
               /XObject<</I1 4673 0 R
                         /I2 4674 0 R
                         /I3 4675 0 R
                         ...
                         /I308 4980 0 R
                         /Im001 4981 0 R
                         ...
                         /Im308 5595 0 R
                         >>
               >>
   /MediaBox[0 0 487 832]
   /StructParents 0
  >>
```

* There is one other pdf which seems to have (blank) pages with mask only.

* The script under `gist.github.com` has been modified in small ways. The original can be found at that location.
  (migrated to python 3, and changing resolution and color inversion; see below).

* For about 90% (i.e. about 40) of the 400, the heuristics (some masks have a "DeviceGray" color space name, and need to
be inverted to be black-text-on-white-background. Such images also have resolution 360 dpi instead of 300 dpi) seems to work.
But 5 pdfs appear white-text-on-black-background, and about 40 have the wrong resolution with values 150dpi, 300dpi, 350 dpi, 360dpi, 500dpi,
and ~642dpi being seen. Script `convert-page2.py` is intended to be run on the result pdf to quickly see the color of page 2 of result.
`resolution-page2.py` is intended to be run on the source pdf quickly to tell the resolution, plus the
every-page-references-every-image and mask-only-page problems.



