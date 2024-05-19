# Dynamic Lead Handling System

## Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   python -c "import asyncio; from database import init_db; asyncio.run(init_db())"
   python workflow_executor.py
   ```
2. Configuration
## Workflows
Workflows are defined in the workflows.yaml file. Each workflow consists of:

* lead_source: The source of the lead (e.g., Salesforce, Hubspot, Facebook).
* persona: The persona to be used for communication.
* actions: The actions to be performed (e.g., send_message).
* output_channel: The channel through which the message is sent (e.g., Whatsapp, Email, Messenger).