import pickle

import cv2
import numpy as np
import face_recognition

import time

ENCODING_FILE = 'encodings.pickle'

APP_TITLE = 'facedoor'
ACTION_ACCEPT = 'a'

if __name__ == '__main__':
    img_check = cv2.imread('resources/check.png', cv2.COLOR_BGR2RGB)
    img_forbidden = cv2.imread('resources/forbidden.png', cv2.COLOR_BGR2RGB)

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

            if cv2.waitKey(1) & 0xFF == ord(ACTION_ACCEPT):
                break

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
                                                     encoding)
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
            # draw the predicted face name on the image
            cv2.rectangle(named_image, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(named_image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)
        # show the output image
        cv2.imshow(APP_TITLE, named_image)
        cv2.waitKey(0)

        # TODO: if accepted then show accept message in screen

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()
