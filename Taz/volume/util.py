from datetime import datetime 
import boto3
from datetime import timedelta
import requests
import json

def shouldTerminate(creation_date, day):
    if creation_date is not None:
        creation_dt1 = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S')
        current_Date = datetime.utcnow()
        #print ('current_date', creation_dt1)
        notification_date = current_Date + timedelta(days=day)
        #print ('Delta= ',notification_date)
        if notification_date > creation_dt1:
            return True
        else:
            #print('don`t terminate it yet!')
            return False
    else:
        print("creation date is set to None")


def exlude_volume(snapshot_name):
    if "Pipeline Generator Agent" in snapshot_name or "jenkins-maven-cache" in snapshot_name:
        return True
    else:
        return False


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
def aws_backup(tags):
    if tags is not None:
            for tag in tags:
                if tag['Key'] == 'aws:backup:source-resource':
                    return True
    else:
        return False

def imp_volumes(tags):
    if tags is not None:
        for tag in tags:
            if tag['Value'] == 'Pipeline Generator Agent' or tag['Value'] == 'jenkins-maven-cache':
                return True
    else:
        return False
def volume_name_fetch(tags):
    if tags is not None:
        for tag in tags:
            if tag['Key'] == 'Name':
                return tag['Value']
            
    else:
        return "No Name"
def active(tags):
    if tags is not None:
        for tag in tags:
            if tag['Value'] == 'active' and tag['Value'] == 'true':
                return True
    else:
        return False


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
    slack_token = 'xxxx'
    user_id = 'Cleanup Bot'
    url = 'https://slack.com/api/chat.postMessage'
    # channel = "xxx" #channel_name is daily_ops_report
    channel = "xxx"  # channel_name is cleanup_governance
    #channel = "xxxxx" # channel dddd
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
                 "color": "blue",
                # "title": title,
                "text": message,
            }
        ])
         ),
        ('channel', channel)
         #('icon_emoji', ':pencil2:')
    ]
    response = requests.post(url, data, headers)
    print(response.text)
