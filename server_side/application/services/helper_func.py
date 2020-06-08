from flask import request


def set_limit_and_page(request):
    limit = 10
    page_num = 1
    if request.args.get('limit') is not None:
       limit = int(request.args.get('limit'))
    if request.args.get('page') is not None:
        page_num = int(request.args.get('page'))
    return limit, page_num