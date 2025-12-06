import React from 'react';
import { useCourseDetailController } from '../hooks/useCourseDetailController';
import { useNavigate } from 'react-router-dom';

const CourseDetailPage = () => {
  const { course, loading, expandedModules, toggleModule } = useCourseDetailController();
  const navigate = useNavigate();

  if (loading || !course) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background-light dark:bg-background-dark text-text-light-primary dark:text-text-dark-primary">
        Loading...
      </div>
    );
  }

  return (
    <div className="relative flex h-auto min-h-screen w-full flex-col group/design-root overflow-x-hidden bg-background-light dark:bg-background-dark font-display text-text-light-primary dark:text-text-dark-primary">
      
      {/* HEADER (Reused from HTML) */}
      <header className="sticky top-0 z-50 w-full flex items-center justify-between whitespace-nowrap border-b border-solid border-border-light dark:border-border-dark px-6 md:px-10 py-3 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-sm">
        <div className="flex items-center gap-8 cursor-pointer" onClick={() => navigate('/')}>
          <div className="flex items-center gap-2 text-text-light-primary dark:text-text-dark-primary">
            <span className="material-symbols-outlined text-primary text-2xl">school</span>
            <h2 className="text-xl font-bold leading-tight tracking-[-0.015em]">MUDemy</h2>
          </div>
          <div className="hidden md:flex items-center gap-9">
            <a className="text-sm font-medium leading-normal hover:text-primary dark:hover:text-primary" href="#">Categories</a>
          </div>
        </div>
        <div className="flex flex-1 justify-end gap-4 md:gap-6 items-center">
          <label className="hidden md:flex flex-col min-w-40 !h-10 max-w-64">
            <div className="flex w-full flex-1 items-stretch rounded-lg h-full">
              <div className="text-text-light-secondary dark:text-text-dark-secondary flex border border-border-light dark:border-border-dark bg-transparent items-center justify-center pl-3 rounded-l-lg border-r-0">
                <span className="material-symbols-outlined">search</span>
              </div>
              <input className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-sm focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-border-light dark:border-border-dark bg-transparent focus:border-primary/50 h-full placeholder:text-text-light-secondary dark:placeholder:text-text-dark-secondary px-4 rounded-l-none border-l-0 pl-2 font-normal leading-normal" placeholder="Search for anything" />
            </div>
          </label>
          <div className="flex gap-2">
            <button className="flex max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 w-10 border border-border-light dark:border-border-dark hover:bg-black/5 dark:hover:bg-white/5 gap-2 text-sm font-bold leading-normal tracking-[0.015em] min-w-0">
              <span className="material-symbols-outlined text-xl">shopping_cart</span>
            </button>
            <button className="flex max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 w-10 border border-border-light dark:border-border-dark hover:bg-black/5 dark:hover:bg-white/5 gap-2 text-sm font-bold leading-normal tracking-[0.015em] min-w-0">
              <span className="material-symbols-outlined text-xl">notifications</span>
            </button>
          </div>
          <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" style={{ backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuC7JmGVLYlbpPv4yj9IrVm5-Y6b7lOh7iXiIZXRwwcWojeGXWrX-2i0A5MSI4jW71LMOTro7cCJO8sr6nQN2k70uHa5sKdYZo-H2sBBOPZEz99Ti1RWzqrWLZO9QNIvxDTarcUge13S80LCagnQYj8RZZXDyaAPbSqhhwYY6JWOawqNt4uuAW5cp4zCcWZmFI3syPvQtrO_XHnhIx6B2Tw2_BXru_7FEk-1VlwoxIhbp1Yp3Rr-c8eZX5Q10iIl1lD5iE-DUNIE6Ow")' }}></div>
        </div>
      </header>

      <main className="layout-container flex h-full grow flex-col">
        <div className="px-6 md:px-10 lg:px-20 xl:px-40 flex flex-1 justify-center py-5 md:py-8">
          <div className="layout-content-container w-full max-w-[1280px]">
            
            {/* Breadcrumb */}
            <div className="flex flex-wrap gap-2 mb-6">
              <a className="text-primary text-sm font-medium leading-normal" href="#">Home</a>
              <span className="text-text-light-secondary dark:text-text-dark-secondary text-sm font-medium leading-normal">/</span>
              <a className="text-primary text-sm font-medium leading-normal" href="#">Databases</a>
              <span className="text-text-light-secondary dark:text-text-dark-secondary text-sm font-medium leading-normal">/</span>
              <a className="text-primary text-sm font-medium leading-normal" href="#">SQL</a>
              <span className="text-text-light-secondary dark:text-text-dark-secondary text-sm font-medium leading-normal">/</span>
              <span className="text-text-light-primary dark:text-text-dark-primary text-sm font-medium leading-normal">{course.title}</span>
            </div>

            <div className="flex flex-col lg:flex-row gap-8">
              
              {/* LEFT COLUMN */}
              <div className="w-full lg:w-2/3 flex flex-col gap-6">
                
                {/* Title & Stats */}
                <div className="flex flex-col gap-3">
                  <h1 className="text-3xl md:text-4xl font-black leading-tight tracking-[-0.033em]">{course.title}</h1>
                  <p className="text-base md:text-lg font-normal leading-normal text-text-light-secondary dark:text-text-dark-secondary">
                    {course.description}
                  </p>
                </div>

                <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
                  <div className="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-yellow-400/20 px-3">
                    <p className="text-yellow-700 dark:text-yellow-400 text-sm font-medium leading-normal">Bestseller</p>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="font-bold text-yellow-500">{course.rating}</span>
                    <div className="flex text-yellow-400">
                      {[...Array(5)].map((_, i) => (
                        <span key={i} className="material-symbols-outlined !text-base" style={{ fontVariationSettings: "'FILL' 1" }}>star</span>
                      ))}
                    </div>
                    <a className="text-sm text-primary underline" href="#">({course.ratingCount} ratings)</a>
                    <span className="text-sm text-text-light-secondary dark:text-text-dark-secondary">{course.studentCount} students</span>
                  </div>
                </div>

                <p className="text-sm">Created by <a className="font-bold text-primary underline" href="#">{course.author.name}</a></p>
                
                <div className="flex flex-wrap items-center gap-3">
                  <div className="flex items-center gap-2 text-sm"><span className="material-symbols-outlined !text-lg">update</span> <span>Last updated {course.lastUpdated}</span></div>
                  <div className="flex items-center gap-2 text-sm"><span className="material-symbols-outlined !text-lg">language</span> <span>{course.language}</span></div>
                  <div className="flex items-center gap-2 text-sm"><span className="material-symbols-outlined !text-lg">closed_caption</span> <span>{course.subtitles}</span></div>
                </div>

                {/* Tabs / Navigation */}
                <div className="mt-4">
                  <div className="flex border-b border-border-light dark:border-border-dark px-0 gap-8">
                    {['Description', 'Curriculum', 'Instructor', 'Reviews'].map((tab, idx) => (
                      <a key={tab} href={`#${tab.toLowerCase()}`} className={`flex flex-col items-center justify-center border-b-[3px] pb-3 pt-2 ${idx === 0 ? 'border-b-primary text-text-light-primary dark:text-text-dark-primary' : 'border-b-transparent text-text-light-secondary dark:text-text-dark-secondary'}`}>
                        <p className="text-base font-bold leading-normal tracking-[0.015em]">{tab}</p>
                      </a>
                    ))}
                  </div>

                  {/* Description Content */}
                  <div className="pt-8">
                    <h2 className="text-2xl font-bold mb-4 text-primary">Course Description</h2>
                    <p className="text-text-light-secondary dark:text-text-dark-secondary leading-relaxed">
                      This course is designed to take you from a complete novice to a confident SQL practitioner. You will learn to write complex queries, join multiple tables, use subqueries, and perform data analysis.
                    </p>
                  </div>

                  {/* Curriculum Accordion */}
                  <div className="pt-8" id="curriculum">
                    <h2 className="text-2xl font-bold mb-4 text-primary">Curriculum</h2>
                    <div className="flex flex-col gap-2">
                      {course.curriculum.map((module, index) => (
                        <div key={index} className={`border border-border-light dark:border-border-dark rounded-lg ${expandedModules[index] ? 'bg-black/5 dark:bg-white/5' : ''}`}>
                          <button 
                            className="w-full flex justify-between items-center p-4 text-left font-semibold"
                            onClick={() => toggleModule(index)}
                          >
                            <span className="font-bold">{module.title}</span>
                            <span className="material-symbols-outlined">{expandedModules[index] ? 'expand_less' : 'expand_more'}</span>
                          </button>
                          {expandedModules[index] && (
                            <div className="px-4 pb-4 text-text-light-secondary dark:text-text-dark-secondary">
                              <ul className="list-disc pl-5 space-y-2">
                                {module.lessons.map((lesson, lIdx) => (
                                  <li key={lIdx}>{lesson}</li>
                                ))}
                                {module.lessons.length === 0 && <li>No preview available</li>}
                              </ul>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Instructor */}
                  <div className="pt-8" id="instructor">
                    <h2 className="text-2xl font-bold mb-4 text-primary">Instructor</h2>
                    <div className="flex flex-col sm:flex-row gap-6 items-start">
                      <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-24 shrink-0" style={{ backgroundImage: `url("${course.author.image}")` }}></div>
                      <div>
                        <h3 className="text-xl font-bold">{course.author.name}</h3>
                        <p className="text-primary font-medium">{course.author.role}</p>
                        <p className="mt-2 text-text-light-secondary dark:text-text-dark-secondary">{course.author.bio}</p>
                      </div>
                    </div>
                  </div>

                </div>
              </div>

              {/* RIGHT COLUMN (Sticky Sidebar) */}
              <div className="w-full lg:w-1/3">
                <div className="sticky top-24">
                  <div className="border border-border-light dark:border-border-dark rounded-xl shadow-lg bg-background-light dark:bg-background-dark overflow-hidden">
                    <div className="relative aspect-video">
                      <div className="absolute inset-0 bg-center bg-no-repeat bg-cover" style={{ backgroundImage: `url("${course.previewImage}")` }}></div>
                      <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                        <button className="bg-white/80 rounded-full h-16 w-16 flex items-center justify-center text-primary backdrop-blur-sm">
                          <span className="material-symbols-outlined !text-5xl">play_arrow</span>
                        </button>
                      </div>
                    </div>
                    <div className="p-6 flex flex-col gap-4">
                      <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-primary">${course.price}</p>
                        <p className="text-lg line-through text-text-light-secondary dark:text-text-dark-secondary">${course.originalPrice}</p>
                        <p className="text-lg text-red-500">{course.discount}</p>
                      </div>
                      <div className="flex flex-col gap-3">
                        <button className="w-full flex cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 bg-primary text-white gap-2 text-base font-bold leading-normal tracking-[0.015em] text-center hover:bg-red-700 dark:hover:bg-red-500">
                          Add to Cart
                        </button>
                        <button className="w-full flex cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 bg-transparent text-primary dark:text-primary border border-primary dark:border-primary gap-2 text-base font-bold leading-normal tracking-[0.015em] text-center hover:bg-primary/10">
                          Buy Course
                        </button>
                      </div>
                      <p className="text-xs text-center text-text-light-secondary dark:text-text-dark-secondary">30-Day Money-Back Guarantee</p>
                      <div className="border-t border-border-light dark:border-border-dark pt-4">
                        <h3 className="font-bold mb-2">What you'll learn:</h3>
                        <ul className="space-y-2">
                          {course.whatYouWillLearn.map((item, idx) => (
                            <li key={idx} className="flex items-start gap-3">
                              <span className="material-symbols-outlined text-primary !text-xl mt-0.5">check</span>
                              <span className="text-sm">{item}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default CourseDetailPage;