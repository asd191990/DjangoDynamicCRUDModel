from django.shortcuts import render

from . import models
from . import Form
from django.http import JsonResponse
from django.db import IntegrityError
import json

### 功能function
def DBSwitch(var):
    return {
        'Personnel': models.Personnel,
        'Case': models.Case,
    }.get(var, 'error')

def EMP_NAME(id):
    return models.Personnel.objects.get(id=id).PersonnelName

#選擇轉化
def DataChangeToUser(key, value):
    #目前是model的key跟value都是一樣的不必修正。
    #預留給可能會要更改的FUN
    #或是使用is__xxxx_display


    return value


###

### axiso URL

def DBAllData(request):  #回傳table格式、新增的form格式
    Get_DB_STR = request.POST['DB']
    Get_DB = DBSwitch(Get_DB_STR)

    table_data = []
    columns = []

    for field in Get_DB._meta.fields:  #建立欄位頭的json
        coldata = {
            "field": field.name,
            "title": field.verbose_name,
            'sortable': 'true',
        }
        coldata["width"] = 120
        if field.name != "id":#不把id加進去
            columns.append(coldata)

    columns.append({"field": "DataOperating", "title": "操作", "width": 150})#放操作欄位

    for v in Get_DB.objects.all():  #建立表格欄位json

        data_dict = v.__dict__
        del data_dict['_state']

        for_data = {}

        for k in data_dict:#顯示TABLE資料
            #根據某些特別欄位名稱去處理
            if k == "CaseOwner_id":  #是實體欄位 去取得人員編號,djagno預設是 欄位名稱_id
                for_data["CaseOwner"] = EMP_NAME(data_dict[k])
            else:
                for_data[k] = DataChangeToUser(k, data_dict[k])

        if "T_emp_id" in for_data:  #預留給非pk的選擇，選擇要填入的id
            the_id = v.T_emp_id
        else:
            the_id = v.id

        operations = f'<div class="container"><button class="btn btn-info row" onclick="Data_Axsio_Fix(\'{str(the_id)}\')" >\
            修改</button> </div>'                                                                                                                             #操作

        for_data["DataOperating"] = operations

        table_data.append(for_data)

    Form_json = Form.DBFromSwitch(Get_DB_STR) #取得FORM資料
    data = {
        "table_head": columns,
        "table_data": table_data,
        "Form_json": Form_json,
    }
    return JsonResponse(data)

def DBDataRemove(request):  #刪除操作

    Get_DB_STR = request.POST['DB']
    data_id = request.POST['id']

    Get_DB = DBSwitch(Get_DB_STR)

    if Get_DB_STR == "BasicPersonnelInformation":
        Get_DB.objects.get(T_emp_id=data_id).delete()
    else:
        Get_DB.objects.get(id=data_id).delete()

    data = {"SMSG": "刪除成功"}
    return JsonResponse(data)


def DBDataJsonCU(request):  #處理模組化的新增跟修改
    data = {}
    print("X")
    Get_DB_STR = request.POST['DB']

    DataJson = json.loads(request.POST['DBDataJson'])
    Get_DB = DBSwitch(Get_DB_STR)
    mode = request.POST['mode']

    if "CaseOwner" in DataJson:  #將實體實體化
        DataJson["CaseOwner"] = models.Personnel.objects.get(
            id=DataJson["CaseOwner"])

    try:
        if mode == "add":  #新增
            Get_DB.objects.create(**DataJson)
        else:  #修改
            if Get_DB_STR == "BasicPersonnelInformation":
                Get_DB.objects.filter(T_emp_id=request.POST['id']).update(
                    **DataJson)
            else:
                Get_DB.objects.filter(id=request.POST['id']).update(**DataJson)

        data = {"MSG": "提交成功"}
    except IntegrityError:
        data = {"MSG": "已有資料。"}
    except Exception as exc:
        print("錯誤class" + str(exc.__class__))
        print(exc)
        data = {"MSG": "未分析錯誤"}

    return JsonResponse(data)


def DBDataFix(request):  #傳給前端修改的資料表單

    Get_DB_STR = request.POST['DB']
    data_id = request.POST['id']

    Get_DB = DBSwitch(Get_DB_STR)
    Fix_Form_json = Form.DBFromSwitch(Get_DB_STR)

    if Get_DB_STR == "BasicPersonnelInformation": #主PK不同
        Get_Data = Get_DB.objects.get(T_emp_id=data_id).__dict__
    else:
        Get_Data = Get_DB.objects.get(id=data_id).__dict__

    del Get_Data['_state']
    i = 0
    for key in Get_Data:
        if (key != "id"):
            Fix_Form_json[i]["value"] = str(Get_Data[key])
            i += 1

    data = {"Data": Fix_Form_json}
    return JsonResponse(data)


###


def Index(request):
    return render(request, 'ArticleManagement.html')