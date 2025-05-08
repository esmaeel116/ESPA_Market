window.addEventListener("DOMContentLoaded", () => {
  const userActions = document.getElementById("user-actions");
  const accessToken = localStorage.getItem("access");

  if (accessToken) {
    userActions.innerHTML = `
      <a href="/frontend/html/profile.html" class="text-sm text-[#063346] hover:text-[#0390b7]">account</a>
      <button id="logout-btn" class="text-sm text-red-500 hover:text-red-600">log out</button>
    `;

    document.getElementById("logout-btn").addEventListener("click", () => {
      localStorage.clear();
      alert("log out successfully!");
      window.location.href = "/frontend/html/login.html";
    });
  } else {

    userActions.innerHTML = `
      <a href="/frontend/html/login.html" class="text-sm bg-[#0390b7] text-white px-4 py-1.5 rounded-lg hover:bg-[#02759a] transition">
        log in
      </a>
    `;
  }
});
