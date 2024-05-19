import random
import asyncio

lead_sources = ['Salesforce', 'Hubspot', 'Facebook']


async def simulate_lead():
    """
    Asynchronously simulate incoming leads from different sources.
    Yields:
        dict: A simulated lead containing source and data (name and email).
    """
    while True:
        lead = {
            'source': random.choice(lead_sources),
            'data': {'name': 'yerram mahendra', 'email': 'yerram.mahendra@example.com'}
        }
        yield lead
        await asyncio.sleep(1)


if __name__ == "__main__":
    async def main():
        async for lead in simulate_lead():
            print(lead)


    asyncio.run(main())
