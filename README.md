# CollabSphere---App-Dev-2-Project

### WSL 0:
Activate the Virtual Environment and install the necessary requirements.
```shell
cd Backend
```

```shell
python3 -m venv env
```

```shell
source env/bin/activate
```

```shell
pip3 install -r requirements.txt
```

### WSL 1:
Run the Redis server for caching and other async tasks.
```shell
redis-server
```


### WSL 2:
Run the backend flask application for API calls and other functionalities.
```shell
cd Backend
```

```shell
source env/bin/activate
```

```shell
python3 app.py
```


### WSL 3:
Initialize the celery worker for async tasks.
```shell
cd Backend
```
```shell
source env/bin/activate
```
```shell
python3 -m celery -A app.celery worker -l info
```

### WSL 4:
Initialize the celery beat for scheduled tasks.
```shell
cd Backend
```
```shell
source env/bin/activate
```
```shell
python3 -m celery -A app.celery beat -l info
```

### WSL 5:
Run Mailhog for showing the incoming email service.
```shell
~/go/bin/MailHog
```


### CMD 1: Run Frontend.
(Install Node JS for running Node Package Manager commands.)
Install or update the necessary frontend libraries.
```shell
npm install
```
Run the frontend application.
```shell
npm run dev
```



### Extra Commands:
MailHog Installation for Linux
```shell
sudo apt-get -y install golang-go
```
```shell
go install github.com/mailhog/MailHog@latest
```
