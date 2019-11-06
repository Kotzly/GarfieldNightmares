from keras.layers import Reshape, Dense, Input, Flatten 
from keras.models import Model
import numpy as np

def get_models(input_shape, latent_dim=2):
    flat = Flatten()
    encoder_1 = Dense(units=128, activation="relu", name="encoder_1")
    latent = Dense(units=latent_dim, activation="relu", name="latent")
    decoder_1 = Dense(units=128, activation="relu", name="decoder_1")
    decoder_output = Dense(units=np.prod(input_shape), activation="sigmoid", name="output")
    output_reshape = Reshape(input_shape)

    autoencoder_input = Input(shape=input_shape, name="autoencoder_input")    
    autoencoder_flat = flat(autoencoder_input)
    autoencoder_enc_1 = encoder_1(autoencoder_flat)
    autoencoder_latent = latent(autoencoder_enc_1)
    autoencoder_dec_1 = decoder_1(autoencoder_latent)
    autoencoder_dec_out = decoder_output(autoencoder_dec_1)
    autoencoder_output = output_reshape(autoencoder_dec_out)

    encoder_input = Input(shape=input_shape, name="encoder_input")
    encoder_flat = flat(encoder_input)
    encoder_enc_1 = encoder_1(encoder_flat)
    encoder_output = latent(encoder_enc_1)

    decoder_input = Input(shape=(latent_dim,), name="decoder_input")
    decoder_dec = decoder_1(decoder_input)
    decoder_output_flat = decoder_output(decoder_dec)
    decoder_output = output_reshape(decoder_output_flat)
    
    autoencoder = Model(inputs=autoencoder_input, outputs=autoencoder_output)
    encoder = Model(inputs=encoder_input, outputs=encoder_output)
    decoder = Model(inputs=decoder_input, outputs=decoder_output)

    return autoencoder, encoder, decoder
