# Demo Scripts

This folder contains two demonnstration scripts, which use the traffic sign AlexNet for classification.

### WT15-DL_SignKafe_main

This sript simply takes the test png images from the folder '../images/', classifies them via the caffe python module and simply prints out the results to the standard out. The input images are test images from the GTSRB (http://benchmark.ini.rub.de/?section=gtsrb&subsection=dataset), converted from ppm to png, and cropped to only show the actual traffic sign (crop bounding boxes are located in the csv file of the test set for every image, see ../labeller)

The script relies on `example.py` which is provided by nvidia (https://github.com/NVIDIA/DIGITS/tree/master/examples/classification).

Usage:
`python2 WT15-DL_SignKafe_main.py`

### detect0r

This script loads an image from a road and uses OpenCV (needs to be installed!) to detect potential traffic signs in the image. After detection it crops out the part of the image where a traffic sign seems to be, and queres the REST API (!!) of DIGITS, for classificatin (using python module requests: `pip install requests`). It does not use the pyhton caffe module!! The script shows the result visualised in a (OpenCV) window.

