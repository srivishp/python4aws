import boto3
import time

# Creating a VPC
ec2 = boto3.client("ec2")
vpc_name = "vpc-python4aws"

# Ensuring VPC doesn't exist before creation
# Creating a filter that searches by the name of our VPC
response = ec2.describe_vpcs(
    Filters=[{'Name': 'tag:Name', 'Values': [vpc_name]}]
)
# Getting the list of existing VPCs
vpcs = response.get('Vpcs', [])

if vpcs:
    vpc_id = vpcs[0]['VpcId']
    print(f"VPC '{vpc_name}' with ID '{vpc_id}' already exists.")
else:
    vpc_response = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    vpc_id = vpc_response["Vpc"]["VpcId"]

    # Adding a delay for our convenience because a VPC takes time to get created
    time.sleep(5)  # 5 seconds

    ec2.create_tags(Resources=[vpc_id], Tags=[
                    {"Key": "Name", "Value": vpc_name}])
    print(f"VPC {vpc_name} with ID '{vpc_id}' has been created")


# Create Internet Gateway
igw_name = "python4aws-igw"
# Ensuring Internet Gateway doesn't exist before creation
# Creating a filter that searches by the name of our IGW
response = ec2.describe_internet_gateways(
    Filters=[{'Name': 'tag:Name', 'Values': [igw_name]}]
)
# Getting the list of existing IGWs
igws = response.get('IGWs', [])

if igws:
    igw_id = igws[0]['IgwId']
    print(f"Internet Gateway '{igw_name}' with ID '{igw_id}' already exists.")
else:
    igw_response = ec2.create_internet_gateway()
    igw_id = igw_response["InternetGateway"]["InternetGatewayId"]
    print(f"Internet Gateway {igw_name} with ID '{igw_id}' has been created")

# Attaching the Internet Gateway to the VPC
ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=igw_id)
print(f"Internet Gateway {igw_name} is attached to the VPC {vpc_name}")


# Create a route table and a public route
rt_response = ec2.create_route_table(VpcId=vpc_id)
rt_id = rt_response["RouteTable"]["RouteTableId"]
route = ec2.create_route(
    RouteTableId=rt_id,
    DestinationCidrBlock="0.0.0.0/0",
    GatewayId=igw_id
)

print(f"Route Table {rt_id} has been created")

# Create 3 subnets
subnet_1 = ec2.create_subnet(
    VpcId=vpc_id, CidrBlock="10.0.1.0/24", AvailabilityZone="us-east-1a")
subnet_2 = ec2.create_subnet(
    VpcId=vpc_id, CidrBlock="10.0.2.0/24", AvailabilityZone="us-east-1b")
subnet_3 = ec2.create_subnet(
    VpcId=vpc_id, CidrBlock="10.0.3.0/24", AvailabilityZone="us-east-1c")

print(
    f"Subnets #1: {subnet_1["Subnet"]["SubnetId"]}, #2: {subnet_2["Subnet"]["SubnetId"]} and #3: {subnet_3["Subnet"]["SubnetId"]} have been created")
