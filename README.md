# facedoor
Facedoor is a face-recoginition access control system using Python, OpenCV and Deep Metric Learning. The correct behavior of the system is: 
- There is a PC executing **facedoor** with a camera connected to it, the PC is also connected to a private resource (it could be a door, other PC, a safe...).
- When someone wants to access that resource show their face to the camera.
- The system processes their face and compares it to the ones it already has stored in a database.
- **facedoor** allow the acces to that resource or not.

# Requirements
In order to run **facedoor** you must have the following packages installed:
## OpenCV
[OpenCV](https://pypi.org/project/opencv-python/) is one of the best known computer vision libraries for python. It could be installed with:
``pip3 install opencv-python``
## dlib
[dlib](http://dlib.net/) is a modern toolkik containing machine learning algorithms and tools for creating complex software in Python/C++ to solve real world problems. It could be installed with: ``pip3 install dlib``.

Note that you will need two packages more to run ``dlib``:
- [CMake](https://cmake.org/install/): following the instructions in the previous link.
- [VisualStudio Community C++](https://visualstudio.microsoft.com/es/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSFeaturesPage&passive=true&tailored=cplus&cid=2031#cplusplus): following the instruction in the previous link.

## numpy
[Numpy](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwilh8fIvfz1AhUjlP0HHeKsBvEQFnoECAcQAQ&url=https%3A%2F%2Fnumpy.org%2F&usg=AOvVaw3L2i9HVc9ZeynETpNrPxO-) is a Python library that allows the creation and use of multidimensional vectors and arrays, with a huge ammount of mathematical high-level functions. It could be installed with: ``pip3 install numpy``.

## face-recognition
[Face-recognition](https://face-recognition.readthedocs.io/en/latest/readme.html) is an easy-to-use library that manipulates and recognize faces from Python. It is built using _dlib_. It could be installed with: ``pip3 install face_recognition``.

# How to run
