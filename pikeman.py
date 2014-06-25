'''
Functions for converting regions of a pdf to tiff.
'''
import subprocess
import sys
import os
import json
import glob
import argparse

def getStdoutFromCmd(command, shell=False):
    ''' 
    Execute command and capture stdout.
    '''
    child = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE)
    output = ''

    while True:
        out = child.stdout.read(1)
        if out == '' and child.poll() != None:
            break
        if out != '':
            output += out
    return output


def bboxToCrop(bbox, scale=1):
    '''
    Convert a bounding box dict to ImageMagick crop syntax.
    '''

    h = scale * (bbox['x2'] - bbox['x1']) 
    w = scale * (bbox['y2'] - bbox['y1'])

    x = scale * bbox['x1']
    y = scale * bbox['y1']

    return '\'%ix%i+%i+%i\'' % (h, w, x, y)


def convertRegion(pdf, bbox, outfile, scale=1, offset_x=0, offset_y=0, dpi=72):
    '''
    Convert a region of pdf to a tiff.
    '''

    bbox['x1'] = bbox['x1'] + offset_x
    bbox['x2'] = bbox['x2'] + offset_x
    bbox['y1'] = bbox['y1'] + offset_y
    bbox['y2'] = bbox['y2'] + offset_y

    crop = bboxToCrop(bbox, scale)
    density = str(dpi * scale)

    command = ['convert', '-monochrome', '-density', density, '-crop ' + crop, pdf+ '[%i]' % (int(bbox['page']) - 1), outfile]

    print ' '.join(command)

    convertOut = getStdoutFromCmd(' '.join(command), shell=True)


if __name__ == '__main__': 
    '''
    Takes bounding boxes in json via stdin and 
    a pdf file as a command line argument and outputs 
    the text in those bounding boxes.
    '''

    parser = argparse.ArgumentParser(description='Bulk extract areas of PDFs.')
    parser.add_argument(dest='inpath', help="Path to directory of pdfs to crop.")
    parser.add_argument("-s", "--scale", dest='scale', type=int, default='1', help="Scale. Enlarges images by this factor.")
   
    args = parser.parse_args()

    # Get bounding boxes from stdin
    bboxes = [json.loads(l) for l in sys.stdin]

    pdfs = glob.glob(os.path.join(args.inpath, '*.pdf'))
    for pdf in pdfs:
        for i, bbox in enumerate(bboxes):
            if 'field' not in bbox:
                bbox['field'] = str(i)

            outfile = '%s_%s.tif' % (pdf[:-4], bbox['field'])
            convertRegion(pdf, bbox, outfile, args.scale, offset_x=0, offset_y=0, dpi=72)

  
