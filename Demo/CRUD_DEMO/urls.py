


from django.urls import path, include,re_path
from . import views

urlpatterns = [
    path('', views.Index),
    #動態axios連結
    path('DBAllData', views.DBAllData),#得到該model資料、表單資料
    path('DBDataJson', views.DBDataJsonCU, name='DBDataJson'), #新增(C)或修改(U)動態資料庫
    path('DBDataFix', views.DBDataFix), #取得要修正的資料
    path('DBDataRemove', views.DBDataRemove, name='DBDataRemove'),#動態刪除
]



