from django.contrib import admin
from django.db.models import Q
from django import forms
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

# Register your models here.
from models import Product, Category, ProductImage, ProductDescription, Discount, CategoryVarient, Cart, ProductVarientList
from models import CategoryWiseDescripionGroup, CategoryWiseProductDescriptionKeys, ComboProducts
from models import ProductOffer


class ProductImagesInline(admin.TabularInline):
    model = ProductImage


class DiscountInline(admin.TabularInline):
    model = Discount


class CategoryVarientInline(admin.TabularInline):
    model = CategoryVarient


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        cat_list = Category.objects.filter(unique_name__icontains='grocery')
        cat_query = Q()
        for cat in cat_list:
            cat_query = cat_query | Q(parent=cat)
        wtf = Category.objects.filter(~Q(cat_query))
        w = self.fields['category'].widget
        choices = []
        for choice in wtf:
            choices.append((choice.id, choice.unique_name))
        w.choices = choices


class ProductAdmin(admin.ModelAdmin):
    list_display = ["page_title", "get_seller", "name", "slug", "description",
                    "final_price", "active", "is_feature_product", 'wholesale_price', 'product_img', 'show_on_website'
                    ]

    # list_filter = ('category',)
    list_editable = ['active', 'is_feature_product', 'wholesale_price']

    search_fields = ('name', 'description')

    filter_horizontal = ('category',)

    form = ProductForm

    def show_on_website(self, obj):
        return "<a href='%s' target='__blank'>%s</a>" % (reverse(
            'product_details',
            args=(
                obj.slug,
                obj.pk,
            )), 'Open'
        )
    show_on_website.allow_tags = True

    def final_price(self, obj):
        return obj.get_final_price()

    def product_img(self, obj):
        product_image_obj = ProductImage.objects.filter(product=obj)
        if product_image_obj:
            return mark_safe('<img src="%s" />' % (product_image_obj[0].image_img()))
        else:
            return '(Sin imagen)'
        product_img.short_description = 'Thumb'

    def get_seller(self, obj):
        return '%s' % (obj.seller.seller.first_name)

    # def get_queryset(self, request):
    #     cat_list = Category.objects.filter(~Q(unique_name__icontains = 'grocery'))
    #     cat_query = Q()
    #     for cat in cat_list:
    #         cat_query = cat_query | Q(category=cat)
    #     return Product.objects.filter(cat_query)

    inlines = [
        ProductImagesInline, DiscountInline,
    ]

    # def get_category(self, obj):
    #     return '%s' % (obj.category.unique_name)


class GroceryProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GroceryProductForm, self).__init__(*args, **kwargs)
        cat_list = Category.objects.filter(unique_name__icontains='grocery')
        cat_query = Q()
        for cat in cat_list:
            cat_query = cat_query | Q(parent=cat)
        wtf = Category.objects.filter(cat_query)
        w = self.fields['category'].widget
        choices = []
        for choice in wtf:
            choices.append((choice.id, choice.unique_name))
        w.choices = choices


class GroceryProductAdmin(ProductAdmin):
    form = GroceryProductForm
    filter_horizontal = ('category',)

    def get_queryset(self, request):
        cat_list = Category.objects.filter(unique_name__icontains='grocery')
        cat_query = Q()
        for cat in cat_list:
            cat_query = cat_query | Q(category=cat)
        return Product.objects.filter(cat_query)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['parent_category', 'name', 'slug', 'description',
                    'pub_date', 'publisher', 'unique_id', 'active']

    def parent_category(self, obj):
        try:
            return '%s' % (obj.parent.name)
        except AttributeError:
            return "MAIN_CATEGORY"

    def get_queryset(self, request):
        return Category.objects.filter(~Q(unique_name__icontains='grocery'))


class GroceryCategoryAdmin(CategoryAdmin):

    def get_queryset(self, request):
        cat_list = Category.objects.filter(unique_name__icontains='grocery')
        cat_query = Q()
        for cat in cat_list:
            cat_query = cat_query | Q(parent=cat)
        return Category.objects.filter(cat_query)


class ProductImageAdmin(admin.ModelAdmin):
    model = ProductImage
    list_display = ['product', 'display_priority', 'varient', 'image', ]

    def image(self, obj):
        return mark_safe('<img src="%s" />' % (obj.image_img()))
        image.short_description = 'Thumb'

    def varient(self, obj):
        return ', '.join([str(key.varient_type) + '-' + str(key.value) for key in obj.category_varient.all()])


class ProductDescriptionAdmin(admin.ModelAdmin):
    list_display = ['product', 'product_desc_key', 'product_desc_value']
    list_filter = ['product']


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['product', 'discount', 'discount_type']
    list_filter = ['product']


class CategoryWiseDescripionGroupAdmin(admin.ModelAdmin):
    model = CategoryWiseDescripionGroup
    list_display = ['category', 'group', 'group_priority', 'active']
    list_filter = ['category']


class CategoryWiseProductDescriptionKeysAdmin(admin.ModelAdmin):
    list_display = ['product_desc_key', 'group', 'active']
    list_filter = ['group']


class CategoryVarientAdmin(admin.ModelAdmin):
    list_display = ['category', 'varient_type', 'value', 'name']
    list_filter = ['category']


class CartAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity',
                    'varient', 'token', 'user', 'listed_type']


def create_modeladmin(modeladmin, model, name=None):
    class Meta:
        proxy = True
        app_label = model._meta.app_label

    attrs = {'__module__': '', 'Meta': Meta}

    newmodel = type(name, (model,), attrs)

    admin.site.register(newmodel, modeladmin)
    return modeladmin


class ProdcutOfferAdmin(admin.ModelAdmin):
    model = ProductOffer


class ComboProductsAdmin(admin.ModelAdmin):

    filter_horizontal = ('products',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "products":
            kwargs["queryset"] = Product.objects.filter(is_combo_product=True)
        return super(ComboProductsAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class ProductVarientListAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'category', 'varients']
    filter_horizontal = ('key',)

    def varients(self, object):
        return ','.join([str(cv) for cv in object.key.all()])

    def category(self, object):
        return str(object.product.category.all()[0].slug)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "key":
            if request.META['PATH_INFO'].strip('/').split('/')[-1] == 'change':
                obj_id = request.META['PATH_INFO'].strip('/').split('/')[-2]
                pv_obj = ProductVarientList.objects.get(id=obj_id)
                p_category = pv_obj.product.category.all()[0]
                kwargs["queryset"] = CategoryVarient.objects.filter(
                    category=p_category)
            else:
                kwargs["queryset"] = CategoryVarient.objects.all()
        return super(ProductVarientListAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
create_modeladmin(GroceryCategoryAdmin,
                  name='Grocery Category', model=Category)
create_modeladmin(GroceryProductAdmin, name='Grocery Products', model=Product)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(CategoryWiseDescripionGroup,
                    CategoryWiseDescripionGroupAdmin)
admin.site.register(CategoryWiseProductDescriptionKeys,
                    CategoryWiseProductDescriptionKeysAdmin)
admin.site.register(CategoryVarient, CategoryVarientAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductDescription, ProductDescriptionAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(ProductVarientList, ProductVarientListAdmin)
admin.site.register(ComboProducts, ComboProductsAdmin)
admin.site.register(ProductOffer, ProdcutOfferAdmin)
