import React, { useState } from 'react';
import {useNavigate } from 'react-router-dom'
const Login = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState(false);
  const [message, setMessage] = useState("");
const navigate=useNavigate();
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevents page reload

    try {
      const response = await fetch("http://127.0.0.1:8000/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      console.log(data);
      if (response.ok) {
        setMessage("Login Successful!");
        setError(false);
        setFormData({ email: "", password: "" });
        localStorage.setItem("token",data.access);
        localStorage.setItem("role",data.role)
        setTimeout(()=>{
            navigate('/');

        },1000);
      } else {
        setMessage(data.message || "Login failed");
        setError(true);
      }
    } catch (e) {
      setError(true);
      setMessage("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="flex justify-center items-center mt-30 bg-gray-100">
      <div className="border w-[700px] h-[500px] rounded-2xl bg-gray-200 shadow-lg shadow-gray-700 p-10 flex flex-col items-center">
        <h1 className="text-4xl font-extrabold text-gray-600 drop-shadow-lg mb-6">
          Login Page
        </h1>
        {/* Wrap inputs and button inside a form */}
        <form onSubmit={handleSubmit} className="w-full flex flex-col items-center mt-10">
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter your email"
            className="w-full p-3 border-2 border-gray-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 mt-4"
          />
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            className="w-full p-3 border-2 border-gray-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 mt-10"
          />
          <button
            type="submit"
            className="text-[20px] font-bold border-2 w-[100px] h-[50px] bg-gray-600 text-white mt-10 rounded-lg"
          >
            Log In
          </button>
        </form>

        {/* Show login message */}
        {message && (
          <p className={`mt-4 ${error ? 'text-red-600' : 'text-green-600'}`}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
};

export default Login;
