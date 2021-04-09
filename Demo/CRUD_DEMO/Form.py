from .models import Personnel

#欄位順序要一樣，title代表欄位名稱 field要對應model的名稱


def DBFromSwitch(var):

    PeopleData = []

    #設定人員的value 和 label(顯示)
    GetPeople = Personnel.objects.all().only('pk', 'PersonnelName')

    for People in GetPeople:
        PeopleData.append({
            "value": str(People.pk),
            "label": str(People.PersonnelName),
        })

    return {
        "Personnel": [
                {
                "type": "input",
                "field": "PersonnelName",
                "title": "人員名稱",
                "validate": [{
                    "required": True,
                    "message": "必填"
                }]
                }, {
                "type":"input",
                "field":"PersonnelPhone",
                "title":"人員電話",
                "validate": [{
                    "required": True,
                    "message": "必填"
                }, {
                    "validator":
                    "(rule,val,d)=>{!/^09[0-9]{8}$/.test(val)?d(true):d()}",
                    "message": "格式為09開頭，ex:0912345678，不需要-符號。"
                }]
            }, {
                "type":"select",
                "field":"PersonnelJob",
                "title":"工作崗位",
                "props": {
                        "placeholder": "請選擇",
                        "placement": "bottom",
                    },
                "validate": [{
                    "required": True,
                    "message": "必填"
                }],
                "options": [
                    {
                        "value": "0",
                        "label": "主管"
                    },
                    {
                        "value": "1",
                        "label": "一般人員"
                    },
                    {
                        "value": "2",
                        "label": "PM"
                    },
                    {
                        "value": "3",
                        "label": "工程師"
                    },
                ],
            }],
        "Case": [
                {
                    "type":"select",
                    "field":"CaseOwner",
                    "title":"選擇專案管理員",
                    "options": PeopleData,
                    "props": {
                        "placeholder": "請選擇",
                        "placement": "bottom",
                    },
                },
                {
                    "type":"input",
                    "field":"CaseName",
                    "title":"專案名稱",
                    "validate": [{
                        "required": True,
                        "message": "必填"
                    }]
                },
                {
                    "type":"input",
                    "field":"CaseMoney",
                    "title":"此專案金錢",
                    "validate": [{
                        "required": True,
                        "message": "必填"
                    }]
                },
                {
                    "type":"input",
                    "field":"CaseStatus",
                    "title":"專案形容",
                    "validate": [{
                        "required": True,
                        "message": "必填"
                    }]
                },
        ],
    }.get(var, 'error')
