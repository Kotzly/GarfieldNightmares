# Experiments

In this folder are the experiments runned during the project.
The protocol described here is subject to changes.

Each experiment consists of:

* model.py : a .py file with a get_models function that returns (autoencoder, encoder, decoder) in case of a AE, or (generator, discriminator) in case of a GAN, or else.
* info.json : a .json file containing some info about the experiment: kind ("AE", "VAE", "GAN", others), n_models (number of models returned by get_models), models_names (names of the models returned), description (string), date (DD/MM/YYYY), time ("MM:HH:SS").
* ./examples : a folder with some examples of the generated images. In this folder the images can be named "image_1.png" etc.
* ./models :  a folder containing the models returned by get_models.
* experiment.py : .py file that runs the experiment.
* run.py : .py file that creates the .md for the experiment with `python run.py md`, run the experiment.py file with `python run.py experiment`.

By now the experiments runned are:

* Example : ![alt text](./example/examples/image_3257 "Logo Title Text 1")
