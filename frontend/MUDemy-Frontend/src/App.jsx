import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import CourseDetailPage from './pages/CourseDetailPage';
import CheckoutPage from './pages/CheckoutPage';
import StudentDashboardPage from './pages/StudentDashboardPage';
import InstructorCoursePage from './pages/InstructorCoursePage';
import InstructorAnalyticsPage from './pages/InstructorAnalyticsPage'; // Import Analytics

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/course/:id" element={<CourseDetailPage />} />
      <Route path="/checkout" element={<CheckoutPage />} />
      <Route path="/dashboard" element={<StudentDashboardPage />} />
      <Route path="/instructor/courses" element={<InstructorCoursePage />} />
      <Route path="/instructor/analytics" element={<InstructorAnalyticsPage />} /> {/* Add Route */}
    </Routes>
  );
}

export default App;