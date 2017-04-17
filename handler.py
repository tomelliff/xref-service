import json
import os

import boto3

import xref_service

dynamodb = boto3.resource('dynamodb')

table_name=os.environ['DYNAMODB_TABLE']

table = dynamodb.Table(table_name)

def get_ids(event, context):
    path_parameters = event['pathParameters']
    system = path_parameters['system1']
    system_id = path_parameters['system1_id']
    system_object = {'system': system, 'id': system_id}

    ids = xref_service.get_ids(table, system_object)

    response = {
        "statusCode": 200,
        "body": json.dumps(ids)
    }

    return response


def new_global_id(event, context):
    global_id = xref_service.create_new_key(table)

    response = {
        "statusCode": 200,
        "body": json.dumps(global_id)
    }

    return response


def link_system_ids(event, context):
    path_parameters = event['pathParameters']
    system1 = path_parameters['system1']
    system1_id = path_parameters['system1_id']
    system_object1 = {'system': system1, 'id': system1_id}
    system2 = path_parameters['system2']
    system2_id = path_parameters['system2_id']
    system_object2 = {'system': system2, 'id': system2_id}

    changes = xref_service.link_system_ids(table, system_object1,
                                           system_object2)

    response = {
        "statusCode": 200,
        "body": json.dumps(changes)
    }

    return response


def delete_id(event, context):
    path_parameters = event['pathParameters']
    system = path_parameters['system1']
    system_id = path_parameters['system1_id']
    system_object = {'system': system, 'id': system_id}

    ids = xref_service.delete_id(table, system_object)

    response = {
        "statusCode": 200
    }

    return response
