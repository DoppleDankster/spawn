import json
from boto_layer import EC2, convert_tags_to_dict


def lambda_handler(event, context):

    params = event["body"]
    region_name = params["region"]
    ec2 = EC2(region_name)

    instances = ec2.get_instances()
    instances = [
        vm_to_json(instance)
        for instance in instances
        if instance.state["Name"] not in ["terminated", "terminating"]
    ]

    return {"statusCode": 200, "body": json.dumps({"result": instances})}


def vm_to_json(spawn_instance) -> dict:
    """
    Represent an EC2 instance as a json


    The json is of the shape:
    ```
    {
      "DNSZone": "i.datapred.com",
      "Size": "S",
      "DNSName": "myvm",
      "Personal": "False",
      "Template": "spawn_default_template:$latest",
      "Owner": "first.lastname",
      "Type": "Spawn",
      "aws:ec2launchtemplate:version": "4",
      "aws:ec2launchtemplate:id": "lt-0b72a59b8b100520c",
      "Name": "myvm",
      "id": "i-05123456789abcdef",
      "state": "stopped"
    }
    ```
    All the fields except the id and the state are extracted from the tags.

    Args:
        - spawn_instance: The boto instance object of a spawn EC2 instance

    Return:
        - json dict
    """

    output = convert_tags_to_dict(spawn_instance.tags)
    output["id"] = spawn_instance.id
    output["state"] = spawn_instance.state["Name"]
    output.pop("type", None)

    return output
