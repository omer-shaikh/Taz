import boto3
import json
from datetime import datetime
from datetime import timedelta
from httplib2 import Http
import requests, json
import util
import configuration
from repo import terminateDBOperations
d = datetime.today()
db = terminateDBOperations()

################### CHECK LAST TIME AND INSERT INTO DATABASE #######################

def get_volume_qa(botoClient, msg, table):
    imp_volume=[]
    name=[]
    delete_volume={}
    response = botoClient.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']    
    for r in response:
        if 'Tags' in r:
            name=util.volume_name_fetch(r['Tags'])            
            if util.imp_volumes(r['Tags']):
                imp_volume.append(r['VolumeId'])
                print("This volume is important \n ")
                print(name)
            elif util.active(r['Tags']):
                imp_volume.append(r['VolumeId'])
                print("This volume is important \n ")
            elif util.shouldTerminate(str(r['CreateTime'])[:19],-1):
                
                if util.tag_check_always_true(r['Tags']) and util.shouldTerminate(str(r['CreateTime'])[:19],-10):
                 
                    delete_volume[r['VolumeId']]=name

                    if 'Iops' in r:
                        db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
                    else:
                        db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
                   
                elif util.tag_check_only_true(r['Tags']) and util.shouldTerminate(str(r['CreateTime'])[:19],-3):
                    delete_volume[r['VolumeId']]=name

                    if 'Iops' in r:
                        db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
                    else:
                        db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
                    
                else:                    
                    delete_volume[r['VolumeId']]=name

                    if 'Iops' in r:
                        db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
                    else:
                        db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
                    
        elif util.shouldTerminate(str(r['CreateTime'])[:19],-1):
            delete_volume[r['VolumeId']]="no name"
            if 'Iops' in r:
                db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
            else:
                db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
           
            print(delete_volume)

    for key, value in delete_volume.items():
        msg=msg+" `"+key+"` = "+"`"+str(value)+"`"+"\n"
        print(key)
        
    #util.sendslacknotification(msg)
    return msg

def get_volume_prod(botoClient, msg, table):
    imp_volume=[]
    name=[]
    delete_volume={}
    response = botoClient.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']
    
    for r in response:
        if 'Tags' in r:
            name=util.volume_name_fetch(r['Tags'])

            if util.imp_volumes(r['Tags']):
                imp_volume.append(r['VolumeId'])
                print("This volume is important \n ")
                print(name)
            elif util.shouldTerminate(str(r['CreateTime'])[:19],-1):
                
                if util.tag_check_always_true(r['Tags']) and util.shouldTerminate(str(r['CreateTime'])[:19],-10):
                    print("Always try volumes")
                   
                elif util.tag_check_only_true(r['Tags']) and util.shouldTerminate(str(r['CreateTime'])[:19],-15):
                    delete_volume[r['VolumeId']]=name

                    if 'Iops' in r:
                        db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
                    else:
                        db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
                else:
                   
                    delete_volume[r['VolumeId']]=name

                    if 'Iops' in r:
                        db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
                    else:
                        db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
                    
        elif util.shouldTerminate(str(r['CreateTime'])[:19],-1):

            delete_volume[r['VolumeId']]="no name"

            if 'Iops' in r:
                db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
            else:
                db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
            
            print(delete_volume)

    for key, value in delete_volume.items():

        msg=msg+" `"+key+"` = "+"`"+str(value)+"`"+"\n"
        print(key)

    #util.sendslacknotification(msg)
    return msg

def main():
    client= boto3.client('ec2','eu-west-1')
    msg="*Below are the available volumes which will be deleted from QA account by EOD* \n"
    msg_qa=get_volume_qa(client, msg, configuration.volume_qa_tablename)
    


############### PROD ################
    msg="*Below are the available volumes which will be deleted from Prod account by EOD* \n"
    prodClient = util.getAssume_roleSession("ec2", configuration.prod_assume_role_arn)
    msg_prod=get_volume_prod(prodClient, msg, configuration.volume_prod_tablename)

############### Stagging ################
    staggingClient = util.getAssume_roleSession("ec2", configuration.stagging_assume_role_arn)
    msg="*Below are the available volumes which will be deleted from Stagging account by EOD* \n"
    msg_stagging=get_volume_qa(staggingClient, msg, configuration.volume_stagging_tablename)

    slack_message=msg_qa +"\n"+ msg_prod +"\n"+ msg_stagging

    #util.sendslacknotification(slack_message)

if __name__=='__main__':
    main()