(function() {
  var blocks = document.querySelectorAll('pre code');
  blocks.forEach(function(code) {
    var classes = code.className || '';
    var match = classes.match(/language-(\w+)/);
    if (!match) return;

    var lang = match[1];
    var labelMap = {
      'python': 'Python',
      'py': 'Python',
      'javascript': 'JavaScript',
      'js': 'JavaScript',
      'typescript': 'TypeScript',
      'ts': 'TypeScript',
      'bash': 'Bash',
      'sh': 'Shell',
      'shell': 'Shell',
      'json': 'JSON',
      'yaml': 'YAML',
      'yml': 'YAML',
      'html': 'HTML',
      'css': 'CSS',
      'go': 'Go',
      'rust': 'Rust',
      'java': 'Java',
      'ruby': 'Ruby',
      'rb': 'Ruby',
      'sql': 'SQL',
      'dockerfile': 'Dockerfile',
      'docker': 'Dockerfile',
      'toml': 'TOML',
      'xml': 'XML',
      'c': 'C',
      'cpp': 'C++',
      'csharp': 'C#',
      'cs': 'C#',
      'php': 'PHP',
      'swift': 'Swift',
      'kotlin': 'Kotlin',
      'scala': 'Scala',
      'r': 'R',
      'lua': 'Lua',
      'perl': 'Perl',
      'makefile': 'Makefile',
      'graphql': 'GraphQL',
      'markdown': 'Markdown',
      'md': 'Markdown',
      'plaintext': 'Text',
      'text': 'Text',
      'ini': 'INI',
      'env': '.env',
    };

    var displayName = labelMap[lang.toLowerCase()] || lang;

    var pre = code.parentElement;
    if (!pre || pre.tagName !== 'PRE') return;

    var label = document.createElement('span');
    label.className = 'code-label';
    label.textContent = displayName;

    var wrapper = pre.closest('.code-block-wrapper');
    if (wrapper) {
      wrapper.insertBefore(label, wrapper.firstChild);
    } else {
      pre.style.position = 'relative';
      label.style.position = 'absolute';
      label.style.top = '0.5rem';
      label.style.right = '0.5rem';
      pre.insertBefore(label, pre.firstChild);
    }
  });
})();
