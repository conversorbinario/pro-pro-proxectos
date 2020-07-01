from zipfile import ZipFile
from PIL import Image
import pytesseract as pyt
import cv2 as cv
import numpy as np

#Exercicio final da especialización: https://www.coursera.org/specializations/python-3-programming

#programa sinxelo. Usando unha serie de librarías, extraemos imaxes comprimidas nun .zip
#as imaxes teñen texto (i.e., como as dun periódico). Se a palabra que desexamos aparece nalgún texto,
#buscamos as caras das fotos, recortámolas e amosámolas.

def cargando_imaxes_zip(list_img):
    #carga imaxes dun .zip e retorna unha lista das mesmas ede tipo numpu.ndarray. blanco e negro
    cv_imgs=[]
    for n in list_img:
        #obxecto cv sacado do zip
        image = cv.imread(zip_img.extract(n))
        #e metémolo nunha lista
        cv_imgs.append(image)
    return cv_imgs

def transformar_bn(numpy_images):
    numpy_bn=[]
    for image in numpy_images:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        numpy_bn.append(image)
    return numpy_bn

def show_cv(cv_images):
    for image in cv_images:  
        cv.imshow('window', image)
        cv.waitKey(2000)
    cv.destroyAllWindows()


def cv_Image(numpyimage):
    #retorna un obexcto Image a partir dunha numpy.nadarray
    return Image.fromarray(numpyimage,"L")

def cv_Text(numpyimage):
    #colle o texto presente na imaxe e retornao como string
    text = pyt.image_to_string(numpyimage)
    return text
    

def cvToImageS(numpyList):
    #converte unha lista de "images numpy" en obxectos de tipo imaxe e retorna a listaxe
    images = []
    for numpyimage in numpyList:
        image=cv_Image(numpyimage)
        images.append(image)
    return images

def elements_image(numpy_image, xml_finder):
    #for a given image in numpy.ndarray, returns what xml_finder can find
    #(faces in my case)
    #esta parte é interesante. cambia os o valor dos últimos parámetros para xogar coas diferetnes
    #sensibilidades de deteccion da funcion. deste modo, detéctanse diferentes obxectos como caras
    #xogando con eles podemos ser máis ou menos precisos na detección das caras
    elements_found = xml_finder.detectMultiScale(numpy_image, 1.3, 5)
    return elements_found

def canvas_image(x, y):
    contact_sheet=Image.new('RGB', (x,y), (0, 0, 0))
    return contact_sheet

def collage_faces(pic, coordenadas):
    x,y=0,0
    canvas=canvas_image(600,160)
    img=Image.fromarray(pic, "L")
    size=(100,80)
    #agora, pegamos as caras no canvas
    for cara in coordenadas:
        cara = cara.tolist()
        #watch out, we are using a tuple (one parameter)
        face=img.crop((cara[0],cara[1],cara[0]+cara[2],cara[1]+cara[3]))
        face.thumbnail(size, Image.ANTIALIAS)
        if x >500:
            y=80
            x=0
        canvas.paste(face, (x,y))
        x+=100
    canvas.show()

face_cascade = cv.CascadeClassifier('YOUR_ABSOLUTEPATH to to the directory where you store you .xml/haarcascade_frontalface_default.xml')

#igual aqui. usa o path (xa sexa absoluto ou relativo) ata o zip que contén as imaxes que queres tratar.
zip_img=ZipFile('readonly/small_img.zip','r')
list_img=zip_img.namelist()

#canvas to paste the faces.

imagesCV=cargando_imaxes_zip(list_img)
print('We are going to show you the faces of pictures present in articles where the key word you are required to introduce is present')
key_word= input('Key word: ')
images_bn=transformar_bn(imagesCV)
i=0

for image in images_bn:
    image_text = cv_Text(image)
    image_text = image_text.split()
    #checking if the desired word is present in the article- If so, let's extract the faces from the pictures
    if key_word in image_text:
        print("Result found in " + list_img[i])
        cor_faces=elements_image(image,face_cascade)

        #pra ver se se topou algunha cara ou non
        if len(cor_faces)>0:
            collage_faces(image, cor_faces)
        else:
            print('But there were no faces in that file!')
    i=i+1
