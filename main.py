import pickle

import cv2
import numpy as np
import face_recognition

import time

ENCODING_FILE = 'encodings.pickle'

APP_TITLE = 'facedoor'
ACTION_ACCEPT = 'a'
ACTION_EXIT = 'e'
UNKNOWN = 'Unknown'
AUTHORIZED_NAMES = ['moncada', 'neo', 'trinity']

if __name__ == '__main__':
    img_check = cv2.imread('resources/check.png', cv2.COLOR_BGR2RGB)
    img_check = cv2.resize(img_check, (200, 200))
    img_forbidden = cv2.imread('resources/forbidden.png', cv2.COLOR_BGR2RGB)
    img_forbidden = cv2.resize(img_forbidden, (200, 200))

    cv2.namedWindow(APP_TITLE, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(APP_TITLE, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        video_capture = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(frame,
                                                 scaleFactor=1.1, minNeighbors=5)

            # Draw a rectangle around the faces
            rectangle = np.copy(frame)
            for (x, y, w, h) in faces:
                cv2.rectangle(rectangle, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display the resulting frame
            cv2.imshow(APP_TITLE, rectangle)

            action = cv2.waitKey(1) & 0xFF
            if action == ord(ACTION_ACCEPT):
                break
            elif action == ord(ACTION_EXIT):
                exit()

        cv2.imshow(APP_TITLE, frame)

        # At this point
        #   frame: contains the face image without rectangle
        #   rentangle: contains the face image with rectangles
        #   faces: contains the coordinates of faces in (x,y,w,h)

        print("[INFO] loading encodings...")
        data = pickle.loads(open(ENCODING_FILE, "rb").read())

        # Transfor 'faces' in order to be input of "face_recognition.face_encodings(rgb, boxes)"
        # faces is like        (x, y, w, h)
        # faces_t must be like (top, right, botton, left)
        faces_t = [(y, x + w, y + h, x) for (x, y, w, h) in faces]

        # Encoding of each face detected
        encodings = face_recognition.face_encodings(frame, faces_t)

        # initialize the list of names for each face detected
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data['encodings'],
                                                     encoding, tolerance=0.5)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                # determine the recognized face with the largest number of
                # votes (note: in the event of an unlikely tie Python will
                # select first entry in the dictionary)
                name = max(counts, key=counts.get)

            # update the list of names
            names.append(name)

        named_image = np.copy(frame)
        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(faces_t, names):
            color = (0, 255, 0)
            if name == UNKNOWN:
                color = (0, 0, 255)

            # draw the predicted face name on the image
            cv2.rectangle(named_image, (left, top), (right, bottom), color, 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(named_image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, color, 2)
        # show the output image
        cv2.imshow(APP_TITLE, named_image)
        cv2.waitKey(1000)

        result_image = np.copy(named_image)
        result_r = int(result_image.shape[0])
        result_c = int(result_image.shape[1])

        img_acess = None
        if any(item in names for item in AUTHORIZED_NAMES):
            img_access = np.copy(img_check)
            cv2.putText(result_image, 'Bienvenido, ' + names[0], (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)
            print('[INFO] Acceso detectado a nombre de: ' + names[0])
        else:
            img_access = np.copy(img_forbidden)
            cv2.putText(result_image, 'Acceso denegado', (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2)

        img_r = int(img_access.shape[0])
        img_c = int(img_access.shape[1])
        f_0 = result_r // 2 - img_r // 2
        f_1 = result_r // 2 + img_r // 2
        c_0 = result_c // 2 - img_c // 2
        c_1 = result_c // 2 + img_c // 2

        result_image[f_0:f_1, c_0:c_1] = img_access

        cv2.imshow(APP_TITLE, result_image)
        cv2.waitKey(1000)
        # cv2.waitKey(0)

        # When everything is done, release the capture
        # video_capture.release()
        # cv2.destroyAllWindows()
