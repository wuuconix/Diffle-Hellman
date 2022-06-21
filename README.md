# Diffle-Hellman

## 目前已实现的功能

+ 协议升级已经大致完成
    + 服务器端A照样发，但是同时会带上自己的RSA公钥和由CA颁布的对RSA公钥的签名
    + 客户端在用CA的公钥进行验证，验证不通过直接退出程序
    + 验证成功后用RSA公钥来加密传输B
        > 这时候客户端已经能够计算出K了
    + 服务端用自己的RSA私钥，解密出B，也能够得到K
    + 开始正常利用K来AES加密传输信息

![carbon (1)](https://tvax1.sinaimg.cn/large/007YVyKcly1h3gccgf87zj31kw2k2e81.jpg)

![carbon (2)](https://tva2.sinaimg.cn/large/007YVyKcly1h3gcgo0v9kj31kw2k2e81.jpg)
