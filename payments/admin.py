from django.contrib import admin

from .models import Course , Order


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title','slug','price','description')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','status','amount','course',)


admin.site.register(Course,CourseAdmin)
admin.site.register(Order,OrderAdmin)


