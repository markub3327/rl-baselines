from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model

import tensorflow as tf
import tensorflow_probability as tfp


# Trieda hraca
class Actor:
    def __init__(self, model_path: str):

        # Nacitaj model
        self.model = load_model(model_path)
        print("Actor loaded from file succesful ... 😊")

        print(self.model.trainable_variables)

        self.model.summary()

        # get log_std layer
        self.noisy_l = self.model.get_layer(name='log_std')

        # Prenosova funkcia vystupnej distribucie
        self.bijector = tfp.bijectors.Tanh()

    @tf.function
    def predict(self, x, reset_noise=False, deterministic=False):
        mean, noise, latent_sde = self.model(x, reset_noise=reset_noise)
        print(mean)

        if deterministic:
            pi_action = mean  #  !! zabudol som na bijector pre testovanie rozsahu mean
        else:
            pi_action = self.bijector.forward(mean + noise)

        return pi_action

    def save(self):
        plot_model(self.model, to_file="img/model_A_SAC.png")

    def sample_weights(self):
        self.noisy_l.sample_weights()