# ycjw_hacker
原创教务管理系统学生账号破解

python版本3.6 linux下可以用virtualenv搭环境

requests库需要单独安装 pip install requests 就ok
请勿尝试！！仅作为参考！！

学生id与密码之间存在一定联系，请知道的及时修改密码，生成两个字典，账号，密码，

简单密码自己生成好了，如果你觉得对方密码比较复杂那就去网上找个字典吧。

python模拟post请求发送给服务器，为了防止http请求失败，建议try catch包裹。

需要较长时间去获得正确的账号密码队，开启了协程，用了asyncic异步，但是速度仍然比较慢，

线程数目可以视情况决定，但是效率还是略低，（建议8左右服务器吃不消）


之后如果可以会写成分布式的（虽然不会）教师的账号其实也是可以获取的，但是有点危险建议不要尝试（操作类似）

最后，大佬给个star？？
