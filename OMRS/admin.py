from django.contrib import admin
from OMRS.models import Shredder,JobStatus,Jobs,Server,Authentication,UserProfile,Document,UserFeed

# Register your models here.

admin.site.register(Shredder)
admin.site.register(Jobs)
admin.site.register(JobStatus)
admin.site.register(Server)
admin.site.register(Authentication)
admin.site.register(UserProfile)
admin.site.register(Document)
admin.site.register(UserFeed)

