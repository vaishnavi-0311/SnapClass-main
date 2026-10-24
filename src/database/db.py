from src.database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()


def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):

    # checks for unique username, returns false when username is already taken

    response = supabase.table("teachers").select("username").eq("username", username).execute()

    return len(response.data) >0 


def create_teacher(username, password, name):
    data = { "username": username,
             "password": hash_pass(password), 
             "name":name 
            }
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username,password):
    response = supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password,teacher['password']):
            return teacher
    return None

def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data

def create_student(new_name, face_embedding = None, voice_embedding=None):
    data = {'name': new_name,'face_embedding':face_embedding,"voice_embedding":voice_embedding}
    response = supabase.table('students').insert(data).execute()

    return response.data

def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code":subject_code, "name":name, "section": section, "teacher_id":teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data 


def get_teacher_subjects(teacher_id):
    response = (
        supabase.table('subjects').select("*, subjects_students(count),attendance_logos(timestamp)").eq("teacher_id",teacher_id).execute()
    )

    
    subjects = response.data

    for sub in subjects:

        # sub['total_students'] = sub.get("subjects_student", [{}])[0].get('count', 0) if sub.get('subjects_students') else 0
        # attendance = sub.get('attendance_logos', [])
        # unique_sessions = len(set(log['timestamp'] for log in attendance))
        # sub['total_classes'] = unique_sessions

         # Count students enrolled in the subject
        student_counts = sub.get("subjects_students", [])
        sub["total_students"] = (
            student_counts[0].get("count", 0)
            if student_counts else 0
        )

        # # Count unique attendance sessions
        attendance = sub.get("attendance_logos", [])
        unique_sessions = {
            log["timestamp"]
            for log in attendance
            if log.get("timestamp") is not None
        }
        sub["total_classes"] = len(unique_sessions)

    
        sub.pop('subjects_students', None)
        sub.pop('aattendance_logos', None)

    return subjects


def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id":subject_id}
    response = supabase.table('subjects_students').insert(data).execute()
    return response.data

def unenroll_student_to_subject(student_id, subject_id):
  
    response = supabase.table('subjects_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()

    return response.data


def get_student_subjects(student_id):
    response = supabase.table('subjects_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data

def get_student_attendance(student_id):
    response = supabase.table('attendance_logos').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def create_attendance(logs):
    response = supabase.table('attendance_logos').insert(logs).execute()
    return response.data


def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logos').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data



