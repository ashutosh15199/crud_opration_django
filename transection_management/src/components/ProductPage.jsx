import React, { useState } from "react";
import Get from "./Get";
import Update from "./Update";

const ProductPage = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);

  const handleEdit = (product) => {
    setSelectedProduct(product);
    setIsOpen(true);
  };

  const handleClose = () => {
    setIsOpen(false);
    setSelectedProduct(null);
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/transections/delete/", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id }),
      });

      if (!response.ok) {
        throw new Error("Failed to delete product");
      }

      console.log(`Product with ID ${id} deleted successfully`);
    } catch (error) {
      console.error("Error deleting product:", error.message);
    }
  };

  return (
    <div className="relative">
      <div className={isOpen ? "blur-sm pointer-events-none select-none" : ""}>
        <Get onEdit={handleEdit} onDelete={handleDelete} />
      </div>
      {isOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 z-50">
          <Update isOpen={isOpen} setIsOpen={setIsOpen} product={selectedProduct} onClose={handleClose} />
        </div>
      )}
    </div>
  );
};


export default ProductPage;
