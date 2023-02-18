"""Database Functions"""
import sqlite3

try:
    print('trying to connect to resources/data.sql')
    connection = sqlite3.connect('resources/data.sql')
except FileNotFoundError:
    connection = sqlite3.connect('../resources/data.sql')

cursor = connection.cursor()

def drop_table():
    """Delete Discord table"""
    cursor.execute('DROP TABLE IF EXISTS discord')

def create_table():
    """Create table"""
    # cursor.execute('''CREATE TABLE competitions (current_comp text)''')
    cursor.execute('''CREATE TABLE discord (token text)''')

def create_table_rankings():
    """Create rankings table"""
    try:
        cursor.execute('''DROP TABLE IF EXISTS rankings''')
        cursor.execute('''CREATE TABLE rankings (name text, points real)''')
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()

def create_table_payments():
    """Create payments table"""
    try:
        cursor.execute('''DROP TABLE IF EXISTS payments''')
        cursor.execute('''CREATE TABLE payments (mod text, recipient text, \
            amount text, date text, imageUrl text)''')
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()

def create_table_members():
    """Create members table"""
    try:
        print('Creating table: members')
        cursor.execute('''DROP TABLE IF EXISTS members''')
        cursor.execute('''CREATE TABLE members\
            (id text PRIMARY KEY, display_name text, top_role text, permissions text,\
                roles text, content text, consultant text)''')
        print('CREATE TABLE members')
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()


def insert_members(user_id, display_name, top_role, permissions, roles, \
    content, consultant):
    """Insert or replace new member"""
    try:
        sql = 'INSERT OR REPLACE INTO members VALUES (?, ?, ?, ?, ?, ?, ?)'
        args = (user_id, display_name, top_role, \
            permissions, roles, content, consultant)
        cursor.execute(sql, args)
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()

def get_members():
    """Select all members from members table"""
    try:
        sql = 'SELECT * FROM members'
        cursor.execute(sql)
    except (connection.error, sql.ProgrammingError, sql.connection) as err:
        print(f'error writing to database: {err}')
    finally:
        connection.commit()
    return cursor.fetchall()

def insert_pets(attachment_id, author, attachment_url, created_at):
    """Insert or replace new pet entry"""
    try:
        sql = 'INSERT OR REPLACE INTO pets VALUES (?, ?, ?, ?)'
        args = (attachment_id, author, attachment_url, created_at)
        cursor.execute(sql, args)
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()


def get_pets():
    """Get mappings of mentors for given content_type"""
    try:
        sql = 'SELECT * FROM pets'
        cursor.execute(sql)
    except (connection.error, sql.ProgrammingError, sql.connection) as err:
        print(f'error writing to database: {err}')
    finally:
        connection.commit()
    return cursor.fetchall()

def insert_mappings(item_id, item_name, image_url):
    """Insert or replace new member"""
    try:
        sql = 'INSERT OR REPLACE INTO mapping VALUES (?, ?, ?)'
        args = (item_id, item_name, image_url)
        cursor.execute(sql, args)
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()


def get_mappings():
    """Get mappings of mentors for given content_type"""
    try:
        sql = 'SELECT * FROM mapping'
        cursor.execute(sql)
    except (connection.error, sql.ProgrammingError, sql.connection) as err:
        print(f'error writing to database: {err}')
    finally:
        connection.commit()
    return cursor.fetchall()

def get_user_id_by_display_name(display_name):
    """Get user id from members by display_name"""
    try:
        sql = f'Select id from members where display_name = "{display_name}"'
        cursor.execute(sql)
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()
    return cursor.fetchone()[0]

def update_mentor(display_name, content, consultant):
    """Update Mentor information"""
    try:
        sql = 'UPDATE members SET content = ?, consultant = ? \
            where display_name = ?'
        args = content, consultant, display_name
        cursor.execute(sql, args)
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()

def update_member_nickname(user_id, after):
    """Update Mentor information"""
    try:
        sql = 'UPDATE members SET display_name = ? WHERE id = ?'
        args = f'{after}', f'{user_id}'
        cursor.execute(sql, args)
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        print(f'Nickname updated {after} for {user_id}')
        connection.commit()

def update_member_roles(user_id, new_roles):
    """Update Mentor information"""
    try:
        sql = 'UPDATE members SET roles = ? WHERE id = ?'
        args = f'{new_roles}', f'{user_id}'
        cursor.execute(sql, args)
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()

def get_mentors_for_content():
    """Get list of mentors for given content_type"""
    try:
        print('Get list of mentors for given content_type')
        sql = 'SELECT display_name, content FROM members WHERE roles LIKE \
            "%mentor%"'
        cursor.execute(sql)
    except (connection.error, sql.ProgrammingError, sql.connection) as err:
        print(f'error writing to database: {err}')
    finally:
        connection.commit()
    return cursor.fetchall()

def get_member_permissions(display_name):
    """Get discord permissions for given display_name"""
    try:
        sql = 'SELECT permissions FROM members WHERE display_name=?'
        args = (display_name,)
        cursor.execute(sql, args)
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()
    return cursor.fetchone()[0]

def delete_members():
    """Delete all memeber records"""
    try:
        sql = 'DELETE FROM members'
        cursor.execute(sql)
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()

def insert_payments(mod, recipient, amount, date, image_url):
    """Insert into payments table"""
    try:
        sql = 'INSERT INTO payments VALUES (?, ?, ?, ?, ?)'
        args = (mod, recipient, amount, date, image_url)
        cursor.execute(sql, args)
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()

def check_if_user_exists_in_rankings(name):
    """Check if user exists in rankings"""
    sql = 'SELECT count(*) FROM rankings WHERE name=?'
    args = (name,)
    cursor.execute(sql, args)
    if cursor.fetchone()[0] == 0:
        return False
    else:
        return True

def insert_rankings(name, points):
    """Insert a new entry into rankings"""
    try:
        sql = 'INSERT INTO rankings VALUES (?, ?)'
        args = (name, points)
        cursor.execute(sql, args)
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()

def update_rankings(name, points):
    """Update rankings"""
    try:
        sql = 'UPDATE rankings SET points = points + ? WHERE name = ?'
        args = (points, name)
        cursor.execute(sql, args)
    except connection.error:
        print(f'error writing to database: {connection.error}')
    finally:
        connection.commit()

def get_rankings():
    """Return ordered rankings"""
    return cursor.execute('SELECT * FROM rankings ORDER BY points DESC')

def insert_competitions(cur, value):
    """Insert into competitions"""
    cur.execute('INSERT INTO competitions VALUES (?)', [value])

def get_current_competition():
    """Get current ongoing competition"""
    return cursor.execute('SELECT * FROM competitions').fetchall()[0][0]

def set_current_competition(value):
    """Set current competition"""
    sql = 'UPDATE competitions SET current_comp = ? WHERE current_comp = ?'
    args = (value, get_current_competition())
    cursor.execute(sql, args)

class Rankings:
    """Rankings object"""
    def __init__(self, name, score):
        self.name = name
        self.score = score

def rankings_as_list():
    """Return list of rankings"""
    rankings_dict = []
    for entry in get_rankings():
        rankings_dict.append(Rankings(entry[0], entry[1]))
    return rankings_dict

ranking_list = rankings_as_list()
