Host='192.168.55.5'
Port=3306
User='root'
Passwd='123456'
DB='smart_dolphin'
CharSet = 'utf8'

Tables = {
    'product': 'product',
    'product_dynamic': 'product_dynamic',
    'product_reviews': 'product_reviews'
}
Columns = {
    'product': ['id', 'asin', 'prod_title', 'prod_image', 'is_complete', 'platform', 'time'],
    'product_dynamic': ['id', 'asin', 'price', 'star', 'comments',
                        'rank_one', 'category_one', 'rank_two', 'category_two',
                        'rank_three', 'category_three', 'rank_four', 'category_four',
                        'rank_five', 'category_five', 'time'],
    'product_reviews': ['id', 'asin', 'review_title', 'review_content', 'attribute_one',
                        'attribute_two', 'votes', 'reviews_time', 'convert_time',
                        'review_author', 'review_star', 'time']
}