// Ensure all DOM-related code runs after the DOM is fully loaded
      document.addEventListener("DOMContentLoaded", () => {
        // Navigation menu toggle
        function toggleMenu() {
          const navLinks = document.querySelector(".nav-links");
          const blurOverlay = document.querySelector(".blur-overlay");

          const isOpen = navLinks.classList.toggle("open");
          if (isOpen) {
            blurOverlay.classList.add("active");
          } else {
            blurOverlay.classList.remove("active");
          }
        }

        // Attach toggleMenu to the global scope so it can be called from HTML
        window.toggleMenu = toggleMenu;

        // Remove active class from blur-overlay on page load
        const blurOverlay = document.querySelector(".blur-overlay");
        if (blurOverlay) {
          blurOverlay.classList.remove("active");
        }

        // FAQ toggle functionality
        const faqItems = document.querySelectorAll(".faq-item");
        faqItems.forEach((item) => {
          const question = item.querySelector(".faq-question");
          const answer = item.querySelector(".faq-answer");

          // Initialize the answer's max-height for transition
          answer.style.maxHeight = "0px";

          question.addEventListener("click", () => {
            // Check if the current item is already active
            const isActive = item.classList.contains("active");

            // Close all other FAQs
            faqItems.forEach((otherItem) => {
              if (
                otherItem !== item &&
                otherItem.classList.contains("active")
              ) {
                otherItem.classList.remove("active");
                const otherAnswer = otherItem.querySelector(".faq-answer");
                otherAnswer.style.maxHeight = "0px";
              }
            });

            // Toggle the current FAQ
            if (!isActive) {
              item.classList.add("active");
              // Add a small buffer to scrollHeight to ensure full visibility
              answer.style.maxHeight = answer.scrollHeight + 20 + "px";
            } else {
              item.classList.remove("active");
              answer.style.maxHeight = "0px";
            }

            // Handle dynamic content changes (e.g., window resize)
            window.addEventListener("resize", () => {
              if (item.classList.contains("active")) {
                answer.style.maxHeight = answer.scrollHeight + 20 + "px";
              }
            });
          });
        });

        // Populate category cards
        const categories = [
          {
            name: "Indoor Plants",
            img: "https://images.pexels.com/photos/793012/pexels-photo-793012.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            desc: "Perfect for bedrooms, kitchens and desks.",
          },
          {
            name: "Flowering Plants",
            img: "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
            desc: "Bring vibrant colors to your garden!",
          },
          {
            name: "Herbs & Medicinal",
            img: "https://images.unsplash.com/photo-1560180474-e8563fd75bab",
            desc: "Grow basil, mint, tulsi & more.",
          },
          {
            name: "Succulents & Cactus",
            img: "https://images.pexels.com/photos/7354858/pexels-photo-7354858.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            desc: "Low maintenance, high charm.",
          },
        ];

        const container = document.getElementById("categoryContainer");
        categories.forEach((cat) => {
          container.innerHTML += `
            <div class="category-card">
              <img src="${cat.img}" alt="${cat.name}" onerror="this.style.display='none';">
              <h3>${cat.name}</h3>
              <p>${cat.desc}</p>
            </div>
          `;
        });
      });