import { useState } from "react";
import { useForm } from "react-hook-form";
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';
const roles = ["patient", "donor", "hospital"];

export default function Signup() {
  const [role, setRole] = useState("patient");
  const [isLoading, setIsLoading] = useState(false);
  const { register, handleSubmit, reset } = useForm();

  const onSubmit = async (data) => {
    setIsLoading(true);
    const { email, password, ...rest } = data;

    try {
      const response = await axios.post(`${API_BASE_URL}/signup`, {
        email: email,
        password: password,
        user_type: role,
        name: role === "hospital" ? data.name : `${data.first_name || ''} ${data.last_name || ''}`.trim(),
        phone: data.phone,
        ...rest
      });

      console.log('Signup successful:', response.data);
      alert(`${role} signed up successfully!`);
      reset();
      
    } catch (error) {
      console.error('Signup failed:', error.response?.data?.detail || error.message);
      alert('Signup failed: ' + (error.response?.data?.detail || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-2xl shadow">
      <h2 className="text-2xl font-bold mb-4 text-center">Signup</h2>

      <div className="mb-4 flex gap-4 justify-center">
        {roles.map((r) => (
          <button
            key={r}
            onClick={() => setRole(r)}
            className={`px-4 py-2 rounded-full border ${
              role === r ? "bg-blue-600 text-white" : "bg-gray-100"
            }`}
          >
            {r.charAt(0).toUpperCase() + r.slice(1)}
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {(role === "patient" || role === "donor") && (
          <>
            <input
              {...register("email")}
              type="email"
              placeholder="Email"
              className="w-full p-3 border rounded-xl"
              required
            />
            <input
              type="password"
              {...register("password")}
              placeholder="Password"
              className="w-full p-3 border rounded-xl"
              required
            />
          </>
        )}

        {role === "patient" && (
          <>
            <input {...register("first_name")} placeholder="First Name" className="w-full p-3 border rounded-xl" />
            <input {...register("last_name")} placeholder="Last Name" className="w-full p-3 border rounded-xl" />
            <input {...register("phone")} placeholder="Phone" className="w-full p-3 border rounded-xl" />
            <input {...register("date_of_birth")} type="date" className="w-full p-3 border rounded-xl" />
            <input {...register("blood_type")} placeholder="Blood Type (e.g. A+)" className="w-full p-3 border rounded-xl" />
            <input {...register("address")} placeholder="Address" className="w-full p-3 border rounded-xl" />
            <input {...register("city")} placeholder="City" className="w-full p-3 border rounded-xl" />
            <input {...register("state")} placeholder="State" className="w-full p-3 border rounded-xl" />
          </>
        )}

        {role === "donor" && (
          <>
            <input {...register("blood_type")} placeholder="Blood Type" className="w-full p-3 border rounded-xl" />
            <input {...register("last_donation")} type="date" className="w-full p-3 border rounded-xl" />
            <input {...register("city")} placeholder="City" className="w-full p-3 border rounded-xl" />
            <input {...register("state")} placeholder="State" className="w-full p-3 border rounded-xl" />
            <select {...register("contact_preference")} className="w-full p-3 border rounded-xl">
              <option value="email">Email</option>
              <option value="phone">Phone</option>
              <option value="both">Both</option>
            </select>
          </>
        )}

        {role === "hospital" && (
          <>
            <input {...register("name")} placeholder="Hospital Name" className="w-full p-3 border rounded-xl" />
            <input {...register("address")} placeholder="Address" className="w-full p-3 border rounded-xl" />
            <input {...register("city")} placeholder="City" className="w-full p-3 border rounded-xl" />
            <input {...register("state")} placeholder="State" className="w-full p-3 border rounded-xl" />
            <input {...register("phone")} placeholder="Phone" className="w-full p-3 border rounded-xl" />
            <input {...register("email")} placeholder="Email" className="w-full p-3 border rounded-xl" />
            <input {...register("services")} placeholder="Services (comma separated)" className="w-full p-3 border rounded-xl" />
            <label className="flex gap-2 items-center">
              <input type="checkbox" {...register("thalassemia_specialist")} />
              Thalassemia Specialist
            </label>
            <input {...register("latitude")} placeholder="Latitude" type="number" step="0.0001" className="w-full p-3 border rounded-xl" />
            <input {...register("longitude")} placeholder="Longitude" type="number" step="0.0001" className="w-full p-3 border rounded-xl" />
          </>
        )}

        <button 
          type="submit" 
          disabled={isLoading}
          className="w-full bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700 disabled:opacity-50"
        >
          {isLoading ? 'Signing up...' : 'Sign Up'}
        </button>
      </form>
    </div>
  );
}