import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useHomeController } from '../hooks/useHomeController';

/**
 * HomePage (View)
 * Displays the public course catalog.
 */
const HomePage = () => {
  const { courses, loading, searchQuery, modalState, user, actions } = useHomeController();
  const navigate = useNavigate(); 

  // --- Modal Content Renderer ---
  const renderModalContent = () => {
    switch (modalState.type) {
      case 'login_prompt':
        return (
          <div className="text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-900/30 mb-4">
              <span className="material-symbols-outlined text-blue-600 dark:text-blue-400">lock</span>
            </div>
            <h3 className="text-lg font-bold text-text-light dark:text-text-dark mb-2">Login Required</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
              You must be logged in to check your eligibility for this course.
            </p>
            <div className="flex gap-3 justify-center">
              <button onClick={actions.closeModal} className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                Cancel
              </button>
              <button onClick={() => navigate('/login')} className="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors">
                Log In
              </button>
            </div>
          </div>
        );
      case 'missing':
        return (
          <div className="text-left">
            <div className="flex items-center gap-3 mb-4 text-amber-600 dark:text-amber-500">
              <span className="material-symbols-outlined text-3xl">warning</span>
              <h3 className="text-lg font-bold text-text-light dark:text-text-dark">Prerequisites Missing</h3>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
              You need to complete the following courses before enrolling:
            </p>
            <ul className="bg-amber-50 dark:bg-amber-900/20 border border-amber-100 dark:border-amber-800/30 rounded-lg p-4 mb-6 space-y-2">
              {modalState.data?.map((req, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm text-amber-900 dark:text-amber-100">
                  <span className="material-symbols-outlined text-base mt-0.5">menu_book</span>
                  <span>{req.Title}</span>
                </li>
              ))}
            </ul>
            <div className="flex justify-end">
              <button onClick={actions.closeModal} className="px-4 py-2 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity">
                Understood
              </button>
            </div>
          </div>
        );
      case 'success':
        return (
          <div className="text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30 mb-4">
              <span className="material-symbols-outlined text-green-600 dark:text-green-400">check_circle</span>
            </div>
            <h3 className="text-lg font-bold text-text-light dark:text-text-dark mb-2">You're Eligible!</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
              You have met all the prerequisites for this course. You can enroll now.
            </p>
            <div className="flex gap-3 justify-center">
              <button onClick={actions.closeModal} className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                Close
              </button>
              <button onClick={() => navigate(`/course/${modalState.courseId}`)} className="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors">
                View Course
              </button>
            </div>
          </div>
        );
      default:
        return (
          <div className="text-center">
            <p>Something went wrong. Please try again.</p>
            <button onClick={actions.closeModal} className="mt-4 px-4 py-2 bg-primary text-white rounded-lg text-sm">Close</button>
          </div>
        );
    }
  };

  // Determine Dashboard Link based on user role (IFlag = Instructor)
  const dashboardLink = user?.IFlag ? '/instructor' : '/dashboard';

  return (
    <div className="relative flex min-h-screen w-full flex-col overflow-x-hidden bg-[#fef2f2] dark:bg-[#1f2937] font-sans text-[#1f2937] dark:text-[#f9fafb]">
      
      {/* --- MODAL OVERLAY --- */}
      {modalState.isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-in fade-in duration-200">
          <div 
            className="bg-white dark:bg-[#2a2f3e] rounded-2xl shadow-xl w-full max-w-md p-6 relative animate-in zoom-in-95 duration-200 border border-gray-100 dark:border-gray-700"
            onClick={(e) => e.stopPropagation()}
          >
            <button 
              onClick={actions.closeModal}
              className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors"
            >
              <span className="material-symbols-outlined">close</span>
            </button>
            {renderModalContent()}
          </div>
        </div>
      )}

      <div className="layout-container flex h-full grow flex-col">
        <div className="flex flex-1 justify-center px-4 sm:px-8 md:px-16 lg:px-24 xl:px-40 py-5">
          <div className="layout-content-container flex w-full max-w-7xl flex-1 flex-col">
            
            {/* --- HEADER --- */}
            <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-[#fee2e2] dark:border-[#4b5563] px-6 lg:px-10 py-3">
              <div className="flex items-center gap-8">
                <div className="flex items-center gap-4 text-[#1f2937] dark:text-[#f9fafb] cursor-pointer" onClick={() => navigate('/')}>
                  <div className="size-6 text-[#dc2626]">
                    <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                      <path d="M6 6H42L36 24L42 42H6L12 24L6 6Z" fill="currentColor"></path>
                    </svg>
                  </div>
                  <h2 className="text-lg font-bold leading-tight tracking-[-0.015em] text-[#1f2937] dark:text-[#f9fafb]">
                    MUDemy
                  </h2>
                </div>
                <div className="hidden lg:flex items-center gap-9">
                  <a className="text-sm font-medium leading-normal text-[#1f2937] dark:text-[#f9fafb] hover:text-[#dc2626] dark:hover:text-[#dc2626]" href="#">Categories</a>
                  <a className="text-sm font-medium leading-normal text-[#1f2937] dark:text-[#f9fafb] hover:text-[#dc2626] dark:hover:text-[#dc2626]" href="#">Become an Instructor</a>
                </div>
              </div>
              
              <div className="flex flex-1 justify-end items-center gap-4">
                <label className="hidden md:flex flex-col min-w-40 !h-10 max-w-64">
                  <div className="flex w-full flex-1 items-stretch rounded-lg h-full">
                    <div className="text-[#6b7280] dark:text-[#d1d5db] flex border-none bg-[#fee2e2] dark:bg-[#4b5563] items-center justify-center pl-4 rounded-l-lg border-r-0">
                      <span className="material-symbols-outlined" style={{ fontSize: '20px' }}> search </span>
                    </div>
                    <input 
                      className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#1f2937] dark:text-[#f9fafb] focus:outline-0 focus:ring-0 border-none bg-[#fee2e2] dark:bg-[#4b5563] focus:border-none h-full placeholder:text-[#6b7280] dark:placeholder:text-[#d1d5db] px-4 rounded-l-none border-l-0 pl-2 text-base font-normal leading-normal" 
                      placeholder="Search" 
                      value={searchQuery}
                      onChange={actions.handleSearchChange}
                    />
                  </div>
                </label>

                {/* --- CONDITIONAL HEADER CONTENT --- */}
                {user ? (
                  <div className="flex items-center gap-3">
                    <button 
                      onClick={() => navigate(dashboardLink)}
                      className="hidden sm:block text-sm font-bold text-[#1f2937] dark:text-[#f9fafb] hover:text-primary transition-colors"
                    >
                      Dashboard
                    </button>
                    
                    <div className="relative group cursor-pointer" onClick={() => navigate(dashboardLink)}>
                      <div 
                        className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10 border border-gray-200 dark:border-gray-600" 
                        style={{ backgroundImage: `url("${user.Avatar || 'https://lh3.googleusercontent.com/aida-public/AB6AXuCLUFjvCwwhv-6mo2wiWpF_punDE3M5LEdO85YAFd7tL8wEbtGgdOWlA21Ii07ovkUQWpuPSKM3Q3JsfjasIOo95MgP52JfYv224flbTFzfz_yQ6UiaAkymnDgLAm7HZSfNB_EpUcyQ00AUwe3T_8V0S6OVcUQgQKU5sggQoOQoLVL6ESZKvZJESy1KANLcmcfxP7NzReCVKLpWRBWdARO9fKFbPqtamkkfhUjRVmzoiYMldothNvc8AeZBFaDcaLUiH_asXQMLOkE'}")` }}
                      ></div>
                    </div>

                    <button 
                      onClick={actions.handleLogout}
                      className="flex h-10 w-10 items-center justify-center rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500 dark:text-gray-400 transition-colors"
                      title="Log Out"
                    >
                      <span className="material-symbols-outlined">logout</span>
                    </button>
                  </div>
                ) : (
                  <div className="flex gap-2">
                    <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#dc2626] text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-red-700 dark:hover:bg-red-500 transition-colors">
                      <span className="truncate">Sign Up</span>
                    </button>
                    <button 
                      onClick={() => navigate('/login')}
                      className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#ffffff] dark:bg-[#374151] border border-[#fee2e2] dark:border-[#4b5563] text-[#1f2937] dark:text-[#f9fafb] text-sm font-bold leading-normal tracking-[0.015em] hover:bg-[#fee2e2] dark:hover:bg-[#4b5563] transition-colors"
                    >
                      <span className="truncate">Log In</span>
                    </button>
                  </div>
                )}
                
                {/* Cart Icon (Always visible) */}
                <button 
                  onClick={() => navigate('/checkout')}
                  className="flex max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 bg-[#ffffff] dark:bg-[#374151] border border-[#fee2e2] dark:border-[#4b5563] text-[#1f2937] dark:text-[#f9fafb] gap-2 text-sm font-bold leading-normal tracking-[0.015em] min-w-0 px-2.5 hover:bg-[#fee2e2] dark:hover:bg-[#4b5563] transition-colors"
                >
                  <span className="material-symbols-outlined" style={{ fontSize: '20px' }}> shopping_cart </span>
                </button>
              </div>
            </header>

            {/* --- MAIN CONTENT --- */}
            <main className="flex flex-col gap-10 md:gap-12 pt-8 md:pt-12">
              
              {/* Search & Filter Section */}
              <section className="flex flex-col gap-6 px-4">
                <h1 className="text-3xl font-bold leading-tight tracking-[-0.015em] text-red-900 dark:text-red-200">Discover Courses</h1>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {/* ... Filters (Same as before) ... */}
                  <label className="flex flex-col min-w-40 col-span-1 md:col-span-2">
                    <div className="flex w-full flex-1 items-stretch rounded-lg h-12 shadow-sm">
                      <div className="text-gray-400 dark:text-gray-500 flex border border-[#fee2e2] dark:border-[#4b5563] bg-[#ffffff] dark:bg-[#374151] items-center justify-center pl-4 rounded-l-lg border-r-0">
                        <span className="material-symbols-outlined" style={{ fontSize: '20px' }}> search </span>
                      </div>
                      <input 
                        className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-none text-[#1f2937] dark:text-[#f9fafb] focus:outline-0 focus:ring-2 focus:ring-inset focus:ring-[#dc2626] border-y border-[#fee2e2] dark:border-[#4b5563] bg-[#ffffff] dark:bg-[#374151] h-full placeholder:text-[#6b7280] dark:placeholder:text-[#d1d5db] px-4 text-base font-normal leading-normal" 
                        placeholder="Search for anything..." 
                        value={searchQuery}
                        onChange={actions.handleSearchChange}
                      />
                      <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-r-lg h-12 px-5 bg-[#dc2626] text-white text-base font-bold leading-normal tracking-[0.015em] hover:bg-red-700 dark:hover:bg-red-500 transition-colors">
                        <span className="truncate">Search</span>
                      </button>
                    </div>
                  </label>
                  {/* ... Dropdowns (Same as before) ... */}
                  <div className="relative h-12">
                    <select className="form-select w-full h-full rounded-lg border border-[#fee2e2] dark:border-[#4b5563] bg-[#ffffff] dark:bg-[#374151] text-[#1f2937] dark:text-[#f9fafb] focus:border-[#dc2626] focus:ring-[#dc2626] shadow-sm">
                      <option>All Categories</option>
                      <option>Development</option>
                      <option>Business</option>
                      <option>Design</option>
                      <option>Marketing</option>
                    </select>
                  </div>
                  <div className="relative h-12">
                    <select className="form-select w-full h-full rounded-lg border border-[#fee2e2] dark:border-[#4b5563] bg-[#ffffff] dark:bg-[#374151] text-[#1f2937] dark:text-[#f9fafb] focus:border-[#dc2626] focus:ring-[#dc2626] shadow-sm">
                      <option>Any Difficulty</option>
                      <option>Beginner</option>
                      <option>Intermediate</option>
                      <option>Advanced</option>
                    </select>
                  </div>
                </div>
              </section>

              {/* Courses Grid Section */}
              <section className="px-4">
                <h2 className="text-red-900 dark:text-red-200 text-[22px] font-bold leading-tight tracking-[-0.015em] pb-4">Featured Courses</h2>
                
                {loading ? (
                  <div className="text-center py-10">Loading courses...</div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {courses.map(course => (
                      <div key={course.id} className="flex flex-col gap-4 rounded-lg bg-[#ffffff] dark:bg-[#374151] shadow-md overflow-hidden transition-shadow hover:shadow-lg hover:ring-2 hover:ring-[#dc2626]">
                        <div 
                          className="w-full bg-center bg-no-repeat aspect-video bg-cover" 
                          style={{ backgroundImage: `url("${course.image}")` }}
                          aria-label={course.title}
                        ></div>
                        <div className="flex flex-col flex-1 p-4 pt-0 gap-3">
                          <div className="flex gap-2 flex-wrap pt-4">
                            <span className={`text-xs font-semibold px-2 py-1 rounded-full ${course.badgeColor}`}>
                              {course.level}
                            </span>
                            <span className="text-xs font-semibold px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-full">
                              {course.category}
                            </span>
                          </div>
                          <h3 className="text-[#1f2937] dark:text-[#f9fafb] text-lg font-bold leading-tight">
                            {course.title}
                          </h3>
                          <p className="text-[#6b7280] dark:text-[#d1d5db] text-sm font-normal leading-normal line-clamp-2">
                            {course.description}
                          </p>
                          {/* <p className="text-[#6b7280] dark:text-[#d1d5db] text-sm font-normal">
                            By <span className="font-medium text-[#1f2937] dark:text-[#f9fafb]">{course.instructor_name}</span>
                          </p> */}
                          
                          <div className="mt-2 flex gap-2">
                            {/* VIEW COURSE BUTTON */}
                            <button 
                              onClick={() => navigate(`/course/${course.id}`)}
                              className="flex-1 cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#dc2626] text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-red-700 dark:hover:bg-red-500 transition-colors"
                            >
                              View
                            </button>

                            {/* CHECK REQUIREMENTS BUTTON */}
                            <button 
                              onClick={() => actions.handleCheckPrerequisites(course.id)}
                              className="flex-1 cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-transparent border border-[#dc2626] text-[#dc2626] text-sm font-bold leading-normal tracking-[0.015em] hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                            >
                              Check Req
                            </button>
                          </div>

                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </section>
            </main>

            {/* --- FOOTER --- */}
            <footer className="mt-16 border-t border-[#fee2e2] dark:border-[#4b5563] py-8 text-[#6b7280] dark:text-[#d1d5db]">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-8 px-4">
                <div className="flex flex-col gap-4">
                  <h3 className="font-bold text-[#1f2937] dark:text-[#f9fafb]">MUDemy</h3>
                  <a className="text-sm hover:text-[#dc2626] dark:hover:text-[#dc2626]" href="#">About Us</a>
                  <a className="text-sm hover:text-[#dc2626] dark:hover:text-[#dc2626]" href="#">Careers</a>
                  <a className="text-sm hover:text-[#dc2626] dark:hover:text-[#dc2626]" href="#">Blog</a>
                </div>
                {/* ... other footer columns ... */}
              </div>
              <div className="mt-8 text-center text-sm">
                <p>© 2024 MUDemy, Inc. All rights reserved.</p>
              </div>
            </footer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;