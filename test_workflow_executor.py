import pytest
import asyncio
from workflow_executor import WorkflowExecutor
from database import init_db

@pytest.fixture(scope='module')
async def setup_database():
    """
    Asynchronous fixture to initialize the database before running the tests.
    """
    await init_db()

@pytest.fixture
def executor(setup_database):
    """
    Fixture to create a WorkflowExecutor instance.
    """
    return WorkflowExecutor('workflows.yaml')

@pytest.mark.asyncio
async def test_process_salesforce_lead(executor):
    """
    Test processing a lead from Salesforce.
    """
    lead = {'source': 'Salesforce', 'data': {'name': 'yerram mahendra', 'email': 'yerram.mahendra@example.com'}}
    await executor.process_lead(lead)

@pytest.mark.asyncio
async def test_process_hubspot_lead(executor):
    """
    Test processing a lead from Hubspot.
    """
    lead = {'source': 'Hubspot', 'data': {'name': 'Jane mahendra', 'email': 'jane.mahendra@example.com'}}
    await executor.process_lead(lead)

@pytest.mark.asyncio
async def test_process_facebook_lead(executor):
    """
    Test processing a lead from Facebook.
    """
    lead = {'source': 'Facebook', 'data': {'name': 'Jake mahendra', 'email': 'jake.mahendra@example.com'}}
    await executor.process_lead(lead)

@pytest.mark.asyncio
async def test_process_unknown_source(executor):
    """
    Test processing a lead from an unknown source.
    """
    lead = {'source': 'Unknown', 'data': {'name': 'Jake mahendra', 'email': 'jake.mahendra@example.com'}}
    await executor.process_lead(lead)

def test_reload_config(executor):
    """
    Test reloading the configuration.
    """
    executor.reload_config()
