(function() {
  function getTheme() {
    try { return localStorage.getItem('theme'); } catch(e) { return null; }
  }
  function setTheme(theme) {
    try { localStorage.setItem('theme', theme); } catch(e) {}
  }

  var toggle = document.getElementById('theme-toggle');
  var stored = getTheme();
  if (stored === 'dark' || stored === 'light') {
    document.documentElement.setAttribute('data-theme', stored);
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
  }
  if (toggle) toggle.addEventListener('click', function() {
    var current = document.documentElement.getAttribute('data-theme');
    var next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    setTheme(next);
  });
})();
