document.addEventListener('DOMContentLoaded', () => {
  // 🛒 Cart badge update logic
  const updateBadge = count => {
    let badge = document.getElementById('cart-count');
    if (count > 0) {
      if (!badge) {
        badge = document.createElement('span');
        badge.id = 'cart-count';
        Object.assign(badge.style, {
          position: 'absolute',
          top: '-6px',
          right: '-12px',
          backgroundColor: '#e53935',
          color: 'white',
          borderRadius: '50%',
          padding: '2px 6px',
          fontSize: '12px'
        });
        document.querySelector('.cart-icon').appendChild(badge);
      }
      badge.textContent = count;
    } else if (badge) {
      badge.remove();
    }
  };

  document.querySelectorAll('.js-add-cart').forEach(btn => {
    btn.addEventListener('click', async e => {
      e.preventDefault();
      const url = btn.dataset.url;
      try {
        const res = await fetch(url);
        const data = await res.json();
        updateBadge(data.cart_count);
      } catch (err) {
        console.error('Cart update failed', err);
      }
    });
  });

  // 👤 User dropdown toggle (desktop)
  function toggleDropdown(event) {
  if (window.innerWidth < 769) return;

  event.preventDefault();
  event.stopPropagation();

  const dropdownMenu = document.getElementById('userDropdown');
  const dropdownArrow = event.currentTarget.querySelector('.dropdown-arrow');
  const isOpen = dropdownMenu.classList.contains('show');

  // Close all dropdowns first
  document.querySelectorAll('.dropdown-menu').forEach(menu => menu.classList.remove('show'));
  document.querySelectorAll('.dropdown-arrow').forEach(arrow => arrow.style.transform = 'rotate(0deg)');

  // Toggle current dropdown
  if (!isOpen) {
    dropdownMenu.classList.add('show');
    dropdownArrow.style.transform = 'rotate(180deg)';
  } else {
    dropdownMenu.classList.remove('show');
    dropdownArrow.style.transform = 'rotate(0deg)';
  }
}

  const dropdownToggle = document.querySelector('.dropdown-toggle');
  const dropdownMenu = document.querySelector('.dropdown-menu');
  const dropdownArrow = document.querySelector('.dropdown-arrow');

  if (dropdownToggle && dropdownMenu) {
    dropdownToggle.addEventListener('click', toggleDropdown);

    // Close dropdown on outside click
  document.addEventListener('click', function (event) {
    const toggleBtn = document.querySelector('.dropdown-toggle');
    const dropdown = document.getElementById('userDropdown');

    // If the click is NOT inside the dropdown or on the toggle button
    if (!event.target.closest('.profile-desktop-dropdown')) {
      if (dropdown) dropdown.classList.remove('show');
      if (toggleBtn) {
        const arrow = toggleBtn.querySelector('.dropdown-arrow');
        if (arrow) arrow.style.transform = 'rotate(0deg)';
      }
    }
  });



    // Close dropdown on Escape key
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        dropdownMenu.classList.remove('show');
        dropdownArrow.style.transform = 'rotate(0deg)';
      }
    });
  }

  // 📱 Mobile nav and blur overlay logic
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('mainNavLinks');
  const blurOverlay = document.getElementById('navBlurOverlay');

  function closeMobileNav() {
    navLinks.classList.remove('open');
    blurOverlay.classList.remove('active');
  }

  if (menuToggle && navLinks && blurOverlay) {
    menuToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      const isOpen = navLinks.classList.toggle('open');
      if (isOpen) {
        blurOverlay.classList.add('active');
      } else {
        blurOverlay.classList.remove('active');
      }
    });

    blurOverlay.addEventListener('click', closeMobileNav);

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeMobileNav();
    });
  }
});