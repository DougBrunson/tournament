import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection.
    Args:
        None
    Returns:
        DB: connection oject
        conn: cursor object
    """
    try:
        DB = psycopg2.connect('dbname=tournament')
        conn = DB.cursor()
        return DB, conn
    except Exception as e:
        print "Database connection failed with error: " + str(e)


def disconnect(db, commit=False):
    """Disconnect database and commit changes if true is passed
    Args: 
        db: connection object
        commit(bool): boolean commit 
    """
    try:
        if commit:
            db.commit()
    except Exception, e:
        db.rollback()
        print "Database transaction failed with error: " + str(e)
        print "\nDatabase rolled back"
    finally:
        db.close()
