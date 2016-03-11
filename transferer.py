import cv2
import numpy as np
from PIL import Image
import cStringIO
import base64
import argparse


def transfer_cv2(source, target):
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype('float32')
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype('float32')

    (slm, sls, sam, sas, sbm, sbs) = mean_std(source)
    (tlm, tls, tam, tas, tbm, tbs) = mean_std(target)

    (l, a, b) = cv2.split(target)

    l -= tlm
    a -= tam
    b -= tbm

    l = (tls / sls) * l
    a = (tas / sas) * a
    b = (tbs / sbs) * b

    l += slm
    a += sam
    b += sbm

    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)

    return cv2.cvtColor(cv2.merge([l, a, b]).astype('uint8'), cv2.COLOR_LAB2BGR)


def mean_std(image):
    (l, a, b) = cv2.split(image)

    return l.mean(), l.std(), a.mean(), a.std(), b.mean(), b.std()


ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True,
                help="path to source image")
ap.add_argument("-t", "--target", required=True,
                help="path to target image")
args = vars(ap.parse_args())

source = cv2.imread(args['source'])
target = cv2.imread(args['target'])
transfered = transfer_cv2(source, target)
cv2.imwrite('transfered.jpg', transfered)
