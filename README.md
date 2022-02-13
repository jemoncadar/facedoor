# facedoor
**Facedoor** is a facial recognition access control system using Python, OpenCV and Deep Metric Learning. The correct behavior of the system is: 
- There is a PC executing **facedoor** with a camera connected to it, the PC is also connected to a private resource controlling its access (it could be a door, another PC, a safe...).
- When someone wants to access that resource show their face to the camera.
- The system processes their face and compares it to the ones it already has stored in a database (dataset).
- **facedoor** allow the access to that resource or not.

**Facedoor** has been developed following [this amazing tutorial](https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/) made by PyImageSearch. This synthesizes and explies all the deep metric learning ideas and relates them with Python code and the libraries. It's great!

# Requirements
In order to run **facedoor** in your own you must have the following packages installed:
## OpenCV
[OpenCV](https://pypi.org/project/opencv-python/) is a library of programming functions mainly aimed at real-time computer vision. Originally developed by Intel, it was later supported by Willow Garage then Itseez (which was later acquired by Intel). In this project, I specially use from OpenCV: camera engine and Haar Cascade face detection algorithm. You can install it with:
``pip3 install opencv-python``
## dlib
[Dlib](http://dlib.net/) is a general purpose cross-platform software library written in the programming language C++. Its design is heavily influenced by ideas from design by contract and component-based software engineering. In this project it is needed to have ``dlib`` install because ``face-recognition`` library depends on it. It could be installed with: ``pip3 install dlib``.

Note that you will need two packages more to run ``dlib``:
- [CMake](https://cmake.org/install/): it can be installed following the instruction in the link.
- [VisualStudio Community C++](https://visualstudio.microsoft.com/es/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSFeaturesPage&passive=true&tailored=cplus&cid=2031#cplusplus): it can be installed following the instruction in the link.

## numpy
[Numpy](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwilh8fIvfz1AhUjlP0HHeKsBvEQFnoECAcQAQ&url=https%3A%2F%2Fnumpy.org%2F&usg=AOvVaw3L2i9HVc9ZeynETpNrPxO-) is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays. It could be installed with: ``pip3 install numpy``.

## face-recognition
[Face-recognition](https://face-recognition.readthedocs.io/en/latest/readme.html) is an easy to use library that manipulates and recognize faces from Python. It is built using ``dlib``. It could be installed with: ``pip3 install face_recognition``.

# How to run
First of all you will need to add photos of the persons you want to give access. For each user are needed at least 20 photos; that photos should be placed in the folder ``dataset/username`` (where ``username`` is the username of the person in the system). These photos don't need to be face-cropped, because before of processing it, the program will execute a face detection algorithm. One important thing is: there only can be one face in the photos, and it must be the one of the user we want to add. The next step is to obtain the features vectors of the dataset photos. It is a long lasting process because it executes complex face detection algorithms (either CNN or HOG). For this reason this process should be performed once, at the installation of **facedoor**. You can do this by executing:

``python3 encode_faces.py -i dataset -e encodings.pickle``

After that, a *pickle* file will have been created (named _encodings.pickle_) and it will contains the features vectors of each face of the dataset. The next step is to run the main program, for that you shoud execute:

``python3 main.py``

At this point if you press ``a`` a photo will be taken and the program will check the access permissions of the people in it; if you press ``q`` it will finish the execution.

# Results
The results obtained were good and satisfied the goals of the project. In the following image results, **facedoor** was executed _offline_ (with images not coming from a camera, you can do this with the file ``recognize_faces_image.py``). Note that for this examples we have used a dataset with 20 photos of two of the main person of the _Matrix_ saga, Neo and Trinty. Faces of other people won't be recognized until you add photos of them to the ``dataset/`` folder!

![Result 1](https://github.com/jemoncadar/facedoor/blob/main/examples/result2.png?raw=true)

![Result 2](https://github.com/jemoncadar/facedoor/blob/main/examples/result3.png?raw=true)

![Result 3](https://github.com/jemoncadar/facedoor/blob/main/examples/result7.png?raw=true)
