const phoneInput = document.getElementById("phone");
const codeInput = document.getElementById("code");
const loginForm = document.getElementById("login-form");
const otpForm = document.getElementById("otp-form");

let phoneNumber = "";

loginForm.addEventListener("submit", function (e) {
  e.preventDefault();
  phoneNumber = phoneInput.value.trim();

  fetch("http://127.0.0.1:8000/api/customers/send-otp/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone_number: phoneNumber }),
  })
    .then((res) => {
      if (res.ok) {
        loginForm.classList.add("hidden");
        otpForm.classList.remove("hidden");
      } else {
        alert("Failed to send OTP.");
      }
    })
    .catch((err) => console.error(err));
});

otpForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const code = codeInput.value.trim();

  fetch("http://127.0.0.1:8000/api/customers/verify-otp/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone_number: phoneNumber, code }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.access && data.refresh) {
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        alert("Login successful!");
        window.location.href = "/frontend/html/products.html";
      } else {
        alert("Invalid code or login failed.");
      }
    })
    .catch((err) => console.error(err));
});
