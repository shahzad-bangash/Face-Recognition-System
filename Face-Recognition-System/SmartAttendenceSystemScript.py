from datetime import datetime
import numpy as np
import cv2
import os
import face_recognition


def encoding_images(images):
    encoding_list = []
    for img in images:
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(img)[0]
        encoding_list.append(encoding)
    return encoding_list

def attendence(name):
    with open('Attendence.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            time_now = datetime.now()
            sztime = time_now.strftime('%H:%M:%S')
            szdate = time_now.strftime('%d/%m/%Y')
            f.writelines(f'\n{name},{sztime},{szdate}')
            print(name + ' entry is added to attendence sheet')
    

path = 'Images'
student_image = []
student_name = []

myList = os.listdir(path)
# print(myList)

for i in myList:
    current_img = cv2.imread(f'{path}/{i}')
    student_image.append(current_img)
    student_name.append(os.path.splitext(i)[0])


# print(student_name)
encode_list = encoding_images(student_image)

#ip_url_video = "http://192.x"
#webcam = cv2.VideoCapture(ip_url_video ) 
webcam = cv2.VideoCapture(0) # 0 for the device default camera
print("Press Enter key to exit webcam")

if not webcam.isOpened():
    print("Error: Unable to access the webcam.")
    exit(1)


print('WebCam started')
while True:
    check, frame = webcam.read()
    if not check or frame is None:
        print("Failed to grab frame")
        break  # or continue, depending on your logic
    frames = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
    faces_in_frames = face_recognition.face_locations(frames)
    encode_in_frames = face_recognition.face_encodings(frames, faces_in_frames)

    for encodeFace, faceLoc in zip(encode_in_frames, faces_in_frames):
        matches = face_recognition.compare_faces(encode_list, encodeFace)
        faceDis = face_recognition.face_distance(encode_list, encodeFace)

        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = student_name[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1, y2+18), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0), 2)
            attendence(name)
    
    cv2.imshow("WebCam", frame)

    # To end the program if Enter key is pressed
    if cv2.waitKey(10) == 13: 
        print("Enter key is Pressed, Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
            
