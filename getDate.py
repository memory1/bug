#!/usr/bin/python
# -*- coding: UTF-8 -*-
import bug
import json
from bugInfo import bugInfo
#import time
import datetime
import xlsxwriter
#import os.path
import pytz
#import numpy as np
import pandas as pd

"""BJTeam = ['baochenw', 'weiy', 'shuhuawang', 'agong', 'jinxingh', 'hongshengl', 'myuan', 'luliu', 'jhuo', 'rxing',
          'yyu1', 'wenshuoc', 'dengy', 'jingy',
          'nge', 'songlil', 'linz', 'smangui', 'bnie', 'gsi', 'xinyangl', 'xwei', 'yanx', 'tzhao', 'vzheng', 'yuez',
          'hek', 'zhaoli', 'bliu', 'jjliu', 'boliu', 'menx', 'qsun', 'dongw', 'wangxiao', 'wyattx', 'yuanmengx',
          'dongyuz', 'baic', 'hbai', 'pguo', 'shou', 'lihuang', 'zji', 'guoxin', 'qinz', 'ziaoy', 'wenyuzhao', 'zzhou',
          'anh', 'wbai', 'chenyu', 'tjia', 'lkong', 'huangl', 'mlu', 'renz', 'ksong', 'songyu', 'xiaoyux', 'wyang',
          'yun', 'chaoz', 'leviz',
          'lxclient-bj-dev', 'yhui', 'view-osx', 'wincdk_guru', 'view-android', 'linali', 'zhaom', 'view-clients-guru',
          'zhiminl', 'yyun',
          'view-ios', 'oye', 'pcoip', 'fyan', 'amzhang', 'boshil', 'kkong', 'ltim', 'pewang', 'qhuang', 'shik', 'zlin',
          'yanh', 'jjzhang',
          'scheng', 'rli', 'txiong', 'cn-dev-vc-win', 'lxclient-bj-dev', 'view-triage', 'yuetingz']"""

BJTeam = ['agong',
        'anh',
        'baic',
        'baochenw',
        'bliu',
        'boliu',
        'chenyu',
        'cn-dev-web',
        'dongyuz',
        'fabulatech_guru',
        'fyan',
        'gaog',
        'gsi',
        'guoxin',
        'hbai',
        'hek',
        'hongshengl',
        'jhuo',
        'jjliu',
        'kkong',
        'ksong',
        'leviz',
        'lihuang',
        'linali',
        'linz',
        'mlu',
        'msun',
        'myuan',
        'mzang',
        'nge',
        'pcoip',
        'pewang',
        'pguo',
        'qinz',
        'qsun',
        'renz',
        'rxing',
        'shik',
        'shou',
        'shuhuawang',
        'smangui',
        'songlil',
        'songyu',
        'thinprint_guru',
        'tzhao',
        'vdesktop-devops',
        'view-ios',
        'view-osx',
        'wangxiao',
        'wbai',
        'weiy',
        'wenshuoc',
        'wenyuzhao',
        'wincdk_guru',
        'wyattx',
        'xinyangl',
        'xwei',
        'yanx',
        'ysan',
        'yuez',
        'yul',
        'yun',
        'yyu1',
        'yyun',
        'zhaoli',
        'zhiminl',
        'zji',
        'zzhou']

KenTeam = ['ysan', 'ltim', 'boshil', 'zlin', 'ljack', 'xinshul', 'swan', 'llv', 'scheng', 'youx', 'jsong','zhoujing']

# test method
def createbuglist():
    foundin_id = bug.getBugbyFoundin('4926')
    array = json.loads(foundin_id)
    bugs = []
    for element in array:
        date = datetime.datetime.fromtimestamp(element[0].get('$date') / 1e3).date()
        buginfo = bugInfo(element[1], date, "")
        bugs.append(buginfo)

def getRegressionBugDateList(foundin):
    foundin_id = bug.getFoundin(foundin)
    result = bug.getRegressionBug(foundin_id)
    return ConvertTStoDateList(result)


def getRegression(foundin, filename):
    foundin_id = bug.getFoundin(foundin)
    result = bug.getRegressionBug(foundin_id)
    datelist = ConvertTStoDateList(result)
    count(datelist, filename)


def getBugDateListbySeverity(foundin, severity):
    foundin_id = bug.getFoundin(foundin)
    print(foundin_id)
    result = bug.getBugListbySeverity(foundin_id, severity)
    print(result)
    return ConvertTStoDateList(result)


# return a list of dates (mmddyy)
def ConvertTStoDateList(result):
    array = json.loads(result)
    datelist = []
    for element in array:
        tz = pytz.timezone('US/Pacific')
        date = datetime.datetime.fromtimestamp(element[0].get('$date') / 1e3, pytz.utc).date()
        datelist.append(date)
    return datelist

def getassigneelist(foundin):
    foundin_id = bug.getFoundin(foundin)
    result = bug.getAllAssignee(foundin_id)
    array = json.loads(result)
    assigneelist = []
    datelist = []
    for element in array:
        assigneelist.append("'"+element[0]+"',")
    dateset = set(assigneelist)
    for element in dateset:
        #print(element)
        count = assigneelist.count(element)
        #print(count)
        datelist.append(count)
    filename = "assignee_"+foundin.strip()+".xlsx"
    writetofile(filename, dateset, datelist, 'No')

def getBugDateforTeam(foundin, filename1, filename2, severity='all',cf_regression = "No"):
    foundin_id = bug.getFoundin(foundin)
    result = bug.getBugbyDateforTeam(foundin_id,severity,cf_regression)
    array = json.loads(result)
    BJBugs = []
    PABugs = []
    for element in array:
        tz = pytz.timezone('US/Pacific')
        date = datetime.datetime.fromtimestamp(element[1].get('$date') / 1e3, pytz.utc).date()
        if element[0] in BJTeam:
            BJBugs.append(date)
            #print("BJ:" + element[0])
        else:
            PABugs.append(date)
            #print("PA:" + element[0])
    count(BJBugs, filename1)
    count(PABugs, filename2)


def getBugbyDateforKenTeam(foundin, filename1):
    foundin_id = bug.getFoundin(foundin)
    result = bug.getBugbyDateforReportTeam(foundin_id)
    array = json.loads(result)
    KenTeamBugs = []
    for element in array:
        tz = pytz.timezone('US/Pacific')
        date = datetime.datetime.fromtimestamp(element[1].get('$date') / 1e3, pytz.utc).date()
        if element[0] in KenTeam:
            KenTeamBugs.append(date)
            print(element[2])
            print(date)
    print(KenTeamBugs)
    count(KenTeamBugs, 'kenbug.xlsx')


def count(datelist, filename):
    dateset = set(datelist)
    datesub = list(dateset)
    datesub.sort()
    datacount = []
    for element in datesub:
        count = datelist.count(element)
        datacount.append(count)
    writetofile(filename, datesub, datacount, 'No')


def BugNumbySeverity(foundin, filename, severity='all',regression ='n'):
    if regression is 'y':
        datelist = getRegressionBugDateList(foundin)
        print(datelist)
    else:
        datelist = getBugDateListbySeverity(foundin, severity)
        print(datelist)
    count(datelist, filename);

def ReopenNumbyWeekTeam(foundin):
    foundin_id = bug.getFoundin(foundin)
    result = bug.getReopenlist(foundin_id)
    """array = json.load(result)
    for element in array:
        tz = pytz.timezone('US/Pacific')
        date = datetime.datetime.fromtimestamp(element[0].get('$date') / 1e3, pytz.utc).date()
        element[0] = date
        BJReopen=[]
        PAReopen=[]
        if element[2] in BJTeam:
            BJReopen.append(element)
        else:
            PAReopen.append(element)
        count(BJReopen[0], foundin+'BJReopen.xlsx')
        count(PAReopen[0], foundin+'PAReopen.xlsx')
"""
def writetofile(excel_name='bugcount.xlsx', data1=[], data2=[], line_chart='Yes'):
    workbook = xlsxwriter.Workbook(excel_name)
    worksheet = workbook.add_worksheet('sheet1')
    workbook.add_format({'bold': True})
    title = ['Time', 'Count']
    top = workbook.add_format({'border': 6, 'align': 'center', 'bg_color': 'cccccc', 'font_size': 13, 'bold': True})
    format = workbook.add_format({'num_format': 'dd/mm/yy'})
    worksheet.set_column('A:B', 15)
    worksheet.write_row('A1', title, top)
    worksheet.write_column('A2', data1, format)
    worksheet.write_column('B2', data2)
    if line_chart is 'Yes' or 'yes':
        chart = workbook.add_chart({'type': 'line'})
        chart.set_title({'name': 'Bug per date'})
        chart.add_series({'categories': 'sheet1!$A$2:$A$' + str(len(data2) + 8),
                          'values': 'sheet1!$B$2:$B$' + str(len(data2) + 8),
                          })
        chart.set_size({'width': 800, 'height': 500})
        chart.set_x_axis({'name': 'Date'})
        chart.set_y_axis({'name': 'Number'})
        chart.set_style(33)
        worksheet.insert_chart('D3', chart)
    workbook.close()


def analyze(infilename, outfilename):
    weeklist = []
    weekcount = []
    originaldata = pd.DataFrame(pd.read_excel(infilename))
    originaldata = originaldata.set_index('Time')
    test = originaldata.resample('W').sum().fillna(0)
    #print('test:')
    #print(test)
    for column in test.columns:
        for idx in test[column].index:
            x = test.at[idx,column]
            weeklist.append(idx)
            weekcount.append(x)
    writetofile(outfilename, weeklist, weekcount, 'Yes')


if __name__ == "__main__":
    print('This is main of module "getDate.py"')
    found_in='CART19FQ2'
    ReopenNumbyWeekTeam(found_in)
    """
    getRegression(found_in, found_in +'_regression.xlsx')
    SourceFile = found_in +'_regression.xlsx'
    analyze(SourceFile, 'analyze_' + SourceFile)
    getassigneelist(found_in)
    getBugDateforTeam(found_in, found_in + '_bj_defects_all.xlsx', found_in + '_pa_defects_all.xlsx')
    getBugDateforTeam(found_in, found_in + '_bj_defects_critical.xlsx', found_in + '_pa_defects_critical.xlsx',severity="('critical','catastrophic')")
    getBugDateforTeam(found_in, found_in + '_bj_defects_regression.xlsx', found_in + '_pa_defects_regression.xlsx',severity="('critical','catastrophic')",cf_regression='Yes')
    SourceFile= found_in +'_bj_defects_all.xlsx'
    analyze(SourceFile, 'analyze_' + SourceFile)

    SourceFile = found_in + 'BJReopen.xlsx'
    analyze(SourceFile, 'analyze_' + SourceFile)
    SourceFile = found_in + 'PAReopen.xlsx'
    analyze(SourceFile, 'analyze_' + SourceFile)


    BugNumbySeverity(found_in, found_in + 'bugcount_Defect.xlsx')
    BugNumbySeverity(found_in, found_in + 'bugcount_Defect_Critical.xlsx',severity="('critical','catastrophic')")

    foundin_id = bug.getFoundin(found_in)
    print(bug.getFoundinPhase(foundin_id,"('FC')"))
    print(bug.getFoundinPhase(foundin_id))
    """
    # createbuglist()
    #getRegression('CART18FQ4', '18fq4_regression.xlsx')
    #getRegression('CART18FQ3', '18fq3_regression.xlsx')
    #getBugbyDateforKenTeam('CART18FQ4', '18fq4_ken.xlsx')
    # analyze('bugcount_q4_Defect.xlsx', 'analyze_q4_Defect.xlsx')
    # getBugbyDateforTeam('Cart17Q2', '18fq2_bj_defect_ser.xlsx', '18fq2_pa_defect_ser.xlsx')
    # getBugbyDateforTeam('CART18FQ3', '18fq3_bj_defect_ser.xlsx', '18fq3_pa_defect_ser.xlsx')
    # getBugbyDateforTeam('CART18FQ4', '18fq4_bj_defect_min.xlsx', '18fq4_pa_defect_min.xlsx')
    # getBugbyDateforTeam('Cart17Q1', '18fq1_bj_Defect.xlsx', '18fq1_pa_Defect.xlsx')
    # analyze('18fq1_bj_Defect.xlsx', 'analyze_q1_bj_Defect.xlsx')
    # analyze('18fq1_pa_Defect.xlsx', 'analyze_q1_pa_Defect.xlsx')
    # getBugbyDateforTeam('CART18FQ4', '18fq4_bj_Defect.xlsx', '18fq4_pa_Defect.xlsx')
    # analyze('18fq4_bj_Defect.xlsx', 'analyze_q4_bj_Defect.xlsx')
    # analyze('18fq4_pa_Defect.xlsx', 'analyze_q4_pa_Defect.xlsx')
    # getBugbyDateforTeam('Cart17Q2', '18fq2_bj_Defect.xlsx', '18fq2_pa_Defect.xlsx')
    # analyze('18fq2_bj_Defect.xlsx', 'analyze_q2_bj_Defect.xlsx')
    # analyze('18fq2_pa_Defect.xlsx', 'analyze_q2_pa_Defect.xlsx')
    # getBugbyDateforTeam('CART18FQ3', '18fq3_bj_Defect.xlsx', '18fq3_pa_Defect.xlsx')
    # analyze('18fq3_bj_Defect.xlsx', 'analyze_q3_bj_Defect.xlsx')
    # analyze('18fq3_pa_Defect.xlsx', 'analyze_q3_pa_Defect.xlsx')
    # createbuglist()
    # calculatebyDate('CART18FQ4', 'bugcount_q4_Defect.xlsx')
    # analyze('bugcount_q4_Defect.xlsx', 'analyze_q4_Defect.xlsx')
    # calculatebyDate('CART18FQ3', 'bugcount_q3_Defect.xlsx')
    # analyze('bugcount_q3_Defect.xlsx', 'analyze_q3_Defect.xlsx')
    # calculatebyDate('Cart17Q1', 'bugcount_q1_Defect.xlsx')
    # analyze('bugcount_q1_Defect.xlsx', 'analyze_q1_Defect.xlsx')
    # calculatebyDate('Cart17Q2', 'bugcount_q2_Defect.xlsx')
    # analyze('bugcount_q2_Defect.xlsx', 'analyze_q2_Defect.xlsx')