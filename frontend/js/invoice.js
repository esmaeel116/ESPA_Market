const container = document.getElementById("invoice-details");
const token = localStorage.getItem("access");
if (!token) {
  alert("Please login first.");
  window.location.href = "/frontend/html/login.html";
}

// Extract order ID from query string (e.g., ?id=3)
const urlParams = new URLSearchParams(window.location.search);
const orderId = urlParams.get("id");
if (!orderId) {
  container.innerHTML = "<p class='text-red-500'>Order ID is missing.</p>";
  throw new Error("Missing order ID.");
}

fetch(`http://127.0.0.1:8000/api/orders/${orderId}/`, {
  headers: {
    Authorization: "Bearer " + token,
  },
})
  .then(res => res.json())
  .then(order => {
    const items = order.items
      .map(
        item => `
      <tr class="border-b">
        <td class="py-2">${item.product}</td>
        <td class="py-2 text-center">${item.quantity}</td>
        <td class="py-2 text-right">${item.unit_price} Toman</td>
      </tr>`
      )
      .join("");

    const total = order.items.reduce((sum, i) => sum + i.quantity * i.unit_price, 0);

    container.innerHTML = `
      <div class="text-sm">
        <p><strong>Order ID:</strong> ${order.id}</p>
        <p><strong>Status:</strong> ${order.status}</p>
        <p><strong>Date:</strong> ${new Date(order.created_at).toLocaleString()}</p>
        <p><strong>Payment:</strong> ${order.is_paid ? "Paid" : "Unpaid"}</p>
      </div>

      <table class="w-full mt-4 border text-sm">
        <thead class="bg-[#ebffff]">
          <tr>
            <th class="text-left py-2 px-2">Product</th>
            <th class="text-center py-2">Qty</th>
            <th class="text-right py-2 px-2">Price</th>
          </tr>
        </thead>
        <tbody>${items}</tbody>
        <tfoot>
          <tr>
            <td colspan="2" class="text-right font-bold py-2 px-2">Total:</td>
            <td class="text-right font-bold py-2 px-2 text-[#10b981]">${total.toLocaleString()} Toman</td>
          </tr>
        </tfoot>
      </table>

      <div class="mt-6 text-center">
        <button onclick="window.print()" class="bg-[#0390b7] text-white px-6 py-2 rounded-lg hover:bg-[#02759a] transition">
          Print Invoice
        </button>
      </div>
    `;
  })
  .catch(err => {
    console.error(err);
    container.innerHTML = "<p class='text-red-500'>Failed to load invoice.</p>";
  });
