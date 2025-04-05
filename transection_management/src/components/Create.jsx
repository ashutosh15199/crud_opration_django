import { useState } from "react";
import Logout from "../pages/Logout";

const Create = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState({ productName: "", price: "" });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(""); // State to show success or error message

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    if (!token) {
      setMessage("Please Login!");
      return;
    }
    if (role !== "admin" && role !== "user") {
      setMessage("❌ You are not authorized to perform this action.");
      return;
    }
    setLoading(true);
    setMessage("");
    const requestData = {
      title: formData.productName, // Convert `productName` to `title`
      amount: Number(formData.price), // Convert `price` to `amount` (ensure it's a number)
      transection_type: "CREDIT", // Add missing `transection_type`
    }; // Reset message before request
    console.log("Submitting Data:", requestData);
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/transections/create/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(requestData),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to create product!");
      }

      const data = await response.json();
      console.log("Product Created", data);
      setMessage("✅ Your product has been created successfully!"); // Set success message
      setFormData({ productName: "", price: "" });
      setIsOpen(false);
    } catch (e) {
      setMessage(`❌ Error: ${e.message}`); // Set error message
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative">
      <Logout />
      {/* Blur effect on content when modal is open */}
      <div className={`flex flex-col items-center justify-center   transition-all duration-300 ${isOpen ? "blur-sm" : ""}`}>
        {/* Success/Error Message */}
        {message && (
          <div
            className={`p-3 text-center mb-4 w-96 rounded-lg ${message.startsWith("✅")
                ? "bg-green-100 text-green-700"
                : "bg-red-100 text-red-700"
              }`}
          >
            {message}
          </div>
        )}

        {/* Button to Open Modal */}
        <button
          onClick={() => setIsOpen(true)}
          className="px-6 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700"
        >
          Add Product
        </button>
      </div>

      {/* Modal Form */}
      {isOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 className="text-xl font-semibold mb-4">Add Product</h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Product Name Field */}
              <div>
                <label className="block text-sm font-medium">Product Name</label>
                <input
                  type="text"
                  name="productName"
                  value={formData.productName}
                  onChange={handleChange}
                  required
                  className="w-full p-2 border border-gray-300 rounded-lg"
                />
              </div>

              {/* Price Field */}
              <div>
                <label className="block text-sm font-medium">Price</label>
                <input
                  type="number"
                  name="price"
                  value={formData.price}
                  onChange={handleChange}
                  required
                  className="w-full p-2 border border-gray-300 rounded-lg"
                />
              </div>

              {/* Buttons */}
              <div className="flex justify-between">
                <button
                  type="button"
                  onClick={() => setIsOpen(false)}
                  className="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                >
                  {loading ? "Submitting..." : "Submit"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Create;
