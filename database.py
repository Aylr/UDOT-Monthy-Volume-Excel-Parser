#!/usr/bin/env python
import records

SITE_TABLE = 'sites'
VOLUME_TABLE = 'volume_measurements'


def setup_db_client(db_filename):
    # type: (str) -> records.Database
    """
    Sets up a db connection
    :param db_filename: name of the db file to connect to
    :return:
    :rtype: records.Database
    """
    db = records.Database('sqlite:///{}'.format(db_filename))

    if type(db) == records.Database:
        return db


def get_all_records_from_table(db, table_name):
    # type: (records.Database, str) -> List[records.Record]
    """
    Retrieves all records from a given table
    :param db: database connection
    :param table_name: string
    :return:
    """
    query = 'SELECT * FROM {}'.format(table_name)
    results = db.query(query)

    return results.all()


def recreate_tables(db):
    # type: (records.Database) -> None
    """
    Drops tables and recreates
    :param db: the database connection
    """
    db.query('DROP TABLE IF EXISTS {};'.format(SITE_TABLE))
    db.query('DROP TABLE IF EXISTS {};'.format(VOLUME_TABLE))
    db.query('DROP INDEX IF EXISTS site_name_index;')
    db.query('DROP INDEX IF EXISTS volume_site_timestamp;')
    db.query('CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT, site_name TEXT, site_location TEXT);'.format(
        SITE_TABLE))
    db.query(
        'CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp INT, volume INT, site_id INT, \
        FOREIGN KEY (site_id) REFERENCES sites(id));'.format(VOLUME_TABLE))
    db.query('CREATE INDEX IF NOT EXISTS site_name_index ON {} (site_name);'.format(SITE_TABLE))
    db.query('CREATE INDEX IF NOT EXISTS volume_site_timestamp ON {} (site_id, timestamp);'.format(VOLUME_TABLE))


def insert_site(db, site_name, site_location):
    # type: (records.Database, str, str) -> int
    """
    Inserts a site if it hasn't already been.
    :param db: connected database
    :param site_name: Name of the site
    :param site_location: Location
    :return: site id
    """
    if does_site_exist(db, site_name) is False:
        query = 'INSERT INTO {} (site_name, site_location) VALUES (:site_name, :site_location)'.format(SITE_TABLE)
        db.query(query, site_name=site_name, site_location=site_location)

    return find_site_id_by_name(db, site_name)


def find_site_id_by_name(db, site_name):
    # type: (records.Database, str) -> int
    """
    Finds a site by name
    :param db:
    :param site_name: Name to search for
    :return: id if found
    """
    query = 'SELECT id FROM {} WHERE site_name = :site_name'.format(SITE_TABLE)
    site = db.query(query, site_name=site_name)
    site_id = site[0].id

    return site_id


def insert_volume(db, timestamp, volume, site_name, site_location):
    # type: (records.Database, int, int, str, str) -> None
    """
    Inserts a volume record if it hasn't already been
    :param db:
    :param timestamp:
    :param volume:
    :param site_name:
    :param site_location:
    """
    if does_site_exist(db, site_name) is False:
        insert_site(db, site_name, site_location)

    site_id = find_site_id_by_name(db, site_name)

    volume_exists = does_volume_entry_exist(db, site_id, timestamp)

    if volume_exists is False:
        query = 'INSERT INTO {} (timestamp, site_id, volume) VALUES (:timestamp, :site_id, :volume)'.format(VOLUME_TABLE)
        db.query(query, timestamp=timestamp, site_id=site_id, volume=volume)


def does_site_exist(db, site_name):
    # type: (records.Database, str) -> bool
    """
    Checks if a site exists searching by name
    :param db:
    :param site_name:
    :return:
    """
    query = 'SELECT * FROM {} WHERE site_name = :site_name;'.format(SITE_TABLE)
    result = db.query(query, site_name=site_name)

    return len(result.all()) is not 0


def does_volume_entry_exist(db, site_id, timestamp):
    # type: (records.Database, int, int) -> bool
    """
    Checks if a volume entry exists searching by timestamp and site_id
    :param db:
    :param site_id:
    :param timestamp:
    :return:
    """
    query = 'SELECT * FROM {} WHERE site_id = :site_id AND timestamp = :timestamp;'.format(VOLUME_TABLE)
    result = db.query(query, site_id=site_id, timestamp=timestamp)

    return len(result.all()) is not 0


def main():
    db = setup_db_client('udot.db')
    recreate_tables(db)

    insert_site(db, 'stuff', 'stuff')
    insert_site(db, 'stuff', 'stuff')
    insert_site(db, 'stuff2', 'stuff2')

    insert_volume(db, 123, 400, 'stuff', 'stuff')
    insert_volume(db, 123, 400, 'stuff', 'stuff')
    insert_volume(db, 123, 400, 'stuff2', 'stuff2')
    insert_volume(db, 123, 400, 'stuff2', 'stuff2')


if __name__ == '__main__':
    main()
