import boto3
import time

# Creating an Aurora Serverless RDS
# We only have access to RDS as a client but not as a resource
rds = boto3.client("rds")

username = "srivishpUser"
password = "MyRDS#123"
db_subnet_group = "vpc-python4aws"
db_cluster_id = "rds-cluster-python4aws"
db_instance_id = "rds-instance-python4aws"


# Creating a DB Cluster
# Checking if DB exists or not
try:
    response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
    print(
        f"DB cluster named '{db_cluster_id}' already exists. Skipping creation...")
except rds.exceptions.DBClusterNotFoundFault:
    response = rds.create_db_cluster(
        Engine='aurora-mysql',
        EngineVersion='8.0',
        DBClusterIdentifier=db_cluster_id,
        MasterUsername=username,
        MasterUserPassword=password,
        DatabaseName='rds_python4aws_db',
        DBSubnetGroupName=db_subnet_group,
        EnableHttpEndpoint=True,
        ServerlessV2ScalingConfiguration={
            'MinCapacity': 0,  # Minimum ACU
            'MaxCapacity': 2,  # Maximum ACU
        }
    )
    print(f"The DB cluster named '{db_cluster_id}' has been created.")

# Wait for the DB cluster to become  available
while True:
    response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
    status = response["DBClusters"][0]["Status"]
    print(f"The status of cluster is '{status}'")
    if status == "available":
        break

    print("Waiting for the DB cluster to become available...")
    time.sleep(40)  # Waiting for 40 seconds

# Serverless V2 requires us to explicitly create an instance
try:
    check_instance_response = rds.describe_db_instances(
        DBInstanceIdentifier=db_instance_id)
    print(
        f"DB instance named '{db_instance_id}' already exists. Skipping creation...")
except rds.exceptions.DBInstanceNotFoundFault:

    instance_response = rds.create_db_instance(
        DBInstanceIdentifier=db_instance_id,
        DBClusterIdentifier=db_cluster_id,
        Engine='aurora-mysql',          # Must match the cluster engine
        # This tells AWS to boot this instance as a Serverless v2 node
        DBInstanceClass='db.serverless'
    )

    print("Serverless v2 cluster and instance creation initiated successfully!")


# Modify the DB cluster. Update the scaling configuration for the cluster. Only allowed for v1 cluster

# response = rds.modify_db_cluster(
#     DBClusterIdentifier=db_cluster_id,
#     ScalingConfiguration={
#         'MinCapacity': 1,  # Minimum ACU
#         'MaxCapacity': 2,  # Maximum ACU
#         'SecondsUntilAutoPause': 600  # Pause after 10 minutes of inactivity
#     }
# )
# print(f"Updated the scaling configuration for DB cluster '{db_cluster_id}'.")

# Deleting the cluster. For v2 instance must be deleted before deleting cluster
response = rds.delete_db_instance(
    DBInstanceIdentifier=db_instance_id
)
time.sleep(40)  # Waiting for 40 seconds
response = rds.delete_db_cluster(
    DBClusterIdentifier=db_cluster_id,
    SkipFinalSnapshot=True
)
print(f"The '{db_cluster_id}' is being deleted.")
