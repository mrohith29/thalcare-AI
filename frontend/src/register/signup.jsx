import { useState } from "react";
import { useForm } from "react-hook-form";
// import { supabase } from "../lib/supabaseClient"; // adjust path accordingly

const roles = ["patient", "donor", "hospital"];

export default function DynamicSignup() {
  const [role, setRole] = useState("patient");
  const { register, handleSubmit, reset } = useForm();

  const onSubmit = async (data) => {
    const { email, password, ...rest } = data;

    if (role === "hospital") {
      const { error } = await supabase.from("hospitals").insert([rest]);
      if (error) alert("Error: " + error.message);
      else alert("Hospital registered!");
    } else {
      const { data: authUser, error: authError } = await supabase.auth.signUp({
        email,
        password,
      });

      if (authError) {
        alert("Signup error: " + authError.message);
        return;
      }

      const user_id = authUser.user?.id;

      if (role === "patient") {
        await supabase.from("profiles").insert([{ id: user_id, ...rest }]);
      } else if (role === "donor") {
        await supabase.from("blood_donors").insert([{ user_id, ...rest }]);
      }

      alert(`${role} signed up successfully!`);
    }

    reset();
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
              placeholder="Email"
              className="input"
              required
            />
            <br /><br />
            <input
              type="password"
              {...register("password")}
              placeholder="Password"
              className="input"
              required
            />
            <br /><br />
          </>
        )}

        {role === "patient" && (
          <>
            <input {...register("first_name")} placeholder="First Name" className="input" />
            <br /> <br />
            <input {...register("last_name")} placeholder="Last Name" className="input" />
            <br /> <br />
            <input {...register("phone")} placeholder="Phone" className="input" />
            <br /> <br />
            <input {...register("date_of_birth")} type="date" className="input" />
            <br /> <br />
            <input {...register("blood_type")} placeholder="Blood Type (e.g. A+)" className="input" />
            <br /> <br />
            <input {...register("address")} placeholder="Address" className="input" />
            <br /> <br />
            <input {...register("city")} placeholder="City" className="input" />
            <br /> <br />
            <input {...register("state")} placeholder="State" className="input" />
            <br /> <br />
          </>
        )}

        {role === "donor" && (
          <>
            <input {...register("blood_type")} placeholder="Blood Type" className="input" />
            <br /><br />
            <input {...register("last_donation")} type="date" className="input" />
            <br /><br />
            <input {...register("city")} placeholder="City" className="input" />
            <br /><br />
            <input {...register("state")} placeholder="State" className="input" />
            <br /><br />
            <select {...register("contact_preference")} className="input">
              <option value="email">Email</option>
              <option value="phone">Phone</option>
              <option value="both">Both</option>
            </select>
            <br /><br />
          </>
        )}

        {role === "hospital" && (
          <>
            <input {...register("name")} placeholder="Hospital Name" className="input" />
            <br /><br />
            <input {...register("address")} placeholder="Address" className="input" />
            <br /><br />
            <input {...register("city")} placeholder="City" className="input" />
            <br /><br />
            <input {...register("state")} placeholder="State" className="input" />
            <br /><br />
            <input {...register("phone")} placeholder="Phone" className="input" />
            <br /><br />
            <input {...register("email")} placeholder="Email" className="input" />
            <br /><br />
            <input
              {...register("services")}
              placeholder="Services (comma separated)"
              className="input"
            />
            <br /><br />
            <label className="flex gap-2 items-center">
              <input type="checkbox" {...register("thalassemia_specialist")} />
              Thalassemia Specialist
            </label>
            <br /><br />
            <input
              {...register("latitude")}
              placeholder="Latitude"
              type="number"
              step="0.0001"
              className="input"
            />
            <br /><br />
            <input
              {...register("longitude")}
              placeholder="Longitude"
              type="number"
              step="0.0001"
              className="input"
            />
            <br /><br />
          </>
        )}

        <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-xl">
          Sign Up
        </button>
      </form>
    </div>
  );
}
