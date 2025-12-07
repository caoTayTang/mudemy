import React from 'react';
import { useStudentDashboardController } from '../hooks/useStudentDashboardController';
import { useNavigate } from 'react-router-dom';
import profileImg from '../assets/profile.jpg';

const StudentDashboardPage = () => {
  const navigate = useNavigate();
  const { 
    user, 
    courses, // These are now filtered & sorted
    rawCount, // Total enrolled count
    loading, 
    activeTab, 
    setActiveTab,
    searchTerm,
    setSearchTerm,
    sortBy,
    setSortBy,
    actions 
  } = useStudentDashboardController();

  if (loading) return (
    <div className="min-h-screen bg-background-light dark:bg-background-dark p-10 text-center text-text-body-light dark:text-text-body-dark">
      Loading dashboard...
    </div>
  );

  // Stats Logic
  const completedCourses = courses.filter(c => c.status === 'Completed' || c.progress === 100).length;
  // Calculate global progress based on current view or raw total
  const totalProgressSum = courses.reduce((acc, curr) => acc + (curr.progress || 0), 0);
  const globalProgress = courses.length > 0 ? Math.round(totalProgressSum / courses.length) : 0;

  return (
    <div className="font-display bg-background-light dark:bg-background-dark text-text-body-light dark:text-text-body-dark">
      <div className="relative flex h-auto min-h-screen w-full flex-col">
        
        {/* HEADER */}
        <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-primary/20 dark:border-primary/30 px-6 sm:px-10 py-3 bg-background-light dark:bg-background-dark sticky top-0 z-10">
          <div className="flex items-center gap-8 cursor-pointer" onClick={() => navigate('/')}>
            <div className="flex items-center gap-2 text-primary">
              <span className="material-symbols-outlined text-2xl">school</span>
              <h2 className="text-[#1b0d0d] dark:text-white text-lg font-bold leading-tight tracking-[-0.015em]">MUDemy</h2>
            </div>
          </div>
          
          {/* SEARCH BAR (CONNECTED) */}
          <div className="hidden md:flex flex-none max-w-lg items-center justify-center mx-auto">
            <label className="flex flex-col w-full !h-10">
              <div className="flex w-full flex-1 items-stretch rounded-lg h-full">
                <div className="text-[#9a4c4c] dark:text-gray-400 flex bg-primary/20 dark:bg-white/10 items-center justify-center pl-4 rounded-l-lg">
                  <span className="material-symbols-outlined">search</span>
                </div>
                <input 
                  className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-[#1b0d0d] dark:text-white focus:outline-0 focus:ring-0 border-none bg-primary/20 dark:bg-white/10 h-full placeholder:text-[#9a4c4c] dark:placeholder:text-gray-400 px-4 pl-2 text-base font-normal leading-normal" 
                  placeholder="Search your courses..." 
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </label>
          </div>

          <div className="flex flex-none justify-end gap-4">
            <button className="flex max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 w-10 bg-primary/20 dark:bg-white/10 text-[#1b0d0d] dark:text-white gap-2 text-sm font-bold leading-normal tracking-[0.015em] min-w-0">
              <span className="material-symbols-outlined">notifications</span>
            </button>
            <div 
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" 
              style={{ backgroundImage: `url("${profileImg}")` }}
            ></div>
          </div>
        </header>

        <div className="flex flex-1">
          {/* SIDEBAR */}
          <aside className="w-64 flex-shrink-0 p-4 border-r border-primary/20 dark:border-primary/30 hidden md:block">
            <div className="flex h-full flex-col justify-between">
              <div className="flex flex-col gap-4">
                <div className="flex gap-3 items-center">
                  <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" style={{ backgroundImage: `url("${profileImg}")` }}></div>
                  <div className="flex flex-col">
                    <h1 className="text-[#1b0d0d] dark:text-white text-base font-medium leading-normal">{user?.User_name || user?.name}</h1>
                    <p className="text-[#9a4c4c] dark:text-gray-400 text-sm font-normal leading-normal">{user?.Email || "Student"}</p>
                  </div>
                </div>
                <div className="flex flex-col gap-2 mt-4">
                  <div className="flex items-center gap-3 px-3 py-2 rounded-lg bg-primary text-white">
                    <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>book</span>
                    <p className="text-sm font-medium leading-normal">Dashboard</p>
                  </div>
                </div>
              </div>
              <div className="flex flex-col gap-1">
                <div className="flex items-center gap-3 px-3 py-2 text-[#1b0d0d] dark:text-white cursor-pointer hover:bg-primary/20 dark:hover:bg-white/10 rounded-lg">
                  <span className="material-symbols-outlined">settings</span>
                  <p className="text-sm font-medium leading-normal">Settings</p>
                </div>
                <div 
                  className="flex items-center gap-3 px-3 py-2 text-[#1b0d0d] dark:text-white cursor-pointer hover:bg-primary/20 dark:hover:bg-white/10 rounded-lg"
                  onClick={actions.handleLogout} 
                >
                  <span className="material-symbols-outlined">logout</span>
                  <p className="text-sm font-medium leading-normal">Log out</p>
                </div>
              </div>
            </div>
          </aside>

          {/* MAIN CONTENT */}
          <main className="flex-1 p-6 sm:p-8 lg:p-10">
            <div className="flex flex-wrap justify-between gap-3 mb-6">
              <div className="flex flex-col gap-4 w-full">
                <div>
                  <p className="text-[#1b0d0d] dark:text-white text-3xl font-black leading-tight tracking-[-0.033em]">Welcome back, {user?.User_name || user?.name}!</p>
                  <p className="text-[#9a4c4c] dark:text-gray-400 text-base font-normal leading-normal">Let's continue your learning journey.</p>
                </div>

                {/* --- TOTAL PROGRESS (Based on Current Filter) --- */}
                <div className="bg-white dark:bg-gray-800 p-4 rounded-xl border border-primary/20 dark:border-primary/30 shadow-sm max-w-2xl">
                  <div className="flex justify-between items-end mb-2">
                    <div>
                      <p className="text-sm font-bold text-primary mb-1">Current Progress</p>
                      <p className="text-xs text-text-body-light dark:text-text-body-dark">
                        Average completion of <span className="font-bold">{courses.length}</span> displayed courses
                      </p>
                    </div>
                    <span className="text-2xl font-black text-primary">{globalProgress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
                    <div 
                      className="bg-primary h-3 rounded-full transition-all duration-500 ease-out" 
                      style={{ width: `${globalProgress}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            {/* CONTROLS BAR: TABS + SORT */}
            <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
              {/* TABS */}
              <div className="flex gap-2 p-1 overflow-x-auto">
                <button 
                  onClick={() => setActiveTab('all')}
                  className={`flex h-9 shrink-0 items-center justify-center gap-x-2 rounded-lg pl-4 pr-4 transition-colors ${activeTab === 'all' ? 'bg-primary text-white' : 'bg-primary/20 dark:bg-white/10 text-[#1b0d0d] dark:text-white hover:bg-primary/30'}`}
                >
                  <p className="text-sm font-medium leading-normal">All Courses</p>
                </button>
                <button 
                  onClick={() => setActiveTab('in-progress')}
                  className={`flex h-9 shrink-0 items-center justify-center gap-x-2 rounded-lg pl-4 pr-4 transition-colors ${activeTab === 'in-progress' ? 'bg-primary text-white' : 'bg-primary/20 dark:bg-white/10 text-[#1b0d0d] dark:text-white hover:bg-primary/30'}`}
                >
                  <p className="text-sm font-medium leading-normal">In Progress</p>
                </button>
                <button 
                  onClick={() => setActiveTab('completed')}
                  className={`flex h-9 shrink-0 items-center justify-center gap-x-2 rounded-lg pl-4 pr-4 transition-colors ${activeTab === 'completed' ? 'bg-primary text-white' : 'bg-primary/20 dark:bg-white/10 text-[#1b0d0d] dark:text-white hover:bg-primary/30'}`}
                >
                  <p className="text-sm font-medium leading-normal">Completed</p>
                </button>
              </div>

              {/* SORT DROPDOWN */}
              <div className="relative">
                <select 
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="appearance-none bg-primary/10 dark:bg-white/5 border border-primary/20 dark:border-white/10 text-[#1b0d0d] dark:text-white rounded-lg pl-3 pr-8 py-2 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-primary/50 cursor-pointer"
                >
                  <option value="recent">Recently Enrolled</option>
                  <option value="title_az">Title (A-Z)</option>
                  <option value="progress_desc">Progress (High to Low)</option>
                  <option value="progress_asc">Progress (Low to High)</option>
                </select>
                <span className="material-symbols-outlined absolute right-2 top-1/2 -translate-y-1/2 text-primary pointer-events-none text-lg">sort</span>
              </div>
            </div>

            {/* COURSES GRID */}
            <div className="grid grid-cols-1 gap-6">
              {courses.length === 0 && (
                <div className="text-center py-10 text-[#9a4c4c] dark:text-gray-400">
                  <span className="material-symbols-outlined text-4xl mb-2">search_off</span>
                  <p>No courses match your criteria.</p>
                  {rawCount === 0 && <button onClick={() => navigate('/')} className="mt-4 text-primary font-bold hover:underline">Browse Catalog</button>}
                </div>
              )}

              {courses.map(course => (
                <div key={course.id} className="flex flex-col gap-4 rounded-xl bg-background-light dark:bg-background-dark p-4 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] border border-primary/20 dark:border-primary/30 hover:border-primary/50 transition-colors">
                  <div className="flex flex-col md:flex-row items-start md:items-center gap-4">
                    <div 
                      className="w-full md:w-48 h-28 bg-center bg-no-repeat bg-cover rounded-lg flex-shrink-0" 
                      style={{ backgroundImage: `url("${course.image}")` }}
                    ></div>
                    <div className="flex-1 w-full">
                      <div className="flex justify-between items-start">
                        <div>
                          <span className={`text-xs font-semibold uppercase tracking-wider px-2 py-1 rounded-full ${course.status === 'Completed' || course.progress === 100 ? 'bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-300' : 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/50'}`}>
                            {course.progress === 100 ? 'Completed' : course.status}
                          </span>
                          <p className="text-[#1b0d0d] dark:text-white text-lg font-bold leading-tight mt-2">{course.title}</p>
                          <p className="text-[#9a4c4c] dark:text-gray-400 text-sm font-normal leading-normal">by {course.instructor}</p>
                        </div>
                        
                        <button className="hidden md:flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-medium leading-normal w-fit transition-transform hover:scale-105">
                          <span>{course.progress === 100 ? 'Review Course' : 'Continue Learning'}</span>
                        </button>
                      </div>
                      
                      {/* INDIVIDUAL PROGRESS (Restored) */}
                      <div className="mt-4">
                        <div className="flex justify-between text-sm text-[#9a4c4c] dark:text-gray-400 mb-1">
                          <span>Progress</span>
                          <span>{Math.round(course.progress)}%</span>
                        </div>
                        <div className="w-full bg-primary/20 dark:bg-white/10 rounded-full h-2">
                          <div 
                            className="bg-primary h-2 rounded-full transition-all duration-300" 
                            style={{ width: `${course.progress}%` }}
                          ></div>
                        </div>
                      </div>

                    </div>
                  </div>
                  
                  {/* LESSONS LIST */}
                  <div className="border-t border-primary/20 dark:border-primary/30 pt-4">
                    <h4 className="text-sm font-bold text-[#1b0d0d] dark:text-white mb-3">Lessons</h4>
                    <ul className="space-y-2">
                      {course.lessons.length > 0 ? course.lessons.map((lesson, idx) => (
                        <li key={idx} className="flex items-center gap-3 text-sm">
                          <span 
                            className={`material-symbols-outlined ${lesson.completed ? 'text-primary' : 'text-[#9a4c4c] dark:text-gray-400'}`} 
                            style={{ fontVariationSettings: lesson.completed ? "'FILL' 1" : "'FILL' 0" }}
                          >
                            {lesson.completed ? 'check_circle' : 'radio_button_unchecked'}
                          </span>
                          <span className={lesson.completed ? "text-[#1b0d0d] dark:text-white" : "text-[#9a4c4c] dark:text-gray-400"}>
                            {lesson.title}
                          </span>
                        </li>
                      )) : <li className="text-sm text-[#9a4c4c] dark:text-gray-400 italic">No lessons available yet.</li>}
                    </ul>
                  </div>
                  
                  {/* Mobile Button */}
                  <button className="md:hidden flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-medium leading-normal w-full mt-2">
                    <span>{course.progress === 100 ? 'Review Course' : 'Continue Learning'}</span>
                  </button>
                </div>
              ))}
            </div>
            
          </main>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboardPage;