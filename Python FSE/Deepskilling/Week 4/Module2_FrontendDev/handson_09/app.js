import { courses } from './data.js';

const courseGrid = document.querySelector('.course-grid');
const totalCreditsText = document.getElementById('total-credits');
const resultsCount = document.getElementById('results-count');

function renderCourses(courseList) {
  courseGrid.innerHTML = '';

  for (const course of courseList) {
    const card = document.createElement('article');
    card.className = 'course-card';
    card.dataset.name = course.name;
    card.dataset.grade = course.grade;

    // keyboard accessibility: make the card reachable by Tab and describe it
    card.tabIndex = 0;
    card.setAttribute('role', 'button');
    card.setAttribute(
      'aria-label',
      course.name + ', ' + course.credits + ' credits, grade ' + course.grade
    );

    card.innerHTML = `
      
${course.name}

      
${course.code}


      ${course.credits} credits
    `;

    courseGrid.appendChild(card);
  }

  // this text change is what aria-live="polite" announces to a screen reader
  resultsCount.textContent = courseList.length + ' courses found';
}

const totalCredits = courses.reduce((sum, course) => sum + course.credits, 0);
renderCourses(courses);
totalCreditsText.textContent = `Total credits: ${totalCredits}`;

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

function selectCourse(card) {
  const name = card.dataset.name;
  const grade = card.dataset.grade;
  document.getElementById('selected-course').textContent = `${name} — Grade: ${grade}`;
}

// mouse: one click listener on the grid handles every card (event delegation)
courseGrid.addEventListener('click', (event) => {
  const card = event.target.closest('.course-card');
  if (!card) return;
  selectCourse(card);
});

// keyboard: Enter on a focused card does exactly what a click does
courseGrid.addEventListener('keydown', (event) => {
  if (event.key !== 'Enter') return;
  const card = event.target.closest('.course-card');
  if (!card) return;
  selectCourse(card);
});

// hamburger button: toggle the nav open/closed and keep aria-expanded in sync
const menuToggle = document.getElementById('menu-toggle');
const mainNav = document.getElementById('main-nav');

menuToggle.addEventListener('click', () => {
  const isOpen = mainNav.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
});