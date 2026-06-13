function sanitize(text) {
  return typeof text === 'string' ? text.trim() : '';
}

function extractPostsFromPage() {
  const articles = Array.from(document.querySelectorAll('div[role="article"]'));
  const collectedPosts = [];

  articles.forEach((article) => {
    const username = sanitize(article.querySelector('span[dir="auto"]')?.innerText || '');
    const contentElement = article.querySelector('div[dir="auto"]');
    const content = sanitize(contentElement?.innerText || '');

    if (username && content) {
      collectedPosts.push({ username, content });
    }
  });

  return collectedPosts;
}

function sendToServer(post) {
  return fetch('http://127.0.0.1:5000/default/calculateSuicidePost', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(post),
  });
}

function getFacebookPosts() {
  const posts = extractPostsFromPage();

  if (!posts.length) {
    return Promise.resolve({ saved: 0, skipped: 0 });
  }

  return Promise.all(posts.map((post) => sendToServer(post))).then((responses) => {
    return responses.reduce(
      (summary, response) => {
        if (response.ok) {
          summary.saved += 1;
        } else {
          summary.skipped += 1;
        }
        return summary;
      },
      { saved: 0, skipped: 0 }
    );
  });
}

function handleScanRequest() {
  return getFacebookPosts().then((summary) => {
    console.log('Scan complete', summary);
    return summary;
  });
}

chrome.runtime.onMessage.addListener((message) => {
  if (message?.type === 'SCAN_FACEBOOK_POSTS') {
    void handleScanRequest();
  }
});

window.addEventListener('shieldAkaton:scan', () => {
  void handleScanRequest();
});

window.addEventListener('load', () => {
  setTimeout(() => {
    void handleScanRequest();
  }, 3000);
});
