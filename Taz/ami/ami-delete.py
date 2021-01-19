import boto3
import utils
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
    for value in row:
        try:
            print ("deregistering this ami", value.get("ami_id"))
            id=value.get("ami_id")
            client.deregister_image(ImageId=id)
            db.updateResourceTerminationState(qa_table,'1', id)
        except Exception as e:
            print(e)


    
def delete_prod(client, prod_table):
    Important_ami=[]
    ami1=[]
    date=[]
    imp_ami=[]
    delete_ami={}
    row={}
    db= terminateDBOperations()
    d = datetime.datetime.today()
    notification_date = d + timedelta(days=-1)
    row=db.selectNonTerminatedResources(prod_table, '0', 'Yes')
    for value in row:
        try:
            print ("deregistering this ami", value.get("ami_id"))
            id=value.get("ami_id")
            client.deregister_image(ImageId=id)
            db.updateResourceTerminationState(prod_table,'1', id)
        except Exception as e:
            print(e)

def delete_stagging(client, stagging_table):
    Important_ami=[]
    ami1=[]
    date=[]
    imp_ami=[]
    delete_ami={}
    row={}
    db= terminateDBOperations()
    d = datetime.datetime.today()
    notification_date = d + timedelta(days=0)
    row=db.selectNonTerminatedResources(stagging_table, '0', 'Yes')
    for value in row:
        try:
            print ("deregistering this ami", value.get("ami_id"))
            id=value.get("ami_id")
            client.deregister_image(ImageId=id)
            db.updateResourceTerminationState(stagging_table,'1', id)
        except Exception as e:
            print(e)

def main():
    #print("python main function")
    msg=" *Below AMI's will be deleted from QA '8485-6932-0300'* by EOD \n"
    client = boto3.client('ec2','eu-west-1')
    delete_qa(client, configuration.ami_qa_tablename)

    ####################

    msg=" *Below AMI's will be deleted from Production Account' by EOD* \n"
    prodclient = utils.getAssume_roleSession("ec2", configuration.prod_assume_role_arn)
    delete_prod(prodclient, configuration.ami_prod_tablename)

    #####################

    msg=" *Below AMI's will be deleted from Stagging Account' by EOD* \n"
    staggingClient = utils.getAssume_roleSession("ec2", configuration.stagging_assume_role_arn)
    delete_stagging(staggingClient, configuration.ami_stagging_tablename)

    #####################

    #msg=" Below AMI are going to be deleted on Stagging 'Accountno' \n"
    #staggingClient = utils.getAssume_roleSession("ec2", configuration.staging_assume_role_arn)
    #amiCleanupOperations(staggingClient, msg)
    #msg=" Below AMI are going to be deleted on Production 'Accountno' \n"
    #prodClient = utils.getAssume_roleSession("ec2", configuration.prod_assume_role_arn)
    #amiCleanupOperations_Prod(prodClient, msg)


if __name__ == '__main__':
    main()

