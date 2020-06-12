import json
import boto3


def get_latest_centos_ami(aws_region):
    """ Grab the lastest CentOS AMI using AWS API """

    EC2 = boto3.client('ec2', region_name=aws_region)
    response = EC2.describe_images(
        Owners=['679593333241'], # CentOS Owner ID
        Filters=[
          {'Name': 'name', 'Values': ['CentOS Linux 7 x86_64 HVM EBS *']},
          {'Name': 'architecture', 'Values': ['x86_64']},
          {'Name': 'root-device-type', 'Values': ['ebs']},
        ],
    )
    
    amis = sorted(response['Images'],
                  key=lambda x: x['CreationDate'],
                  reverse=True)
    return str(amis[0]['ImageId'])


class FilterModule(object):

    def filters(self):
        return { 'get_latest_centos_ami': get_latest_centos_ami, }
