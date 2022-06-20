import boto3

client = boto3.client('lambda')

response = client.list_functions(MaxItems=50)
names = response['Functions']


def lambdas_function():
    for func in names:
        print(
            "Function Name: {0}\nX-Ray: {1}\n".format(
                func['FunctionName'],
                func['TracingConfig'],
            )
        )


lambdas_function()