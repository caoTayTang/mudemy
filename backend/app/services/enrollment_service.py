from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from datetime import datetime, date
from ..models.models import Enrollment, Payment, Certificate

class EnrollmentService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, enrollment_id: str, course_id: str, payment_id: str,
               student_id: str, status: str = 'Active') -> Enrollment:
        enrollment = Enrollment(
            EnrollmentID=enrollment_id,
            CourseID=course_id,
            PaymentID=payment_id,
            StudentID=student_id,
            Status=status,
            Enroll_date=datetime.utcnow()
        )
        db = self.db_session()
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        db.close()
        return enrollment

    def get_by_id(self, enrollment_id: str) -> Optional[Enrollment]:
        db = self.db_session()
        result = db.query(Enrollment).filter(Enrollment.EnrollmentID == enrollment_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Enrollment]:
        db = self.db_session()
        result = db.query(Enrollment).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_student(self, student_id: str) -> List[Enrollment]:
        db = self.db_session()
        result = db.query(Enrollment).filter(Enrollment.StudentID == student_id).all()
        db.close()
        return result

    def get_by_course(self, course_id: str) -> List[Enrollment]:
        db = self.db_session()
        result = db.query(Enrollment).filter(Enrollment.CourseID == course_id).all()
        db.close()
        return result

    def get_by_status(self, status: str) -> List[Enrollment]:
        db = self.db_session()
        result = db.query(Enrollment).filter(Enrollment.Status == status).all()
        db.close()
        return result

    def get_by_student_and_course(self, student_id: str, course_id: str) -> Optional[Enrollment]:
        db = self.db_session()
        result = db.query(Enrollment).filter(
            Enrollment.StudentID == student_id,
            Enrollment.CourseID == course_id
        ).first()
        db.close()
        return result

    def update(self, enrollment_id: str, status: Optional[str] = None) -> Optional[Enrollment]:
        db = self.db_session()
        enrollment = db.query(Enrollment).filter(Enrollment.EnrollmentID == enrollment_id).first()
        if not enrollment:
            db.close()
            return None
        
        if status is not None:
            enrollment.Status = status
        
        db.commit()
        db.refresh(enrollment)
        db.close()
        return enrollment

    def delete(self, enrollment_id: str) -> bool:
        db = self.db_session()
        enrollment = db.query(Enrollment).filter(Enrollment.EnrollmentID == enrollment_id).first()
        if not enrollment:
            db.close()
            return False
        
        db.delete(enrollment)
        db.commit()
        db.close()
        return True

    def count_by_course(self, course_id: str) -> int:
        db = self.db_session()
        count = db.query(Enrollment).filter(Enrollment.CourseID == course_id).count()
        db.close()
        return count


class PaymentService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, payment_id: str, user_id: str, amount: int,
               payment_method: Optional[str] = None) -> Payment:
        payment = Payment(
            PaymentID=payment_id,
            UserID=user_id,
            Amount=amount,
            Payment_method=payment_method,
            Payment_date=datetime.utcnow()
        )
        db = self.db_session()
        db.add(payment)
        db.commit()
        db.refresh(payment)
        db.close()
        return payment

    def get_by_id(self, payment_id: str) -> Optional[Payment]:
        db = self.db_session()
        result = db.query(Payment).filter(Payment.PaymentID == payment_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        db = self.db_session()
        result = db.query(Payment).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_user(self, user_id: str) -> List[Payment]:
        db = self.db_session()
        result = db.query(Payment).filter(Payment.UserID == user_id).all()
        db.close()
        return result

    def get_by_method(self, payment_method: str) -> List[Payment]:
        db = self.db_session()
        result = db.query(Payment).filter(Payment.Payment_method == payment_method).all()
        db.close()
        return result

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Payment]:
        db = self.db_session()
        result = db.query(Payment).filter(
            Payment.Payment_date >= start_date,
            Payment.Payment_date <= end_date
        ).all()
        db.close()
        return result

    def update(self, payment_id: str, amount: Optional[int] = None,
               payment_method: Optional[str] = None) -> Optional[Payment]:
        db = self.db_session()
        payment = db.query(Payment).filter(Payment.PaymentID == payment_id).first()
        if not payment:
            db.close()
            return None
        
        if amount is not None:
            payment.Amount = amount
        if payment_method is not None:
            payment.Payment_method = payment_method
        
        db.commit()
        db.refresh(payment)
        db.close()
        return payment

    def delete(self, payment_id: str) -> bool:
        db = self.db_session()
        payment = db.query(Payment).filter(Payment.PaymentID == payment_id).first()
        if not payment:
            db.close()
            return False
        
        db.delete(payment)
        db.commit()
        db.close()
        return True

    def get_total_by_user(self, user_id: str) -> int:
        db = self.db_session()
        result = db.query(Payment).filter(Payment.UserID == user_id).all()
        total = sum(payment.Amount for payment in result)
        db.close()
        return total


class CertificateService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, certificate_id: str, course_id: str, student_id: str,
               certificate_number: str, expiry_date: Optional[date] = None,
               issue_date: Optional[date] = None) -> Certificate:
        certificate = Certificate(
            CertificateID=certificate_id,
            CourseID=course_id,
            StudentID=student_id,
            Certificate_number=certificate_number,
            Expiry_date=expiry_date,
            Issue_date=issue_date or datetime.utcnow().date()
        )
        db = self.db_session()
        db.add(certificate)
        db.commit()
        db.refresh(certificate)
        db.close()
        return certificate

    def get_by_id(self, certificate_id: str) -> Optional[Certificate]:
        db = self.db_session()
        result = db.query(Certificate).filter(Certificate.CertificateID == certificate_id).first()
        db.close()
        return result

    def get_by_number(self, certificate_number: str) -> Optional[Certificate]:
        db = self.db_session()
        result = db.query(Certificate).filter(Certificate.Certificate_number == certificate_number).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Certificate]:
        db = self.db_session()
        result = db.query(Certificate).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_student(self, student_id: str) -> List[Certificate]:
        db = self.db_session()
        result = db.query(Certificate).filter(Certificate.StudentID == student_id).all()
        db.close()
        return result

    def get_by_course(self, course_id: str) -> List[Certificate]:
        db = self.db_session()
        result = db.query(Certificate).filter(Certificate.CourseID == course_id).all()
        db.close()
        return result

    def get_by_student_and_course(self, student_id: str, course_id: str) -> Optional[Certificate]:
        db = self.db_session()
        result = db.query(Certificate).filter(
            Certificate.StudentID == student_id,
            Certificate.CourseID == course_id
        ).first()
        db.close()
        return result

    def get_expired(self) -> List[Certificate]:
        db = self.db_session()
        today = datetime.utcnow().date()
        result = db.query(Certificate).filter(
            Certificate.Expiry_date < today
        ).all()
        db.close()
        return result

    def get_valid(self) -> List[Certificate]:
        db = self.db_session()
        today = datetime.utcnow().date()
        result = db.query(Certificate).filter(
            (Certificate.Expiry_date >= today) | (Certificate.Expiry_date == None)
        ).all()
        db.close()
        return result

    def update(self, certificate_id: str, expiry_date: Optional[date] = None,
               certificate_number: Optional[str] = None) -> Optional[Certificate]:
        db = self.db_session()
        certificate = db.query(Certificate).filter(Certificate.CertificateID == certificate_id).first()
        if not certificate:
            db.close()
            return None
        
        if expiry_date is not None:
            certificate.Expiry_date = expiry_date
        if certificate_number is not None:
            certificate.Certificate_number = certificate_number
        
        db.commit()
        db.refresh(certificate)
        db.close()
        return certificate

    def delete(self, certificate_id: str) -> bool:
        db = self.db_session()
        certificate = db.query(Certificate).filter(Certificate.CertificateID == certificate_id).first()
        if not certificate:
            db.close()
            return False
        
        db.delete(certificate)
        db.commit()
        db.close()
        return True

    def is_valid(self, certificate_id: str) -> bool:
        db = self.db_session()
        certificate = db.query(Certificate).filter(Certificate.CertificateID == certificate_id).first()
        if not certificate:
            db.close()
            return False
        
        if certificate.Expiry_date is None:
            db.close()
            return True
        
        today = datetime.utcnow().date()
        is_valid = certificate.Expiry_date >= today
        db.close()
        return is_valid