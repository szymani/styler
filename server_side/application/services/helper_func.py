from flask import request


def set_limit_and_page(request):
    limit = 10
    page_num = 1
    if request.args.get('limit') is not None:
        limit = int(request.args.get('limit'))
    if request.args.get('page') is not None:
        page_num = int(request.args.get('page'))
    return limit, page_num


def paginate_list(list_to_pag, page_num, limit):
    result = []
    for i in range((page_num - 1) * limit, page_num * limit):
        try:
            result.append(list_to_pag[i])
            # result.append(current_user.followers[i].as_dict())
        except:
            break
    return result
