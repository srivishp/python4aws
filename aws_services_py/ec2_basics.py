import boto3

# Create EC2 resource and instance name
ec2 = boto3.resource("ec2")
instance_name = "sample-ec2-python4aws-srivishp"

# Store instance ID
instance_id = None

# Creating instance only if it doesn't exist. Work with instance that is not terminated
instances = ec2.instances.all()
instance_exists = False

for instance in instances:
    for tag in instance.tags:
        if tag['Key'] == 'Name' and tag['Value'] == instance_name:
            instance_exists = True
            instance_id = instance.id
            print(
                f"An instance named '{instance_name}' with id '{instance_id}' already exists.")
            break
    if instance_exists:
        break


# Launch an EC2 if it hasn't been created
if not instance_exists:
    new_instance = ec2.create_instances(
        ImageId='ami-0bdc7d025135d7b49',  # replace with a valid AMI ID
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='sample-ec2-keyPair',  # replace with your key pair name
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                                'Key': 'Name',
                                'Value': instance_name
                    },
                ]
            },
        ]
    )
    instance_id = new_instance[0].id
    print(
        f"An instance named '{instance_name}' with id '{instance_id}' created.")

# Stopping the EC2 instance
# ec2.Instance(instance_id).stop()
# print(
#     f"An instance named '{instance_name}' with id '{instance_id}' is stopped.")

# Starting the EC2 instance
# ec2.Instance(instance_id).start()
# print(
#     f"An instance named '{instance_name}' with id '{instance_id}' has started.")

# Terminate the EC2 instance
ec2.Instance(instance_id).terminate()
print(
    f"An instance named '{instance_name}' with id '{instance_id}' has been terminated.")
