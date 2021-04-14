# Internet
Checking internet from time to time and saving it in a database
## install
```
pip install -r requirements.txt
```
## run
```
python check.py
python api.py
```
## docker
```
docker build -t internet:testing .
docker run --rm -d -P -it internet:testing
```
## api

- Port exposed: ***5000*** *if no port defined in the environment*
- Route: **/speed**
- (local) host: **[127.0.0.1](http://127.0.0.1:5000/)**