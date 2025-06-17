document.addEventListener('DOMContentLoaded', () => {
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

  function toggleDropdown(event) {
    event.preventDefault();
    const dropdownMenu = document.getElementById('userDropdown');
    const dropdownArrow = event.currentTarget.querySelector('.dropdown-arrow');

    if (dropdownMenu.style.display === 'none' || !dropdownMenu.style.display) {
        dropdownMenu.style.display = 'block';
        dropdownArrow.style.transform = 'rotate(180deg)';
    } else {
        dropdownMenu.style.display = 'none';
        dropdownArrow.style.transform = 'rotate(0)';
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', function closeDropdown(e) {
        if (!e.target.closest('.dropdown')) {
            dropdownMenu.style.display = 'none';
            dropdownArrow.style.transform = 'rotate(0)';
            document.removeEventListener('click', closeDropdown);
        }
    });
}

  const dropdownToggle = document.querySelector('.dropdown-toggle');
  const dropdownMenu = document.querySelector('.dropdown-menu');
  const dropdownArrow = document.querySelector('.dropdown-arrow');

  if (dropdownToggle && dropdownMenu) {
    // Toggle dropdown on click
    dropdownToggle.addEventListener('click', toggleDropdown);

    // Close dropdown when clicking outside
    document.addEventListener('click', function (event) {
      const dropdowns = document.getElementsByClassName('dropdown-menu');
      const arrows = document.getElementsByClassName('dropdown-arrow');

      for (const dropdown of dropdowns) {
        if (dropdown.classList.contains('show')) {
          dropdown.classList.remove('show');
        }
      }

      for (const arrow of arrows) {
        arrow.style.transform = 'rotate(0)';
      }
    });

    // Close dropdown on escape key
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        const dropdowns = document.getElementsByClassName('dropdown-menu');
        const arrows = document.getElementsByClassName('dropdown-arrow');

        for (const dropdown of dropdowns) {
          dropdown.classList.remove('show');
        }

        for (const arrow of arrows) {
          arrow.style.transform = 'rotate(0)';
        }
      }
    });
  }
});