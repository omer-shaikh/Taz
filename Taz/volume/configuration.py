# Assume Role ARNs

prod_assume_role_arn = 'arn:aws:iamXXXXX/ec2-cost-saving-cross-account-role'
stagging_assume_ro:wqle_arn = 'arn:aws:iam::xxxxxxxx:role/assume_role_governance_ec2_s3'
bus_stagging_assume_role_arn = 'arn:aws:iam::xxxxx:role/ec2-cost-saving-cross-account-role'
bus_data_assume_role_arn = 'arn:aws:iam::xxxxx:role/ec2-cost-saving-cross-account-role'
bus_dr_assume_role_arn = 'arn:aws:iam::xxxxxx:role/ec2-cost-saving-cross-account-role'
bus_prod_assume_role_arn = 'arn:aws:iam::xxxxxxxx:role/ec2-cost-saving-cross-account-role'
bus_dev_assume_role_arn = 'arn:aws:iam::xxxxxx:role/ec2-cost-saving-cross-account-role'





# login credentials
hostname = "xxxx.rds.amazonaws.com"
username = "admin"
db = "backuphistory"
password = "xxxxxx"

ami_qa_tablename="backuphistory.ami_qa"
ami_prod_tablename="backuphistory.ami_prod"
ami_stagging_tablename="backuphistory.ami_stagging"

snapshot_qa_tablename="backuphistory.snapshot_qa"
snapshot_prod_tablename="backuphistory.snapshot_prod"
snapshot_stagging_tablename="backuphistory.snapshot_stagging"

volume_qa_tablename="backuphistory.volume_qa"
volume_prod_tablename="backuphistory.volume_prod"
volume_stagging_tablename="backuphistory.volume_stagging"
volume_bus_stagging_tablename="backuphistory.volume_bus_stagging"
volume_bus_data_tablename="backuphistory.volume_bus_data"
volume_bus_dr_tablename="backuphistory.volume_bus_dr"
volume_bus_prod_tablename="backuphistory.volume_bus_prod"
volume_bus_dev_tablename="backuphistory.volume_bus_dev"
