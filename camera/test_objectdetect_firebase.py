import numpy as np
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import math
import cv2
import time
import matplotlib
matplotlib.use('Agg')

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

import pyrebase
from datetime import datetime, timedelta, date
import urllib.request, json

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("/home/mike/models/research")
from object_detection.utils import ops as utils_ops

if tf.__version__ < '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')
from object_detection.utils import label_map_util

from object_detection.utils import visualization_utils as vis_util

startTime = time.time()
# What model to download.
MODEL_NAME = 'faster_rcnn_nas_coco_2017_11_08'
#MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('/home/mike/models/research/object_detection/data', 'mscoco_label_map.pbtxt')
#PATH_TO_LABELS = os.path.join('/home/mike/models/research/object_detection/data', 'mscoco_label_map1.pbtxt')

NUM_CLASSES = 90
# opener = urllib.request.URLopener()
# opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
# tar_file = tarfile.open(MODEL_FILE)
# for file in tar_file.getmembers():
#     file_name = os.path.basename(file.name)
#     if 'frozen_inference_graph.pb' in file_name:
#         tar_file.extract(file, os.getcwd())
#
#
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
#
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

# For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = '/home/mike/models/research/object_detection/test_images'
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 3) ]

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

def run_inference_for_single_image(image, graph):
    with graph.as_default():
        with tf.Session() as sess:
          # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
                'num_detections', 'detection_boxes', 'detection_scores',
                'detection_classes', 'detection_masks'
                ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                    tensor_name)
            if 'detection_masks' in tensor_dict:
                # The following processing is only for single image
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                    detection_masks, detection_boxes, image.shape[0], image.shape[1])
                detection_masks_reframed = tf.cast(
                    tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                # Follow the convention by adding back the batch dimension
                tensor_dict['detection_masks'] = tf.expand_dims(
                    detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

            # Run inference
            output_dict = sess.run(tensor_dict,
                                 feed_dict={image_tensor: np.expand_dims(image, 0)})

            # all outputs are float32 numpy arrays, so convert types as appropriate
            output_dict['num_detections'] = int(output_dict['num_detections'][0])
            output_dict['detection_classes'] = output_dict[
                'detection_classes'][0].astype(np.uint8)
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
            output_dict['detection_scores'] = output_dict['detection_scores'][0]
            if 'detection_masks' in output_dict:
                output_dict['detection_masks'] = output_dict['detection_masks'][0]
    return output_dict

config = {
  "apiKey": None,
  "authDomain": None,
  "databaseURL": "firebase url",
  "storageBucket": None
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def checking_mamaro(id):
    ress=""
    # try:
    all_users = db.child("camera").child(str(id)).child().order_by_child("time").get()
    nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cou=0
    recou=0
    kecou=0
    check=False
    for user in all_users.each():
        #print(user.key())
        d = json.dumps(user.val())
        decoded = json.loads(d)
        #print(decoded["time"])
        d1 = datetime.strptime(decoded["time"], '%Y-%m-%d %H:%M:%S')

        tmpfolder=d1.strftime('%Y%m%d')
        os.makedirs(os.getcwd()+"/mamaro_cam/"+str(id)+"/"+str(tmpfolder), exist_ok=True)

        tmpfilename=d1.strftime('%Y%m%d%H%M%S')
        urllib.request.urlretrieve(decoded["imgurl"], os.getcwd()+"/mamaro_cam/"+str(id)+"/"+str(tmpfolder)+"/"+str(tmpfilename)+".jpg")
        ress=str(os.getcwd()+"/mamaro_cam/"+str(id)+"/"+str(tmpfolder)+"/"+str(tmpfilename)+".jpg")
        cou+=1

    ress="total download:"+str(cou)
    # except:
    #     ress="id:"+str(id)+",fail checking."
    return ress

def checking_person(folder_path):
    ress=""
    couu=0
    hcouu=0
    filelist=os.listdir(folder_path)
    os.makedirs(folder_path+"_1/res/", exist_ok=True)
    os.makedirs(folder_path+"_1/res_human/", exist_ok=True)

    #print(os.listdir(folder_path))
    for image_path_img in filelist:
        couu+=1
        startTime = time.time()
        #print(folder_path+"/"+image_path)

        image_path=folder_path+"/"+image_path_img

        image = Image.open(image_path)
        #print(image.size)
        img=cv2.imread(image_path)
        height, width, channels = img.shape
        #print(height)
        #print(width)
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        image_np = load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Actual detection.
        output_dict = run_inference_for_single_image(image_np, detection_graph)
        #print(output_dict['detection_boxes'])
        checkhuman=False

        for i in range(len(output_dict['detection_classes'])):
            if output_dict['detection_classes'][i]==1:
                if output_dict['detection_scores'][i]>0.9:
                    checkhuman=True
                    #print(i)
                    #print(output_dict['detection_scores'][i])
                    cv2.rectangle(img, (int(round(output_dict['detection_boxes'][i][1]*image.size[0])),
                     int(round(output_dict['detection_boxes'][i][0]*image.size[1]))), (int(round(output_dict['detection_boxes'][i][3]*image.size[0])),
                     int(round(output_dict['detection_boxes'][i][2]*image.size[1]))), (255,0,0), 2)
        if checkhuman:
            hcouu+=1
            cv2.imwrite(folder_path+"_1/res_human/"+image_path_img,img)
            print(folder_path+"_1/res_human/"+image_path_img)
            vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    output_dict['detection_boxes'],
                    output_dict['detection_classes'],
                    output_dict['detection_scores'],
                    category_index,
                    instance_masks=output_dict.get('detection_masks'),
                    use_normalized_coordinates=True,
                    line_thickness=8)
            plt.figure(figsize=IMAGE_SIZE)
            plt.imshow(image_np)
            endind=image_path_img.rfind('.')
            plt.savefig(folder_path+"_1/res/"+image_path_img[:endind]+".png")
            print(folder_path+"_1/res/"+image_path_img[:endind]+".png")
        else:
            print("nothing")

        endTime = time.time()
        print ("time :", endTime - startTime)



    ress="finished : total:"+str(couu)+",have human:"+str(hcouu)
    return ress


if __name__ == "__main__":
    id=38
    nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(nowdatetime)
    #print(checking_mamaro(38))
    #print([x[0] for x in os.walk(os.getcwd()+"/mamaro_cam/"+str(id)+"/")])
    subdir=[x[0] for x in os.walk(os.getcwd()+"/mamaro_cam/"+str(id)+"/")]
    path=subdir[1]
    print(checking_person(path))
    print(nowdatetime)
    nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(nowdatetime)

# # image_path='/home/mike/models/research/object_detection/test_images/image2.jpg'
# #image_path='/home/mike/桌面/test/setup_command/testimg/maxresdefault.jpg'
# #image_path='/home/mike/桌面/test/setup_command/testimg/Street.jpg'
# image_path='/home/mike/桌面/test/setup_command/testimg/testimg.jpg'
#
# image = Image.open(image_path)
# #print(image.size)
# img=cv2.imread(image_path)
# height, width, channels = img.shape
# #print(height)
# #print(width)
# # the array based representation of the image will be used later in order to prepare the
# # result image with boxes and labels on it.
# image_np = load_image_into_numpy_array(image)
# # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
# image_np_expanded = np.expand_dims(image_np, axis=0)
# # Actual detection.
# output_dict = run_inference_for_single_image(image_np, detection_graph)
# #print(output_dict['detection_boxes'])
#
# for i in range(len(output_dict['detection_classes'])):
#     if output_dict['detection_classes'][i]==1:
#         if output_dict['detection_scores'][i]>0.9:
#             #print(i)
#             #print(output_dict['detection_scores'][i])
#             cv2.rectangle(img, (int(round(output_dict['detection_boxes'][i][1]*image.size[0])),
#              int(round(output_dict['detection_boxes'][i][0]*image.size[1]))), (int(round(output_dict['detection_boxes'][i][3]*image.size[0])),
#              int(round(output_dict['detection_boxes'][i][2]*image.size[1]))), (255,0,0), 2)
#
# cv2.imwrite("test1.png",img)
#
# endTime = time.time()
# print ("time :", endTime - startTime)

# for image_path in TEST_IMAGE_PATHS:
#     image = Image.open(image_path)
#     # the array based representation of the image will be used later in order to prepare the
#     # result image with boxes and labels on it.
#     image_np = load_image_into_numpy_array(image)
#     # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
#     image_np_expanded = np.expand_dims(image_np, axis=0)
#     # Actual detection.
#     output_dict = run_inference_for_single_image(image_np, detection_graph)
#     print(output_dict)
#     # Visualization of the results of a detection.
#     vis_util.visualize_boxes_and_labels_on_image_array(
#         image_np,
#         output_dict['detection_boxes'],
#         output_dict['detection_classes'],
#         output_dict['detection_scores'],
#         category_index,
#         instance_masks=output_dict.get('detection_masks'),
#         use_normalized_coordinates=True,
#         line_thickness=8)
#     plt.figure(figsize=IMAGE_SIZE)
#     plt.imshow(image_np)
#     plt.savefig('test.png')
