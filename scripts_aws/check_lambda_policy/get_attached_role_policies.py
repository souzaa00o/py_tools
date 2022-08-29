import resource
import boto3

def main():
    cf = boto3.client("cloudformation")
    lf = boto3.client("lambda")
    iamf = boto3.client("iam")
    stacks_names = get_stacks_functions(cf)
    stack_resources = get_stack_resource(stacks_names, cf)
    role_resources = get_function_configuration(lf, stack_resources)
    attached_policies = get_attached_role_policies(iamf, role_resources)

    print(attached_policies)


def get_stacks_functions(cf):
    stacks = cf.list_stacks(StackStatusFilter=['CREATE_COMPLETE','UPDATE_COMPLETE','ROLLBACK_COMPLETE','DELETE_FAILED'])
    stacks_names = [stack["StackName"] for stack in stacks["StackSummaries"]]

    while stacks.get("NextToken"):
        stacks = cf.list_stacks(NextToken=stacks["NextToken"])
        stacks_names.append([stack["StackName"] for stack in stacks["StackSummaries"]])

    return stacks_names


def get_stack_resource(stacks_names, cf):
    fname_result = []

    for stack in stacks_names:
        resources = cf.list_stack_resources(StackName=stack)

        for resource in resources["StackResourceSummaries"]:    
            if resource["ResourceType"] == "AWS::Lambda::Function":
                function_info = {
                    "stack_name": stack,
                    "function_name": resource["PhysicalResourceId"]
                }

                fname_result.append(function_info)

    return fname_result


def get_function_configuration(lf, stack_resources):
    # rname_result = []

    for stack in stack_resources:
        function_name = stack["function_name"]
        try:
            configuration = lf.get_function_configuration(FunctionName=function_name)
        except Exception:
            continue

        stack['role'] = configuration["Role"].split('/')[1]

        # role_info = {
        #     "stack_name": stack["stack_name"],
        #     "function_name": function_name,
        #     "role": configuration["Role"].split('/')[1]
        # }
            
        # rname_result.append(role_info)
    
    return stack_resources

def get_attached_role_policies(iamf, role_resources):
    pname_result = []
    
    for role in role_resources:
        role_name = role.get("role")
        try:
            policy = iamf.list_attached_role_policies(RoleName=role_name)
        except Exception:
            continue
        
        for policy in policy["AttachedPolicies"]:
            pname_result.append({
                "stack_name": role["stack_name"],
                "function_name": role["function_name"],
                "policies": policy
            })
    print(pname_result)
    return pname_result


main()