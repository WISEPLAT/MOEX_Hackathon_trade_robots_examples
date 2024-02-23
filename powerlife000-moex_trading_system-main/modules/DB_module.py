#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class DB():
    
    def con(self):
        import psycopg2    
        return psycopg2.connect(
            host=self.db_host,
            database=self.db_database,
            user=self.db_user,
            password=self.db_password
        )
    
    def __init__(self, config):
        import psycopg2
        
        self.db_host=config.db_host
        self.db_database=config.db_database
        self.db_user=config.db_user
        self.db_password=config.db_password
        
        try:
            self.connection = self.con()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)      
            
    def execute(self, sql, data = None):
        import psycopg2
        try:
            #Проверяем наличие соединения
            if self.connection.closed == 1:
                #переподключаемся при отсутствии соединения
                self.connection = self.con()
            
            if self.connection.closed == 0:
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
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
    def executemany(self, sql, data):
        import psycopg2
        try:
            #Проверяем наличие соединения
            if self.connection.closed == 1:
                #переподключаемся при отсутствии соединения
                self.connection = self.con()
                
            if self.connection.closed == 0:
                cursor = self.connection.cursor()
                cursor.executemany(sql, data)
                try:
                    result = cursor.fetchall()
                except:
                    result = []
                self.connection.commit()
                cursor.close()
                return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
    def close(self):
        if self.connection.closed == 0:
            self.connection.close()
            print("DB connection is closed")

