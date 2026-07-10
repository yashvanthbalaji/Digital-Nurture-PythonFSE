import { courses } from './data.js';

// ---------- TASK 1: ES6+ syntax practice ----------

for (const course of courses) {
  const { name, credits } = course;
  console.log(`${name} - ${credits} credits`);
}

const formattedCourses = courses.map(course =>
  `${course.code} — ${course.name} (${course.credits} credits)`
);
console.log("Formatted courses:", formattedCourses);

const highCreditCourses = courses.filter(course => course.credits >= 4);
console.log("Courses with 4+ credits:", highCreditCourses.length);

const totalCredits = courses.reduce((sum, course) => sum + course.credits, 0);
console.log("Total credits:", totalCredits);

const showCourse = (course) => {
  console.log(`${course.name} (${course.code})`);
};
courses.forEach(showCourse);


// ---------- TASK 2: build the cards from data ----------

const courseGrid = document.querySelector('.course-grid');
const totalCreditsText = document.getElementById('total-credits');

function renderCourses(courseList) {
  courseGrid.innerHTML = '';

  for (const course of courseList) {
    const card = document.createElement('article');
    card.className = 'course-card';
    card.dataset.name = course.name;
    card.dataset.grade = course.grade;

    card.innerHTML = `
      
${course.name}

      
${course.code}


      ${course.credits} credits
    `;

    courseGrid.appendChild(card);
  }
}

renderCourses(courses);
totalCreditsText.textContent = `Total credits: ${totalCredits}`;


// ---------- TASK 3: search, sort, and click ----------

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

// event delegation: one click listener on the whole grid
courseGrid.addEventListener('click', (event) => {
  const card = event.target.closest('.course-card');
  if (!card) return;

  const name = card.dataset.name;
  const grade = card.dataset.grade;
  document.getElementById('selected-course').textContent =
    `${name} — Grade: ${grade}`;
});