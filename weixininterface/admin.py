from django.contrib import admin
from .models import Course,Question,Player,CoursesRecord,QuestionsRecord
# # Register your models here.
#

admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Player)
admin.site.register(CoursesRecord)
admin.site.register(QuestionsRecord)

