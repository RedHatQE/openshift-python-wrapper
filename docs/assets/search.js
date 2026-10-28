(function() {
  // Create modal HTML
  var overlay = document.createElement('div');
  overlay.className = 'search-modal-overlay';
  overlay.innerHTML = '<div class="search-modal">' +
    '<input type="text" class="search-modal-input" placeholder="Search documentation..." autofocus />' +
    '<div class="search-modal-results"></div>' +
    '<div class="search-modal-footer"><kbd>Esc</kbd> to close &nbsp; <kbd>&#x2191;&#x2193;</kbd> to navigate &nbsp; <kbd>Enter</kbd> to open</div>' +
    '</div>';
  document.body.appendChild(overlay);

  var input = overlay.querySelector('.search-modal-input');
  var results = overlay.querySelector('.search-modal-results');
  var index = [];
  var selectedIdx = -1;

  // Load index
  fetch('search-index.json').then(function(r) { return r.json(); })
    .then(function(data) { index = data; }).catch(function() {});

  // Open/close
  function openModal() {
    overlay.classList.add('active');
    input.value = '';
    results.innerHTML = '';
    selectedIdx = -1;
    setTimeout(function() { input.focus(); }, 50);
  }

  function closeModal() {
    overlay.classList.remove('active');
  }

  // Keyboard shortcut
  document.addEventListener('keydown', function(e) {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      openModal();
    }
    if (e.key === 'Escape') closeModal();
  });

  // Click overlay to close
  overlay.addEventListener('click', function(e) {
    if (e.target === overlay) closeModal();
  });

  // Search trigger button in sidebar
  var sidebarSearch = document.getElementById('search-input');
  if (sidebarSearch) {
    sidebarSearch.addEventListener('focus', function(e) {
      e.preventDefault();
      this.blur();
      openModal();
    });
  }

  // Search trigger button in top bar
  var topBarSearch = document.getElementById('search-trigger');
  if (topBarSearch) {
    topBarSearch.addEventListener('click', function(e) {
      e.preventDefault();
      openModal();
    });
  }

  // Search logic
  input.addEventListener('input', function() {
    var q = this.value.toLowerCase().trim();
    results.innerHTML = '';
    selectedIdx = -1;
    if (!q) return;

    var matches = index.filter(function(item) {
      return item.title.toLowerCase().includes(q) || item.content.toLowerCase().includes(q);
    }).slice(0, 10);

    matches.forEach(function(m, i) {
      var div = document.createElement('a');
      div.href = m.slug + '.html';
      div.className = 'search-result-item';

      var title = document.createElement('span');
      title.className = 'search-result-title';
      title.textContent = m.title;
      div.appendChild(title);

      // Content preview
      var preview = document.createElement('span');
      preview.className = 'search-result-preview';
      var contentIdx = m.content.toLowerCase().indexOf(q);
      if (contentIdx >= 0) {
        var start = Math.max(0, contentIdx - 40);
        var end = Math.min(m.content.length, contentIdx + q.length + 60);
        var snippet = (start > 0 ? '...' : '') + m.content.substring(start, end) + (end < m.content.length ? '...' : '');
        preview.textContent = snippet;
      }
      div.appendChild(preview);
      results.appendChild(div);
    });

    if (matches.length === 0) {
      var empty = document.createElement('div');
      empty.className = 'search-no-results';
      empty.textContent = 'No results found';
      results.appendChild(empty);
    }
  });

  // Keyboard navigation
  input.addEventListener('keydown', function(e) {
    var items = results.querySelectorAll('.search-result-item');
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIdx = Math.min(selectedIdx + 1, items.length - 1);
      items.forEach(function(item, i) { item.classList.toggle('selected', i === selectedIdx); });
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIdx = Math.max(selectedIdx - 1, 0);
      items.forEach(function(item, i) { item.classList.toggle('selected', i === selectedIdx); });
    } else if (e.key === 'Enter' && selectedIdx >= 0 && items[selectedIdx]) {
      window.location.href = items[selectedIdx].href;
    }
  });
})();
