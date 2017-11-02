from django.contrib import admin
from appxiencias.models import *
from django.contrib.admin.filters import RelatedOnlyFieldListFilter
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy


class CmyvalAdminSite(AdminSite):
    site_header = 'CMYVAL'

cmyvaladmin = CmyvalAdminSite(name='cmyvaladmin')



class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'CMYVAL'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class MultiDBTabularInline(admin.TabularInline):
    using = 'CMYVAL'

    def get_queryset(self, request):
        # Tell Django to look for inline objects on the 'other' database.
        return super(MultiDBTabularInline, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBTabularInline, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBTabularInline, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


# @admin.register(Traficosms)
# class TraficosmsAdmin(admin.ModelAdmin):
#     list_display = ('id','get_lote','destino','mensaje','status')

#     def get_lote(self, obj):
# 		return obj.lote.name

# Specialize the multi-db admin objects for use with specific models.



#admin.site.register(Traficosms, MultiDBModelAdmin)


cmyvaladmin.register(Traficosms, MultiDBModelAdmin)








