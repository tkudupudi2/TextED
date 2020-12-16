# TextED
An educational web application made to connect virtually with friends, peers, and professors during COVID-19.

## Application requirements
Have **Flask, Python3, SQLite**, and **Redis server** installed.

## Packages to Install
The following are the commands to install the necesssary packages. Even if you think you have them installed, run the command on terminal to make sure.
Flask Packages:
```
pip3 install Flask --user
pip3 install -U Flask-SQLAlchemy --user
pip3 install flask-bcrypt --user
pip3 install flask-login --user
pip3 install Flask-Mail --user
pip3 install redis --user
pip3 install Pillow --user
pip3 install Flask-WTF --user
pip3 install email_validator --user
```
If you don't have homebrew:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install wget
```
Redis Server:
```
brew install redis
```
To start redis
```
brew services start redis
```
To stop redis
```
brew services stop redis
```

## How to run
- Navigate to the project folder using the terminal.
- Run : python3 run.py
- Enter local ip address http://127.0.0.1:5000/ in your browser
- Welcome to the site

## Features: 
* [x] Register: Users are able to create an account.
* [x] Login: A login manager that keeps users authenticated.
* [x] Chat: Registered users can privately chat with other registered users.
* [x] Calendar: Registered users can setup/edit appointments and events.
* [x] Logout: A sign out button that allows users to logout.

## License

    Copyright [2020] [Tanav Kudupudi]

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
