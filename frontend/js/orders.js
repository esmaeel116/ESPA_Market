const orderList = document.getElementById("order-list");

const token = localStorage.getItem("access");
if (!token) {
  alert("Please login first.");
  window.location.href = "/frontend/html/login.html";
}

fetch("http://127.0.0.1:8000/api/orders/", {
  headers: { Authorization: "Bearer " + token },
})
  .then((res) => res.json())
  .then((orders) => {
    if (!orders.length) {
      orderList.innerHTML = "<p class='text-center text-gray-500'>No orders found.</p>";
      return;
    }

    orders.forEach((order) => {
      const paidLabel = order.is_paid
        ? `<span class="text-green-600">Paid</span>`
        : `<span class="text-red-500">Unpaid</span>`;

      let itemsHtml = "";
      order.items.forEach((item) => {
        itemsHtml += `
          <li class="text-sm text-gray-700">
            ${item.product} × ${item.quantity} - ${item.unit_price} Toman
          </li>`;
      });

      orderList.innerHTML += `
        <div class="bg-white rounded-lg shadow p-4">
          <div class="flex justify-between items-center">
            <h2 class="font-semibold">Order #${order.id}</h2>
            <span>${paidLabel}</span>
          </div>
          <p class="text-sm text-gray-500 mt-1">Created at: ${new Date(order.created_at).toLocaleString()}</p>
          <ul class="mt-3 space-y-1">${itemsHtml}</ul>
          ${
            order.is_paid
              ? `<a href="http://127.0.0.1:8000/api/orders/${order.id}/invoice/" target="_blank" class="inline-block mt-4 text-sm text-[#0390b7] hover:underline">View Invoice</a>`
              : ""
          }
        </div>
      `;
    });
  })
  .catch((err) => {
    console.error(err);
    orderList.innerHTML = `<p class='text-red-500'>Error loading orders.</p>`;
  });
