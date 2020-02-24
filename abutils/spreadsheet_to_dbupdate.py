import gspread
from oauth2client.service_account import ServiceAccountCredentials
from designer.models import DesignerContactDetails
from designer.models import Designer
from product.models import Category
from product.models import Product, Discount, ProductImage, CategoryVarient, ProductVarientList
from django.core.files import File
from seller.models import Seller
from absupport.models import Pincode
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

import requests
import yaml

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'apidrive.json', scope)
gc = gspread.authorize(credentials)


# this script will fetch data from google drive spreadsheet
# workbook name = Designers contacts details
# sheet index= 0 for sheet1 which contain designer contact details


def read_all_from_sheet(work_book_name, sheet_index, row_start_index, row_end_index):
    wks = gc.open(work_book_name)
    sheet = wks.worksheets()[sheet_index]
    no_of_rows = row_end_index - row_start_index
    required_values = []
    for i in range(no_of_rows):
        row_number = i+row_start_index
        values = sheet.row_values(row_number)
        required_values.append(values)

    for i in required_values:
        p = DesignerContactDetails(name=i[1], email=i[2], mobile=i[
                                   3], website=i[4], address=i[5])
        p.save()


def stringsplitter(str_list):
    temp = str_list.split(',')
    d = []
    for x in temp:
        d.append(x.strip())
    return d


def update_from_sheet(work_book_name, sheet_index, row_start_index, row_end_index):
    wks = gc.open(work_book_name)
    sheet = wks.worksheets()[sheet_index]
    no_of_rows = row_end_index - row_start_index
    required_values = []
    count = 0
    for i in range(no_of_rows):
        row_number = i + row_start_index
        values = sheet.row_values(row_number)
        required_values.append(values)

    for i in required_values:
        if((not DesignerContactDetails.objects.filter(email=i[2]).exists()) or (not DesignerContactDetails.objects.filter(mobile=i[3]).exists()) or (i[2].strip() == "") or (i[3].strip() == "")):
            p = DesignerContactDetails(name=i[1], email=i[2], mobile=i[
                                       3], website=i[4], address=i[5])
            p.save()
            count = count + 1
        else:
            print(i[2])

    print("No of records updated " + str(count))


def bulk_upload_designer_sima(work_book_name="Designers contacts details", sheet_index=2, row_start_index=4, row_end_index=21):
    wks = gc.open(work_book_name)
    sheet = wks.worksheets()[sheet_index]
    no_of_rows = row_end_index - row_start_index
    required_values = []
    count = 0
    for i in range(no_of_rows):
        row_number = i + row_start_index
        values = sheet.row_values(row_number)
        required_values.append(values)

    category1 = Category.objects.get(name="Designer Wear")
    category2 = Category.objects.get(name="Women")
    designer = Designer.objects.get(id=1)  # 1 sima meheta designer id is 1

    for i in required_values:
        product = Product.objects.create(seller=designer.designer,
                                         name=i[1],
                                         description=i[2],
                                         price=i[7],
                                         wholesale_price=i[7],
                                         active=True,
                                         is_customization_available=True,
                                         product_type=Product.DESIGNER_TYPE[0],
                                         )
        product.save()  # todo product size and quantity
        product.category = [category1, category2] + \
            list(Category.objects.filter(name__icontains=i[5]))
        product.save()
        d = Discount.objects.create(
            product=product, discount_type="PERCENTAGE")
        try:
            File(open('tmp/sima/' + i[1].replace(" ", "-") + '.jpg', 'rb'))
            pi = ProductImage.objects.create(product=product, product_photo=File(
                open('tmp/sima/' + i[1].replace(" ", "-") + '.jpg', 'rb')))
        except IOError:
            print "Image not uploaded, product id:" + str(product.pk)
        count = count + 1
    print("No of records updated " + str(count))


def bulk_upload_tshirt(work_book_name, sheet_index, row_start_index, row_end_index, gender):
    wks = gc.open(work_book_name)
    sheet = wks.worksheets()[sheet_index]
    no_of_rows = row_end_index - row_start_index
    required_values = []
    count = 0
    for i in range(no_of_rows):
        row_number = i + row_start_index
        values = sheet.row_values(row_number)
        required_values.append(values)

    for i in required_values:
        updated = False
        if "ERROR" in i[0] or len(i[0]) == 0:
            try:
                product = Product.objects.create(seller=Seller.objects.get(id=1),
                                                 name=i[2],
                                                 description=i[3],
                                                 price=i[8],
                                                 wholesale_price=i[8],
                                                 active=True,
                                                 is_customization_available=True,
                                                 product_type=Product.DESIGNER_TYPE[
                                                     1],
                                                 )
                product.save()
                cat_objs = []
                for j in i[14:19]:
                    cat_obj = Category.objects.filter(name=j)
                    cat_obj = [
                        k for k in cat_obj if k.get_main_parent() == gender]
                    cat_objs = cat_objs + cat_obj
                product.category = cat_objs
                product.save()
                p_cat_objs = []
                for cat_obj in cat_objs:
                    p_cat_objs = p_cat_objs + cat_obj.get_branch_nodes()
                p_cat_objs = set(p_cat_objs)

                cat_obj = Category.objects.get(id=381)

                fabric_varients = CategoryVarient.objects.filter(
                    category=cat_obj, varient_type='FABRIC', value=i[6].upper().strip())
                fitting_varients = CategoryVarient.objects.filter(
                    category=cat_obj, varient_type='FITTING', value=i[5].upper().strip())
                neck_varients = CategoryVarient.objects.filter(
                    category=cat_obj, varient_type='NECK', value=i[11].upper().strip())
                sleeves_varients = CategoryVarient.objects.filter(
                    category=cat_obj, varient_type='SLEEVES', value=i[12].upper().strip())
                size_varients = CategoryVarient.objects.filter(
                    category=cat_obj, varient_type='SIZE')

                size = [j.strip() for j in i[9].upper().split(',')]
                colors = [j.strip() for j in i[10].upper().split(',')]

                for varient in size_varients:
                    if varient.varient_type == "SIZE" and varient.value in size:
                        for color in colors:
                            varient2 = []
                            color_var_objs = CategoryVarient.objects.filter(
                                category=cat_obj, varient_type='COLOR', value=color.upper())
                            if len(color_var_objs) > 0:
                                varient2 = [color_var_objs[0]]
                            else:
                                cv = CategoryVarient.objects.create(
                                    category=cat_obj, varient_type="COLOR", value=color.upper())
                                varient2 = [cv]
                            pv = ProductVarientList.objects.create(
                                product=product, quantity=i[13], price=i[8])
                            pv.key = list([varient]) + list(varient2) + list(fabric_varients) + list(
                                fitting_varients) + list(neck_varients) + list(sleeves_varients)
                            pv.save()
                do = Discount.objects.create(
                    product=product, discount_type="FLAT", discount=int(i[8]) - int(i[7]))
                try:
                    img = File(open('/tmp/tshirt/' + i[2] + '.jpg', 'rb'))
                    ProductImage.objects.create(
                        product=product, product_photo=img)
                    updated = True
                except IOError:
                    product.delete()
                    do.delete()
                    print "Image not uploaded, product id:" + str(product.pk)
                count = count + 1

                if updated:
                    for l in range(2, 5):
                        try:
                            img = File(
                                open('/tmp/tshirt/' + i[2] + " " + str(l) + '.jpg', 'rb'))
                            ProductImage.objects.create(
                                product=product, product_photo=img)
                        except IOError:
                            print "--"
                    sheet.update_acell(
                        'A' + str(required_values.index(i) + row_start_index), product.id)

                else:
                    error = 'ERROR : image not found /tmp/tshirt/' + \
                        i[2] + '.jpg'
                    sheet.update_acell(
                        'A' + str(required_values.index(i) + row_start_index), error)
            except Exception, e:
                sheet.update_acell(
                    'A' + str(required_values.index(i) + row_start_index), "ERROR" + str(e))
    print("No of records updated " + str(count))





def pincode_update(work_book_name, sheet_index, row_start_index, row_end_index):
    wks = gc.open(work_book_name)
    sheet = wks.worksheets()[sheet_index]
    no_of_rows = row_end_index - row_start_index
    required_values = []
    count = 0
    for i in range(no_of_rows):
        row_number = i + row_start_index
        values = sheet.row_values(row_number)
        required_values.append(values)
    
    for row in required_values:
        if row[1].strip() == "" or row[1].strip() == 'error':
            pincode = row[0]
            city,state = get_city_from_pincode(pincode)
            if city == 'error' and state == 'error':
                print pincode,'error'
            else:
                try:
                    Pincode.objects.create(pincode=pincode,city=city,state=state)
                    print pincode,city,state
                except IntegrityError:
                    p = Pincode.objects.get(pincode=pincode)
                    p.state = state
                    p.city = city
                    p.save()
                    print "Updated",pincode,city,state

            sheet.update_acell('B' + str(required_values.index(row) + row_start_index), city)
            sheet.update_acell('C' + str(required_values.index(row) + row_start_index), state)



def get_city_from_pincode(pincode):
    req_url = "http://postalpincode.in/api/pincode/"
    resp = requests.get(req_url + pincode )
    data = yaml.load(resp.content)

    if data['Status'] == 'Success':
        state = data['PostOffice'][0]['State']
        district = data['PostOffice'][0]['District']
        return district,state
    else:
        return 'error','error'
        


def bulk_update_varients_tshirt(work_book_name, sheet_index, row_start_index, row_end_index, gender):
    wks = gc.open(work_book_name)
    sheet = wks.worksheets()[sheet_index]
    no_of_rows = row_end_index - row_start_index
    required_values = []
    count = 0
    for i in range(no_of_rows):
        row_number = i + row_start_index
        values = sheet.row_values(row_number)
        required_values.append(values)

    cat_obj = Category.objects.get(name='tshirt')

    fabric_varients = CategoryVarient.objects.filter(
                    category=cat_obj, varient_type='FABRIC', value='COTTON')
    fitting_varients = CategoryVarient.objects.filter(
                    category=cat_obj, varient_type='FITTING', value='REGULAR FIT')
    neck_varients = CategoryVarient.objects.filter(
                    category=cat_obj, varient_type='NECK', value='ROUND NECK')
    sleeves_varients = CategoryVarient.objects.filter(
                    category=cat_obj, varient_type='SLEEVES', value='HALF SLEEVES')
    size_varients = CategoryVarient.objects.filter(
                    category=cat_obj, varient_type='SIZE')
    for i in required_values:
        try:
            product = Product.objects.get(name=i[2])
            colors = [j.strip() for j in i[10].upper().split(',')]
            print (product, i[13],i[8])
            for varient in size_varients:
                for color in colors:
                    varient2 = []
                    color_var_objs = CategoryVarient.objects.filter(
                                category=cat_obj, varient_type='COLOR', value=color.upper())
                    if len(color_var_objs) > 0:
                        varient2 = [color_var_objs[0]]
                    else:
                        print 'COLOR NOT FOUND-',color,'   ', product.name
                    pv = ProductVarientList.objects.create(product=product, quantity=i[13], price=i[8])
                    pv.key = list([varient]) + list(varient2) + list(fabric_varients) + list(fitting_varients) + list(neck_varients) + list(sleeves_varients)
                    pv.save()
                    print list([varient]) + list(varient2) + list(fabric_varients) + list(fitting_varients) + list(neck_varients) + list(sleeves_varients)
            print '----------------------------------------------------------------------------------'

        except ObjectDoesNotExist:
            print 'product Not Found ' + i[2]

    print 'end'