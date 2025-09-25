import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';
const roles = ["patient", "donor", "hospital", "doctor"];

// Password strength checker
const checkPasswordStrength = (password) => {
  let score = 0;
  let feedback = [];

  if (password.length >= 8) score++;
  else feedback.push("At least 8 characters");

  if (/[a-z]/.test(password)) score++;
  else feedback.push("Include lowercase letters");

  if (/[A-Z]/.test(password)) score++;
  else feedback.push("Include uppercase letters");

  if (/[0-9]/.test(password)) score++;
  else feedback.push("Include numbers");

  if (/[^A-Za-z0-9]/.test(password)) score++;
  else feedback.push("Include special characters");

  if (score <= 2) return { score, strength: "Weak", color: "text-red-500", bgColor: "bg-red-100" };
  if (score <= 3) return { score, strength: "Fair", color: "text-yellow-500", bgColor: "bg-yellow-100" };
  if (score <= 4) return { score, strength: "Good", color: "text-blue-500", bgColor: "bg-blue-100" };
  return { score, strength: "Strong", color: "text-green-500", bgColor: "bg-green-100" };
};

export default function Signup() {
  const [role, setRole] = useState("patient");
  const [isLoading, setIsLoading] = useState(false);
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [errors, setErrors] = useState({});
  
  const { register, handleSubmit, reset, watch, formState: { errors: formErrors } } = useForm();
  const watchPassword = watch("password");

  const onSubmit = async (data) => {
    if (!acceptTerms) {
      setErrors({ terms: "Please accept the terms and conditions" });
      return;
    }

    if (data.password !== data.confirmPassword) {
      setErrors({ confirmPassword: "Passwords do not match" });
      return;
    }

    setIsLoading(true);
    setErrors({});
    const { email, password, confirmPassword, ...rest } = data;

    // First, test if the server is reachable
    try {
      console.log('Testing server connectivity...');
      const healthCheck = await axios.get(`${API_BASE_URL}/`, {
        timeout: 5000
      });
      console.log('Server is reachable:', healthCheck.status);
    } catch (error) {
      console.log('Server connectivity test failed:', error.message);
      if (error.code === 'ECONNREFUSED') {
        setErrors({ general: 'Backend server is not running. Please start the server on http://127.0.0.1:8000' });
        setIsLoading(false);
        return;
      }
    }

    // Try FastAPI common patterns
    const endpoints = [
      `${API_BASE_URL}/auth/register`,
      `${API_BASE_URL}/users/register`,
      `${API_BASE_URL}/register`,
      `${API_BASE_URL}/signup`,
      `${API_BASE_URL}/api/v1/auth/register`,
      `${API_BASE_URL}/api/v1/users/register`,
      `${API_BASE_URL}/api/auth/register`,
      `${API_BASE_URL}/api/users/register`
    ];

    // Clean payload - remove undefined values
    const cleanData = Object.fromEntries(
      Object.entries({
        email: email,
        password: password,
        user_type: role,
        first_name: data.first_name,
        last_name: data.last_name,
        phone: data.phone,
        ...rest
      }).filter(([key, value]) => value !== undefined && value !== '')
    );

    console.log('Cleaned payload:', cleanData);

    let lastError = null;

    for (const endpoint of endpoints) {
      try {
        console.log(`Trying endpoint: ${endpoint}`);
        
        const response = await axios.post(endpoint, cleanData, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          timeout: 10000
        });

        console.log('Signup successful:', response.data);
        
        // Success
        setErrors({ general: 'Account created successfully! Please check your email for verification.' });
        reset();
        setPassword("");
        setAcceptTerms(false);
        setIsLoading(false);
        
        // Redirect after 2 seconds
        setTimeout(() => {
          window.location.href = '/login';
        }, 2000);
        
        return;
        
      } catch (error) {
        console.log(`Failed with endpoint ${endpoint}:`, {
          status: error.response?.status,
          data: error.response?.data,
          message: error.message
        });
        
        lastError = error;
        
        // If we get 422 (validation error) or 400 (bad request), 
        // this might be the correct endpoint but with wrong data format
        if (error.response && [400, 422].includes(error.response.status)) {
          console.log('Found potential correct endpoint with validation error:', endpoint);
          break;
        }
        
        // If we get 409 (conflict), user already exists
        if (error.response && error.response.status === 409) {
          setErrors({ general: 'An account with this email already exists.' });
          setIsLoading(false);
          return;
        }
      }
    }

    // Handle the final error
    console.error('All signup attempts failed. Last error:', lastError);
    
    let errorMessage = 'Unable to create account';
    
    if (lastError && lastError.response) {
      const status = lastError.response.status;
      const data = lastError.response.data;
      
      console.log('Final error response data:', data);
      
      if (status === 404) {
        errorMessage = 'Signup endpoint not found. Please contact support or check if the correct backend is running.';
      } else if (status === 400) {
        if (data?.detail && Array.isArray(data.detail)) {
          errorMessage = data.detail.map(err => `${err.loc?.join(' ')}: ${err.msg}`).join(', ');
        } else {
          errorMessage = data?.detail || data?.message || data?.error || 'Invalid request data';
        }
      } else if (status === 422) {
        if (data?.detail && Array.isArray(data.detail)) {
          errorMessage = 'Validation errors: ' + data.detail.map(err => `${err.loc?.join(' ')}: ${err.msg}`).join(', ');
        } else {
          errorMessage = data?.detail || data?.message || 'Validation error';
        }
      } else if (status === 500) {
        errorMessage = 'Server error. Please try again later or contact support.';
      } else {
        errorMessage = data?.detail || data?.message || data?.error || `Server error (${status})`;
      }
    } else if (lastError && lastError.code === 'ECONNREFUSED') {
      errorMessage = 'Cannot connect to server. Please ensure the backend is running on http://127.0.0.1:8000';
    } else if (lastError && lastError.code === 'ENOTFOUND') {
      errorMessage = 'Server not found. Please check the server address.';
    } else if (lastError && lastError.code === 'NETWORK_ERROR') {
      errorMessage = 'Network error. Please check your internet connection.';
    } else {
      errorMessage = lastError?.message || 'An unexpected error occurred';
    }
    
    setErrors({ general: errorMessage });
    setIsLoading(false);
  };

  const passwordStrength = checkPasswordStrength(password);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-2xl mx-auto bg-white rounded-3xl shadow-xl overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-6 text-white">
          <h2 className="text-3xl font-bold text-center">Create Your Account</h2>
          <p className="text-center text-blue-100 mt-2">Join ThalCare to make a difference</p>
        </div>

        <div className="p-8">
          {/* Role Selection */}
          <div className="mb-8">
            <label className="block text-sm font-medium text-gray-700 mb-3">Select Your Role</label>
            <div className="flex gap-3 justify-center">
              {roles.map((r) => (
                <button
                  key={r}
                  type="button"
                  onClick={() => setRole(r)}
                  className={`px-6 py-3 rounded-xl border-2 transition-all duration-200 ${
                    role === r 
                      ? "border-blue-600 bg-blue-600 text-white shadow-lg" 
                      : "border-gray-200 bg-white text-gray-700 hover:border-blue-300 hover:bg-blue-50"
                  }`}
                >
                  <div className="text-lg font-semibold">{r.charAt(0).toUpperCase() + r.slice(1)}</div>
                  <div className="text-xs opacity-80">
                    {r === "patient" && "Need blood"}
                    {r === "donor" && "Donate blood"}
                    {r === "hospital" && "Provide care"}
                    {r === "doctor" && "Provide treatment"}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Error Display */}
          {errors.general && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700">
              <div className="flex items-center">
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                {errors.general}
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Common Fields for All Roles */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                <input
                  {...register("email", { 
                    required: "Email is required",
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: "Invalid email address"
                    }
                  })}
                  type="email"
                  placeholder="your@email.com"
                  className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                />
                {formErrors.email && (
                  <p className="mt-1 text-sm text-red-600">{formErrors.email.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
                <input
                  {...register("phone", { required: "Phone is required" })}
                  type="tel"
                  placeholder="+1 (555) 123-4567"
                  className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                />
                {formErrors.phone && (
                  <p className="mt-1 text-sm text-red-600">{formErrors.phone.message}</p>
                )}
              </div>
            </div>

            {/* Password Fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
                <div className="relative">
                  <input
                    {...register("password", { 
                      required: "Password is required",
                      minLength: { value: 8, message: "Password must be at least 8 characters" }
                    })}
                    type={showPassword ? "text" : "password"}
                    placeholder="Create a strong password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full p-4 pr-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    {showPassword ? "👁️" : "👁️‍🗨️"}
                  </button>
                </div>
                
                {/* Password Strength Indicator */}
                <div className="mt-2">
                  <div className="flex items-center gap-2 mb-1">
                    <div className={`text-sm font-medium ${passwordStrength.color}`}>
                      {passwordStrength.strength}
                    </div>
                    <div className="flex gap-1">
                      {[1, 2, 3, 4, 5].map((level) => (
                        <div
                          key={level}
                          className={`w-2 h-2 rounded-full ${
                            level <= passwordStrength.score ? passwordStrength.bgColor : "bg-gray-200"
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                  <p className="text-xs text-gray-500">
                    Include uppercase, lowercase, numbers, and special characters
                  </p>
                </div>
                
                {formErrors.password && (
                  <p className="mt-1 text-sm text-red-600">{formErrors.password.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Confirm Password</label>
                <div className="relative">
                  <input
                    {...register("confirmPassword", { required: "Please confirm your password" })}
                    type={showConfirmPassword ? "text" : "password"}
                    placeholder="Confirm your password"
                    className="w-full p-4 pr-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    {showConfirmPassword ? "👁️" : "👁️‍🗨️"}
                  </button>
                </div>
                {errors.confirmPassword && (
                  <p className="mt-1 text-sm text-red-600">{errors.confirmPassword}</p>
                )}
              </div>
            </div>

            {/* Role-Specific Fields */}
            {role === "patient" && (
              <div className="bg-blue-50 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-blue-900 mb-4">Patient Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input {...register("first_name", { required: "First name is required" })} placeholder="First Name" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("last_name", { required: "Last name is required" })} placeholder="Last Name" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("date_of_birth")} type="date" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("blood_type")} placeholder="Blood Type (e.g. A+)" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("address")} placeholder="Address" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("city")} placeholder="City" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("state")} placeholder="State" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                </div>
              </div>
            )}

            {role === "donor" && (
              <div className="bg-green-50 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-green-900 mb-4">Donor Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input {...register("blood_type", { required: "Blood type is required" })} placeholder="Blood Type" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("last_donation")} type="date" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("city")} placeholder="City" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("state")} placeholder="State" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <select {...register("contact_preference")} className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
                    <option value="email">Email</option>
                    <option value="phone">Phone</option>
                    <option value="both">Both</option>
                  </select>
                </div>
              </div>
            )}

            {role === "hospital" && (
              <div className="bg-purple-50 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-purple-900 mb-4">Hospital Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input {...register("name", { required: "Hospital name is required" })} placeholder="Hospital Name" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("address")} placeholder="Address" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("city")} placeholder="City" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("state")} placeholder="State" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("services")} placeholder="Services (comma separated)" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <div className="flex items-center gap-3 p-4 border border-gray-300 rounded-xl">
                    <input type="checkbox" {...register("thalassemia_specialist")} className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500" />
                    <span className="text-gray-700">Thalassemia Specialist</span>
                  </div>
                </div>
              </div>
            )}

            {role === "doctor" && (
              <div className="bg-indigo-50 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-indigo-900 mb-4">Doctor Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input {...register("first_name", { required: "First name is required" })} placeholder="First Name" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("last_name", { required: "Last name is required" })} placeholder="Last Name" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("specialization")} placeholder="Specialization" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("experience_years")} type="number" placeholder="Years of Experience" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("license_number")} placeholder="License Number" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <input {...register("consultation_fee")} type="number" placeholder="Consultation Fee (₹)" className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  <div className="flex items-center gap-3 p-4 border border-gray-300 rounded-xl">
                    <input type="checkbox" {...register("thalassemia_specialist")} className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500" />
                    <span className="text-gray-700">Thalassemia Specialist</span>
                  </div>
                </div>
              </div>
            )}

            {/* Terms and Conditions */}
            <div className="flex items-start gap-3">
              <input
                type="checkbox"
                id="terms"
                checked={acceptTerms}
                onChange={(e) => setAcceptTerms(e.target.checked)}
                className="mt-1 w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
              />
              <label htmlFor="terms" className="text-sm text-gray-700">
                I agree to the{" "}
                <a href="#" className="text-blue-600 hover:text-blue-800 underline">Terms and Conditions</a>
                {" "}and{" "}
                <a href="#" className="text-blue-600 hover:text-blue-800 underline">Privacy Policy</a>
              </label>
            </div>
            {errors.terms && (
              <p className="text-sm text-red-600">{errors.terms}</p>
            )}

            {/* Submit Button */}
            <button 
              type="submit" 
              disabled={isLoading || !acceptTerms}
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-4 rounded-xl hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              {isLoading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Creating Account...
                </div>
              ) : (
                `Create ${role.charAt(0).toUpperCase() + role.slice(1)} Account`
              )}
            </button>

            {/* Login Link */}
            <p className="text-center text-gray-600">
              Already have an account?{" "}
              <a href="/login" className="text-blue-600 hover:text-blue-800 font-semibold underline">
                Sign in here
              </a>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}