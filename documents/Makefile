.PHONY: init release preview

# setup environment
init:
	curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -
	sudo apt-get install -y nodejs
	sudo pip3 install hugo==0.124.1
	sudo add-apt-repository ppa:longsleep/golang-backports
	sudo apt update
	sudo apt install golang-go
	npm install -D autoprefixer
	npm install -D postcss-cli
	npm install -D postcss

# build
release:
	hugo --minify --baseURL $(url)

# load server and preview
preview:
	hugo server -p 8080
