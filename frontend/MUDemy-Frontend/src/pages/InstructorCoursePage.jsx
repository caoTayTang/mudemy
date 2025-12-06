import React from 'react';
import { useInstructorCourseController } from '../hooks/useInstructorCourseController';

const InstructorCoursePage = () => {
  const { 
    profile, 
    courses, 
    selectedCourse, 
    loading, 
    formState, 
    filterState,
    actions 
  } = useInstructorCourseController();

  // Destructure submitting from formState
  const { isEditing, isCreating, formData, error, submitting } = formState;

  if (!profile && loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;

  return (
    <div className="font-display bg-background-light dark:bg-background-dark text-text-light dark:text-text-dark">
      <div className="relative flex min-h-screen w-full">
        
        {/* SIDEBAR - LIST VIEW */}
        <aside className="flex w-80 flex-col border-r border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark p-4 hidden md:flex">
          {/* Profile */}
          <div className="flex items-center gap-3 p-2 mb-4 border-b border-border-light dark:border-border-dark pb-4">
            <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" style={{ backgroundImage: `url("${profile?.avatar || 'https://lh3.googleusercontent.com/aida-public/AB6AXuAssnCt9Egd0VLTCsLA4FxjYlGsBTXYa95CI4yF8TQMm60NRBPXhDca5JGRRDEi_5NHIY_mf5YvBDCLaeayU3XSOX6kR7wR6-fV1Ia-KxMXH_eGBMnN0zYCv8tuUOyknCmUC-tutsoxZbUAktYcj9TfqNg-zaGiUOj7TzHqTkZgNftdJlTxhQxTDLoszMoobNBZHT7EZZR-7aVbQ0_GbFrV_FHpFnP57FSE0doVrm0TE2khrNRYbcnibkWPZUzovZFr8j1XCNOXVYY'}")` }}></div>
            <div className="flex flex-col">
              <h1 className="text-base font-medium">{profile?.User_name || "Instructor"}</h1>
              <p className="text-text-muted-light dark:text-text-muted-dark text-sm">Course Manager</p>
            </div>
          </div>

          {/* Controls */}
          <div className="flex flex-col gap-2 mb-4">
            <input 
              type="text" 
              placeholder="Filter by title..." 
              value={filterState.searchTerm}
              onChange={(e) => actions.setSearchTerm(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-border-light dark:border-border-dark rounded bg-background-light dark:bg-background-dark focus:outline-none focus:border-primary"
            />
            <select 
              value={filterState.sortBy}
              onChange={(e) => actions.setSortBy(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-border-light dark:border-border-dark rounded bg-background-light dark:bg-background-dark focus:outline-none focus:border-primary"
            >
              <option value="title">Sort by Title</option>
              <option value="difficulty">Sort by Difficulty</option>
            </select>
          </div>
          
          {/* List */}
          <div className="flex flex-col gap-2 flex-grow overflow-y-auto">
            {courses.length === 0 && <p className="text-sm text-center text-text-muted-light">No courses found.</p>}
            {courses.map(course => (
              <div 
                key={course.CourseID}
                onClick={() => !submitting && actions.handleSelectCourse(course.CourseID)}
                className={`flex flex-col gap-1 px-3 py-2 rounded-lg cursor-pointer transition-colors border ${
                  selectedCourse?.CourseID === course.CourseID 
                    ? 'bg-primary/10 border-primary dark:bg-primary/20' 
                    : 'border-transparent hover:bg-gray-100 dark:hover:bg-gray-800/50'
                } ${submitting ? 'pointer-events-none opacity-50' : ''}`}
              >
                <p className="font-bold text-sm leading-normal truncate">{course.Title}</p>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-text-muted-light dark:text-text-muted-dark">{course.Difficulty}</span>
                  <span className="text-xs text-text-muted-light dark:text-text-muted-dark">{course.Language}</span>
                </div>
              </div>
            ))}
          </div>
          
          <button 
            onClick={actions.handleCreateInit}
            disabled={submitting}
            className={`flex items-center justify-center h-10 px-4 mt-4 bg-primary text-white text-sm font-bold rounded-lg transition-colors ${submitting ? 'opacity-50 cursor-not-allowed' : 'hover:bg-red-700'}`}
          >
            Create New Course
          </button>
        </aside>

        {/* MAIN CONTENT AREA */}
        <main className="flex-1 flex flex-col min-w-0 bg-background-light dark:bg-background-dark">
          
          {/* Header */}
          <header className="flex items-center justify-between border-b border-border-light dark:border-border-dark px-10 py-3 bg-surface-light dark:bg-surface-dark">
            <h2 className="text-lg font-bold">Course Details</h2>
            {selectedCourse && !isEditing && !isCreating && (
               <button 
                 onClick={() => actions.handleDelete(selectedCourse.CourseID)} 
                 disabled={submitting}
                 className="text-red-500 text-sm font-bold hover:underline disabled:opacity-50"
               >
                 Delete Course
               </button>
            )}
          </header>

          <div className="flex-1 overflow-y-auto p-10">
            {/* --- CREATE / EDIT FORM --- */}
            {(isCreating || isEditing) ? (
              <div className="max-w-2xl mx-auto bg-surface-light dark:bg-surface-dark p-8 rounded-xl shadow-sm border border-border-light dark:border-border-dark">
                <h3 className="text-2xl font-bold mb-6 text-primary">{isCreating ? "Create New Course" : "Edit Course"}</h3>
                
                {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded text-sm">{error}</div>}

                <form onSubmit={actions.handleSave} className="flex flex-col gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Course Title *</label>
                    <input 
                      name="Title" 
                      value={formData.Title} 
                      onChange={actions.handleInputChange}
                      className="w-full p-2 border border-border-light dark:border-border-dark rounded bg-transparent focus:border-primary focus:outline-none"
                      placeholder="e.g. Advanced Python"
                      disabled={submitting}
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Description *</label>
                    <textarea 
                      name="Description" 
                      value={formData.Description} 
                      onChange={actions.handleInputChange}
                      className="w-full p-2 border border-border-light dark:border-border-dark rounded bg-transparent h-32 focus:border-primary focus:outline-none"
                      placeholder="Course overview..."
                      disabled={submitting}
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Difficulty</label>
                      <select 
                        name="Difficulty" 
                        value={formData.Difficulty} 
                        onChange={actions.handleInputChange}
                        className="w-full p-2 border border-border-light dark:border-border-dark rounded bg-transparent focus:border-primary focus:outline-none"
                        disabled={submitting}
                      >
                        <option value="Beginner">Beginner</option>
                        <option value="Intermediate">Intermediate</option>
                        <option value="Advanced">Advanced</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Language</label>
                      <input 
                        name="Language" 
                        value={formData.Language} 
                        onChange={actions.handleInputChange}
                        className="w-full p-2 border border-border-light dark:border-border-dark rounded bg-transparent focus:border-primary focus:outline-none"
                        disabled={submitting}
                      />
                    </div>
                  </div>

                  <div className="flex gap-3 mt-6">
                    <button 
                      type="button" 
                      onClick={actions.cancelForm} 
                      className="px-4 py-2 border border-border-light dark:border-border-dark rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                      disabled={submitting}
                    >
                      Cancel
                    </button>
                    
                    {/* LOADING STATE APPLIED HERE */}
                    <button 
                      type="submit" 
                      className={`px-6 py-2 bg-primary text-white rounded font-bold flex items-center gap-2 transition-colors ${submitting ? 'opacity-70 cursor-not-allowed' : 'hover:bg-red-700'}`}
                      disabled={submitting}
                    >
                      {submitting && <span className="material-symbols-outlined animate-spin text-sm">progress_activity</span>}
                      {submitting ? "Processing..." : (isCreating ? "Create Course" : "Save Changes")}
                    </button>
                  </div>
                </form>
              </div>
            ) : selectedCourse ? (
              /* --- DETAIL VIEW --- */
              <div className="max-w-4xl mx-auto">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h1 className="text-4xl font-black text-primary mb-2">{selectedCourse.Title}</h1>
                    <p className="text-text-muted-light dark:text-text-muted-dark">{selectedCourse.Description}</p>
                  </div>
                  <button 
                    onClick={actions.handleEditInit}
                    className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded hover:bg-gray-300 dark:hover:bg-gray-600 font-bold text-sm transition-colors"
                  >
                    Edit Details
                  </button>
                </div>

                <div className="grid grid-cols-2 gap-4 border-y border-border-light dark:border-border-dark py-4 mb-8">
                  <div>
                    <span className="text-sm text-text-muted-light block">Difficulty</span>
                    <span className="font-medium">{selectedCourse.Difficulty}</span>
                  </div>
                  <div>
                    <span className="text-sm text-text-muted-light block">Language</span>
                    <span className="font-medium">{selectedCourse.Language}</span>
                  </div>
                </div>

                <h2 className="text-2xl font-bold mb-4">Content Preview</h2>
                <div className="p-8 border border-dashed border-border-light dark:border-border-dark rounded-xl text-center text-text-muted-light">
                  <p>Select "Create New Course" or edit this one to add modules.</p>
                  <p className="text-xs mt-2">(Module management will be implemented in the next phase)</p>
                </div>
              </div>
            ) : (
              /* --- EMPTY STATE --- */
              <div className="flex flex-col items-center justify-center h-full text-text-muted-light">
                <span className="material-symbols-outlined text-6xl mb-4">school</span>
                <p className="text-lg">Select a course to view details or create a new one.</p>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

export default InstructorCoursePage;