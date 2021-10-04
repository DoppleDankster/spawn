#!/usr/bin/env python3
from typing import List, Dict, Optional, Sequence
import boto3
from mypy_boto3_ec2.service_resource import EC2ServiceResource, Instance


class EC2:
    def __init__(self, region_name):
        self.ec2 = boto3.resource("ec2", region_name=region_name)

    def get_instance(self, instance_id: str) -> Instance:
        """
        Return an ec2 instance object.

        Args:
        - instance_id: the ID of the ec2 instance

        Return:
        - Instance object

        Throw:
        - botocore.exception.ClientError
        """
        return self.ec2.Instance(instance_id)

    def get_instances(self) -> Sequence[Instance]:
        """
        Return The list of Spawn EC2 instances.

        Return:
        - list of Instance objects
        """
        filters = [{"Name": "tag:Type", "Values": ["Spawn"]}]
        instance_list = self.ec2.instances.filter(Filters=filters)
        return [self.get_instance(instance.id) for instance in instance_list]

    def create_instance(
        self,
        launch_template_name: str,
        launch_template_version: str,
        instance_type: str = None,
        tags: Sequence[dict] = None,
    ) -> Instance:
        """
        Create a new EC2 instance and start it.

        Args:
        - launch_template_name: the launch template name
        - instance_type: the size of the vm following the aws specifications:
        https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html

        - tags: list of dict specifying new tags to attach to the instance

        Return:
        - an ec2 Instance object

        Throw:
        - botocore.exception.ClientError
        """
        instances = self.ec2.create_instances(
            InstanceType=instance_type,
            LaunchTemplate={
                "LaunchTemplateName": launch_template_name,
                "Version": "$Default",
            },
            TagSpecifications=[{"ResourceType": "instance", "Tags": tags}],
            MaxCount=1,
            MinCount=1,
        )
        return list(instances)[0]
