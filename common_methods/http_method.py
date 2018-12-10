# coding:utf-8
import json
from urllib.parse import unquote
import data_product

# 解析url中的参数
def resolve_params(request):
    data = request.request.body
    data = data.decode('utf-8').split('&')
    params = {}
    for item in data:
        params[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    return params

# 根据传参执行操作并返回json数据
def product_action(request):
    params = resolve_params(request)
    method = eval('data_product.' + params.get('method'))
    result_data = method(params)
    resp = http_response(result_data)
    return json.dumps(resp)

# api响应格式
def http_response(data):
    resp = {
        'code': 200,
        'data': data
    }
    if type(data) == list:
        resp['code'] = 200
    else:
        bad_request = data.get('BadRequestError', None)
        not_found = data.get('NotFoundError', None)
        error = data.get('Error', None)
        if bad_request:
            resp['code'] = 401
        if not_found:
            resp['code'] = 404
        if error:
            resp['code'] = 500
    return resp