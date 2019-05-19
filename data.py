#!/usr/bin/python2

import cgi,os
import cgitb; cgitb.enable()

head = 0
specs=0
female=0
male=0

form= cgi.FieldStorage()


fileitem = form['d']

if(type(fileitem)!=list):
	if fileitem.name:
	   fn = os.path.basename(fileitem.filename.replace("\\", "/" ))
	   open('data2/'+fn, 'wb').write(fileitem.file.read())

	   message = 'The file "' + fn + '" was uploaded successfully'
	   
	else:
	   message = 'No file was uploaded'

else:
	for i in fileitem:
		if i.name:
		   fn = os.path.basename(i.filename.replace("\\", "/" ))
		   open('data2/'+fn, 'wb').write(i.file.read())

		   message = 'The file "' + fn + '" was uploaded successfully'
		   
		else:
		   message = 'No file was uploaded'

# main operation on images starting from now

import cv2
import numpy as np
import os.path

from cv2 import WINDOW_NORMAL
from face_detection import find_faces


#loading face xml database
face_cascade = cv2.CascadeClassifier('face.xml')
glass_cascade= cv2.CascadeClassifier('specs.xml')

def analyze_picture(model_gender, path, head,male,female,specs ):
    image = cv2.imread(path, 1)
    for normalized_face, (x, y, w, h) in find_faces(image):
        gender_prediction = model_gender.predict(normalized_face)
        if (gender_prediction[0] == 0):
            female=female+1
        else:
            male=male+1
        head=head+1
        glass = glass_cascade.detectMultiScale(normalized_face,1.04,5)
        for(gx,gy,gw,gh) in glass:
        	specs+=1
    specs=int(specs/2)
    return [head,male,female,specs]

# Load model
fisher_face_gender = cv2.face.FisherFaceRecognizer_create()
fisher_face_gender.read('gender_classifier_model.xml')
try :
	if(type(fileitem)!=list):
		path = "data2/"
		path += os.path.basename(fileitem.filename.replace("\\", "/" ))
		head,male,female,specs = analyze_picture(fisher_face_gender, path, head,male,female,specs)
	else:
		for i in fileitem:
			path = "data2/"
			path += os.path.basename(i.filename.replace("\\", "/" ))
			head,male,female,specs = analyze_picture(fisher_face_gender, path, head,male,female,specs)

except Exception as e:
	pass

#now variable are formed to store result in html format

ans = '''

<h2>no of persons in crowd are:</h2>
<h4>%d</h4>
<h2>no of persons having glasses:</h2>
<h4>%d</h4>
<h2>no of males in crowd are:</h2>
<h4>%d</h4>
<h2>no of females in crowd are:</h2>
<h4>%d</h4>

'''%(head, specs, male, female)



page = '''


<!DOCTYPE html>
<html>

<head>
<title> CROWD DETAIL EXTRACTOR</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link href="css/style.css" rel="stylesheet" type="text/css" media="all" />
<link href="//fonts.googleapis.com/css?family=Cormorant+SC:300,400,500,600,700" rel="stylesheet">
<link href="//fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i,800,800i" rel="stylesheet">
</head>

<body>
	<div class="padding-all">
		<div class="header">
			<h1>CROWD FACE ANALYSER</h1>
		</div>

    <div id="after" class="design-w3l">
      %s
    </div>
		
</body>
</html>

'''%(ans)

open("/var/www/html/redirect.html",'wb').write(page)


print "Location: http://127.0.0.1/redirect.html\n"



