import React from 'react';
import { useCourseDetailController } from '../hooks/useCourseDetailController';
import { useNavigate } from 'react-router-dom';
import logoImg from '../assets/logo.png'; // Imported logo

const CourseDetailPage = () => {
  const { course, loading, expandedModules, toggleModule } = useCourseDetailController();
  const navigate = useNavigate();

  if (loading || !course) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background-light dark:bg-background-dark text-text-light-primary dark:text-text-dark-primary">
        <span className="material-symbols-outlined animate-spin text-4xl text-primary">progress_activity</span>
      </div>
    );
  }

  return (
    <div className="relative flex h-auto min-h-screen w-full flex-col group/design-root overflow-x-hidden bg-background-light dark:bg-background-dark font-display text-text-light-primary dark:text-text-dark-primary">
      
      {/* HEADER */}
      <header className="sticky top-0 z-50 w-full flex items-center justify-between whitespace-nowrap border-b border-solid border-border-light dark:border-border-dark px-6 md:px-10 py-3 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-sm">
        <div className="flex items-center gap-8 cursor-pointer" onClick={() => navigate('/')}>
          <div className="flex items-center gap-2 text-text-light-primary dark:text-text-dark-primary">
            <img src={logoImg} alt="MUDemy Logo" className="h-8 w-auto"/>
            <h2 className="text-xl font-bold leading-tight tracking-[-0.015em]">MUDemy</h2>
          </div>
        </div>
        
        {/* Simple Header Actions */}
        <div className="flex gap-2">
          <button className="flex h-10 w-10 items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/5">
            <span className="material-symbols-outlined text-xl">shopping_cart</span>
          </button>
        </div>
      </header>

      <main className="layout-container flex h-full grow flex-col">
        <div className="px-6 md:px-10 lg:px-20 xl:px-40 flex flex-1 justify-center py-5 md:py-8">
          <div className="layout-content-container w-full max-w-[1280px]">
            
            {/* Breadcrumb */}
            <div className="flex flex-wrap gap-2 mb-6 text-sm">
              <a className="text-primary font-medium hover:underline" href="/">Home</a>
              <span className="text-text-light-secondary dark:text-text-dark-secondary">/</span>
              <span className="text-text-light-secondary dark:text-text-dark-secondary">Courses</span>
              <span className="text-text-light-secondary dark:text-text-dark-secondary">/</span>
              <span className="text-text-light-primary dark:text-text-dark-primary font-medium">{course.title}</span>
            </div>

            <div className="flex flex-col lg:flex-row gap-8">
              
              {/* LEFT COLUMN: Content */}
              <div className="w-full lg:w-2/3 flex flex-col gap-6">
                
                {/* Title & Description */}
                <div className="flex flex-col gap-3">
                  <h1 className="text-3xl md:text-4xl font-black leading-tight tracking-[-0.033em]">{course.title}</h1>
                  <p className="text-base md:text-lg font-normal leading-normal text-text-light-secondary dark:text-text-dark-secondary">
                    {course.description}
                  </p>
                </div>

                {/* Badges & Stats */}
                <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
                  <span className="px-3 py-1 rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300 text-xs font-bold uppercase tracking-wider">
                    {course.level}
                  </span>
                  <div className="flex items-center gap-1.5 text-yellow-500">
                    <span className="font-bold">{course.rating}</span>
                    <span className="material-symbols-outlined text-base" style={{ fontVariationSettings: "'FILL' 1" }}>star</span>
                    <span className="text-sm text-text-light-secondary dark:text-text-dark-secondary">({course.ratingCount} ratings)</span>
                  </div>
                  <span className="text-sm text-text-light-secondary dark:text-text-dark-secondary">{course.studentCount} students</span>
                </div>

                <p className="text-sm">Created by <span className="font-bold text-primary">{course.author.name}</span></p>
                
                <div className="flex flex-wrap items-center gap-4 text-sm text-text-light-secondary dark:text-text-dark-secondary">
                  <div className="flex items-center gap-1"><span className="material-symbols-outlined text-lg">language</span> <span>{course.language}</span></div>
                  <div className="flex items-center gap-1"><span className="material-symbols-outlined text-lg">update</span> <span>Last updated {course.lastUpdated}</span></div>
                </div>

                {/* Tabs */}
                <div className="mt-4 border-b border-border-light dark:border-border-dark">
                  <div className="flex gap-8">
                    <button className="border-b-[3px] border-primary pb-3 pt-2 font-bold text-text-light-primary dark:text-text-dark-primary">Description</button>
                    <button className="border-b-[3px] border-transparent pb-3 pt-2 font-bold text-text-light-secondary dark:text-text-dark-secondary hover:text-primary transition-colors">Curriculum</button>
                    <button className="border-b-[3px] border-transparent pb-3 pt-2 font-bold text-text-light-secondary dark:text-text-dark-secondary hover:text-primary transition-colors">Instructor</button>
                  </div>
                </div>

                {/* Course Description Body */}
                <div className="pt-6">
                  <h2 className="text-2xl font-bold mb-4 text-primary">About this course</h2>
                  <p className="leading-relaxed text-text-light-primary dark:text-text-dark-primary">
                    {course.description}
                  </p>
                  
                  {/* Prerequisites Section */}
                  {course.prerequisites && course.prerequisites.length > 0 && (
                    <div className="mt-6 p-4 bg-amber-50 dark:bg-amber-900/10 border border-amber-100 dark:border-amber-800/30 rounded-lg">
                      <h3 className="font-bold text-amber-800 dark:text-amber-200 mb-2">Prerequisites</h3>
                      <ul className="list-disc pl-5 text-sm text-amber-900 dark:text-amber-100">
                        {course.prerequisites.map((req, idx) => (
                          <li key={idx}>{req}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* Curriculum Accordion */}
                <div className="pt-8">
                  <h2 className="text-2xl font-bold mb-4 text-primary">Curriculum</h2>
                  <div className="flex flex-col gap-2">
                    {course.curriculum.map((module, index) => (
                      <div key={index} className="border border-border-light dark:border-border-dark rounded-lg overflow-hidden">
                        <button 
                          className="w-full flex justify-between items-center p-4 text-left font-semibold bg-surface-light dark:bg-surface-dark hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                          onClick={() => toggleModule(index)}
                        >
                          <span className="font-bold">{module.title}</span>
                          <span className="material-symbols-outlined">{expandedModules[index] ? 'expand_less' : 'expand_more'}</span>
                        </button>
                        {expandedModules[index] && (
                          <div className="px-4 pb-4 bg-surface-light dark:bg-surface-dark border-t border-border-light dark:border-border-dark">
                            <ul className="space-y-3 pt-3">
                              {module.lessons.map((lesson, lIdx) => (
                                <li key={lIdx} className="flex items-center gap-3 text-sm text-text-light-secondary dark:text-text-dark-secondary">
                                  <span className="material-symbols-outlined text-primary text-lg">play_circle</span>
                                  {lesson}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

              </div>

              {/* RIGHT COLUMN: Sticky Sidebar */}
              <div className="w-full lg:w-1/3">
                <div className="sticky top-24">
                  <div className="border border-border-light dark:border-border-dark rounded-xl shadow-lg bg-surface-light dark:bg-surface-dark overflow-hidden">
                    {/* Preview Image */}
                    <div className="relative aspect-video">
                      <div className="absolute inset-0 bg-center bg-no-repeat bg-cover" style={{ backgroundImage: `url("${course.image}")` }}></div>
                      <div className="absolute inset-0 bg-black/40 flex items-center justify-center group cursor-pointer hover:bg-black/50 transition-colors">
                        <button className="bg-white/90 rounded-full h-16 w-16 flex items-center justify-center text-primary shadow-lg transform group-hover:scale-110 transition-transform">
                          <span className="material-symbols-outlined !text-5xl ml-1">play_arrow</span>
                        </button>
                      </div>
                    </div>

                    <div className="p-6 flex flex-col gap-4">
                      <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-primary">${course.price}</p>
                        <p className="text-lg line-through text-text-light-secondary dark:text-text-dark-secondary">${course.originalPrice}</p>
                        <p className="text-sm font-bold text-green-600 dark:text-green-400">{course.discount}</p>
                      </div>
                      
                      <div className="flex flex-col gap-3">
                        <button className="w-full h-12 bg-primary text-white rounded-lg font-bold hover:bg-red-700 transition-colors shadow-md hover:shadow-lg">
                          Add to Cart
                        </button>
                        <button className="w-full h-12 bg-transparent text-primary border-2 border-primary rounded-lg font-bold hover:bg-primary/5 transition-colors">
                          Buy Now
                        </button>
                      </div>
                      
                      <p className="text-xs text-center text-text-light-secondary dark:text-text-dark-secondary">30-Day Money-Back Guarantee</p>
                      
                      <div className="border-t border-border-light dark:border-border-dark pt-4 mt-2">
                        <h3 className="font-bold mb-3 text-sm uppercase tracking-wide text-text-light-primary dark:text-text-dark-primary">What you'll learn</h3>
                        <ul className="space-y-2">
                          {course.whatYouWillLearn.map((item, idx) => (
                            <li key={idx} className="flex items-start gap-3 text-sm text-text-light-secondary dark:text-text-dark-secondary">
                              <span className="material-symbols-outlined text-green-500 text-lg mt-0.5">check</span>
                              <span>{item}</span>
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