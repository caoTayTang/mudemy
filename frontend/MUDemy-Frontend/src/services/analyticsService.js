/**
 * Analytics Service (Model)
 * Handles data fetching for instructor analytics.
 */

const MOCK_ANALYTICS_OVERVIEW = {
  totalRevenue: 0.00,
  totalEnrollments: 0,
  averageRating: 0.00,
  currency: "$"
};

export const analyticsService = {
  getOverview: async (timeRange) => {
    // Simulate API call based on timeRange (e.g., '12m', '30d')
    return new Promise(resolve => {
      setTimeout(() => {
        resolve(MOCK_ANALYTICS_OVERVIEW);
      }, 300);
    });
  }
};