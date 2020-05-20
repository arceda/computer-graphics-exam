#May-18-2020 06:42:31 PM
 
import cv2
import numpy as np
import matplotlib as plt

img = cv2.imread("question_2.jpg")

#########  write your code here ##################


for i in range(10):
    for j in range(10):
        img[i][j] = 10

print("image opened, size:", img.shape)

#normal contrast stretching #########################################
a = 0
b = 255
c = img.min()
d = img.max()
print("c:", c)
print("d:", d)

def contrast_stretching(img, a, b, c, d):
    img = img.astype(int) #this is very import because the images are normally unsigned
    
    factor = (b-a)/(d-c)
    new_img = ((img - c)*factor) + a

    print(new_img.min())
    print(new_img.max())

    for i, row in enumerate(new_img):
        for j, x in enumerate(row):
            if x < 0:
                new_img[i][j] = 0
            if x > 255:
                new_img[i][j] = 255

    
    return new_img


new_img = contrast_stretching(img, a, b, c, d)




img_out = new_img

######## the result have to be set in img_out ####
######## not modify from here ####################

cv2.imwrite("question_2_sol.jpg", img_out)
    