import boto3
import util
import datetime
from repo import terminateDBOperations
import configuration
from datetime import timedelta
from repo import terminateDBOperations
db= terminateDBOperations()
d = datetime.datetime.today()



def delete_qa(client, qa_table):
    row={}
    notification_date = d + timedelta(days=-1)
    print (notification_date.strftime('%d-%m-%Y'))
    row=db.selectNonTerminatedResources(qa_table, '0', 'Yes')
    print(row)
    for snapshot in row:
        print('Terminate this snapshot=', snapshot.get("SnapshotId"))
        try:
            client.delete_snapshot(SnapshotId=snapshot.get("SnapshotId"))
            db.updateResourceTerminationState(qa_table,'1', snapshot.get("SnapshotId"))
        except Exception as e:
            print(e)


def delete_prod(client, prod_table):
    row={}
    notification_date = d + timedelta(days=-1)
    print (notification_date.strftime('%d-%m-%Y'))
    row=db.selectNonTerminatedResources(prod_table, '0', 'Yes')
    print(row)
    for snapshot in row:
        print('Terminate this snapshot=', snapshot.get("SnapshotId"))
        try:
            client.delete_snapshot(SnapshotId=snapshot.get("SnapshotId"))
            db.updateResourceTerminationState(prod_table,'1', snapshot.get("SnapshotId"))
        except Exception as e:
            print(e)


def delete_stagging(client, stagging_table):
    row={}
    notification_date = d + timedelta(days=-1)
    print (notification_date.strftime('%d-%m-%Y'))
    row=db.selectNonTerminatedResources(stagging_table, '0', 'Yes')
    print(row)
    for snapshot in row:
        print('Terminate this snapshot=', snapshot.get("SnapshotId"))
        try:
            client.delete_snapshot(SnapshotId=snapshot.get("SnapshotId"))
            db.updateResourceTerminationState(stagging_table,'1', snapshot.get("SnapshotId"))
        except Exception as e:
            print(e)
def main():

    msg=" Below Snapshot are going to be deleted on QA '8485-6932-0300' \n"
    client = boto3.client('ec2','eu-west-1')
    delete_qa(client, configuration.snapshot_qa_tablename)

    ####################

    msg=" Below Snapshot are going to be deleted on Production Account' \n"
    prodclient = util.getAssume_roleSession("ec2", configuration.prod_assume_role_arn)
    delete_prod(prodclient, configuration.snapshot_prod_tablename)

    #####################

    msg=" Below Snapshot are going to be deleted Stagging account' \n"
    staggingClient = util.getAssume_roleSession("ec2", configuration.stagging_assume_role_arn)
    delete_stagging(staggingClient, configuration.snapshot_stagging_tablename)

    #####################



if __name__ == '__main__':
    main()