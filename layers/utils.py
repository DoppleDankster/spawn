from typing import Sequence, Dict


def convert_tags_to_dict(tags: Sequence[Dict]) -> Dict:
    """
    Return a list of Instance tags into a dict
    """
    return_dict = {}
    for tag in tags:
        return_dict[tag["Key"]] = tag["Value"]
    return return_dict


def make_tags(tag_dict: dict) -> Sequence[Dict]:
    """
    Return the metadatas in tag format.

    The tag format is used to attach labels to an
    EC2 Instance at creation time.

    The data is represented as a list of dict of the shape
    {"Key":"somekey","Value":"somevalue"}

    Args:
        tag_dict: Key Value pair of tags to attach

    Returns:
        Sequence(dict): Tag formated labels
    """

    tags = [
        {"Key": "Type", "Value": "Spawn"},
    ]
    for key, value in tag_dict.items():
        tags.append({"Key": key, "Value": value})
    return tags
