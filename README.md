# ycjw_hacker
zjut原创教务管理系统学生账号获取

python版本3.6 用virtualenv搭环境

requests库需要单独安装 pip install requests

学生id与密码之间存在一定联系，生成两个字典，账号，密码，

简单密码自己生成好了，如果你觉得对方密码比较复杂那就去网上找个字典吧。

python模拟post请求发送给服务器

线程数目可以视情况决定，但是效率还是略低
其实就是用requests库给服务器发post表单，再从返回的response中分析是否成功
