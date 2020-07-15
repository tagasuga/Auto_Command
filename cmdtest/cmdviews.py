
from django.shortcuts import render
from cmdtest.models import Cmdcase, Cmdcasestep
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pymysql
# Create your views here.
import time

from django.contrib.auth.decorators import login_required
from pymysql import connect
from lib.get_device_info import devices_list
import os
from lib.logging import Log

SerialNum = devices_list()
log = Log()

# cmd用例管理

@login_required
def cmdcase_manage(request):
    cmdcase_list = Cmdcase.objects.all()
    cmdcase_count = Cmdcase.objects.all().count()
    # 统计产品数
    username = request.session.get('user', '')  # 读取浏览器登录session
    paginator = Paginator(cmdcase_list, 8)  # 生成paginator对象,设置每页显示8条记录
    page = request.GET.get('page', 1)  # 获取当前的页码数,默认为第1页
    currentPage = int(page)  # 把获取的当前页码数转换成整数类型
    try:
        cmdcase_list = paginator.page(page)  # 获取当前页码数的记录列表
    except PageNotAnInteger:
        cmdcase_list = paginator.page(1)  # 如果输入的页数不是整数则显示第1页的内容
    except EmptyPage:
        cmdcase_list = paginator.page(paginator.num_pages)  # 如果输入的页数不在系统的页数中则显示最后一页
    return render(request, "cmdcase_manage.html",
                  {"user": username, "cmdcases": cmdcase_list, "cmdcasecounts": cmdcase_count})


# cmd用例测试步聚
@login_required
def cmdcasestep_manage(request):

    username = request.session.get('user', '')
    cmdcaseid = request.GET.get('cmdcase.id', None)

    cmdcase = Cmdcase.objects.get(id=cmdcaseid)
    cmdcasestep_list = Cmdcasestep.objects.all()
    print('cmdid============================', cmdcaseid)
    return render(request, "cmdcasestep_manage.html",
                  {"user": username, "cmdcase.id":cmdcaseid,"cmdcase": cmdcase, "cmdcasesteps": cmdcasestep_list})

# 搜索功能
@login_required
def cmdsearch(request):
    username = request.session.get('user', '')  # 读取浏览器登录session
    search_cmdcasename = request.GET.get("cmdcasename", "")
    cmdcase_list = Cmdcase.objects.filter(cmdcasename__icontains=search_cmdcasename)
    return render(request, 'cmdcase_manage.html', {"user": username, "cmdcases": cmdcase_list})


# 搜索功能
@login_required
def cmdstepsearch(request):
    username = request.session.get('user', '')  # 读取浏览器登录session
    search_cmdcasename = request.GET.get("cmdcasename", "")
    cmdcasestep_list = Cmdcasestep.objects.filter(cmdcasename__icontains=search_cmdcasename)
    return render(request, 'cmdcasestep_manage.html', {"user": username, "cmdcasesteps": cmdcasestep_list})


@login_required
def cmdtest_report(request):
    username = request.session.get('user', '')
    cmdcase_list = Cmdcasestep.objects.all()
    cmdcase_count = Cmdcasestep.objects.all().count()
    db = pymysql.connect(user='root', db='autotest', passwd='11111111', host='127.0.0.1')
    cursor = db.cursor()
    sql1 = "SELECT count(id) FROM cmdtest_cmdcasestep WHERE cmdtestresult='PASS'"
    aa=cursor.execute(sql1)
    cmd_pass_count = [row[0] for row in cursor.fetchmany(aa)][0]
    sql2 = "SELECT count(id) FROM cmdtest_cmdcasestep WHERE cmdtestresult='FAIL'"
    bb=cursor.execute(sql2)
    cmd_fail_count = [row[0] for row in cursor.fetchmany(bb)][0]
    db.close()
    return render(request, "cmdtestreport.html", {"user": username,"cmds": cmdcase_list,"cmdscounts": cmdcase_count,"cmds_pass_counts": cmd_pass_count,"cmds_fail_counts": cmd_fail_count})

def cmdauto(request):
    cmdid = request.GET.get('cmdcase.id', None)
    sql = "SELECT id,cmdtestobjname,assertdeclare,assertInfo1,assertInfo2,assertInfo3,assertInfo4 from cmdtest_cmdcasestep where cmdtest_cmdcasestep.cmdcase_id=%s ORDER BY id ASC;"
    db = connect(host="127.0.0.1", user="root", password="11111111", db="autotest", port=3306, charset="utf8")
    cur = db.cursor()
    aa = cur.execute(sql % cmdid)
    info = cur.fetchmany(aa)
    for ii in info:
        case_list = []
        case_list.append(ii)
        cmdtestcase(case_list)
    db.commit()
    cur.close()
    db.close()

def InsertResult(TestResult,case_id):
    db = connect(host="127.0.0.1", user="root", password="11111111", db="autotest", port=3306, charset="utf8")
    cur = db.cursor()
    sql = "UPDATE cmdtest_cmdcasestep SET cmdtestresult='{0}' where id={1}".format(TestResult,case_id)
    cur.execute(sql)
    db.commit()

def cmdtestcase(case_list):
    for case in case_list:
        try:
            case_id = case[0]
            cmdcommand = case[1]
            assertdeclare = case[2]
            assertInfo1 = case[3]
            assertInfo2 = case[4]
            assertInfo3 = case[5]
            assertInfo4 = case[6]

        except Exception as e:
            return '测试用例格式不正确！%s' % e

        print(case_list)
        time.sleep(5)
        if assertdeclare == 'assertIn':
            test01 = os.popen(cmdcommand)
            log01 = test01.read()
            log.info(log01)
            time.sleep(5)
            if assertInfo1 in log01:
                InsertResult('PASS',case_id)
            else:
                InsertResult('FAIL',case_id)
        elif assertdeclare == 'assertNotIn':
            test01 = os.popen(cmdcommand)
            log01 = test01.read()
            log.info(log01)
            time.sleep(5)
            if assertInfo1 in log01:
                InsertResult('FAIL',case_id)
            else:
                InsertResult('PASS',case_id)
            if assertInfo2 != None:
                if assertInfo2 in log01:
                    InsertResult('FAIL',case_id)
                else:
                    InsertResult('PASS',case_id)
            if assertInfo3 != None:
                if assertInfo2 in log01:
                    InsertResult('FAIL',case_id)
                else:
                    InsertResult('PASS',case_id)
            if assertInfo4 != None:
                if assertInfo2 in log01:
                    InsertResult('FAIL',case_id)
                else:
                    InsertResult('PASS',case_id)
        else:
            InsertResult('Assert Fail',case_id)

# web测试报告


# @login_required
# def webtest_report(request):
#     username = request.session.get('user', '')
#
#     return render(request, "webtest_report.html")
