# Assume Role ARNs

prod_assume_role_arn = 'arn:aws:iam::xxxxx:role/ec2-cost-saving-cross-account-role'
stagging_assume_role_arn = 'arn:aws:iam::xxxxx:role/assume_role_governance_ec2_s3'
bus_stagging_assume_role_arn = 'arn:aws:iam::xxxxx:role/ec2-cost-saving-cross-account-role'
bus_data_assume_role_arn = 'arn:aws:iam::xxxxxx:role/ec2-cost-saving-cross-account-role'
bus_dr_assume_role_arn = 'arn:aws:iam::xxxxxxxx:role/ec2-cost-saving-cross-account-role'
bus_prod_assume_role_arn = 'arn:aws:iam::xxxxxxxx:role/ec2-cost-saving-cross-account-role'
bus_dev_assume_role_arn = 'arn:aws:iam::xxxxxxxx:role/ec2-cost-saving-cross-account-role'





# login credentials
hostname = "xxxxxxx.eu-west-1.rds.amazonaws.com"
username = "admin"
db = "backuphistory"
password = "xxxxxxx"

ami_qa_tablename="backuphistory.ami_qa"
ami_prod_tablename="backuphistory.ami_prod"
ami_stagging_tablename="backuphistory.ami_stagging"


snapshot_qa_tablename="backuphistory.snapshot_qa"
snapshot_prod_tablename="backuphistory.snapshot_prod"
snapshot_stagging_tablename="backuphistory.snapshot_stagging"
snapshot_bus_stagging_tablename="backuphistory.snapshot_bus_stagging"
snapshot_bus_data_tablename="backuphistory.snapshot_bus_data"
snapshot_bus_dr_tablename="backuphistory.snapshot_bus_dr"
snapshot_bus_prod_tablename="backuphistory.snapshot_bus_prod"
snapshot_bus_dev_tablename="backuphistory.snapshot_bus_dev"
