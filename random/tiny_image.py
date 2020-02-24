from PIL import Image
for path, subdirs, files in os.walk("/development/src/uploads/product_photo"):
    for name in files:
        try:
            image = Image.open(os.path.join(path, name))
            image.save(path + "/tiny_" + image.filename.rsplit('/', 1)
                       [1], image.format, quality=1, optimize=True)
        except IOError:
            print "leaving for -->" + path + name


 "tiny_" + image.filename.rsplit('/', 1)[1], image.format, quality=1, optimize=True
