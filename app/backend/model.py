# tensorFlow packages
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dropout, Dense, GlobalMaxPool2D, Conv2D
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.layers import Concatenate
from tensorflow.keras.layers import Layer

# Transformers packages

from transformers import TFCamembertModel, TFBertModel
from .preprocessing import model_bert, model_camembert, MAX_LEN


# Model text ML Bert
def build_bert(max_len=MAX_LEN):
    input_ids = Input(shape=(MAX_LEN,), name='input_ids_bert', dtype='int32')
    attention_mask = Input(shape=(MAX_LEN,), name='attention_mask_bert', dtype='int32')

    transformer = TFBertModel.from_pretrained(model_bert)
    embedding_layer = transformer([input_ids, attention_mask])[0]
    seq_output = embedding_layer[:, 0, :]

    # Freeze des layers
    for layer in transformer.layers:
        layer.trainable = True

    return Model(inputs=[input_ids, attention_mask], outputs=seq_output)


# Model text Camembert

def build_camembert(max_len=MAX_LEN):
    input_ids = Input(shape=(MAX_LEN,), name='input_ids_cam', dtype='int32')
    attention_mask = Input(shape=(MAX_LEN,), name='attention_mask_cam', dtype='int32')

    transformer = TFCamembertModel.from_pretrained(model_camembert)
    embedding_layer = transformer([input_ids, attention_mask])[0]
    seq_output = embedding_layer[:, 0, :]

    # Freeze des layers
    for layer in transformer.layers:
        layer.trainable = True

    return Model(inputs=[input_ids, attention_mask], outputs=seq_output)


# Model Image
def build_resnet():
    shape = (224, 224, 3)
    base_model = ResNet50V2(weights='imagenet', include_top=False, input_shape=shape)
    base_model.trainable = True  # fine tune

    inputs = Input(shape=shape, name='input_im')
    resnet = base_model(inputs, training=True)
    conv2d = Conv2D(filters=768, kernel_size=3, padding='same')(resnet)

    reduce_dim = GlobalMaxPool2D(name='reduce_dim')(conv2d)

    return Model(inputs=inputs, outputs=reduce_dim)


# Création d'un ensemble: va gérer le poids de chaque modèles pur la concaténation
class LinearW(Layer):

    def __init__(self):
        super(LinearW, self).__init__()

    def build(self, input_shape):
        self.W = self.add_weight(
            shape=(1, 1, len(input_shape)),
            initializer='uniform',
            dtype=tf.float32,
            trainable=True, name='weighted_layer')

    def call(self, inputs):
        # inputs is a list of tensor of shape [(n_batch, n_feat), ..., (n_batch, n_feat)]
        # expand last dim of each input passed [(n_batch, n_feat, 1), ..., (n_batch, n_feat, 1)]
        inputs = [tf.expand_dims(i, -1) for i in inputs]
        inputs = Concatenate(axis=-1)(inputs)  # (n_batch, n_feat, n_inputs)
        weights = tf.nn.softmax(self.W, axis=-1)  # (1,1,n_inputs)
        # weights sum up to one on last dim

        return tf.reduce_sum(weights * inputs, axis=-1)  # (n_batch, n_feat)


def final_model():
    model_img = build_resnet()
    model_bert = build_bert()
    model_camembert = build_camembert()
    merged = LinearW()([model_img.output, model_bert.output, model_camembert.output])  # concatenation des trois models
    model_out = Dense(256, activation='relu', name='dense_1')(merged)
    model_out = Dropout(0.2, name='dropout_1')(model_out)
    model_out = Dense(128, activation='relu', name='dense_2')(model_out)
    model_out = Dropout(0.2, name='dropout_2')(model_out)
    model_out = Dense(27, activation='softmax', name='classifer')(model_out)
    return Model([model_img.input, model_bert.input, model_camembert.input], model_out)  ## Final layer


def create_model():
    model = final_model()
    model.load_weights('app/backend/Model_Bert_Resnet.h5')

    return model
