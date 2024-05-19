import aiosqlite


async def init_db():
    """
    Initialize the SQLite database with required tables.
    """
    async with aiosqlite.connect('leads.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                name TEXT,
                email TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER,
                action TEXT,
                persona TEXT,
                output_channel TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads (id)
            )
        ''')
        await db.commit()


async def save_lead(lead):
    """
    Save a lead to the database.

    Args:
        lead (dict): The lead data to save.

    Returns:
        int: The ID of the saved lead.
    """
    async with aiosqlite.connect('leads.db') as db:
        cursor = await db.execute('''
            INSERT INTO leads (source, name, email) VALUES (?, ?, ?)
        ''', (lead['source'], lead['data']['name'], lead['data']['email']))
        await db.commit()
        return cursor.lastrowid


async def log_action(lead_id, action, persona, output_channel):
    """
    Log an action taken on a lead.

    Args:
        lead_id (int): The ID of the lead.
        action (str): The action taken.
        persona (str): The persona used.
        output_channel (str): The output channel used.
    """
    async with aiosqlite.connect('leads.db') as db:
        await db.execute('''
            INSERT INTO logs (lead_id, action, persona, output_channel) VALUES (?, ?, ?, ?)
        ''', (lead_id, action, persona, output_channel))
        await db.commit()
