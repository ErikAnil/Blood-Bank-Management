from django.contrib import admin
from myapp.models import doner,patient,bloodrequest,directrequest
# Register your models here.
admin.site.register(doner)
admin.site.register(patient)
admin.site.register(bloodrequest)
admin.site.register(directrequest)