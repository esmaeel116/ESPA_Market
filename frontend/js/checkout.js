const token = localStorage.getItem("access");
const container = document.getElementById("checkout-summary");

if (!token) {
  alert("Please login first.");
  window.location.href = "/frontend/html/login.html";
}

fetch("http://127.0.0.1:8000/api/cart/", {
  headers: {
    Authorization: "Bearer " + token,
  },
})
  .then((res) => res.json())
  .then((cartList) => {
    const cart = cartList[0]; // user has only one cart
    if (!cart || !cart.items.length) {
      container.innerHTML = "<p>Your cart is empty.</p>";
      return;
    }

    let total = 0;
    let itemsHtml = "";

    cart.items.forEach((item) => {
      total += item.quantity * item.unit_price;
      itemsHtml += `
        <li class="flex justify-between text-sm text-gray-700 border-b py-2">
          <span>${item.product.title} × ${item.quantity}</span>
          <span>${item.unit_price} Toman</span>
        </li>`;
    });

    container.innerHTML = `
      <ul>${itemsHtml}</ul>
      <div class="text-right font-bold mt-4 text-[#10b981]">Total: ${total.toLocaleString()} Toman</div>

      <div class="mt-6 flex items-center gap-4">
        <input type="text" id="coupon-code" placeholder="Enter coupon code"
          class="px-3 py-2 border rounded w-1/2 focus:outline-none focus:ring-2 focus:ring-[#0390b7]" />
        <button onclick="applyCoupon()" class="bg-[#0390b7] text-white px-4 py-2 rounded hover:bg-[#02759a]">
          Apply
        </button>
      </div>

      <button onclick="proceedToCheckout()"
        class="w-full mt-6 bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition">
        Proceed to Payment
      </button>
    `;
  })
  .catch((err) => {
    console.error(err);
    container.innerHTML = "<p class='text-red-500'>Error loading cart.</p>";
  });

function applyCoupon() {
  const code = document.getElementById("coupon-code").value.trim();
  if (!code) return alert("Enter a valid coupon code");

  localStorage.setItem("applied_coupon", code);
  alert("Coupon applied! It'll be used during checkout.");
}

function proceedToCheckout() {
  const coupon = localStorage.getItem("applied_coupon");

  fetch("http://127.0.0.1:8000/api/checkout/", {
    method: "POST",
    headers: {
      Authorization: "Bearer " + token,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ coupon }),
  })
    .then((res) => res.json())
    .then((data) => {
      alert(`Order #${data.detail || "created"} created successfully.`);
      window.location.href = "/frontend/html/orders.html";
    })
    .catch((err) => console.error(err));
}
