// 折叠样式,需要根据不同的系统做出修改
$('.treeview>a').click(function () {
    $(this).next().removeClass('show','menu-open')    // 移除当前标签的show、menu-open类值
        .parent().siblings('li').children('ul').removeClass('show')
});      // 点击父级标签（父级兄弟标签）时,menu-open会自动移除；所以只需要注意把兄弟标签下的ul里的show类值移除就行了
