from django_redis import get_redis_connection
import ast


class Offers():
    """docstring forOffersme"""

    def __init__(self):
        self.redis = get_redis_connection("default")

    def update_product_with_offers(self):
        self.redis.lpush()

    def update_offer(self, name, rule):
        self.redis.lpush('offers', rule)
        from product import offers
        this_offer = getattr(offers, rule)
        this_offer().update_on_product_cache()

    def refresh_offers_on_products(self):
        self.redis.delete('offers')
        from product import offers
        from product.models import ProductOffer
        offer_obj = ProductOffer.objects.filter(active=True)
        for i in offer_obj:
            if i.rule not in self.redis.lrange('offers', 0, -1):
                self.redis.lpush('offers', i.rule)
                self.redis.delete(i.rule)
        for i in self.redis.lrange('offers', 0, -1):
            this_offer = getattr(offers, i)
            this_offer().update_on_product_cache()

    @staticmethod
    def get_offer_on_product(product_id):
        offers_list = get_redis_connection("default").hget(
            "product:" + str(product_id), 'offer')
        if offers_list:
            return [str(i) for i in ast.literal_eval(offers_list) if offers_list]
        else:
            return []

    def get_discount_for_products(self, products):
        min_offer = 0
        offer_applied = ''
        from product import offers
        for i in self.redis.lrange('offers', 0, -1):
            this_offer = getattr(offers, i)
            offer, offer_name = this_offer().condition(products)
            if offer and not min_offer:
                min_offer = offer
                offer_applied = offer_name
            elif offer and offer < min_offer:
                min_offer = offer
                offer_applied = offer_name
        return offer_applied, min_offer


class BuyTwoPlainTshirtInDiscount(Offers):
    """docstring for BuyOneGetOne"""

    def all_eligible_products(self):
        value_from_cache = self.redis.lrange(self.__class__.__name__, 0, -1)
        if value_from_cache:
            return value_from_cache
        else:
            from auraai.models import ProductTagMap
            products = [i.product for i in ProductTagMap.objects.filter(
                tag__tag='plain tshirt')]
            for i in products:
                if i.active:
                    self.redis.lpush(self.__class__.__name__, i.id)
            return self.redis.lrange(self.__class__.__name__, 0, -1)

    def update_on_product_cache(self):
        products = self.all_eligible_products()
        for i in products:
            hash_key = 'product:' + i
            existing_product_dict = self.redis.hgetall(hash_key)
            if 'offer' in existing_product_dict.keys():
                offer_list = ast.literal_eval(existing_product_dict['offer'])
                offer_list.append(self.__class__.__name__)
                existing_product_dict.update({'offer': offer_list})
            else:
                existing_product_dict.update(
                    {'offer': [self.__class__.__name__]})
            self.redis.hmset(hash_key, existing_product_dict)

    def condition(self, products):
        discount = 0
        all_plain_tshirts = []
        product_total_count = 0
        for i in products.keys():
            if i in self.all_eligible_products():
                all_plain_tshirts.append(i)
                product_total_count = product_total_count + products[i]
        if len(all_plain_tshirts) % 2 == 0 and len(all_plain_tshirts) > 0:
            discount = 200
        return discount, self.__class__.__name__


class ChrismasDiscount(Offers):
    """docstring for BuyOneGetOne"""

    def all_eligible_products(self):
        value_from_cache = self.redis.lrange(self.__class__.__name__, 0, -1)
        if value_from_cache:
            return value_from_cache
        else:
            from product.models import ProductVarientList, Product
            products = [i for i in Product.objects.filter(
                wholesale_price=200)]
            all_product_varients = []
            for i in products:
                all_product_varients.extend(
                    [v for v in ProductVarientList.objects.filter(product=i)])
                self.redis.lpush("PRODUCTSOFFER:" +
                                 self.__class__.__name__, i.id)
            for i in all_product_varients:
                self.redis.lpush(self.__class__.__name__, i.id)
            return self.redis.lrange(self.__class__.__name__, 0, -1), self.redis.lrange("PRODUCTSOFFER:" + self.__class__.__name__, 0, -1)

    def update_on_product_cache(self):
        products = self.all_eligible_products()[1]
        from product.models import ProductOffer
        offer_name = ProductOffer.objects.get(
            rule=self.__class__.__name__).name
        for i in products:
            hash_key = 'product:' + i
            existing_product_dict = self.redis.hgetall(hash_key)
            if 'offer' in existing_product_dict.keys():
                offer_list = ast.literal_eval(existing_product_dict['offer'])
                offer_list.append(offer_name)
                existing_product_dict.update({'offer': offer_list})
            else:
                existing_product_dict.update({'offer': [offer_name]})
            self.redis.hmset(hash_key, existing_product_dict)

    def condition(self, products):
        discount = 0
        all_chrismas_tshirts = []
        product_total_count = 0
        for i in products.keys():
            if i in self.all_eligible_products():
                all_chrismas_tshirts.append(i)
                product_total_count = product_total_count + products[i]
        if product_total_count == 2:
            discount = 499
        elif product_total_count == 3:
            discount = 798
        return discount, self.__class__.__name__
