from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import os
import numpy as np


cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
path = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
face_classifier = cv2.CascadeClassifier(path)
classifier =load_model(r'/Users/rishirajdatta7/Desktop/Hackathon_techolution/Emotion_Detection_CNN/model.h5')

emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

# cap = cv2.VideoCapture(0)



# while True:
#     _, frame = cap.read()
#     labels = []
#     gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#     faces = face_classifier.detectMultiScale(gray)

#     for (x,y,w,h) in faces:
#         cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
#         roi_gray = gray[y:y+h,x:x+w]
#         roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



#         if np.sum([roi_gray])!=0:
#             roi = roi_gray.astype('float')/255.0
#             roi = img_to_array(roi)
#             roi = np.expand_dims(roi,axis=0)

#             prediction = classifier.predict(roi)[0]
#             label=emotion_labels[prediction.argmax()]
#             label_position = (x,y)
#             cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
#         else:
#             cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
#     cv2.imshow('Emotion Detector',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# image_path = '/Users/rishirajdatta7/Downloads/test_image1.jpeg'  # Replace with your image file path
# frame = cv2.imread(image_path)

# # Convert the image to grayscale
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# # Detect faces in the image
# faces = face_classifier.detectMultiScale(gray)

# for (x, y, w, h) in faces:
#     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
#     roi_gray = gray[y:y + h, x:x + w]
#     roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

#     if np.sum([roi_gray]) != 0:
#         roi = roi_gray.astype('float') / 255.0
#         roi = img_to_array(roi)
#         roi = np.expand_dims(roi, axis=0)

#         prediction = classifier.predict(roi)[0]
#         label = emotion_labels[prediction.argmax()]
#         label_position = (x, y)
#         cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#     else:
#         cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# # Display the image with detected faces and emotion labels
# cv2.imshow('Emotion Detector', frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2
import os
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array


# Directory containing images
image_directory = '/Users/rishirajdatta7/Desktop/frames'  # Replace with the directory containing your images

# Initialize a dictionary to count emotions
emotion_count = {label: 0 for label in emotion_labels}
count = 0
count_positive = 0
count_negative = 0
count_neutral = 0
# Iterate through all images in the directory
for filename in os.listdir(image_directory):
    if filename.endswith(('.jpg', '.jpeg', '.png')):  # Check for image file extensions
        # Construct the full file path
        count+=1
        image_path = os.path.join(image_directory, filename)

        # Read the image
        frame = cv2.imread(image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_classifier.detectMultiScale(gray)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                prediction = classifier.predict(roi)[0]
                label = emotion_labels[prediction.argmax()]
                if(label == 'Happy' or label == 'Surprise'):
                    count_positive += 1
                elif(label == 'Disgust' or label == 'Angry' or label == 'Fear' or label == 'Sad'):
                    count_negative += 1
                elif(label == 'Neutral'):
                    count_neutral += 1
                label_position = (x, y)
                cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Increment the emotion count in the dictionary
                emotion_count[label] += 1
            else:
                cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the image with detected faces and emotion labels
        cv2.imshow('Emotion Detector', frame)
        #cv2.waitKey(0)

# Print the emotion count dictionary
print("Emotion Count:")
for label, count in emotion_count.items():
    print(f"{label}: {count}")
# for label,count in emotion_count.items():
#     if(label == 'Happy' or label == 'Surprise'):
#         count_positive += 1
#     elif(label == 'Disgust' or label == 'Angry' or label == 'Fear' or label == 'Sad'):
#         count_negative += 1
#     elif(label == 'Neutral'):
#         count_neutral += 1
# count = count_positive + count_negative + count_neutral
final_count = count_positive+count_neutral*(-1*0.5)-count_negative 
# print("Metric :" , (final_count/count))
file_path = "/Users/rishirajdatta7/Desktop/emotion_dictionary.txt"

# Write the emotion dictionary to the text file
with open(file_path, "w") as file:
    for emotion, freq in emotion_count.items():
        file.write(f"{emotion}: {freq}\n")

print(f"Emotion dictionary saved to {file_path}")

cv2.destroyAllWindows()
