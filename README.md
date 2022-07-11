<h2> To run the project please write following commands </h2>

<p>Installing requirements</p>

```sh
pip install -r requirements.txt
```
```sh
cd src
```
```sh
export FLASK_APP=app
```
<p>Initializing db and running migrations</p>
 
```sh
flask db init
```
```sh
flask db migrate
```
```sh
flask db upgrade
```

<p>Parsing files</p>

```sh
flask parse
```

<p>Running project</p>

```sh
flask run
```
