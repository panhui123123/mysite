import copy

from django.utils.safestring import mark_safe


class Pagination:
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        '''
        :param request: 请求的对象
        :param queryset: 符合的数据（根据这个数据分页处理）
        :param page_size: 每一页显示多少数据
        :param page_param: 在URl中获取分页的参数（/pretty/list/?page=1）
        :param plus: 显示当前页 前或后几页
        '''
        # 获取当前url里面的参数，我们就搞为page好了
        self.page_param = page_param
        # 获取url里面的参数值，如果是空字符串，默认为1
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        # 类属性page赋值
        self.page = page
        self.page_size = page_size
        # 当前页数据的索引开始、结束
        self.start = (page - 1) * page_size
        self.end = page * page_size
        # 获取当前页的这几个数据
        self.page_queryset = queryset[self.start: self.end]
        # 总页码数
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        # 下述是为了解决，搜索出一堆数据之后，切换分页数据时，会将搜索条件去掉的问题
        # 拼接查询条件 ?q=888&xx=123&page=12 QueryDict:{'q':['888'],'xx':['123']}
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.plus = plus

    def html(self):
        # 1、计算出显示当前页的前5页and后5页
        # 数据库中数据比较少，没有达到11项
        if self.total_page_count <= 2 * self.plus + 1:
            self.start_page = 1
            self.end_page = self.total_page_count
        # 数据库中数据比较多，大于11项
        else:
            # 当前页page<5时（小极值）
            if self.page <= self.plus:
                self.start_page = 1
                self.end_page = 2 * self.plus + 1
            else:
                # 当前页page>5
                # 当前页+5 > 总页数
                if (self.page + self.plus) > self.total_page_count:
                    self.start_page = self.total_page_count - 2 * self.plus
                    self.end_page = self.total_page_count
                    # 当前页+5 < 总页数
                else:
                    self.start_page = self.page - self.plus
                    self.end_page = self.page + self.plus

        page_str_list = []  # 装html代码

        # 2.首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 3.上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                self.query_dict.urlencode())
        else:
            prev = '<li class="disabled"><span aria-hidden="true">&laquo;</span></li>'
        page_str_list.append(prev)

        # 4.页面
        for i in range(self.start_page, self.end_page + 1):
            print(self.start_page, self.end_page + 1)
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 5.下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    self.query_dict.urlencode())
        else:
            prev = '<li class="disabled"><span aria-hidden="true">&raquo;</span></li>'
        page_str_list.append(prev)

        # 6.尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_string = """
                <li>
                    <form style="float: left; margin-left: -1px"  method="get">
                        <input type="text" style="position: relative; float: left; display: inline-block; width: 80px;
                        border-radius: 0; " class="form-control" placeholder="页码" name="page">
                        <button style="border-radius: 0" class="btn btn-primary" type="submit">跳转</button>
                    </form>
                </li>
                """

        page_str_list.append(search_string)

        # mark_safe()没有这个的话，页面会直接显示html代码
        # page_str_list里的html代码拼接成一串字符串，并返回
        page_string = mark_safe("".join(page_str_list))
        return page_string
