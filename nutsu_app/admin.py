from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

#admin.site.register()
admin.site.register(Newsletter)
admin.site.register(NewsletterBlock)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Query)
admin.site.register(Service)
admin.site.register(ConsultedCustomer)
admin.site.register(Payment)
admin.site.register(BadPayment)
admin.site.register(Review)