from django.shortcuts import render
# Create your views here.

from django.core.files.storage import FileSystemStorage

from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
import json
from tensorflow import Graph


img_height, img_width=224,224
with open('./models/imagenet_classes.json','r') as f:
    labelInfo=f.read()

labelInfo=json.loads(labelInfo)


model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model=load_model('./models/inception_facefeatures_new_model.h5')



def index(request):
    context={'a':1}
    return render(request,'index.html',context)



def predictImage(request):
    print (request)
    print (request.POST.dict())
    fileObj=request.FILES['filePath']
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName)
    testimage='.'+filePathName
    img = tf.keras.utils.load_img(testimage, target_size=(img_height, img_width))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x=x/255
    x=x.reshape(1,img_height, img_width,3)
    with model_graph.as_default():
        with tf_session.as_default():
            predi=model.predict(x)

    import numpy as np
    #predictedLabel=labelInfo[str(np.argmax(predi[0]))]

    r=np.argmax(predi)
        
    if result[0][0] == 1:
        prediction = 'Request'
    elif result[0][1] == 1:
        prediction = 'Skin'
    elif result[0][2] == 1:
        prediction = 'Bad'
    elif result[0][3] == 1:
        prediction = 'Beautiful'
    elif result[0][4] == 1:
        prediction = 'Friend'
    elif result[0][5] == 1:
        prediction = 'Good'
    elif result[0][6] == 1:
        prediction = 'House'
    elif result[0][7] == 1:
        prediction = 'Me'
    elif result[0][8] == 1:
        prediction = 'My'
    elif result[0][9] == 1:
        prediction = 'Urine'
    elif result[0][10] == 1:
        prediction = 'You'
    else:
        prediction = 'invalid'
        
    #print(prediction)
    context=prediction


    #context={'filePathName':filePathName,'predictedLabel':predictedLabel[1]}
    return render(request,'index.html',context) 

def viewDataBase(request):
    import os
    listOfImages=os.listdir('./media/')
    listOfImagesPath=['./media/'+i for i in listOfImages]
    context={'listOfImagesPath':listOfImagesPath}
    return render(request,'viewDB.html',context) 
