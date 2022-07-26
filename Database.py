from sqlalchemy import create_engine, MetaData, Table, Column, String


def setup():
    sqlite_engine = create_engine('sqlite:///database.db', echo=False)
    meta = MetaData()
    table = Table(
        'users', meta,
        Column('discord_id', String, primary_key=True),
        Column('access_token', String),
        Column('pocket_username', String),
    )
    meta.create_all(sqlite_engine)
    connection = sqlite_engine.connect()
    return sqlite_engine, table, connection


engine, users, conn = setup()


def add_user(discord_id, access_token, pocket_username):
    insert_user = users.insert().values(discord_id=str(
        discord_id), access_token=str(access_token), pocket_username=str(pocket_username))
    result = conn.execute(insert_user)


def get_user(discord_id):
    query = users.select().where(users.c.discord_id == str(discord_id))
    result = conn.execute(query)
    row = result.fetchone()
    return row


def is_in_db(discord_id):
    query = users.select().where(users.c.discord_id == str(discord_id))
    result = conn.execute(query)
    row = result.fetchone()
    return True if row else False
