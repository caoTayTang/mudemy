import React from 'react';
import { useLoginController } from '../hooks/useLoginController';

const LoginPage = () => {
  const { 
    authMode, 
    toggleAuthMode, 
    formData, 
    status, 
    handleInputChange, 
    handleSubmit 
  } = useLoginController();

  const isRegister = authMode === 'register';

  return (
    <div className="font-display">
      <div className="relative flex min-h-screen w-full flex-col bg-background-light dark:bg-background-dark group/design-root overflow-x-hidden" style={{ fontFamily: 'Lexend, "Noto Sans", sans-serif' }}>
        <div className="flex-grow flex items-stretch">
          
          {/* --- LEFT SIDE (DECORATIVE) --- */}
          <div className="hidden lg:flex lg:w-1/2 items-center justify-center p-8 relative overflow-hidden bg-primary/5 dark:bg-primary/10">
            <div className="absolute inset-0 z-0">
              <div className="absolute -bottom-1/4 -left-1/4 w-1/2 h-1/2 rounded-full bg-primary/20 dark:bg-primary/30 blur-3xl opacity-50"></div>
              <div className="absolute -top-1/4 -right-1/4 w-3/4 h-3/4 rounded-full bg-primary/10 dark:bg-primary/20 blur-3xl opacity-40"></div>
              <div className="absolute bottom-10 right-10 w-1/3 h-1/3 rounded-full bg-primary/10 dark:bg-primary/20 blur-2xl opacity-60"></div>
            </div>
            <div className="w-full max-w-md text-center z-10">
              <div className="inline-flex items-center justify-center p-6 bg-white dark:bg-[#2a1818] rounded-full shadow-lg mb-8 border border-primary/10">
                <span className="material-symbols-outlined text-6xl text-primary">school</span>
              </div>
              <h2 className="text-3xl font-bold text-[#1b0d0d] dark:text-[#fcf8f8]">Unlock Your Potential</h2>
              <p className="mt-2 text-[#9a4c4c] dark:text-[#e7cfcf]">Join thousands of learners and start your journey with MUDemy today.</p>
            </div>
          </div>

          {/* --- RIGHT SIDE (FORM) --- */}
          <div className="w-full lg:w-1/2 flex items-center justify-center p-4 sm:p-8">
            <div className="w-full max-w-md space-y-6">
              
              {/* Mobile Header */}
              <div className="flex justify-center lg:hidden">
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-4xl text-primary">school</span>
                  <span className="text-3xl font-bold text-[#1b0d0d] dark:text-[#fcf8f8]">MUDemy</span>
                </div>
              </div>

              <div className="bg-white dark:bg-[#2a1818] p-6 sm:p-8 rounded-xl shadow-md border border-[#e7cfcf] dark:border-[#3e2c2c]">
                <h1 className="text-[#1b0d0d] dark:text-[#fcf8f8] tracking-light text-[32px] font-bold leading-tight text-left pb-3 pt-6">
                  {isRegister ? 'Create an Account' : 'Welcome Back'}
                </h1>

                {/* Status Message */}
                {status.error && (
                  <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded text-sm">
                    {status.error}
                  </div>
                )}

                {/* Toggle Switch */}
                <div className="flex py-3">
                  <div className="flex h-10 flex-1 items-center justify-center rounded-lg bg-[#f3e7e7] dark:bg-[#3e2c2c] p-1">
                    <label className={`flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 text-sm font-medium leading-normal transition-all ${!isRegister ? 'bg-[#fcf8f8] dark:bg-[#543d3d] shadow-[0_0_4px_rgba(0,0,0,0.1)] text-[#1b0d0d] dark:text-[#fcf8f8]' : 'text-[#9a4c4c] dark:text-[#e7cfcf]'}`}>
                      <span className="truncate">Login</span>
                      <input 
                        className="invisible w-0" 
                        type="radio" 
                        name="auth-toggle" 
                        checked={!isRegister} 
                        onChange={() => toggleAuthMode('login')} 
                      />
                    </label>
                    <label className={`flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 text-sm font-medium leading-normal transition-all ${isRegister ? 'bg-[#fcf8f8] dark:bg-[#543d3d] shadow-[0_0_4px_rgba(0,0,0,0.1)] text-[#1b0d0d] dark:text-[#fcf8f8]' : 'text-[#9a4c4c] dark:text-[#e7cfcf]'}`}>
                      <span className="truncate">Register</span>
                      <input 
                        className="invisible w-0" 
                        type="radio" 
                        name="auth-toggle" 
                        checked={isRegister} 
                        onChange={() => toggleAuthMode('register')} 
                      />
                    </label>
                  </div>
                </div>

                {/* Form */}
                <form className="space-y-4" onSubmit={handleSubmit}>
                  
                  {/* Register Fields */}
                  {isRegister && (
                    <>
                      <div className="register-field">
                        <p className="text-[#1b0d0d] dark:text-[#fcf8f8] text-base font-medium leading-normal pb-2">Full Name</p>
                        <input 
                          name="fullName"
                          value={formData.fullName}
                          onChange={handleInputChange}
                          className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#1b0d0d] dark:text-[#fcf8f8] focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-[#e7cfcf] dark:border-[#3e2c2c] bg-background-light dark:bg-[#221010] focus:border-primary h-14 placeholder:text-[#9a4c4c] dark:placeholder:text-[#9a4c4c] p-[15px] text-base font-normal leading-normal" 
                          placeholder="Enter your full name" 
                        />
                      </div>
                    </>
                  )}

                  {/* Common Fields */}
                  <div className="flex flex-col min-w-40 flex-1">
                    <p className="text-[#1b0d0d] dark:text-[#fcf8f8] text-base font-medium leading-normal pb-2">Username</p>
                    <input 
                      name="username"
                      type="text"
                      value={formData.username}
                      onChange={handleInputChange}
                      className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#1b0d0d] dark:text-[#fcf8f8] focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-[#e7cfcf] dark:border-[#3e2c2c] bg-background-light dark:bg-[#221010] focus:border-primary h-14 placeholder:text-[#9a4c4c] dark:placeholder:text-[#9a4c4c] p-[15px] text-base font-normal leading-normal" 
                      placeholder="Enter your username" 
                    />
                  </div>
                  
                  <div className="flex flex-col min-w-40 flex-1">
                    <p className="text-[#1b0d0d] dark:text-[#fcf8f8] text-base font-medium leading-normal pb-2">Password</p>
                    <div className="flex w-full flex-1 items-stretch rounded-lg">
                      <input 
                        name="password"
                        type="password"
                        value={formData.password}
                        onChange={handleInputChange}
                        className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#1b0d0d] dark:text-[#fcf8f8] focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-[#e7cfcf] dark:border-[#3e2c2c] bg-background-light dark:bg-[#221010] focus:border-primary h-14 placeholder:text-[#9a4c4c] dark:placeholder:text-[#9a4c4c] p-[15px] rounded-r-none border-r-0 pr-2 text-base font-normal leading-normal" 
                        placeholder="Enter your password" 
                      />
                      <button className="text-[#9a4c4c] dark:text-[#e7cfcf] flex border border-[#e7cfcf] dark:border-[#3e2c2c] bg-background-light dark:bg-[#221010] items-center justify-center px-[15px] rounded-r-lg border-l-0 focus:outline-none focus:ring-2 focus:ring-primary/50" type="button">
                        <span className="material-symbols-outlined">visibility</span>
                      </button>
                    </div>
                  </div>

                  {/* Role Selection (Common for Login and Register) */}
                  <div className="register-field">
                    <p className="text-[#1b0d0d] dark:text-[#fcf8f8] text-base font-medium leading-normal pb-2">{isRegister ? 'Register as' : 'Login as'}</p>
                    <div className="grid grid-cols-2 gap-4">
                      <label className={`flex items-center gap-3 p-4 rounded-lg border cursor-pointer ${formData.role === 'tutee' ? 'bg-primary/10 dark:bg-primary/20 border-primary' : 'border-[#e7cfcf] dark:border-[#3e2c2c]'}`}>
                        <input 
                          type="radio" 
                          name="role" 
                          value="tutee" 
                          checked={formData.role === 'tutee'}
                          onChange={handleInputChange}
                          className="form-radio text-primary focus:ring-primary" 
                        />
                        <span className="text-[#1b0d0d] dark:text-[#fcf8f8] font-medium">Student</span>
                      </label>
                      <label className={`flex items-center gap-3 p-4 rounded-lg border cursor-pointer ${formData.role === 'tutor' ? 'bg-primary/10 dark:bg-primary/20 border-primary' : 'border-[#e7cfcf] dark:border-[#3e2c2c]'}`}>
                        <input 
                          type="radio" 
                          name="role" 
                          value="tutor" 
                          checked={formData.role === 'tutor'}
                          onChange={handleInputChange} 
                          className="form-radio text-primary focus:ring-primary" 
                        />
                        <span className="text-[#1b0d0d] dark:text-[#fcf8f8] font-medium">Instructor</span>
                      </label>
                    </div>
                  </div>

                  {/* Login Extras */}
                  {!isRegister && (
                    <p className="text-[#9a4c4c] dark:text-[#e7cfcf] text-sm font-normal leading-normal pb-3 pt-1 text-right underline cursor-pointer hover:text-primary">
                      Forgot Password?
                    </p>
                  )}

                  <button 
                    type="submit" 
                    className="w-full bg-primary text-white font-bold py-4 px-4 rounded-lg hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary dark:focus:ring-offset-[#221010] transition-colors duration-300"
                    disabled={status.loading}
                  >
                    {status.loading ? 'Processing...' : (isRegister ? 'Create Account' : 'Log In')}
                  </button>
                </form>

                <div className="relative flex py-5 items-center">
                  <div className="flex-grow border-t border-[#e7cfcf] dark:border-[#3e2c2c]"></div>
                  <span className="flex-shrink mx-4 text-sm text-[#9a4c4c] dark:text-[#e7cfcf]">OR</span>
                  <div className="flex-grow border-t border-[#e7cfcf] dark:border-[#3e2c2c]"></div>
                </div>

                <div className="space-y-3">
                  <button className="w-full flex items-center justify-center gap-3 border border-[#e7cfcf] dark:border-[#3e2c2c] bg-white dark:bg-transparent text-[#1b0d0d] dark:text-[#fcf8f8] font-medium py-3 px-4 rounded-lg hover:bg-[#f3e7e7] dark:hover:bg-[#3e2c2c] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#e7cfcf] dark:focus:ring-offset-[#221010] transition-colors duration-300">
                    <img alt="Google logo" className="w-6 h-6" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAxtJykgU6MtKK4Dp1fqQNUUaNHrFdlBlQGF4ds1uNb6reg-9XaeEHL9zfcxTOZfrVYC-VYclhauovBwWWuw6ioHDgd_IoaU1rhMoAlcioizTIEUGH5-gb7CSXAJZVpUbJKu4tK_WbyZ8hjW8kiPeptAj_NeQtT4rMzJTyYgsHkusm9HHlJrCkA8wFN_Cjee1J3dZbY0S-tYD1E_esbk9wrju8q9R_5hWNCpZAYtZueS1IysmkLfLrX2Gh52pHzCJlE_6MJdO9o4Yo"/> 
                    Continue with Google
                  </button>
                  <button className="w-full flex items-center justify-center gap-3 border border-[#e7cfcf] dark:border-[#3e2c2c] bg-white dark:bg-transparent text-[#1b0d0d] dark:text-[#fcf8f8] font-medium py-3 px-4 rounded-lg hover:bg-[#f3e7e7] dark:hover:bg-[#3e2c2c] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#e7cfcf] dark:focus:ring-offset-[#221010] transition-colors duration-300">
                    <img alt="Facebook logo" className="w-6 h-6" src="https://lh3.googleusercontent.com/aida-public/AB6AXuB3B4_mZDfNuf-kOa1nipqIwLGbmnFOi8-Pm60MKYRVzWYbPT3xbRYaKBvQP9jLSBcS_GeVpyYCzFnt4ygb139zZCSOan6A_PAoF2lEvxZsgsQT1ZM5hq5M9B2caqIGG_nYqgANOhnW1NU-yiDg-ViGtu7Ww3HWIAoWckZBcGM7shg50KAw5nJM_JZqEDqVrf1H3v4ik_im9NY1Hw26RF4zEcTBFySSW36wWfLDwEmzrPQ9Og96SjND-xyFuM7zAYsyd-C1SVs7KQI"/> 
                    Continue with Facebook
                  </button>
                </div>

              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default LoginPage;