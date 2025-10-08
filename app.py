# app.py
import os
import json
from flask import Flask, render_template, request, redirect, session, flash, send_from_directory
import mysql.connector
from mysql.connector import Error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import PyPDF2
import docx2txt
import pandas as pd
from werkzeug.security import check_password_hash


# ----------------- Config -----------------
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "super_secret_key")
MODEL_FILE = "placement_model.pkl"

# ----------------- MySQL Connection -----------------
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "placement_db")
DB_PORT = int(os.environ.get("DB_PORT", 3307))  # change to 3306 if needed

def connect_db():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        print("✅ Connected to MySQL successfully!")
        return conn
    except Error as err:
        print(f"❌ MySQL connection error: {err}")
        return None

db = connect_db()

# ----------------- Serve Uploaded Resumes -----------------
@app.route('/resumes/<filename>')
def serve_resume(filename):
    return send_from_directory('resumes', filename, as_attachment=False)

# ----------------- Helper Functions -----------------
def train_model():
    global db
    if not db:
        print("⚠️ No DB connection — can't train model.")
        return None

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM studentsss")
    data = cursor.fetchall()
    cursor.close()

    if not data:
        print("⚠️ No student data in DB to train model")
        return None

    df = pd.DataFrame(data)

   
# Convert 'placed' to numeric safely
    if 'placed' in df.columns:
        def parse_placed(val):
            val = str(val).strip()
            if val.lower() in ['no', '0']:
                return 0.0
            elif val.lower() in ['yes', '100']:
                return 100.0
            else:
                try:
                    return float(val.rstrip('%'))
                except:
                    return 0.0
        df['placed'] = df['placed'].apply(parse_placed)
    else:
        df['placed'] = 0.0



    # Convert categorical columns to numeric codes safely
    if 'academic_performance' in df.columns:
        df['academic_performance'] = df['academic_performance'].map({
        'Excellent': 3, 'Good': 2, 'Average': 1, 'Poor': 0
        }).fillna(0).astype(int)
    else:
        df['academic_performance'] = pd.Series([0]*len(df))

    if 'extra_curricular_activity' in df.columns:
        df['extra_curricular_activity'] = df['extra_curricular_activity'].map({
            'Yes': 1, 'No': 0
        }).fillna(0).astype(int)
    else:
        df['extra_curricular_activity'] = pd.Series([0]*len(df))

    if 'communication' in df.columns:
        df['communication'] = df['communication'].map({
            'Excellent': 3, 'Good': 2, 'Average': 1, 'Poor': 0
        }).fillna(0).astype(int)
    else:
        df['communication'] = pd.Series([0]*len(df))


    # ML features
    ml_features = [
        'cgpa', 'salary', 'ssc_percentage', 'hsc_percentage', 'prev_sem_result',
        'projects', 'internship', 'certifications',
        'academic_performance', 'extra_curricular_activity', 'communication'
    ]

    # Ensure numeric
    for col in ml_features:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            df[col] = 0

    # Drop rows with missing target
    df.dropna(subset=ml_features + ['placed'], inplace=True)

    if len(df) < 10:
        print("⚠️ Not enough data to train (need at least 10 rows).")
        return None

    X = df[ml_features]
    y = df['placed'].astype(float)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    try:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        print(f"🎯 Model R²: {r2_score(y_test, y_pred):.3f}, MAE: {mean_absolute_error(y_test, y_pred):.2f}")
          
           # Save the trained model
        joblib.dump(model, MODEL_FILE)
        return model
    except Exception as e:
        print(f"❌ Error while training model: {e}")
        return None

def extract_text_from_resume(resume_path):
    text = ""
    resume_path = str(resume_path)
    try:
        if resume_path.lower().endswith(".pdf"):
            with open(resume_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += (page.extract_text() or "") + " "
        elif resume_path.lower().endswith(".docx"):
            text = docx2txt.process(resume_path) or ""
    except Exception as e:
        print(f"⚠️ Error reading resume {resume_path}: {e}")
    return text.lower()

def analyze_resume(resume_text, job_role_skills):
    resume_text = (resume_text or "").lower()
    extracted_skills = [s for s in job_role_skills if s.lower() in resume_text]
    missing_skills = [s for s in job_role_skills if s not in extracted_skills]
    return extracted_skills, missing_skills

def recommend_companies(missing_skills):
    recommendations = []
    if "python" in missing_skills: recommendations.append("Company A (Python Developer Track)")
    if "machine learning" in missing_skills: recommendations.append("Company B (AI/ML Internships)")
    if "sql" in missing_skills: recommendations.append("Company C (Database Analyst)")
    if not recommendations: recommendations.append("✅ You are well-prepared for most roles!")
    return recommendations

def recommend_for_low_chances(prob, data, missing_skills):
    recs = []
    try:
        if prob < 50:
            if "python" in missing_skills: recs.append("🔹 Take Python courses (Coursera/Udemy)")
            if "machine learning" in missing_skills: recs.append("🔹 Learn Machine Learning with projects")
            if "sql" in missing_skills: recs.append("🔹 Learn SQL / Database Management")
            recs.append("🔹 Complete certifications: AI, Cloud, Data Analytics")
            if data.get('internship', 0) == 0: recs.append("🔹 Apply for internships to gain experience")
            if data.get('projects', 0) == 0: recs.append("🔹 Work on personal or college projects")
    except Exception as e:
        print(f"⚠️ recommend_for_low_chances error: {e}")
    return recs

# ----------------- Load ML Model -----------------
model = None
if os.path.exists(MODEL_FILE):
    try:
        model = joblib.load(MODEL_FILE)
        print("✅ Loaded model from disk.")
    except Exception as e:
        print(f"⚠️ Could not load model file: {e}")
        model = None

if model is None:
    model = train_model()

# ----------------- Routes -----------------
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/student-form')
def student_form():
    return render_template("student-form.html")

@app.route('/submit', methods=['POST'])
def submit():
    global db, model
    if not db:
        return "❌ MySQL connection not established."

    def get_form(name, default=""):
        value = request.form.get(name, default)
        if isinstance(value, str):
            return value.strip()
        return value

    try:
        data = {
            'name': get_form('name'),
            'skills': get_form('skills'),
            'cgpa': float(get_form('cgpa', 0) or 0),
            'salary': float(get_form('salary', 0) or 0),
            'ssc_percentage': float(get_form('ssc_percentage', 0) or 0),
            'hsc_percentage': float(get_form('hsc_percentage', 0) or 0),
            'prev_sem_result': float(get_form('prev_sem_result', 0) or 0),
            'academic_performance': get_form('academic_performance', ''),
            'extra_curricular_activity': get_form('extra_curricular_activity', ''),
            'communication': get_form('communication', ''),
            'projects': int(get_form('projects', 0) or 0),
            'internship': int(get_form('internship', 0) or 0),
            'certifications': int(get_form('certifications', 0) or 0),
            'date': get_form('date'),
            'company': get_form('company'),
            'branch': get_form('branch', 'CSE'),
            'year': int(get_form('year') or 2025)
        }
    except ValueError as e:
        return f"❌ Invalid form data: {e}"

    # Resume upload
    resume_file = request.files.get('resume')
    resume_filename = ""
    if resume_file and resume_file.filename:
        os.makedirs('resumes', exist_ok=True)
        safe_name = secure_filename(resume_file.filename)
        resume_filename = f"{secure_filename(data['name'] or 'user')}_{safe_name}"
        resume_path = os.path.join('resumes', resume_filename)
        resume_file.save(resume_path)
    data['resume'] = resume_filename

    # ML Prediction
    prob_percent = 0.0
    if model is not None:
        input_data = [[
            data['cgpa'], data['salary'], data['ssc_percentage'], data['hsc_percentage'], data['prev_sem_result'],
            data['projects'], data['internship'], data['certifications'],
            {'Excellent':3,'Good':2,'Average':1,'Poor':0}.get(data['academic_performance'],0),
            {'Yes':1,'No':0}.get(data['extra_curricular_activity'],0),
            {'Excellent':3,'Good':2,'Average':1,'Poor':0}.get(data['communication'],0)
        ]]
        try:
            pred = model.predict(input_data)[0]
            prob_percent = float(max(0, min(pred, 100)))  # clamp 0–100
        except Exception as e:
            print(f"⚠️ Prediction error: {e}")

    # --- Added Section: Placement Status ---
    if prob_percent >= 80:
        placement_status = "High Chance"
    elif prob_percent >= 50:
        placement_status = "Moderate Chance"
    else:
        placement_status = "Low Chance"

    # Resume Analysis
    extracted_skills, missing_skills = [], []
    if data['resume']:
        resume_text = extract_text_from_resume(os.path.join('resumes', data['resume']))
        job_role_skills = ["python", "machine learning", "sql", "communication", "teamwork"]
        extracted_skills, missing_skills = analyze_resume(resume_text, job_role_skills)

    low_prob_recs = recommend_for_low_chances(prob_percent, data, missing_skills)

    # Save to DB
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO studentsss 
            (college_name, name, skills, cgpa, salary, date, branch,
            projects, internship, certifications, academic_performance, extra_curricular_activity,
            communication, company, resume, placed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                "Arvind Gavali College", data['name'], data['skills'], data['cgpa'], data['salary'],
                data['date'], data['branch'],
                data['projects'], data['internship'], data['certifications'],
                data['academic_performance'], data['extra_curricular_activity'], data['communication'],
                data['company'], data['resume'], f"{prob_percent:.2f}%"
            )
        )
        db.commit()
        cursor.close()
    except Exception as e:
        print(f"❌ DB insert error: {e}")

    return render_template(
        "result.html",
        company=data['company'],
        ssc_percentage=data['ssc_percentage'],
        hsc_percentage=data['hsc_percentage'],
        prev_sem_result=data['prev_sem_result'],
        academic_performance=data['academic_performance'],
        extra_curricular_activity=data['extra_curricular_activity'],
        communication=data['communication'],
        extracted_skills=extracted_skills,
        missing_skills=missing_skills,
        prediction=prob_percent,
        placement_status=placement_status
    )


@app.route('/contact')
def contact():
    return render_template('contact.html')

#--------- Admin Routes -----------------
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if not db:
            flash("❌ Database connection not available.", "error")
            return redirect('/admin')

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
        admin = cursor.fetchone()
        cursor.close()

        if admin and check_password_hash(admin['password'], password):
            session['admin'] = True
            return redirect('/admin-dashboard')
        else:
            flash("❌ Invalid username or password", "error")
            return redirect('/admin')

    return render_template('admin.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin')
    if not db:
        return "❌ No DB connection."

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM studentsss")
    students = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame(students)
    if not df.empty:
        placement_year = df.groupby('year')['placed'].count().to_dict()
        placement_branch = df.groupby('branch')['placed'].count().to_dict()
    else:
        placement_year, placement_branch = {}, {}

    return render_template("admin-dashboard.html",
                           students=students,
                           placement_year=json.dumps(placement_year),
                           placement_branch=json.dumps(placement_branch))

    
@app.route('/company')
def company():
    return render_template('company.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/admin')

# ---------------- Run Flask -----------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
