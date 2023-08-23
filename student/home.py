       
from django.http import HttpResponse
from .models import *
from django.core.mail import EmailMessage
from django.http import StreamingHttpResponse
import threading
import cv2
import torch
import numpy as np
from PIL import Image as im
from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL
from django.views.decorators import gzip

import time


import face_recognition
import os

path='C:/güvenilir_online_sınav_sistemi/student_face_data/exp/weights/last.pt'
model = torch.hub.load('ultralytics/yolov5','custom', path, force_reload=True)


@gzip.gzip_page
def Home(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(cam.update(), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'student/app1.html')

#to capture video class
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()



    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def update(self):
        # global countdown
        # countdown=5
        
        # start_time = time.time()
        while True:
            (self.grabbed, self.frame) = self.video.read()
            results=model(self.frame, augment=True)
            for i in results.render():
                data = im.fromarray(i)
                data.save('demo.jpg')
            cv2.imwrite('demo.jpg', self.frame)
            
            self.frame=np.squeeze(results.render())
            
            # if results.pandas().xyxy[0].empty:
            #     # Get the current time in seconds
            #     current_time = time.time()

            #     # Calculate the elapsed time
            #     elapsed_time = current_time - start_time
                
            #     # Check if the elapsed time has reached 1 second
            #     if elapsed_time >= 1:
                   
            #         countdown -= 1

            #         # Reset the start time for the next interval
            #         start_time = time.time()
            #         print(countdown)
            #         if countdown<=0:
            #             return HttpResponseRedirect('afterlogin')

            
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n\r\n')

