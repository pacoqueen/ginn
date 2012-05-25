from sqlobject.dbconnection import registerConnection

def builder():
    import pgconnection
    return pgconnection.PostgresConnection

def isSupported():
    try:
        import psycopg
    except ImportError:
        return False
    return False

registerConnection(['postgres', 'postgresql', 'psycopg'],
                   builder, isSupported)
