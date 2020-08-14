Notebefore deploying system:

1. If you want to view more details about our source code, you can follow
session 1 (**System Requirements**) and session 2 (**Deploying system package**) to 
deploy our system package on local.

2. We have published our app on Expo. If you are using **Android phone**, 
you can directly view our app without any setup. 
Please skip session 1 and 2,to access our production app at session3 
(**Production Details**).

1 System Requirements
===================

To setup and deploy on local environment please make sure the following
have been installed in your system.

Operating System: Windows 7+, Linux

-   Python 3+ <https://www.python.org/downloads/>

-   MySQL <https://dev.mysql.com/downloads/installer/>

-   Node JS <https://nodejs.org/en/download/>

-   Java JDK7 <https://www.oracle.com/au/java/technologies/javase/javase-jdk8-downloads.html>

2 Deploying system package
========================

2.1 Get app package from GitHub with Https
--------------------------------------
```shell script
git clone https:*//github.com/CircEx/book-cataloging.git*
```
If you do not have access to Github, please download our package in Teams group 2.

2.2 Setup and Deployment backend
----------------------------

-   **Step1: Config local database**

If you are going to setup the application on your own localhost, you need to setup your own local MySQL database and replace the **username, password and local database** in the **[app/main/config.py]** with username, password and schema name of your local database:
```python
local_db = "mysql+pymysql://username:password@127.0.0.1/local-database"
```
-   **Step2: Install the Python dependencies**
```shell script
 sudo pip3 install -r requirements.txt
```
-   **Step3: Setup running environment**

We provide three running environments: **development, test,** and **production,** the default environment is **production**.
If you want to try another environment, you can modify it in the **[setup_app.py]**:
```python
app = create_app('development')
```
-   **Step4: Setup database**

Please run the following commend under the project root folder -- **book-cataloging**:

To create all the tables in the database
```shell script
python3 set_up.py create_all
```
To delete all the tables in the database
```shell script
python3 set_up.py drop_all
```
-   **Step5: Run the application under the project root folder -- book-cataloging**
```shell script
python3 set_up.py run
```
-   **Step6: Initialize database under the project root folder -- book-cataloging**

Run the following command to add initial data to database along with some testing data.
```shell script
python3 init_data.py
```
2.3 Setup and Deployment Frontend 
-----------------------------

-   **Step 1: Install Expo CLI and React Native CLI**
```shell script
npm i -g expo-cli
npm i -g react-native-cli
```
-   **Step 2: Install Node Modules under book-cataloging/client
    directory**
```shell script
cd client
npm install
```
-   **Step 3: Prepare your emulator or device**

**a. Test with your own device (recommended)**

If you want to test the app in your **own device**, install "Expo client" application in your iOS or android mobile phone.

We recommend you use your own device for testing the app, because it is easier to take images using the camera of your device.

 **b. Test with an Android emulator**

Install Android Studio 4 and set platform tools of Android SDK to environment variable.
Setup SDK in Android studio to API.

Create an Android Virtual Device (AVD) you want to use and start it.

-   **Step 4: Configure axios file**

To connect front-end and backend, you need to provide backend server domain details in the 'baseUrl' of axios file. If you are running
backend server on your local machine set your **IP address** in the
'baseURL' in the file **[client/config/axios.js]**.
```javascript
let api = axios.create({
    baseURL: 'http://your_ip_address_here:5000',
    timeout: 10000
});
```

-   **Step 5: Run the front-end server**

```shell script
expo start
```

-   **Step 6: View the app in your device or AVD**

Now you would get a popup to your browser as below. To avoid developer logs, please **enable the
production mode**.

 6.1 Using your own **iOS device** to test the app.

 Please scan the QR code in the page using your phone camera. And then
 you will be redirected to Expo client.

 Note: Your device and local machine should under same Wi-Fi.

 6.2 Using an **Android emulator**
 
 Please click "Run on Android device/emulator" and view the app on AVD.

3 Production Details (Only for Android)
=====================================

You can try our production environment available as follows:

Backend server has been configured for production with AWS RDS database
and deployed on AWS EC2 instance.

Swagger API Documentation
-------------------------

'swagger.json' file can be found in the source code at the location
**[app/swagger.json]**.

You can also access the published swagger docs at

<http://ec2-3-25-170-12.ap-southeast-2.compute.amazonaws.com:5000/>

App
---

To use our published 'circex' app, please

1.  download the Expo Client <https://expo.io/tools#client>

2.  scan the app QR using your camera from 
    <https://expo.io/@medical_coder/circex>

4 Instructions for using the app
==============================

Please read detail instructions in session4 of 
**"Setup Deployment and Usage Manual"** file.