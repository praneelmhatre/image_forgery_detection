from django.shortcuts import render
#import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
#from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping
from keras.models import load_model

from django.views.generic import TemplateView
from forgery.forms import ImagesForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse

from .forms import ImagesForm
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Images
import re
from PIL import Image, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS
import os
import itertools
# %matplotlib inline
# np.random.seed(2)
image_size = (128, 128)
X = [] # ELA converted images
Y = [] # 0 for fake, 1 for real

class_names = ['fake', 'real']


def convert_to_ela_image(path, quality):
    temp_filename = 'temp_file_name.jpg'
    ela_filename = 'static/img/temp_ela.png'
    
    image = Image.open(path).convert('RGB')
    image.save(temp_filename, 'JPEG', quality = quality)
    temp_image = Image.open(temp_filename)
    
    ela_image = ImageChops.difference(image, temp_image)
    
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
 #   eli=image.save(ela_image)
    ela_image.save(ela_filename, 'JPEG', quality = quality)
    ela_image.save("temp_ela.png", 'JPEG', quality = quality)
#    elaii=open("temp_ela.png","rb")
    
    return ela_image

def prepare_image(image_path):
    return np.array(convert_to_ela_image(image_path, 90).resize(image_size)).flatten() / 255.0


model=load_model('model2_casia_run6.h5', compile = False)

def compute_ela_cv(path, quality):
    temp_filename = 'temp_file_name.jpg'
    SCALE = 15
    orig_img = cv2.imread(path)
    orig_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2RGB)
    
    cv2.imwrite(temp_filename, orig_img, [cv2.IMWRITE_JPEG_QUALITY, quality])

    # read compressed image
    compressed_img = cv2.imread(temp_filename)

    # get absolute difference between img1 and img2 and multiply by scale
    diff = SCALE * cv2.absdiff(orig_img, compressed_img)
    return diff

def masking():
    img = cv2.imread('temp_ela.png', cv2.IMREAD_UNCHANGED)

    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    #img_ = cv2.threshold(gray,100,225,cv2.THRESH_BINARY)
    edges = cv2.Canny(gray, 250, 250)
    # Binarize edges
    binedge=(edges>0).astype(np.uint8)
    # Removing edges too close from left and right borders
    binedge[:,:20]=0
    binedge[:,-20:]=0
    # Fatten them so that there is no hole
    ker=np.ones((3,3))
    fatedge=cv2.dilate(binedge, ker)
    # Find connected black areas
    n,comp=cv2.connectedComponents((fatedge==0).astype(np.uint8))
    # comp is an image whose each value is the index of the connected component
    # Assuming that point (0,0) is in the border, not inside the character, border is where comp is == comp[0,0]
    # So character is where it is not
    # Or, variant from new image: considering "outside" any part that touches one of the left, right, or top border
    # Note: that is redundant with previous 0ing of left and right borders
    # Set of all components touching left, right or top border
    listOutside=set(comp[:,0]).union(comp[:,-1]).union(comp[0,:])
    if 0 in listOutside: listOutside.remove(0) # 0 are the lines, that is what is False in fatedge==0
    filled=(~np.isin(comp, list(listOutside))).astype(np.uint8) # isin need array or list, not set

    # Just to be extra accurate, since we had dilated edges, with can now erode result
    output=cv2.erode(filled, ker)
    cv2.imwrite('static/img/masked.png',output*255)
    return output

# def loadmod():
#     # load model
#     model=load_model('model2_casia_run4_best3.h5')
    
#     return model

# Create your views here.

# class home(CreateView):
#     model=Image
#     form_class=ImagesForm
#     template_name='index.html'

def media(request):
    pass

# def index2(request):
#     # print("Loaded the model file")
#     # summ=model.summary()

#     if request.method=='POST':
#         form=ImagesForm(request.POST, request.FILES)
#         if form.is_valid() :
#             form.save()
#             messages.success(request, 'Uploaded !')
#             return redirect('success')
#         else:
#             messages.info(request, 'some error occured')
#             return redirect('index.html',{'form': form })

#     else:
#         form = ImagesForm(request.POST)
#         return render(request,'index.html', {'form': form })
    
def index(request):
    real_img=None
    if request.method=='POST':
        upimg=request.FILES.get('file')
        
        ela=convert_to_ela_image(upimg,98)
        img=Images.objects.create(uploaded_image=upimg)
        img.save()

        orgimg = Image.open(upimg)
        org = orgimg.rotate(0)
        org= orgimg.convert('RGB')
        org.save("orgimg.jpeg", "jpeg") 
        elacv=compute_ela_cv("orgimg.jpeg", 98)
        plt.imshow(elacv)
        plt.savefig('static/img/elacv.png')
        # Masking
        masking()
        #predict
        image = prepare_image(upimg)
        image = image.reshape(-1, 128, 128, 3)
        y_pred = model.predict(image)
        y_pred_class = np.argmax(y_pred, axis = 1)[0]
        pred_class=class_names[y_pred_class]
        real_img = Images.objects.all().last()
        #real_img = Images.objects.latest('uploaded_image')

        # open the image
        imageeee = Image.open("orgimg.jpeg")
 
        # extracting the exif metadata
        exifdata = imageeee.getexif()

        # getting the basic metadata from the image
        info_dict = {
            "Filename": imageeee.filename,
            "Image Size": imageeee.size,
            "Image Height": imageeee.height,
            "Image Width": imageeee.width,
            "Image Format": imageeee.format,
            "Image Mode": imageeee.mode,
            "Image is Animated": getattr(imageeee, "is_animated", False),
            "Frames in Image": getattr(imageeee, "n_frames", 1)
        }

        messages.info(request,"Request send successfully")
        return render(request,'Results.html',{'ela':ela,'real_img':real_img,'pred':y_pred,'pred_class':pred_class,'info_dict':info_dict})
    else:
        return render(request,'Homee.html',{'real_img':real_img})
 
def success(request):
    return HttpResponse('successfully uploaded')

def aboutus(request):
    real_img = Images.objects.values_list('uploaded_image')[0]
    ri=Images.objects.all()
#    real_img = Images.objects.all()
    return render(request,'aboutus.html',{'real_img':real_img,'ri':ri})   

def result(request):
    real_img = Images.objects.values_list('uploaded_image')[0]
    ri=Images.objects.all()
#    real_img = Images.objects.all()
    return render(request,'Results.html',{'real_img':real_img,'ri':ri})   
# class Home(TemplateView):
#     form = ImagesForm
#     template_name = 'index.html'

#     def post(self, request, *args, **kwargs):
#         form = ImagesForm(request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse_lazy('home', kwargs={'pk': pk}))
#         context = self.get_context_data(form=form)
#         return self.render_to_response(context)     

#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)

# def index_old(request):
#   print("Loaded the model file")
#   summ=model.summary()
#   if request.method=='POST':
       

#         image=request.FILES['image']
#         convert_to_ela_image(image,90)

#         return render(request,'index.html',{'summary':summ,'img':image})
#   else:
#         return render(request,'index.html',{'summary':summ})
