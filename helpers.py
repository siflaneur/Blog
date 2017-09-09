# coding=utf-8
from flask import request, render_template


def g_object_list(template_name, query, paginate_by=20, **content):
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    object_list = query.paginate(page, paginate_by)
    return render_template(template_name, object_list=object_list, **content)
