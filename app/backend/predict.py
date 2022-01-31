from app import model
from .preprocessing import encode, preprocess_sentence, tokenizer_cam, tokenizer_bert, MAX_LEN, make_test
import pandas as pd
import numpy as np


# Real func
def predict(df):
    df['text'] = df.text.apply(lambda x: preprocess_sentence(x))
    text_input_ids_bert, text_attention_masks_bert = encode(df.text.values, tokenizer_bert, maxlen=MAX_LEN)
    text_input_ids_cam, text_attention_masks_cam = encode(df.text.values, tokenizer_cam, maxlen=MAX_LEN)
    image = df.filename.values
    dataset = make_test(image,
                        text_input_ids_bert,
                        text_attention_masks_bert,
                        text_input_ids_cam,
                        text_attention_masks_cam)
    print(dataset)
    y_pred = model.predict(dataset)

    return y_pred


def save_to_csv(df, pred):
    pred_class = np.argpartition(pred, -3, axis=1)[:, -3:]
    pred_class = np.fliplr(pred_class)
    print(pred_class)
    result = pd.DataFrame(pred_class, columns=["Cat_1", "Cat_2", "Cat_3"])
    result = pd.concat([df, result], axis=1)
    result.to_csv('app/predictions/results.csv', encoding='utf-8', index=False, header='True')
    return result
