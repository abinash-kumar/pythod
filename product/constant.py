MENS_CATEGORY = {
    'men-half-sleeves-round-neck-tshirt': 'HALF ROUND TSHIRT',
    'men-full-sleeves-round-neck-tshirt': 'FULL SLEEVES',
    'men-polo-tshirt': 'POLO',
    'men-vest': 'VEST',
    'men-plain-tshirt': 'PLAIN',
}

WOMENS_CATEGORY = {
    'women-half-sleeves-round-neck-tshirt': 'HALF ROUND TSHIRT',
    'women-full-sleeves-round-neck-tshirt': 'FULL SLEEVES',
    'women-polo-tshirt': 'POLO',
    'croptop': 'CROPTOP',
    'women-plain-tshirt': 'PLAIN',
    'women-vest': 'TANKTOP',
}

COUPLE_CATEGORY = {
    # 'couple-half-sleeves-round-neck-tshirt': 'HALF ROUND TSHIRT',
    # 'couple-full-sleeves-round-neck-tshirt': 'FULL SLEEVES',
    # 'couple-polo-tshirt': 'POLO',
    # 'couple-plain-tshirt': 'PLAIN',
}


PRODUCT_VARIENTS = {
    'tshirt' : ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'kurti' : ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'hoodie' : ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'sweatshirt' : ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'furniture' : ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'lehenga' : ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'cap' : ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'saree' : ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'designerwear' : ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'handicraft' : ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'croptop' : ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'handbag' : ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'vest' : ['GENDER', 'COLOR', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
}

# CATEGORY_VARIENTS = {
#     'SIZE' : ['XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL', '5XL'],
#     'COLOR' : ['BLACK', 'WHITE', 'ANTRA GREY', 'GREY MELANGE', 'LIGHT GREY', 'DARK GREY', 'RED', 'ORANGE', 'MAROON', 'NAVY BLUE', 'YELLOW', 'ROYAL BLUE', 'BLUE', 'SKY BLUE'],
#     'FABRIC' : ['COTTON', 'TAIWAN', 'IMPORTED', 'PREMIUM', 'POLYCOTTON', 'KINTTED COTTON'],
#     'NECK' : ['ROUNDNECK', 'VNECK', 'POLO'],
#     'FITTING' : ['REGULARFIT', 'SLIMFIT', 'LOOSEFIT'],
#     'TYPE' : ['PLAIN', 'PRINTED'],
#     'SLEEVES' : ['HALFSLEEVES', 'FULLSLEEVES'],
#     'GENDER' : ['MALE', 'FEMALE', 'COUPLE'],
# }


ALL_CATEGORIES_LIST = MENS_CATEGORY.keys() + WOMENS_CATEGORY.keys() + \
    COUPLE_CATEGORY.keys()

ALL_CATEGORIES = ((i, i) for i in ALL_CATEGORIES_LIST)

SLUG_FOLDERNAME_MAP = {
    'men-half-sleeves-round-neck-tshirt': 'tshirt',
    'men-full-sleeves-round-neck-tshirt': 'fullroundmentshirts',
    'men-polo-tshirt': 'POLO',
    'men-vest': 'vest',
    'men-plain-tshirt': 'PLAIN',
    'women-half-sleeves-round-neck-tshirt': 'halfroundwomentshirts',
    'women-full-sleeves-round-neck-tshirt': 'fullroundwomentshirts',
    'women-polo-tshirt': 'POLO',
    'croptop': 'croptop',
    'women-plain-tshirt': 'PLAIN',
    'women-vest': 'tanktop',
}

VARIENT_PREFRENCE = {
    'tshirt': ['GENDER', 'COLOR', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC'],
    'croptop': ['COLOR', 'FITTING', 'SLEEVES', 'NECK', 'SIZE', 'TYPE', 'FABRIC'],
    'vest' : ['GENDER', 'COLOR', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
    'tanktop' : ['GENDER', 'COLOR', 'NECK', 'SIZE', 'TYPE', 'FABRIC', 'FITTING'],
}


# content

MENS_CLOTHING = """ ffdgdfg
"""

WOMENS_CLOTHING = """ ffdgdfg
"""

CUSTOMIZATION = """ sfsdfsdf
"""

ABOUT_PRINTED_TSHIRT = """
"""

ALL_PRODUCT_DESCRIPTION = """
"""
VARIENTS_NOT_TO_BE_SHOWN = [{'tshirt': 'COMBO_TYPE'}]
