from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import time

if __name__ == '__main__':

    t = time.time()

    # Arguments:
    # -i dataset of user images
    # -e encodings file to be created with encodings of dataset
    # -d detection method cnn or hog
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--dataset", required=True,
                    help="path to input directory of faces + images")
    ap.add_argument("-e", "--encodings", required=True,
                    help="path to serialized db of facial encodings")
    ap.add_argument("-d", "--detection-method", type=str, default="cnn",
                    help="face detection model to use: either `hog` or `cnn`")
    args = vars(ap.parse_args())

    print("[INFO] Cuantificando caras...")
    imagePaths = list(paths.list_images(args["dataset"]))

    knownEncodings = []
    knownNames = []

    for (i, imagePath) in enumerate(imagePaths):

        name = imagePath.split(os.path.sep)[-2]
        print("[INFO] Procesando imagen {}/{} de {}".format(i + 1,
                                                            len(imagePaths), name))

        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR -> RGB

        # Detectar coordenadas (x, y) de los bounding boxes correspondientes a cada cara en la imagen de entrada
        boxes = face_recognition.face_locations(rgb,
                                                model=args["detection_method"])
        # Computa el vector de características
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings: # Por cada encoding (puede haber más de uno si en la imagen había más de una cara)
            # Añade cada encoding + nombre al set de nombres conocidos y encodings
            knownEncodings.append(encoding)
            knownNames.append(name)

    # Carga los encodings al disco
    print("[INFO] Serializando encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open(args["encodings"], "wb")
    f.write(pickle.dumps(data))
    f.close()

    print('[INFO] Duración: '+str(time.time()-t))
