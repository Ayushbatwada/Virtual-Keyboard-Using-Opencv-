import numpy as np
import cv2
from playsound import playsound
import os

xs={}
prev="He"

#Blue
lower_b = np.array([100,120,100])
upper_b = np.array([150,255,255])
"""
#red
lower_b = np.array([0, 50, 50])
upper_b = np.array([50, 255, 255])
# Green
lower_b= np.array([50,80,80])
upper_b= np.array([100,255,255])
"""
# Keyboard Settings
keyboard = np.zeros((450,800,4),np.uint8)

keys_set3={ 0:"0",1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",
            10:"Q",11:"W",12:"E",13:"R",14:"T",15:"Y",16:"U",17:"I",18:"O",19:"P",
             20:"A",21:"S",22:"D",23:"F",24:"G",25:"H",26:"J",27:"K",28:"L",
             29:"Z",30:"X",31:"C",32:"V",33:"B",34:"N",35:"M",36:"<<",37:"$",38:"cl",39:"         "
        }

kernelOpen = np.ones((4,4))
kernelClose = np.ones((18,18))
sent=""
def letter(letter_index,text):

    # Keys
    y=int(letter_index/10)
    x=(letter_index%10)

    if y==3 and letter_index>37:
        y=4
        x=letter_index%38
    if y==3 and letter_index<=37:
        x+=1
    if y ==2 and letter_index==29:
        y=3
        x=0

    #print(y,x)
    width=75
    height=75
    if y==4 and x==1:
        x=(4)*75
        width=150
    elif y==4 and x==0:
        x=(2)*75
        width=150
    else:
        x=x*75
    y=y*75

    #x=x+int(y/4)
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
    for i in range(40):
       letter(i,keys_set3[i])

    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHsv,lower_b,upper_b)

    #   Morphology
    maskOpen =cv2.morphologyEx(mask, cv2.MORPH_OPEN,kernelOpen)
    maskClose =cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE,kernelClose)

    res = cv2.findContours(maskClose.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    conts,h = res if len(res) == 2 else res[1:3]

    if(len(conts)==1):
        cv2.drawContours(img,conts,-1,(255,0,0),3)
        x1,y1,w1,h1 = cv2.boundingRect(conts[0])

        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        height,width=75,75
        th= 3 #thickness

        if int(x1/width)<=9 and int(y1/height) <4 and not((int(y1/height) ==2 or int(y1/height)==3) and int(x1/width)>8):
            indX = int(x1/width)
            indY = int(y1/width)

            if indY==3:
                indX-=1

            curr=keys_set3[indX+indY*10]
            cv2.rectangle(img, (int(x1/width)*75+th,int(y1/height)*75+th), (int(x1/width)*75+width-th,int(y1/height)*75+height-th),(0,0,255),th)

            if frame_count ==12:
                cv2.rectangle(img, (int(x1/width)*75+th,int(y1/height)*75+th), (int(x1/width)*75+width-th,int(y1/height)*75+height-th),(-1),th)
                playsound('sound.wav')
                frame_count=0

                if curr =="<<":
                    keyboard = np.zeros((450,800,4),np.uint8)
                    pos=0
                    sent= sent[:-1]
                    for _ in sent:
                        cv2.putText(keyboard, _ , (pos,100),  cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),3, 2)
                        if _ =="I":
                            pos+=15
                        else:
                            pos+=25

                elif curr=='I':
                    sent+=curr
                    cv2.putText(keyboard,curr, (pos,100),  cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),3, 2)
                    pos+=15

                elif curr=="$":
                    fl=open("lol.html","w")
                    temp="Your Text is:<br><h1 style='color:red;border: 5px solid blue;'>"+sent+"</h1>"
                    fl.write(temp)
                    fl.close()
                    os.system("start lol.html")

                else:
                    sent+=curr
                    cv2.putText(keyboard,curr, (pos,100),  cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),3, 2)
                    pos+=25
            if(curr!=prev):

                frame_count=0
                prev=curr
            else:
                frame_count+=1
        elif int(x1/width)>=2 and int(x1/width)<4 and int(y1/height)==4:
            curr="cl"
            print(curr)
            height=75
            width=150
            cv2.rectangle(img,(150+th,int(y1/height)*75+th), (300-th,int(y1/height)*75+height-th),(0,0,255),th)
            if frame_count ==12:
                cv2.rectangle(img, (int(x1/width)*75+th,int(y1/height)*75+th), (int(x1/width)*75+width-th,int(y1/height)*75+height-th),(-1),th)
                playsound('sound.wav')
                frame_count=0
                keyboard = np.zeros((450,800,4),np.uint8)
                pos=0
                sent=""
            if(curr!=prev):
                frame_count=0
                prev=curr
            else:
                frame_count+=1
        elif int(x1/width)>=4 and int(x1/width)<6 and int(y1/height)==4:
            curr=" "
            print(curr)
            height=75
            width=150
            cv2.rectangle(img, (300+th,int(y1/height)*75+th), (450-th,int(y1/height)*75+height-th),(0,0,255),th)

            if frame_count ==12:
                sent+=curr
                cv2.rectangle(img, (int(x1/width)*75+th,int(y1/height)*75+th), (int(x1/width)*75+width-th,int(y1/height)*75+height-th),(-1),th)
                playsound('sound.wav')
                frame_count=0
                cv2.putText(keyboard,curr, (pos,100),  cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),3, 2)
                pos+=25


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