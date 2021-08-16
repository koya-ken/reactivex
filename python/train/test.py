import cv2
import numpy as np

from scipy import signal

def ReLu(x):
    return np.maximum(0.5, x)

def softmax(x):
  if (x.ndim == 1):
    x = x[None,:]    # ベクトル形状なら行列形状に変換
  # テンソル（x：行列）、軸（axis=1： 列の横方向に計算）
  return np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)

def to_image(b, g, r):
    img = np.dstack([b,g,r])
    max_v = np.max(img)
    # img = softmax(ReLu(img)) * 255
    img = (img / max_v) * 255
    img[img < 255 * 0.3] = 0
    img = img.astype(np.uint8)
    return cv2.applyColorMap(img, cv2.COLORMAP_JET)

def rand_img():
    img = cv2.imread('test.jpg')
    orig_img = img.copy()
    row = np.random.randint(3,12)
    col = row
    print(row)
    size = row * col
    img_filter = np.random.randn(size).reshape(col,row)
    img = img / 255
    b = signal.convolve2d(img[:,:,0], img_filter,'same')
    g = signal.convolve2d(img[:,:,1], img_filter,'same')
    r = signal.convolve2d(img[:,:,2], img_filter,'same')

    img_b = to_image(b,b,b)
    img_g = to_image(g,g,g)
    img_r = to_image(r,r,r)
    img = to_image(b,g,r)
    print(img.shape)
    print(orig_img.shape)

    t = np.hstack([img_b, img_g])
    b = np.hstack([img_r, orig_img])
    img = np.vstack([t,b])
    return img

while True:
    img = rand_img()
    cv2.imshow('test', img)
    key = cv2.waitKey(0)

    if key == ord('q'):
        break
