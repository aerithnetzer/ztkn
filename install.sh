curl https://raw.githubusercontent.com/aerithnetzer/ztkn/refs/heads/main/install.sh

chmod +x install.sh

git clone https://github.com/aerithnetzer/ztkn/

mv ztkn /usr/local/bin/

ln -s /usr/local/bin/ztkn/src.py /usr/local/bin/ztkn

export PATH=$PATH:/usr/local/bin/ztkn

python /usr/local/bin/ztkn/setup.py
