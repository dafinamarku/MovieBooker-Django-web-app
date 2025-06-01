# 🎬 MovieBooker - Django Web Application

**MovieBooker** is a Django-based web application for managing movies, cinema rooms, screening schedules, and seat reservations by users.

## 🚀 Features
  
- ✅ Admin can create and edit movies and screening rooms  
- ✅ Automatic conflict detection between screenings  
- ✅ Display available rooms based on time and room schedules  
- ✅ Seat selection and booking system  
- ✅ User authentication and role-based access (Admin & Client)  
- ✅ Clean UI for both admin and client views  

## 🛠 Technologies Used

- Python 3.13.2  
- Django  
- SQLite  
- HTML, CSS, JavaScript  
- Bootstrap

## 📦 Local Setup

1. **Clone the repository**:
```bash
git clone https://github.com/dafinamarku/MovieBooker-Django-web-app.git
cd MovieBooker-Django-web-app
```

2. **Create and activate a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Apply migrations**:
```bash
python manage.py migrate
```

5. **Load initial demo data (optional)**:
```bash
python manage.py loaddata dumb_data/fixtures/initial_data.json
```

6. **Run the development server**:
```bash
python manage.py runserver
```


## 👥 User Roles

- **Admin** – Full access to movie, room, and screening management  
- **Client** – Can browse movies and book available seats  

## 🧪 Testing

To test the app:
- You can use users:
	- Admin: username -> admin	password->test123
	- Client: username -> dafina	password->test123

## 📃 License

This project is intended for educational and personal use. 

---

💡 **Author:** Dafina Marku  
🔗 [GitHub](https://github.com/dafinamarku)
