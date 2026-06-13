const statusEl = document.getElementById('status');
const buttonEl = document.getElementById('scrape');

function setStatus(message, isError = false) {
  if (!statusEl) {
    return;
  }

  statusEl.textContent = message;
  statusEl.style.color = isError ? '#ff6b6b' : '#2f4f4f';
}

buttonEl?.addEventListener('click', async () => {
  setStatus('Scanning the current Facebook page…');

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.id) {
      throw new Error('No tab is currently active.');
    }

    await chrome.tabs.sendMessage(tab.id, { type: 'SCAN_FACEBOOK_POSTS' });
    setStatus('Scan requested. High-risk posts will be sent to the local server.');
  } catch (error) {
    setStatus(error.message || 'The scan could not be started.', true);
  }
});
  