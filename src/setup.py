from flask import Flask
import mysql.connector

from config import Config, DatabaseConfig, DevelopmentConfig

db_consts = {
    "CHARSET" : "utf8mb4"
}

def setup():
    app = Flask(__name__)

    # set up config #todo: Add environment cases
    app.config.from_object(DevelopmentConfig)

    # set up the database
    setup_db(DevelopmentConfig()) # todo: Manage environments ? wrap setup in conditional depending on os.env['ENVIRONMENT']

    return app




# todo: Move this to a separate setup location
def setup_db(conf: Config):
    # 1. get a connection
    conn = get_setup_connection(conf.DATABASE)

    # todo: Define a referential services table, with descriptions and more, to be used in display ref.service
    # todo: Define a referential table for possible activities ref.activity

    db_name = conf.DATABASE.DATABASE_NAME

    with conn.cursor() as cursor:
        # 2. Create database
        # todo: Following two statements might be prone to sql injections
        cursor.execute(
            f"Create database if not exists {db_name} CHARACTER SET {db_consts['CHARSET']} COLLATE utf8mb4_unicode_ci;")
        cursor.execute(f"USE {db_name}")  # todo: database name
        # 4. Create the necessary tables
        cursor.execute(f"""            
            CREATE TABLE IF NOT EXISTS leads (
                id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                num VARCHAR(30) NOT NULL,
                phone_id VARCHAR(50) NOT NULL,
                state VARCHAR(30),
                started_at DATETIME,
                ended_at DATETIME,
                in_casa BOOLEAN,
                service VARCHAR(100),
                activity VARCHAR(100),
                is_organic BOOLEAN,
                lang VARCHAR(2),
                is_complete BOOLEAN
            ) CHARACTER SET {db_consts['CHARSET']} COLLATE utf8mb4_unicode_ci;
            """)
    conn.close()


def get_setup_connection(db_conf: DatabaseConfig):
    conn = mysql.connector.connect(
        host=db_conf.HOST,
        user=db_conf.USER,
        password=db_conf.PASSWORD,
        charset=db_consts['CHARSET']
    )
    return conn





