import resource

import boto3


def list_functions():
    cf_cli = boto3.client("cloudformation")
    stack_names = list_stack_names(cf_cli)

    functions = []

    for stack_name in stack_names:
        resources = cf_cli.list_stack_resources(StackName=stack_name)

        for resource in resources["StackResourceSummaries"]:
            if resource["ResourceType"] == "AWS::Lambda::Function":
                function_info = {
                    "stack": stack_name,
                    "function": resource["PhysicalResourceId"],
                }

                functions.append(function_info)

    return functions


def list_stack_names(cf_cli):
    stacks = cf_cli.list_stacks()
    stack_names = []
    invalid_status = ["DELETE_COMPLETE", "DELETE_IN_PROGRESS"]

    for stack in stacks["StackSummaries"]:
        if stack["StackStatus"] not in invalid_status:
            stack_names.append(stack["StackName"])

    while stacks.get("NextToken"):
        stacks = cf_cli.list_stacks(NextToken=stacks["NextToken"])
        for stack in stacks["StackSummaries"]:
            if stack["StackStatus"] not in invalid_status:
                stack_names.append(stack["StackName"])

    return stack_names


def list_role_functions(functions):
    lambda_cli = boto3.client("lambda")

    roles = []

    for function in functions:
        try:
            configuration = lambda_cli.get_function_configuration(FunctionName=function["function"])
        except Exception:
            continue

        role = configuration.get("Role", "").split("/", maxsplit=1)

        try:
            role = role[1]
        except IndexError:
            continue

        role = {"role": role, **function}
        roles.append(role)

    return roles


def list_function_policies():
    functions = list_functions()
    roles = list_role_functions(functions)

    iam = boto3.client("iam")

    result = []

    for role in roles:
        role_name = role.get("role")

        if role_name:
            try:
                policies = iam.list_attached_role_policies(RoleName=role_name)
            except Exception:
                continue

            for policy in policies["AttachedPolicies"]:
                result.append(
                    {
                        "stack": role["stack"],
                        "function": role["function"],
                        "policy": policy["PolicyName"],
                    }
                )

    return result

list_functions()
