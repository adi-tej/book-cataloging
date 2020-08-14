System Requirements
===================

To setup and deploy on local environment please make sure the following
have been installed in your system.

Operating System: Windows 7+, Linux

-   Python 3+ <https://www.python.org/downloads/>

-   MySQL <https://dev.mysql.com/downloads/installer/>

-   Node JS <https://nodejs.org/en/download/>

-   Java JDK7 <https://www.oracle.com/au/java/technologies/javase/javase-jdk8-downloads.html>

Deploying system package
========================

 Get app package from GitHub with Https
--------------------------------------
```
git clone https:*//github.com/CircEx/book-cataloging.git*
```
If you do not have access to Github, please download our package in Teams group 2.

Setup and Deployment backend
----------------------------

-   **Step1: Config local database**

If you are going to setup the application on your own localhost, you need to setup your own local MySQL database and replace the **username, password and local database** in the **[app/main/config.py]** with username, password and schema name of your local database:
```
local_db = "mysql+pymysql://username:password\@127.0.0.1/local-database\
```
-   **Step2: Install the Python dependencies**
```
 sudo pip3 install -r requirements.txt
```
-   **Step3: Setup running environment**

We provide three running environments: **development, test,** and **production,** the default environment is **production**.
If you want to try another environment, you can modify it in the **[setup_app.py]**:
```
app = create_app(\'development\')
```
-   **Step4: Setup database**

Please run the following commend under the project root folder --
> **book-cataloging**:

To create all the tables in the database
```
python3 set_up.py create_all
```
To delete all the tables in the database
```
python3 set_up.py drop_all
```
-   **Step5: Run the application under the project root folder -- book-cataloging**
```
python3 set_up.py run
```
-   **Step6: Initialize database under the project root folder -- book-cataloging**

Run the following command to add initial data to database along with some testing data.
```
python3 init_data.py
```
Setup and Deployment Frontend 
-----------------------------

-   **Step 1: Install Expo CLI and React Native CLI**
```
npm i -g expo-cli
npm i -g react-native-cli
```
-   **Step 2: Install Node Modules under book-cataloging/client
    directory**
```
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

https://github.com/CircEx/book-cataloging/blob/master/images/WhatsApp%20Image%202020-07-25%20at%2023.51.52.jpeg
Create an Android Virtual Device (AVD) you
want to use and start it.

-   **Step 4: Configure axios file**

> To connect front-end and backend, you need to provide backend server
> domain details in the 'baseUrl' of axios file. If you are running
> backend server on your local machine set your **IP address** in the
> 'baseURL' in the file **[client/config/axios.js]{.ul}**.
>
> **let** api = axios.create({
>
> baseURL: \'http://your_ip_address_here:5000\',
>
> timeout: 10000
>
> });

-   **Step 5: Run the front-end server**

> expo start

-   **Step 6: View the app in your device or AVD**

> Now you would get a popup to your browser as below.
>
> ![](media/image5.png){width="4.815972222222222in"
> height="3.53125in"}To avoid developer logs, please **enable the
> production mode**.
>
> 6.1 Using your own **iOS device** to test the app.
>
> Please scan the QR code in the page using your phone camera. And then
> you will be redirected to Expo client.
>
> Note: Your device and local machine should under same Wi-Fi.
>
> 6.2 Using an **Android emulator**
>
> Please click "Run on Android device/emulator" and view the app on AVD.

Production Details (Only for Android)
=====================================

You can try our production environment available as follows:

Backend server has been configured for production with AWS RDS database
and deployed on

AWS EC2 instance.

Swagger API Documentation
-------------------------

'swagger.json' file can be found in the source code at the location
**[app/swagger.json]{.ul}**.

You can also access the published swagger docs at

<http://ec2-3-25-170-12.ap-southeast-2.compute.amazonaws.com:5000/>

App
---

To use our published 'circex' app, please

1.  download the Expo Client <https://expo.io/tools#client>

2.  scan the app QR using your camera from here
    > <https://expo.io/@medical_coder/circex>

Instructions for using the app
==============================

We show 6 key paths for users to use this book cataloguing app.

3.  

    1.  Login CircEx Book Cataloguing app
        ---------------------------------

This app does not provide "Create account" functionality, you can only
login the app with an

invitation link from Admin process.

You can use the following credentials:

> Username: [[admin\@circex.com]{.ul}](mailto:admin@circex.com)
>
> Password: 123456

The app takes you to the Dashboard after successful login.

3.  

4.  1.  

    2.  List items on eBay
        ------------------

    ```{=html}
    <!-- -->
    ```
    1.  **Enter "book cataloging" page**

> ![](media/image6.png){width="2.2368055555555557in"
> height="1.1083333333333334in"}Click on "+" button at top-right corner
> to enter Camera Tabs (Image 1). There are three main methods to
> complete a listing: Barcode scanning, manually enter ISBN and manually
> enter in all book detail (Image 2).

Image 1: "Plus button"

a.  **Barcode scanning**

> If there is a barcode on the book, please use Barcode Scanner. Click
> on the 'Barcode' tab and allow access to the camera of the phone.
> Locate the barcode with the camera and you can get book details
> automatically.

b.  **Manually enter ISBN number**

> For situations in which the barcode scanner fails, you can click on
> 'Manual' tab and manually enter the ISBN. Only 10-digits or 13-digits
> is a verified ISBN. By clicking "Search", you can get the book details
> automatically for a valid ISBN.

c.  **Manually enter book details**

> ![](media/image7.jpeg){width="5.420138888888889in"
> height="2.696527777777778in"}If there is no ISBN number on this book,
> you can click on "No ISBN" button on the manual tab to navigate to
> "Book cataloging" page.

Image 2: Camera Tabs (left) Barcode Scanner, (mid) Manually enter ISBN,
(right) No ISBN

2.  **Update the book information and list it on eBay**

> You can enter the book price, select the condition, or add more
> description about the book and update other book details in "List a
> book" page. Book title, price, condition, and cover image are
> required.
>
> Additionally, you can click the white plus button to add images and
> red cross button to remove them (Image 3). There is a limit of 10
> images for one item.

![](media/image13.png){width="2.658333333333333in"
height="1.0946073928258968in"}

Image 3: Image Carousel

You can click "List on eBay" to list this book on eBay (Image 4).

![](media/image14.png){width="1.6567016622922135in" height="2.875in"}

Image 4: List on eBay

Editing/Removing existing book items
------------------------------------

> Once login, at the home page you are greeted on the Active Listing tab
> (Image 5). It shows a list of items that are currently listed out on
> eBay store in the order of recent updated.
>
> You can click onto an item card, you can see the selected item in
> detail (i.e. Title, name, ISBN), and be able to update or remove it
> (Image 6).

![](media/image15.png){width="3.875in" height="2.990972222222222in"}

Image 5: Active Listing tab Image 6: Edit book page

Deal with in-store orders (Checkout)
------------------------------------

> If a customer purchases books in store, you can use "Checkout"
> functionality to remove books from eBay and mark books as "sold" in
> database.

1.  **Enter "Checkout" page**

> Click on "Checkout" button at the bottom-right corner to enter Camera
> Tabs (Image 7). There are three main methods of completing a checkout
> two of which which are the same as "Listing" functionality (Image 2):
> Barcode scanning, manually enter ISBN. You can select a suitable mode
> according to your case.
>
> Additionally, for a book without ISBN number, you can click "No ISBN"
> in "Manual" tab and then enter a book title to search the required
> book in the database (Image 8).

![](media/image19.png){width="4.176388888888889in"
height="3.0083333333333333in"}

Image 7 "Checkout button" Image 8 Enter a book title to checkout

2.  **Checkout the book**

> ![](media/image23.png){width="1.8152777777777778in"
> height="3.0722222222222224in"}After scanning or manually entering
> ISBN/title, a checkout page would pop up and show you some information
> of this book (Image 9).

Image 9 Checkout popup

> You can click "Checkout item" to remove this book from eBay. If you
> click "Close", you will navigate back to the Camera Tabs again.

Deal with online orders from eBay 
---------------------------------

> For orders made from eBay which are awaiting confirmation, cab be
> viewed on "Pending Orders" tab on the home page. You can select one of
> the order cards to view its details (Image 10).
>
> On each order, you can view all ordered book items and total price. To
> confirm this order, you can click on "Confirm Order" to finalize this
> purchase (Image 11).

Once you confirmed an order, this order would be moved to "Accepted
Orders" tab (Image 12).

![](media/image24.png){width="5.731944444444444in" height="2.925in"}

Image 10 Pending orders Image 11 Order details Image 12 Accepted orders

Search 
------

> ![](media/image30.png){width="2.0875in"
> height="1.4510673665791776in"}On the search icon, you can search an
> active listing book through ISBN or book title and then enter "edit
> book details" page to edit the item details on eBay (Image 13).

Image 13 Search an item

Work in Progress
================

The following are some of the work in progress features.

1.  **OCR Functionality**

> User can scan the book ISBN using OCR which will be added to Camera
> Tabs to serve the listing and checkout.

2.  **Verify and Confirm Order**

> The staff can verify the availability of the items in the store and in
> data base before confirming the order. However, the in-store checkout
> will be given priority over online order.
>
> Notifying the customer and shipping process after successful
> confirmation.

3.  **Cancel Order**

> Integration of cancel order process with eBay to notify the customer
> about the refund process.

4.  **Analytics and Feedback**

> Tracking the purchases and enabling staff to make use of analytics and
> customer feedback.
