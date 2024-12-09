import asyncio
import os
import re

from pyzeebe import ZeebeWorker, Job, create_camunda_cloud_channel

# IMPORTANT:
# 
# Create your API credentials in camunda cloud first and download the credentials.
# The download file is a txt-file that holds export statements for setting the following environment variables:
#
# export ZEEBE_ADDRESS='xxxxxxxx.bru-2.zeebe.camunda.io:443'
# export ZEEBE_CLIENT_ID='yyyyyyyyy'
# export ZEEBE_CLIENT_SECRET='zzzzzzzzzzz'
# export ZEEBE_AUTHORIZATION_SERVER_URL='https://login.cloud.camunda.io/oauth/token'


zeebe_client_id = os.environ.get('ZEEBE_CLIENT_ID')
assert zeebe_client_id

zeebe_client_secret = os.environ.get('ZEEBE_CLIENT_SECRET')
assert zeebe_client_secret

zeebe_address = os.environ.get('ZEEBE_ADDRESS')
assert zeebe_address

camunda_region = os.environ.get('CAMUNDA_CLUSTER_REGION')
assert camunda_region

match = re.search(r'(?P<cluster_id>[^\.]*)\..*', zeebe_address)
camundacloud_cluster_id = match.group('cluster_id')
assert camundacloud_cluster_id

channel = create_camunda_cloud_channel(client_id=zeebe_client_id, client_secret=zeebe_client_secret,
                                       cluster_id=camundacloud_cluster_id, region=camunda_region)
worker = ZeebeWorker(channel)  # Create a zeebe worker


async def on_error(exception: Exception, job: Job):
    print(exception)
    await job.set_error_status(f"Failed to handle job {job}. Error: {str(exception)}")


# OTHER DEPARTMENT TASKS
@worker.task(task_type="send_request_to_procurement_department", exception_handler=on_error)
def send_request_to_procurement_department(department: str) -> dict:
    print("--------------------------")
    print(f"{department.upper()}")

    print("Sending procurement request to Procurement Department.")
    return {"output": "Sending procurement request to Procurement Department."}


# PROCUREMENT DEPARTMENT TASKS
@worker.task(task_type="submit_budget_increase_request", exception_handler=on_error)
def submit_budget_increase_request(budget: int, costs: int) -> dict:
    print("--------------------------")
    print("PROCUREMENT DEPARTMENT")

    print(f"Budget is not sufficient! Current budget is {budget} and the costs are {costs}!")
    requested_increase_amount = costs - budget
    print(f"Submit request to increase the current budget by {requested_increase_amount}!")
    return {"requestedIncreaseAmount": requested_increase_amount}


# FINANCIAL DEPARTMENT TASKS
@worker.task(task_type="approve_request", exception_handler=on_error)
def approve_request(requestedIncreaseAmount: int, budget: int) -> dict:
    print("--------------------------")
    print("FINANCIAL DEPARTMENT")

    print(f"Budget increase of {requestedIncreaseAmount} is approved.")
    print(f"New budget is: {budget + requestedIncreaseAmount}.")
    return {"output": f"New budget is: {budget + requestedIncreaseAmount}."}


@worker.task(task_type="reject_request", exception_handler=on_error)
def reject_request(requestedIncreaseAmount: int, budget: int) -> dict:
    print("--------------------------")
    print("FINANCIAL DEPARTMENT")

    print(f"Budget increase by {requestedIncreaseAmount} is not approved.")
    print(f"Budget stays at old amount of {budget}.")
    return {"output": f"Budget stays at old amount of {budget}."}


loop = asyncio.get_event_loop()
loop.run_until_complete(worker.work())
