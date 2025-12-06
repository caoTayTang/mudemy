import { useState, useEffect } from 'react';
import { courseService } from '../services/courseService';

export const useCheckoutController = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [paymentMethod, setPaymentMethod] = useState('card'); // 'card' or 'paypal'
  
  // Calculate Totals
  const subtotal = cartItems.reduce((acc, item) => acc + item.price, 0);
  const discount = 0; // Logic for coupons could go here
  const total = subtotal - discount;

  useEffect(() => {
    const fetchCart = async () => {
      try {
        const data = await courseService.getCartItems();
        setCartItems(data);
      } catch (error) {
        console.error("Failed to load cart", error);
      } finally {
        setLoading(false);
      }
    };
    fetchCart();
  }, []);

  const handleRemoveItem = (id) => {
    setCartItems(prev => prev.filter(item => item.id !== id));
  };

  const handlePaymentMethodChange = (method) => {
    setPaymentMethod(method);
  };

  return {
    cartItems,
    loading,
    totals: {
      subtotal: subtotal.toFixed(2),
      discount: discount.toFixed(2),
      total: total.toFixed(2)
    },
    paymentMethod,
    handlePaymentMethodChange,
    handleRemoveItem
  };
};