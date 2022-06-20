import boto3


def lambda_handler(event, context):

    # Listando as regioes
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]

    # Buscando em todas as regioes
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)

        print("Region:", region)

        # Filtrando por instancias ligadas
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

        # Parando as Instancias
        for instance in instances:
            instance.stop()
            print('Stopped instance: ', instance.id)

if __name__ == "__main__":
    lambda_handler({}, {})