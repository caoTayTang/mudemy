import React from 'react';
import { useInstructorCourseController } from '../hooks/useInstructorCourseController';
import profileImg from "../assets/profile.jpg";
import { useNavigate } from 'react-router-dom';

const InstructorCoursePage = () => {
  const navigate = useNavigate();
  const { 
    profile, 
    courses, 
    selectedCourse, 
    relatedData, 
    loading, 
    formState, 
    filterState,
    actions 
  } = useInstructorCourseController();

  const { isEditing, isCreating, formData, error, submitting } = formState;
  const { modules = [], enrollments = [] } = relatedData || {};

  // If loading initially
  if (!profile && loading) return (
    <div className="min-h-screen flex items-center justify-center bg-background-light dark:bg-background-dark text-text-light dark:text-text-dark">
      <span className="material-symbols-outlined animate-spin text-4xl text-primary">progress_activity</span>
    </div>
  );

  return (
    <div className="font-display bg-background-light dark:bg-background-dark text-text-light dark:text-text-dark">
      <div className="relative flex min-h-screen w-full">
        
        {/* =======================
            SIDEBAR
           ======================= */}
        <aside 
          
          className="flex w-72 flex-col border-r border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark p-4 hidden md:flex h-screen sticky top-0"
        >
          {/* Profile Section */}
          <div 
            onClick={ () => navigate('/instructor') } 
            className="cursor-pointer flex items-center gap-3 p-2 mb-4"
          >
            <div 
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10 flex-shrink-0"
              style={{ backgroundImage: `url(${profileImg})` }}
            ></div>
            <div className="flex flex-col min-w-0">
              <h1 className="text-text-light dark:text-text-dark text-base font-medium leading-normal truncate">
                {profile?.User_name || "Instructor"}
              </h1>
              <p className="text-text-muted-light dark:text-text-muted-dark text-sm font-normal leading-normal">
                Instructor
              </p>
            </div>
          </div>

          {/* Filter/Search (Kept from functionality requirements) */}
          <div className="mb-4 space-y-2">
             <input 
              type="text" 
              placeholder="Filter courses..." 
              value={filterState.searchTerm}
              onChange={(e) => actions.setSearchTerm(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-border-light dark:border-border-dark rounded-lg bg-background-light dark:bg-background-dark focus:outline-none focus:border-primary transition-colors"
            />
          </div>

          {/* Course List */}
          <div className="flex flex-col gap-2 flex-grow overflow-y-auto pr-1 custom-scrollbar">
            {courses.length === 0 && (
              <p className="text-sm text-center text-text-muted-light py-4">No courses found.</p>
            )}
            
            {courses.map(course => {
              const isActive = selectedCourse?.CourseID === course.CourseID;
              return (
                <div 
                  key={course.CourseID}
                  onClick={() => !submitting && actions.handleSelectCourse(course.CourseID)}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors border ${
                    isActive 
                      ? 'bg-primary/10 dark:bg-primary/20 border-transparent' 
                      : 'border-transparent hover:bg-gray-100 dark:hover:bg-gray-800/50'
                  } ${submitting ? 'pointer-events-none opacity-50' : ''}`}
                >
                  <span 
                    className={`material-symbols-outlined ${isActive ? 'text-primary' : 'text-text-muted-light dark:text-text-muted-dark'}`} 
                    style={isActive ? { fontVariationSettings: "'FILL' 1" } : {}}
                  >
                    book
                  </span>
                  <p className={`${isActive ? 'text-primary font-bold' : 'text-text-light dark:text-text-dark font-medium'} text-sm leading-normal truncate`}>
                    {course.Title}
                  </p>
                </div>
              );
            })}
          </div>
          
          <button 
            onClick={actions.handleCreateInit}
            disabled={submitting}
            className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] mt-4 hover:bg-red-700 dark:hover:bg-red-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="truncate">Create New Course</span>
          </button>
        </aside>

        {/* =======================
            MAIN CONTENT
           ======================= */}
        <main className="flex-1 flex flex-col min-w-0">
          
          {/* Header */}
          <header className="flex items-center justify-between whitespace-nowrap border-b border-border-light dark:border-border-dark px-6 md:px-10 py-3 bg-surface-light dark:bg-surface-dark sticky top-0 z-10">
            <div className="flex items-center gap-4 text-text-light dark:text-text-dark">
              <div className="size-6 text-primary">
                <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                  <path d="M4 42.4379C4 42.4379 14.0962 36.0744 24 41.1692C35.0664 46.8624 44 42.2078 44 42.2078L44 7.01134C44 7.01134 35.068 11.6577 24.0031 5.96913C14.0971 0.876274 4 7.27094 4 7.27094L4 42.4379Z" fill="currentColor"></path>
                </svg>
              </div>
              <h2 className="text-text-light dark:text-text-dark text-lg font-bold leading-tight tracking-[-0.015em]">MUDemy Instructor</h2>
            </div>
            
            {/* Contextual Actions */}
            <div className="flex gap-2">
              {selectedCourse && !isEditing && !isCreating && (
                <button 
                  onClick={() => actions.handleDelete(selectedCourse.CourseID)}
                  className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-red-700 dark:hover:bg-red-500 transition-colors"
                >
                  Delete
                </button>
              )}
              {/* <button className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-red-700 dark:hover:bg-red-500 transition-colors">
                <span className="truncate">Submit for Approval</span>
              </button> */}
            </div>
          </header>

          <div className="flex-1 overflow-y-auto p-6 md:p-10">
            <div className="max-w-4xl mx-auto">
              
              {/* --- VIEW: CREATE / EDIT FORM --- */}
              {(isCreating || isEditing) ? (
                <div className="bg-surface-light dark:bg-surface-dark p-8 rounded-lg border border-border-light dark:border-border-dark shadow-sm">
                  <div className="flex items-center gap-3 mb-6">
                    <button onClick={actions.cancelForm} className="text-text-muted-light hover:text-primary">
                      <span className="material-symbols-outlined">arrow_back</span>
                    </button>
                    <h3 className="text-2xl font-bold text-primary">
                      {isCreating ? "Create New Course" : "Edit Course Details"}
                    </h3>
                  </div>
                  
                  {error && (
                    <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-300 rounded-lg text-sm flex items-center gap-2">
                      <span className="material-symbols-outlined">error</span>
                      {error}
                    </div>
                  )}

                  <form onSubmit={actions.handleSave} className="flex flex-col gap-6">
                    <div className="space-y-1">
                      <label className="text-sm font-medium text-text-light dark:text-text-dark">Course Title</label>
                      <input 
                        name="Title" 
                        value={formData.Title} 
                        onChange={actions.handleInputChange}
                        className="w-full px-4 py-3 rounded-lg border border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark text-text-light dark:text-text-dark focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
                        placeholder="e.g. Advanced Database Management"
                        disabled={submitting}
                      />
                    </div>

                    <div className="space-y-1">
                      <label className="text-sm font-medium text-text-light dark:text-text-dark">Description</label>
                      <textarea 
                        name="Description" 
                        value={formData.Description} 
                        onChange={actions.handleInputChange}
                        className="w-full px-4 py-3 rounded-lg border border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark text-text-light dark:text-text-dark focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all h-32 resize-y"
                        placeholder="What will students learn in this course?"
                        disabled={submitting}
                      />
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                      <div className="space-y-1">
                        <label className="text-sm font-medium text-text-light dark:text-text-dark">Difficulty</label>
                        <div className="relative">
                          <select 
                            name="Difficulty" 
                            value={formData.Difficulty} 
                            onChange={actions.handleInputChange}
                            className="w-full appearance-none px-4 py-3 rounded-lg border border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark text-text-light dark:text-text-dark focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
                            disabled={submitting}
                          >
                            <option value="Beginner">Beginner</option>
                            <option value="Intermediate">Intermediate</option>
                            <option value="Advanced">Advanced</option>
                          </select>
                          <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-text-muted-light pointer-events-none">expand_more</span>
                        </div>
                      </div>
                      <div className="space-y-1">
                        <label className="text-sm font-medium text-text-light dark:text-text-dark">Language</label>
                        <input 
                          name="Language" 
                          value={formData.Language} 
                          onChange={actions.handleInputChange}
                          className="w-full px-4 py-3 rounded-lg border border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark text-text-light dark:text-text-dark focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
                          disabled={submitting}
                        />
                      </div>
                    </div>

                    <div className="flex gap-4 pt-4">
                      <button 
                        type="button" 
                        onClick={actions.cancelForm} 
                        className="px-6 py-3 rounded-lg border border-border-light dark:border-border-dark text-text-light dark:text-text-dark font-medium hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                        disabled={submitting}
                      >
                        Cancel
                      </button>
                      
                      <button 
                        type="submit" 
                        className={`flex-1 px-6 py-3 bg-primary text-white rounded-lg font-bold flex items-center justify-center gap-2 transition-all ${submitting ? 'opacity-70 cursor-not-allowed' : 'hover:bg-red-700 shadow-md hover:shadow-lg'}`}
                        disabled={submitting}
                      >
                        {submitting && <span className="material-symbols-outlined animate-spin text-xl">progress_activity</span>}
                        {submitting ? "Saving..." : "Save Changes"}
                      </button>
                    </div>
                  </form>
                </div>
              ) : selectedCourse ? (
                
                /* --- VIEW: COURSE DETAILS (Matches your HTML Design) --- */
                <>
                  {/* Course Info Header */}
                  <div className="flex flex-wrap justify-between items-center gap-4 p-4 mb-4 bg-surface-light dark:bg-surface-dark rounded-lg border border-border-light dark:border-border-dark shadow-sm">
                    <div className="flex min-w-72 flex-col gap-3">
                      <div className="flex items-center gap-3">
                        <p className="text-primary dark:text-red-400 text-3xl md:text-4xl font-black leading-tight tracking-[-0.033em]">
                          {selectedCourse.Title}
                        </p>
                      </div>
                      <p className="text-text-muted-light dark:text-text-muted-dark text-base font-normal leading-normal">
                        {selectedCourse.Description}
                      </p>
                    </div>
                    <button 
                      onClick={actions.handleEditInit}
                      className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-gray-200 dark:bg-gray-700 text-text-light dark:text-text-dark text-sm font-bold leading-normal tracking-[0.015em] hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                    >
                      <span className="truncate">Edit Details</span>
                    </button>
                  </div>

                  {/* Meta Grid */}
                  <div className="p-4 grid grid-cols-1 sm:grid-cols-2 border-y border-solid border-border-light dark:border-border-dark mb-8">
                    <div className="flex flex-col gap-1 py-4 pr-2 sm:border-r border-solid border-border-light dark:border-border-dark">
                      <p className="text-text-muted-light dark:text-text-muted-dark text-sm font-normal leading-normal">Language</p>
                      <p className="text-text-light dark:text-text-dark text-sm font-normal leading-normal">{selectedCourse.Language}</p>
                    </div>
                    <div className="flex flex-col gap-1 py-4 sm:pl-4">
                      <p className="text-text-muted-light dark:text-text-muted-dark text-sm font-normal leading-normal">Difficulty</p>
                      <p className="text-text-light dark:text-text-dark text-sm font-normal leading-normal">{selectedCourse.Difficulty}</p>
                    </div>
                  </div>

                  {/* Curriculum Header */}
                  <h2 className="text-primary dark:text-red-400 text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3">
                    Course Curriculum
                  </h2>

                  {/* Modules List */}
                  <div className="px-4 py-2 space-y-4">
                    
                    {modules.length === 0 ? (
                      <div className="p-8 border-2 border-dashed border-border-light dark:border-border-dark rounded-xl text-center">
                        <span className="material-symbols-outlined text-4xl text-text-muted-light mb-2">post_add</span>
                        <p className="text-text-muted-light">No modules created yet.</p>
                        <p className="text-xs text-text-muted-dark mt-1">Click "Add Module" to start building your curriculum.</p>
                      </div>
                    ) : (
                      modules.map((mod) => (
                        <div key={mod.ModuleID} className="bg-surface-light dark:bg-surface-dark rounded-lg border border-border-light dark:border-border-dark shadow-sm overflow-hidden transition-all hover:border-primary/30">
                          {/* Module Header */}
                          <div className="flex items-center justify-between p-4 bg-gray-50/50 dark:bg-gray-800/30">
                            <div className="flex items-center gap-3">
                              <span className="material-symbols-outlined text-text-muted-light dark:text-text-muted-dark">folder_open</span>
                              <p className="text-base font-medium text-text-light dark:text-text-dark">{mod.Title}</p>
                            </div>
                            <div className="flex items-center gap-1">
                              <button className="p-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-text-muted-light">
                                <span className="material-symbols-outlined text-xl">edit</span>
                              </button>
                              <button className="p-2 rounded-md hover:bg-red-100 dark:hover:bg-red-900/30 hover:text-red-600 transition-colors text-text-muted-light">
                                <span className="material-symbols-outlined text-xl">delete</span>
                              </button>
                            </div>
                          </div>

                          {/* Lessons inside Module */}
                          <div className="border-t border-border-light dark:border-border-dark pl-4 pr-4 py-2 space-y-1">
                            {(mod.lessons || []).length === 0 ? (
                                <p className="text-xs text-text-muted-light italic p-2 ml-9">No lessons yet.</p>
                            ) : (
                              mod.lessons.map(lesson => (
                                <div key={lesson.id} className="flex items-center justify-between p-2 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors group">
                                  <div className="flex items-center gap-3 pl-2">
                                    <span className="material-symbols-outlined text-gray-400 dark:text-gray-500 text-xl group-hover:text-primary transition-colors">description</span>
                                    <p className="text-sm text-text-light dark:text-text-dark">{lesson.title}</p>
                                  </div>
                                  <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <button className="p-1.5 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600">
                                      <span className="material-symbols-outlined text-gray-500 text-lg">edit</span>
                                    </button>
                                    <button 
                                      onClick={() => actions.handleDeleteLesson(mod.ModuleID, lesson.id)}
                                      className="p-1.5 rounded-md hover:bg-red-100 dark:hover:bg-red-900/30 hover:text-red-600"
                                    >
                                      <span className="material-symbols-outlined text-gray-500 text-lg">delete</span>
                                    </button>
                                  </div>
                                </div>
                              ))
                            )}

                            {/* Add Lesson Button */}
                            <button 
                              onClick={() => actions.handleAddLesson(mod.ModuleID)}
                              className="w-full flex items-center justify-center gap-2 p-2 mt-2 text-sm font-medium text-primary hover:bg-primary/10 rounded-md transition-colors border border-transparent hover:border-primary/20"
                            >
                              <span className="material-symbols-outlined text-lg">add</span>
                              Add Lesson
                            </button>
                          </div>
                        </div>
                      ))
                    )}

                    {/* Add Module Button */}
                    <button 
                      onClick={actions.handleAddModule}
                      className="w-full flex items-center justify-center gap-2 h-12 mt-4 text-sm font-bold text-primary dark:text-red-400 bg-surface-light dark:bg-surface-dark border-2 border-dashed border-primary/30 hover:border-primary hover:bg-primary/5 dark:hover:bg-primary/10 rounded-lg transition-all"
                    >
                      <span className="material-symbols-outlined text-lg">add_circle</span>
                      Add New Module
                    </button>
                  </div>
                </>
              ) : (
                /* --- VIEW: EMPTY STATE --- */
                <div className="flex flex-col items-center justify-center h-[60vh] text-text-muted-light animate-in fade-in duration-500">
                  <div className="bg-surface-light dark:bg-surface-dark p-8 rounded-full mb-6 shadow-sm">
                    <span className="material-symbols-outlined text-6xl text-primary/50">school</span>
                  </div>
                  <h3 className="text-xl font-bold text-text-light dark:text-text-dark mb-2">Manage Your Courses</h3>
                  <p className="text-base max-w-md text-center">
                    Select a course from the sidebar to view details, manage curriculum, or edit information.
                  </p>
                  <button 
                    onClick={actions.handleCreateInit}
                    className="mt-6 px-6 py-3 bg-primary text-white rounded-lg font-bold hover:bg-red-700 transition-colors shadow-md"
                  >
                    Get Started
                  </button>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default InstructorCoursePage;