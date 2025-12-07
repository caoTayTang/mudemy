import { useState, useEffect } from 'react';
import { analyticsService } from '../services/analyticsService';
import { authService } from '../services/authService'; // Import Auth Service
import { useNavigate } from 'react-router-dom';

export const useInstructorAnalyticsController = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalRevenue: 0,
    totalEnrollments: 0,
    averageRating: 0
  });

  const [user, setUser] = useState(null); // NEW: Track Logged-in User

  
  // State for filters
  const [timeRange, setTimeRange] = useState('Last 12 months');
  const [activeTab, setActiveTab] = useState('Overview');
  const navigate = useNavigate();
  
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await analyticsService.getOverview(timeRange);
        setStats(data);
      } catch (error) {
        console.error("Failed to fetch analytics", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [timeRange]);

  const handleTimeRangeChange = (e) => {
    setTimeRange(e.target.value);
  };

  // NEW: Logout Action
  const handleLogout = async () => {
    await authService.logout();
    setUser(null);
    navigate('/');
  };

  return {
    loading,
    user,
    stats,
    filters: {
      timeRange,
      activeTab
    },
    actions: {
      handleTimeRangeChange,
      setActiveTab,
      handleLogout
    }
  };
};