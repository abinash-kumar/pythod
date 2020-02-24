import csv
from abutils.spreadsheet_to_dbupdate import get_city_from_pincode
from django.shortcuts import get_object_or_404
from absupport.models import Pincode

file = open("testfile.txt", "a+")
pincodes_with_error = file.read().split(',')

with open("pincode.csv") as csv_file:
    readCSV = csv.reader(csv_file, delimiter=',')
    for row in readCSV:
        pincode = row[0]
        if Pincode.objects.filter(pincode=pincode).count() > 0 or pincode in pincodes_with_error:
            print "Already Updated or error", pincode
        else:
            city, state = get_city_from_pincode(pincode)
            if city == 'error' and state == 'error':
                print pincode, 'error'
                file.write(pincode)
                file.write(",")
            else:
                try:
                    Pincode.objects.create(pincode=pincode, city=city, state=state)
                    p = Pincode.objects.get(pincode=pincode)
                    p.state = state
                    p.city = city
                    p.save()
                    print "Already Updated", pincode, city, state
                except:
                    print "something went wrong for pincode ->", pincode
file.close()
