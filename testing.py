import cv2
import pytesseract
cropping = False
x_start, y_start, x_end, y_end = 0, 0, 0, 0
image = cv2.imread('Capture.PNG')
oriImage = image.copy()
def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping
    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False # cropping is finished
        refPoint = [(x_start, y_start), (x_end, y_end)]
        print(refPoint)
        print(refPoint[0][1])
        if len(refPoint) == 2: #when two points were found
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
            img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            custom_config = r'-l hrv --psm 6'
            rez = pytesseract.image_to_string(img, lang="hrv", config=custom_config)
            print(rez)

            #<---------------nije potrebno dodatno crtati kvadrate kada u while to radimo----------->
            #boxes = pytesseract.image_to_data(roi)
            #for x, b in enumerate(boxes.splitlines()):
                #if x != 0:
                    #b = b.split()
                    #if len(b) == 12:
                        #x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                        #cv2.rectangle(roi, (x, y), (w + x, h + y), (0, 0, 255), 1)
                        # cv2.putText(img, b[11], (x, y + 65), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            #cv2.imshow("Odabrani tekst za čitanje", roi)

cv2.namedWindow("Slika")
cv2.setMouseCallback("Slika", mouse_crop)
while True:
    i = image.copy()
    if cv2.waitKey(10) == 27:
        break
    elif not cropping:
        cv2.imshow("Slika", image)
    elif cropping:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        cv2.imshow("Slika", i)

# close all open windows
cv2.destroyAllWindows()