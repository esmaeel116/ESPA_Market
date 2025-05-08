const token = localStorage.getItem("access");
const box = document.getElementById("confirmation-box");

if (!token) {
  alert("Please login to confirm payment.");
  window.location.href = "/frontend/html/login.html";
}

// شبیه‌سازی تایید پرداخت بعد از چند ثانیه
setTimeout(() => {
  fetch("http://127.0.0.1:8000/api/orders/confirm-payment/", {
    method: "GET",
    headers: { Authorization: "Bearer " + token },
  })
    .then(res => res.json())
    .then(data => {
      box.innerHTML = `
        <h2 class="text-2xl font-bold text-[#10b981] mb-4">Payment Successful</h2>
        <p class="mb-6 text-gray-700">Your order has been confirmed successfully.</p>
        <a href="/frontend/html/orders.html"
           class="bg-[#0390b7] text-white px-5 py-2 rounded hover:bg-[#02759a] transition">
          View Orders
        </a>
      `;
    })
    .catch(err => {
      console.error(err);
      box.innerHTML = `
        <h2 class="text-xl font-bold text-red-500 mb-4">Error</h2>
        <p class="text-gray-600">Something went wrong. Try again later.</p>
      `;
    });
}, 2000);
