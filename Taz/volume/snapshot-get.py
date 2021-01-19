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


def get_volume(botoClient, msg, table):
    Important_ami=[]
    snapshot=[]
    date=[]
    imp_snapshot=[]
    delete_snapshot={}
    response = botoClient.describe_snapshots(OwnerIds=['self'])
    db= terminateDBOperations()
    for r in response['Snapshots']:
        if util.shouldTerminate(str(r['StartTime'])[:19],-1):
            if 'Tags' in r:
                older_than_10_days=util.shouldTerminate(str(r['StartTime'])[:19],-10)
                older_than_3_days=util.shouldTerminate(str(r['StartTime'])[:19],-3)
                always_true=util.tag_check_always_true(r['Tags'])
                only_true=util.tag_check_only_true(r['Tags'])
                aws_backup=util.aws_backup(r['Tags'])
                if aws_backup:
                    imp_snapshot.append(r['SnapshotId'])
                    print("Important ami")
                elif always_true:
                    if older_than_10_days:
                        delete_snapshot[r['SnapshotId']]=r['Description']
                        db.putResourceInfoToDatabase(qa_table,r['SnapshotId'], str(r['StartTime'].strftime('%Y-%m-%d')), r['VolumeId'], r['VolumeSize'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Description'],'enter comment if required')
                        ###### DB integration reqruied in this line ###########
                        print ("delete with 10 day done with always true tag")
                        print ("this is the one catch" , r['SnapshotId'])
                elif only_true:
                    if older_than_3_days:
                        delete_snapshot[r['SnapshotId']]=r['Description']
                        print ("delete with 3 days done with only true tag")
                        db.putResourceInfoToDatabase(qa_table,r['SnapshotId'], str(r['StartTime'].strftime('%Y-%m-%d')), r['VolumeId'], r['VolumeSize'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Description'],'enter comment if required')
            else:
                print ("Images doesn't have any tag")
                delete_snapshot[r['SnapshotId']]=r['Description']
                db.putResourceInfoToDatabase(qa_table,r['SnapshotId'], str(r['StartTime'].strftime('%Y-%m-%d')), r['VolumeId'], r['VolumeSize'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Description'],'enter comment if required')

    for key, value in delete_snapshot.items():
        print ("These snapshots will be deleted", key, value)
        msg=msg+" `"+key+"`\n"
    #util.sendslacknotification(msg)






def get_snapshot_prod(botoClient, msg, prod_table):
    Important_ami=[]
    snapshot=[]
    date=[]
    imp_snapshot=[]
    delete_snapshot={}
    delete_ami={}
    response = botoClient.describe_snapshots(OwnerIds=['self'])
    db= terminateDBOperations()
    for r in response['Snapshots']:
        if util.shouldTerminate(str(r['StartTime'])[:19],-1):
            if 'Tags' in r:
                older_than_15_days=util.shouldTerminate(str(r['StartTime'])[:19],-15)
                always_true=util.tag_check_always_true(r['Tags'])
                only_true=util.tag_check_only_true(r['Tags'])
                aws_backup=util.aws_backup(r['Tags'])
                if aws_backup:
                    imp_snapshot.append(r['SnapshotId'])
                    print("aws backup ami: ", r['SnapshotId'])
                elif always_true:
                    imp_snapshot.append(r['SnapshotId'])
                    print("Important ami: ", r['SnapshotId'])
                elif only_true:
                    if older_than_15_days:
                        delete_snapshot[r['SnapshotId']]=r['Description']
                        print ("delete with 15 days done with only true tag")
                        db.putResourceInfoToDatabase(prod_table,r['SnapshotId'], str(r['StartTime'].strftime('%Y-%m-%d')), r['VolumeId'], r['VolumeSize'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Description'],'enter comment if required')
            else:
                print ("Images doesn't have any tag")
                delete_snapshot[r['SnapshotId']]=r['Description']
                db.putResourceInfoToDatabase(prod_table,r['SnapshotId'], str(r['StartTime'].strftime('%Y-%m-%d')), r['VolumeId'], r['VolumeSize'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Description'],'enter comment if required')

    for key, value in delete_snapshot.items():
        print ("These snapshots will be deleted", key, value)
        msg=msg+" `"+key+"`\n"
    #util.sendslacknotification(msg)




def get_snapshot_stagging(botoClient, msg, stagging_table):
    imp_snapshot=[]
    delete_snapshot={}
    response = botoClient.describe_snapshots(OwnerIds=['self'])
    db= terminateDBOperations()
    for r in response['Snapshots']:
        if util.shouldTerminate(str(r['StartTime'])[:19],-1):
            if 'Tags' in r:
                older_than_10_days=util.shouldTerminate(str(r['StartTime'])[:19],-10)
                older_than_3_days=util.shouldTerminate(str(r['StartTime'])[:19],-3)
                always_true=util.tag_check_always_true(r['Tags'])
                only_true=util.tag_check_only_true(r['Tags'])
                aws_backup=util.aws_backup(r['Tags'])
                if aws_backup:
                    imp_snapshot.append(r['SnapshotId'])
                    print("Important ami")
                elif always_true:
                    if older_than_10_days:
                        delete_snapshot[r['SnapshotId']]=r['Description']
                        db.putResourceInfoToDatabase(stagging_table,r['SnapshotId'], str(r['StartTime'].strftime('%Y-%m-%d')), r['VolumeId'], r['VolumeSize'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Description'],'enter comment if required')
                        ###### DB integration reqruied in this line ###########
                        print ("delete with 10 day done with always true tag")
                        print ("this is the one catch" , r['SnapshotId'])
                elif only_true:
                    if older_than_3_days:
                        delete_snapshot[r['SnapshotId']]=r['Description']
                        print ("delete with 3 days done with only true tag")
                        db.putResourceInfoToDatabase(stagging_table,r['SnapshotId'], str(r['StartTime'].strftime('%Y-%m-%d')), r['VolumeId'], r['VolumeSize'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Description'],'enter comment if required')
            else:
                print ("Images doesn't have any tag")
                delete_snapshot[r['SnapshotId']]=r['Description']
                db.putResourceInfoToDatabase(stagging_table,r['SnapshotId'], str(r['StartTime'].strftime('%Y-%m-%d')), r['VolumeId'], r['VolumeSize'], '0', 'Yes', d.strftime('%d-%m-%Y'),r['Description'],'enter comment if required')

    for key, value in delete_snapshot.items():
        print ("These snapshots will be deleted", key, value)
        msg=msg+" `"+key+"`\n"
    #util.sendslacknotification(msg)



def main():
    msg="*Below Snapshot QA account snapshots are going to be deleted by the EOD*\n"
    client= boto3.client('ec2','eu-west-1')
    get_snapshot_qa(client, msg, configuration.snapshot_qa_tablename)

########################################

    msg=" Below Snapshot are going to be deleted on Production 'Account' \n"
    prodClient = util.getAssume_roleSession("ec2", configuration.prod_assume_role_arn)
    get_snapshot_prod(prodClient, msg, configuration.snapshot_prod_tablename)

########################################
    
    msg=" Below Snapshot are going to be deleted on Stagging 'Account' \n"
    staggingClient = util.getAssume_roleSession("ec2", configuration.stagging_assume_role_arn)
    get_snapshot_stagging(staggingClient, msg, configuration.snapshot_stagging_tablename)
    

if __name__=='__main__':
    main()
