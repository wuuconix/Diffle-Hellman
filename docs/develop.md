# 开发文档

## 协议设计

### DH密钥交换

![](https://s1.ax1x.com/2022/06/20/XvE15F.png)

1. 客户端向服务端发送hello

```json
{
    "status": 0,
    "body": {
        "msg": "hello"
    }
}
```

2. 服务端向客户端发送密钥


```json
{
    "status": 1,
    "body": {
        "A": "xxxx",
        "g": "xxxx",
        "p": "xxxx",
        "pk": "xxxx", //improve下新增，存放服务器的RSA公钥
        "sign": "xxxx" //improve下新增，存放利用CA对服务器公钥的签名
    }
}
```

3. 客户端向服务端发送密钥

```json
{
    "status": 2,
    "body": {
        "B": "xxxx" //improve修改语义 利用服务器的公钥把B进行加密
    }
}
```

4. 客户端和服务端信息加密传输

```json
{
    "status": 3,
    "body": {
        "msg": "xxxx"
    }
}
```
