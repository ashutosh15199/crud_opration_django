import React, { useEffect, useState } from "react";
import { FaEdit, FaTrash } from "react-icons/fa";
import Update from "./Update";
import image from '../assets/image/1.jpg';

const Get = ({ onEdit, onDelete }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    const token = localStorage.getItem("token");
  
    if (!token) {
      setError("❌ Unauthorized: Please login to view this content.");
      setLoading(false);
      return;
    }
  
    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8000/api/transections/get/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}` // ✅ CORRECT HEADER
        },
      });
  
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to fetch products");
      }
  
      const data = await response.json();
      setProducts(data.data || []);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };
  
  

  const handleDelete = async (id) => {
    try {
      await onDelete(id); // Call delete API from ProductPage
      setProducts(products.filter(product => product.id !== id)); // Remove from UI
    } catch (error) {
      console.error("Failed to delete product:", error);
    }
  };

  return (
    <div className="relative">
      <div className={`p-6 transition-all duration-300 ${isOpen ? "blur-sm" : ""}`}>
        <h2 className="text-2xl font-semibold text-center mb-6">Product List</h2>

        {error && <p className="text-red-500 text-center">{error}</p>}

        {loading ? (
          <p className="text-center text-gray-600">Loading...</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {products.length > 0 ? (
              products.map((product) => (
                <div key={product.id} className="bg-white p-4 rounded-lg shadow-lg relative">
                  {/* Delete Button */}
                  <div 
                    className="absolute top-2 left-2 bg-white p-1 rounded-full shadow-md cursor-pointer"
                    onClick={() => handleDelete(product.id)}
                  >
                    <FaTrash size={20} className="text-red-500 hover:text-red-700" />
                  </div>

                  {/* Edit Button */}
                  <div 
                    className="absolute top-2 right-2 bg-white p-1 rounded-full shadow-md cursor-pointer"
                    onClick={() => onEdit(product)}
                  >
                    <FaEdit size={20} className="text-blue-500 hover:text-blue-700" />
                  </div>

                  <img
                    src={image}
                    alt={product.title}
                    className="w-full h-50 object-cover rounded-lg mb-4"
                  />

                  <h3 className="text-lg font-semibold">{product.title}</h3>
                  <p className="text-gray-600">Price: ₹{product.amount}</p>
                </div>
              ))
            ) : (
              <p className="text-center text-gray-500">No products found.</p>
            )}
          </div>
        )}
      </div>

      {/* Update Form Modal */}
      <Update isOpen={isOpen} setIsOpen={setIsOpen} product={selectedProduct} onClose={() => setIsOpen(false)} />
    </div>
  );
};

export default Get;
