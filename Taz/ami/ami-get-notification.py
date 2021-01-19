import boto3
import json
from datetime import datetime
from datetime import timedelta
from httplib2 import Http
import requests, json
import utils
import configuration
from repo import terminateDBOperations
d = datetime.today()

################# ONLY NOTIFY NO DATABASE INSERTION ##################

def amiCleanupOperations_QA(botoClient, msg, qa_table):
    imp_ami=[]
    delete_ami={}
    response = botoClient.describe_images(Owners=['self'])
    for r in response['Images']:
        older_than_1_day, create_date=utils.shouldTerminate(r['CreationDate'],-1)
        do_not_delete_ami=utils.exclude_ami(r['Name'])
        if do_not_delete_ami:
            imp_ami.append(r['ImageId'])
            print ('Images are important ' +  r['Name'])
        else:
            if older_than_1_day :
                if 'Tags' in r:
                    if utils.active(r['Tags']):
                        imp_ami.append(r['ImageId'])
                        print ('Images are important ' +  r['Name'])
                    else:
                        older_than_3_day, create_date=utils.shouldTerminate(r['CreationDate'],-3)
                        older_than_10_day,create_date=utils.shouldTerminate(r['CreationDate'],-10)
                        always_true=utils.tag_check_always_true(r['Tags'])
                        only_true = utils.tag_check_only_true(r['Tags'])
                        if always_true:
                            if older_than_10_day:
                                print('10 days are done please delete ' + r['Name'])
                                delete_ami[r['ImageId']]=r['Name']                            
                            else:
                                print('it has always true tag but 10 days are not done leave')                    
                        elif only_true:
                            if older_than_3_day:
                                print('3 days are completed delete this')
                                delete_ami[r['ImageId']]=r['Name']
                            else:
                                print('3 days are not done do not delete this')
                else:
                    print ('Images do not have tag we are deleting this ami : ' + r['Name'])
                    delete_ami[r['ImageId']]=r['Name']
                    
    print ('Important Ami:')
    print (imp_ami)
    print ('Delete Ami:')
    print (delete_ami)
    if len(delete_ami) == 0:
        msg=msg + "*No AMI*"
    else:
        for key, value in delete_ami.items():
            msg=msg+" `"+key+"` = "+value+"\n"
    #utils.sendslacknotification(msg)
    return msg

def amiCleanupOperations_Prod(botoClient, msg, prod_table):
    imp_ami=[]
    delete_ami={}
    response = botoClient.describe_images(Owners=['self'])
    for r in response['Images']:
        older_than_1_day, create_date=utils.shouldTerminate(r['CreationDate'],-1)
        do_not_delete_ami=utils.exclude_ami(r['Name'])
        if do_not_delete_ami:
            imp_ami.append(r['ImageId'])
            print ('Images are important ' +  r['Name'], '\n')
        else:
            if older_than_1_day:
                if 'Tags' in r:
                    if utils.active(r['Tags']):
                        imp_ami.append(r['ImageId'])
                        print ('Images are important ' +  r['Name'])
                    else:
                    #older_than_3_day, create_date=utils.shouldTerminate(r['CreationDate'],-3)
                        older_than_15_day,create_date=utils.shouldTerminate(r['CreationDate'],-15)
                        always_true=utils.tag_check_always_true(r['Tags'])
                        only_true = utils.tag_check_only_true(r['Tags'])
                        if always_true:
                            imp_ami.append(r['ImageId'])
                        elif only_true:
                            if older_than_15_day:
                                print('15 days are completed delete this')
                                delete_ami[r['ImageId']]=r['Name']
                            else:
                                print('15 days are not done do not delete this')        
                else:
                    print ('Images do not have tag we are deleting this ami : ' + r['Name'], '\n')
                    delete_ami[r['ImageId']]=r['Name']
                    
    if len(delete_ami) == 0:
        msg=msg + "*No AMI*"
    else:    
        for key, value in delete_ami.items():
            msg=msg+" `"+key+"` = "+value+"\n"
    return msg
    #utils.sendslacknotification(msg)

def amiCleanupOperations_stagging(botoClient, msg, stagging_table):
    imp_ami=[]
    delete_ami={}
    response = botoClient.describe_images(Owners=['self'])

    for r in response['Images']:
        older_than_1_day, create_date=utils.shouldTerminate(r['CreationDate'],-1)
        do_not_delete_ami=utils.exclude_ami(r['Name'])
        if do_not_delete_ami:
            imp_ami.append(r['ImageId'])
            print ('Images are important ' +  r['Name'])
        else:
            if older_than_1_day :
                if 'Tags' in r:
                    if utils.active(r['Tags']):
                        imp_ami.append(r['ImageId'])
                        print ('Images are important ' +  r['Name'])
                    else:
                        older_than_3_day, create_date=utils.shouldTerminate(r['CreationDate'],-3)
                        older_than_10_day,create_date=utils.shouldTerminate(r['CreationDate'],-10)
                        always_true=utils.tag_check_always_true(r['Tags'])
                        only_true = utils.tag_check_only_true(r['Tags'])
                        if always_true:
                            if older_than_10_day:
                                print('10 days are done please delete ' + r['Name'])
                                delete_ami[r['ImageId']]=r['Name']
                            else:
                                print('it has always true tag but 10 days are not done leave')
                        elif only_true:
                            if older_than_3_day:
                                print('3 days are completed delete this')
                                delete_ami[r['ImageId']]=r['Name']    
                            else:
                                print('3 days are not done do not delete this')
                else:
                    print ('Images do not have tag we are deleting this ami : ' + r['Name'])
                    delete_ami[r['ImageId']]=r['Name']
                    
    if len(delete_ami) == 0:
        msg=msg + "*No AMI*"
    else:
        for key, value in delete_ami.items():
            msg=msg+" `"+key+"` = "+value+"\n"
    #utils.sendslacknotification(msg)
    return msg






def main():
    print("python main function")
    msg=" *Below AMI's will be deleted from QA '8485-6932-0300' by EOD* \n"
    client = boto3.client('ec2','eu-west-1')
    msg_qa=amiCleanupOperations_QA(client, msg, configuration.ami_qa_tablename)

############################################

    msg=" *Below AMI's will be deleted from Stagging Account by EOD* \n"
    staggingClient = utils.getAssume_roleSession("ec2", configuration.stagging_assume_role_arn)
    msg_stagging=amiCleanupOperations_stagging(staggingClient, msg, configuration.ami_stagging_tablename)

############################################

    msg=" *Below AMI's will be deleted from Production Account by EOD*' \n"
    prodClient = utils.getAssume_roleSession("ec2", configuration.prod_assume_role_arn)
    msg_prod=amiCleanupOperations_Prod(prodClient, msg, configuration.ami_prod_tablename)

############################################

    msg=" *Below AMI's will be deleted from BUS Stagging Account Please Tag them respectively*' \n"
    busStaggingclient = utils.getAssume_roleSession("ec2", configuration.bus_stagging_assume_role_arn)
    msg_bus_stagging=amiCleanupOperations_stagging(busStaggingclient, msg, configuration.ami_bus_stagging_tablename)

############################################

    msg=" *Below AMI's will be deleted from BUS Data Account Please tag them respectively*' \n"
    busDataClient = utils.getAssume_roleSession("ec2", configuration.bus_data_assume_role_arn)
    msg_bus_data=amiCleanupOperations_stagging(busDataClient, msg, configuration.ami_bus_data_tablename)

############################################

    msg=" *Below AMI's will be deleted from BUS DR Account Please tag them respectively*' \n"
    busDrClient = utils.getAssume_roleSession("ec2", configuration.bus_dr_assume_role_arn)
    msg_bus_dr=amiCleanupOperations_stagging(busDrClient, msg, configuration.ami_bus_dr_tablename)

############################################

    msg=" *Below AMI's will be deleted from BUS PROD Account Please tag them respectively*' \n"
    busProdClient = utils.getAssume_roleSession("ec2", configuration.bus_prod_assume_role_arn)
    msg_bus_prod=amiCleanupOperations_Prod(busProdClient, msg, configuration.ami_bus_prod_tablename)

############################################

    msg=" *Below AMI's will be deleted from BUS DEV Account Please tag them respectively*' \n"
    busDevClient = utils.getAssume_roleSession("ec2", configuration.bus_dev_assume_role_arn)
    msg_bus_dev=amiCleanupOperations_Prod(busDevClient, msg, configuration.ami_bus_dev_tablename)




    slack_message=msg_prod +"\n"+ msg_bus_prod +"\n"+ msg_qa +"\n"+ msg_bus_stagging +"\n"+ msg_bus_data +"\n"+ msg_bus_dr +"\n"+ msg_stagging +"\n"+ msg_bus_dev
    utils.sendslacknotification(slack_message)

if __name__ == '__main__':
    main()