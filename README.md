

---

# 📊 Placement Prediction System

*A Machine Learning + Django based web application to predict student placement chances.*

---

## 🚀 Overview

The **Placement Prediction System** helps students and colleges predict whether a student is likely to get placed based on academic performance, skills, and other parameters.
It uses a **Machine Learning model** integrated with a **Django web application** and a clean UI built with **HTML, CSS**.

---

## ✨ Features

✔ Predicts placement probability using ML
✔ Django-based backend
✔ Clean and responsive UI (HTML + CSS)
✔ Stores and fetches data using MySQL
✔ User-friendly form input
✔ Real-time prediction results
✔ Separate pages for:
  • Home
  • Prediction form
  • Result page

---

## 🛠️ Tech Stack

**Frontend:**

* HTML
* CSS

**Backend:**

* Python
* Django Framework

**Database:**

* MySQL

**Machine Learning:**

* Scikit-Learn
* Pandas
* NumPy

---



### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/placement-prediction.git
cd placement-prediction
```

### 2️⃣ Create a virtual environment

```bash
python -m venv env
env\Scripts\activate   # On Windows
source env/bin/activate  # On Linux/Mac
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure MySQL

Create a database in MySQL:

```sql
CREATE DATABASE placement_db;
```

Update your Django `settings.py` with DB credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'placement_db',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5️⃣ Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Run the server

```bash
python manage.py runserver
```

---

## 🎯 How It Works

1. User fills out the student details form
2. Form data is sent to Django backend
3. Django loads the trained Machine Learning model
4. Model predicts the placement probability
5. Result is displayed to the user in an attractive UI

---

## 📌 Future Enhancements

🔹 Add more ML models to improve accuracy
🔹 Add admin dashboard
🔹 Add charts for visualization
🔹 Implement user authentication
🔹 Deploy on AWS / Render / Railway

---

## 🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss what you would like to change.

---



