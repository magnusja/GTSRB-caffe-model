import cv2
import sys
import requests


def main():
    img = cv2.imread('../images/road.png')

    # convert to gray and to binary using a threshold, to detect edges/shapes
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 4)

    # find shapes/contours
    contours, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:

        perimeter = cv2.arcLength(contour, True)
        # skip shape/contour if it is too small or too big
        if perimeter < 50 or perimeter > 400 or cv2.isContourConvex(contour):
            continue

        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        x, y, w, h = cv2.boundingRect(contour)

        # colour different shapes
        if len(approx) == 3:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        elif len(approx) == 4:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        elif len(approx) >= 100:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        else:
            # not an interesting shape for us
            continue

        # crop out the image, which might be a traffic sign,
        # save it to test.png
        cropped = img[y:y + h, x:x + w]
        cv2.imwrite('test.png', cropped)

        # query DIGITS REST API for classification
        response = requests.post(
            'http://localhost:5000/models/images/classification/classify_one.json?job_id=20151207-223900-80d9',
            files={'image_file': ('file.png', open('test.png', 'rb'))})

        predictions = response.json()['predictions']

        # only label shape if over 90%
        if predictions[0][1] > 90:
            print predictions[0][0]
            cv2.putText(img, predictions[0][0], (x + w + 5, y + h + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

    cv2.imshow('Demo', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
