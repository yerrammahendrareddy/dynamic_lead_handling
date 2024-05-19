import yaml
import logging
import asyncio
import aiohttp
import time
from database import init_db, save_lead, log_action

# Configure logging to write to a .gitignore
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("lead_processing.log"),
        logging.StreamHandler()
    ]
)


class WorkflowExecutor:
    def __init__(self, config_file):
        """
        Initialize the WorkflowExecutor with the given configuration .gitignore.

        Args:
            config_file (str): Path to the configuration .gitignore.
        """
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        """
        Load the workflow configuration from the configuration .gitignore.
        """
        try:
            with open(self.config_file, 'r') as file:
                self.config = yaml.safe_load(file)
        except Exception as e:
            logging.error(f"Failed to load configuration: {e}")
            self.config = {'workflows': []}

    def reload_config(self):
        """
        Reload the workflow configuration.
        """
        self.load_config()
        logging.info("Workflow configuration reloaded")

    async def process_lead(self, lead):
        """
        Process an incoming lead according to the workflow configuration.

        Args:
            lead (dict): The lead data to process.
        """
        if not self.validate_lead(lead):
            logging.error(f"Invalid lead data: {lead}")
            return

        lead_id = await save_lead(lead)
        for workflow in self.config['workflows']:
            if lead['source'] == workflow['lead_source']:
                await self.execute_workflow(lead, workflow, lead_id)
                return
        logging.info(f"No workflow found for lead source {lead['source']}")

    def validate_lead(self, lead):
        """
        Validate the lead data to ensure required fields are present.

        Args:
            lead (dict): The lead data to validate.

        Returns:
            bool: True if the lead is valid, False otherwise.
        """
        required_keys = {'source', 'data'}
        if not all(key in lead for key in required_keys):
            return False
        if not all(key in lead['data'] for key in {'name', 'email'}):
            return False
        return True

    async def execute_workflow(self, lead, workflow, lead_id):
        """
        Execute the workflow actions for a given lead.

        Args:
            lead (dict): The lead data.
            workflow (dict): The workflow configuration.
            lead_id (int): The ID of the lead.
        """
        try:
            for action in workflow['actions']:
                if action['type'] == 'send_message':
                    message = action['message'].format(**lead['data'])
                    await self.send_message(lead, workflow['output_channel'], message)
                    await log_action(lead_id, 'send_message', workflow['persona'], workflow['output_channel'])
                    logging.info(
                        f"Processed lead from {lead['source']} with persona {workflow['persona']} over {workflow['output_channel']}")
        except Exception as e:
            logging.error(f"Error executing workflow: {e}")

    async def send_message(self, lead, channel, message):
        """
        Simulate sending a message through the specified output channel.

        Args:
            lead (dict): The lead data.
            channel (str): The output channel.
            message (str): The message to send.
        """
        async with aiohttp.ClientSession() as session:
            try:
                # Simulate sending a message through the specified output channel
                logging.info(f"Sending message to {lead['data']['email']} via {channel}: {message}")
                # Here you can implement actual API calls to messaging services
            except Exception as e:
                logging.error(f"Error sending message: {e}")


if __name__ == "__main__":
    from lead_simulator import simulate_lead

    executor = WorkflowExecutor('workflows.yaml')


    async def main():
        """
        Main function to initialize the database and process incoming leads.
        """
        await init_db()
        try:
            async for lead in simulate_lead():
                await executor.process_lead(lead)
                await asyncio.sleep(0.5)
                # Simulate periodic reloading of the configuration .gitignore
                if time.time() % 10 < 0.5:
                    executor.reload_config()
        except asyncio.CancelledError:
            logging.info("Task cancelled")
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received, stopping lead processing")
        finally:
            await asyncio.sleep(0.1)  # Ensure all tasks are properly cancelled


    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Stopped by user")
