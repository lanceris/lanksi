sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install virtualenvwrapper
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source ~/.local/bin/virtualenvwrapper.sh
if ! grep -Fxq '# virtualenv' ~/.bashrc
then
    printf '\n%s\n%s\n%s' '# virtualenv' 'export WORKON_HOME=~/virtualenvs' 'source ~/.local/bin/virtualenvwrapper.sh' >> ~/.bashrc
fi

source ~/.bashrc

mkvirtualenv -p python3.6 lanksi
workon lanksi
pip install -r requirements.txt
cd lanksi
python manage.py migrate
x-terminal-emulator -x sh -e "bash -c 'cd ..;. ./second.sh'"
x-terminal-emulator -x sh -e "bash -c 'celery worker -l info -A lanksi --beat'"
