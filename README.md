Pikeman
=======

Bulk PDF processing with Tabula.  Use bounding box output from [Tabula](https://github.com/jazzido/tabula) to export images from multiple PDFs.  Useful for PDF liberation on a large scale.

####Usage

Extract bounding boxes in a JSON document from pdfs in directory `pdfs`:

    > cat multiple_bboxes.json | python pikeman.py pdfs --scale 3
    
  
#####Requirements

ImageMagick
