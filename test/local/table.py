#!/usr/bin/env python
"""Create table locally and seed it with data

Should be using Serverless or something else to build real DynamoDB tables in
AWS.

"""

import argparse
import json
import random
import uuid

import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

TABLE_NAME = 'xref-service'
TEST_DATA_FILE = 'test_data.json'

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


def delete_table(dynamodb, table_name):
    table = dynamodb.Table(table_name)
    table.delete()


def add_test_data(dynamodb, table_name, test_data_file):
    with open(test_data_file, 'r') as file:
        test_data = json.load(file)

    dynamodb.batch_write_item(
        RequestItems=test_data
    )


def generate_test_data(table_name, test_data_file):
    m3_min_value = 100000
    m3_max_value = 999999
    tp_min_value = 1000
    tp_max_value = 9999

    test_data = {table_name: []}
    for _ in xrange(10):
        rand = random.randint(1, 10)
        item = {'global': str(uuid.uuid4())}
        if rand >= 2:
            item['m3'] = str(random.randint(m3_min_value, m3_max_value))
        if rand <= 7:
            item['tp'] = str(random.randint(tp_min_value, tp_max_value))

        put_request = {'PutRequest': {'Item': item}}
        test_data[table_name].append(put_request)

    with open(test_data_file, 'w') as file:
        json.dump(test_data, file, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Manage a local DynamoDB table')
    parser.add_argument('action', choices=['create', 'delete', 'populate', 'generate'])
    args = parser.parse_args()
    if args.action == 'create':
        create_table(dynamodb, TABLE_NAME)
    elif args.action == 'delete':
        delete_table(dynamodb, TABLE_NAME)
    elif args.action == 'populate':
        add_test_data(dynamodb, TABLE_NAME, TEST_DATA_FILE)
    elif args.action == 'generate':
        generate_test_data(TABLE_NAME, TEST_DATA_FILE)
