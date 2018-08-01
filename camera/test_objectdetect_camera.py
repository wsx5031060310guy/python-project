import numpy as np
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
from datetime import datetime, timedelta, date
import scipy.misc
import matplotlib
matplotlib.use('Agg')

# 加入 OpenCV 模組
import cv2

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

print(tf.__version__)
if tf.__version__ < '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.0!')

# 建立 VideoCapture 物件
cap = cv2.VideoCapture(0)

# 設定擷取的畫面解析度
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

sys.path.append("/home/mike/models/research")

from object_detection.utils import label_map_util

from object_detection.utils import visualization_utils as vis_util

MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('/home/mike/models/research/object_detection/data', 'mscoco_label_map.pbtxt')
#PATH_TO_LABELS = os.path.join('/home/mike/models/research/object_detection/data', 'mscoco_label_map1.pbtxt')
NUM_CLASSES = 90

opener = urllib.request.URLopener()
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
tar_file = tarfile.open(MODEL_FILE)
for file in tar_file.getmembers():
  file_name = os.path.basename(file.name)
  if 'frozen_inference_graph.pb' in file_name:
    tar_file.extract(file, os.getcwd())

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

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    # 使用無窮迴圈，持續擷取網路攝影機影像
    while True:
      # 讀取一個影格
      ret, image_np = cap.read()
      height, width, channels = image_np.shape
      img = image_np.copy()

      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
      detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')
      image_np_expanded = np.expand_dims(image_np, axis=0)

      (boxes, scores, classes, num) = sess.run(
          [detection_boxes, detection_scores, detection_classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})

      #print(len(classes[0]))
      ####save to folder
      check=False
      # for i in range(len(classes[0])):
      #     if classes[0][i]==1:
      #         if scores[0][i]>0.4:
      #             check=True
      #             #print(i)
      #             #print(output_dict['detection_scores'][i])
      #             cv2.rectangle(img, (int(round(boxes[0][i][1]*width)),
      #              int(round(boxes[0][i][0]*height))), (int(round(boxes[0][i][3]*width)),
      #              int(round(boxes[0][i][2]*height))), (255,0,0), 2)
      # if check:
      #     tmpfilename=datetime.now().strftime('%Y%m%d%H%M%S%f')
      #     cv2.imwrite("./testrecord/"+tmpfilename+".jpg",img)

      vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=4)
      # 以 OpenCV 視窗即時顯示辨識結果
      cv2.imshow('object detection', image_np)
      if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
