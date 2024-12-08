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


@worker.task(task_type="send_request_to_procurement_department", exception_handler=on_error)
def send_request_to_procurement_department(department: str) -> dict:
    print(f"Sending procurement request from {department}!")
    return {"output": f"Sending procurement request from {department}!"}


@worker.task(task_type="submit_budget_increase_request", exception_handler=on_error)
def submit_budget_increase_request(budget: str) -> dict:
    print(f"Budget is not sufficient! Current budget is {budget}")
    # print(f"Submit request to increase the current budget by {requestedIncreaseAmount}!")
    return {"output": f"Current budget: {budget}"}

'''
@worker.task(task_type="approve_request", exception_handler=on_error)
def approve_request(requestedIncreaseAmount: str, budget: str) -> dict:
    print(f"New budget is {budget + requestedIncreaseAmount}")
    # print(f"Submit request to increase the current budget by {requestedIncreaseAmount}!")
    return {"output": f"New budget: {budget + requestedIncreaseAmount}"}
'''


loop = asyncio.get_event_loop()
loop.run_until_complete(worker.work())
