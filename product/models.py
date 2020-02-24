from __future__ import unicode_literals

import datetime
import os
from PIL import Image
from codeab import settings
from decimal import Decimal
import uuid
from PIL import ImageFile

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from seller.models import Seller
from customer.models import Coupon

from product.offers import Offers

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def category_image_upload(instance, filename):
    reqpath = "category_photo/"
    filepath = BASE_DIR + "/uploads/" + reqpath
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    ext = filename.split('.')[-1]
    name = str(datetime.datetime.now()).replace(
        ' ', '').replace('.', '').replace(':', '')
    return reqpath + '{}.{}'.format(name, ext)


def category_size_chart(instance, filename):
    reqpath = "size_charts/"
    filepath = BASE_DIR + "/uploads/" + reqpath
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    ext = filename.split('.')[-1]
    name = str(datetime.datetime.now()).replace(
        ' ', '').replace('.', '').replace(':', '')
    return reqpath + '{}.{}'.format(name, ext)


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True,
                               related_name='children')
    name = models.CharField(max_length=150, unique=False)
    slug = models.SlugField(max_length=200, blank=True, null=False,
                            editable=False)
    description = models.TextField(null=True, blank=True, max_length=1000)
    active = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    publisher = models.CharField(max_length=300)
    unique_id = models.CharField(max_length=300, blank=True, null=False,
                                 editable=False)
    unique_name = models.CharField(max_length=500, blank=True, null=False)
    category_photo = models.ImageField(upload_to=category_image_upload,
                                       default='uploads/blogimages/dummy.jpg',
                                       blank=True, null=True)
    size_chart_url = models.ImageField(upload_to=category_size_chart,
                                       default='uploads/blogimages/dummy.jpg',
                                       blank=True, null=True)

    def __unicode__(self):
        return self.unique_name

    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in Category.objects.filter(parent=self):
            _r = c.get_all_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r

    def get_main_parent(self):
        if self.parent != None:
            obj = self.parent
            while obj.parent != None:
                obj = obj.parent
            return obj
        else:
            return self

    def get_level(self):
        if self.parent != None:
            obj = self
            count = 0
            while obj.parent != None:
                obj = obj.parent
                count = count + 1
            return count
        else:
            return 0

    def get_branch_nodes(self):
        r = []
        r.append(self)
        s = self
        while(s.parent != None):
            r.append(s.parent)
            s = s.parent
        return r

    @classmethod
    def create(cls, parent, name, description, publisher):
        category = cls(parent=parent, name=name,
                       description=description, publisher=publisher)
        # category.save()
        return category

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.parent is None:
            self.unique_id = str(self.pk)
            self.unique_name = self.name
            super(Category, self).save(*args, **kwargs)
        else:
            self.unique_id = str(self.parent.unique_id) + '-' + str(self.pk)
            self.unique_name = self.parent.unique_name + '-' + self.name
            super(Category, self).save(*args, **kwargs)

# class SubCategory(models.Model):
#     catalog = models.ForeignKey('Catalog',related_name='categories')
#     parent = models.ForeignKey('self', blank=True, null=True,related_name='children')
#     name = models.CharField(max_length=300)
#     slug = models.SlugField(max_length=150)
#     description = models.TextField(blank=True)


class CategoryWiseDescripionGroup(models.Model):
    category = models.ForeignKey(Category)
    group = models.CharField(max_length=300, null=False, blank=False)
    group_priority = models.IntegerField(null=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.group


class CategoryWiseProductDescriptionKeys(models.Model):
    product_desc_key = models.CharField(
        max_length=300, null=False, blank=False)
    group = models.ForeignKey(CategoryWiseDescripionGroup)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.product_desc_key


class Product(models.Model):

    DESIGNER_TYPE = (
        ("DESIGNER", "designer"),
        ("NORMAL", "normal"),
        ("USERQUERY", "userquery")
    )
    seller = models.ForeignKey(Seller)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=1500, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    wholesale_price = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ManyToManyField(Category, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    added_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    is_feature_product = models.BooleanField(default=False)
    keywords = models.CharField(
        max_length=200, blank=True, null=True, default=None)
    meta_description = models.CharField(
        max_length=500, blank=True, null=True, default=None)
    page_title = models.CharField(
        max_length=200, blank=True, null=False, default="Addiction Bazaar")
    is_customization_available = models.BooleanField(default=False)
    product_type = models.CharField(
        max_length=60, blank=True, choices=DESIGNER_TYPE, default=DESIGNER_TYPE[1])
    refundable = models.BooleanField(default=False)
    product_views = models.IntegerField(default=0)
    tags = models.CharField(max_length=150, blank=True)
    customization_details = models.CharField(max_length=300, blank=True)
    is_combo_product = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def get_categories(self):
        return "\n".join([c.name for c in self.category.all()])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.price = float(Decimal(self.price).quantize(Decimal("0.00")))
        self.wholesale_price = float(
            Decimal(self.wholesale_price).quantize(Decimal("0.00")))
        super(Product, self).save(*args, **kwargs)

    def get_final_price(self):
        discount_obj = Discount.objects.filter(product=self)
        if discount_obj:
            if discount_obj[0].discount_type.upper() == 'PERCENTAGE':
                return self.price * (1 - discount_obj[0].discount / 100)
            else:
                return self.price - discount_obj[0].discount

    def get_absolute_url(self):
        return "/product/" + str(self.slug) + '/' + str(self.id) + '/'


class ProductDescription(models.Model):
    product = models.ForeignKey(Product)
    product_desc_key = models.ForeignKey(CategoryWiseProductDescriptionKeys)
    product_desc_value = models.CharField(
        max_length=300, null=False, blank=False)

    def __unicode__(self):
        return self.product_desc_value


class CategoryVarient(models.Model):
    category = models.ForeignKey(Category)
    varient_type = models.CharField(max_length=50, null=False, blank=False)
    value = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)

    def save(self, *args, **kwargs):
        category_objs = CategoryVarient.objects.filter(category=self.category)
        for c in category_objs:
            if c.varient_type == self.varient_type and c.name == self.name:
                raise("Varient is Present")
        super(CategoryVarient, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.varient_type + "-" + self.value


def f(instance, filename):
    reqpath = "product_photo/" + \
        str(instance.product.category.first().pk) + \
        "/" + str(instance.product.pk) + "/"
    filepath = BASE_DIR + "/uploads/" + reqpath
    # print "path of product image->",BASE_DIR + filepath
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    ext = filename.split('.')[-1]
    name = str(datetime.datetime.now()).replace(
        ' ', '').replace('.', '').replace(':', '')
    return reqpath + '{}.{}'.format(name, ext)


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    product_photo = models.ImageField (upload_to=f,blank=True,null=True)
    display_priority = models.IntegerField(null=True, blank=True)
    category_varient = models.ManyToManyField(CategoryVarient, blank=True)

    def image_img(self):
        if self.product_photo:
            return self.get_thumbname_url()
        else:
            return '(Sin imagen)'

    def get_tiny_image(self):
        if self.product_photo:
            return self.get_tiny_url()
        else:
            return '(Sin imagen)'

    def create_thumbnail(self):
        original_image_path = self.product_photo.url.split('/', 1)[1]
        original_image = open(original_image_path, 'rw')
        # size=(400,400)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        img = ImageFile.Image.open(original_image)
        img.load()
        img.thumbnail((600, 600), Image.ANTIALIAS)
        # img = resizeimage.resize_thumbnail(img, [400, 400])
        # img.thumbnail((400,400), ImageFile.Image.ANTIALIAS)
        path, file_name = original_image_path.rsplit('/', 1)
        new_path = path + "/th_" + file_name
        # new = ImageFile.Image.new('RGBA', size, (255, 255, 255, 0))  #with alpha
        # new.paste(img,((size[0] - img.size[0]) / 2, (size[1] - img.size[1]) / 2))
        img.save(new_path, img.format)
        original_image.close()

    def get_thumbname_url(self):
        path, file_name = self.product_photo.url.rsplit('/', 1)
        return path + "/th_" + file_name

    def get_tiny_url(self):
        path, file_name = self.product_photo.url.rsplit('/', 1)
        return path + "/tiny_th_" + file_name

    def save(self, *args, **kwargs):
        image = Image.open(self.product_photo).convert("RGBA")
        non_transparent = Image.new('RGBA', image.size, (255, 255, 255, 255))
        non_transparent.paste(image, (0, 0), image)
        new_filename = ''.join(
            f(self, self.product_photo.name).split('.')[:-1]) + ".jpg"
        non_transparent.convert('RGB').save(
            settings.MEDIA_ROOT + '/' + new_filename)
        self.product_photo = new_filename
        # product = Product.objects.get(pk=int(args))
        # self.product = product
        super(ProductImage, self).save(*args, **kwargs)
        self.create_thumbnail()

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        super(ProductImage, self).delete(*args, **kwargs)

    def get_detailed_json(self):
        json = {'image_url': self.product_photo.url, 'product_id': self.product.id, 'image_id': self.pk}
        return json


class Discount(models.Model):
    DISCOUNT_TYPE = (
        ("FLAT", "flat"),
        ("PERCENTAGE", "percentage")
    )
    product = models.OneToOneField(Product)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    discount_type = models.CharField(max_length=150, choices=DISCOUNT_TYPE)

    def save(self, *args, **kwargs):
        self.discount = float(Decimal(self.discount).quantize(Decimal("0.00")))
        super(Discount, self).save(*args, **kwargs)


class DeliveryDetails(models.Model):
    product = models.ForeignKey(Product)
    # weight in grams
    weight = models.IntegerField(default=1)
    # height width and length in CMs
    height = models.IntegerField(default=1)
    width = models.IntegerField(default=1)
    length = models.IntegerField(default=1)
    is_ready_to_ship = models.BooleanField(default=False)
    fast_delivery_avelable = models.BooleanField(default=False)
    gift_wrap_avelable = models.BooleanField(default=False)


class ProductVarientList(models.Model):
    product = models.ForeignKey(Product)
    key = models.ManyToManyField(CategoryVarient)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=15, decimal_places=2)
    sellers = models.ManyToManyField(Seller)
    product_image = models.ForeignKey(ProductImage, null=True)

    # def save(self, *args, **kwargs):
    #     if not self.sellers.all(
    #         self.sellers.add(self.product.seller)
    #     super(ProductVarientList, self).save(*args, **kwargs)


class Cart(models.Model):
    LISTED_TYPE = (
        ("WISHLIST", "WISHLIST"),
        ("CART", "CART")
    )
    product = models.ForeignKey(Product)
    product_varient = models.ForeignKey(ProductVarientList)
    quantity = models.IntegerField(default=1)
    varient = models.CharField(default="NA", max_length=150)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, default=None, null=True, blank=True)
    listed_type = models.CharField(max_length=150, choices=LISTED_TYPE)
    active = models.BooleanField(default=True)


class ComboProducts(models.Model):
    LISTED_TYPE = (
        ("COUPLE", "COUPLE"),
    )
    products = models.ManyToManyField(Product)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=450)
    combo_type = models.CharField(
        max_length=150, choices=LISTED_TYPE, blank=True)


class ProductOffer(models.Model):
    name = models.CharField(max_length=150)
    rule = models.CharField(max_length=200, unique=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        from product import offers
        this_offer = getattr(offers, self.rule)
        super(ProductOffer, self).save(*args, **kwargs)
        self.update_in_cache()

    def update_in_cache(self):
        x = Offers()
        x.update_offer(self.name, self.rule)
