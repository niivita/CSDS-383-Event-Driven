import json
import boto3

dynamodb = boto3.client('dynamodb')

# used to add event and view events
def handler(event, context):
    print(event)
    #print(event['queryStringParameters'])

    table_name = 'Events'
    
    # if the request is to add an event
    if event.get('queryStringParameters') is not None:
        
        #ADDING EVENT to DynamoDB
        event_data = {
            'eventID': {'S': event['queryStringParameters']['eventID']},
            'date': {'S': event['queryStringParameters']['date']},
            'time': {'S': event['queryStringParameters']['time']},
            'title': {'S': event['queryStringParameters']['title']},
            'description': {'S': event['queryStringParameters']['description']},
            'host_email': {'S': event['queryStringParameters']['email']}
        }
        
        # Put the item in the Events table
        response = dynamodb.put_item(
            TableName=table_name,
            Item=event_data,
            ConditionExpression='attribute_not_exists(eventID)'
        )
        
        # Check if the operation was successful
        if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
            message = 'Added Event with EventID: {}, date: {}, time: {}, title: {}, description: {}, and email: {}'.format(
                event['queryStringParameters']['eventID'],
                event['queryStringParameters']['date'],
                event['queryStringParameters']['time'],
                event['queryStringParameters']['title'],
                event['queryStringParameters']['description'],
                event['queryStringParameters']['email']
            )
        else:
            message = 'Failed to add the event to DynamoDB'

        print(message)
        
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body":  json.dumps({
                "message" : message
            })
            
        }
    # otherwise, return events 
    else:
        try:
            response = dynamodb.scan(
                TableName=table_name
            )
            items = response.get('Items', [])
            
            data = []
            for item in items:
                formatted_item = {
                    'EventID': item['eventID']['S'],
                    'Title': item['title']['S'],
                    'Description': item['description']['S'],
                    'Date': item['date']['S'],
                    'Time': item['time']['S'],
                    'Email': item['host_email']['S']
                }
                data.append(formatted_item)
            
            # IMPLEMENTING RETRIEVING ALL EVENTS from DynamoDB 
            return {
                'statusCode': 200,
                "headers": {
                        "Access-Control-Allow-Headers" : "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                    },
                'body': json.dumps(data)
            }
        except Exception as E:
            return {
                'statusCode': 500,
                'body': str(E)
            }
        