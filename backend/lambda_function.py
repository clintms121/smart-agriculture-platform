import json


def lambda_handler(event, context):
    """
    This will process IoT messages and insert into RDS
    Test it locally to understand the logic
    """

    print("Received event:", json.dumps(event))

    sensor_id = event.get('sensor_id')
    reading_value = event.get('reading_value')

    # Simulate what will happen in AWS
    print(f"Would insert: sensor_id={sensor_id}, value={reading_value}")

    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }


# Test locally
if __name__ == "__main__":
    test_event = {
        "sensor_id": 1,
        "reading_value": 45.5,
        "timestamp": 1234567890
    }

    result = lambda_handler(test_event, None)
    print("Lambda result:", result)