from django.db import models 

def custom_upload_to(instance, filename):
    return 'todo_images/{0}'.format(filename)

class Todo(models.Model):
    content = models.CharField(max_length=255)
    text_content = models.TextField(default='')
    image = models.ImageField(upload_to=custom_upload_to, null=True, blank=True, verbose_name='todo_image')
    #time = models.TextField(default='00:00')
    time = models.TimeField(default='00:00:00')
    star = models.BooleanField(default=False, null=False)
    done = models.BooleanField(default=False, null=False)