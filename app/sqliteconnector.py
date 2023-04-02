import sqlite3
from datetime import datetime
from sqlite3 import Error
from loguru import logger
class SqliteConnector:
    def __init__(self):
        self.db_file = "config/appinfo.db"
        self.conn = None
        self.create_tables()

    def open_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            logger.error(str(e))

    def close_connection(self):
        try:
            self.conn.close()
        except Error as e:
            logger.error(str(e))

    def create_tables(self):
        self.open_connection()
        create_apps_table = """ CREATE TABLE IF NOT EXISTS apps (
                                    AppId text PRIMARY KEY,
                                    AppName text NOT NULL,
                                    AppURL text NOT NULL,
                                    AppImage text NOT NULL,
                                    LastChanged text NOT NULL
                                ); """


        try:
            c = self.conn.cursor()
            c.execute(create_apps_table) 
            c.close()
            self.conn.close()          
        except Error as e:
            logger.error(str(e))
   
    def add_app_info(self,AppId,AppName,AppURL,AppImage,LastChanged):
        try:
            Tunnel = (AppId,AppName,AppURL,AppImage,LastChanged,)
            self.open_connection()
            sql =  """ INSERT INTO apps(AppId,AppName,AppURL,AppImage,LastChanged) VALUES (?,?,?,?,?)"""
            cur = self.conn.cursor()
            cur.execute(sql,Tunnel)
            self.conn.commit()
            self.conn.close()
            return str(cur.lastrowid>0), "App info addedd successfully"
        except Error as e:
            logger.error(str(e))
            return False, str(e)

    def update_app_info(self,AppId,AppName,AppURL,AppImage,LastChanged):
        try:
            Tunnel = (AppName,AppURL,AppImage,LastChanged,AppId)
            self.open_connection()
            sql = ''' UPDATE apps
              SET AppName = ?,
                  AppURL = ?,
                  AppImage = ?,
                  LastChanged = ?
                  WHERE AppId = ?'''
            cur = self.conn.cursor()
            cur.execute(sql,Tunnel)
            self.conn.commit()
            self.conn.close()
            return str(cur.lastrowid>0), "App info updated successfully"
        except Error as e:
            logger.error(str(e))
            return False, str(e)

    def get_app_info_by_id(self, AppId):
        """
        Query tasks by priority
        :param conn: the Connection object
        :param priority:
        :return:
        """
        try:
            self.open_connection()
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM apps WHERE AppId=? Limit 1", (AppId,))
            rows = cur.fetchall()
            self.conn.close()
            return rows
        except Error as e:
            logger.error(str(e))
            return False, str(e)

    def is_app_info_exists(self,AppId):
        rows = self.get_app_info_by_id(AppId=AppId)
        return (True if rows else False)



  