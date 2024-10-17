# CollabSphere---App-Dev-2-Project

WSL 0:
cd Backend

python3 -m venv env

source env/bin/activate

pip3 install -r requirements.txt

WSL 1:
redis-server


WSL 2:
cd Backend

source env/bin/activate

python3 app.py


WSL 3:
cd Backend

source env/bin/activate

python3 -m celery -A app.celery worker -l info


WSL 4:
cd Backend

source env/bin/activate

python3 -m celery -A app.celery beat -l info


WSL 5:
~/go/bin/MailHog




CMD 1:
npm install

npm run dev






Extra Commands:
MailHog Installation -
sudo apt-get -y install golang-go
go install github.com/mailhog/MailHog@latest
