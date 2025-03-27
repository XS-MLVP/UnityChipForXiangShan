---
title: 环境配置
linkTitle: 环境配置
weight: 12
---

## WSL2+Ubuntu22.04+GTKWave（Windows用户推荐使用）

我们推荐 Windows10/11 用户通过 WSL2 进行开发，在此给出通过此方法进行环境配置的教程集锦，仅供参考。如环境安装过程中出现任何问题，欢迎在QQ群（群号：<b>976081653</b>）中提出，我们将尽力帮助解决。此页面将收集大家提出的所有环境配置相关问题并提供解决方案，欢迎随时向我们提问！

### 1、在 Windows 下安装 WSL2（Ubuntu22.04）

参考资源：

--- 微软官方教程：[如何使用 WSL 在 Windows 上安装 Linux](https://learn.microsoft.com/zh-cn/windows/wsl/install)

--- 其它资源：[安装WSL2和Ubuntu22.04版本](https://blog.csdn.net/HHHBan/article/details/126843786)

### 2、打开 WSL，换源

推荐使用清华源：[清华大学开源软件镜像站-Ubuntu软件仓库](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)

### 3、配置验证环境

请参照[开放验证平台学习资源-快速开始-搭建验证环境](https://open-verify.cc/mlvp/docs/quick-start/installer/)配置环境。

以下是示例方法：
```bash
# 基本工具包
cd ~ && sudo apt-get update
sudo apt-get install -y build-essential cmake git wget curl lcov autoconf flex bison libgoogle-perftools-dev gcc python3.11 python3.11-dev python3.11-distutils python3-pip python-is-python3
rm -rf /var/lib/apt/lists/*
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
# verilator
git clone https://github.com/verilator/verilator.git
cd verilator
git checkout v4.218 # 4.218为最低需求版本，可自行查看并选择新版本
autoconf && ./configure && make -j$(nproc) && make install
cd .. && rm -rf verilator
# verible
curl -sS https://github.com/chipsalliance/verible/releases/download/v0.0-3946-g851d3ff4/verible-v0.0-3946-g851d3ff4-linux-static-x86_64.tar.gz -o /tmp/
tar -zxvf /tmp/verible-v0.0-3946-g851d3ff4-linux-static-x86_64.tar.gz -C /tmp/
copy /tmp/verible-v0.0-3946-g851d3ff4/bin/verible-* /usr/local/bin/
sudo chmod +x /usr/local/bin/verible-*
rm /tmp/verible-*
# pcre2
curl -sS https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.45/pcre2-10.45.tar.gz -o /tmp/
tar -zxvf /tmp/pcre2-10.45.tar.gz -C /tmp/
cd /tmp/pcre2-10.45
./configure --prefix=/usr/local && make -j$(nproc) && make install
rm -rf /tmp/pcre2* && cd ~
# swig 
# 注意不要使用 apt install swig，将会下载不符合最低要求的版本 4.0.2
curl -sS http://prdownloads.sourceforge.net/swig/swig-4.3.0.tar.gz -o /tmp/
tar -zxvf /tmp/swig-4.3.0.tar.gz -C /tmp/
cd /tmp/swig-4.3.0
./configure --prefix=/usr/local && make -j$(nproc) && make install
rm -rf /tmp/swig* && cd ~
# 更新本地包
apt-get update && apt-get -y upgrade
# picker
git clone https://github.com/XS-MLVP/picker.git --depth=1
cd picker
make init && make && make install
cd .. && rm -rf picker
# UnityChipForXiangShan
git clone https://github.com/XS-MLVP/UnityChipForXiangShan.git
cd UnityChipForXiangShan
pip3 install --no-cache-dir -r requirements.txt
```

### 4、使用 GTKWave 查看波形文件

使用[重庆大学硬件综合设计实验文档-Windows原生GTKWave](https://co.ccslab.cn/tips/win-gtkwave/)给出的方法，可以通过在WSL中输入 `gtkwave.exe wave.fst` 打开在 Windows 下安装的 GTKWave。请注意，gtkwave在使用中需要进入 fst 文件所在文件夹，否则会出现无法
initialize 的情况。

```bash
gtkwave.exe /out/{test_name}.fst
```

### 5、使用 VSCode 插件 Live Server 查看验证报告

成功安装插件Live Server后，打开文件列表，定位到 `/out/report/2025*-itlb-doc-*/index.html` 右键并选择 `Open With Live Server`，之后在浏览器中打开提示的端口（默认为`//localhost:5500`）即可。

## docker一键部署方案（MAC用户可用）

我们提供了 MAC 可用的 docker 环境，已在 Docker Hub 发布，名称为 `unitychip-env`。安装 Docker Desktop 后在命令行使用以下命令即可获取并打开开发环境。需下载约 500MB 的镜像，展开后约占用 1GB 空间。

```bash
docker search unitychip-env
docker pull dingjunbi/unitychip-env && docker run unitychip-env
cd UnityChipForXiangShan && git pull
```

[Docker Hub使用文档](https://docs.docker.com/docker-hub/)

[Docker：docker 拉取镜像及查看pull下来的image在哪里](https://blog.csdn.net/sj349781478/article/details/105267887/)