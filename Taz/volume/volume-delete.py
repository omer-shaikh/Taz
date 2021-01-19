import boto3
import util
import datetime
from repo import terminateDBOperations
import configuration
from datetime import timedelta
from repo import terminateDBOperations
db= terminateDBOperations()
d = datetime.datetime.today()



def delete(client, table):
    row={}
    notification_date = d + timedelta(days=-1)
    print (notification_date.strftime('%d-%m-%Y'))
    row=db.selectNonTerminatedResources(table, '0', 'Yes')
    print(row)
    for volume in row:
        print('Terminate this Volume=', volume.get("VolumeId"))
        try:
            client.delete_volume(VolumeId=volume.get("VolumeId"))
            db.updateResourceTerminationState(table,'1', volume.get("VolumeId"))
        except Exception as e:
            print(e)


def main():

    #msg=" Below Snapshot are going to be deleted on QA '8485-6932-0300' \n"
    client = boto3.client('ec2','eu-west-1')
    delete(client, configuration.volume_qa_tablename)

    ####################

    msg=" Below Snapshot are going to be deleted on Production Account' \n"
    prodclient = util.getAssume_roleSession("ec2", configuration.prod_assume_role_arn)
    delete(prodclient, configuration.volume_prod_tablename)

    #####################

    msg=" Below Snapshot are going to be deleted Stagging account' \n"
    staggingClient = util.getAssume_roleSession("ec2", configuration.stagging_assume_role_arn)
    #delete(staggingClient, configuration.volume_stagging_tablename)

    #####################



if __name__ == '__main__':
    main()