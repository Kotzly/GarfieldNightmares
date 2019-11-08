from model import get_models
from keras.optimizers import Adam
import sys
from PIL import Image
import numpy as np
from os.path import join
import os

sys.path.append("../..")
import dataset

autoencoder, encoder, decoder = get_models(input_shape=(100, 100, 1), latent_dim=64)
print("Nº of parameters: {}".format(autoencoder.count_params()))

images = dataset.load_png_dataset(sample=100, resize=(300, 100), conversion="L", strip_mode="1x3")
images = (images/255).astype(np.float16)

from keras.losses import mean_squared_error, cosine
loss1 = cosine(autoencoder.layers[0].input, autoencoder.layers[-2].output)
loss2 = mean_squared_error(autoencoder.layers[0].input, autoencoder.layers[-2].output)
autoencoder.compile(metrics=["mse"], optimizer=Adam(lr=1e-4))
autoencoder.add_loss(loss1)
autoencoder.add_loss(loss2)
autoencoder.fit(images, images, epochs=10, batch_size=200)

try:
    os.mkdir("./examples")
except:
    pass
try:
    os.mkdir("./models")
except:
    pass
for i in np.random.choice(range(len(images)), 10, replace=False):
    x = images[i]
    x_img = (x.squeeze()*255).astype(np.uint8)
    Image.fromarray(x_img, "L").save(f"./examples/original_{i}.png")

    x = np.expand_dims(x, 0)
    y = autoencoder.predict(x)[0]
    y_img = (y.squeeze()*255).astype(np.uint8)
    Image.fromarray(y_img, "L").save(f"./examples/image_{i}.png")

model_folder = "./models/"
autoencoder.save(join(model_folder,"autoencoder.k"))
autoencoder.save(join(model_folder,"encoder.k"))
autoencoder.save(join(model_folder,"decoder.k"))
