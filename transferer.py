import cv2
import numpy as np


def transfer(source_path, target_path, transfer_path):
    source = cv2.cvtColor(cv2.imread(source_path), cv2.COLOR_BGR2LAB).astype('float32')
    target = cv2.cvtColor(cv2.imread(target_path), cv2.COLOR_BGR2LAB).astype('float32')

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

    res = cv2.cvtColor(cv2.merge([l, a, b]).astype('uint8'), cv2.COLOR_LAB2BGR)
    cv2.imwrite(transfer_path, res)


def mean_std(image):
    (l, a, b) = cv2.split(image)

    return l.mean(), l.std(), a.mean(), a.std(), b.mean(), b.std()
