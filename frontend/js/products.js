const container = document.getElementById("product-list");

fetch("http://127.0.0.1:8000/api/products/products/")
  .then((res) => res.json())
  .then((data) => {
    container.innerHTML = "";
    data.forEach((product) => {
      container.innerHTML += `
        <div class="bg-white rounded-xl shadow hover:shadow-lg transition p-4 flex flex-col justify-between">
          <img src="${product.image}" alt="${product.title}" class="w-full h-40 object-cover rounded-md mb-3" />
          <h2 class="text-lg font-semibold">${product.title}</h2>
          <p class="text-sm text-gray-500 mt-1 mb-2">${product.category || "No category"}</p>
          <p class="text-[#10b981] font-bold text-md mb-3">${Number(product.price).toLocaleString()}$</p>
          <button onclick="addToCart(${product.id}, ${product.price})"
            class="mt-auto bg-[#0390b7] hover:bg-[#02759a] text-white px-4 py-2 rounded-lg transition text-sm">
            Add to cart
          </button>
        </div>
      `;
    });
  })
  .catch((err) => {
    container.innerHTML = `<p class="text-red-500">Error loading products</p>`;
    console.error(err);
  });

function addToCart(productId, unitPrice) {
  const token = localStorage.getItem("access");
  if (!token) {
    alert("Please log in first.");
    window.location.href = "/frontend/html/login.html";
    return;
  }

  fetch("http://127.0.0.1:8000/api/cart-items/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
    },
    body: JSON.stringify({
      product_id: productId,
      quantity: 1,
      unit_price: unitPrice,
    }),
  })
    .then((res) => {
      if (res.ok) {
        alert("Successfully added to cart.");
      } else {
        alert("Error adding to cart.");
      }
    })
    .catch((err) => console.error(err));
}
