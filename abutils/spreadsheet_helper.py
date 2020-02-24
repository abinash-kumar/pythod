import gspread
from oauth2client.service_account import ServiceAccountCredentials
import math
from seller.models import Seller
from django.core.files import File
import os
import shutil
import requests

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('apidrive.json', scope)
gc = gspread.authorize(credentials)


# def roundup(x):
#     return int(math.ceil(x / 10.0)) * 10

# def upload_products_in_bulk(work_book_name, sheet_index, product_list_start_row_index,
#      product_list_end_row_index,seller_user_id,main_category):
#     wks = gc.open(work_book_name)
#     sheet = wks.worksheets()[sheet_index]
#     no_of_products = product_list_end_row_index - product_list_start_row_index
#     for i in range(no_of_products):
        # row_number = i+product_list_start_row_index
        # values = sheet.row_values(row_number)
        # sku_id = values[0].strip()
        # name = values[1]
        # description = values[2]
        # category = values[3].strip()
        # price = roundup(float(values[6]))
        # offer = int(values[7].strip())
        # current_status = values[18].strip().lower()
        # script_status = values[19].strip()

        # if current_status == 'done' or script_status == 'Uploaded Successfully' or "Image not uploaded" in script_status:
        #     print "skipping, already exist"
        #     continue

        # print "Adding Product........."

        # try:
        #     category_obj = Category.objects.get(unique_name__icontains=main_category,name__iexact=category)
        # except:
        #     sheet.update_acell('T'+str(row_number),"Category not available")
        #     continue

        # seller_obj = Seller.objects.get(mobile=seller_user_id)
        # try :
        #     p = Product.objects.create(
        #         seller=seller_obj,
        #         name=name,
        #         description=description,
        #         price=price,
        #         wholesale_price=price,
        #         )
        #     p.category.add(category_obj)
        #     d = Discount.objects.create(product=p, discount=offer,discount_type="PERCENTAGE")
        #     try:
        #         File(open('tmp/'+sku_id+'.jpg', 'rb'))
        #         pi = ProductImage.objects.create(product=p,product_photo=File(open('tmp/'+sku_id+'.jpg', 'rb')))
        #         sheet.update_acell('T'+str(row_number),"Uploaded Successfully")
        #     except IOError:
        #         sheet.update_acell('T'+str(row_number),"Image not uploaded, product id:"+str(p.pk))
        # except Exception,e:
        #     sheet.update_acell('T'+str(row_number),"some error"+str(e))
        #     try:
        #         pi.delete()
        #     except NameError:
        #         print "dont know what is this"

        #     try:
        #         d.delete()
        #     except NameError:
        #         print "dont know what is this"

        #     try:
        #         p.delete()
        #     except NameError:
        #         print "dont know what is this"

#         row_number = i + product_list_start_row_index
#         values = sheet.row_values(row_number)
#         # sku_id = values[0].strip()
#         name = values[0]
#         description = values[0]
#         d1 = values[2]
#         d2 = values[7]
#         d3 = values[8]
#         d4 = values[11]
#         d5 = values[13]
#         d6 = values[9]
#         d7 = values[10]
#         # category = values[3].strip()
#         price = roundup(float(values[4]))
#         offer = 0
#         current_status = values[31].strip().lower()
#         script_status = values[32].strip()

#         if current_status == 'done' or script_status == 'Uploaded Successfully' or "Image not uploaded" in script_status:
#             print "skipping, already exist"
#             continue

#         print "Adding Product........."

#         try:            
#             category_obj = Category.objects.get(id=390)
#         except:
#             sheet.update_acell('T'+str(row_number),"Category not available")
#             continue

#         seller_obj = Seller.objects.get(mobile=seller_user_id)
#         try :
#             p = Product.objects.create(
#                 seller=seller_obj,
#                 name=name,
#                 description=description,
#                 price=price,
#                 wholesale_price=price,
#                 )
#             p.category.add(category_obj)
#             d = Discount.objects.create(product=p, discount=offer,discount_type="PERCENTAGE")
#             try:
#                 # upload image code
#                 sheet.update_acell('T'+str(row_number),"Uploaded Successfully")
#             except IOError:
#                 sheet.update_acell('T'+str(row_number),"Image not uploaded, product id:"+str(p.pk))
#         except Exception,e:
#             sheet.update_acell('T'+str(row_number),"-"+str(e))
#             try: 
#                 pi.delete()
#             except NameError: 
#                 print "dont know what is this"

#             try: 
#                 d.delete()
#             except NameError: 
#                 print "dont know what is this"

#             try: 
#                 p.delete()
#             except NameError: 
#                 print "dont know what is this"

# def upload_products_in_bulk_generic(work_book_name, sheet_index, product_list_start_row_index,
#      product_list_end_row_index,seller_user_id,main_category):
#     wks = gc.open(work_book_name)
#     sheet = wks.worksheets()[sheet_index]
    
#     no_of_products = product_list_end_row_index - product_list_start_row_index
#     for i in range(no_of_products):
#         row_number = i+product_list_start_row_index
#         values = sheet.row_values(row_number)
#         # sku_id = values[0].strip()
#         name = values[0]
#         description = name + "\n" + values[20]
#         d1 = values[2]
#         d2 = values[7]
#         d3 = values[8]
#         d4 = values[11]
#         d5 = values[13]
#         d6 = values[9]
#         d7 = values[10]


#         print d1
#         print d2
#         print d3
#         print d4
#         print d5
#         print d6
#         print d7

#         # category = values[3].strip()
#         price = roundup(float(values[4]))
#         offer = 0
#         current_status = values[31].strip().lower()
#         script_status = values[32].strip()

#         image_url_1 = values[25]
#         image_url_2 = values[26]
#         image_url_3 = values[27]
#         image_url_4 = values[28]
#         image_url_5 = values[29]

#         if current_status == 'done' or script_status == 'Uploaded Successfully' or "Image not uploaded" in script_status:
#             print "skipping, already exist"
#             continue

#         print "Adding Product........."

#         try:            
#             category_obj = Category.objects.get(id=390)
#         except:
#             sheet.update_acell('T'+str(row_number),"Category not available")
#             continue

#         seller_obj = Seller.objects.get(mobile=seller_user_id)

#         p = Product.objects.create(
#             seller=seller_obj,
#             name=name,
#             description=description,
#             price=price,
#             wholesale_price=price,
#             )
#         print "Added produded"
#         p.category.add(category_obj)
#         print "Category added"
#         d = Discount.objects.create(product=p, discount=offer,discount_type="PERCENTAGE")
#         print "discount object added"
#         try:
#             for i in range(5):
#                 if values[25+i] != '':
#                     response = requests.get(values[25 + i].split('?')[0] + "?raw=1", stream=True)
#                     file_name = "/tmp/" + name.replace(' ','_') + "_" + str(i) + ".jpg"
#                     with open(file_name, 'wb') as out_file:
#                         shutil.copyfileobj(response.raw, out_file)
#                         image = File(open(file_name,'rb'))
#                         ProductImage.objects.create(product=p,product_photo=image, display_priority=i+1)
#                         print str(i+1) + " image uploaded"
#             sheet.update_acell('T'+str(row_number),"Uploaded Successfully")
#             print "product " + name + "uploaded successfully"
#             print "adding description ....."
#         except IOError:
#             sheet.update_acell('T'+str(row_number),"Image not uploaded, product id:"+str(p.pk))
#         # description Update code 
#         c=CategoryWiseProductDescriptionKeys.objects.get(id=88)
#         ProductDescription.objects.create(product=p,product_desc_key=c,product_desc_value=d2)
#         c=CategoryWiseProductDescriptionKeys.objects.get(id=89)
#         ProductDescription.objects.create(product=p,product_desc_key=c,product_desc_value=d3)
#         c=CategoryWiseProductDescriptionKeys.objects.get(id=90)
#         ProductDescription.objects.create(product=p,product_desc_key=c,product_desc_value=d6)
#         c=CategoryWiseProductDescriptionKeys.objects.get(id=91)
#         ProductDescription.objects.create(product=p,product_desc_key=c,product_desc_value=d1)
#         c=CategoryWiseProductDescriptionKeys.objects.get(id=92)
#         ProductDescription.objects.create(product=p,product_desc_key=c,product_desc_value=d4)
#         c=CategoryWiseProductDescriptionKeys.objects.get(id=93)
#         ProductDescription.objects.create(product=p,product_desc_key=c,product_desc_value=d7)
#         c=CategoryWiseProductDescriptionKeys.objects.get(id=94)
#         ProductDescription.objects.create(product=p,product_desc_key=c,product_desc_value=d5)
#         print "all done .. kool"


