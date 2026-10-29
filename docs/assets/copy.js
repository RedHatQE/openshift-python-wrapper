(function() {
  // Icon-only so it does not sit over the code on a short block. The word moves
  // to title/aria-label, which still gives a tooltip and a screen-reader name.
  var ICON_COPY =
    '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" ' +
    'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<rect x="5.5" y="5.5" width="8" height="9" rx="1.5"/>' +
    '<path d="M10.5 3.5v-1a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h1"/></svg>';
  var ICON_OK =
    '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" ' +
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M2.5 8.5l3.5 3.5 7-8"/></svg>';
  var ICON_FAIL =
    '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" ' +
    'stroke-width="1.5" stroke-linecap="round" aria-hidden="true">' +
    '<path d="M4 4l8 8M12 4l-8 8"/></svg>';

  function setIcon(btn, icon, label) {
    btn.innerHTML = icon;
    btn.title = label;
    btn.setAttribute('aria-label', label);
  }

  function flash(btn, icon, label, backTo, backLabel) {
    setIcon(btn, icon, label);
    btn.classList.add('copied');
    setTimeout(function() {
      setIcon(btn, backTo, backLabel);
      btn.classList.remove('copied');
    }, 2000);
  }

  document.querySelectorAll('pre').forEach(function(pre) {
    // Idempotent: this file can run more than once (cached asset, a second
    // injection, a client-side navigation). Without this guard every run left
    // another copy-btn behind and the block grew a stack of them.
    var existing = pre.querySelector('.copy-btn');
    if (existing) existing.remove();
    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.type = 'button';
    setIcon(btn, ICON_COPY, 'Copy code');
    btn.addEventListener('click', function() {
      var code = pre.querySelector('code');
      var text = code ? code.textContent : pre.textContent;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function() {
          flash(btn, ICON_OK, 'Copied', ICON_COPY, 'Copy code');
        }).catch(function() {
          fallbackCopy(text, btn);
        });
      } else {
        fallbackCopy(text, btn);
      }
    });
    pre.style.position = 'relative';
    pre.appendChild(btn);
  });

  function fallbackCopy(text, btn) {
    var textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    var ok = false;
    try {
      ok = document.execCommand('copy');
    } catch (e) {
      ok = false;
    }
    document.body.removeChild(textarea);
    if (ok) flash(btn, ICON_OK, 'Copied', ICON_COPY, 'Copy code');
    else flash(btn, ICON_FAIL, 'Copy failed', ICON_COPY, 'Copy code');
  }
})();
