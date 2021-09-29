#!/usr/bin/env python3
from typing import List, Dict, Optional
import boto3
from boto3.dynamodb.conditions import Key


class Dynamodb:
    def __init__(self, table_name: str):
        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(table_name)
        # Will raise instantly if the table is not accessible / does not exists
        self.table.load()

    def get(self, owner: str = None, name: str = None) -> Optional[List[Dict]]:
        """
        Return Spawn instances from the DynDb table.

        Results can be filetered using the instance name and owner.
        The filtering check if the fields `starts with` the passed value.

        Args:
            owner(str): The owner of the instance
            name(str): The name of the instance

        Return:
            A list of instance dict or None if there is no match.
        """
        query = {}

        if owner:
            query["FilterExpression"] = Key("owner").begins_with(owner)
        if name:
            query["FilterExpression"] = Key("name").begins_with(name)

        return self.table.scan(**query).get("Item")

    def put(self, instance_data: dict) -> Dict:
        """
        Post or Update an instance in the DynDb table.

        If an entry with the same instance_id already exists,
        then it will be overrided by the new data.

        Args:
            instance_data(dict): The Data to insert as a dict

        Returns:
            Dict: The response from dynamodb as a dict

        """
        return self.table.put_item(Item=instance_data)

    def delete(self, instance_id: str) -> Dict:
        """
        Delete an instance in the DynDb table.

        This operation is idempotent, deleting a non existing
        object yields no error because the result is the same.

        Args:
            instance_id(str): The instance_id of the instance to delete

        Returns:
            Dict: The response from dynamodb as a dict
        """
        return self.table.delete_item(Key={"instance_id": instance_id})
