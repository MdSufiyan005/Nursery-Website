// Define function immediately - available right away
// In external JS file
      function toggleMenu() {
        const navLinks = document.querySelector(".nav-links");
        const blurOverlay = document.querySelector(".blur-overlay");

        if (!navLinks || !blurOverlay) {
          console.error("Navigation links or blur overlay not found.");
          return;
        }

        navLinks.classList.toggle("open");
        blurOverlay.classList.toggle("active");
      }

      // Additional DOM-related logic after DOM is loaded
      document.addEventListener("DOMContentLoaded", () => {
        const blurOverlay = document.querySelector(".blur-overlay");
        if (blurOverlay) {
          blurOverlay.addEventListener("click", () => {
            const navLinks = document.querySelector(".nav-links");
            if (!navLinks) {
              console.error("Navigation links not found.");
              return;
            }
            blurOverlay.classList.remove("active");
            navLinks.classList.remove("open");
          });
        }
      });