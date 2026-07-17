import apiClient from './apiClient';

// jsonplaceholder has no real "courses" endpoint, so -- same trick as
// earlier hands-ons -- we reuse /posts and reshape it into course-like data
export function getAllCourses() {
  return apiClient.get('/posts?_limit=5').then((posts) =>
    posts.map((post, index) => ({
      id: post.id,
      name: post.title,
      code: 'CS10' + (index + 1),
      credits: 3,
      grade: 'A'
    }))
  );
}

export function getCourseById(id) {
  return apiClient.get('/posts/' + id).then((post) => ({
    id: post.id,
    name: post.title,
    code: 'CS10' + post.id,
    credits: 3,
    grade: 'A'
  }));
}

// simulates the shape a real "enroll" endpoint would have
export function enrollStudent(studentId, courseId) {
  return apiClient.post('/posts', { studentId, courseId });
}
