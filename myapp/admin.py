from django.contrib import admin
from .models import children, CustomerData,Message

# Register the 'children' model
@admin.register(children)
class childrenAdmin(admin.ModelAdmin):
    list_display = ['name', 'sex', 'age']  # Make sure these fields exist on the 'children' model

# Register the 'CustomerData' model
@admin.register(CustomerData)
class CustomerDataAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'cust_name', 'product_id', 'gender', 'age_group', 'age', 'marital_status', 'state', 'zone', 'occupation', 'product_category', 'orders', 'amount']
    # Adjust these fields to match the field names in your 'CustomerData' model
admin.register(Message)