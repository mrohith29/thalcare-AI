import { useState } from "react";
import { useForm } from "react-hook-form";
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export default function Login() {
  const { register, handleSubmit, reset } = useForm();
  const [isLoading, setIsLoading] = useState(false);

  const onSubmit = async (data) => {
    setIsLoading(true);
    
    try {
      const response = await axios.post(`${API_BASE_URL}/login`, {
        email: data.email,
        password: data.password
      });
      
      console.log('Login successful:', response.data);
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user_id', response.data.user_id);
      alert('Login successful!');
      reset();
      
    } catch (error) {
      console.error('Login failed:', error.response?.data?.detail || error.message);
      alert('Login failed: ' + (error.response?.data?.detail || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-2xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <input
          {...register("email")}
          type="email"
          placeholder="Email"
          className="w-full p-3 border rounded-xl"
          required
        />
        
        <input
          {...register("password")}
          type="password"
          placeholder="Password"
          className="w-full p-3 border rounded-xl"
          required
        />

        <button 
          type="submit" 
          disabled={isLoading}
          className="w-full bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700 disabled:opacity-50"
        >
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
}