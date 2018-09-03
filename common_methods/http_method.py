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
def action(request):
    params = resolve_params(request)
    method = eval('data_product.' + params.get('method'))
    result = method(params)
    return json.dumps(result)