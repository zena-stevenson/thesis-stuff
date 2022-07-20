
# coding: utf-8

# 545 project code adapted into a module of methods for displaying results of testing a model- displays target, signal, prediction, and difference images, calculates MSE's and SSIM's, etc

# In[1]:


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image

def unnorm(og_img, normed_img):
    
    un= normed_img*np.std(og_img)
    un=un+np.mean(og_img)

    return(un)


def display(signal, target, prediction, target_csv=False, plotdiff=False, signed=False, norm=False):
    '''Inputs: String names of signal, target, and prediction images, and csv of all target images
    Outputs: Technically no returns but displays signal, target, prediction, and target-prediction images.'''
    if norm:
        target_list=open(target_csv).readlines()
        imgnum=int(target.split('/')[-2])
        #print(imgnum)
        target_og=target_list[imgnum+1].split(',')[1].strip().replace('/fs1/project/iip/', '/home/')
        signal_og = target_list[imgnum+1].split(',')[0].strip().replace('/fs1/project/iip/', '/home/')
        #plt.imshow(np.array(Image.open(target_og)), cmap='gray')
        target_og=np.array(Image.open(target_og))
        signal_og = np.array(Image.open(signal_og))
    
    plt.figure(figsize=(10, 10))
    
    
    s = Image.open(signal)
    s = np.array(s)
    t = Image.open(target)
    t = np.array(t)
   # print(np.amin(t), np.amax(t))
    p = Image.open(prediction)
    p = np.array(p)
    
    if norm:
        s=unnorm(signal_og, s)
        t=unnorm(target_og, t)
        p=unnorm(target_og, p)

    #print(np.amin(target_og), np.amax(target_og))
    #print(np.amin(t), np.amax(t))
    
    if plotdiff:
        plt.subplot(2, 2, 1)
        plt.imshow(s, cmap='gray')
        plt.title('signal')
        plt.axis('off')

        plt.subplot(2, 2, 2)
        plt.imshow(t, cmap='gray')
        plt.title('target')
        plt.axis('off')

        plt.subplot(2, 2, 4)
        plt.imshow(p, cmap='gray')
        plt.title('prediction')
        plt.axis('off')
        plt.subplot(2, 2, 3)
        diff = (t - p)
        plt.imshow(diff, cmap='gray')
        plt.title('difference')
        plt.axis('off')
        
    else:
        plt.subplot(131)
        plt.imshow(s, cmap='gray')
        plt.title('Signal')
        plt.axis('off')
        
        if norm:
            plt.subplot(132)
            plt.imshow(t, cmap='gray', vmin=0, vmax=255)
            plt.title('Target')
            plt.axis('off')

            plt.subplot(133)
            plt.imshow(p, cmap='gray', vmin=0, vmax=255)
            plt.title('Prediction')
            plt.axis('off')
            plt.axis('off')
        else:
            plt.subplot(132)
            plt.imshow(t, cmap='gray')
            plt.title('Target')
            plt.axis('off')

            plt.subplot(133)
            plt.imshow(p, cmap='gray')
            plt.title('Prediction')
            plt.axis('off')
            plt.axis('off')
        
def ssim_mse(target_list1, prediction_list1, og_target_csv1, target_list2, prediction_list2, og_target_csv2, target_list3=None, prediction_list3=None, og_target_csv3=None, plot=True, ssim_norm='min-max', simname=''):
    '''Inputs: glob-compatible target_path and prediction_path 1 and 2, optional parameters plot=True and ssim_norm='min-max'
    Outputs: lists of ssim's and mse's respectively for each image pair in target_ and prediction_ path.
    '''
    
    from skimage.metrics import structural_similarity as compare_ssim
    from skimage.metrics import normalized_root_mse as compare_nrmse
    import glob
    

    ssim1 = []
    mse1 = []
    ssim2 = []
    mse2 = []
    
    og_target_list1=open(og_target_csv1).readlines()
    og_target_list2=open(og_target_csv2).readlines()
    
    if og_target_csv3:
        og_target_list3=open(og_target_csv3).readlines()
    
    
    
    for t in target_list1:
        p = prediction_list1[target_list1.index(t)]
        t_og=og_target_list1[target_list1.index(t)+1].split(',')[1].strip().replace('/fs1/project/iip', '/home')
        t_og=np.array(Image.open(t_og))
        t = np.array(Image.open(t))
        p = np.array(Image.open(p))
        
        
        t=unnorm(t_og, t)
        p=unnorm(t_og, p)
        
        ssim1.append(compare_ssim(t, p)) 
        mse1.append(compare_nrmse(t, p, normalization=ssim_norm))
    
    for t in target_list2:
        p = prediction_list2[target_list2.index(t)]
        t_og=og_target_list2[target_list2.index(t)+1].split(',')[1].strip().replace('/fs1/project/iip', '/home')
        t_og=np.array(Image.open(t_og))
        t = np.array(Image.open(t))
        p = np.array(Image.open(p))
                
        t=unnorm(t_og, t)
        p=unnorm(t_og, p)
        
        ssim2.append(compare_ssim(t, p)) 
        mse2.append(compare_nrmse(t, p, normalization=ssim_norm))

    
    if target_list3!=None:
        ssim3=[]
        mse3=[]
        for t in target_list3:
            p = prediction_list3[target_list3.index(t)]
            t_og=og_target_list3[target_list3.index(t)+1].split(',')[1].strip().replace('/fs1/project/iip', '/home')
            t_og=np.array(Image.open(t_og))
            t = np.array(Image.open(t))
            p = np.array(Image.open(p))
        
        
            t=unnorm(t_og, t)
            p=unnorm(t_og, p)

            ssim3.append(compare_ssim(t, p)) 
            mse3.append(compare_nrmse(t, p, normalization=ssim_norm))
        
        
    if plot==True:
        #idx = (np.abs(ssim - np.mean(ssim))).argmin()
        #ssim closest to mean
        #mean_ssim = ssim[idx]
        
        plt.figure(figsize = (10, 8))
        
        plt.scatter(range(len(ssim1)), ssim1, label='SameAR', s=40)
        plt.hlines(np.mean(ssim1), 0, len(ssim1), 'r', label='average (SameAR) = '+str(round(np.mean(ssim1), 4)))
        
        plt.scatter(range(len(ssim2)), ssim2, label='DiffAR', color='g', marker='x')
        plt.hlines(np.mean(ssim2), 0, len(ssim2), 'r', linestyles='dashed', label='average (DiffAR) = '+str(round(np.mean(ssim2), 4)))
        
        if target_list3!=None:
            plt.scatter(range(len(ssim3)), ssim3, label='SouthAR', color='c', marker='v')
            plt.hlines(np.mean(ssim3), 0, len(ssim3), 'r', linestyles='dotted', label='average (SouthAR) = '+str(round(np.mean(ssim3), 4)))
        
        #plt.ylim((0, .9))
        plt.title('SSIM: '+simname, fontsize=20)
        plt.ylabel('SSIM', fontsize=15)
        plt.xlabel('Image', fontsize=15)
        plt.legend(fontsize=15)
        #plt.savefig('fig7')
        plt.show()
           
        plt.figure(figsize = (10, 8))
        
        plt.scatter(range(len(mse1)), mse1, label='SameAR')
        plt.hlines(np.mean(mse1), 0, len(mse1), 'r', label='average (SameAR)= '+str(round(np.mean(mse1), 4)))
        
        plt.scatter(range(len(mse2)), mse2, label='DiffAR', color='g', marker='x')
        plt.hlines(np.mean(mse2), 0, len(mse2), 'r', linestyles='dashed', label='average (DiffAR)= '+str(round(np.mean(mse2), 4)))
        if target_list3!=None:
            plt.scatter(range(len(mse3)), mse3, label='SouthAR', color='c', marker='v')
            plt.hlines(np.mean(mse3), 0, len(mse3), 'r', linestyles='dotted', label='average (SouthAR) = '+str(round(np.mean(mse3), 4)))
            
        plt.ylim((0, .1))
        plt.ylabel('Normalized RMSE', fontsize=15)
        plt.xlabel('Image', fontsize=15)
        plt.legend(fontsize=15)
        plt.title('NRMSE: '+simname, fontsize=20)
        #plt.savefig('fig6.png')
        plt.show()
        #plt.savefig('fig6.png')        
        
    
    return [ssim1, mse1, ssim2, mse2]


def best(ssim, mse, signal_list, target_list, prediction_list):
    
    print('best MSE = ' +str(min(mse)))
    print('worst MSE = ' +str(max(mse)))
    print('best SSIM = ' +str(max(ssim)))
    print('worst SSIM = ' +str(min(ssim)))
    
          
    #"best" images
    best_ssim = ssim.index(max(ssim))
    best_mse =  mse.index(min(mse))
    
    #"worst" images
    worst_mse = mse.index(max(mse))
    worst_ssim= ssim.index(min(ssim))
    
    plt.figure(figsize=(15, 15))
    t = np.array(Image.open(target_list[best_mse]))
    p = np.array(Image.open(prediction_list[best_mse]))
    s = np.array(Image.open(signal_list[best_mse]))
    
    
    plt.subplot(1, 4, 1)
    plt.title('Signal')
    plt.ylabel('Best MSE')
    plt.imshow(s, cmap='gray')
    plt.subplot(1, 4, 2)
    plt.title('Target')
    plt.imshow(t, cmap='gray')
    plt.subplot(1, 4, 3)
    plt.title('Prediction')
    plt.imshow(p, cmap='gray', vmin=t.min(), vmax = t.max())
    plt.subplot(1, 4, 4)
    plt.title('Difference (target - prediction)')
    diff = np.subtract(t, p)
    plt.imshow(diff, cmap='gray')
    #https://rebrand.ly/feb1u9 #i have no idea what this is? tf?
    #plt.savefig('fig81.png')
    
    
    plt.figure(figsize=(15, 15))
    t = np.array(Image.open(target_list[worst_mse]))
    p = np.array(Image.open(prediction_list[worst_mse]))
    s = np.array(Image.open(signal_list[worst_mse]))
    plt.subplot(1, 4, 1)
    plt.imshow(s, cmap='gray')
    plt.ylabel('Worst MSE')
    plt.subplot(1, 4, 2)
    plt.imshow(t, cmap='gray')
    plt.subplot(1, 4, 3)
    plt.imshow(p, cmap='gray')
    plt.subplot(1, 4, 4)
    diff = np.subtract(t, p)
    plt.imshow(diff, cmap='gray')
    #plt.savefig('fig82.png')
    
    plt.figure(figsize=(15, 15))
    t = np.array(Image.open(target_list[best_ssim]))
    p = np.array(Image.open(prediction_list[best_ssim]))
    s = np.array(Image.open(signal_list[best_ssim]))
    plt.subplot(1, 4, 1)
    plt.imshow(s, cmap='gray')
    plt.ylabel('Best SSIM')
    plt.subplot(1, 4, 2)
    plt.imshow(t, cmap='gray')
    plt.subplot(1, 4, 3)
    plt.imshow(p, cmap='gray')
    plt.subplot(1, 4, 4)
    diff = np.subtract(t, p)
    plt.imshow(diff, cmap='gray')
    #plt.savefig('fig83.png')
    
    plt.figure(figsize=(15, 15))
    t = np.array(Image.open(target_list[worst_ssim]))
    p = np.array(Image.open(prediction_list[worst_ssim]))
    s = np.array(Image.open(signal_list[worst_ssim]))
    plt.subplot(1, 4, 1)
    plt.imshow(s, cmap='gray')
    plt.ylabel('Worst SSIM')
    plt.subplot(1, 4, 2)
    plt.imshow(t, cmap='gray')
    plt.subplot(1, 4, 3)
    plt.imshow(p, cmap='gray')
    plt.subplot(1, 4, 4)
    diff = np.subtract(t, p)
    plt.imshow(diff, cmap='gray')
    #plt.savefig('fig84.png')

#t = np.array(Image.open(target_list[best_ssim]))
#p = np.array(Image.open(prediction_list[best_ssim]))
#s = np.array(Image.open(signal_list[best_ssim]))
#plt.figure(figsize = (15, 15))
#plt.subplot(1, 3, 1)
#plt.imshow(s, cmap='gray')
#plt.subplot(1, 3, 2)
#plt.imshow(t, cmap='gray')
#plt.subplot(1, 3, 3)
#plt.imshow(p, cmap='gray')
#plt.savefig('fig4.png')
##
#
## In[114]:
#
#
##this isn't like useful or anything but it turned out very pretty so I'm saving it
#intensity = np.divide(p, t)
#plt.figure(figsize=(15,15))
#plt.plot(intensity)
#plt.show()
#
#
## In[115]:
#
#
##this isn't like useful or anything but it's very pretty
#intensity = np.divide(p, t)
#intensity.sort()
#plt.figure(figsize=(15,15))
#plt.plot(intensity)
#plt.show()
#
#
## In[131]:
#
#
#import skimage.exposure as e
#intensity = np.divide(p, t)
#y, x =e.histogram(intensity, nbins = 512)
#
#plt.figure(figsize=(10, 10))
#plt.plot(x, y)
#plt.xlim((-2, 2))
#
#
##plt.figure(figsize=(10,10))
##onerow = intensity[0, :]
##onerow.sort()
##plt.plot(onerow)
##plt.show()
#
#
## In[210]:
#
#
#import skimage.exposure as e
#
#plt.figure(figsize=(15,10))
#
#t = np.array(Image.open(target_list[best_ssim]))
#p = np.array(Image.open(prediction_list[best_ssim]))
#
#p_flat = np.ndarray.flatten(p)
#t_flat = np.ndarray.flatten(t)
#order=np.argsort(t_flat)
#t_flat.sort()
#
#plt.subplot(121)
#plt.scatter(t_flat, p_flat[order])
#plt.plot(range(t_flat.max()), range(t_flat.max()), 'r')
#plt.title('Highest SSIM')
#plt.xlabel('Target pixel value')
#plt.ylabel('Predicted pixel value')
#
#t = np.array(Image.open(target_list[worst_ssim]))
#p = np.array(Image.open(prediction_list[worst_ssim]))
#p_flat = np.ndarray.flatten(p)
#t_flat = np.ndarray.flatten(t)
#
#order=np.argsort(t_flat)
#t_flat.sort()
##plt.figure(figsize=(10,10))
#plt.subplot(122)
#plt.scatter(t_flat, p_flat[order])
#plt.plot(range(t_flat.max()), range(t_flat.max()), 'r')
#plt.title('Lowest SSIM')
#plt.xlabel('Target pixel value')
#plt.ylabel('Predicted pixel value')
#
#plt.suptitle('Fig. 9')
#plt.savefig('fig9.png')
#plt.show()
#
#
## In[ ]:
#
#
#t = np.array(Image.open(target_list[best_mse]))
#p = np.array(Image.open(prediction_list[best_mse]))
#p_flat = np.ndarray.flatten(p)
#t_flat = np.ndarray.flatten(t)
#
#order=np.argsort(t_flat)
#t_flat.sort()
#
#plt.subplot(223)
#plt.scatter(t_flat, p_flat[order])
#plt.plot(range(t_flat.max()), range(t_flat.max()), 'r')
#
#t = np.array(Image.open(target_list[worst_mse]))
#p = np.array(Image.open(prediction_list[worst_mse]))
#p_flat = np.ndarray.flatten(p)
#t_flat = np.ndarray.flatten(t)
#
#order=np.argsort(t_flat)
#t_flat.sort()
#
#plt.subplot(224)
#plt.scatter(t_flat, p_flat[order])
#plt.plot(range(t_flat.max()), range(t_flat.max()), 'r')
#plt.show()
#
