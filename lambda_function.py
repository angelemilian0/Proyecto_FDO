import json
import random

def lambda_handler(event, context):
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'random_number': random.randint(1, 100),
            'message': 'Microservicio Lambda funcionando correctamente.'
        })
    }
    return response

