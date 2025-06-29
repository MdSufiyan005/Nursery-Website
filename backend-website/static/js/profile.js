      function toggleMobileMenu() {
        const menu = document.getElementById("dropdownMenu");
        const blurOverlay = document.querySelector(".blur-overlay");

        menu.classList.toggle("show");
        blurOverlay.classList.toggle("active");
      }

      function switchTab(tabId) {
        document
          .querySelectorAll(".tab-content")
          .forEach((tab) => tab.classList.remove("active"));

        const targetTab = document.getElementById(tabId);
        if (targetTab) {
          targetTab.classList.add("active");
        }

        document
          .querySelectorAll(".tab-btn")
          .forEach((btn) => btn.classList.remove("active"));

        const buttons = Array.from(document.querySelectorAll(".tab-btn"));
        const activeButton = buttons.find(
          (b) => b.textContent.trim().toLowerCase() === tabId.toLowerCase()
        );

        if (activeButton) activeButton.classList.add("active");
      }

      function previewImage(event) {
        const reader = new FileReader();
        reader.onload = function () {
          const output = document.getElementById("profile-img");
          output.src = reader.result;
        };
        reader.readAsDataURL(event.target.files[0]);
      }

      // Close menu when clicking on blur overlay
      document
        .querySelector(".blur-overlay")
        .addEventListener("click", function () {
          const menu = document.getElementById("dropdownMenu");
          const blurOverlay = document.querySelector(".blur-overlay");

          menu.classList.remove("show");
          blurOverlay.classList.remove("active");
        });
              document.addEventListener("DOMContentLoaded", function () {
        var hamburger = document.querySelector(".hamburger");
        var sidebar = document.getElementById("sidebar");

        function toggleSidebar() {
          sidebar.classList.toggle("show");
        }

        if (hamburger) {
          hamburger.addEventListener("click", function (e) {
            e.stopPropagation();
            toggleSidebar();
          });
        }

        // Close sidebar when clicking outside of it (on content)
        document.addEventListener("click", function (e) {
          if (
            sidebar.classList.contains("show") &&
            !sidebar.contains(e.target) &&
            !hamburger.contains(e.target)
          ) {
            sidebar.classList.remove("show");
          }
        });

        window.addEventListener("resize", function () {
          if (window.innerWidth > 768) {
            sidebar.classList.remove("show");
          }
        });
      });