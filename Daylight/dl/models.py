from django.db import models 
from datetime import datetime, time  # Python의 datetime 모듈에서 date를 가져옴

def custom_upload_to(instance, filename):
    return 'todo_images/{0}'.format(filename)

class Todo(models.Model):
    content = models.CharField(max_length=255)
    text_content = models.TextField(default='')
    image = models.ImageField(upload_to=custom_upload_to, null=True, blank=True, verbose_name='todo_image')
    #time = models.TextField(default='00:00')
    #time = models.TimeField(default='00:00')  # 시간을 저장할 경우 TimeField 사용
    time = models.DateTimeField(default=datetime.combine(datetime.today(), time(0, 0)))  # 시간을 저장할 경우 TimeField 사용
    star = models.BooleanField(default=False, null=False)
    done = models.BooleanField(default=False, null=False)