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
        Source image with padding around it.
        The values of padding equal to the those of edge.
        The size of padding is (row, col)
    
    Usage:
        padded = _padding(sourceImage)
'''
def _padding(nparray, row, col):
    return np.pad(nparray, ((row, row), (col, col)), 'edge')

'''
    Function: 
        _singleErosion(image, kernel)

    Parameter: 
        image - the square of source image whose size should equal to that of kernel
        kernel - kernel

    Return Value:
        The single point erosion result of input image
    
    Usage:
        target[r][c] = _singleErosion(square, kernel)
'''
def _singleErosion(image, kernel):
    if (image.shape != kernel.shape):
        return -12450
    
    return np.max(image * kernel)


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
    kernelX, kernelY = kernel.shape
    padded = _padding(image, kernelX, kernelY)

    target = np.zeros((image.shape))
    for r, row in enumerate(image):
        for c, column in enumerate(row):
            square = padded[r : r + kernelX, c : c + kernelY]
            target[r][c] = _singleErosion(square, kernel)
    return target

'''
    Function: 
        _singleDilation(image, kernel)

    Parameter: 
        image - the square of source image whose size should equal to that of kernel
        kernel - kernel

    Return Value:
        The single point dilation result of input image
    
    Usage:
        target[r][c] = _singleDilation(square, kernel)
'''
def _singleDilation(image, kernel):
    if (image.shape != kernel.shape):
        return -12450
    
    return np.min(image * kernel)

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
    kernelX, kernelY = kernel.shape
    padded = _padding(image, kernelX, kernelY)

    target = np.zeros((image.shape))
    for r, row in enumerate(image):
        for c, column in enumerate(row):
            square = padded[r : r + kernelX, c : c + kernelY]
            target[r][c] = _singleDilation(square, kernel)
    return target

def iopen(image, kernel):
    temp = erosion(image, kernel)
    temp = dilation(temp, kernel)
    return temp

def iclose(image,kernel):
    temp = dilation(image, kernel)
    temp = erosion(image, kernel)
    return temp

if __name__ == '__main__':
    sourceImage = Image.open("woman.jpg").convert('L')
    sourceImage.show()
    src = np.array(sourceImage)

    #kernel = np.array([[0,1,0],[1,1,1],[0,1,0]])
    kernel = np.ones((3,3))

    '''
    ero = erosion(src, kernel)
    erosion = Image.fromarray(ero)
    erosion.show()

    dil = dilation(ero,kernel)
    dilation = Image.fromarray(dil)
    dilation.show()
    '''

    temp = iopen(src, kernel)
    temp = Image.fromarray(temp)
    temp.show()

    temp = iclose(src, kernel)
    temp = Image.fromarray(temp)
    temp.show()
