from django.contrib import admin
from app.backup.models import Backup, Machine, ScheduleBackup, FolderBackup, Company, Customer, Location, Storage, SQLBackup, ClientVersion

class ScheduleBackupInline(admin.TabularInline):
    model = ScheduleBackup
    
class FolderBackupInline(admin.TabularInline):
    model = FolderBackup


class SQLBackupInline(admin.TabularInline):
    model = SQLBackup

class BackupInline(admin.TabularInline):
    model = Backup

class ClientVersionsAdmin(admin.ModelAdmin):
    model = ClientVersion
    list_display = ['name', 'datetime','current']


class MachineAdmin(admin.ModelAdmin):
    model = Machine
    search_fields = ['machine_id', 'name']

    inlines = [
        ScheduleBackupInline,
        ]

class ScheduleAdmin(admin.ModelAdmin):
    model = ScheduleBackup
    search_fields = ['folder']

    inlines = [
        FolderBackupInline,
        SQLBackupInline,
        ]

#Company
class CustomerInline(admin.TabularInline):
    model = Customer
class CompanyAdmin(admin.ModelAdmin):
    model = Company
    inlines = [
        CustomerInline,
        ]

#Customer
class LocationInline(admin.TabularInline):
    model = Location
class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    inlines = [
        LocationInline,
        ]

#Location
class MachineInline(admin.TabularInline):
    model = Machine

class LocationAdmin(admin.ModelAdmin):
    model = Location
    inlines = [
        MachineInline,
        ]

#Backup
class BackupAdmin(admin.ModelAdmin):
    model = Backup

#Storage
class StorageAdmin(admin.ModelAdmin):
    model = Storage

admin.site.register(Machine, MachineAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(ScheduleBackup, ScheduleAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Backup, BackupAdmin)
admin.site.register(ClientVersion, ClientVersionsAdmin)