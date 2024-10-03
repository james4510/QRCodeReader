# QRCodeReader
# Church Inventory Management System

This is a web-based inventory management system designed for churches to keep track of items by generating and scanning QR codes. It helps you manage church equipment and assets, including details like item ID, manager, department, borrow date, and the current status of the item (borrowed or returned).

## Features

- Add new items to the database with relevant details such as item name, manager, department, borrow date, and borrow status.
- Automatically generate a QR code for each item, which can be scanned to view item details.
- Responsive and user-friendly UI built with Bootstrap for ease of use.
- QR code generation with real-time URL pointing to the item details page.
- Item details page with comprehensive information such as manager, department, and borrow status.

## Requirements

Before you can run the project, make sure you have the following installed:

- Python 3.x
- Flask (`pip install Flask`)
- qrcode library for Python (`pip install qrcode[pil]`)
- Bootstrap (included via CDN)

## Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/james4510/church_inventory.git

2. **Install dependencies**:
   ```bash
   pip install Flask qrcode[pil]
3. **Run the application**:
     You can start the Flask server by running the following command:
   ```bash
   python church_inventory.py
   By default, the server will run on `http://0.0.0.0:5000`, and the app will be accessible on the local network.
4. **Access the application**:
   - Open your browser and navigate to `http://<server_ip>:5000/` (replace `<server_ip>` with your server's IP address.)
   - You can now add new items, generate QR codes, and view item details via QR code scanning.
  
## How to use
### Add a New Item
1. Navigate to the homepage.
2. Fill out the form with the item details
3. Submit the form to add the item and automatically generate a QR code.

## View Item Details via QR Code
1. After adding an item, a QR code will be generated.
2. You can scan the QR code with a mobile device to view the item's details.
3. The details page will show information like the item ID, manager, department, borrow date, and the current staus

## Project Structure
```php
church_inventory.py # Main Python file contaning the Flask app
static/ # Directory for storing QR code images
templates/ # HTML templates
```

## License
This project is licensed under the MIT License. See the LICENSE fill for more information.


### Additional Instructions:
- Replace the placeholder `<yourusername>` in the repository URL with your actual GitHub username.
- Take some screenshots of the different UI pages, such as the "Add Item" form, the generated QR code, and the "Item Details" page. Save them in a `screenshots/` folder for use in the README.
- Customize the `server_ip` variable inside the `create_qr_code()` function with your server’s actual IP address.

This README will provide potential users with clear instructions and an overview of your project, making it easy to understand and run.

   
