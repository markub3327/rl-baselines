from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Concatenate, Dense
from tensorflow.keras.utils import plot_model

# Trieda hraca
class Actor:

    def __init__(self, state_shape, action_shape, lr):
        state_input = Input(shape=state_shape, name='state_input')
        l1 = Dense(400, activation='relu', use_bias=True, kernel_initializer='he_uniform', name='h1')(state_input)
        l2 = Dense(300, activation='relu', use_bias=True, kernel_initializer='he_uniform', name='h2')(l1)
        
        # vystupna vrstva   -- musi byt tanh pre (-1,1) ako posledna vrstva!!!
        output = Dense(action_shape[0], activation='tanh', use_bias=True, kernel_initializer='glorot_uniform', name='action')(l2)

        # Vytvor model
        self.model = Model(inputs=state_input, outputs=output)

        # Skompiluj model
        self.optimizer = Adam(learning_rate=lr)

        self.model.summary()

    def save(self):
        plot_model(self.model, to_file='model_A.png')


# Trieda kritika
class Critic:

    def __init__(self, state_shape, action_shape, lr):
        # vstupna vsrtva
        state_input = Input(shape=state_shape, name='state_input')
        action_input = Input(shape=action_shape, name='action_input')

        merged = Concatenate()([state_input, action_input])
        l1 = Dense(400, activation='relu', use_bias=True, kernel_initializer='he_uniform', name='h1')(merged)
        l2 = Dense(300, activation='relu', use_bias=True, kernel_initializer='he_uniform', name='h2')(l1)

        # vystupna vrstva   -- musi byt linear ako posledna vrstva pre regresiu Q funkcie (-nekonecno, nekonecno)!!!
        output = Dense(1, activation='linear', use_bias=True, kernel_initializer='glorot_uniform', name='q_val')(l2)

        # Vytvor model
        self.model = Model(inputs=[state_input, action_input], outputs=output)

        # Skompiluj model
        self.optimizer = Adam(learning_rate=lr)

        self.model.summary()

    def save(self):
        plot_model(self.model, to_file='model_C.png')
