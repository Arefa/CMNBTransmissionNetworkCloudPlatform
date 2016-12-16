from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

import os
import csv
import codecs


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/networkAnalyze/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'networkAnalyze/signin.html', {})


@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/networkAnalyze/')


@login_required
def index(request):
    return render(request, 'networkAnalyze/index.html')


@login_required
def upload(request):
    if request.method == 'POST':
        if os.path.exists('E:\\upload\\neinfo.csv'):
            os.remove('E:\\upload\\neinfo.csv')
        if os.path.exists('E:\\upload\\cneinfo.csv'):
            os.remove('E:\\upload\\cneinfo.csv')
        if os.path.exists('E:\\upload\\ne2ne.csv'):
            os.remove('E:\\upload\\ne2ne.csv')
        neinfo = request.FILES.get("neinfo", None)  # 获取上传的文件，如果没有文件，则默认为None
        ne2ne = request.FILES.get("ne2ne", None)  # 获取上传的文件，如果没有文件，则默认为None
        cneinfo = request.FILES.get("cneinfo", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not neinfo and ne2ne and cneinfo:
            return HttpResponse("no files for upload!")
        destination_neinfo = open(os.path.join("E:\\upload", neinfo.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        destination_ne2ne = open(os.path.join("E:\\upload", ne2ne.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        destination_cneinfo = open(os.path.join("E:\\upload", cneinfo.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in neinfo.chunks():  # 分块写入文件
            destination_neinfo.write(chunk)
        destination_neinfo.close()
        for chunk in ne2ne.chunks():  # 分块写入文件
            destination_ne2ne.write(chunk)
        destination_ne2ne.close()
        for chunk in cneinfo.chunks():  # 分块写入文件
            destination_cneinfo.write(chunk)
        destination_cneinfo.close()
        print(u"成功上传数据源！")
        return HttpResponse("文件上传成功!")
    else:
        return render(request, 'networkAnalyze/upload_data.html')


@login_required
def evaluate(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'networkAnalyze/evaluate.html')


@login_required
def autotools(request):
    if request.method == 'POST':
        if os.path.exists('E:\\upload\\neinfo.csv'):
            os.remove('E:\\upload\\neinfo.csv')
        if os.path.exists('E:\\upload\\cneinfo.csv'):
            os.remove('E:\\upload\\cneinfo.csv')
        if os.path.exists('E:\\upload\\ne2ne.csv'):
            os.remove('E:\\upload\\ne2ne.csv')
        neinfo = request.FILES.get("neinfo", None)  # 获取上传的文件，如果没有文件，则默认为None
        ne2ne = request.FILES.get("ne2ne", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not neinfo and ne2ne:
            return HttpResponse("no files for upload!")
        destination_neinfo = open(os.path.join("E:\\upload", neinfo.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        destination_ne2ne = open(os.path.join("E:\\upload", ne2ne.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in neinfo.chunks():  # 分块写入文件
            destination_neinfo.write(chunk)
        destination_neinfo.close()
        for chunk in ne2ne.chunks():  # 分块写入文件
            destination_ne2ne.write(chunk)
        destination_ne2ne.close()
        print(u"成功上传数据源！")
        cnelist = []
        access_ne_type = ('OptiX PTN 910', 'OptiX PTN 950', 'OptiX PTN 960', 'OptiX PTN 1900')
        converge_ne_type = ('OptiX PTN 3900', 'PTN 6900', 'OptiX PTN 7900-24')

        with codecs.open("E:\\upload\\neinfo.csv", "r", "utf-8") as neinfo_csvfile:
            neinfo_read = csv.reader(neinfo_csvfile)
            nelist = [ne_row for ne_row in neinfo_read]
            convergenelist = []
            if nelist[7][0] == '网元名称' and nelist[7][1] == '网元类型' and nelist[7][9] == '所属子网':
                for nelist_range in range(8, len(nelist)):
                    if nelist[nelist_range][1] in converge_ne_type:
                        convergenelist.append(nelist[nelist_range][0])

        with codecs.open("E:\\upload\\ne2ne.csv", "r", "utf-8") as ne2ne_csvfile:
            ne2ne_read = csv.reader(ne2ne_csvfile)
            ne2nelist = [ne2ne_row for ne2ne_row in ne2ne_read]
            if ne2nelist[7][5] == '源网元' and ne2nelist[7][7] == '宿网元' and ne2nelist[7][16] == '备注':
                for convergenelistrange in range(0, len(convergenelist)):
                    for ne2nelist_range in range(8, len(ne2nelist)):
                        if ne2nelist[ne2nelist_range][5] == convergenelist[convergenelistrange]:
                            for nerange in range(8, len(nelist)):
                                if ne2nelist[ne2nelist_range][7] == nelist[nerange][0] and nelist[nerange][1] in access_ne_type:
                                    cnelist.append([(nelist[nerange][9])[0:2], convergenelist[convergenelistrange],
                                                    nelist[nerange][9]])
                        elif ne2nelist[ne2nelist_range][7] == convergenelist[convergenelistrange]:
                            for nerange in range(8, len(nelist)):
                                if ne2nelist[ne2nelist_range][5] == nelist[nerange][0] and nelist[nerange][1] in access_ne_type:
                                    cnelist.append([(nelist[nerange][9])[0:2], convergenelist[convergenelistrange],
                                                    nelist[nerange][9]])
        cnedistictlist = []
        for r in range(0, len(cnelist)):
            if cnelist[r] not in cnedistictlist:
                cnedistictlist.append(cnelist[r])

        with open('E:\\upload\\cneinfo.csv', 'w', newline='', encoding='utf-8') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
            spamwriter.writerow(['区域', '网元名称', '所属子网'])
            spamwriter.writerows(cnedistictlist)
        return HttpResponse("生成成功！")
    else:
        return render(request, 'networkAnalyze/autotools.html')


@login_required
def config(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'networkAnalyze/config.html')