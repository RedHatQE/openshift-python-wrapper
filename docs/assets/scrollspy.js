(function() {
  var tocLinks = document.querySelectorAll('.toc-container a');
  if (tocLinks.length === 0) return;

  var headings = [];
  tocLinks.forEach(function(link) {
    var href = link.getAttribute('href');
    if (href && href.startsWith('#')) {
      var target = document.getElementById(href.substring(1));
      if (target) {
        headings.push({ element: target, link: link });
      }
    }
  });

  if (headings.length === 0) return;

  function updateActive() {
    var scrollPos = window.scrollY + 100;
    var current = null;

    for (var i = 0; i < headings.length; i++) {
      if (headings[i].element.offsetTop <= scrollPos) {
        current = headings[i];
      }
    }

    tocLinks.forEach(function(link) {
      link.classList.remove('active');
    });

    if (current) {
      current.link.classList.add('active');
    }
  }

  var ticking = false;
  window.addEventListener('scroll', function() {
    if (!ticking) {
      window.requestAnimationFrame(function() {
        updateActive();
        ticking = false;
      });
      ticking = true;
    }
  });

  updateActive();
})();
