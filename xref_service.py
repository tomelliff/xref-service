#!/usr/bin/env python
from __future__ import print_function
import json
import uuid

from botocore.exceptions import ClientError
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

table = dynamodb.Table('xref-service')

def create_new_key(table):
    global_id = uuid.uuid4()
    response = table.put_item(
        Item={
            'global': str(global_id)
        }
    )

    return global_id


def get_ids(table, system_object):
    if system_object['system'] == 'global':
        ids = _get_by_global_id(table, system_object['id'])
    else:
        ids = _get_by_system_id(table, system_object)

    return ids


def _get_by_global_id(table, global_id):
    response = table.get_item(
        Key={
            'global': global_id
        }
    )

    return response['Item']


def _get_by_system_id(table, system_object):
    system_name = system_object['system']
    system_id = system_object['id']
    response = table.query(
        IndexName='{}_system'.format(system_name),
        KeyConditionExpression=Key(system_name).eq(system_id)
    )

    return response['Items'][0]


def link_system_ids(table, system_object1, system_object2):
    if system_object1['system'] == 'global':
        global_id = system1['id']
    else:
        global_id = _get_by_system_id(table, system_object1)['global']

    changes = _link_system(table, global_id, system_object2['system'],
                           system_object2['id'])

    return changes


def _link_system(table, global_id, system, system_id):
    response = table.update_item(
        Key={
            'global': global_id
        },
        UpdateExpression='set {} = :v'.format(system),
        ExpressionAttributeValues={':v': system_id},
        ReturnValues='ALL_NEW'
    )

    return response['Attributes']


def delete_id(table, system_object):
    if system_object['system'] == 'global':
        _delete_global_id(table, system_object['id'])
    else:
        global_id = _get_by_system_id(table, system_object)['global']
        _delete_system_id(table, global_id, system_object['system'])


def _delete_global_id(table, global_id):
    try:
        response = table.delete_item(
            Key={
                'global': global_id
            },
            ConditionExpression="attribute_not_exists(m3) and attribute_not_exists(tp)",
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise


def _delete_system_id(table, global_id, system):
    response = table.update_item(
        Key={
            'global': global_id
        },
        UpdateExpression='REMOVE {}'.format(system),
        ReturnValues='ALL_NEW'
    )

    return response['Attributes']


def get_specific_id(table, system_object1, system_wanted):
    id = get_ids(table, system_object1)[system_wanted]

    return id


#print(create_new_key(table))

system1 = {'system': 'global', 'id': 'eb4e8ee4-bc85-4848-b389-3b0763ed318f'}
system2 = {'system': 'm3', 'id': '6666'}
system3 = {'system': 'global', 'id': '572b21aa-07fd-4349-a621-abe3b9bd1a40'}
system4 = {'system': 'tp', 'id': '1235'}
system5 = {'system': 'tp', 'id': '1236'}

#print(link_system_ids(table, system1, system2))
#print(link_system_ids(table, system2, system5))

#delete_id(table, system2)

#print(get_specific_id(table, system4, 'm3'))


#print(get_ids(table, system1))
