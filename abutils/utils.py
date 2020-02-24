import requests
import json
from django.conf import settings
import os
from PIL import Image
from codeab.celery import app
from product.models import Category
import shutil
import tinify
import urllib2


def get_shorten_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key={}'.format(
        settings.GOOGLE_SHORT_URL_KEY)
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    return r.json()


@app.task
def prerender_page_create(url, desktop_file_name, mobile_file_name):
    print "on prerender..........."
    path = os.path.join(settings.BASE_DIR, "templates", "cached")
    print "path", path
    desktop_url = "http://localhost:3000/render?url=https://www.addictionbazaar.com{}?prerender=true".format(url)
    mobile_url = "http://localhost:3000/render?width=500&url=https://www.addictionbazaar.com{}?prerender=true".format(url)
    desktop_page = urllib2.urlopen(desktop_url)
    desktop_page_data = desktop_page.read()
    mobile_page = urllib2.urlopen(mobile_url)
    mobile_page_data = mobile_page.read()

    with open(os.path.join(path, desktop_file_name), "w+") as desktop_version_file:
        desktop_version_file.write(desktop_page_data)
    with open(os.path.join(path, mobile_file_name), "w+") as mobile_version_file:
        mobile_version_file.write(mobile_page_data)

@app.task
def create_tshirts_from_design(design_file_path, id):
    path = os.path.join(settings.BASE_DIR,
                        "uploads/raw_products/tshirt/raw_images")
    if os.path.exists(path):
        print "creting tshirt"
        tshirts_file_path = [path + "/" + i for i in os.listdir(path)]
        final_dir = "uploads/raw_products/tshirt/final/" + str(id)
        if os.path.exists(final_dir):
            shutil.rmtree(final_dir)
        os.mkdir(final_dir)
        os.mkdir(final_dir + "/tmp/")
        for t in tshirts_file_path:
            trans = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/tshirt/trans.png'))
            effect = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/tshirt/trans1.png'))
            background = Image.open(t)
            bg = trans.copy()
            foreground = Image.open(design_file_path)
            new_h = background.height * 0.33
            new_w = (new_h) * foreground.height / foreground.width
            fg = foreground.resize((int(new_h), int(new_w)), Image.ANTIALIAS)
            bg.paste(fg, ((background.width - fg.width) / 2 - 5, 240))
            save_path = os.path.join(settings.BASE_DIR, "uploads/raw_products/tshirt/final/" + str(id) + "/tmp",
                                     design_file_path.rsplit('/', 1)[1].split('.')[0] + ".png")
            bg.save(save_path)
            final_name = (str(id) + '_' + t.rsplit('/', 1)
                          [1]).replace(' ', '_')
            base_design = Image.alpha_composite(background.convert("RGBA"), bg)
            Image.alpha_composite(base_design, effect).save(
                os.path.join(settings.BASE_DIR, final_dir, final_name))
        shutil.rmtree(final_dir + "/tmp/")
    else:
        print 'category Image folder not present-tshirt'


@app.task
def create_fullroundmentshirts_from_design(design_file_path, id):
    path = os.path.join(settings.BASE_DIR,
                        "uploads/raw_products/fullroundmentshirts/raw_images")
    if os.path.exists(path):
        print "creting fullroundmentshirts"
        tshirts_file_path = [path + "/" + i for i in os.listdir(path)]
        final_dir = "uploads/raw_products/fullroundmentshirts/final/" + str(id)
        if os.path.exists(final_dir):
            shutil.rmtree(final_dir)
        os.mkdir(final_dir)
        os.mkdir(final_dir + "/tmp/")
        for t in tshirts_file_path:
            trans = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/fullroundmentshirts/trans.png'))
            effect = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/fullroundmentshirts/trans1.png'))
            background = Image.open(t)
            bg = trans.copy()
            foreground = Image.open(design_file_path)
            new_h = background.height * 0.35
            new_w = (new_h) * foreground.height / foreground.width
            fg = foreground.resize((int(new_h), int(new_w)), Image.ANTIALIAS)
            bg.paste(fg, ((background.width - fg.width) / 2, 250))
            save_path = os.path.join(settings.BASE_DIR, "uploads/raw_products/fullroundmentshirts/final/" + str(id) + "/tmp",
                                     design_file_path.rsplit('/', 1)[1].split('.')[0] + ".png")
            bg.save(save_path)
            final_name = (str(id) + '_' + t.rsplit('/', 1)
                          [1]).replace(' ', '_')
            base_design = Image.alpha_composite(background.convert("RGBA"), bg)
            Image.alpha_composite(base_design, effect).save(
                os.path.join(settings.BASE_DIR, final_dir, final_name))
        shutil.rmtree(final_dir + "/tmp/")
    else:
        print 'category Image folder not present-tshirt'


@app.task
def create_fullroundwomentshirts_from_design(design_file_path, id):
    path = os.path.join(settings.BASE_DIR,
                        "uploads/raw_products/fullroundwomentshirts/raw_images")
    if os.path.exists(path):
        print "creting fullroundwomentshirts"
        tshirts_file_path = [path + "/" + i for i in os.listdir(path)]
        final_dir = "uploads/raw_products/fullroundwomentshirts/final/" + \
            str(id)
        if os.path.exists(final_dir):
            shutil.rmtree(final_dir)
        os.mkdir(final_dir)
        os.mkdir(final_dir + "/tmp/")
        for t in tshirts_file_path:
            trans = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/fullroundwomentshirts/trans.png'))
            effect = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/fullroundwomentshirts/trans1.png'))
            background = Image.open(t)
            bg = trans.copy()
            foreground = Image.open(design_file_path)
            new_h = background.height * 0.30
            new_w = (new_h) * foreground.height / foreground.width
            fg = foreground.resize((int(new_h), int(new_w)), Image.ANTIALIAS)
            bg.paste(fg, ((background.width - fg.width) / 2, 300))
            save_path = os.path.join(settings.BASE_DIR, "uploads/raw_products/fullroundwomentshirts/final/" + str(id) + "/tmp",
                                     design_file_path.rsplit('/', 1)[1].split('.')[0] + ".png")
            bg.save(save_path)
            final_name = (str(id) + '_' + t.rsplit('/', 1)
                          [1]).replace(' ', '_')
            base_design = Image.alpha_composite(background.convert("RGBA"), bg)
            Image.alpha_composite(base_design, effect).save(
                os.path.join(settings.BASE_DIR, final_dir, final_name))
        shutil.rmtree(final_dir + "/tmp/")
    else:
        print 'Women Full Tshirt Image folder not present '


@app.task
def create_croptop_from_design(design_file_path, id):
    path = os.path.join(settings.BASE_DIR,
                        "uploads/raw_products/croptop/raw_images")
    if os.path.exists(path):
        print "creting croptop"
        tshirts_file_path = [path + "/" + i for i in os.listdir(path)]
        final_dir = "uploads/raw_products/croptop/final/" + \
            str(id)
        if os.path.exists(final_dir):
            shutil.rmtree(final_dir)
        os.mkdir(final_dir)
        os.mkdir(final_dir + "/tmp/")
        for t in tshirts_file_path:
            trans = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/croptop/trans.png'))
            effect = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/croptop/trans1.png'))
            background = Image.open(t)
            bg = trans.copy()
            foreground = Image.open(design_file_path)
            new_h = background.height * 0.2
            new_w = (new_h) * foreground.height / foreground.width
            fg = foreground.resize((int(new_h), int(new_w)), Image.ANTIALIAS)
            bg.paste(fg, ((background.width - fg.width) / 2, 250))
            save_path = os.path.join(settings.BASE_DIR, "uploads/raw_products/croptop/final/" + str(id) + "/tmp",
                                     design_file_path.rsplit('/', 1)[1].split('.')[0] + ".png")
            bg.save(save_path)
            final_name = (str(id) + '_' + t.rsplit('/', 1)
                          [1]).replace(' ', '_')
            base_design = Image.alpha_composite(background.convert("RGBA"), bg)
            Image.alpha_composite(base_design, effect).save(
                os.path.join(settings.BASE_DIR, final_dir, final_name))
        shutil.rmtree(final_dir + "/tmp/")
    else:
        print 'Women Full Tshirt Image folder not present '


@app.task
def create_halfroundwomentshirts_from_design(design_file_path, id):
    path = os.path.join(settings.BASE_DIR,
                        "uploads/raw_products/halfroundwomentshirts/raw_images")
    if os.path.exists(path):
        print "creting halfroundwomentshirts"
        tshirts_file_path = [path + "/" + i for i in os.listdir(path)]
        final_dir = "uploads/raw_products/halfroundwomentshirts/final/" + \
            str(id)
        if os.path.exists(final_dir):
            shutil.rmtree(final_dir)
        os.mkdir(final_dir)
        os.mkdir(final_dir + "/tmp/")
        for t in tshirts_file_path:
            trans = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/halfroundwomentshirts/trans.png'))
            effect = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/halfroundwomentshirts/trans1.png'))
            background = Image.open(t)
            bg = trans.copy()
            foreground = Image.open(design_file_path)
            new_h = background.height * 0.3
            new_w = (new_h) * foreground.height / foreground.width
            fg = foreground.resize((int(new_h), int(new_w)), Image.ANTIALIAS)
            bg.paste(fg, ((background.width - fg.width) / 2, 250))
            save_path = os.path.join(settings.BASE_DIR, "uploads/raw_products/halfroundwomentshirts/final/" + str(id) + "/tmp",
                                     design_file_path.rsplit('/', 1)[1].split('.')[0] + ".png")
            bg.save(save_path)
            final_name = (str(id) + '_' + t.rsplit('/', 1)
                          [1]).replace(' ', '_')
            base_design = Image.alpha_composite(background.convert("RGBA"), bg)
            Image.alpha_composite(base_design, effect).save(
                os.path.join(settings.BASE_DIR, final_dir, final_name))
        shutil.rmtree(final_dir + "/tmp/")
    else:
        print 'Women Full Tshirt Image folder not present '


@app.task
def create_vest_from_design(design_file_path, id):
    path = os.path.join(settings.BASE_DIR,
                        "uploads/raw_products/vest/raw_images")
    if os.path.exists(path):
        print "creting Vests"
        tshirts_file_path = [path + "/" + i for i in os.listdir(path)]
        final_dir = "uploads/raw_products/vest/final/" + \
            str(id)
        if os.path.exists(final_dir):
            shutil.rmtree(final_dir)
        os.mkdir(final_dir)
        os.mkdir(final_dir + "/tmp/")
        for t in tshirts_file_path:
            trans = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/vest/trans.png'))
            effect = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/vest/trans1.png'))
            background = Image.open(t)
            bg = trans.copy()
            foreground = Image.open(design_file_path)
            new_h = background.height * 0.35
            new_w = (new_h) * foreground.height / foreground.width
            fg = foreground.resize((int(new_h), int(new_w)), Image.ANTIALIAS)
            bg.paste(fg, ((background.width - fg.width) / 2, 350))
            save_path = os.path.join(settings.BASE_DIR, "uploads/raw_products/vest/final/" + str(id) + "/tmp",
                                     design_file_path.rsplit('/', 1)[1].split('.')[0] + ".png")
            bg.save(save_path)
            final_name = (str(id) + '_' + t.rsplit('/', 1)
                          [1]).replace(' ', '_')
            base_design = Image.alpha_composite(background.convert("RGBA"), bg)
            Image.alpha_composite(base_design, effect).save(
                os.path.join(settings.BASE_DIR, final_dir, final_name))
        shutil.rmtree(final_dir + "/tmp/")
    else:
        print 'Vest folder not present '

@app.task
def create_tanktop_from_design(design_file_path, id):
    path = os.path.join(settings.BASE_DIR,
                        "uploads/raw_products/tanktop/raw_images")
    if os.path.exists(path):
        print "creating tanktop"
        tshirts_file_path = [path + "/" + i for i in os.listdir(path)]
        final_dir = "uploads/raw_products/tanktop/final/" + \
            str(id)
        if os.path.exists(final_dir):
            shutil.rmtree(final_dir)
        os.mkdir(final_dir)
        os.mkdir(final_dir + "/tmp/")
        for t in tshirts_file_path:
            trans = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/tanktop/trans.png'))
            effect = Image.open(os.path.join(
                settings.BASE_DIR, 'uploads/raw_products/tanktop/women-tank-top.png'))
            background = Image.open(t)
            bg = trans.copy()
            foreground = Image.open(design_file_path)
            new_h = background.height * 0.35
            new_w = (new_h) * foreground.height / foreground.width
            fg = foreground.resize((int(new_h), int(new_w)), Image.ANTIALIAS)
            bg.paste(fg, ((background.width - fg.width) / 2, 350))
            save_path = os.path.join(settings.BASE_DIR, "uploads/raw_products/tanktop/final/" + str(id) + "/tmp",
                                     design_file_path.rsplit('/', 1)[1].split('.')[0] + ".png")
            bg.save(save_path)
            final_name = (str(id) + '_' + t.rsplit('/', 1)
                          [1]).replace(' ', '_')
            base_design = Image.alpha_composite(background.convert("RGBA"), bg)
            Image.alpha_composite(base_design, effect).save(
                os.path.join(settings.BASE_DIR, final_dir, final_name))
        shutil.rmtree(final_dir + "/tmp/")
    else:
        print 'Tanktop folder not present '

def create_products(design_file_path, id):
    print "creating Products"
    print design_file_path
    print id
    create_tshirts_from_design.delay(design_file_path, id)
    create_fullroundmentshirts_from_design.delay(design_file_path, id)
    create_fullroundwomentshirts_from_design.delay(design_file_path, id)
    create_croptop_from_design.delay(design_file_path, id)
    create_halfroundwomentshirts_from_design.delay(design_file_path, id)
    create_vest_from_design.delay(design_file_path, id)
    create_tanktop_from_design.delay(design_file_path, id)    


def create_tiny_artist_design(design_path, new_path):
    _create_tiny_designs.delay(design_path, new_path)


@app.task
def _create_tiny_designs(design_path, new_path):
    print 'creating tiny design'
    print '\n' + design_path + '\n' + new_path
    tinify.key = "JGVHFxx6OrgRldx1v525qZRAmUhBjCkq"
    source = tinify.from_file(design_path)
    resized = source.resize(method="scale", width=500)
    resized.to_file(new_path)
