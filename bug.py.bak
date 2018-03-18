#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask,request,Response
from flask import send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import requests
import httplib
import json
import MySQLdb
import socket
import fcntl
import struct
from bson import json_util
import json


BUGZILLA_DATABASE_HOST = "bz3-db3.eng.vmware.com"
BUGZILLA_DATABASE_PORT = 3306
BUGZILLA_DATABASE_USER ="mts"
BUGZILLA_DATABASE_PW="mts"
BUGZILLA_DATABASE_DATABASE="bugzilla"

def pic_url(component):
    if component == 'osx':
        return 'pic1'
    else:
        return 'pic2'

def bug_color(priority):
    if priority == 'P0':
        return '#990033'
    elif priority == 'P1':
        return '#FF0033'
    else:
        return '#FFFFF'

def substr(string):
    if len(string) > 60:
        return string[0:59]+'...'
    else:
        return string

##test method for debug or search sth
def test():
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)

    cursor = bzdb_conn.cursor()

    #sql = """select bug_id, priority, bug_severity, short_desc from bugs where found_in_product_id='18' and found_in_version_id='4926' ORDER BY priority"""
    #sql = """select COLUMN_NAME from information_schema.COLUMNS where table_name = 'bugs_activity'""";
    #sql = """select * from bugs_activity where bug_id='1997211'"""
    sql = """select * from bugs where bug_id="1997211" ORDER BY priority"""
    #sql = """select * from groups"""
    #sql = """select reporter,count(reporter) from bugs where found_in_version_id="CART18FQ4" group by reporter order by reporter"""
    #sql = """select COLUMN_NAME from COLUMN_NAME from information_schema.COLUMNS where table_name = 'profiles'""";
    #sql = """select userid from profiles where login_name='zhaom'""";
    #sql = """select COLUMN_NAME from information_schema.COLUMNS where table_name = 'categories'""";
    #sql = """select * from categories where name= 'L10n Server'""";
    #sql = """select * from categories where name= 'Documentation' and product_id = '18'""" ;
    #sql = """select * from products where name= 'vdi'""";
    #sql = """select * from bug_severity where name= 'Critical'""";
    cursor.execute(sql)
    result= cursor.fetchall()
    print result

#Count bug by reporter
def count_by_person(foundin_id, phaselist):
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)
    cursor = bzdb_conn.cursor()
    print phaselist
    if len(phaselist)>1:
        sql = """select login_name,count(reporter) from bugs,profiles where bugs.reporter = profiles.userid  and bugs.found_in_version_id= '{0}' and bugs.found_in_phase_id in {1} group by bugs.reporter""".format(foundin_id, phaselist)
    else:
        sql = """select login_name,count(reporter) from bugs,profiles where bugs.reporter = profiles.userid  and bugs.found_in_version_id= '{0}' and bugs.found_in_phase_id= '{1}' group by bugs.reporter""".format(foundin_id, phaselist[0])
    cursor.execute(sql)
    bug_foundin = cursor.fetchall()
    result_json=json.dumps(bug_foundin)
    return result_json

def count_by_person_allphase(foundin_id):
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)
    cursor = bzdb_conn.cursor()
    sql = """select login_name,count(reporter) from bugs,profiles where bugs.reporter = profiles.userid  and bugs.found_in_version_id= '{0}' group by bugs.reporter""".format(foundin_id)
    cursor.execute(sql)
    bug_foundin = cursor.fetchall()
    result_json=json.dumps(bug_foundin)
    return result_json

def bug_cycle(bug_id):
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)
    cursor = bzdb_conn.cursor()
    sql = """select * from bugs_activity where bug_id='{0}'""".format(bug_id)
    cursor.execute(sql)
    update = cursor.fetchall()
    result_json=json.dumps(update,default=json_util.default)
    return result_json

#get foundin ID
def getFoundin(foundin_name):
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)
    cursor = bzdb_conn.cursor()
    sql = """select id from versions where name= '{0}' """.format(foundin_name)
    cursor.execute(sql)
    result= cursor.fetchall()
    result_json = json.dumps(result)
    print result_json
    array = json.loads(result_json)
    return array[0][0]

# get foundin phase
def getFoundinPhase(foundin_id, foundin_phase):
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)
    cursor = bzdb_conn.cursor()
    print foundin_phase
    if len(foundin_phase)>1:
        sql = """select id from phases where name in {0} and  version_id = '{1}' """.format(foundin_phase, foundin_id)
    else: 
        sql = """select id from phases where name = '{0}' and  version_id = '{1}' """.format(foundin_phase[0], foundin_id)
    cursor.execute(sql)
    result= cursor.fetchall()
    result_json = json.dumps(result)
    array = json.loads(result_json)
    phaselist = []
    for element in array:
        phaselist.append(element[0])
    for item in foundin_phase:
        if item == '': 
            phaselist.append('')
            break
    phaselist1 = tuple(phaselist)
    return phaselist1

def getCountbyPhase(foundin_id, foundin_phase):
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)
    cursor = bzdb_conn.cursor()
    print foundin_phase
    i18nbug = ('1800', '1742', '2451' , '736')
    if len(foundin_phase)>1:
        sql = """select count(*) from bugs where found_in_phase_id in {0} and  found_in_version_id = '{1}' and product_id = '18' and category_id not in {2}""".format(foundin_phase, foundin_id, i18nbug)
    else: 
        sql = """select count(*)  from bugs where found_in_phase_id = '{0}' and  found_in_version_id = '{1}' and product_id = '18' and category_id not in {2}""".format(foundin_phase[0], foundin_id, i18nbug)
    cursor.execute(sql)
    result= cursor.fetchall()
    return result

def getBugbyDate(foundin_id):
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)
    zdb_conn = MySQLdb.connect(host="bz3-db3.eng.vmware.com", port=3306, user="mts", passwd="mts", db="bugzilla")
    cursor = bzdb_conn.cursor()
    i18nbug = ('2451', '1800','1742', '736')
    # includes ('L10n Feature Pack', 'L10n Remote Client', 'L10n Server' 'Documentation')
    sql = """select creation_ts, bug_id from bugs where found_in_version_id = '{0}' and product_id = '18' and category_id not in {1} and cf_type = 'Defect'""".format(foundin_id, i18nbug)
    cursor.execute(sql)
    result= cursor.fetchall()
    result_json=json.dumps(result,default=json_util.default)
    return result_json

def getRegressionBug(foundin_id):
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)
    cursor = bzdb_conn.cursor()
    i18nbug = ('2451', '1800','1742', '736')
    sql = """select creation_ts, bug_id,cf_regression from bugs where found_in_version_id = '{0}' and product_id = '18' and category_id not in {1} and cf_type = 'Defect' and short_desc NOT LIKE '%[i18N%' and cf_regression = 'Yes'""".format(foundin_id, i18nbug)
    cursor.execute(sql)
    result= cursor.fetchall()
    result_json=json.dumps(result,default=json_util.default)
    return result_json

def getBugbyDateforTeam(foundin_id):
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)
    cursor = bzdb_conn.cursor()
    i18nbug = ('2451', '1800','1742', '736')
    #sql = """select login_name, creation_ts, bug_id, short_desc from bugs, profiles where bugs.assigned_to = profiles.userid and found_in_version_id = '{0}' and product_id = '18' and category_id not in {1}  and cf_type = 'Defect' and short_desc NOT LIKE '%[i18N%'""".format(foundin_id, i18nbug)
    #sql = """select login_name, creation_ts, bug_id from bugs, profiles where bugs.assigned_to = profiles.userid and found_in_version_id = '{0}' and product_id = '18' and category_id not in {1}  and bug_severity in ('critical', 'catastrophic') and priority in ('P0', 'P1') and cf_type = 'Defect' and short_desc NOT LIKE '%[i18N%'""".format(foundin_id, i18nbug)
    #sql = """select login_name, creation_ts, bug_id from bugs, profiles where bugs.assigned_to = profiles.userid and found_in_version_id = '{0}' and product_id = '18' and category_id not in {1}  and priority in ('P2', 'P3', 'P4', '---') and cf_type = 'Defect' and short_desc NOT LIKE '%[i18N%'""".format(foundin_id, i18nbug)
    sql = """select login_name, creation_ts, bug_id from bugs, profiles where bugs.assigned_to = profiles.userid and found_in_version_id = '{0}' and product_id = '18' and category_id not in {1}  and bug_severity in ('serious', 'minor', 'cosmetic') and priority in ('P0', 'P1') and cf_type = 'Defect' and short_desc NOT LIKE '%[i18N%'""".format(foundin_id, i18nbug)
    cursor.execute(sql)
    result= cursor.fetchall()
    result_json=json.dumps(result,default=json_util.default)
    return result_json


def getBugbyDateforReportTeam(foundin_id):
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)
    cursor = bzdb_conn.cursor()
    i18nbug = ('2451', '1800','1742', '736')
    sql = """select login_name, creation_ts, bug_id from bugs, profiles where bugs.reporter = profiles.userid and found_in_version_id = '{0}' and product_id = '18' and category_id not in {1}""".format(foundin_id, i18nbug)
    cursor.execute(sql)
    result= cursor.fetchall()
    result_json=json.dumps(result,default=json_util.default)
    return result_json

def getAllAssignee(foundin_id):
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)
    cursor = bzdb_conn.cursor()
    i18nbug = ('2451', '1800','1742', '736')
    sql = """select login_name from bugs, profiles where bugs.assigned_to = profiles.userid and found_in_version_id = '{0}' and product_id = '18' and category_id not in {1} and bug_severity in ('critical', 'catastrophic') """.format(foundin_id, i18nbug)
    cursor.execute(sql)
    result= cursor.fetchall()
    result_json=json.dumps(result)
    return result_json

def getBugbyDateandPro(foundin_id, severity):
    bzdb_conn = MySQLdb.connect(host=BUGZILLA_DATABASE_HOST, port=BUGZILLA_DATABASE_PORT, user=BUGZILLA_DATABASE_USER, passwd=BUGZILLA_DATABASE_PW, db=BUGZILLA_DATABASE_DATABASE)
    zdb_conn = MySQLdb.connect(host="bz3-db3.eng.vmware.com", port=3306, user="mts", passwd="mts", db="bugzilla")
    cursor = bzdb_conn.cursor()
    i18nbug = ('2451', '1800','1742', '736')
    sql = """select creation_ts, bug_id from bugs where found_in_version_id = '{0}' and product_id = '18' and category_id not in {1} and bug_severity = '{2}'""".format(foundin_id, i18nbug, severity)
    cursor.execute(sql)
    result= cursor.fetchall()
    result_json=json.dumps(result,default=json_util.default)
    return result_json

if __name__ == "__main__":
    print ('This is main of module "bug.py"')
    test()
    #getBugbyDateforTeam('4926')
