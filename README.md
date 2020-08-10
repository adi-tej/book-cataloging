# book-cataloging

## Introduction
Book cataloging is a mobile application which help oppotunity shops to retrive book infomation, list books to e-bay, create catalog for books, maintain orders of book. This application will try to digitalize the oppotunity shops, enhance the efficiency of trading books, and make the opshop more digitial and highly efficient.

## Overview
There are altogether four services:
* retrive book information using barcode/OCR
* make autopricing and auto description for book
* list specific books to e-bay
* maintain the orders for books

## Tech Stack
Below graph is showing the whole tech tools used in this application.<br>
![image](https://github.com/CircEx/book-cataloging/blob/WeiSong/app/images/tech.jpg)

## The detailed tech process
![image](https://github.com/CircEx/book-cataloging/blob/WeiSong/app/images/detailed.jpg)

## Setup backend
* step1: install the dependency of Python<br>
```
pip3 install -r requirements.txt
```
* step2: run the application from project backend folder<br>
```
python3 setup_app.py run
```
* step3: setup the database config with another terminal window<br>
```
python3 init_data.py
```
