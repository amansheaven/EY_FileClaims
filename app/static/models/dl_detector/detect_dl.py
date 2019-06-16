import cv2 
  
path = 'app/static/uploads/'
roi_count = 0

def par_save(image,c,c_b,tag):
    global roi_count
    res_w, res_h = image.shape[:2]
    area = res_h*res_w
    area_b =  ((c_b[0]-c[0])*(c_b[1]-c[1]))
#     print('AREA : ' , area, 'AREA_B : ',area_b)
    per = (area_b/area)*100
    if(per>=5):
        roi = image[c[1]:c_b[1], c[0]:c_b[0]]
        name = path+'roi_'+str(roi_count)+'_'+tag+'.jpg'
        print(name)
        cv2.imwrite(name,roi)
        roi_count = roi_count+1
    return True

def initiate(name):
    global path  
    print(name)
    path_i = path +'unprocessed/'+name+'.jpg'
    print(path_i)
    
    image = cv2.imread(path_i)

    blur = cv2.GaussianBlur(image,(5,5),0)
    gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY) # grayscale 

    _,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) #threshold 
    cv2.imwrite("thresh.jpg", thresh)  
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3)) 
    dilated = cv2.dilate(thresh,kernel,iterations = 15) # dilate
    cv2.imwrite("dilate.jpg", dilated)  
    contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours 
    # for each contour found, draw a rectangle around it on original image 

    for contour in contours:   
        [x,y,w,h] = cv2.boundingRect(contour)   

    #     print(w,h)

        if h<20 or w<20:
            print('skip')
            continue

        if par_save(image, (x,y) , (x+w,y+h), name):
            print('Accepted')
        else :
            print('Rejected')

    for contour in contours: 
        [x,y,w,h] = cv2.boundingRect(contour)
        if h<20 or w<20:
            print('skip')
            continue
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)

    cv2.imwrite(path+"contoured_"+name+".jpg", image)
    print('Saving contoured image at '+path+"contoured_"+name+".jpg")
    return True
