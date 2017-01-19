from PIL import Image, ImageChops, ImageDraw
from itertools import izip
import math
import operator

class ImageComparator():

    def __init__(self, image1_path, image2_path):
        self.image1 = Image.open(image1_path)
        self.image2 = Image.open(image2_path)
        if self.image1.size != self.image2.size and self.image1.mode != self.image2.mode:
            raise 

    def pixel_compare(self):
        data = izip(self.image1.getdata(),self.image2.getdata())
        if len(self.image1.getbands()) == 1:
            # gray scale
            dif = sum(abs(p1-p2) for p1,p2 in data)
            size = self.image1.size[0]*self.image1.size[1]
        else:
            dif = sum(abs(c1-c2) for p1,p2 in data for c1, c2 in zip(p1,p2))
            size = self.image1.size[0]*self.image1.size[1]*3

        return (dif/255.0*100)/size

    def get_image_diff(self, filename):
        # Mark diff in bounding box and save image
        diff = ImageChops.difference(self.image1, self.image2).getbbox()
        draw = ImageDraw.Draw(self.image2)
        draw.rectangle(diff, outline = (0,255,0))
        self.image2.save(filename)

    def histogram_compare(self):
        # Compare two images and return RMS
        h1 = self.image1.histogram()
        h2 = self.image2.histogram()
        rms = math.sqrt(reduce(operator.add, map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
        return rms
