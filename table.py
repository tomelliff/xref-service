#!/usr/bin/env python
"""Create table locally and seed it with data

Should be using Serverless or something else to build real DynamoDB tables in
AWS.

"""

import argparse

import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

table_name = 'xref-service'

def create_table(dynamodb, table_name):
    dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'global',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'm3',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'tp',
                'AttributeType': 'S'
            }
        ],
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'global',
                'KeyType': 'HASH'
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'm3_system',
                'KeySchema': [
                    {
                        'AttributeName': 'm3',
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
            },
            {
                'IndexName': 'tp_system',
                'KeySchema': [
                    {
                        'AttributeName': 'tp',
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
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )


table = dynamodb.Table(table_name)


def delete_table(table):
    table.delete()


def add_test_data(table):
    raise NotImplementedError()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Manage a local DynamoDB table')
    parser.add_argument('action',  choices=['create', 'delete', 'populate'])
    args = parser.parse_args()
    if args.action == 'create':
        create_table(dynamodb, table_name)
    elif args.action == 'delete':
        delete_table(table)
    elif args.action == 'populate':
        add_test_data(table)
