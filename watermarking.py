import copy
import os

import numpy as np
from PIL import Image
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import ortho_group, pearsonr
from BitVector import BitVector

########## part 1
msg=BitVector(intVal = 1, size = 3)
k=3
x = ortho_group.rvs(k)
im = Image.open(r"ucid/ucid00007.tif")
image = np.array(im)
img=copy.deepcopy(image)
message=7
msg=BitVector(intVal = message, size = 3)
m=[int(x) for x in msg]
print(m)
sign=[1 if i==1 else -1 for i in m]
alfa=1

print(sign)
print(img.shape)
print(x)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        k=0
        for c in range(img.shape[2]):
            img[i, j]=img[i, j]+(alfa*sign[k]*x[k])
            k+=1
new_im = Image.fromarray(img)
test = image - img
print(np.linalg.norm(np.array(test).flatten(), 1))
new_im.save("watermarked_img07.png")

im_o = image
image_water = Image.open("watermarked_img07.png")
im_w = np.array(image_water)
im11= np.where(img==im_w)
message=(im_o-im_w)

message_im = Image.fromarray(message)
message_im.save("watermarked_MESSAGE.png")
# corr, _ = pearsonr(im_o, im_w)
######### part 2

train_files = list()
for dir, _, filenames in os.walk("watermarked_images"):
    for file_ in filenames:
        train_files.append(os.path.join(dir, file_))

train_files_flattened = list()
for img in train_files:
    train_files_flattened.append(np.array(Image.open(img)).flatten())

tensor = np.array(train_files_flattened)
# high pass filter

tensor = StandardScaler().fit_transform(tensor)
print(tensor.shape)


pca = PCA()
pr_components = pca.fit(tensor)
print("principle components")
for i, v in enumerate(pr_components.explained_variance_ratio_):
    print(i+1, v)
