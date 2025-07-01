const loginBtn = document.getElementById("loginBtn");
      const signupBtn = document.getElementById("signupBtn");
      const loginForm = document.getElementById("loginForm");
      const signupForm = document.getElementById("signupForm");

      function setFormEnabled(form, enabled) {
        Array.from(form.elements).forEach(el => {
          if (el.tagName !== 'DIV') el.disabled = !enabled;
        });
      }

      // Initial state: login form enabled, signup form disabled
      setFormEnabled(loginForm, true);
      setFormEnabled(signupForm, false);

      loginBtn.onclick = () => {
        loginForm.classList.add("active");
        signupForm.classList.remove("active");
        loginBtn.classList.add("active");
        signupBtn.classList.remove("active");
        setFormEnabled(loginForm, true);
        setFormEnabled(signupForm, false);
      };

      signupBtn.onclick = () => {
        signupForm.classList.add("active");
        loginForm.classList.remove("active");
        signupBtn.classList.add("active");
        loginBtn.classList.remove("active");
        setFormEnabled(signupForm, true);
        setFormEnabled(loginForm, false);
      };