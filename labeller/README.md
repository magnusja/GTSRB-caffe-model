# Labeller

This script converts the images from the GTSRB dataset from the ppm to the png format, which is used by DIGITS/caffe per default. In addition it crops out only the part of the actual traffic sign from the image. The traffic sign bounding box is given by the csv file for each image in the GTSRB data set.

### Usage

The script takes four parameters:
- Input folder: the folder where the GTSRB train and/or test images are located
- Output foler: the folder where the converted pngs and the textfiles are saved
- Prepend path: the path which should be prepended to the label map textfile (used when copying the complete folder to a different location e.g. via scp)
- Label: train or test, defines what data set we are currently looking at, either GTSRB train images or GTSRB test images

Examples:

`python2 main.py /Volumes/MacintoshHD/Users/mep/Downloads/GTSRB/Final_Test/Images /Volumes/MacintoshHD/Users/mep/Downloads/signs /home/ga68fey/signs test`


`python2 main.py /Volumes/MacintoshHD/Users/mep/Downloads/GTSRB/Final_Training/Images /Volumes/MacintoshHD/Users/mep/Downloads/signs /home/ga68fey/signs train`

### Output

#### Train mode

```
[class folders with images]
label.txt -> all available labels
train.txt -> textfile which maps images to classes
```

##### train.txt

```
/home/ga68fey/signs/train/00000/00000_00000.png 20_speed 
/home/ga68fey/signs/train/00000/00000_00001.png 20_speed 
/home/ga68fey/signs/train/00000/00000_00002.png 20_speed 
/home/ga68fey/signs/train/00000/00000_00003.png 20_speed 
/home/ga68fey/signs/train/00000/00000_00004.png 20_speed 
/home/ga68fey/signs/train/00000/00000_00005.png 20_speed 
/home/ga68fey/signs/train/00000/00000_00006.png 20_speed 
/home/ga68fey/signs/train/00000/00000_00007.png 20_speed 
/home/ga68fey/signs/train/00000/00000_00008.png 20_speed 
/home/ga68fey/signs/train/00000/00000_00009.png 20_speed 
/home/ga68fey/signs/train/00000/00000_00010.png 20_speed 
/home/ga68fey/signs/train/00000/00000_00011.png 20_speed 
...
```

#### Test mode

Just the cropped and converted images in the folder, and dummy data for labels and label map textfile, because GTSRB does not provide classifications for the test data set.