from django.contrib import admin

# Register your models here.

from .models import Blog, Tags


from django import forms

# class BlogModelForm( forms.ModelForm ):
#     content = forms.CharField( widget=forms.Textarea )
#     class Meta:
#         model = Blog

class TagsInline(admin.TabularInline):
    model = Tags

class BlogAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(BlogAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'content':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield
    # form = BlogModelForm
    # model = Blog
    inlines = [
        TagsInline,
    ]   
    list_display = ['title']#Blog._meta.get_fields()


admin.site.register(Blog,BlogAdmin)

    
