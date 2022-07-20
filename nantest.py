import glob
test=glob.glob('/fs1/project/iip/zenalisa/data/fixed_aia/*/*/*/*/*.tiff')+glob.glob('/fs1/project/iip/zenalisa/data/fixed_aia/*/*/*/*.tiff')
#test=target_list
for t in test:
    img=np.array(Image.open(t))
    if np.isnan(np.sum(img)):
        print(t)
    