(function() {
  var blockquotes = document.querySelectorAll('blockquote');
  blockquotes.forEach(function(bq) {
    var firstStrong = bq.querySelector('strong');
    if (!firstStrong) return;

    var text = firstStrong.textContent.toLowerCase().replace(':', '').trim();
    var type = null;

    if (text === 'note' || text === 'info') {
      type = 'note';
    } else if (text === 'warning' || text === 'caution') {
      type = 'warning';
    } else if (text === 'tip' || text === 'hint') {
      type = 'tip';
    } else if (text === 'danger' || text === 'error') {
      type = 'danger';
    } else if (text === 'important') {
      type = 'important';
    }

    if (type) {
      bq.classList.add('callout', 'callout-' + type);
    }
  });
})();
