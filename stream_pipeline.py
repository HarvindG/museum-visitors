# pylint: disable=C0303
"""
Python script that accesses static data, prepares it for upload, 
and finally sends the data to the database for storage.
"""

import json
import logging
from datetime import datetime
from os import environ

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from confluent_kafka import Consumer


ASSIST_OR_EM_REQUEST = -1
ASSIST_REQUEST = 0


def get_database_connection() -> connection:
    """Return a connection our database"""
    return connect(
                    user = environ["DATABASE_USERNAME"],
                    host = environ["DATABASE_IP"],
                    port = environ["DATABASE_PORT"],
                    database = environ["DATABASE_NAME"],
                    password = environ["DATABASE_PASSWORD"],
                    cursor_factory = RealDictCursor
                    )


def get_kafka_connection() -> Consumer:
    """Return a connection to the data stream"""
    return Consumer({
        "bootstrap.servers": environ["BOOTSTRAP_SERVERS"],
        "group.id": environ["GROUP"],
        "auto.offset.reset": environ["AUTO_OFFSET"],
        'security.protocol': environ["SECURITY_PROTOCOL"],
        'sasl.mechanisms': environ["SASL_MECHANISM"],
        'sasl.username': environ["USERNAME"],
        'sasl.password': environ["PASSWORD"]                                                         
    })


def upload_assistance_data(conn: connection, data: list[str]) -> None:
    """Writes assistance data entries to the assistance table in the database."""
    query = """
        INSERT INTO assistance_interaction
            (assistance_timestamp,
            exhibit_code)
        VALUES (%s, %s)
        ;
    """

    with conn.cursor() as cur:
        cur.execute(query, (data[0], data[1]))

    conn.commit()


def upload_emergency_data(conn: connection, data: list[str]) -> None:
    """Writes emergency data entries to the emergency table in the database."""
    query = """
        INSERT INTO emergency_interaction
            (emergency_timestamp,
            exhibit_code)
        VALUES (%s, %s)
        ;
    """

    with conn.cursor() as cur:
        cur.execute(query, (data[0], data[1]))

    conn.commit()


def upload_rating_data(conn: connection, data: list[str]) -> None:
    """Writes rating data entries to the rating table in the database."""   
    query = """
        INSERT INTO rating_interaction
            (rating_timestamp,
            exhibit_code,
            rating_value)
        VALUES (%s, %s, %s)
        ;
    """

    with conn.cursor() as cur:
        cur.execute(query, (data[0], data[1], data[2]))
    conn.commit()


def validate_msg(msg: dict)->bool:
    """Check that incoming data is in correct format and log erroneous data"""

    primary_keys = ['at', 'site', 'val']
    valid_site_ids = ['0','1','2','3','4','5']
    valid_vals = [-1, 0, 1, 2, 3, 4]

    if all(key in msg for key in primary_keys):
        
        try: 
            datetime.fromisoformat(msg['at'])
        except:
            logging.debug('Incorrect date format: ' + msg['at'])
            return False

        if msg['site'] not in valid_site_ids:
            logging.debug('Invalid site ID: ' + msg['site'])
            return False

        if msg['val'] in valid_vals:
            
            if msg['val'] == -1:   
                try:
                    if msg['type'] not in [0, 1]:
                        logging.debug('Invalid type ID: ' + str(msg['type']))
                        return False
                except KeyError:
                    logging.debug('Type ID not provided')
                    return False 
                
            elif msg['val'] >= 0:
                if 'type' in msg:
                    logging.debug("Type ID shouln't be provided")
                    return False 
            
            return True
        
    logging.debug("Incomplete dataset")
    return False


def consume_messages(cons:Consumer, conn:connection)-> None:
    """Reads data coming in from data stream and inputs into database"""
    
    while True:
        message = cons.poll(1)

        if message:
            message_content = json.loads(message.value().decode())
            
            if validate_msg(message_content):  
                filtered_data = list(message_content.values())

                if int(filtered_data[2]) == ASSIST_OR_EM_REQUEST:
                    if int(filtered_data[3]) == ASSIST_REQUEST:
                        upload_assistance_data(conn, filtered_data)
                    else:
                        upload_emergency_data(conn, filtered_data)
                elif  0 <= int(filtered_data[2]) <= 4:
                    upload_rating_data(conn, filtered_data)


if __name__ == "__main__":
    
    load_dotenv()

    logging.basicConfig(filename='erroneous_data.log', encoding='utf-8', level=logging.DEBUG)
    # Connect to AWS RDS 
    db_conn = get_database_connection() 
    # Connect to data stream
    consumer = get_kafka_connection()
    # Isolate messages coming from desired topic and log into database
    consumer.subscribe([environ["TOPIC"]])
    consume_messages(consumer, db_conn)