# coding:utf-8

import json

#捕获错误的  异常代码  异常信息
def catch_exception(request_result):
    error=''
    if 'Error' in request_result:
        result = json.loads(request_result)
        error = result['ErrorResponse']['Error']
    return error