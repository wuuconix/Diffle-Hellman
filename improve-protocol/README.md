如何抵御中间人攻击？

+ 引入一个服务器和客户端都信任的一个实体CA
+ 服务器向客户端发送A的时候，顺便把A 用CA签名一下，得到sign，一起发过去。
+ 客户端收到A和sign后，向CA进行签名验证，如果验证通过说明肯定是服务器，如果验证失败则说明是中间人。


程序运行截图

![image](https://tvax3.sinaimg.cn/large/007YVyKcly1h3rln7b9evj31hc0u04qp.jpg)