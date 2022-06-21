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
        "pk": "xxxx", //improve下新增，存放 经过CA私钥加密后的服务器的公钥
    }
}
```

3. 客户端向服务端发送密钥

```json
{
    "status": 2,
    "body": {
        "B": "xxxx" //利用服务器的公钥把B进行加密
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
