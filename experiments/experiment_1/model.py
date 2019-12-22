import numpy as np
from scipy.stats import norm
import json
from keras.layers import Input, Dense, Lambda, Flatten, Reshape, BatchNormalization
from keras.layers import Conv2D, Conv2DTranspose
from keras.models import Model
from keras.optimizers import Adam
from keras import backend as K
from keras import metrics

def get_models():
    """
    This script demonstrates how to build a variational autoencoder
    with Keras and deconvolution layers.
    # Reference
    - Auto-Encoding Variational Bayes
    https://arxiv.org/abs/1312.6114
    """

    K.clear_session()

    ## Model hyperparameters
    # input image dimensions
    img_rows, img_cols, img_chns = 120, 120, 3
    filters = 32
    num_conv = 6
    latent_dim = 64
    intermediate_dim = 196
    epsilon_std = 1
    batch_size = 100
    config = dict(img_rows=120,
                  img_cols=120,
                  img_chns=3,
                  filters=32,
                  num_conv=6,
                  latent_dim=6,
                  intermediate_dim=196,
                  epsilon_std=1)
    with open("config.json", "w") as json_file:
        json.dump(config, json_file)
    ## Model instantiation
    if K.image_data_format() == 'channels_first':
        original_img_size = (img_chns, img_rows, img_cols)
    else:
        original_img_size = (img_rows, img_cols, img_chns)

    # Encoder layers instantiation
    x = Input(shape=original_img_size)
    conv_1 = Conv2D(img_chns,
                    kernel_size=(2, 2),
                    padding='same', activation='relu',
                    name="encod_conv_1")
    conv_2 = Conv2D(filters,
                    kernel_size=(2, 2),
                    padding='same', activation='relu',
                    strides=(2, 2),
                    name="encod_conv_2")
    conv_3 = Conv2D(filters,
                    kernel_size=num_conv,
                    padding='same', activation='relu',
                    strides=1,
                    name="encod_conv_3")
    conv_4 = Conv2D(filters,
                    kernel_size=num_conv,
                    padding='same', activation='relu',
                    strides=(2, 2),
                    name="encod_conv_4")


    flat = Flatten()

    # Model(x, flat).summary()
    hidden = Dense(intermediate_dim, activation='relu')

    z_mean = Dense(latent_dim)
    z_log_var = Dense(latent_dim, activation="sigmoid")

    def sampling(args):
        z_mean, z_log_var = args
        epsilon = K.random_normal(shape=(K.shape(z_mean)[0], latent_dim), mean=0., stddev=epsilon_std)
        return z_mean + K.exp(z_log_var) * epsilon


    # Variational inference modelling
    # note that "output_shape" isn't necessary with the TensorFlow backend
    # so you could write `Lambda(sampling)([z_mean, z_log_var])`
    z = Lambda(sampling, output_shape=(latent_dim,))

    # we instantiate these layers separately so as to reuse them later
    i = img_cols//4
    j = img_rows//4

    # Decoder instantiation
    decoder_hid = Dense(intermediate_dim, activation='tanh', name="decoder_hid")
    decoder_upsample = Dense(filters * i * j, activation='relu', name="decoder_upsample")

    if K.image_data_format() == 'channels_first':
        output_shape = (batch_size, filters, i, j)
    else:
        output_shape = (batch_size, i, j, filters)

    decoder_reshape = Reshape(output_shape[1:])

    decoder_deconv_1 = Conv2DTranspose(filters,
                                    kernel_size=num_conv,
                                    padding='same',
                                    strides=1,
                                    activation='relu',
                                    name="deconv_1")

    decoder_deconv_2_upsamp = Conv2DTranspose(filters,
                                            kernel_size=(3, 3),
                                            strides=(2, 2),
                                            padding='same',
                                            activation='relu',
                                            name="deconv_2_upsample")

    decoder_deconv_3 = Conv2DTranspose(filters,
                                    kernel_size=num_conv,
                                    padding='same',
                                    strides=1,
                                    activation='relu',
                                    name="deconv_3")

    decoder_deconv_4_upsamp = Conv2DTranspose(filters,
                                            kernel_size=(3, 3),
                                            strides=(2, 2),
                                            padding='valid',
                                            activation='relu',
                                            name="deconv_4_upsample")


    if K.image_data_format() == 'channels_first':
        output_shape = (batch_size, filters, img_rows, img_cols)
    else:
        output_shape = (batch_size, img_rows, img_cols, filters)
    decoder_mean_squash = Conv2D(img_chns,
                                kernel_size=2,
                                padding='valid',
                                activation='sigmoid',
                                name="decoder_squash")

    conv1 = conv_1(x)
    conv2 = conv_2(conv1)
    conv3 = conv_3(conv2)
    conv4 = conv_4(conv3)
    flattened = flat(conv4)
    hid = hidden(flattened)
    z_mean_tensor = z_mean(hid)
    z_log_var_tensor = z_log_var(hid)
    z_tensor = z([z_mean_tensor, z_log_var_tensor])

    hid_decoded = decoder_hid(z_tensor)
    up_decoded = decoder_upsample(hid_decoded)
    reshape_decoded = decoder_reshape(up_decoded)
    deconv_1_decoded = decoder_deconv_1(reshape_decoded)
    deconv_2_decoded = decoder_deconv_2_upsamp(deconv_1_decoded)
    deconv_3_decoded = decoder_deconv_3(deconv_2_decoded)
    x_decoded_relu = decoder_deconv_4_upsamp(deconv_3_decoded)
    x_decoded_mean_squash = decoder_mean_squash(x_decoded_relu)

    encoder = Model(x, hid_decoded)
    vae = Model(x, x_decoded_mean_squash)

    xent_loss =  K.sum(K.binary_crossentropy(K.flatten(x),
                                    K.flatten(x_decoded_mean_squash)))
    kl_loss = - 0.5 * K.sum(1 + z_log_var_tensor - K.square(z_mean_tensor) - K.exp(z_log_var_tensor), axis=-1)
    vae_loss = xent_loss + kl_loss

    vae.add_loss(vae_loss)
    
    vae.compile(optimizer=Adam(lr=1e-4), metrics=["mse", "binary_crossentropy"])
    vae.summary()
    
    decoder_input = Input(shape=(latent_dim,))
    _hid_decoded = decoder_hid(decoder_input)
    _up_decoded = decoder_upsample(_hid_decoded)
    _reshape_decoded = decoder_reshape(_up_decoded)
    _deconv_1_decoded = decoder_deconv_1(_reshape_decoded)
    _deconv_2_decoded = decoder_deconv_2_upsamp(_deconv_1_decoded)
    _deconv_3_decoded = decoder_deconv_3(_deconv_2_decoded)
    _x_decoded_relu = decoder_deconv_4_upsamp(_deconv_2_decoded)
    _x_decoded_mean_squash = decoder_mean_squash(_x_decoded_relu)
    generator = Model(decoder_input, _x_decoded_mean_squash)


    return vae, encoder, generator

    # def save_generator(epoch, logs):
    # try:
    #     os.mkdir("./experiment_checkpoints")
    # except:
    #     pass
    # generator.save("./experiment_checkpoints/generator.cpkt")

    # genc = LambdaCallback(on_epoch_end=save_generator)
    # lrs = LearningRateScheduler(sched)
    # mc = ModelCheckpoint("model.cpkt")
    # callbacks = [mc, genc]
    # vae.fit_generator(train_generator, shuffle=True, epochs=epochs, steps_per_epoch=len(train_generator), verbose=1, callbacks=callbacks)
