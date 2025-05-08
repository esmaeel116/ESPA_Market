const cartContainer = document.getElementById("cart-items");
const cartTotalDisplay = document.getElementById("cart-total");
const checkoutBtn = document.getElementById("checkout-btn");

const token = localStorage.getItem("access");
if (!token) {
  alert("Please login first.");
  window.location.href = "/frontend/html/login.html";
}

function loadCart() {
  fetch("http://127.0.0.1:8000/api/cart-items/", {
    headers: { Authorization: "Bearer " + token },
  })
    .then((res) => res.json())
    .then((data) => {
      cartContainer.innerHTML = "";
      let total = 0;

      data.forEach((item) => {
        total += item.unit_price * item.quantity;

        cartContainer.innerHTML += `
          <div class="flex items-center justify-between bg-white p-4 rounded-lg shadow">
            <div>
              <h2 class="font-semibold">${item.product.title}</h2>
              <p class="text-sm text-gray-500">${item.unit_price} Toman × ${item.quantity}</p>
            </div>
            <button onclick="removeItem(${item.id})" class="text-red-500 hover:text-red-600">Remove</button>
          </div>
        `;
      });

      cartTotalDisplay.textContent = total.toLocaleString() + " Toman";
    })
    .catch((err) => {
      console.error(err);
      cartContainer.innerHTML = `<p class="text-red-500">Error loading cart.</p>`;
    });
}

function removeItem(itemId) {
  fetch(`http://127.0.0.1:8000/api/cart-items/${itemId}/`, {
    method: "DELETE",
    headers: { Authorization: "Bearer " + token },
  }).then(() => {
    loadCart();
  });
}

checkoutBtn.addEventListener("click", () => {
  fetch("http://127.0.0.1:8000/api/checkout/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
    },
  })
    .then((res) => {
      if (res.ok) {
        alert("Order created successfully!");
        window.location.href = "/frontend/html/orders.html";
      } else {
        return res.json().then((data) => alert(data.detail || "Checkout failed."));
      }
    })
    .catch((err) => console.error(err));
});

loadCart();
