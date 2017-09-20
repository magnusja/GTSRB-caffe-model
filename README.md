# Documentation

This is the documentation for the image recognition of German traffic signs using the deep learning model AlexNet. The images to train the model were retrieved from www.benchmark.ini.rub.de.

*If you have trouble downloading the model, because of my git lfs quota being exceeded, please download here: https://drive.google.com/drive/folders/0B-iC5XyHDwtPT29TaUVaVkg1T0U?usp=sharing*

## Images

The Institut fuer Neuroinformatik of the Ruhr-Universitaet Bonn provides a data set of over 50,000 images of 43 different street signs. The images are in a PPM format and contain one traffic sign each. Sizes vary from 15x15 to 250x250 pixels and the images are not necessarily square. With the images come annotations that are provided in CSV files and that yield the filename, the size, the coordinates of the bounding box in which the sign is to be found, and the assigned class label.

## Preparation

As the interface DIGITS, we are using to train the model, only takes images in a png format, we firstly convert the images from PPM to png. In the same step, we also cropp the images using the coordinates given in the added CSV files such that only the signs are visible in the images. The program we wrote to achieve this is called labeller.py and can be found in the correspondig directory.

## Training

To train the AlexNet model, we first created an image data (color, 256x256 -> ALexNet default) set from our prepared images (using the script in labeller folder). For the data set we first used the `squash` mode to resize images with a different size than 256x256. After training the model we had a very low accuracy, so we switched to `fill` mode, which adds random noise to the image if it is smaller than 256x256 (all of our training images are smaller than 256x256). Then we trained an AlexNet with default parameters (batch size: 40, because of memory issues; snapshot only every 15th epoch, because of the quota limit on the machines).

## Trained Model

After about six hours of training, the model was finished and reached an accuracy of roughly 97%.

![Accuracy Screenshot](https://www.dropbox.com/s/9mvq7dwuqd292is/graph.png?dl=1)

We tested the network with the test images from GTSRB (converted to png and cropped, also available in the Dropbox folder) and the DIGITS web interface. In roughly 9 of 10 cases the classification of the network is correct.

### Strange issue

When classifying many images over the web interface, roughly about the first ten images are not correctly classified, though the classification works properly when only classifying these ten images or classifiyng every image seperately.

## Detection

Currently the network can only classify a sign correctly, if only the sign and a little bit of background is on the image. The test dataset, for instance, is only classified correctly, when the sign was cropped out of the test image corresponding to the bounding box in the csv file. Therefore we also tried to pre process images where different signs and other 'background' things are located on the image. We used OpenCV and tried some basic shape/edge detection, by first converting the input image to gray scale and then to binary using a certain threshold (only black and white, no different gray tones). Then we used the 'findContours' function of OpenCV to get potential traffic sign areas. If the area seems to be promising, we query the REST API of DIGITS, to get a classification from the neural network.

## Folder structure

- caffe: traffic sign caffe model; epoch 30
- demo: classification and detection demo scripts (need caffe, OpenCV and requests installed)
- images: some test images for the demo scripts
- labeller: script used to convert images from GTSRB dataset to our desired format to use them as input for caffe/DIGITS

## Further references and interesting links regarding the topic

- Dropbox folder with presentation and converted pngs: https://www.dropbox.com/sh/ruy75osbm0eak8z/AADReqmuzjH24N8TVsgEx5Lta?dl=0
- https://www.vision.ee.ethz.ch/en/publications/papers/proceedings/eth_biwi_01052.pdf
- http://cs229.stanford.edu/proj2014/Dashiell%20Bodington,%20Eric%20Greenstein,%20Matthew%20Hu,%20Implementing%20Machine%20Learning%20Algorithms%20on%20GPUs%20for%20Real-Time%20Traffic%20Sign%20Classification.pdf
- https://rdmilligan.wordpress.com/2015/03/01/road-sign-detection-using-opencv-orb/
- https://www.youtube.com/watch?v=7xvy9oru_0g
- http://www.emgu.com/wiki/index.php/Traffic_Sign_Detection_in_CSharp
- https://www.quora.com/What-is-the-best-method-to-do-traffic-sign-recognition-using-OpenCV-on-iPhone
- https://www.youtube.com/watch?v=JXYXSG7mVPk
- http://ieeexplore.ieee.org/xpl/login.jsp?reload=true&tp=&arnumber=7033810&url=http%3A%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D7033810
- http://bartlab.org/Dr.%20Jackrit's%20Papers/ney/1.TRAFFIC_SIGN_Lorsakul_ISR.pdf
- https://sites.google.com/site/mcvibot2011sep/home
- https://github.com/dzhibas/pedestrian-sign-detection
- http://stackoverflow.com/questions/28223491/opencv-traffic-sign-recognition
- https://groups.google.com/forum/#!msg/caffe-users/1O59_bjGyec/vUGUsKQ9itwJ <- Yes, we have !
