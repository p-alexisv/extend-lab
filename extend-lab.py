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
        print('extend-lab.py -l <lab> -d <domain>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('extend-lab.py -l <lab> -d <domain>')
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
        rsv.id,
        l.id as lab_fk,
        l.lab_number,
        s.slot_number,
        l.lab_description,
        tm.name,
        tm.email,
        rsv.last_reservation_modification_date,
        rsv.purpose,
        rsv.end_of_reservation_date,
        rsv.number_of_renews,
        rsv.terminated
    FROM 
        reservation rsv,
        lab l,
        team_member tm,
        slot s
    WHERE 
        rsv.clean_status = 'NONE' 
        AND 
        l.lab_number = %s
        AND
        s.slot_number = %s
        AND
        rsv.lab_fk = l.id
        AND
        rsv.team_member_fk = tm.id
        AND
        l.slot_fk = s.id
        AND
        rsv.terminated = 0
    """ % (labno, slotno)

    cols,qres = execute_read_query(connection, query)
    eord = None
    nor = None
    rsvid = None
    for r in qres:
        for i, rv in enumerate(r):
            print(cols[i]," : ", rv)
            if cols[i] == "id": rsvid = rv
            if cols[i] == "end_of_reservation_date": eord = rv
            if cols[i] == "number_of_renews": nor = rv
        print("\n")
    if rsvid is None:
        print("Nothing to extend!  Bye!")
        return
    proceed = input("Do you want to extend this lab? (y/n)")
    if proceed == "y":
        print("Ni")
        if (rsvid is not None and eord is not None and nor is not None):
            print("Need to add 7 days to %s" % eord)
            print("need to add 1 to %s" % nor)
            #yyyy, mm, dd = eord.split("-")
            #eordo = date(yyyy, mm, dd)
            newdate = eord + timedelta(weeks=1)
            newnor = nor + 1
            print("new date: %s" % newdate)
            print("newnor: %s" % newnor)
            updateSql = """
UPDATE 
    reservation
SET
    end_of_reservation_date = "%s",
    number_of_renews = %s
WHERE
    id = %s
""" % (newdate, newnor, rsvid)
            print("Update SQL: %s" % updateSql)
            proceedUpdate = input("Proceed? (y/n)")
            if proceedUpdate == "y":
                print("Ok.  Extending...")
                execute_query(connection, updateSql)
            else:
                print("Bye!")
        else:
            print("Oh, shrubbery!")
    else:
        print("Bye!")
        return 0

if __name__ == "__main__":
    main()


"""
UPDATE `reservation` SET `end_of_reservation_date` = '2022-02-25', `number_of_renews` = '3', `terminated` = b'0' WHERE `reservation`.`id` = 1461 
"""
