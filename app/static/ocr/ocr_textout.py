try:  
    from PIL import Image
except ImportError:  
    import Image
import pytesseract
import glob
import cv2
import numpy as np

path = 'app/static/uploads/'
# path = '../uploads/'
def ocr_core(filename):  
    """
    This function will handle the core OCR processing of images.
    """
    img = cv2.imread(filename)
    # Convert to gray    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
    # Apply dilation and erosion to remove some noise    
    kernel = np.ones((1, 1), np.uint8)    
    img = cv2.dilate(img, kernel, iterations=1)    
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite('temp1.jpg', img)    
    # Apply threshold to get image with only black and white    
    img = cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 20)  #31,20 giving superb result for pan cards
    cv2.imwrite('temp.jpg', img)    
    """
    PREPROCESSING ENDS HERE
    """
    text = pytesseract.image_to_string(Image.open('temp.jpg'))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

def initiate(pat):
    rois = glob.glob(path+'roi_*_'+pat+'.jpg')
    j=0
    corp = ''
    print(rois)
    # print(rois,pat)
    for i in rois:
        add='ROI'+str(j)+'\n'
        text = ocr_core(i)
        corp = corp+add+text+'\n'
        j =j+1
    # print('final text leaving ::'+corp)
    for ch in ['}','{','!','(',')']:
        corp = corp.replace(ch,'I')
    return corp    

