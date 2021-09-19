# 分页搜索
from django.utils.safestring import mark_safe  #{{ page_html|safe }}

class Paging:

    def __init__(self,current_page_number,total_count,per_page_num,page_number_show,recv_data=None):
        """

        :param current_page_number: 当前页码
        :param total_count:         总数据量
        :param per_page_num:    每页显示多少条数据
        :param page_number_show:    总共显示多少个页码
        :total_page_count:          总的页码数
        :param star_page_number:    起始页码
        :param end_page_number:     结束页码
        """
        self.recv_data = recv_data   # <QueryDict: {'search_field': ['qq'], 'keyword': ['172']}>


        try:  # 防止恶意输入错误代码
            current_page_number = int(current_page_number)
        except Exception:
            current_page_number = 1

        half_number = page_number_show // 2

        a, b = divmod(total_count, per_page_num)  # 商和余数
        if b:  # 如果余数不为0，页码总数为商加一
            total_page_count = a + 1
        else:
            total_page_count = a

        # 如果当前页码大于等于总页数，默认显示最后一页----并处理没有数据时total——page_count=0的情况
        if current_page_number >= total_page_count:
            current_page_number = total_page_count

        # 如果当前页码小于等于0时，默认显示第一页
        if current_page_number <= 0:
            current_page_number = 1

        start_page_number = current_page_number - half_number  #
        end_page_number = current_page_number + half_number + 1  # 6

        if start_page_number <= 0:
            start_page_number = 1
            end_page_number = page_number_show + 1  # 7

        if end_page_number >= total_page_count:  # 6 > 2
            start_page_number = total_page_count - page_number_show + 1  # -4
            end_page_number = total_page_count + 1  # 3

        # 如果总页数小于需要展示的页数
        if total_page_count < page_number_show:
            start_page_number = 1
            end_page_number = total_page_count + 1

        self.current_page_number = current_page_number
        self.per_page_num = per_page_num
        self.total_page_count = total_page_count
        self.start_page_number = start_page_number
        self.end_page_number = end_page_number

    @property
    def start_data_number(self):
        return (self.current_page_number -1)*self.per_page_num

    @property
    def end_data_number(self):
        return self.current_page_number * self.per_page_num

    @property
    def page_html_func(self):
        # 页面数据
        page_html = '''
                     <nav aria-label="Page navigation" class="center-block" style="width:450px; margin-">
                          <ul class="pagination">
            '''
        self.recv_data['page'] = 1
        # print(self.recv_data.urlencode(),'xxx')  # search_field=customer__name__contains&keyword=xm&page=1 xxx
        first_page = f"""
                               <li>
                                 <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                                   <span aria-hidden="true">首页</span>
                                 </a>
                               </li>"""
        page_html += first_page
        self.recv_data['page'] = self.current_page_number - 1
        previous_page = f"""
                          <li>
                            <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                              <span aria-hidden="true">&laquo;</span>
                            </a>
                          </li>
                          """
        page_html += previous_page
        for i in range(self.start_page_number,self.end_page_number):
            self.recv_data['page'] = i
            if i == self.current_page_number:

                page_html += f'<li class="active"><a href="?{self.recv_data.urlencode()}">{i}</a></li>'
            else:
                page_html += f"""<li><a href="?{self.recv_data.urlencode()}">{i}</a></li>"""

        self.recv_data['page'] = self.current_page_number + 1
        next_page = f'''
                    <li>
                      <a href="?{self.recv_data.urlencode()}" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                      </a>
                    </li>
            '''
        page_html += next_page
        self.recv_data['page'] = self.total_page_count
        last_page = f'''
                      <li>
                        <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                          <span aria-hidden="true">尾页</span>
                        </a>
                      </li>'''
        page_html += last_page
        page_html += '''
                      </ul>
                     </nav>
            '''

        return mark_safe(page_html)

