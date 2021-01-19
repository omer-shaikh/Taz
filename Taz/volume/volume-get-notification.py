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

################# ONLY NOTIFY NO DATABASE INSERTION ##################

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
                        print("Iops")
                        #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
                    else:
                        print("Without Iops")
                        #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
                   
                elif util.tag_check_only_true(r['Tags']) and util.shouldTerminate(str(r['CreateTime'])[:19],-3):
                    delete_volume[r['VolumeId']]=name

                    if 'Iops' in r:
                        print("Iops")
                        #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
                    else:
                        print("Without Iops")
                        #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
                    
                else:                    
                    delete_volume[r['VolumeId']]=name

                    if 'Iops' in r:
                        print("Iops")
                        #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
                    else:
                        print("Wihtout Iops")
                        #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
                    
        elif util.shouldTerminate(str(r['CreateTime'])[:19],-1):
            delete_volume[r['VolumeId']]="no name"
            if 'Iops' in r:
                print("Iops")
                #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
            else:
                print("Wihout Iops")
                #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
           
            print(delete_volume)
    if len(delete_volume) == 0:
        msg=msg + "*No Volume*"
    else:
        for key, value in delete_volume.items():
            msg=msg+" `"+key+"` = "+"`"+str(value)+"`"+"\n"
            print(key)

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
                        print("Iops")
                        #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
                    else:
                        print("Wihout Iops")
                        #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
                else:
                   
                    delete_volume[r['VolumeId']]=name

                    if 'Iops' in r:
                        print("Iops")
                        #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
                    else:
                        print("Wihout Iops")
                        #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
                    
        elif util.shouldTerminate(str(r['CreateTime'])[:19],-1):

            delete_volume[r['VolumeId']]="no name"

            if 'Iops' in r:
                print("Iops")
                #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Iops'],'enter comment if required')
            else:
                print("Wihout Iops")
                #db.putResourceInfoToDatabase(table,r['VolumeId'], str(r['CreateTime'].strftime('%Y-%m-%d')), r['SnapshotId'], r['Size'], r['VolumeType'], '0', 'Yes', d.strftime('%d-%m-%Y'),"NULL",'enter comment if required')
            
            print(delete_volume)

    if len(delete_volume) == 0:
        msg=msg + "*No Volume*"
    else:
        for key, value in delete_volume.items():
            msg=msg+" `"+key+"` = "+"`"+str(value)+"`"+"\n"
            print(key)

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

########################################

    msg=" *Below Volumes will be deleted from BUS Stagging Account Please Tag them respectively* \n"
    busStaggingclient = util.getAssume_roleSession("ec2", configuration.bus_stagging_assume_role_arn)
    msg_bus_stagging=get_volume_qa(busStaggingclient, msg, configuration.volume_bus_stagging_tablename)

############################################

    msg=" *Below Volumes will be deleted from BUS Data Account Please tag them respectively* \n"
    busDataClient = util.getAssume_roleSession("ec2", configuration.bus_data_assume_role_arn)
    msg_bus_data=get_volume_qa(busDataClient, msg, configuration.volume_bus_data_tablename)

############################################

    msg=" *Below Snapshots will be deleted from BUS DR Account Please tag them respectively* \n"
    busDrClient = util.getAssume_roleSession("ec2", configuration.bus_dr_assume_role_arn)
    msg_bus_dr=get_volume_prod(busDrClient, msg, configuration.volume_bus_dr_tablename)

############################################

    msg=" *Below Volumes will be deleted from BUS PROD Account Please tag them respectively* \n"
    busProdClient = util.getAssume_roleSession("ec2", configuration.bus_prod_assume_role_arn)
    msg_bus_prod=get_volume_prod(busProdClient, msg, configuration.volume_bus_prod_tablename)

############################################

    msg=" *Below Volumes will be deleted from BUS DEV Account Please tag them respectively* \n"
    busDevClient = util.getAssume_roleSession("ec2", configuration.bus_dev_assume_role_arn)
    msg_bus_dev=get_volume_qa(busDevClient, msg, configuration.volume_bus_dev_tablename)




    #slack_message=msg_qa +"\n"+ msg_prod +"\n"+ msg_stagging 
    slack_message= msg_prod +"\n"+ msg_bus_prod +"\n"+ msg_qa +"\n"+ msg_stagging +"\n"+ msg_bus_stagging +"\n"+ msg_bus_dev +"\n"+ msg_bus_data +"\n"+ msg_bus_dr

    util.sendslacknotification(slack_message)

if __name__=='__main__':
    main()