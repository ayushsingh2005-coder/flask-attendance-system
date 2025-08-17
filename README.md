# flask-attendance-system

# Attendance Management System

A simple web-based attendance management system built with Flask and SQLite.  
This README documents all files in the project, their purpose, and usage.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [File Documentation](#file-documentation)
  - [requirements.txt](#requirementstxt)
  - [app.py](#apppy)
  - [templates/base.html](#templatesbasehtml)
  - [templates/index.html](#templatesindexhtml)
  - [templates/students.html](#templatesstudentshtml)
  - [templates/add_student.html](#templatesadd_studenthtml)
  - [templates/attendance.html](#templatesattendancehtml)
  - [templates/mark_attendance.html](#templatesmark_attendancehtml)
  - [templates/reports.html](#templatesreportshtml)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Notes](#notes)

---

## Project Structure

```
Attendance/
├── app.py
├── requirements.txt
├── attendance.db
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── students.html
│   ├── add_student.html
│   ├── attendance.html
│   ├── mark_attendance.html
│   └── reports.html
```

---

## Installation

1. **Clone the repository**  
   Download or clone the project to your local machine.

2. **Install dependencies**  
   Run the following command in your terminal:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**  
   ```
   python app.py
   ```
   The app will start at [http://localhost:5000](http://localhost:5000).

---

## Usage

- **Dashboard:** Overview of students and today's attendance.
- **Students:** Add, view, and delete students.
- **Mark Attendance:** Mark attendance for students.
- **Attendance Records:** View attendance records by date.
- **Reports:** View attendance summaries and export data.

---

## File Documentation

### requirements.txt

Lists Python dependencies:
- `Flask`: Web framework.
- `Flask-SQLAlchemy`: ORM for database.
- `Werkzeug`: Utility library (used by Flask).

---

### app.py

Main Flask application file.

**Key Features:**
- Initializes Flask and SQLAlchemy.
- Defines two models: `Student` and `Attendance`.
- Implements routes for:
  - Dashboard (`/`)
  - Students list (`/students`)
  - Add student (`/add_student`)
  - Attendance records (`/attendance`)
  - Mark attendance (`/mark_attendance`)
  - Reports (`/reports`)
  - Delete student (`/delete_student/<student_id>`)
  - Attendance data API (`/api/attendance_data`)
- On first run, creates tables and adds sample students if none exist.

**How to use:**
- Run `python app.py` to start the server.
- All routes are accessible via the browser.

---

### templates/base.html

Base template for all pages.

**Features:**
- Loads Bootstrap and FontAwesome.
- Navigation bar with links to all main pages.
- Flash message display for success/error notifications.
- Content block for child templates.
- Includes Bootstrap and Chart.js scripts.
- Auto-hides flash messages after 5 seconds.

---

### templates/index.html

Dashboard page.

**Features:**
- Shows statistics: total students, present today, total marked today.
- Quick action buttons for adding students, marking attendance, viewing records, and reports.
- Today's overview: shows attendance status and system status.

---

### templates/students.html

Students management page.

**Features:**
- Lists all students in a table.
- Shows student details: ID, name, roll number, email, joined date.
- Actions: Mark attendance, delete student (with confirmation modal).
- Uses Bootstrap modal for delete confirmation.
- Handles date formatting for joined date.
- If no students, prompts to add the first student.

---

### templates/add_student.html

Add new student page.

**Features:**
- Form to add a new student (name, roll number, email).
- Client-side validation for required fields and email format.
- Guidelines card for user help.
- Back button to students list.

---

### templates/attendance.html

Attendance records page.

**Features:**
- Filter attendance records by date.
- Paginated table of attendance records.
- Shows student, roll number, date, status, time in, notes, marked at.
- Summary card for the selected date (total, present, absent, late).
- Pagination controls.
- If no records, prompts to mark attendance.

---

### templates/mark_attendance.html

Mark attendance page.

**Features:**
- Form to mark attendance for a student (select student, date, status, notes).
- Client-side validation for required fields.
- Quick mark section: button to mark all students present (requires backend implementation).
- Notes field updates placeholder based on status selection.

---

### templates/reports.html

Attendance reports page.

**Features:**
- Table summarizing attendance for each student (total days, present, absent, late, percentage, status).
- Export options: CSV export, print report.
- Attendance distribution pie chart and student performance bar chart (Chart.js).
- If no data, prompts to add students or mark attendance.

---

## Database Models

### Student

- `id`: Integer, primary key.
- `name`: String, student's full name.
- `roll_number`: String, unique roll number.
- `email`: String, unique email address.
- `created_at`: DateTime, when student was added.
- `attendance_records`: Relationship to Attendance.

### Attendance

- `id`: Integer, primary key.
- `student_id`: Foreign key to Student.
- `date`: Date, attendance date.
- `status`: String, 'Present', 'Absent', or 'Late'.
- `time_in`: Time, when student arrived (if present).
- `time_out`: Time, when student left (optional).
- `notes`: Text, additional notes.
- `created_at`: DateTime, when record was created.

---

## API Endpoints

- `/api/attendance_data`:  
  Returns JSON data for last 7 days' attendance (used for charts).

---

## Notes

- **Quick Mark All Present:** The button in `mark_attendance.html` is a placeholder. Backend logic needs to be implemented for bulk marking.
- **CSV Export:** In `reports.html`, you can export attendance summary as CSV.
- **Charts:** Attendance distribution and performance charts use Chart.js.
- **Bootstrap Modals:** Used for delete confirmation in students list.
- **Flash Messages:** Displayed for success/error actions.

---

## License

# Attendance Management System

A simple web-based attendance management system built with Flask and SQLite.

## Technologies Used

| Component       | Technology         |
|-----------------|--------------------|
| Web Framework   | Flask              |
| ORM             | Flask-SQLAlchemy   |
| Database        | SQLite             |
| Templating      | Jinja2             |
| UI Styling      | Bootstrap, Chart.js |
| Utilities       | Werkzeug, Click    |

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [File Documentation](#file-documentation)
- ... (and so on)


This project is for educational/demo purposes.

