from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from ..models.models import Enrollment, Payment, Certificate, Course, Instruct, User
from ..models import generate_id

class EnrollmentService:
    """Service for Enrollment CRUD operations"""
    
    def __init__(self, db_session: sessionmaker, max_retries=50):
        self.db_session = db_session
        self.max_retries = max_retries

    def create_enrollment(self, enrollment_data: Dict[str, Any]) -> Enrollment:
        """Create a new enrollment"""
        for attempt in range(self.max_retries):
            new_id = generate_id(self.db_session, Enrollment.EnrollmentID)
            enrollment_data["EnrollmentID"] = new_id
            with self.db_session() as session:
                try:
                    enrollment = Enrollment(**enrollment_data)
                    session.add(enrollment)
                    session.commit()
                    session.refresh(enrollment)
                    return enrollment
                except IntegrityError:
                    session.rollback()
                    print(f"Collision detected for {new_id}. Retrying...")
                    continue
                except Exception as e:
                    session.rollback()
                    raise e
        raise Exception(f"Failed to generate unique ID for {Enrollment.__name__} after {self.max_retries} attempts.")
    
    def get_enrollment_by_id(self, enrollment_id: str) -> Optional[Enrollment]:
        """Get enrollment by ID"""
        with self.db_session() as session:
            return session.query(Enrollment).filter(
                Enrollment.EnrollmentID == enrollment_id
            ).first()
    
    def get_enrollment(self, enrollment_id: str, course_id: str, 
                       payment_id: str, student_id: str) -> Optional[Enrollment]:
        """Get enrollment by composite primary key"""
        with self.db_session() as session:
            return session.query(Enrollment).filter(
                Enrollment.EnrollmentID == enrollment_id,
                Enrollment.CourseID == course_id,
                Enrollment.PaymentID == payment_id,
                Enrollment.StudentID == student_id
            ).first()
    
    # Not use too little detail
    def get_student_enrollments(self, student_id: str) -> List[Enrollment]:
        """Get all enrollments for a student"""
        with self.db_session() as session:
            return session.query(Enrollment).filter(
                Enrollment.StudentID == student_id
            ).all()
        
    def get_student_enrollments_with_details(self, student_id: str):
        """
        Fetches enrollments with Course Title, Instructor Name, and Progress.
        """
        # 1. Build the Query
        # We join Enrollment -> Course
        # Then Course -> Instruct -> User (to find the instructor)
        # We use distinct() because a course might have multiple instructors, avoiding duplicate rows
        with self.db_session() as session:
            results = (
                session.query(
                    Enrollment.EnrollmentID,
                    Enrollment.Status,
                    Enrollment.Enroll_date,
                    Course.CourseID,
                    Course.Title.label("course_title"),
                    User.Full_name.label("instructor_name")
                )
                .join(Course, Enrollment.CourseID == Course.CourseID)
                .outerjoin(Instruct, Course.CourseID == Instruct.CourseID) # Left join in case no instructor assigned
                .outerjoin(User, Instruct.UserID == User.UserID)
                .filter(Enrollment.StudentID == student_id)
                .distinct(Enrollment.EnrollmentID) # Ensure one row per enrollment
                .all()
            )

        # 2. Format the output to match what your React Frontend needs
        enrollments_data = []
        for row in results:
            # Optional: Fetch lessons/modules count for progress calculation if 'progress' isn't a column
            # This is a sub-query optimization you can add later.
            
            enrollments_data.append({
                "id": row.CourseID, # Frontend uses CourseID as key often
                "enrollment_id": row.EnrollmentID,
                "title": row.course_title,
                "instructor": row.instructor_name or "MUDemy Instructor",
                "status": row.Status,
                "progress": row.progress if hasattr(row, 'progress') else 0,
                "lessons": [] 
            })
        print("Enrollments Data:", enrollments_data)
        return enrollments_data
    
    def get_course_enrollments(self, course_id: str) -> List[Enrollment]:
        """Get all enrollments for a course"""
        with self.db_session() as session:
            return session.query(Enrollment).filter(
                Enrollment.CourseID == course_id
            ).all()
    
    def get_active_enrollments(self, student_id: str) -> List[Enrollment]:
        """Get all active enrollments for a student"""
        with self.db_session() as session:
            return session.query(Enrollment).filter(
                Enrollment.StudentID == student_id,
                Enrollment.Status == 'Active'
            ).all()
    
    def get_completed_enrollments(self, student_id: str) -> List[Enrollment]:
        """Get all completed enrollments for a student"""
        with self.db_session() as session:
            return session.query(Enrollment).filter(
                Enrollment.StudentID == student_id,
                Enrollment.Status == 'Completed'
            ).all()
    
    def is_student_enrolled(self, student_id: str, course_id: str) -> bool:
        """Check if a student is enrolled in a course"""
        with self.db_session() as session:
            enrollment = session.query(Enrollment).filter(
                Enrollment.StudentID == student_id,
                Enrollment.CourseID == course_id
            ).first()
            return enrollment is not None
    
    def update_enrollment_status(self, enrollment_id: str, status: str) -> Optional[Enrollment]:
        """Update enrollment status"""
        with self.db_session() as session:
            enrollment = session.query(Enrollment).filter(
                Enrollment.EnrollmentID == enrollment_id
            ).first()
            
            if not enrollment:
                return None
            
            valid_statuses = ['Active', 'Completed', 'Dropped', 'Suspended']
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            
            enrollment.Status = status
            session.commit()
            session.refresh(enrollment)
            return enrollment
    
    def update_enrollment(self, enrollment_id: str, update_data: Dict[str, Any]) -> Optional[Enrollment]:
        """Update enrollment information"""
        with self.db_session() as session:
            enrollment = session.query(Enrollment).filter(
                Enrollment.EnrollmentID == enrollment_id
            ).first()
            
            if not enrollment:
                return None
            
            for key, value in update_data.items():
                if hasattr(enrollment, key):
                    setattr(enrollment, key, value)
            
            session.commit()
            session.refresh(enrollment)
            return enrollment
    
    def delete_enrollment(self, enrollment_id: str) -> bool:
        """Delete an enrollment"""
        with self.db_session() as session:
            enrollment = session.query(Enrollment).filter(
                Enrollment.EnrollmentID == enrollment_id
            ).first()
            
            if not enrollment:
                return False
            
            session.delete(enrollment)
            session.commit()
            return True
    
    def get_enrollment_count_by_course(self, course_id: str) -> int:
        """Get total enrollment count for a course"""
        with self.db_session() as session:
            return session.query(Enrollment).filter(
                Enrollment.CourseID == course_id
            ).count()
    
    def get_enrollment_stats(self, student_id: str) -> Dict[str, Any]:
        """Get enrollment statistics for a student"""
        with self.db_session() as session:
            all_enrollments = session.query(Enrollment).filter(
                Enrollment.StudentID == student_id
            ).all()
            
            active = sum(1 for e in all_enrollments if e.Status == 'Active')
            completed = sum(1 for e in all_enrollments if e.Status == 'Completed')
            dropped = sum(1 for e in all_enrollments if e.Status == 'Dropped')
            suspended = sum(1 for e in all_enrollments if e.Status == 'Suspended')
            
            return {
                'total_enrollments': len(all_enrollments),
                'active': active,
                'completed': completed,
                'dropped': dropped,
                'suspended': suspended
            }


class PaymentService:
    """Service for Payment CRUD operations"""
    
    def __init__(self, db_session: sessionmaker, max_retries=50):
        self.db_session = db_session
        self.max_retries = max_retries

    def create_payment(self, payment_data: Dict[str, Any]) -> Payment:
        """Create a new payment"""
        for attempt in range(self.max_retries):
            new_id = generate_id(self.db_session, Payment.PaymentID)
            payment_data["PaymentID"] = new_id
            with self.db_session() as session:
                try:
                    payment = Payment(**payment_data)
                    session.add(payment)
                    session.commit()
                    session.refresh(payment)
                    return payment
                except IntegrityError:
                    session.rollback()
                    print(f"Collision detected for {new_id}. Retrying...")
                    continue
                except Exception as e:
                    session.rollback()
                    raise e
        raise Exception(f"Failed to generate unique ID for {Payment.__name__} after {self.max_retries} attempts.")
                
    
    def get_payment_by_id(self, payment_id: str) -> Optional[Payment]:
        """Get payment by ID"""
        with self.db_session() as session:
            return session.query(Payment).filter(Payment.PaymentID == payment_id).first()
    
    def get_payments_by_user(self, user_id: str) -> List[Payment]:
        """Get all payments made by a user"""
        with self.db_session() as session:
            return session.query(Payment).filter(Payment.UserID == user_id).all()
    
    def get_payments_by_method(self, payment_method: str) -> List[Payment]:
        """Get all payments by payment method"""
        with self.db_session() as session:
            return session.query(Payment).filter(Payment.Payment_method == payment_method).all()
    
    def get_payments_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Payment]:
        """Get payments within a date range"""
        with self.db_session() as session:
            return session.query(Payment).filter(
                Payment.Payment_date >= start_date,
                Payment.Payment_date <= end_date
            ).all()
    
    def get_all_payments(self, limit: int = 100) -> List[Payment]:
        """Get all payments with pagination"""
        with self.db_session() as session:
            return session.query(Payment).limit(limit).all()
    
    def update_payment(self, payment_id: str, update_data: Dict[str, Any]) -> Optional[Payment]:
        """Update payment information"""
        with self.db_session() as session:
            payment = session.query(Payment).filter(Payment.PaymentID == payment_id).first()
            if not payment:
                return None
            
            for key, value in update_data.items():
                if hasattr(payment, key):
                    setattr(payment, key, value)
            
            session.commit()
            session.refresh(payment)
            return payment
    
    def delete_payment(self, payment_id: str) -> bool:
        """Delete a payment"""
        with self.db_session() as session:
            payment = session.query(Payment).filter(Payment.PaymentID == payment_id).first()
            if not payment:
                return False
            
            session.delete(payment)
            session.commit()
            return True
    
    def get_total_revenue(self) -> int:
        """Get total revenue from all payments"""
        with self.db_session() as session:
            result = session.query(func.sum(Payment.Amount)).scalar()
            return int(result) if result else 0
    
    def get_revenue_by_user(self, user_id: str) -> int:
        """Get total amount paid by a user"""
        with self.db_session() as session:
            result = session.query(func.sum(Payment.Amount)).filter(
                Payment.UserID == user_id
            ).scalar()
            return int(result) if result else 0
    
    def get_revenue_by_date_range(self, start_date: datetime, end_date: datetime) -> int:
        """Get total revenue within a date range"""
        with self.db_session() as session:
            result = session.query(func.sum(Payment.Amount)).filter(
                Payment.Payment_date >= start_date,
                Payment.Payment_date <= end_date
            ).scalar()
            return int(result) if result else 0
    
    def get_payment_statistics(self) -> Dict[str, Any]:
        """Get payment statistics"""
        with self.db_session() as session:
            total_payments = session.query(Payment).count()
            total_revenue = session.query(func.sum(Payment.Amount)).scalar() or 0
            avg_payment = session.query(func.avg(Payment.Amount)).scalar() or 0
            
            methods = session.query(
                Payment.Payment_method,
                func.count(Payment.PaymentID)
            ).group_by(Payment.Payment_method).all()
            
            return {
                'total_payments': total_payments,
                'total_revenue': int(total_revenue),
                'average_payment': float(avg_payment),
                'payment_methods': {method: count for method, count in methods}
            }


class CertificateService:
    """Service for Certificate CRUD operations"""
    
    def __init__(self, db_session: sessionmaker, max_retries=50):
        self.db_session = db_session
        self.max_retries = max_retries
        
    def create_certificate(self, certificate_data: Dict[str, Any]) -> Certificate:
        """Create a new certificate"""
        for attempt in range(self.max_retries):
            new_id = generate_id(self.db_session, Certificate.CertificateID)
            certificate_data["CertificateID"] = new_id
            with self.db_session() as session:
                try:
                    cer = Certificate(**certificate_data)
                    session.add(cer)
                    session.commit()
                    session.refresh(cer)
                    return cer
                except IntegrityError:
                    session.rollback()
                    print(f"Collision detected for {new_id}. Retrying...")
                    continue
                except Exception as e:
                    session.rollback()
                    raise e
        raise Exception(f"Failed to generate unique ID for {Certificate.__name__} after {self.max_retries} attempts.")
    
    def get_certificate_by_id(self, certificate_id: str) -> Optional[Certificate]:
        """Get certificate by ID"""
        with self.db_session() as session:
            return session.query(Certificate).filter(
                Certificate.CertificateID == certificate_id
            ).first()
    
    def get_certificate(self, certificate_id: str, course_id: str, 
                        student_id: str) -> Optional[Certificate]:
        """Get certificate by composite primary key"""
        with self.db_session() as session:
            return session.query(Certificate).filter(
                Certificate.CertificateID == certificate_id,
                Certificate.CourseID == course_id,
                Certificate.StudentID == student_id
            ).first()
    
    def get_student_certificates(self, student_id: str) -> List[Certificate]:
        """Get all certificates for a student"""
        with self.db_session() as session:
            return session.query(Certificate).filter(
                Certificate.StudentID == student_id
            ).all()
    
    def get_course_certificates(self, course_id: str) -> List[Certificate]:
        """Get all certificates issued for a course"""
        with self.db_session() as session:
            return session.query(Certificate).filter(
                Certificate.CourseID == course_id
            ).all()
    
    def get_certificate_by_number(self, certificate_number: str) -> Optional[Certificate]:
        """Get certificate by certificate number"""
        with self.db_session() as session:
            return session.query(Certificate).filter(
                Certificate.Certificate_number == certificate_number
            ).first()
    
    def has_certificate(self, student_id: str, course_id: str) -> bool:
        """Check if a student has a certificate for a course"""
        with self.db_session() as session:
            certificate = session.query(Certificate).filter(
                Certificate.StudentID == student_id,
                Certificate.CourseID == course_id
            ).first()
            return certificate is not None
    
    def update_certificate(self, certificate_id: str, update_data: Dict[str, Any]) -> Optional[Certificate]:
        """Update certificate information"""
        with self.db_session() as session:
            certificate = session.query(Certificate).filter(
                Certificate.CertificateID == certificate_id
            ).first()
            
            if not certificate:
                return None
            
            for key, value in update_data.items():
                if hasattr(certificate, key):
                    setattr(certificate, key, value)
            
            session.commit()
            session.refresh(certificate)
            return certificate
    
    def delete_certificate(self, certificate_id: str) -> bool:
        """Delete a certificate"""
        with self.db_session() as session:
            certificate = session.query(Certificate).filter(
                Certificate.CertificateID == certificate_id
            ).first()
            
            if not certificate:
                return False
            
            session.delete(certificate)
            session.commit()
            return True
    
    def get_active_certificates(self, student_id: str) -> List[Certificate]:
        """Get all non-expired certificates for a student"""
        with self.db_session() as session:
            today = date.today()
            return session.query(Certificate).filter(
                Certificate.StudentID == student_id,
                (Certificate.Expiry_date.is_(None)) | (Certificate.Expiry_date > today)
            ).all()
    
    def get_expired_certificates(self, student_id: str) -> List[Certificate]:
        """Get all expired certificates for a student"""
        with self.db_session() as session:
            today = date.today()
            return session.query(Certificate).filter(
                Certificate.StudentID == student_id,
                Certificate.Expiry_date <= today
            ).all()
    
    def is_certificate_valid(self, certificate_id: str) -> bool:
        """Check if a certificate is still valid (not expired)"""
        with self.db_session() as session:
            certificate = session.query(Certificate).filter(
                Certificate.CertificateID == certificate_id
            ).first()
            
            if not certificate:
                return False
            
            # If no expiry date, certificate is always valid
            if certificate.Expiry_date is None:
                return True
            
            return certificate.Expiry_date > date.today()
    
    def get_certificates_issued_in_range(self, start_date: date, end_date: date) -> List[Certificate]:
        """Get certificates issued within a date range"""
        with self.db_session() as session:
            return session.query(Certificate).filter(
                Certificate.Issue_date >= start_date,
                Certificate.Issue_date <= end_date
            ).all()
    
    def get_certificate_count_by_course(self, course_id: str) -> int:
        """Get total number of certificates issued for a course"""
        with self.db_session() as session:
            return session.query(Certificate).filter(
                Certificate.CourseID == course_id
            ).count()
    
    def get_certificate_statistics(self) -> Dict[str, Any]:
        """Get certificate statistics"""
        with self.db_session() as session:
            total_certificates = session.query(Certificate).count()
            
            today = date.today()
            active_certificates = session.query(Certificate).filter(
                (Certificate.Expiry_date.is_(None)) | (Certificate.Expiry_date > today)
            ).count()
            
            expired_certificates = session.query(Certificate).filter(
                Certificate.Expiry_date <= today
            ).count()
            
            return {
                'total_certificates': total_certificates,
                'active_certificates': active_certificates,
                'expired_certificates': expired_certificates
            }