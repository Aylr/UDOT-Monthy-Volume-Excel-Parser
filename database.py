#!/usr/bin/env python
import records


SITE_TABLE = 'sites'
VOLUME_TABLE = 'volume_measurements'

def setup_db_client(db_filename):
    # type: (string) -> records.Database
    """
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
    :param db: database connection
    :param table_name: string
    :return:
    """
    if type(db) is records.Database and type(table_name):
        results = db.query('SELECT * FROM "{}"'.format(table_name))

        return results


def recreate_tables(db):
    if type(db) is not records.Database:
        return

    db.query('DROP TABLE IF EXISTS {};'.format(SITE_TABLE))
    db.query('DROP TABLE IF EXISTS {};'.format(VOLUME_TABLE))
    db.query('CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT, site_name TEXT, site_location TEXT);'.format(SITE_TABLE))
    db.query('CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp INT, volume INT, site_id INT, FOREIGN KEY (site_id) REFERENCES sites(id));'.format(VOLUME_TABLE))


def insert_site(db, site_name, site_location):
    if type(db) is not records.Database:
        return

    if does_site_exist(db, site_name) is False:
        db.query('INSERT INTO {} (site_name, site_location) VALUES (:site_name, :site_location)'.format(SITE_TABLE), site_name=site_name, site_location=site_location)
    else:
        print('Site {} exists, skipping'.format(site_name))


def does_site_exist(db, site_name):
    if type(db) is not records.Database:
        return

    result = db.query('SELECT * FROM ' + SITE_TABLE + ' WHERE site_name = :site_name;', site_name=site_name)
    for row in result:
        print row
    return len(result.all()) is not 0


def main():
    # print 'Recreating database'
    # db = setup_db_client('udot.db')
    # recreate_tables(db)
    db = setup_db_client('udot.db')

    insert_site(db, 'stuff', 'stuff')
    insert_site(db, 'stuff2', 'stuff2')

    print does_site_exist(db, 'stuff')


if __name__  == '__main__':
    main()