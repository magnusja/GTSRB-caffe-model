import sys
import csv
import os
from PIL import Image
import re

label_map = {
    '0': '20_speed',
    '1': '30_speed',
    '2': '50_speed',
    '3': '60_speed',
    '4': '70_speed',
    '5': '80_speed',
    '6': '80_lifted',
    '7': '100_speed',
    '8': '120_speed',
    '9': 'no_overtaking_general',
    '10': 'no_overtaking_trucks',
    '11': 'right_of_way_crossing',
    '12': 'right_of_way_general',
    '13': 'give_way',
    '14': 'stop',
    '15': 'no_way_general',
    '16': 'no_way_trucks',
    '17': 'no_way_one_way',
    '18': 'attention_general',
    '19': 'attention_left_turn',
    '20': 'attention_right_turn',
    '21': 'attention_curvy',
    '22': 'attention_bumpers',
    '23': 'attention_slippery',
    '24': 'attention_bottleneck',
    '25': 'attention_construction',
    '26': 'attention_traffic_light',
    '27': 'attention_pedestrian',
    '28': 'attention_children',
    '29': 'attention_bikes',
    '30': 'attention_snowflake',
    '31': 'attention_deer',
    '32': 'lifted_general',
    '33': 'turn_right',
    '34': 'turn_left',
    '35': 'turn_straight',
    '36': 'turn_straight_right',
    '37': 'turn_straight_left',
    '38': 'turn_right_down',
    '39': 'turn_left_down',
    '40': 'turn_circle',
    '41': 'lifted_no_overtaking_general',
    '42': 'lifted_no_overtaking_trucks'
}


def read_traffic_signs_train(root_path):
    """Reads traffic sign data for German Traffic Sign Recognition Benchmark.

    Arguments: path to the traffic sign data, for example './GTSRB/Training'
    Returns:   list of image paths, list of corresponding labels"""

    image_paths = []  # images
    labels = []  # corresponding labels
    crop_boxes = []
    # loop over all 42 classes
    for c in range(0, 43):
        class_folder = format(c, '05d')
        prefix = root_path + '/' + class_folder + '/'  # subdirectory for class
        gt_file = open(prefix + 'GT-' + format(c, '05d') + '.csv')  # annotations file
        gt_reader = csv.reader(gt_file, delimiter=';')  # csv parser for annotations file
        gt_reader.next()  # skip header

        # loop over all images in current annotations file
        for row in gt_reader:
            image_paths.append(prefix + row[0])  # the 1th column is the filename
            labels.append(label_map[row[7]])  # the 8th column is the label
            crop_boxes.append((int(row[3]), int(row[4]), int(row[5]), int(row[6])))
        gt_file.close()

    return image_paths, labels, crop_boxes


def read_traffic_signs_test(root_path):
    image_paths = []  # images
    labels = []  # corresponding labels
    crop_boxes = []

    root_path += '/'

    gt_file = open(root_path + 'GT-final_test.test.csv')  # annotations file
    gt_reader = csv.reader(gt_file, delimiter=';')  # csv parser for annotations file
    gt_reader.next()  # skip header

    # loop over all images in current annotations file
    for row in gt_reader:
        image_paths.append(root_path + row[0])  # the 1th column is the filename
        labels.append('test') # for test images just use test as defualt label
        crop_boxes.append((int(row[3]), int(row[4]), int(row[5]), int(row[6])))
    gt_file.close()

    return image_paths, labels, crop_boxes


def write_labels(output_path):
	"""Writes a textfile with all available labels, each in a new line"""
    print('Writing labels.txt')
    with open(os.path.join(output_path, 'labels.txt'), 'w+') as file:
        for label in label_map.values():
            file.write('%s %s' % (label, os.linesep))


def write_label_map(label_textfile, prepend_path, input_path, output_path, image_paths, labels):
	"""Writes for each image the path and the corresponding label in a text file"""
    print 'Writing %s.txt' % label_textfile
    with open(os.path.join(output_path, '%s.txt' % label_textfile), 'w+') as file:
        for image_path, label in zip(image_paths, labels):
            relative_path = image_path.replace(input_path, '')
            relative_path = relative_path.replace('.ppm', '.png')
            relative_path = relative_path[1:] if relative_path[0] == os.path.sep else relative_path
            path = os.path.join(prepend_path, label_textfile,relative_path)
            file.write('%s %s %s' % (path, label, os.linesep))


def convert_images(input_path, output_path, image_paths, labels, crop_boxes):
	"""Converts images to png format and crops the interesting path as stated in csv file"""
    print 'Converting images'
    for image_path, crop_box, label in zip(image_paths, crop_boxes, labels):
        relative_path = image_path.replace(input_path, '')
        relative_path = relative_path.replace('.ppm', '.png')
        relative_path = relative_path[1:] if relative_path[0] == os.path.sep else relative_path
        # write png files into folder named like the corresponding label and not 00001, ...
        relative_path = re.sub('000\d{2}/', label + '/', relative_path)
        converted_image_path = os.path.join(output_path, relative_path)

        if not os.path.exists(os.path.dirname(converted_image_path)):
            os.makedirs(os.path.dirname(converted_image_path))
        else:
            if os.path.isfile(converted_image_path):
                os.remove(converted_image_path)

        image = Image.open(image_path)
        image = image.crop(crop_box)
        image.save(converted_image_path, format='png')


def main():
	# input to GTSRB
    input_folder = sys.argv[1]
    # output of pngs and textfiles
    output_folder = sys.argv[2]
    # for train.txt -> path which shall be prepended, if you would like to copy it somewhere else
    # after converting, e.g. on a remtoe amchine via scp
    train_txt_prepend_path = sys.argv[3]
    # 'train' or 'test' -> GTSRB train or test image processing
    label_textfile = sys.argv[4]

    output_folder = os.path.join(output_folder, label_textfile)

    print 'Input: %s' % input_folder
    print 'Output: %s' % output_folder

    image_paths, labels, crop_boxes = read_traffic_signs_train(input_folder) \
        if label_textfile == 'train' else read_traffic_signs_test(input_folder)

    print 'Image count: %s' % len(image_paths)
    print 'Image count (labels): %s' % len(labels)

    assert len(image_paths) == len(labels)

    if not os.path.exists(output_folder):
     os.makedirs(output_folder)

    write_labels(output_folder)
    write_label_map(label_textfile, train_txt_prepend_path, input_folder, output_folder, image_paths, labels)

    convert_images(input_folder, output_folder, image_paths, labels, crop_boxes)

    print 'Done'

if __name__ == '__main__':
    main()
