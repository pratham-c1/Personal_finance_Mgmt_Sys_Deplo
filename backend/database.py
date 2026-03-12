import mysql.connector
from mysql.connector import pooling
import logging, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import Config

logger = logging.getLogger(__name__)
connection_pool = None

def init_pool():
    global connection_pool
    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="pf_pool",
            pool_size=5,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            autocommit=True,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            connection_timeout=30,
        )
        logger.info("DB pool initialized OK")
        return True
    except Exception as e:
        logger.error(f"DB pool init FAILED: {e}")
        return False

def get_connection():
    global connection_pool
    if not connection_pool:
        init_pool()
    return connection_pool.get_connection()

def execute_query(query, params=None, fetch=True):
    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        logger.error(f"Query error: {e} | SQL: {query}")
        raise
    finally:
        if cursor: cursor.close()
        if conn:   conn.close()

def execute_one(query, params=None):
    conn = cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        return cursor.fetchone()
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise
    finally:
        if cursor: cursor.close()
        if conn:   conn.close()
