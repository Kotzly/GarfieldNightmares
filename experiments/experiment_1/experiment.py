from model import get_models
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
import sys
from PIL import Image
import numpy as np
from os.path import join
import os
from keras.utils import Sequence
import matplotlib.pyplot as plt
from nightmares.images_defines import EXPERIMENTS_FOLDER
from nightmares import dataset
import warnings
warnings.simplefilter("ignore")

autoencoder, encoder, decoder = get_models()
print("Nº of parameters: {}".format(autoencoder.count_params()))

images = dataset.load_png_dataset(sample=2000, resize=(360, 120), conversion="RGB", strip_mode="1x3")
plt.imshow(images[0])
plt.show()

class Generator(Sequence):
  def __init__(self, imgs):
    self.images = np.float16(imgs)/255
  def __len__(self):
    return len(self.images)//100
  def __getitem__(self, i):
    return self.images[i*100:(i+1)*100], None

train_generator = Generator(images)

epochs = 200
batch_size = 100
mc = ModelCheckpoint(join(EXPERIMENTS_FOLDER, "experiment_1", "models", "model.cpkt"))
callbacks = [mc]

models_folder = join(EXPERIMENTS_FOLDER, "experiment_1", "models")
examples_folder = join(EXPERIMENTS_FOLDER, "experiment_1", "examples")
try:
    os.mkdir(examples_folder)
except:
    pass
try:
    os.mkdir(models_folder)
except:
    pass

autoencoder.fit_generator(train_generator, shuffle=True, epochs=epochs, steps_per_epoch=len(train_generator), verbose=1, callbacks=callbacks)

for i in np.random.choice(range(len(images)), 10, replace=False):
    x_img = images[i]
    Image.fromarray(x_img, "RGB").save(join(examples_folder, f"original_{i}.png"))
    
    x_input = np.float16(x_img)/255
    x_input = np.expand_dims(x, axis=0)
    y = autoencoder.predict(x_input)
    y_img = np.uint8(y[0]*255)
    Image.fromarray(y_img, "RGB").save(join(examples_folder, f"image_{i}.png"))
    
autoencoder.save(join(models_folder,"autoencoder.k"))
encoder.save(join(models_folder,"encoder.k"))
decoder.save(join(models_folder,"decoder.k"))
