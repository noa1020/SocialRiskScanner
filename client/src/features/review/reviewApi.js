const API_URL = 'http://127.0.0.1:5000/default/getAllPosts';

export async function fetchReviewItems() {
  const response = await fetch(API_URL);
  if (!response.ok) {
    throw new Error('Unable to load review items.');
  }

  const data = await response.json();
  return Array.isArray(data) ? data : [];
}
