import os
#from RunTrain import BASE_DIR
#from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static

from simpletransformers.classification import MultiLabelClassificationModel, ClassificationModel

#modelFolder = static('multi')


def get_category(raw_outputs, threshold):
    """multi class"""
    # in future, when list: result = [1 if p > threshold else 0 for p in raw_outputs[0]]

    pred_dict_m = {2: 'Animals',
                   3: 'Environment',
                   1: 'People',
                   4: 'Politics',
                   5: 'Products & Services'}
    list_vals = list(raw_outputs[0])
    max_val = max(list_vals)
    if max_val > threshold:
        k = list_vals.index(max_val) + 1
        cat_id = k
        print('category is', pred_dict_m[k])
    else:
        cat_id = None
    return cat_id


def get_tendency(res):
    # tend_dict defined in ReplaceSentimentsWithIndexes
    tend_id_dict = {0: 1,  # id = 1  'negative', #id = 1
                    1: 3,  # id = 3 'controversial'
                    2: 2}  # id = 2 'positive'

    tend_name_dict = {0: 'negative',  # id = 1
                      1: 'controversial',
                      2: 'positive'}

    try:
        k = res.index(1)
        tend_id = tend_id_dict[k]
        print('tendency is', tend_name_dict[k])
    except ValueError:
        tend_id = 3  # controversial
    return tend_id


def multi_predict_text(text_m, model_path, threshold = 0.3):
    #Ideally the model wouldn't be loaded everytime someone predicts something, but kept in the GPU memory.

    algorithm = 'roberta'
    args = {
        'output_dir': model_path,
        'reprocess_input_data': True,
        'overwrite_output_dir': True,
        'num_train_epochs': 6,
        'silent': True,
        'use_cached_eval_features': False,
        'threshold': 0.5
    }
    model_saved = MultiLabelClassificationModel(algorithm, model_path, args=args, use_cuda=False)

    prediction, raw_outputs = model_saved.predict([text_m])
    print(text_m[:10])
    print(prediction)
    cat_id = get_category(raw_outputs, threshold)

    return cat_id


def sentiment_predict(text, model_path, threshold=0.5):
    algorithm = 'xlnet'

    args = {
        'output_dir': model_path,
        'reprocess_input_data': True,
        'overwrite_output_dir': True,
        'num_train_epochs': 5,
        'silent': True,
        'use_cached_eval_features': False,
    }
    model_saved = ClassificationModel(algorithm, model_path, args=args, use_cuda=False)

    prediction, raw_outputs = model_saved.predict([text])
    print(prediction)
    print(raw_outputs)

    result = [1 if p > threshold else 0 for p in raw_outputs[0]]
    tend_id = get_tendency(result)

    return tend_id


def analyze_text(text):
    cat_id = multi_predict_text(text)
    tend_id = sentiment_predict(text)
    return cat_id, tend_id


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _MODEL_DEF = os.path.join(BASE_DIR, 'prediki/static/prediki/model_data/')
    p_senti = os.path.join(_MODEL_DEF, 'sentiment')
    p_multi = os.path.join(_MODEL_DEF, 'multi')
    #cat_id = multi_predict_text('people')
    #tend_id = sentiment_predict('bad is bad is good. is actually very good. but they also killed people.')
    analyze_text('asd')

