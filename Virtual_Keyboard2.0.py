import numpy as np
import cv2
import wx
from playsound import playsound

xs={}
prev="He"

# Blue
lower_b = np.array([100,120,100])
upper_b = np.array([150,255,255])

# Keyboard Settings
keyboard = np.zeros((450,750,3),np.uint8)

keys_set3={0:"Q",1:"W",2:"E",3:"R",4:"T",
             5:"Y",6:"U",7:"I",8:"O",9:"P",
             10:"A",11:"S",12:"D",13:"F",14:"G",
             15:"H",16:"J",17:"K",18:"L",19:"' '",
             20:"Z",21:"X",22:"C",23:"V",24:" ",
             25:"B",26:"N",27:"M",28:",",29:"cl"
        }

app =wx.App(False)
(sx,sy) =wx.DisplaySize()

kernelOpen = np.ones((4,4))
kernelClose = np.ones((18,18))

def letter(letter_index,text):

    # Keys
    x=(letter_index%10)*75
    y=int(letter_index/10)*75

    xs[x,y]=text

    height,width=75,75
    th= 3 #thickness
    cv2.rectangle(img, (x+th,y+th), (x+width-th,y+height-th),(100,255,255),th)

    # Text-settings
    font_scale=4
    font_th =3
    font_letter =  cv2.FONT_HERSHEY_PLAIN
    text_size =cv2.getTextSize(text,font_letter,font_scale,font_th)[0]
    width_text, height_text = text_size[0],text_size[1]

    text_x= int((width-width_text)/2) +x
    text_y = int((height+height_text)/2) +y

    cv2.putText(img,text,(text_x,text_y),font_letter,font_scale,(100,255,255),font_th)

cam = cv2.VideoCapture(0)
frame_count=0
pos=0
while True:
    _,img = cam.read()
    img= cv2.resize(img,(800,600))
    img = cv2.flip( img, 1)

    # Letters
    for i in range(30):
       letter(i,keys_set3[i])

    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHsv,lower_b,upper_b)

    #   Morphology
    maskOpen =cv2.morphologyEx(mask, cv2.MORPH_OPEN,kernelOpen)
    maskClose =cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE,kernelClose)

    conts,h = cv2.findContours(maskClose.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    if(len(conts)==1):
        cv2.drawContours(img,conts,-1,(255,0,0),3)
        x1,y1,w1,h1 = cv2.boundingRect(conts[0])

        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        height,width=75,75
        th= 3 #thickness

        if int(x1/width) <=9 and int(y1/height) <=2:
            curr=keys_set3[int(x1/width)+int(y1/height)*10]
            cv2.rectangle(img, (int(x1/width)*75+th,int(y1/height)*75+th), (int(x1/width)*75+width-th,int(y1/height)*75+height-th),(0,0,255),th)

            if frame_count ==12:
                cv2.rectangle(img, (int(x1/width)*75+th,int(y1/height)*75+th), (int(x1/width)*75+width-th,int(y1/height)*75+height-th),(-1),th)
                playsound('sound.wav')
                frame_count=0

                if curr=='cl':
                    keyboard = np.zeros((450,750,3),np.uint8)
                    #cv2.putText(keyboard, curr, (pos,100),  cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255),3, 4)
                    pos=0

                elif curr=='I':
                    cv2.putText(keyboard,curr, (pos,100),  cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),3, 2)
                    pos+=20

                else:
                    cv2.putText(keyboard,curr, (pos,100),  cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),3, 2)
                    pos+=30
            if(curr!=prev):

                frame_count=0
                prev=curr
            else:
                frame_count+=1
        else:
            prev="He"


    cv2.imshow('virtual', img)
    cv2.imshow('board',keyboard)


    key=cv2.waitKey(1)
    if key==27:
        break

cam.release()
cv2.destroyAllWindows()