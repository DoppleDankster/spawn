#!/usr/bin/env python3
import boto3
from typing import List, Dict, Optional


class Route53:
    def __init__(self, zone_name: str):

        self.route53 = boto3.client("route53")
        self.zone_name = self._format_zone_name(zone_name)
        self.zone_id = self._get_zone_id()

    def put(self, name: str, ipv4: str) -> Dict:
        """
        Create or Update a A type record on the specified zone.

        Args:
            name(str): The name of the A record
            ipv4(str): The IPv4 to bind with the A record

        Return:
            dict: The response from route53 as a dict
        """
        record_name = f"{name}.{self.zone_name}"
        payload = self._generate_batch_payload("UPSERT", record_name, ipv4)
        response = self.route53.change_resource_record_sets(
            HostedZoneId=self.zone_id, ChangeBatch=payload
        )

    def delete(self, name: str) -> Dict:
        """
        Delete a A type record on the specified zone.


        Args:
            name(str): The name of the A record

        Return:
            dict: The response from route53 as a dict or None if the record
            doesn't exists to begin with.
        """
        record = self.get(name)
        if record == []:
            return

        record_name = record["Name"]
        record_ip = record["ResourceRecords"][0]["Value"]
        payload = self._generate_batch_payload(
            "DELETE", record_name, record_ip
        )
        return self.route53.change_resource_record_sets(
            HostedZoneId=self.zone_id, ChangeBatch=payload
        )

    def get(self, name: str) -> Optional[Dict]:
        """
        Check if a record exists using it's name.

        Args:
            name: The value of the `A` record to look for

        Returns:
            None if no match dict if there is one.
        """
        paginator = self.route53.get_paginator("list_resource_record_sets")

        zone_records = list(paginator.paginate(HostedZoneId=self.zone_id))
        record_list = zone_records[0]["ResourceRecordSets"]
        query = list(
            filter(
                lambda elem: elem["Name"] == f"{name}.{self.zone_name}",
                record_list,
            )
        )
        if query == []:
            return None
        return query[0]

    def _get_zone_id(self) -> str:
        """
        Return the ID of a hosted zone on AWS.

        Returns:
            str: The hosted zone id
        """
        query = self.route53.list_hosted_zones()
        hosted_zones = query["HostedZones"]

        for zone in hosted_zones:
            if self.zone_name in zone["Name"]:
                zone_id = zone["Id"]
                return zone_id.split("/")[-1]
        raise ValueError(f"No such Hosted Zone {self.zone_name}")

    @staticmethod
    def _generate_batch_payload(action: str, name: str, ipv4: str) -> dict:

        """
        Return the required payload to perform modifications on a ROUTE53 record.

        Args:
            action(str): The Action to perform ex UPSERT | DELETE | CREATE
            name(str): Name of the A record to create/edit/delete
            ipv4(str): IPv4 to bind / unbind on the A record
        """
        return {
            "Changes": [
                {
                    "Action": action.upper(),
                    "ResourceRecordSet": {
                        "Name": name,
                        "Type": "A",
                        "SetIdentifier": "string",
                        "Weight": 100,
                        "TTL": 60,
                        "ResourceRecords": [
                            {"Value": ipv4},
                        ],
                    },
                }
            ]
        }

    @staticmethod
    def _format_zone_name(zone_name: str):
        """
        Formats the zone name to make sure it ends with a '.'
        """
        if zone_name[-1] != ".":
            zone_name += "."
        return zone_name
