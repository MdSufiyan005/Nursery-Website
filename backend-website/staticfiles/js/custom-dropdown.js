// Custom dropdown for category and sort
// This script replaces native <select> with a custom dropdown for full styling control

document.addEventListener('DOMContentLoaded', function () {
  function createCustomDropdown(select) {
    // Remove any previous custom dropdown for this select
    const prev = select.parentNode.querySelector('.custom-dropdown-display');
    if (prev) prev.remove();
    const prevList = select.parentNode.querySelector('.custom-dropdown-list');
    if (prevList) prevList.remove();

    // Hide the original select
    select.style.display = 'none';
    // Create display
    const display = document.createElement('div');
    display.className = 'custom-dropdown-display';
    display.tabIndex = 0;
    display.innerText = select.options[select.selectedIndex]?.text || select.options[0].text;
    select.parentNode.appendChild(display);

    // Create dropdown list
    const list = document.createElement('ul');
    list.className = 'custom-dropdown-list';
    for (let i = 0; i < select.options.length; i++) {
      const li = document.createElement('li');
      li.innerText = select.options[i].text;
      li.dataset.value = select.options[i].value;
      if (select.selectedIndex === i) li.classList.add('selected');
      li.addEventListener('click', function () {
        select.selectedIndex = i;
        display.innerText = select.options[i].text;
        list.querySelectorAll('li').forEach(el => el.classList.remove('selected'));
        li.classList.add('selected');
        select.dispatchEvent(new Event('change'));
        list.classList.remove('open');
      });
      list.appendChild(li);
    }
    select.parentNode.appendChild(list);

    // Toggle dropdown
    display.addEventListener('click', function (e) {
      e.stopPropagation();
      list.classList.toggle('open');
    });
    display.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        list.classList.toggle('open');
      }
    });
    document.addEventListener('click', function () {
      list.classList.remove('open');
    });
  }

  // Apply to category and sort selects
  const selects = [
    document.getElementById('categorySelect'),
    document.getElementById('sortSelect')
  ];
  selects.forEach(sel => sel && createCustomDropdown(sel));
});