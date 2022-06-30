项目结构

+ basic-protocol 为基础协议实现
+ improve-protocol 为升级版协议 可以抵御中间人
+ middle-attack 中间人攻击代码

环境配置

```bash
# 进入/root目录
cd /root

# 克隆此项目
git clone https://github.com/wuuconix/Diffle-Hellman.git

# 拉取配套docker镜像 wuuconix/debian-python3
docker pull wuuconix/debian-python3

# 开启middle 中间人攻击容器
docker run -itd --name middle -v /root/Diffle-Hellman:/root/Diffle-Hellman wuuconix/debian-python3

# 开启server 服务器容器
docker run -itd --name server -v /root/Diffle-Hellman:/root/Diffle-Hellman wuuconix/debian-python3

# 开启client 客户端容器
docker run -itd --name client -v /root/Diffle-Hellman:/root/Diffle-Hellman wuuconix/debian-python3
```

基础协议运行

```bash
# 终端1
    # 进入server容器
    docker exec -it server bash
    # 运行服务
    python3 /root/Diffle-Hellman/basic-protocol/server/server.py 0.0.0.0 23333

# 终端2
    # 进入client容器
    docker exec -it client bash
    # 运行客户端
    python3 /root/Diffle-Hellman/basic-protocol/server/server.py 172.17.0.3 23333
```

改进协议运行

```bash
# 终端1
    # 进入server容器
    docker exec -it server bash
    # 运行服务
    python3 /root/Diffle-Hellman/improve-protocol/server/server.py 0.0.0.0 23333

# 终端2
    # 进入client容器
    docker exec -it client bash
    # 运行客户端
    python3 /root/Diffle-Hellman/improve-protocol/server/server.py 172.17.0.3 23333
```

中间人攻击运行

```bash
# 终端1
    # 以特权身份进入middle容器
    docker exec -it --privileged middle bash
    # 设置iptables规则
    sh /root/Diffle-Hellman/middle-attack/iptables.sh
    # 运行arp欺骗脚本
    python3 /root/Diffle-Hellman/middle-attack/arp_spoof.py

# 终端2
    # 以特权身份进入middle容器
    docker exec -it --privileged middle bash
    # 运行中间人攻击脚本
    python3 /root/Diffle-Hellman/middle-attack/middle.py

# 终端3
    # 以特权身份进入server容器
    docker exec -it --privileged server bash
    # 运行服务
    python3 /root/Diffle-Hellman/basic-protocol/server/server.py 0.0.0.0 23333

# 终端4
    # 以特权身份进入client容器
    docker exec -it --privileged client bash
    # 运行客户端
    python3 /root/Diffle-Hellman/basic-protocol/client/client.py 172.17.0.3 23333
```

![image](https://tva2.sinaimg.cn/large/007YVyKcly1h3o05palq8j31hc0u0noc.jpg)

查看arp欺骗的结果

+ 正常情况

    172.17.0.3 即服务器的mac地址为 02:42:ac:11:00:03

    ![image](https://tvax2.sinaimg.cn/large/007YVyKcly1h3qqsl5b7uj30k602mwfh.jpg)

+ arp欺骗后

    服务器的mac地址被欺骗为了 02:42:ac:11:00:02

    ![image](https://tvax1.sinaimg.cn/large/007YVyKcly1h3qqszcz8lj30k202l75i.jpg)

+ 攻击结束后如何恢复arp表?

    `arp -d 172.17.0.3` 删除arp表中的记录即可