import boto3
import json

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('MT_serveres_test')

def __get_all_policy_number():
    response = table.scan()
    return response['Items']

def handler(event, context):
    person = __get_all_policy_number()
    return {
        'statusCode': 200,
        'body': json.dumps({
            'result': person
        })
    }
