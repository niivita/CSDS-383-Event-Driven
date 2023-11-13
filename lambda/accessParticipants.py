import json
import boto3

dynamodb = boto3.client('dynamodb')

# used to add participants and view participants
def handler(event, context):
    print(event)
    
    table_name = 'Participants'
   
    # if the request is to add an participant 
    if event.get('queryStringParameters') is not None:
        # TODO: IMPLEMENT ADDING PARTICIPANT to DynamoDB
        
        # for testing invocation: (delete later)
        message = 'Adding Participant with participant_uuid: {}, event_uuid: {}, name: {}, and participant_email: {}'.format(event['queryStringParameters']['participantID'], event['queryStringParameters']['eventID'], event['queryStringParameters']['name'], event['queryStringParameters']['email'])  
        
        participant_data = {
            'participant_uuid': {'S': event['queryStringParameters']['participantID']},
            'event_uuid': {'S': event['queryStringParameters']['eventID']},
            'name': {'S': event['queryStringParameters']['name']},
            'participant_email': {'S': event['queryStringParameters']['email']}
        }
        
        response = dynamodb.put_item(
            TableName=table_name,
            Item=participant_data,
            ConditionExpression='attribute_not_exists(participant_uuid)'
        )
        
        
        if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
            message = 'Added Participant with participant_uuid: {}, event_uuid: {}, name: {}, participant_email: {}'.format(
                event['queryStringParameters']['participantID'],
                event['queryStringParameters']['eventID'],
                event['queryStringParameters']['name'],
                event['queryStringParameters']['email']
            )
        else:
            message = 'Failed to add the participant to DynamoDB'

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
    # otherwise, return participants 
    else:
        try:
            response = dynamodb.scan(
                TableName=table_name
            )
            items = response.get('Items', [])
            
            data = []
            for item in items:
                formatted_item = {
                    'participant_uuid': item['participant_uuid']['S'],
                    'event_uuid': item['event_uuid']['S'],
                    'name': item['name']['S'],
                    'participant_email': item['participant_email']['S']
                }
                data.append(formatted_item)
            
            # TODO: IMPLEMENT RETRIEVING ALL EVENTS from DynamoDB 
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
        
    