import cv2
import pytesseract
extraer=0.0
suma=0.0
cantidadP=0
cantidadI=0
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
placa = []

image = cv2.imread('placa.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.blur(gray,(3,3))
canny = cv2.Canny(gray,150,200)
canny = cv2.dilate(canny,None,iterations=1)

cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


for c in cnts:
  area = cv2.contourArea(c)

  x,y,w,h = cv2.boundingRect(c)
  epsilon = 0.09*cv2.arcLength(c,True)
  approx = cv2.approxPolyDP(c,epsilon,True)
  
  if len(approx)==4 and area>9000:
    print('area=',area)
    #cv2.drawContours(image,[approx],0,(0,255,0),3)

    aspect_ratio = float(w)/h
    if aspect_ratio>2.4:
      placa = gray[y:y+h,x:x+w]
      text = pytesseract.image_to_string(placa,config='--psm 11')
      

      cv2.imshow('PLACA',placa)
      cv2.moveWindow('PLACA',780,10)
      cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
      cv2.putText(image,text,(x-20,y-10),1,2.2,(0,255,0),3)
     
      
      #Busca digitos dentro de el texto ledido y los guarda dentro de una lista de tipo cadeda
      numbers = [str(temp)for temp in text.split() if temp.isdigit()]
     
     #Concatena los elementos de la lista string y los convierte en un solo elemento
      StrA = "".join(numbers)
      #convierte la cadena StrA a un entero numero
      numero=int(StrA)
   

      #Ciclo para separa los digitos del numero
      while numero != 0:
         extraer = numero % 10
         #condicion para sumar la cantidad de numeros pares encontrados
         if(extraer%2==0):
           cantidadP+=1
           #condicion para sumar la cantidad de numeros impares encontrados
         if(extraer%2!=0):
          cantidadI+=1
         numero //= 10.
         suma+= extraer
          #SUMA DE NUMEROS
  

      #salidas de pantalla para suma total en los digitos y cantidades de pares e impares
      print("Suma total: "+str(suma))
      print("Impares: "+str(cantidadI))
      print("Pares: "+str(cantidadP))
      cv2.putText(image,"Suma de digitos: "+str(suma),(30,30),1,2.2,(255,255,255),3)
      cv2.putText(image,"Cantidad de numeros Pares: "+str(cantidadP),(30,60),1,2.2,(255,255,255),3)
      cv2.putText(image,"Cantidad de numeros Impares: "+str(cantidadI),(30,90),1,2.2,(255,255,255),3)
  
cv2.imshow('Image',image)
cv2.moveWindow('Image',45,10)
cv2.waitKey(0)