---
title: 环境配置
linkTitle: 环境配置
weight: 12
---

## 推荐使用WSL2+Ubuntu22.04+GTKWave

我们推荐Windows10/11用户通过WSL2进行开发，在此给出通过此方法进行环境配置的教程集锦，仅供参考。如环境安装过程中出现任何问题，欢迎在QQ群（群号：<b>976081653</b>）中提出，我们将尽力帮助解决。此页面将收集大家提出的所有环境配置相关问题并提供解决方案，欢迎随时向我们提问！

## 1、在Windows下安装WSL2（Ubuntu22.04）

参考资源：

--- 微软官方教程：[如何使用 WSL 在 Windows 上安装 Linux](https://learn.microsoft.com/zh-cn/windows/wsl/install)

--- 其它资源：[安装WSL2和Ubuntu22.04版本](https://blog.csdn.net/HHHBan/article/details/126843786)

## 2、打开WSL，换源

推荐使用清华源：[清华大学开源软件镜像站-Ubuntu软件仓库](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)

## 3、配置验证环境

请参照[开放验证平台学习资源-快速开始-搭建验证环境](https://open-verify.cc/mlvp/docs/quick-start/installer/)配置picker环境。

## 4、使用 GTKWave

使用[重庆大学硬件综合设计实验文档-Windows原生GTKWave](https://co.ccslab.cn/tips/win-gtkwave/)给出的方法，可以通过在WSL中输入 `gtkwave.exe wave.fst` 打开在Windows下安装的GTKWave。请注意，gtkwave在使用中需要进入fst文件所在文件夹，否则会出现无法
initialize的情况。

```bash
cd out
gtkwave.exe {test_name}.fst
cd ..
```

## 5、使用VSCode插件Live Server查看验证报告

成功安装插件Live Server后，打开文件列表，定位到 `/out/report/2025*-itlb-doc-*/index.html` 右键并选择 `Open With Live Server`，之后在浏览器中打开提示的端口（默认为`//localhost:5500`）即可。
