# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 21:30:37 2020

@author: adwait
"""
import cv2
import numpy as np

# class ImageTransform:

def backgroundSubtract(frame, frame_bg, alpha, inv = False): #subtract background
    print(frame.shape)
    if alpha == 1: #direct subtraction if alpha is one
        frame_fg = cv2.subtract(255-frame,255-frame_bg)
        frame_fg_scaled = 255 - frame_fg
    else: #blend
##            alpha = 0.5
        frame_fg_scaled  = cv2.addWeighted(frame, 1 - alpha, 255 - frame_bg,
                                          alpha, 0.0)
    frame_subtracted = 255 - frame_fg_scaled if inv == True else frame_fg_scaled
    print("bgSubtract")
    return frame_subtracted

def applyBrightnessContrast(brightness, contrast, frame):
    
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow

        buf = cv2.addWeighted(frame, alpha_b, frame, 0, gamma_b)
    else:
        buf = frame.copy()

    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    
    print("brightness")
    return buf
    
#histogram correction
def histogramCorrection(frame, correction_type = 'None', clip_lim = 2, tile_size = 8):
    if correction_type == 'None':
        return frame
    elif correction_type == 'Global':
        frame_corrected = cv2.equalizeHist(frame)
    elif correction_type == 'Adaptive':
        clahe = cv2.createCLAHE(clipLimit=clip_lim, tileGridSize=(tile_size,
                                                                  tile_size))
        frame_corrected = clahe.apply(frame)

    print("histogram correct")
    return frame_corrected

##    def window_show(window_name, frame, posx, posy, resize_fraction):
##        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
##    #    sc = 0.5 #window resize scale factor
##        h, w = tuple(int(resize_fraction*x) for x in frame.shape[:2])    
##        cv2.moveWindow(window_name, posx, posy)
##        cv2.resizeWindow(window_name, w, h)
##        cv2.imshow(window_name, frame)
   

def imageFilter(ftype, param1, param2, frame): #image filtering
    # roi = self.roiBound
    # frame1 = frame[roi[1]:roi[3], roi[0]:roi[2]].copy() #filter inside roi
##        frame_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
##        del frame1
    if ftype == "Average Filter":
        frame_filtered = cv2.blur(frame,(param1,param1))
    elif ftype == "Gaussian Filter":
        frame_filtered = cv2.GaussianBlur(frame,(param1,param1),param2)
    elif ftype == "Median Filter":
        frame_filtered = cv2.medianBlur(frame,param1)
    elif ftype == "Bilateral Filter":
        frame_filtered = cv2.bilateralFilter(frame,0,param1,param2)
    elif ftype == "Morph Open":
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (param1,param2))
        frame_filtered = cv2.morphologyEx(frame, cv2.MORPH_OPEN, rect_kernel)
    elif ftype == "Morph Close":
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (param1,param2))
        frame_filtered = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, rect_kernel)
    else:
        frame_filtered = frame.copy()

##        frame_filtered2 = cv2.cvtColor(frame_filtered.astype(np.uint8),
##                                    cv2.COLOR_GRAY2BGR)
    # h, w, s  = frame.shape
    # l, r, t, d = roi[0], w - roi[2], roi[1], h - roi[3]
    # print(h, w, s, t, d, l, r)
    # #fill border with zero to equalize frame size
    # frame_filtered2 = cv2.copyMakeBorder(frame_filtered, t, d, l, r,
    #                                        cv2.BORDER_CONSTANT, 0)
    
    return frame_filtered
        

def dftFilter(r_lp, r_hp, frame_gray): #DFT Filter (Gaussian Bandpass)
    mask_gauss, img_back, img_back_gauss, img_back_scaled, \
        img_filtered, magnitude_spectrum, spectrum_masked = (None,)*7
    #DFT
    #if frame == None:
    #   frame = self.frame
    # print("dft init", self.roiBound)
    # roi = self.roiBound
    # print("roi")
    # frame1 = frame[roi[1]:roi[3], roi[0]:roi[2]].copy()
    print("dft")
    # frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # del frame
    print(frame_gray.shape)

    dft = cv2.dft(np.float32(frame_gray),flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)


    magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],
                                                 dft_shift[:,:,1]))
    rows, cols = frame_gray.shape
    # crow,ccol = int(rows/2) , int(cols/2)
    print("low pass")
    #Low Pass
    kernal = cv2.getGaussianKernel(max(rows, cols), r_lp)
    kernal2d = kernal * kernal.transpose()
    kernal2d = kernal2d / kernal2d.max()
##        kernal2d_inverse = 1 - kernal2d

    mask_lowpass = np.zeros((rows,cols),np.float64)
    if r_lp > 0:
        mask_lowpass = kernal2d[int((max(rows, cols)-rows)/2):
        int((max(rows, cols)+rows)/2),int((max(rows, cols)-cols)/2):
            int((max(rows, cols)+cols)/2)] #image sizes must be even integer
    else:
        mask_lowpass = np.zeros((rows,cols),np.float64)
    print("high pass")
    #High Pass
    kernal = cv2.getGaussianKernel(max(rows, cols), r_hp)
    kernal2d = kernal * kernal.transpose()
    kernal2d = kernal2d / kernal2d.max()
    kernal2d_inverse = 1 - kernal2d

    mask_highpass = np.ones((rows,cols),np.float64)
    if r_hp > 0:
        mask_highpass = kernal2d_inverse[int((max(rows, cols)-rows)/2):
        int((max(rows, cols)+rows)/2),int((max(rows, cols)-cols)/2):
            int((max(rows, cols)+cols)/2)] #image sizes must be even integer
    else:
        mask_highpass = np.ones((rows,cols),np.float64)
    print("band pass")
    #Band Pass
    if r_hp <= r_lp and r_lp > 0:
        mask_gauss = mask_lowpass * mask_highpass
        mask_gauss = mask_gauss/mask_gauss.max()
    else:
        mask_gauss = np.zeros((rows,cols),np.float64)

    del mask_lowpass, mask_highpass, kernal, kernal2d, kernal2d_inverse
    
    #Inverse DFT
    fshift = dft_shift*np.expand_dims(mask_gauss, axis = 2)
    f_ishift = np.fft.ifftshift(fshift)
    del fshift

    img_back = cv2.idft(f_ishift)
    img_back_gauss = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])
    print("img_back_gauss", img_back_gauss.shape)
    spectrum_masked = magnitude_spectrum * mask_gauss
##        img_back_scaled = None
    img_back_scaled = 255*img_back_gauss/img_back_gauss.max()
    img_filtered = img_back_scaled.astype(np.uint8)
    # img_filtered = cv2.cvtColor(img_back_scaled.astype(np.uint8),
    #                             cv2.COLOR_GRAY2BGR)
    print("dft end")
    # h, w, s  = frame.shape
    # l, r, t, d = roi[0], w - roi[2], roi[1], h - roi[3]
    # print(h, w, s, t, d, l, r)
    # #fill border with zero to equalize frame size
    # img_filtered1 = cv2.copyMakeBorder(img_filtered, t, d, l, r,
    #                                        cv2.BORDER_CONSTANT, 0)

    # print(img_filtered.shape, img_filtered1.shape, frame.shape)
    return img_filtered, spectrum_masked
            