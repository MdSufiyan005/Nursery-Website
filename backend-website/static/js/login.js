    // (function() {
    //   'use strict';

    //   const loginForm = document.getElementById('loginForm');
    //   const usernameInput = loginForm.username;
    //   const passwordInput = loginForm.password;

    //   loginForm.addEventListener('submit', e => {
    //     e.preventDefault();

    //     if (!loginForm.checkValidity()) {
    //       loginForm.reportValidity();
    //       return;
    //     }

    //     const username = usernameInput.value.trim();
    //     const password = passwordInput.value;

    //     if(username.length >= 3 && password.length >= 6){
    //       alert(`Welcome, ${username}! Login successful.`);
    //         // Example: perform AJAX request here, then on success:
    //       window.location.href = '/home/';  // redirect to home page
    //       loginForm.reset();
    //       usernameInput.focus();
    //     } else {
    //       alert("Invalid username or password format.");
    //     }
    //   });

    //   document.getElementById('forgotPasswordLink').addEventListener('click', e => {
    //     e.preventDefault();
    //     alert('Password reset feature coming soon.');
    //   });
    // })();
      const loginBtn = document.getElementById("loginBtn");
      const signupBtn = document.getElementById("signupBtn");
      const loginForm = document.getElementById("loginForm");
      const signupForm = document.getElementById("signupForm");

      loginBtn.onclick = () => {
        loginForm.classList.add("active");
        signupForm.classList.remove("active");
        loginBtn.classList.add("active");
        signupBtn.classList.remove("active");
      };

      signupBtn.onclick = () => {
        signupForm.classList.add("active");
        loginForm.classList.remove("active");
        signupBtn.classList.add("active");
        loginBtn.classList.remove("active");
      };