import boto3
import json
import datetime
from datetime import datetime
from datetime import timedelta
from httplib2 import Http
import requests, json

def getAssume_roleSession(resource_name,role_arn):
    sts_client = boto3.client('sts')
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="AssumeRoleSession1"
    )
    credentials = assumed_role_object['Credentials']
    resource = boto3.client(
        resource_name,
        region_name='eu-west-1',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )
    return resource

def sendslacknotification(message):
    slack_token = 'xoxb-xxxxxxxxxxx-xxxxxx-xxx'
    user_id = 'Cleanup Bot'
    url = 'https://slack.com/api/chat.postMessage'
    # channel = "xxx" #channel_name is daily_ops_report
     channel = "xxx"  # channel_name is cleanup_governance
    #channel = "xxxx" # channel_name is dddd
    # title = '@here :bangbang: Check this out'
    headers = {'content-type': 'application/json'}
    data = [
        ('token', slack_token),
        ('username', user_id),
        # ('as_user', 'false'),
        ('link_names', 1),
        # ('text', title),
        ('attachments', json.dumps([
            {
                "fallback": "Required plain-text summary of the attachment.",
                # "color": "blue",
                # "title": title,
                "text": message,
            }
        ])
         ),
        ('channel', channel)
        # ('icon_emoji', ':pencil2:')
    ]
    response = requests.post(url, data, headers)
    print(response.text)

def exclude_ami(ami):
    if "Pipeline" in ami or "Jenkins" in ami or "jenkins" in ami or "CICD" in ami or "cicd" in ami:
        return True
    else:
        return False

def shouldTerminate(creation_date, day):
    if creation_date is not None:
        creation_dt1 = datetime.strptime(creation_date, '%Y-%m-%dT%H:%M:%S.%fz')
        current_Date = datetime.utcnow()
        #print ('current_date', current_Date)
        notification_date = current_Date + timedelta(days=day)
        #print ('Delta= ',notification_date)
        if notification_date > creation_dt1:
            return True, creation_dt1
        else:
            #print('don`t terminate it yet!')
            return False, creation_dt1
    else:
        print("creation date is set to None")

def tag_check_always_true(tags):
        if tags is not None:
            for tag in tags:
                if tag['Key'] == 'exclude' and tag['Value'] == 'always-true':
                    return True
        else:
            return False
def tag_check_only_true(tags):
    if tags is not None:
            for tag in tags:
                if tag['Key'] == 'exclude' and tag['Value'] == 'true':
                    return True
    else:
        return False
def active(tags):
    if tags is not None:
        for tag in tags:
            if tag['Key'] == 'active' and tag['Value'] == 'true':
                return True
    else:
        return False
