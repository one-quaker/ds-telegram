import boto3
import json
import sys
import os


aws_conf = dict()
aws_conf_fn = 'aws.json'


def write_json_conf(data, fp):
    with open(fp, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ': '), sort_keys=True)


if not os.path.isfile(aws_conf_fn):
    print(f'Please edit "{aws_conf_fn}"')
    write_json_conf(
        dict(
            aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
            aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY',
            region_name='eu-west-1',
            service_name='comprehend',
        ),
        aws_conf_fn
    )
    sys.exit()


with open(aws_conf_fn) as f:
    aws_conf = json.load(f)


if not aws_conf:
    print('Empty AWS credentials')
    sys.exit()


comprehend = boto3.client(**aws_conf)


comment_list = sys.argv[1:]
if len(sys.argv) == 1:
    print('Please add some text!!!\nFor example:\n{} {} "This movie is bad"'.format(sys.executable, sys.argv[0]))


for text in comment_list:
    json_resp = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    result = '{1} == {0}'.format(text, json_resp.get('Sentiment'))
    result = dict(
        text=text,
        sentiment=json_resp['Sentiment'],
        score=json_resp['SentimentScore'],
    )
    print(json.dumps(result))
