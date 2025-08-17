from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import os

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with attendance records
    attendance_records = db.relationship('Attendance', backref='student', lazy=True)
    
    def __repr__(self):
        return f'<Student {self.name}>'

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(20), nullable=False)  # 'Present', 'Absent', 'Late'
    time_in = db.Column(db.Time)
    time_out = db.Column(db.Time)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Attendance {self.student.name} - {self.date} - {self.status}>'

# Routes
@app.route('/')
def index():
    """Home page showing dashboard"""
    total_students = Student.query.count()
    today = date.today()
    today_attendance = Attendance.query.filter_by(date=today).count()
    present_today = Attendance.query.filter_by(date=today, status='Present').count()
    
    return render_template('index.html', 
                         total_students=total_students,
                         today_attendance=today_attendance,
                         present_today=present_today,
                         today=today)

@app.route('/students')
def students():
    """View all students"""
    all_students = Student.query.all()
    return render_template('students.html', students=all_students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    """Add new student"""
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        email = request.form['email']
        
        # Check if student already exists
        if Student.query.filter_by(roll_number=roll_number).first():
            flash('Student with this roll number already exists!', 'error')
            return render_template('add_student.html')
        
        if Student.query.filter_by(email=email).first():
            flash('Student with this email already exists!', 'error')
            return render_template('add_student.html')
        
        # Create new student
        new_student = Student(name=name, roll_number=roll_number, email=email)
        db.session.add(new_student)
        db.session.commit()
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('students'))
    
    return render_template('add_student.html')

@app.route('/attendance')
def attendance():
    """View attendance records"""
    page = request.args.get('page', 1, type=int)
    selected_date = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    
    # Convert string date to date object
    try:
        filter_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except:
        filter_date = date.today()
    
    attendance_records = Attendance.query.filter_by(date=filter_date)\
                                        .order_by(Attendance.created_at.desc())\
                                        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('attendance.html', 
                         attendance_records=attendance_records,
                         selected_date=selected_date)

@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    """Mark attendance for students"""
    if request.method == 'POST':
        student_id = request.form['student_id']
        status = request.form['status']
        notes = request.form.get('notes', '')
        attendance_date = request.form.get('date', date.today().strftime('%Y-%m-%d'))
        
        # Convert string date to date object
        try:
            attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
        except:
            attendance_date = date.today()
        
        # Check if attendance already marked for this student today
        existing_attendance = Attendance.query.filter_by(
            student_id=student_id, 
            date=attendance_date
        ).first()
        
        if existing_attendance:
            flash('Attendance already marked for this student on this date!', 'error')
        else:
            # Create new attendance record
            new_attendance = Attendance(
                student_id=student_id,
                status=status,
                date=attendance_date,
                notes=notes
            )
            
            if status == 'Present':
                new_attendance.time_in = datetime.now().time()
            
            db.session.add(new_attendance)
            db.session.commit()
            
            flash('Attendance marked successfully!', 'success')
        
        return redirect(url_for('mark_attendance'))
    
    # GET request - show form
    students = Student.query.all()
    today = date.today().strftime('%Y-%m-%d')
    return render_template('mark_attendance.html', students=students, today=today)

@app.route('/reports')
def reports():
    """View attendance reports"""
    # Get attendance summary for each student
    students = Student.query.all()
    report_data = []
    
    for student in students:
        total_days = Attendance.query.filter_by(student_id=student.id).count()
        present_days = Attendance.query.filter_by(student_id=student.id, status='Present').count()
        absent_days = Attendance.query.filter_by(student_id=student.id, status='Absent').count()
        late_days = Attendance.query.filter_by(student_id=student.id, status='Late').count()
        
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        report_data.append({
            'student': student,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'late_days': late_days,
            'attendance_percentage': round(attendance_percentage, 2)
        })
    
    return render_template('reports.html', report_data=report_data)

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    """Delete a student and their attendance records"""
    student = Student.query.get_or_404(student_id)
    
    # Delete all attendance records for this student
    Attendance.query.filter_by(student_id=student_id).delete()
    
    # Delete the student
    db.session.delete(student)
    db.session.commit()
    
    flash('Student and their attendance records deleted successfully!', 'success')
    return redirect(url_for('students'))

@app.route('/api/attendance_data')
def attendance_data():
    """API endpoint for attendance chart data"""
    # Get last 7 days attendance data
    attendance_data = []
    for i in range(7):
        check_date = date.today() - timedelta(days=i)
        present_count = Attendance.query.filter_by(date=check_date, status='Present').count()
        absent_count = Attendance.query.filter_by(date=check_date, status='Absent').count()
        
        attendance_data.append({
            'date': check_date.strftime('%Y-%m-%d'),
            'present': present_count,
            'absent': absent_count
        })
    
    return jsonify(attendance_data)

def create_tables():
    """Create database tables and add sample data"""
    db.create_all()
    
    # Add sample data if no students exist
    if Student.query.count() == 0:
        sample_students = [
            Student(name='John Doe', roll_number='001', email='john@example.com'),
            Student(name='Jane Smith', roll_number='002', email='jane@example.com'),
            Student(name='Bob Johnson', roll_number='003', email='bob@example.com'),
        ]
        
        for student in sample_students:
            db.session.add(student)
        
        db.session.commit()
        print("Sample students added to database!")

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        create_tables()
    
    print("Starting Attendance Management System...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True)