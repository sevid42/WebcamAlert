import cv2
from time import sleep
import datetime
import os
import pyttsx3
import threading
  

# transforma texto a voz
def habla(engine):
    try:       
        engine.say("I know your face mother fucker")
        engine.runAndWait()
    except:
            pass


#configurar los parametros usados para la voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)


lista_estados=[None,None]
imagen_inicial=None
video=cv2.VideoCapture(0)


while True:
    check, frame = video.read()
    estado=0
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),2) #el ultimo es la desviacion, a mas grandes mas borroso

    if imagen_inicial is None:
        imagen_inicial=gray_frame
        continue

    delta=cv2.absdiff(imagen_inicial,gray_frame)
    threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    (contornos,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    for contorno in contornos:
        if cv2.contourArea(contorno) < 10000:
            continue
        estado=1
        (x, y, w, h)=cv2.boundingRect(contorno)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)
    lista_estados.append(estado)

    if lista_estados[-1]==1 and lista_estados[-2]==0:
        
        t = threading.Thread(target=habla, args=(engine,))
        t.start()

     

        print("Te pillamos master")
        

        name=str(datetime.datetime.now())
        name = name.replace(":", "")
        name = name.replace(".", "_")+ '.jpg'
        
        cv2.imwrite(name,frame)

        #habla(engine)


        #sleep(0.1)
  

    cv2.imshow("gray_frame Frame",gray_frame)
    cv2.imshow("Delta Frame",delta)
    cv2.imshow("Threshold Frame",threshold)
    cv2.imshow("Color Frame",frame)
    
    if cv2.waitKey(1)==ord('q'):
        break

#libera recursos
video.release()
cv2.destroyAllWindows