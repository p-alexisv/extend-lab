#!/usr/local/bin/python3

import mysql.connector
import sys, getopt

from mysql.connector import Error
from datetime import timedelta

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_read_query(connection, query):
    cursor = connection.cursor()
    cols = None
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cols = [description[0] for description in cursor.description]
        return cols,result
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def main():
    #labno = 24
    #slotno = 34
    labno = ''
    slotno = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hl:d:",["lab=","domain="])
    except:
        print("Exception!")
        print('free-lab.py -l <lab> -d <domain>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('free-lab.py -l <lab> -d <domain>')
            sys.exit()
        elif opt in ("-l", "--lab"):
            labno = arg
        elif opt in ("-d", "--domain"):
            slotno = arg
    print("Lab is %s" % labno)
    print("Domain is %s" % slotno)
    
    dbhost = "DBHOST"
    dbuser = "DBUSER"
    dbpass = "DBPASS"
    dbname = "service_instance_db"
    connection = create_connection(dbhost, dbuser, dbpass, dbname)
    if (connection == None):
        return -1
    query = """
    SELECT 
        l.id as lab_id,
        l.slot_fk,
        s.id as slot_id,
        rsv.id as reservation_id,
        rsv.lab_fk,
        rsv.terminated
    FROM 
        lab l,
        slot s,
        reservation rsv
    WHERE 
        l.lab_number = %s
        AND
        s.slot_number = %s
        AND
        s.id = l.slot_fk
        AND
        rsv.lab_fk = l.id
    """ % (labno, slotno)

    cols,qres = execute_read_query(connection, query)
    terminated = None
    labfk = None
    for r in qres:
        for i, rv in enumerate(r):
            print(cols[i]," : ", rv)
            if cols[i] == "terminated": terminated = rv
            if cols[i] == "lab_fk": labfk = rv
        print("\n")
    if labfk is None:
        print("Nothing to free!  Bye!")
        return
    if terminated == 1:
        print("Terminated is already 1.  Nothing to free!")
        return
    proceed = input("Do you want to free this lab? (y/n)")
    if proceed == "y":
        print("Ni")
        #if (rsvid is not None and eord is not None and nor is not None):
            #print("Need to add 7 days to %s" % eord)
            #print("need to add 1 to %s" % nor)
            #yyyy, mm, dd = eord.split("-")
            #eordo = date(yyyy, mm, dd)
            #newdate = eord + timedelta(weeks=1)
            #newnor = nor + 1
            #print("new date: %s" % newdate)
            #print("newnor: %s" % newnor)
        updateSql = """
UPDATE 
    `reservation`
SET
    `terminated` = 1
WHERE
    `terminated` = 0
    AND
    `lab_fk` = %s
""" % (labfk)
        print("Update SQL: %s" % updateSql)
        proceedUpdate = input("Proceed? (y/n)")
        if proceedUpdate == "y":
            print("Ok.  Freeing...")
            execute_query(connection, updateSql)
        else:
            print("Not proceeding with SQL update!")
    else:
        print("Not proceeding. Bye!")
        return 0

if __name__ == "__main__":
    main()


"""
UPDATE `reservation` SET `terminated` = 1 WHERE terminated = 0 and lab_fk = 22 
"""
