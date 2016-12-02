def initialize_mysql_connector(hostname:str,
                               user_name:str,
                               password:str,
                               dbname:str):
    """
    """
    import MySQLdb
    conn = MySQLdb.connect(hostname, user_name, password, dbname)
    return conn


def initialize_pymysql_connector(hostname:str,
                                 user_name:str,
                                 password:str,
                                 dbname:str):
    import pymysql.cursors
    # MySQLに接続する
    connection = pymysql.connect(host=hostname,
                                 user=user_name,
                                 password=password,
                                 db=dbname,
                                 charset='utf8')
    return connection
