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
  var selectedIdx = -1;
  // Load index. Normally fetched once and shared by every page, so nothing is
  // inlined and the pages stay small. An inline copy is used when the generator
  // was asked to embed it. Note: fetch() of a local file is blocked by CORS on
  // file:// in most browsers, so opening the site straight off disk needs the
  // inline mode; served over HTTP this is not an issue.
  var index = Array.isArray(window.__DOCS_SEARCH_INDEX__) ? window.__DOCS_SEARCH_INDEX__ : null;
  var indexError = null;
  // HTTP status when a response actually arrived, null when the request never
  // completed (offline, DNS, CORS) or the body was not JSON. The two are not the
  // same failure: a 500 or a dropped connection says nothing about the index
  // file, so the reader must not be told to rebuild because of one.
  var indexStatus = null;
  // Opening the file straight off disk is the one case CORS blocks, and so the
  // one case where "serve the site over HTTP" is the remedy. Over HTTP a failed
  // fetch means a missing or corrupt search-index.json, and telling the reader
  // to serve the site when they already do is advice that cannot help (#875).
  var onFileProtocol = location.protocol === 'file:';
  if (!index) {
    fetch('search-index.json').then(function(r) {
      if (!r.ok) { indexStatus = r.status; throw new Error('HTTP ' + r.status); }
      return r.json();
    }).then(function(searchIndex) {
      index = searchIndex;
      console.debug('[docs] search index loaded:', searchIndex.length, 'entries');
      // The user may have typed before the fetch resolved. Their first query
      // was answered with "Loading search index..." and never re-run, so the
      // results stayed hidden until they edited the box again.
      if (typeof render === 'function' && input.value.trim()) render();
    }).catch(function(err) {
      indexError = err;
      console.error('[docs] search index unavailable:', err,
        onFileProtocol
          ? '— serve the site over HTTP, or build it with the search index inlined.'
          : (indexStatus
              ? '— the server answered HTTP ' + indexStatus + ' for search-index.json; the index may be fine.'
              : '— search-index.json could not be fetched or parsed; check the network and rebuild if it persists.'));
      // Same reason as the success path: a query typed while the request was
      // pending would otherwise stay on "Loading search index..." forever, now
      // that the request has failed.
      if (typeof render === 'function' && input.value.trim()) render();
    });
  }

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
  function render() {
    var q = input.value.toLowerCase().trim();
    results.innerHTML = '';
    selectedIdx = -1;
    if (!q) return;

    if (!index) {
      var err = document.createElement('div');
      err.className = 'search-no-results';
      if (!indexError) {
        err.textContent = 'Loading search index...';
      } else if (onFileProtocol) {
        err.textContent = 'Search needs the site served over HTTP (opening the file directly blocks it).';
      } else if (indexStatus === 404) {
        err.textContent = 'Search index not found — rebuild the site.';
      } else if (indexStatus === 401 || indexStatus === 403 || (indexStatus >= 400 && indexStatus < 500 && indexStatus !== 408 && indexStatus !== 429)) {
        // A permanent client error: waiting does not lift an access restriction
        // or a bad request, so do not send the reader round the retry loop.
        err.textContent = 'Search index unavailable (HTTP ' + indexStatus + '). Check the site\'s access configuration.';
      } else if (indexStatus) {
        err.textContent = 'Search index unavailable (HTTP ' + indexStatus + '). Try again shortly.';
      } else {
        err.textContent = 'Search index could not be loaded (network error or invalid index).';
      }
      results.appendChild(err);
      return;
    }

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
  }

  input.addEventListener('input', render);

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
