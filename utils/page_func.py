from django.utils.safestring import mark_safe  #{{ page_html|safe }}

class Paging:

    def __init__(self,current_page_number,total_count,per_page_num=10,page_number_show=7,recv_data=None):
        """

        :param current_page_number: 当前页码
        :param total_count:         总数据量
        :param per_page_num_page:    每页显示多少条数据
        :param page_number_show:    总共显示多少个页码
        :total_page_count:          总的页码数
        :param star_page_number:    起始页码
        :param end_page_number:     结束页码
        """
        self.recv_data = recv_data   # <QueryDict: {'search_field': ['qq'], 'keyword': ['172']}>


        try:  # 防止恶意输入错误代码
            current_page_number = abs(int(current_page_number))
        except Exception:
            current_page_number = 1



        half_number = page_number_show // 2

        a, b = divmod(total_count, per_page_num)  # 商和余数
        if b:  # 如果余数不为0，页码总数为商加一
            total_page_count = a + 1
        else:
            total_page_count = a

        # 如果当前页码小于等于0时，默认显示第一页
        if current_page_number <= 0:
            current_page_number = 1

        if current_page_number >= total_page_count:
            current_page_number = total_page_count

        star_page_number = current_page_number - half_number   # 起始页码
        end_page_number = current_page_number + half_number + 1  # range故首不顾尾

        if star_page_number < 1:
            star_page_number = 1
            end_page_number = page_number_show + 1

        if end_page_number >= total_page_count:
            star_page_number = total_page_count - page_number_show + 1
            end_page_number = total_page_count + 1

        # 如果总页数小于需要展示的页数
        if total_page_count < page_number_show:
            star_page_number = 1
            end_page_number = total_page_count + 1
        self.current_page_number = current_page_number
        self.per_page_num = per_page_num
        self.total_page_count = total_page_count
        self.star_page_number = star_page_number
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
        page_html = ''
        for i in range(self.star_page_number,self.end_page_number):
            self.recv_data['page'] = i
            # <QueryDict: {'search_field': ['qq'], 'keyword': ['172'],'page':['2']}>
            if i == self.current_page_number:  # 为当前页添加颜色

                page_html += f'<li class="active"><a href="?page={i} " > {i} </a></li>'
            else:
                # page_html += f"<li><a href = '?page={i}&{self.recv_data.urlencode().replace('page='+str(self.current_page_number)+'&','')  if 'page=' in self.recv_data.urlencode() else self.recv_data.urlencode() }' > {i} </a></li>"
                page_html += f"<li><a href = '?{self.recv_data.urlencode() }' > {i} </a></li>"

        # 前一页
        self.recv_data['page'] = self.current_page_number-1
        previous_page = f'''
                    <li>
                       <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                         <span aria-hidden="true">&laquo;</span>
                       </a>
                    </li>
                '''
        # 后一页
        self.recv_data['page'] = self.current_page_number+1
        next_page = f'''
                    <li>
                        <a href="?{self.recv_data.urlencode()}" aria-label="Next">
                         <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                '''
        # 第一页
        self.recv_data['page'] = 1
        first_page = f'''
                <li>
                   <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                     <span aria-hidden="true">首页</span>
                   </a>
                </li>
            '''
        #最后一页
        self.recv_data['page'] = self.total_page_count
        last_page = f'''
                <li>
                   <a href="?{self.recv_data.urlencode()}" aria-label="Previous">
                     <span aria-hidden="true">尾页</span>
                   </a>
                </li>
            '''

        page_html = f'''
            <nav aria-label="Page navigation">
                <ul class="pagination">
                    {first_page}
                    {previous_page}
                    {page_html}
                    {next_page}
                    {last_page}
                </ul>
            </nav>
            '''
        return mark_safe(page_html)

