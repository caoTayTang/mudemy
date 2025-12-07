import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import CourseDetailPage from './pages/CourseDetailPage';
import CheckoutPage from './pages/CheckoutPage';
import StudentDashboardPage from './pages/StudentDashboardPage';
import InstructorCoursePage from './pages/InstructorCoursePage';
import InstructorAnalyticsPage from './pages/InstructorAnalyticsPage'; // Import Analytics
import { AuthProvider } from './context/AuthContext'; // Import Provider
import ProtectedRoute from './components/ProtectedRoute'; // Import Protection Wrapper


function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/course/:id" element={<CourseDetailPage />} />

        <Route 
          path="/checkout" 
          element={
            <ProtectedRoute>
              <CheckoutPage />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <StudentDashboardPage/>
            </ProtectedRoute>
          } 
        />

          <Route 
            path="/instructor/courses" 
            element={
              <ProtectedRoute allowedRoles={['tutor']}>
                <InstructorCoursePage />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/instructor" 
            element={
              <ProtectedRoute allowedRoles={['tutor']}>
                <InstructorAnalyticsPage />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </AuthProvider>
  );
}

export default App;