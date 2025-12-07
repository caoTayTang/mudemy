import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children, allowedRoles = [] }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background-light dark:bg-background-dark">
        <span className="material-symbols-outlined animate-spin text-4xl text-primary">progress_activity</span>
      </div>
    );
  }

  // 1. Check if Logged In
  if (!user) {
    // Redirect to login, remembering where they tried to go
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // 2. Check Role (if specific roles required)
  // Logic: Instructors have IFlag=true, Students have SFlag=true
  if (allowedRoles.length > 0) {
    const isInstructor = user.IFlag || user.role === 'tutor';
    const isStudent = user.SFlag || user.role === 'tutee';

    if (allowedRoles.includes('tutor') && !isInstructor) {
      return <Navigate to="/" replace />; // Unauthorized
    }
    // Add other role checks if needed
  }

  return children;
};

export default ProtectedRoute;