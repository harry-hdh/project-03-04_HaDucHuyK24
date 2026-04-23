import random
from faker import Faker
import pandas as pd
import numpy as np
from faker_ecommerce import EcommerceProvider

faker = Faker()
faker.add_provider(EcommerceProvider)

faker_vn = Faker('vi_VN')
faker_vn.add_provider(EcommerceProvider)

pd.set_option('display.max_columns', None)
#print(fk.company())

def generate_brand_data(num_records):
    data = {
        'brand_name': [faker.brand_name() for _ in range(num_records)],
        'country': [faker.country() for _ in range(num_records)],
        'created_at': [faker.date_time_this_decade() for _ in range(num_records)]
    }
    return pd.DataFrame(data)

def generate_categories_data(num_records):
    root_data = {
        'category_name': ['Electronics', 'Fashion', 'Others'],
        'parent_category_id': [None, None, None],
        'level': [1, 1, 1],
        'created_at': [faker.date_time_this_decade() for _ in range(3)]
    }
    df_roots = pd.DataFrame(root_data)

    remaining_count = num_records - 2
    if remaining_count > 0:
        other_categories = ('Phones', 'Jackets', 'Head phone', 'Jeans', 'Shoes', 'AC', 'TV', 'Bags', 'Boots')
        data_others = {
            'category_name': [faker.unique.random_element(elements=other_categories) for _ in range(remaining_count)],
            'parent_category_id': [faker.random_int(min=1, max=3) for _ in range(remaining_count)],
            'level': [2] * remaining_count,
            'created_at': [faker.date_time_this_decade() for _ in range(remaining_count)]
        }
        df_others = pd.DataFrame(data_others)

        df =  pd.concat([df_roots, df_others], ignore_index=True)
    else:
        df = df_roots

    # df['parent_category_id'] = df['parent_category_id'].astype('Int64')
    # is_top_level = df['category_name'].isin(['Electronics', 'Fashion'])
    # df.loc[is_top_level, 'parent_category_id'] = None
    # df['level'] = is_top_level.map({True: 1, False: 2})

    return df

def generate_sellers_data(num_records):
    data = {
        'seller_name': [faker_vn.unique.company() for _ in range(num_records)],
        'join_date': [faker.date_between(start_date ='-1y', end_date = 'today') for _ in range(num_records)],
        'seller_type': [faker.random_element(elements=('Official', 'Marketplace', 'B2B')) for _ in range(num_records)],
        'rating': [round(faker.random.uniform(1, 5),1) for _ in range(num_records)],
        'country': 'Vietnam'
    }
    return pd.DataFrame(data)

def generate_products_data(num_records, cate_max=10, brand_max=20, seller_max=25):
    data = {
        'product_name': [faker.product_name(include_brand=True) for _ in range(num_records)],
        'category_id': [faker.random_int(min = 1, max = cate_max) for _ in range(num_records)],
        'brand_id': [faker.random_int(min = 1, max = brand_max) for _ in range(num_records)],
        'seller_id': [faker.random_int(min=1, max=seller_max) for _ in range(num_records)],
        'price': [round(faker.random.uniform(100000, 500000),2) for _ in range(num_records)],
        'discount_price': 0.00,
        'stock_qty': [faker.random_int(min = 0, max = num_records) for _ in range(num_records)],
        'rating': [round(faker.random.uniform(1, 5),1) for _ in range(num_records)],
        'created_at': [faker.date_time_this_decade() for _ in range(num_records)],
        'is_active': [faker.boolean(chance_of_getting_true=50) for _ in range(num_records)]
    }

    df =  pd.DataFrame(data)
    df['discount_price'] = (df['price'] * np.random.uniform(0.7, 1.0, size=num_records)).round(2)

    return df

def generate_promotions_data(num_records):
    data = {
        'promotion_name': [faker.random_element(elements=('Limited Time Offer', 'Buy One - Get One Free', 'Unlock Exclusive Access' , "Don't Miss Out", '80% Mega Sale')) for _ in range(num_records)],
        'promotion_type': [faker.random_element(elements=('product', 'category', 'seller', 'flash sale', 'online promotion')) for _ in range(num_records)],
        'discount_type': [faker.random_element(elements=('percentage', 'fixed_amount')) for _ in range(num_records)],
        'discount_value': [random.randrange(10, 100, 10) for _ in range(num_records)],
        'start_date': [faker.date_between(start_date ='-2y', end_date = 'today') for _ in range(num_records)],
        'end_date': 'yyyy-mm-dd'
    }

    df =  pd.DataFrame(data)
    df['end_date'] = df['start_date'] + pd.Timedelta(days=random.randint(30,50))

    return df

def generate_promotion_products_data(num_records, promotion_max=10, product_max = 1000):
    data = {
        'promotion_id': [faker.random_int(min=1, max=promotion_max) for _ in range(num_records)],
        'product_id': [faker.random_int(min=1, max=product_max) for _ in range(num_records)],
        'created_at': [faker.date_time_this_decade() for _ in range(num_records)]
    }

    return pd.DataFrame(data)

#df_brands = generate_brand_data(20)
# df_cats = generate_categories_data(10)
#df_sellers = generate_sellers_data(25)
#df_products = generate_products_data(1000)
#df_promotions = generate_promotions_data(10)
#df_promo_product = generate_promotion_products_data(100)
# print(df_cats.head(10))
# print(df_cats.info())
#print(df_cats.columns)