import { courses } from './data.js';

// ---------- TASK 1: promises and async/await ----------

function fetchUser(id) {
  return fetch('https://jsonplaceholder.typicode.com/users/' + id)
    .then(response => response.json())
    .then(user => {
      console.log("User name (using .then):", user.name);
    });
}
fetchUser(1);

async function fetchUserAsync(id) {
  try {
    const response = await fetch('https://jsonplaceholder.typicode.com/users/' + id);
    const user = await response.json();
    console.log("User name (using async/await):", user.name);
  } catch (error) {
    console.log("Something went wrong:", error.message);
  }
}
fetchUserAsync(2);

function fetchAllCourses() {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(courses);
    }, 1000);
  });
}

async function fetchTwoUsersTogether() {
  const [response1, response2] = await Promise.all([
    fetch('https://jsonplaceholder.typicode.com/users/1'),
    fetch('https://jsonplaceholder.typicode.com/users/2')
  ]);
  const user1 = await response1.json();
  const user2 = await response2.json();
  console.log("Both users loaded together:", user1.name, user2.name);
}
fetchTwoUsersTogether();


// ---------- TASK 2: render courses + fetch with error handling ----------

const courseGrid = document.querySelector('.course-grid');
const totalCreditsText = document.getElementById('total-credits');

function renderCourses(courseList) {
  courseGrid.innerHTML = '';

  for (const course of courseList) {
    const card = document.createElement('article');
    card.className = 'course-card';
    card.dataset.name = course.name;
    card.dataset.grade = course.grade;

    card.innerHTML = '<h3>' + course.name + '</h3>' +
      '<p>' + course.code + '</p>' +
      '<span>' + course.credits + ' credits</span>';

    courseGrid.appendChild(card);
  }
}

async function loadCourses() {
  courseGrid.innerHTML = '<p>Loading courses...</p>';
  const loadedCourses = await fetchAllCourses();
  const totalCredits = loadedCourses.reduce((sum, course) => sum + course.credits, 0);

  renderCourses(loadedCourses);
  totalCreditsText.textContent = 'Total credits: ' + totalCredits;
}
loadCourses();

async function apiFetch(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Request failed with status ' + response.status);
  }
  return response.json();
}

async function loadNotifications() {
  const notifList = document.getElementById('notifications-list');
  const statusText = document.getElementById('notif-status');
  const retryBtn = document.getElementById('retry-btn');

  notifList.innerHTML = '';
  statusText.textContent = 'Loading notifications...';
  retryBtn.style.display = 'none';

  try {
    const posts = await apiFetch('https://jsonplaceholder.typicode.com/posts');
    statusText.textContent = '';

    const firstFivePosts = posts.slice(0, 5);
    for (const post of firstFivePosts) {
      const card = document.createElement('div');
      card.className = 'notification-card';
      card.innerHTML = '<h4>' + post.title + '</h4><p>' + post.body + '</p>';
      notifList.appendChild(card);
    }
  } catch (error) {
    statusText.textContent = 'Could not load notifications. Please try again.';
    retryBtn.style.display = 'inline-block';
  }
}

document.getElementById('retry-btn').addEventListener('click', loadNotifications);
loadNotifications();


// ---------- TASK 3: introduction to axios ----------

async function apiFetchAxios(url) {
  const response = await axios.get(url);
  return response.data;
}

async function loadUserOnePosts() {
  const response = await axios.get('https://jsonplaceholder.typicode.com/posts', {
    params: { userId: 1 }
  });
  console.log("Posts by user 1 (via axios):", response.data);
}
loadUserOnePosts();

axios.interceptors.request.use((config) => {
  console.log("API call started:", config.url);
  return config;
});

/*
  Fetch vs Axios — 3 differences:
  1. Fetch needs response.json() manually; Axios parses JSON automatically into response.data.
  2. Fetch only rejects on network errors (e.g. being offline); Axios also throws on 404/500 responses.
  3. Axios lets you pass a "params" object to build the query string; Fetch needs the URL built by hand.
*/


// ---------- search, sort & click (carried over from Hands-On 3) ----------

const searchInput = document.getElementById('search-courses');
searchInput.addEventListener('input', () => {
  const searchText = searchInput.value.toLowerCase();
  const filtered = courses.filter(course =>
    course.name.toLowerCase().includes(searchText)
  );
  renderCourses(filtered);
});

const sortBtn = document.getElementById('sort-btn');
sortBtn.addEventListener('click', () => {
  courses.sort((a, b) => b.credits - a.credits);
  renderCourses(courses);
});

courseGrid.addEventListener('click', (event) => {
  const card = event.target.closest('.course-card');
  if (!card) return;

  const name = card.dataset.name;
  const grade = card.dataset.grade;
  document.getElementById('selected-course').textContent =
    name + ' — Grade: ' + grade;
});