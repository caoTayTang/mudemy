import { useState, useEffect } from 'react';
import { analyticsService } from '../services/analyticsService';

export const useInstructorAnalyticsController = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalRevenue: 0,
    totalEnrollments: 0,
    averageRating: 0
  });
  
  // State for filters
  const [timeRange, setTimeRange] = useState('Last 12 months');
  const [activeTab, setActiveTab] = useState('Overview');

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

  return {
    loading,
    stats,
    filters: {
      timeRange,
      activeTab
    },
    actions: {
      handleTimeRangeChange,
      setActiveTab
    }
  };
};