
from ..models import*
from ..services import*
from ..core import*
from fastapi import Depends, HTTPException, status, Cookie, Response
from datetime import datetime, timezone, timedelta


def get_current_user_from_session(
    session_id: str | None = Cookie(None), 
    #role: UserRole = None
    #db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Cookie"},
    )

    if session_id is None:
        raise credentials_exception
    
    with  mututor_session() as db:
        session = db.query(MuSession).filter(MuSession.session_id == session_id).first()
        
        if not session:
           raise credentials_exception
            
        if session.expires_at < datetime.utcnow():
            db.delete(session)
            db.commit()
            raise credentials_exception
        
        # if session.role != role:
        #     return None

    return session