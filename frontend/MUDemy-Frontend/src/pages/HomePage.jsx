import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useHomeController } from '../hooks/useHomeController';

/**
 * HomePage (View)
 * Displays the landing page using data from the Controller.
 */
const HomePage = () => {
  const { courses, loading, searchQuery, handleSearchChange } = useHomeController();
  const navigate = useNavigate(); // Hook for navigation

  return (
    <div className="relative flex min-h-screen w-full flex-col overflow-x-hidden bg-[#fef2f2] dark:bg-[#1f2937] font-sans text-[#1f2937] dark:text-[#f9fafb]">
      
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
                      defaultValue=""
                    />
                  </div>
                </label>
                <div className="flex gap-2">
                  <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#dc2626] text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-red-700 dark:hover:bg-red-500 transition-colors">
                    <span className="truncate">Sign Up</span>
                  </button>
                  {/* UPDATED: Added onClick handler for navigation */}
                  <button 
                    onClick={() => navigate('/login')}
                    className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#ffffff] dark:bg-[#374151] border border-[#fee2e2] dark:border-[#4b5563] text-[#1f2937] dark:text-[#f9fafb] text-sm font-bold leading-normal tracking-[0.015em] hover:bg-[#fee2e2] dark:hover:bg-[#4b5563] transition-colors"
                  >
                    <span className="truncate">Log In</span>
                  </button>
                  <button className="flex max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 bg-[#ffffff] dark:bg-[#374151] border border-[#fee2e2] dark:border-[#4b5563] text-[#1f2937] dark:text-[#f9fafb] gap-2 text-sm font-bold leading-normal tracking-[0.015em] min-w-0 px-2.5 hover:bg-[#fee2e2] dark:hover:bg-[#4b5563] transition-colors">
                    <span className="material-symbols-outlined" style={{ fontSize: '20px' }}> shopping_cart </span>
                  </button>
                </div>
              </div>
            </header>

            {/* --- MAIN CONTENT --- */}
            <main className="flex flex-col gap-10 md:gap-12 pt-8 md:pt-12">
              
              {/* Search & Filter Section */}
              <section className="flex flex-col gap-6 px-4">
                <h1 className="text-3xl font-bold leading-tight tracking-[-0.015em] text-red-900 dark:text-red-200">Discover Courses</h1>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <label className="flex flex-col min-w-40 col-span-1 md:col-span-2">
                    <div className="flex w-full flex-1 items-stretch rounded-lg h-12 shadow-sm">
                      <div className="text-gray-400 dark:text-gray-500 flex border border-[#fee2e2] dark:border-[#4b5563] bg-[#ffffff] dark:bg-[#374151] items-center justify-center pl-4 rounded-l-lg border-r-0">
                        <span className="material-symbols-outlined" style={{ fontSize: '20px' }}> search </span>
                      </div>
                      <input 
                        className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-none text-[#1f2937] dark:text-[#f9fafb] focus:outline-0 focus:ring-2 focus:ring-inset focus:ring-[#dc2626] border-y border-[#fee2e2] dark:border-[#4b5563] bg-[#ffffff] dark:bg-[#374151] h-full placeholder:text-[#6b7280] dark:placeholder:text-[#d1d5db] px-4 text-base font-normal leading-normal" 
                        placeholder="Search for anything..." 
                        value={searchQuery}
                        onChange={handleSearchChange}
                      />
                      <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-r-lg h-12 px-5 bg-[#dc2626] text-white text-base font-bold leading-normal tracking-[0.015em] hover:bg-red-700 dark:hover:bg-red-500 transition-colors">
                        <span className="truncate">Search</span>
                      </button>
                    </div>
                  </label>
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
                          <p className="text-[#6b7280] dark:text-[#d1d5db] text-sm font-normal">
                            By <span className="font-medium text-[#1f2937] dark:text-[#f9fafb]">{course.author}</span>
                          </p>
                          <button 
                            onClick={() => navigate(`/course/${course.id}`)}
                            className="flex mt-2 min-w-[84px] w-full max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#dc2626] text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-red-700 dark:hover:bg-red-500 transition-colors"
                          >
                            <span className="truncate">View Course</span>
                          </button>
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
                <div className="flex flex-col gap-4">
                  <h3 className="font-bold text-[#1f2937] dark:text-[#f9fafb]">Support</h3>
                  <a className="text-sm hover:text-[#dc2626] dark:hover:text-[#dc2626]" href="#">Help Center</a>
                  <a className="text-sm hover:text-[#dc2626] dark:hover:text-[#dc2626]" href="#">Contact Us</a>
                  <a className="text-sm hover:text-[#dc2626] dark:hover:text-[#dc2626]" href="#">Terms of Service</a>
                </div>
                <div className="flex flex-col gap-4">
                  <h3 className="font-bold text-[#1f2937] dark:text-[#f9fafb]">Categories</h3>
                  <a className="text-sm hover:text-[#dc2626] dark:hover:text-[#dc2626]" href="#">Development</a>
                  <a className="text-sm hover:text-[#dc2626] dark:hover:text-[#dc2626]" href="#">Business</a>
                  <a className="text-sm hover:text-[#dc2626] dark:hover:text-[#dc2626]" href="#">Design</a>
                </div>
                <div className="flex flex-col gap-4">
                  <h3 className="font-bold text-[#1f2937] dark:text-[#f9fafb]">Follow Us</h3>
                  <div className="flex gap-4">
                    <a className="hover:text-[#dc2626] dark:hover:text-[#dc2626]" href="#">
                      <svg aria-hidden="true" className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                        <path clipRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" fillRule="evenodd"></path>
                      </svg>
                    </a>
                  </div>
                </div>
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