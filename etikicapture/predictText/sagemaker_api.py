import json
import boto3
import botocore
import os



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


def sentiment_predict(text):

    endpoint_name = 'pytorch-inference-2020-09-24-13-42-26-455'
    content_type = 'application/json'  # The MIME type of the input data in the request body.
    accept = 'application/json'  # The desired MIME type of the inference in the response.

    body = {'text': text}
    body_json = json.dumps(body)

    aws_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_DEFAULT_REGION')

    client = boto3.client('sagemaker-runtime',
                          aws_access_key_id=aws_key_id,
                          aws_secret_access_key=aws_key,
                          region_name=aws_region
                          )
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        # CustomAttributes=custom_attributes,
        ContentType=content_type,
        Accept=accept,
        Body=body_json
    )

    resp_body = response['Body']
    if type(resp_body) == botocore.response.StreamingBody:
        resp_body = resp_body.read()
        resp_data = resp_body.decode('utf-8')
    else:
        resp_data = resp_body.data.decode('utf-8')

    print(resp_data)

    return resp_data


def analyze_text(text):
    cat_id = multi_predict_text(text)
    tend_id = sentiment_predict(text)
    return cat_id, tend_id


if __name__ == '__main__':
    from etikiptype1.settings.secrets import AWS_KEY_ID, AWS_KEY, AWS_REGION

    os.environ['AWS_ACCESS_KEY_ID'] = AWS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_KEY
    os.environ['AWS_DEFAULT_REGION'] = AWS_REGION

    txt = 'bad is bad is good. is actually very good. '
    sentiment_predict(txt)


