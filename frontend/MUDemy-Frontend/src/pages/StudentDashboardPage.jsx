import React from 'react';
import { useStudentDashboardController } from '../hooks/useStudentDashboardController';
import { useNavigate } from 'react-router-dom';

const StudentDashboardPage = () => {
  const navigate = useNavigate();
  const { user, courses, loading, activeTab, setActiveTab, actions } = useStudentDashboardController();

  if (loading) return <div className="min-h-screen bg-background-light dark:bg-background-dark p-10 text-center text-text-body-light dark:text-text-body-dark">Loading dashboard...</div>;

  const totalCourses = courses.length;
  const completedCourses = courses.filter(c => c.status === 'Completed' || c.progress === 100).length;
  const globalProgress = totalCourses > 0 ? Math.round((completedCourses / totalCourses) * 100) : 0;

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
          
          {/* SEARCH BAR - CENTERED */}
          <div className="hidden md:flex flex-1 max-w-lg items-center justify-center mx-auto">
            <label className="flex flex-col w-full !h-10">
              <div className="flex w-full flex-1 items-stretch rounded-lg h-full">
                <div className="text-[#9a4c4c] dark:text-gray-400 flex bg-primary/20 dark:bg-white/10 items-center justify-center pl-4 rounded-l-lg">
                  <span className="material-symbols-outlined">search</span>
                </div>
                <input className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-[#1b0d0d] dark:text-white focus:outline-0 focus:ring-0 border-none bg-primary/20 dark:bg-white/10 h-full placeholder:text-[#9a4c4c] dark:placeholder:text-gray-400 px-4 pl-2 text-base font-normal leading-normal" placeholder="Search for courses..." />
              </div>
            </label>
          </div>

          <div className="flex flex-1 justify-end gap-4 sm:gap-6">
            <button className="flex max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 w-10 bg-primary/20 dark:bg-white/10 text-[#1b0d0d] dark:text-white gap-2 text-sm font-bold leading-normal tracking-[0.015em] min-w-0">
              <span className="material-symbols-outlined">notifications</span>
            </button>
            <div 
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" 
              style={{ backgroundImage: `url("${user?.avatar}")` }}
            ></div>
          </div>
        </header>

        <div className="flex flex-1">
          {/* SIDEBAR */}
          <aside className="w-64 flex-shrink-0 p-4 border-r border-primary/20 dark:border-primary/30 hidden md:block">
            <div className="flex h-full flex-col justify-between">
              <div className="flex flex-col gap-4">
                <div className="flex gap-3 items-center">
                  <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" style={{ backgroundImage: `url("${user?.avatar}")` }}></div>
                  <div className="flex flex-col">
                    <h1 className="text-[#1b0d0d] dark:text-white text-base font-medium leading-normal">{user?.User_name || user?.name}</h1>
                    <p className="text-[#9a4c4c] dark:text-gray-400 text-sm font-normal leading-normal">{user?.email}</p>
                  </div>
                </div>
                <div className="flex flex-col gap-2 mt-4">
                  <div className="flex items-center gap-3 px-3 py-2 text-[#1b0d0d] dark:text-white cursor-pointer hover:bg-primary/20 dark:hover:bg-white/10 rounded-lg">
                    <span className="material-symbols-outlined">dashboard</span>
                    <p className="text-sm font-medium leading-normal">Dashboard</p>
                  </div>
                  <div className="flex items-center gap-3 px-3 py-2 rounded-lg bg-primary text-white">
                    <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>book</span>
                    <p className="text-sm font-medium leading-normal">My Courses</p>
                  </div>
                  <div className="flex items-center gap-3 px-3 py-2 text-[#1b0d0d] dark:text-white cursor-pointer hover:bg-primary/20 dark:hover:bg-white/10 rounded-lg">
                    <span className="material-symbols-outlined">search</span>
                    <p className="text-sm font-medium leading-normal">Browse Catalog</p>
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
                  onClick={() => navigate('/login')} 
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
              <div className="flex flex-col gap-2">
                <p className="text-[#1b0d0d] dark:text-white text-3xl font-black leading-tight tracking-[-0.033em]">Welcome back, {user?.User_name || user?.name}!</p>
                <p className="text-[#9a4c4c] dark:text-gray-400 text-base font-normal leading-normal">
                  You have completed <span className="font-bold text-primary">{completedCourses}</span> out of <span className="font-bold">{totalCourses}</span> courses ({globalProgress}%).
                </p>
              </div>
            </div>

            {/* TABS */}
            <div className="flex gap-2 p-1 overflow-x-auto mb-6">
              <button 
                onClick={() => setActiveTab('all')}
                className={`flex h-9 shrink-0 items-center justify-center gap-x-2 rounded-lg pl-4 pr-4 ${activeTab === 'all' ? 'bg-primary text-white' : 'bg-primary/20 dark:bg-white/10 text-[#1b0d0d] dark:text-white'}`}
              >
                <p className="text-sm font-medium leading-normal">All Courses</p>
              </button>
              <button 
                onClick={() => setActiveTab('in-progress')}
                className={`flex h-9 shrink-0 items-center justify-center gap-x-2 rounded-lg pl-4 pr-4 ${activeTab === 'in-progress' ? 'bg-primary text-white' : 'bg-primary/20 dark:bg-white/10 text-[#1b0d0d] dark:text-white'}`}
              >
                <p className="text-sm font-medium leading-normal">In Progress</p>
              </button>
              <button 
                onClick={() => setActiveTab('completed')}
                className={`flex h-9 shrink-0 items-center justify-center gap-x-2 rounded-lg pl-4 pr-4 ${activeTab === 'completed' ? 'bg-primary text-white' : 'bg-primary/20 dark:bg-white/10 text-[#1b0d0d] dark:text-white'}`}
              >
                <p className="text-sm font-medium leading-normal">Completed</p>
              </button>
            </div>

            {/* COURSES GRID */}
            <div className="grid grid-cols-1 gap-6">
              {courses.map(course => (
                <div key={course.id} className="flex flex-col gap-4 rounded-xl bg-background-light dark:bg-background-dark p-4 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] border border-primary/20 dark:border-primary/30">
                  <div className="flex flex-col md:flex-row items-start md:items-center gap-4">
                    <div 
                      className="w-full md:w-48 h-28 bg-center bg-no-repeat bg-cover rounded-lg flex-shrink-0" 
                      style={{ backgroundImage: `url("${course.image}")` }}
                    ></div>
                    <div className="flex-1 w-full">
                      <div className="flex justify-between items-start">
                        <div>
                          <span className={`text-xs font-semibold uppercase tracking-wider px-2 py-1 rounded-full`}>
                            {course.status}
                          </span>
                          <p className="text-[#1b0d0d] dark:text-white text-lg font-bold leading-tight mt-2">{course.title}</p>
                          <p className="text-[#9a4c4c] dark:text-gray-400 text-sm font-normal leading-normal">by {course.instructor}</p>
                        </div>
                        
                        {/* Desktop Buttons */}
                        <div className="hidden md:flex flex-col gap-2">
                          <button className="min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-medium leading-normal w-fit">
                            <span>{course.status === 'Completed' ? 'Review Course' : 'Continue Learning'}</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="text-sm italic text-gray-500">
                    <span>
                      {course.description}
                    </span>
                  </div>
                  {/* LESSONS LIST */}
                  <div className="border-t border-primary/20 dark:border-primary/30 pt-4">
                    <h4 className="text-sm font-bold text-[#1b0d0d] dark:text-white mb-3">Lessons</h4>
                    <ul className="space-y-2">
                      {course.lessons.map((lesson, idx) => (
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
                      ))}
                    </ul>
                  </div>
                  
                  {/* Mobile Buttons */}
                  <div className="md:hidden flex flex-col gap-2 mt-2">
                    <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-medium leading-normal w-full">
                      <span>{course.status === 'Completed' ? 'Review Course' : 'Continue Learning'}</span>
                    </button>
                    <button 
                      onClick={() => actions.handleCheckPrerequisites(course.courseId || course.id)}
                      className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-9 px-4 bg-transparent border border-primary/30 text-primary text-sm font-medium leading-normal w-full"
                    >
                      Check Requirements
                    </button>
                  </div>
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