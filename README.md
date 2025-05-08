
# 🛍️ ESPA MARKET

Welcome to **ESPA MARKET**, a modern, full-featured online store built with Django REST Framework and Tailwind CSS.

This project is part of a final assignment, designed to be completed in a few days and demonstrate strong frontend-backend integration, beautiful UI, and a professional e-commerce experience.

---

## 🚀 Features

- 🛒 Product catalog with categories, discounts, and active promotions  
- 🧺 Dynamic shopping cart with quantity and price updates  
- 💳 Checkout system with coupon codes and simulated payment  
- 📦 Order management with PDF invoice generation (xhtml2pdf)  
- 📧 Email notification after order confirmation with PDF attached  
- 📥 OTP authentication for secure login and registration  
- 📃 Blog and FAQ system (SEO-ready)  
- 📊 Admin dashboard (Django Admin) + Customer dashboard (API)  
- 🎨 Responsive and beautiful UI using Tailwind CSS  
- 🌐 JWT-based authentication with DRF

---

## 🧠 Tech Stack

| Layer       | Technology                        |
|-------------|------------------------------------|
| Backend     | Django 5.x, Django REST Framework  |
| Database    | PostgreSQL                         |
| Frontend    | HTML, JS (Vanilla), Tailwind CSS   |
| Auth        | JWT (djangorestframework-simplejwt) |
| Media       | Pillow (images), xhtml2pdf (PDF)   |
| Email       | Django Email Backend               |

---

## 📂 Project Structure

```
ESPA_MARKET/
├── espa_market/         # Main Django project
├── products/            # Product + Category + Discount models
├── cart/                # Cart and CartItem logic
├── orders/              # Orders, OrderItems, Coupons, PDF invoice
├── customers/           # Customer profiles
├── otp/                 # OTP authentication
├── frontend/            # HTML, JS, and static assets
│   ├── html/
│   ├── js/
│   └── components/
├── templates/
│   ├── frontend/        # UI templates (home, etc.)
│   ├── orders/          # invoice.html
│   └── emails/          # order_confirmation.html
└── README.md            # You’re reading it!
```

---

## ⚙️ Setup Instructions

1. 🔽 Clone the repository:

```bash
git clone https://github.com/esmaeel116/ESPA_Market.git
cd ESPA_Market
```

2. 🐍 Create virtual environment (using .venv):

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

3. 📦 Install dependencies:

```bash
pip install -r requirements.txt
```

4. 🧪 Setup PostgreSQL

Make sure you have PostgreSQL installed and a database created:

- DB Name: espa_market  
- User: espa_user  
- Password: espapass123

Update the DATABASES setting in settings.py accordingly.

5. ⚒️ Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. 🧑 Create superuser:

```bash
python manage.py createsuperuser
```

7. 🌍 Run the dev server:

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## 📝 API Endpoints

All API endpoints are prefixed with `/api/`. Authenticated routes require a JWT token.

- `/api/products/`  
- `/api/cart/`, `/api/cart-items/`  
- `/api/orders/`, `/api/checkout/`, `/api/orders/confirm-payment/`  
- `/api/orders/<id>/invoice/`  
- `/api/otp/register/`, `/api/otp/login/`  
- ...

📄 API documentation with examples may be added later using Swagger or ReDoc.

---

## 📬 Email & PDF

- A confirmation email with an attached PDF invoice is sent after a successful payment.  
- PDF invoices are generated using xhtml2pdf.

---

## 🧠 Notes for Instructor

- ✅ Follows best practices for code organization and modularity  
- ✅ Follows Conventional Commits style for all commits  
- ✅ Frontend and backend are fully integrated  
- ✅ Beautiful, user-friendly, and responsive UI  
- ✅ Project is fully functional and production-ready

---

## 🧑‍💻 Author

Made with ❤️ by [@esmaeel116](https://github.com/esmaeel116)

---

## 📜 License

This project is licensed for academic and educational use.
