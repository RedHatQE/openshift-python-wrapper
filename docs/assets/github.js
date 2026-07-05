(function() {
  var link = document.getElementById('github-link');
  if (!link) return;

  var repoUrl = link.getAttribute('data-repo-url');
  if (!repoUrl) return;

  // Extract owner/repo from GitHub URL
  var match = repoUrl.match(/github\.com[/:]([^/]+)\/([^/.]+)/);
  if (!match) return;

  var owner = match[1];
  var repo = match[2];

  var starsEl = document.getElementById('github-stars');
  if (!starsEl) return;

  fetch('https://api.github.com/repos/' + owner + '/' + repo)
    .then(function(response) {
      if (!response.ok) return null;
      return response.json();
    })
    .then(function(data) {
      if (!data || typeof data.stargazers_count === 'undefined') return;
      var count = data.stargazers_count;
      var display;
      if (count >= 1000) {
        display = (count / 1000).toFixed(1).replace(/\.0$/, '') + 'k';
      } else {
        display = count.toString();
      }
      starsEl.textContent = '★ ' + display;
      starsEl.title = count.toLocaleString() + ' stars';
    })
    .catch(function() {
      // Silently fail - star count is a nice-to-have
    });
})();
