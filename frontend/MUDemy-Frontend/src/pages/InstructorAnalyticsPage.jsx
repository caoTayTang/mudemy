import React from 'react';
import { useInstructorAnalyticsController } from '../hooks/useInstructorAnalyticsController';
import { useNavigate } from 'react-router-dom';

const InstructorAnalyticsPage = () => {
  const navigate = useNavigate();
  const { loading, stats, filters, actions } = useInstructorAnalyticsController();

  return (
    <div className="bg-background-light dark:bg-background-dark font-poppins text-text-light dark:text-text-dark min-h-screen flex">
      
      {/* --- MAIN SIDEBAR (Global) --- */}
      <aside className="w-64 flex flex-col bg-[#0f172a] text-white flex-shrink-0">
        <div className="p-6">
          <div className="bg-primary h-12 w-12 rounded flex items-center justify-center cursor-pointer" onClick={() => navigate('/')}>
            <span className="text-white text-3xl font-bold">M</span>
          </div>
        </div>
        <nav className="flex-1 px-4 space-y-2">
          <a className="flex items-center space-x-3 px-3 py-2 rounded text-slate-300 hover:bg-slate-700/50 transition-colors" href="/instructor/courses">
            <span className="material-icons-outlined">apps</span>
            <span>Dashboard</span>
          </a>
          <a className="flex items-center space-x-3 px-3 py-2 rounded text-slate-300 hover:bg-slate-700/50 transition-colors" href="/instructor/courses">
            <span className="material-icons-outlined">play_circle</span>
            <span>Courses</span>
          </a>
          <a className="flex items-center space-x-3 px-3 py-2 rounded text-slate-300 hover:bg-slate-700/50 transition-colors" href="#">
            <span className="material-icons-outlined">schedule</span>
            <span>Communication</span>
          </a>
          {/* Active State */}
          <a className="flex items-center space-x-3 px-3 py-2 rounded bg-primary/20 border-l-4 border-primary text-white" href="#">
            <span className="material-icons-outlined">bar_chart</span>
            <span>Performance</span>
          </a>
          <a className="flex items-center space-x-3 px-3 py-2 rounded text-slate-300 hover:bg-slate-700/50 transition-colors" href="#">
            <span className="material-icons-outlined">build</span>
            <span>Tools</span>
          </a>
          <a className="flex items-center space-x-3 px-3 py-2 rounded text-slate-300 hover:bg-slate-700/50 transition-colors" href="#">
            <span className="material-icons-outlined">help_outline</span>
            <span>Resources</span>
          </a>
        </nav>
        <div className="p-4">
          <a className="flex items-center space-x-3 px-3 py-2 rounded text-slate-300 hover:bg-slate-700/50 transition-colors" href="#">
            <span className="material-icons-outlined">settings</span>
            <span>Settings</span>
          </a>
        </div>
      </aside>

      <div className="flex-1 flex flex-col min-w-0">
        
        {/* --- TOP HEADER --- */}
        <header className="h-16 flex items-center justify-end px-8 border-b border-border-light dark:border-border-dark bg-white dark:bg-[#0f172a] flex-shrink-0">
          <div className="flex items-center space-x-6">
            <a className="text-sm font-medium text-text-muted-light dark:text-slate-300 hover:text-primary transition-colors" href="#">Instructor</a>
            <button className="relative text-text-muted-light dark:text-slate-400 hover:text-primary transition-colors">
              <span className="material-icons-outlined">notifications</span>
            </button>
            <button className="w-10 h-10 rounded-full bg-slate-700 text-white font-bold flex items-center justify-center">L</button>
          </div>
        </header>

        {/* --- CONTENT AREA --- */}
        <main className="flex-1 flex overflow-hidden">
          
          {/* SUB SIDEBAR (Performance Nav) */}
          <nav className="w-64 border-r border-border-light dark:border-border-dark bg-white dark:bg-[#0f172a] p-6 hidden md:block flex-shrink-0 overflow-y-auto">
            <h2 className="text-2xl font-bold text-text-light dark:text-white mb-6">Performance</h2>
            <ul className="space-y-1">
              <li>
                <button 
                  onClick={() => actions.setActiveTab('Overview')}
                  className={`w-full text-left block px-4 py-2 font-semibold rounded-r transition-colors ${filters.activeTab === 'Overview' ? 'text-primary border-l-4 border-primary bg-primary/5 dark:bg-primary/10' : 'text-text-muted-light dark:text-slate-300 hover:text-primary hover:bg-slate-100 dark:hover:bg-slate-800/50'}`}
                >
                  Overview
                </button>
              </li>
              {['Revenue', 'Students', 'Reviews'].map((tab) => (
                 <li key={tab}>
                  <button 
                    onClick={() => actions.setActiveTab(tab)}
                    className="w-full text-left block px-4 py-2 text-text-muted-light dark:text-slate-300 hover:text-primary hover:bg-slate-100 dark:hover:bg-slate-800/50 rounded transition-colors"
                  >
                    {tab}
                  </button>
                </li>
              ))}
              <li>
                <a className="flex justify-between items-center px-4 py-2 text-text-muted-light dark:text-slate-300 hover:text-primary hover:bg-slate-100 dark:hover:bg-slate-800/50 rounded transition-colors cursor-pointer">
                  <span>Engagement</span>
                  <span className="material-icons-outlined text-base">expand_more</span>
                </a>
              </li>
              <li><a className="block px-4 py-2 text-text-muted-light dark:text-slate-300 hover:text-primary hover:bg-slate-100 dark:hover:bg-slate-800/50 rounded transition-colors cursor-pointer">Traffic & conversion</a></li>
            </ul>
          </nav>

          {/* MAIN STATS CONTENT */}
          <div className="flex-1 p-8 overflow-y-auto">
            {loading ? (
              <div className="text-center p-10">Loading analytics...</div>
            ) : (
              <>
                <div className="mb-6">
                  <div className="flex items-center space-x-2">
                    <h1 className="text-3xl font-bold text-text-light dark:text-white">Overview</h1>
                    <button className="flex items-center text-primary font-semibold">
                      <span>All courses</span>
                      <span className="material-icons-outlined text-lg">expand_more</span>
                    </button>
                  </div>
                  <p className="text-text-muted-light dark:text-slate-400 mt-1">Get top insights about your performance</p>
                </div>

                {/* KPI CARDS */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                  <div className="bg-white dark:bg-slate-800/50 p-4 rounded border border-border-light dark:border-border-dark shadow-sm">
                    <div className="flex items-center text-sm text-text-muted-light dark:text-slate-400">
                      <span>This month so far</span>
                      <span className="material-icons-outlined text-base ml-1">info_outline</span>
                    </div>
                    <p className="text-3xl font-bold text-text-light dark:text-white mt-2">${stats.totalRevenue.toFixed(2)}</p>
                    <p className="text-sm text-text-muted-light dark:text-slate-400">$0.00 total revenue</p>
                  </div>
                  
                  <div className="bg-white dark:bg-slate-800/50 p-4 rounded border border-border-light dark:border-border-dark shadow-sm">
                    <div className="flex items-center text-sm text-text-muted-light dark:text-slate-400">
                      <span>This month so far</span>
                      <span className="material-icons-outlined text-base ml-1">info_outline</span>
                    </div>
                    <p className="text-3xl font-bold text-text-light dark:text-white mt-2">{stats.totalEnrollments}</p>
                    <p className="text-sm text-text-muted-light dark:text-slate-400">0 total enrollments</p>
                  </div>

                  <div className="bg-white dark:bg-slate-800/50 p-4 rounded border border-border-light dark:border-border-dark shadow-sm">
                    <div className="flex items-center text-sm text-text-muted-light dark:text-slate-400">
                      <span>This month so far</span>
                      <span className="material-icons-outlined text-base ml-1">info_outline</span>
                    </div>
                    <p className="text-3xl font-bold text-text-light dark:text-white mt-2">{stats.averageRating.toFixed(2)}</p>
                    <p className="text-sm text-text-muted-light dark:text-slate-400">0.00 average rating</p>
                  </div>
                </div>

                {/* CHART SECTION */}
                <div className="bg-white dark:bg-slate-800/50 p-6 rounded border border-border-light dark:border-border-dark shadow-sm">
                  <div className="flex flex-col sm:flex-row justify-end items-center mb-4 gap-4">
                    <div className="flex items-center space-x-4">
                      <span className="text-sm text-text-muted-light dark:text-slate-400">Date range:</span>
                      <div className="relative">
                        <select 
                          value={filters.timeRange}
                          onChange={actions.handleTimeRangeChange}
                          className="appearance-none bg-white dark:bg-slate-700 border border-border-light dark:border-border-dark rounded py-2 pl-3 pr-8 text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary text-text-light dark:text-white"
                        >
                          <option>Last 12 months</option>
                          <option>Last 6 months</option>
                          <option>Last 30 days</option>
                        </select>
                        <span className="material-icons-outlined text-lg absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none text-text-muted-light">expand_more</span>
                      </div>
                      <button className="bg-primary text-white font-semibold py-2 px-4 rounded flex items-center space-x-1 hover:bg-red-700 transition-colors">
                        <span>Export</span>
                        <span className="material-icons-outlined text-lg">expand_more</span>
                      </button>
                    </div>
                  </div>

                  <div className="h-80 flex items-center justify-center border-t border-border-light dark:border-border-dark">
                    <p className="text-text-muted-light dark:text-slate-400">No data to display</p>
                  </div>
                  
                  <div className="border-t border-border-light dark:border-border-dark mt-4 pt-4 text-center">
                    <a className="text-primary font-semibold text-sm flex items-center justify-center hover:underline cursor-pointer">
                      <span>Revenue Report</span>
                      <span className="material-icons-outlined text-lg ml-1">chevron_right</span>
                    </a>
                  </div>
                </div>
              </>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

export default InstructorAnalyticsPage;