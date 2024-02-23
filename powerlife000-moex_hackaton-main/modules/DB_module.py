#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class DB():
    
    def con(self):
        import mysql.connector
        return mysql.connector.connect(
            host=self.db_host,
            database=self.db_database,
            user=self.db_user,
            password=self.db_password
        )
    
    def __init__(self, config):
        from mysql.connector import Error
        
        self.db_host=config.db_host
        self.db_database=config.db_database
        self.db_user=config.db_user
        self.db_password=config.db_password
        
        try:
            self.connection = self.con()
        except Error as e:
            print("Error while connecting to MySQL", e)     
            
    
            
    def execute(self, sql, data = None):
        from mysql.connector import Error
        try:
            #Проверяем наличие соединения
            if self.connection.is_connected() != True:
                #переподключаемся при отсутствии соединения
                self.connection = self.con()
            
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                if data == None:
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, data)
                try:
                    result = cursor.fetchall()
                except:
                    result = []
                self.connection.commit()
                cursor.close()
                return result
        except Error as e:
            print("Error while connecting to MySQL", e)
            
    def executemany(self, sql, data):
        from mysql.connector import Error
        try:
            #Проверяем наличие соединения
            if self.connection.is_connected() != True:
                #переподключаемся при отсутствии соединения
                self.connection = self.con()
                
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.executemany(sql, data)
                try:
                    result = cursor.fetchall()
                except:
                    result = []
                self.connection.commit()
                cursor.close()
                return result
        except Error as e:
            print("Error while connecting to MySQL", e)
            
    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

