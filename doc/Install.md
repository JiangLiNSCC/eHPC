# 1 SETUP PYTHON VIRTUAL ENV
## 1.0 install python3 

	 wget http://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
         tar xvf Python-3.4.3.tgz
cd Python-3.4.3
./configure --prefix=/HOME/nscc-gz_jiangli/virtualenv/localpython
make -j 12 
make install
## 1.2 install virtualenv 
/HOME/nscc-gz_jiangli/virtualenv/localpython/bin/pip3 install --timeout 3600 virtualenvwrapper
## 1.3 setup
export PATH=/HOME/nscc-gz_jiangli/virtualenv/localpython/bin:$PATH
export VIRTUALENVWRAPPER_PYTHON=/HOME/nscc-gz_jiangli/virtualenv/localpython/bin/python3.4
source /HOME/nscc-gz_jiangli/virtualenv/localpython/bin/virtualenvwrapper.sh
cd /HOME/nscc-gz_jiangli/virtualenv
mkvirtualenv -p /HOME/nscc-gz_jiangli/virtualenv/localpython/bin/python3.4 py34
which python
 python --version
python -c "print('hello')"

git clone  https://github.com/JiangLiNSCC/eHPC.git

pip install  --timeout 3600 -r eHPC/requirements.txt 



