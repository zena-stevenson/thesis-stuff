#code to make NL masks for a signed magnetogram image.
#last updated 5/13/21 using notebook NLtest to uh. test the NL's. surprise surprise.
#but making that note so that if/when I fix/update NLtest later, I maybe hopefully remember to update this too


from scipy.signal import *
import numpy as np
import skimage.measure as measure
from PIL import Image

def gradient(image):
    sobelx = [[-1,0,1],[-2,0,2],[-1,0,1]]
    sobely = [[1,2,1],[0,0,0],[-1,-2,-1]]
    
    gx = convolve2d(image,sobelx, boundary='symm')
    gy = convolve2d(image,sobely, boundary='symm')
    
    M = (gx**2 + gy**2)**(1./2)
    
    return M

def extractNL(image):
    avg10 = (1. / 100)*np.ones([10,10])
    avgim = convolve2d(image,avg10,mode='same', boundary='symm')
    out = measure.find_contours(avgim,level = 128)
    #out = measure.find_contours(image,level = 128)
    return out

def NLmaskgen(contours,image):
    width = image.shape[0]
    height = image.shape[1]
    mask = np.zeros([height,width])
    for n,contour in enumerate(contours):
        #print n,contour
        for i in range(len(contour)):
            y = int(round(contour[i,1]))
            #print i,x
            x = int(round(contour[i,0]))
            mask[x,y] = 1.
    return mask
    
    
def get_mask(image_path):

    mg=Image.open(image_path)
    mg=np.array(mg)
    
    grad=gradient(mg)
    contours=extractNL(mg)
    nl_mask=NLmaskgen(contours,mg)*grad[1:-1,1:-1]
    
    #not sure this next line is entirely correct, but it'll do for now to make this a real mask
    nl_mask[nl_mask!=0.]=1.
    
    return nl_mask








