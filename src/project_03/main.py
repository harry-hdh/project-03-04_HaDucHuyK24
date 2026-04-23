import psycopg2
import io
from config import load_config
from generate_data import generate_promotions_data, generate_products_data, generate_brand_data, generate_sellers_data, generate_promotion_products_data, generate_categories_data


def insert_data(data,table_name):
    buffer = io.StringIO()
    data.to_csv(buffer, index=False, header=False, na_rep=r'\N')
    buffer.seek(0)

    columns = tuple(data.columns)

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cur = conn.cursor()

        cur.copy_from(buffer, table_name, sep=',', columns=columns)

        conn.commit()
        cur.close()
        conn.close()
        print(f'>>> {table_name} - Done!')
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    insert_data(generate_brand_data(20),'brands')
    insert_data(generate_categories_data(10), 'categories')
    insert_data(generate_sellers_data(25), 'sellers')
    insert_data(generate_products_data(1000), 'products')
    insert_data(generate_promotions_data(10), 'promotions')
    insert_data(generate_promotion_products_data(100), 'promotion_product')