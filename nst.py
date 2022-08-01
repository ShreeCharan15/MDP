import tensorflow as tf
import numpy as np
import PIL
import matplotlib.pyplot as plt
from matplotlib import gridspec
import tensorflow_hub as hub
import datetime
# import sys
import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
class NST:
  def __init__(self):
    # os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    if tf.test.gpu_device_name():
      print('GPU found')
    else:
        print("No GPU found")
    
    self.hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    print("Model loaded")

  def crop_center(self,image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape)
    return image

  def load_image(self,image_path, image_size=(256, 256), preserve_aspect_ratio=True,sameSize=False):
    """Loads and preprocesses images."""
    # Cache image file locally.
    # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
    img = tf.io.decode_image(
        tf.io.read_file(image_path),
        channels=3, dtype=tf.float32)[tf.newaxis, ...]
    # img = crop_center(img)
    shape=(image_size[0],image_size[1])
    if sameSize:
      image_size=img.shape
      shape=(image_size[1],image_size[2])
    print(shape)

    max_dim = 720
    long_dim = max(shape)
    scale = max_dim / long_dim
    print(scale)
    new_shape = tf.cast((shape[0]*scale,shape[1]*scale),tf.int32)
    print(new_shape)
    img = tf.image.resize(img, new_shape, preserve_aspect_ratio=True)
    return img

  def show_n(self,images, titles=('',)):
    n = len(images)
    image_sizes = [image.shape[1] for image in images]
    w = (image_sizes[0] * 6) // 320
    plt.figure(figsize=(w * n, w))
    gs = gridspec.GridSpec(1, n, width_ratios=image_sizes)
    for i in range(n):
      plt.subplot(gs[i])
      plt.imshow(images[i][0], aspect='equal')
      plt.axis('off')
      plt.title(titles[i] if len(titles) > i else '')
    plt.show()


  def tensor_to_image(self,tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
      assert tensor.shape[0] == 1
      tensor = tensor[0]
    return PIL.Image.fromarray(tensor)



  def convertImage(self,content_path,style_path,save_path):
    content_image,style_image = self.load_image(content_path,sameSize=True),self.load_image(style_path)
    print("Images loaded")
    style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')
    
    stylized_image = self.hub_model(tf.constant(content_image), tf.constant(style_image))[0]
    print("Transformeddd")
    fn=(os.path.basename(style_path).split('.')[0])+'_'+os.path.basename(content_path)
    print(style_path,content_path,fn)
    dest=save_path+'/'+fn
    self.tensor_to_image(stylized_image).save(dest)
    return dest


