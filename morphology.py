'''
Version 1.0
Naive erosion and dilation
---------
Scan every value covered by kernel to get the max/min.
---------

========================================
Version 1.1
Optimize the speed of _singleErosion() and _singleDilation()
---------
Multiply the kernel and the square of the image to get the max/min
---------
'''

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
        return -12450 # Error
    
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
        return -12450 #Error
    
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

'''
    Note:
        This is class for experiment
    
    Usage:
        kernel = np.ones((3,3))
        testInstance = test("woman.jpg",kernel)

        testInstance.erosion()
        testInstance.dilation()
'''
class test:
    '''
    Parameter:
        imagePath - the path to the source image
        kernel - the np.array of kernel
    '''
    def __init__(self, imagePath="woman.jpg", kernel=np.ones((3,3))):
        self.setImage(imagePath)
        self.kernel = kernel
    
    def setKernel(self, kernel):
        self.kernel = kernel

    def setImage(self, imagePath):
        self.imagePath = imagePath
        self.image = Image.open(imagePath)
        self.grayImage = self.image.convert('L')
        self.grayImage.show()
        self.grayArray = np.array(self.grayImage)

    def erosion(self):
        res = erosion(self.grayArray, self.kernel)
        self._show(res)
        return res

    def dilation(self):
        res = dilation(self.grayArray, self.kernel)
        self._show(res)
        return res

    def open(self):
        res = iopen(self.grayArray, self.kernel)
        self._show(res)
        return res

    def close(self):
        res = iclose(self.grayArray, self.kernel)
        self._show(res)
        return res
    
    def _show(self, image):
        img = Image.fromarray(image)
        img.show()
        

if __name__ == '__main__':
    #kernel = np.array([[0,1,0],[1,1,1],[0,1,0]])
    kernel = np.ones((3,3))
    testInstance = test("woman.jpg", kernel)

    testInstance.open()
    testInstance.close()
