import face_recognition
import cv2

# showin image on window in RGB formate by default it is in BGR formate
image1 = face_recognition.load_image_file('Images/John_Mccarthy.jpg')
# test = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
#cv2.imshow('Image', image1)

# finding face in the image and encoding it
faceLocation = face_recognition.face_locations(image1)[0]
top, right, bottom, left = faceLocation
cv2.rectangle(image1, (left, top), (right, bottom), (255, 255, 0), 2)
cv2.putText(image1, 'Image1', (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
cv2.imshow('Image', image1)
encoding_image1 = face_recognition.face_encodings(image1)[0]

# getting test image and encoding it
image2 = face_recognition.load_image_file('Images/SteveJobs.jpg')
image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
encoding_Image2 = face_recognition.face_encodings(image2)

# comparing both images
results = face_recognition.compare_faces(encoding_image1, encoding_Image2)

# printing matched and unmatched text
if results == [True]:
    results = 'Matched'
else:
    results = 'Unmatched'

cv2.putText(image2, f'Image2: {results} with Image1', (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
cv2.imshow('test_image', image2)

cv2.waitKey(5000)
cv2.destroyAllWindows()
