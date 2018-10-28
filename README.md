# Flask-REST-api
Using flask to create a rest api for a TODO list
using commandline CURL instead of POSTMAN https://www.getpostman.com/ 

To create a db:
  cd to app folder open python3 shell and type
    from myApi import db
    db.create_all()

The following commands apply to both users and TODOs
on the terminal to start api
  python3 myApi.py
  on another terminal in the same folder write use:
  replace <user> with  todo for the same manipulations
  

To add user:
  curl -i -H http://127.0.0.1:5000/user/ "Content-Type: application/json" -X POST -d '{"username","password"}'

To get public id:
  curl -i http://127.0.0.1:5000/Users/

To delete user:
  curl -i -H http://127.0.0.1:5000/user/ "Content-Type: application/json" -X POST -d <user public id>

To update user:
  curl -i -H "Content-Type: application/json" -X PUT -d '{"admin":true}' 
  
