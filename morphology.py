import numpy as np
from PIL import Image

'''
    Function: 
        _imageCategory(nparray)

    Parameter: 
        nparray - np.array of image

    Return Value:
        0 - Gray
        1 - RGB
        -1 - Not a image
    
    Usage:
        if _imageCategory(image) == 0:
            print("Grey")
'''
def _imageCategory(nparray):
    if (nparray.ndim == 2):
        return 0
    elif (nparray.ndim == 3):
        return 1
    return -1

'''
    Function: 
        _padding(nparray)

    Parameter: 
        nparray - np.array of image

    Return Value:
        Source image with padding of 0 of width 1 around it
    
    Usage:
        padded = _padding(sourceImage)
'''
def _padding(nparray):
    return np.pad(nparray, ((1, 1), (1, 1)), 'constant')

'''
    Function: 
        _singleErosion(image, r, c, kernel)

    Parameter: 
        image - np.array of source image
        r - a specific row of source image
        c - a specific column of source image
        kernel - kernel

    Return Value:
        The erosion result of (r, c) in source image
    
    Usage:
        target[r][c] = _singleErosion(source, r, c, kernel)
'''
def _singleErosion(image, r, c ,kernel):
    maximum = 0
    radiusX, radiusY = kernel.shape
    imageX, imageY = image.shape
    radiusX = int(radiusX/2)
    radiusY = int(radiusY/2)
    startX = r - radiusX
    endX = r + radiusX
    startY = c - radiusY
    endY = c + radiusY
    
    for i in range(startX, endX+1):
        if (i < 0 or i >= imageX):
            continue
        for j in range(startY, endY+1):
            if (j < 0 or j >= imageY):
                continue
            if (kernel[i-startX][j-startY] == 0):
                continue
            value = image[i][j]
            if value > maximum:
                maximum = value
    return maximum

'''
    Function: 
        erosion(image, kernel)

    Parameter: 
        image - np.array of source image
        kernel - kernel

    Return Value:
        The erosion result of source image
    
    Usage:
        erosion = erosion(image, kernel)
'''
def erosion(image, kernel):
    category = _imageCategory(image)
    if (category != 0):
        return -1
    if (kernel.ndim != 2):
        return -1

    '''
    Maybe there should be more validation
    '''  

    source = _padding(image)
    target = np.zeros((source.shape))
    for r, row in enumerate(source):
        for c, column in enumerate(row):
            target[r][c] = _singleErosion(source, r, c, kernel)
    return target

'''
    Function: 
        _singleDilation(image, r, c, kernel)

    Parameter: 
        image - np.array of source image
        r - a specific row of source image
        c - a specific column of source image
        kernel - kernel

    Return Value:
        The dilation result of (r, c) in source image
    
    Usage:
        target[r][c] = _singleDilation(source, r, c, kernel)
'''
def _singleDilation(image, r, c ,kernel):
    minimum = 255
    radiusX, radiusY = kernel.shape
    imageX, imageY = image.shape
    radiusX = int(radiusX/2)
    radiusY = int(radiusY/2)
    startX = r - radiusX
    endX = r + radiusX
    startY = c - radiusY
    endY = c + radiusY
    
    for i in range(startX, endX+1):
        if (i < 0 or i >= imageX):
            continue
        for j in range(startY, endY+1):
            if (j < 0 or j >= imageY):
                continue
            if (kernel[i-startX][j-startY] == 0):
                continue
            value = image[i][j]
            if value < minimum:
                minimum = value
    return minimum

'''
    Function: 
        dilation(image, kernel)

    Parameter: 
        image - np.array of source image
        kernel - kernel

    Return Value:
        The dilation result of source image
    
    Usage:
        dilation = dilation(image, kernel)
'''
def dilation(image, kernel):
    category = _imageCategory(image)
    if (category != 0):
        return -1
    if (kernel.ndim != 2):
        return -1

    '''
    Maybe there should be more validation
    '''  

    source = _padding(image)
    target = np.zeros((source.shape))
    for r, row in enumerate(source):
        for c, column in enumerate(row):
            target[r][c] = _singleDilation(source, r, c, kernel)
    return target

if __name__ == '__main__':
    sourceImage = Image.open("969fb5f8aecaf913a679139ef3de3438.jpg").convert('L')
    sourceImage.show()
    src = np.array(sourceImage)

    #kernel = np.array([[0,1,0],[1,1,1],[0,1,0]])
    kernel = np.ones((21,21))

    #tar = erosion(src, kernel)
    tar = dilation(src,kernel)
    target = Image.fromarray(tar)
    target.show()