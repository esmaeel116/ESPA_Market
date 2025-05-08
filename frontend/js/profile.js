const token = localStorage.getItem("access");
if (!token) {
  alert("Please login first.");
  window.location.href = "/frontend/html/login.html";
}

const profileBox = document.getElementById("profile-info");
const logoutBtn = document.getElementById("logout-btn");

fetch("http://127.0.0.1:8000/api/customers/me/", {
  headers: { Authorization: "Bearer " + token },
})
  .then((res) => res.json())
  .then((data) => {
    profileBox.innerHTML = `
      <p><strong>Full Name:</strong> ${data.full_name || "N/A"}</p>
      <p><strong>Phone:</strong> ${data.phone_number}</p>
      <p><strong>Joined:</strong> ${new Date(data.created_at).toLocaleDateString()}</p>
    `;
  })
  .catch((err) => {
    console.error(err);
    profileBox.innerHTML = "<p class='text-red-500'>Error loading profile.</p>";
  });

logoutBtn.addEventListener("click", () => {
  localStorage.clear();
  alert("You have been logged out.");
  window.location.href = "/frontend/html/login.html";
});
