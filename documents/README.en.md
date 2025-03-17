# Documentation Deployment Instructions

English | [中文](/README.zh.md)

## Build

### Basic Environment Setup

1. Install [Node.js](https://nodejs.org/en/) (version 10.15.3 or above)

   ```bash
   curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. Install [Hugo](https://gohugo.io/getting-started/installing/) (version 0.124.1 or above)

   ```bash
   sudo pip3 install hugo
   ```

3. Install [Golang](https://golang.org/doc/install) (version 1.18.0 or above)

   ```bash
   sudo add-apt-repository ppa:longsleep/golang-backports
   sudo apt update
   sudo apt install golang-go
   ```

4. Install Dependencies

   ```bash
   npm install -D autoprefixer
   npm install -D postcss-cli
   npm install -D postcss
   ```

<!--
### View Documents

Execute the following commands in the `UnityChipForXiangShan/documents` folder: (please specify `port_num` yourself)

```bash
cd ~/UnityChipForXiangShan/documents
hugo server -p <port_num> -D # Example：hugo server -p 1313 -D
```

After the server is successfully started, access it through the browser:

```bash
http://localhost:<port_num>
```
-->
