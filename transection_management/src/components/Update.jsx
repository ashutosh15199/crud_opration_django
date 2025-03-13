import React, { useEffect, useState } from "react";

const Update = ({ isOpen, setIsOpen, product, onClose }) => {
  const [formData, setFormData] = useState({
    productId: "",
    productName: "",
    price: "",
    transection_type: "CREDIT", // Default value
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (product) {
      setFormData({
        productId: product.id,
        productName: product.title,
        price: Math.abs(Number(product.amount)), // Ensure price is positive for input
        transection_type: product.transection_type || "CREDIT",
      });
    }
  }, [product]);

  const handleChange = (e) => {
    const { name, value } = e.target;
  
    setFormData((prevData) => ({
      ...prevData,
      [name]: name === "price" ? Math.abs(Number(value)) || "" : value, // Ensure price is always positive
    }));
  };
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    const requestData = {
      id: formData.productId,
      title: formData.productName,
      amount: formData.transection_type === "DEBIT" ? -Math.abs(Number(formData.price)) : Math.abs(Number(formData.price)), // Handle negative amounts correctly
      transection_type: formData.transection_type, // User-selected value
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/api/transections/update/", {
        method: "PUT", 
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error("Failed to update product!");
      }

      const data = await response.json();

      setMessage("✅ Your product has been updated successfully!");

      // Update formData with latest API response
      setFormData({
        productId: data.data.id,
        productName: data.data.title,
        price: Math.abs(data.data.amount),
        transection_type: data.data.transection_type,
      });

      // Close modal after a short delay
      setTimeout(() => {
        setIsOpen(false);
      }, 1000);

    } catch (e) {
      setMessage(`❌ Error: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    isOpen && (
      <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg w-96">
          <h2 className="text-xl font-semibold mb-4">Update Product</h2>

          {message && (
            <div
              className={`p-3 text-center mb-4 rounded-lg ${
                message.startsWith("✅") ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
              }`}
            >
              {message}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
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

            <div>
              <label className="block text-sm font-medium">Price</label>
              <input
                type="number"
                name="price"
                value={Math.abs(product.amount)}
                onChange={handleChange}
                required
                className="w-full p-2 border border-gray-300 rounded-lg"
              />
            </div>

            {/* Transaction Type Dropdown */}
            <div>
              <label className="block text-sm font-medium">Transaction Type</label>
              <select
                name="transection_type"
                value={formData.transection_type}
                onChange={handleChange}
                className="w-full p-2 border border-gray-300 rounded-lg"
              >
                <option value="CREDIT">Credit</option>
                <option value="DEBIT">Debit</option>
              </select>
            </div>

            <div className="flex justify-between">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                {loading ? "Updating..." : "Update"}
              </button>
            </div>
          </form>
        </div>
      </div>
    )
  );
};

export default Update;
