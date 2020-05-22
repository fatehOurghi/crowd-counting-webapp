import numpy as np
import cv2
import onnxruntime as rt
import os
import requests
import json
########################################################################################################################
#################################################   Processing   #######################################################
########################################################################################################################

def norm_rgb_img(img):
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    for i in range(0, 3):
        img[:, :, i] = (img[:, :, i] - mean[i]) / std[i]
    return img


def isgray(img):
    if len(img.shape) == 3:
        return False
    return True


def preprocess(img, input_shape, pre_order):
    w = input_shape["width"] if isinstance(input_shape["width"], int) and input_shape["width"] > 0 else img.shape[1]
    h = input_shape["height"] if isinstance(input_shape["height"], int) and input_shape["height"] > 0 else img.shape[0]
    img = cv2.resize(img, (w, h))
    # rgb required
    if input_shape["depth"] == 3:
        if isgray(img):
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img = img / 255.0
        img = norm_rgb_img(img)
    # gray required
    else:
        if not isgray(img):
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = img / 255.0
        img = np.reshape(img, (w, h, 1))
    img = np.expand_dims(img.astype(np.float32), axis=0)
    return np.einsum(pre_order + '->' + input_shape["order"], img)


def postprocess(img):
    return np.squeeze(img)


########################################################################################################################
#################################################   Inference   ########################################################
########################################################################################################################

def local_infer():
    input_shape = {
        "batch_size": 1,
        "height": 768,
        "width": 1024,
        "depth": 3,
        "order": "bhwd"  # "bdhw"
    }
    pre_order = "bhwd"
    print(os.listdir())
    img = cv2.imread(os.path.join("account/img.jpg"))
    im = preprocess(img, input_shape, pre_order)

    session = rt.InferenceSession(os.path.join("account/models/modelsanet.onnx"))

    out = session.run(None, {session.get_inputs()[0].name: im})
    print(np.sum(out[0]))
    cv2.imshow("dm", postprocess(out[0]) * 255)
    cv2.waitKey(0)


def ort_client(image, model, dtype, pre_order, input_shape, url):
    # preprocess
    img = preprocess(image, input_shape, pre_order)

    # prepare data
    data_to_send = {
        "input": img.tolist(),
        "model": model,
        "dtype": dtype
    }
    headers = {
        'content-type': 'application/json'
    }

    # send to server and receive response
    response = requests.post(url, json=data_to_send, headers=headers)

    # postprocess
    data = json.loads(response.text)
    densitymap = postprocess(np.array(data['output']))
    count = int(np.sum(densitymap))

    return densitymap * 255, count
