# 文档部署说明

[English](/README.en.md) | 中文

## 构建指南

### 基础环境配置

1. 安装 [Node.js](https://nodejs.org/en/) (版本 10.15.3 或更高)

   ```bash
   curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. 安装 [Hugo](https://gohugo.io/getting-started/installing/) (版本 0.124.1 或更高)

   ```bash
   sudo pip3 install hugo
   ```

3. 安装 [Golang](https://golang.org/doc/install) (版本 1.18.0 或更高)

   ```bash
   sudo add-apt-repository ppa:longsleep/golang-backports
   sudo apt update
   sudo apt install golang-go
   ```

4. 安装依赖项

   ```bash
   npm install -D autoprefixer
   npm install -D postcss-cli
   npm install -D postcss
   ```

<!--
### 查看文档

在 `UnityChipForXiangShan/documents` 目录下执行以下命令（请自行指定 `port_num` 端口号）：

```bash
cd ~/UnityChipForXiangShan/documents
hugo server -p <port_num> -D # 示例：hugo server -p 1313 -D
```

服务成功启动后，可通过浏览器访问：

```bash
http://localhost:<port_num>
```
-->
