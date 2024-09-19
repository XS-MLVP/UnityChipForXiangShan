# Documents of DUTs

## Build

### Basic Environment Setup

1. Install [Node.js](https://nodejs.org/en/) (version 10.15.3 or above)
   ```bash
   curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. Install [Hugo](https://gohugo.io/getting-started/installing/) (version 0.110.0 or above)
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

### View Documents

In the documents dir, execlute the flow command:

```bash
hugo server
```

Then u