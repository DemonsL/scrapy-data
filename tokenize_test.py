# coding:utf-8

import pymysql

# 查询
def select_sql(sql):
    db = pymysql.connect(host='192.168.55.6', user='root', password='123456', port=3306, db='smart_dolphin',
                         charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    resp = cursor.fetchall()
    db.commit()
    return resp

# 更新
def update_sql(id, status):
    db = pymysql.connect(host='192.168.55.6', user='root', password='123456', port=3306, db='smart_dolphin',
                         charset="utf8")
    cursor = db.cursor()
    sql = 'UPDATE shoes_word SET status = "%s" WHERE id = "%s";' % (status, id)
    cursor.execute(sql)
    db.commit()


def tokenize_test():
    shoes_sql = 'SELECT id, keyword FROM shoes_word where status is null  and id between 102488 and 220000;'
    use_shoes_sql = 'SELECT words FROM use_unquite_shoes;'
    unuse_shoes_sql = 'SELECT words FROM unuse_unquite_shoes;'
    # 鞋类词表
    shoes = list(select_sql(shoes_sql))
    # 有用词表
    use_words = select_sql(use_shoes_sql)
    use_words = [word[0] for word in use_words]
    # 无用词表
    unuse_words = select_sql(unuse_shoes_sql)
    unuse_words = [word[0] for word in unuse_words]

    data = {}
    c, n, m = 0, 0, 0
    for shoe in shoes:
        c += 1
        shoe = list(shoe)
        if shoe[1] in use_words:
            data[shoe[0]] = 1
            n += 1
        if shoe[1] in unuse_words:
            data[shoe[0]] = 2
            m += 1
    print('总数：%s, 有用：%s, 无用：%s'% (c, n, m))
    return data



if __name__ == '__main__':
    data = tokenize_test()
    print('start...')
    for key, value in data.items():
        update_sql(key, value)
    print('done!')

