import boto3

# AWS credentials (ensure you have appropriate access)

region_name = 'us-east-1'

ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Retrieve instances with a specific tag
tag_key = 'ansible'
tag_value = 'yes'

response = ec2_client.describe_instances(
    Filters=[
        {
            'Name': f'tag:{tag_key}',
            'Values': [tag_value]
        }
    ]
)

instances = []

# Iterate over the reservations and extract instance details
for reservation in response['Reservations']:
    instances.extend(reservation['Instances'])

# Write the inventory to a file (overwriting existing content)
with open('inventory.ini', 'w') as inventory_file:
    inventory_file.write('[flask]\n')
    for i, instance in enumerate(instances, start=1):
        public_ip = str(instance['PublicIpAddress'])
        inventory_file.write(f'flask{i} ansible_host={public_ip} ansible_user=ec2-user ansible_ssh_private_key_file=/home/oryaeer/.ssh/oryaeer.pem\n')

print("Inventory file created successfully.")
