from django.db import models

#簡單的實作 人員管理專案


#人員管理
class Personnel(models.Model):
    class Meta:
        verbose_name = "人員資料"

    PersonnelName = models.CharField(max_length=3, verbose_name="人員名字")
    PersonnelPhone = models.CharField(max_length=10, verbose_name="人員電話",unique=True)
    JobChoices = (('0', '主管'), ('1', '一般人員'), ('2', 'PM'), ('3', '工程師'))
    PersonnelJob = models.CharField(max_length=1,
                                    choices=JobChoices,
                                    verbose_name="人員等級")


#專案管理
class Case(models.Model):
    class Meta:
        verbose_name = "專案管理"

    CaseOwner = models.ForeignKey(Personnel,
                                  on_delete=models.CASCADE,
                                  verbose_name="專案管理者")
    CaseName = models.CharField(max_length=3, verbose_name="專案名字")
    CaseMoney = models.CharField(max_length=3, verbose_name="專案金額")
    CaseStatus = models.CharField(max_length=3, verbose_name="專案狀態形容")
