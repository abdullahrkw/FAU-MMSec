import copy
import os
import random

import numpy as np
from PIL import Image
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import ortho_group, pearsonr
from BitVector import BitVector


########## part 1
# Generate normally distributed random numbers as a sequence
# Take their sign() to map them to {-1, 1}
def generateWatermarkSequence(n):
    #	watermarkrange = random.randrange(1, n)
    sign = []
    for i in range(n):
        if (random.randrange(1, n) * 2 - n < 0):
            sign.append(-1)
        else:
            sign.append(1)
    return sign


def image_to_vector(image: np.ndarray) -> np.ndarray:
    """Args:  image: numpy array of shape (length, height, depth)  Returns: v: a vector of shape (length x height x depth, 1) """
    global length, height, depth
    length, height, depth = image.shape
    return image.reshape((length * height * depth, 1))


def embedd_watermark(in_img, out_img, n, alpha):
    # load the image
    image = Image.open(in_img)
    # convert image to numpy array
    image_array = np.asarray(image)
    imageVector = image_to_vector(image_array)
    imageVectorCopy = copy.deepcopy(imageVector)
    print(imageVectorCopy)
    imageVectorCopy = np.sort(imageVectorCopy)
    print(imageVectorCopy)
    watermarkSeq = generateWatermarkSequence(n)
    print(watermarkSeq)
    for i in range(0, n):
        imageVectorCopy[i][0] = (imageVectorCopy[i][0]) + (watermarkSeq[i] *
                                                           alpha)
        print(imageVectorCopy[i][0])
    #Convert back image vector to watermarked image
    imageVectorCopy = np.reshape(imageVectorCopy, (length, height, depth))
    #Converted from 1D to 3D
    watermarkedImage = Image.fromarray(imageVectorCopy, 'RGB')
    watermarkedImage.save(out_img)


def detect_watermark(img_path, n, alpha):
    # load the image
    watermarkedImage = Image.open(img_path)
    # convert image to numpy array
    watermarked_image_array = np.asarray(watermarkedImage)
    watermarked_image_vector = image_to_vector(watermarked_image_array)
    watermarked_image_vector_copy = copy.deepcopy(watermarked_image_vector)
    watermarked_image_vector_copy = np.sort(watermarked_image_vector_copy)
    watermarkSeq = generateWatermarkSequence(n)
    for i in range(0, n):
        val = ((watermarked_image_vector_copy[i][0]) * watermarkSeq[i]) / alpha
        if val < 0:
            val = 0
        else:
            val = 1
        print(val)


######### part 2
def pca_analysis(watermarked_images):
    train_files = list()
    for dir, _, filenames in os.walk(watermarked_images):
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
        print(i + 1, v)


if __name__ == "__main__":
    in_img = "ucid/ucid00019.tif"
    out_img = "watermarktest19.png"
    n = 3
    alpha = 2.5
    embedd_watermark(in_img, out_img, n, alpha)
    detect_watermark(out_img, n, alpha)
    pca_analysis("watermarked_images")
