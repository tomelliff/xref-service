#!/usr/bin/env python
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

table = dynamodb.Table('xref-service')

def add_system_gsi(table, system):
    table.update(
        AttributeDefinitions=[
            {
                'AttributeName': system,
                'AttributeType': 'S'
            }
        ],
        GlobalSecondaryIndexUpdates=[
            {
                'Create': {
                    'IndexName': '{}_system'.format(system),
                    'KeySchema': [
                        {
                            'AttributeName': system,
                            'KeyType': 'HASH'
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            }
        ]
    )

def delete_system_gsi(table, system):
    table.update(
        GlobalSecondaryIndexUpdates=[
            {
                'Delete': {
                    'IndexName': '{}_system'.format(system)
                }
            }
        ]
    )

#add_system_gsi(table, 'tp')

#delete_system_gsi(table, 'tp')
