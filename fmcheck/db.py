import os
import sqlite3
import logging
import time


def createDb(dbname):
    '''Create Db file or Open Db file if exists'''
    dbPath=os.curdir +'/' + dbname  + '.db'
    conn = sqlite3.connect(dbPath)
    logging.debug("Opened DB connection to %s", dbPath)
    cur = conn.cursor()
    return cur, conn

def createTable(dbcur,tbname, tbstr1):
    '''dbcur :  Cusrsor retruned by createDb() to create Table within opened database
       tbname : Table Name
       kwargs : dictionary of column_name: data_type
       columnStr = Returns comma separated string of created Cloumns'''
    tbStr= "CREATE TABLE IF NOT EXISTS {} ({});".format(tbname, tbstr1)
    logging.debug("Table String is %s", tbStr)
    dbcur.execute(tbStr)
    logging.debug("Table %s created successfully", tbname)

def enterTabledata(dbcur, dbconn,tbname, columnStr, *args):
    '''args: tuple of variables correponding to coulm'''
    InsertStr = "INSERT INTO {} ({})  VALUES (?,?,?,?)".format(tbname,columnStr)
    logging.debug("Insert String is %s", InsertStr)
    dbcur.execute(InsertStr, args)
    dbconn.commit()

def selectTable(dbcur,tbname, columnStr):
    fetchStr = "SELECT {} from {}".format(columnStr,tbname)
    logging.debug("Select String is %s", fetchStr)
    listofTablerows = dbcur.execute(fetchStr)
    return listofTablerows

def deleteTable(dbcur,dbconn,dbname,tbname):
    deleteStr = "DROP TABLE {}.{};".format(dbname,tbname)
    logging.debug("Delete String is %s", deleteStr)
    dbcur.execute(deleteStr)
    dbconn.commit()

def dbClose(dbcur,dbconn):
    dbconn.commit()
    dbcur.close()
    dbconn.close()
