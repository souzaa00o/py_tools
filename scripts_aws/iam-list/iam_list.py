import boto3

iam = boto3.client("iam")
accounts = iam.get_account_authorization_details()

def list_users():

    for user in accounts['UserDetailList']:
        print("User: {0}\nPolicy: {1}\n".format(
            user['UserName'],
            user['AttachedManagedPolicies']
            )
        )
        for group in accounts['GroupDetailList']:
            a = list()
            print("Group Name: {0}\n{0} Policies: {1}\n".format(
                group['GroupName'],
                group['AttachedManagedPolicies']
                )
            )

list_users()
