from model import get_models
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
import sys
from PIL import Image
import numpy as np
from os.path import join
import os
from keras.utils import Sequence
sys.path.append("../..")
import dataset


autoencoder, encoder, decoder = get_models()
print("Nº of parameters: {}".format(autoencoder.count_params()))

images = dataset.load_png_dataset(sample=100, resize=(360, 120), conversion="RGB", strip_mode="1x3")
images = (images/255).astype(np.float16)

class Generator(Sequence):
  def __init__(self, imgs):
    self.images = np.float16(imgs/255)
  def __len__(self):
    return len(self.images)//100
  def __getitem__(self, i):
    return self.images[i*100:(i+1)*100], None

train_generator = Generator(images)

epochs = 200
batch_size = 100
mc = ModelCheckpoint(".models/model.cpkt")
callbacks = [mc]


try:
    os.mkdir("./examples")
except:
    pass
try:
    os.mkdir("./models")
except:
    pass

autoencoder.fit_generator(train_generator, shuffle=True, epochs=epochs, steps_per_epoch=len(train_generator), verbose=1, callbacks=callbacks)


for i in np.random.choice(range(len(images)), 10, replace=False):
    x = images[i]
    x_img = (x.squeeze()*255).astype(np.uint8)
    Image.fromarray(x_img, "RGB").save(f"./examples/original_{i}.png")

    y = autoencoder.predict(x)[0]
    y_img = (y.squeeze()*255).astype(np.uint8)
    Image.fromarray(y_img, "RGB").save(f"./examples/image_{i}.png")

model_folder = "./models/"
autoencoder.save(join(model_folder,"autoencoder.k"))
encoder.save(join(model_folder,"encoder.k"))
decoder.save(join(model_folder,"decoder.k"))
