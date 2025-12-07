import React from 'react';
import { useCheckoutController } from '../hooks/useCheckoutController';
import { useNavigate } from 'react-router-dom';
import logoImg from '../assets/logo.png'; // Imported logo

const CheckoutPage = () => {
  const navigate = useNavigate();
  const { 
    cartItems, 
    loading, 
    totals, 
    paymentMethod, 
    handlePaymentMethodChange, 
    handleRemoveItem 
  } = useCheckoutController();

  if (loading) return <div className="p-10 text-center">Loading cart...</div>;

  return (
    <div className="font-display">
      <div className="relative flex h-auto min-h-screen w-full flex-col bg-background-light dark:bg-background-dark group/design-root overflow-x-hidden text-text-body-light dark:text-text-body-dark">
        <div className="layout-container flex h-full grow flex-col">
          
          {/* HEADER */}
          <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-border-light dark:border-border-dark px-6 md:px-10 lg:px-20 py-4">
            <div className="flex items-center gap-4 cursor-pointer" onClick={() => navigate('/')}>
              <div className="size-6 text-primary">
                <img src={logoImg} alt="MUDemy Logo" className="h-8 w-auto"/>
              </div>
              <h2 className="text-xl font-bold tracking-tight">MUDemy</h2>
            </div>
            <nav className="hidden md:flex flex-1 justify-center items-center gap-9">
              <a className="text-sm font-medium hover:text-primary" href="#">Courses</a>
              <a className="text-sm font-medium hover:text-primary" href="#">My Learning</a>
              <a className="text-sm font-medium hover:text-primary" href="#">About Us</a>
            </nav>
            <div className="flex items-center gap-3">
              <button className="flex h-10 w-10 cursor-pointer items-center justify-center overflow-hidden rounded-full hover:bg-black/5 dark:hover:bg-white/10">
                <span className="material-symbols-outlined text-text-secondary-light dark:text-text-secondary-dark">shopping_cart</span>
              </button>
              <button className="flex h-10 w-10 cursor-pointer items-center justify-center overflow-hidden rounded-full hover:bg-black/5 dark:hover:bg-white/10">
                <span className="material-symbols-outlined text-text-secondary-light dark:text-text-secondary-dark">notifications</span>
              </button>
              <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" style={{ backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAtA21y5vixltxudbDKTJ5SjeLbpYrf4ZzJ5OfaqE4XD_Qq6WE_HnUEOtf-7bozkMQR7ns-t-yN7SQrxjOYZ465XMO5G6IrkhQnUDNARYQLhTWMEuQyqqMiEJns9z61H5NmX0utOOFoRPORB-Sh9X8AoH6O8bCJsnRR34OSruoe_pe7LagtM0TmgQ2hbnvZYJLjbhc3HPDOrp2FltCdICsh0EXra0fCZ-iVzU4HJAu3euhAoAqHkm_PvykMBHBR_yyXKV40pUOVVJs")' }}></div>
            </div>
          </header>

          <main className="flex-1 px-4 sm:px-6 lg:px-8 py-10">
            <div className="mx-auto max-w-7xl">
              <div className="flex flex-wrap justify-between gap-3 pb-8">
                <p className="text-4xl font-black tracking-tighter">Checkout</p>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12">
                
                {/* --- LEFT COLUMN: CART ITEMS --- */}
                <div className="lg:col-span-2 space-y-6">
                  <h3 className="text-2xl font-bold tracking-tight">Shopping Cart</h3>
                  <p className="text-base font-normal text-text-secondary-light dark:text-text-secondary-dark">
                    {cartItems.length} Courses in Cart
                  </p>
                  
                  <div className="border-t border-border-light dark:border-border-dark divide-y divide-border-light dark:divide-border-dark">
                    {cartItems.map((item) => (
                      <div key={item.id} className="flex gap-4 bg-transparent px-0 py-6 justify-between items-start">
                        <div className="flex items-start gap-4 flex-1">
                          <div 
                            className="bg-center bg-no-repeat aspect-video bg-cover rounded-lg h-[70px] w-[124px] flex-shrink-0" 
                            style={{ backgroundImage: `url("${item.image}")` }}
                          ></div>
                          <div className="flex flex-1 flex-col justify-center">
                            <p className="text-base font-semibold">{item.title}</p>
                            <p className="text-sm font-normal text-text-secondary-light dark:text-text-secondary-dark">By {item.author}</p>
                            <div className="flex items-baseline gap-2 mt-1">
                              <p className="text-lg font-bold text-accent">${item.price}</p>
                              <p className="text-sm font-normal text-text-secondary-light dark:text-text-secondary-dark line-through">${item.originalPrice}</p>
                            </div>
                          </div>
                        </div>
                        <div className="shrink-0 flex flex-col items-end gap-2 text-sm">
                          <button 
                            onClick={() => handleRemoveItem(item.id)}
                            className="font-medium text-primary hover:underline"
                          >
                            Remove
                          </button>
                          <button className="font-medium text-text-secondary-light dark:text-text-secondary-dark hover:underline">
                            Save for Later
                          </button>
                        </div>
                      </div>
                    ))}
                    {cartItems.length === 0 && (
                      <div className="py-8 text-center text-text-secondary-light">Your cart is empty.</div>
                    )}
                  </div>
                </div>

                {/* --- RIGHT COLUMN: SUMMARY & PAYMENT --- */}
                <div className="lg:col-span-1">
                  
                  {/* Summary Box */}
                  <div className="space-y-6 rounded-lg bg-secondary dark:bg-background-dark p-6 border border-border-light dark:border-border-dark">
                    <h3 className="text-2xl font-bold tracking-tight">Summary</h3>
                    <div className="space-y-3 text-sm">
                      <div className="flex justify-between">
                        <span className="text-text-secondary-light dark:text-text-secondary-dark">Subtotal</span>
                        <span>${totals.subtotal}</span>
                      </div>
                      <div className="flex justify-between items-center text-text-secondary-light dark:text-text-secondary-dark">
                        <span>Discount</span>
                        <span>${totals.discount}</span>
                      </div>
                    </div>
                    <div className="border-t border-border-light dark:border-border-dark pt-4">
                      <div className="flex justify-between font-bold text-lg">
                        <span>Total</span>
                        <span className="text-primary">${totals.total}</span>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <input className="flex-1 rounded-md border-border-light dark:border-border-dark bg-background-light dark:bg-zinc-800 text-sm focus:border-primary focus:ring-primary p-2" placeholder="Coupon Code" type="text"/>
                      <button className="px-4 py-2 rounded-md border border-primary text-primary font-semibold text-sm hover:bg-primary/10">Apply</button>
                    </div>
                  </div>

                  {/* Payment Method */}
                  <div className="space-y-6 mt-8">
                    <h3 className="text-2xl font-bold tracking-tight">Payment Method</h3>
                    <div className="space-y-4">
                      <label className={`flex items-center gap-4 p-4 border rounded-lg cursor-pointer ${paymentMethod === 'card' ? 'border-primary bg-primary/5 dark:bg-primary/20' : 'border-border-light dark:border-border-dark hover:border-primary'}`}>
                        <input 
                          type="radio" 
                          name="payment_method" 
                          checked={paymentMethod === 'card'} 
                          onChange={() => handlePaymentMethodChange('card')}
                          className="text-primary focus:ring-primary" 
                        />
                        <span className="font-semibold">Credit/Debit Card</span>
                      </label>
                      <label className={`flex items-center gap-4 p-4 border rounded-lg cursor-pointer ${paymentMethod === 'paypal' ? 'border-primary bg-primary/5 dark:bg-primary/20' : 'border-border-light dark:border-border-dark hover:border-primary'}`}>
                        <input 
                          type="radio" 
                          name="payment_method" 
                          checked={paymentMethod === 'paypal'} 
                          onChange={() => handlePaymentMethodChange('paypal')}
                          className="text-primary focus:ring-primary" 
                        />
                        <span className="font-semibold">PayPal</span>
                      </label>
                    </div>

                    {/* Credit Card Form (Only show if Card selected) */}
                    {paymentMethod === 'card' && (
                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium mb-1" htmlFor="card-number">Card Number</label>
                          <input className="w-full rounded-md border-border-light dark:border-border-dark bg-background-light dark:bg-zinc-800 focus:border-primary focus:ring-primary p-2" id="card-number" placeholder="•••• •••• •••• ••••" type="text"/>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium mb-1" htmlFor="expiry-date">Expiration Date</label>
                            <input className="w-full rounded-md border-border-light dark:border-border-dark bg-background-light dark:bg-zinc-800 focus:border-primary focus:ring-primary p-2" id="expiry-date" placeholder="MM / YY" type="text"/>
                          </div>
                          <div>
                            <label className="block text-sm font-medium mb-1" htmlFor="cvc">CVC</label>
                            <input className="w-full rounded-md border-border-light dark:border-border-dark bg-background-light dark:bg-zinc-800 focus:border-primary focus:ring-primary p-2" id="cvc" placeholder="•••" type="text"/>
                          </div>
                        </div>
                      </div>
                    )}

                    <button className="w-full bg-primary text-white font-bold py-3 rounded-lg text-base hover:bg-primary/90 transition-colors">Complete Checkout</button>
                    <div className="flex items-center justify-center gap-2 text-sm text-text-secondary-light dark:text-text-secondary-dark">
                      <span className="material-symbols-outlined text-base">lock</span>
                      <span>Secure SSL Encrypted Payment</span>
                    </div>
                  </div>

                </div>
              </div>
            </div>
          </main>

          <footer className="mt-auto border-t border-border-light dark:border-border-dark text-text-secondary-light dark:text-text-secondary-dark text-sm">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8 flex flex-col sm:flex-row justify-between items-center gap-4">
              <p>© 2024 MUDemy, Inc.</p>
              <div className="flex gap-6">
                <a className="hover:text-primary hover:underline" href="#">Terms of Service</a>
                <a className="hover:text-primary hover:underline" href="#">Privacy Policy</a>
                <a className="hover:text-primary hover:underline" href="#">Help Center</a>
              </div>
            </div>
          </footer>

        </div>
      </div>
    </div>
  );
};

export default CheckoutPage;