import { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import Footer from './components/Footer';
import CourseCard from './components/CourseCard';
import StudentProfile from './components/StudentProfile';

const courseNames = ["Web Development Basics", "Data Structures", "Database Systems", "UI/UX Design Principles", "Cloud Computing Basics"];
const courseCodes = ["CS101", "CS102", "CS103", "CS104", "CS105"];
const courseCredits = [4, 3, 4, 2, 3];
const courseGrades = ["A", "B+", "A-", "B", "A"];

function App() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [enrolledCourses, setEnrolledCourses] = useState([]);

  useEffect(() => {
    async function loadCourses() {
      try {
        const response = await fetch('https://jsonplaceholder.typicode.com/posts');
        const posts = await response.json();

        const firstFivePosts = posts.slice(0, 5);

        const courseLikeData = firstFivePosts.map((post, index) => ({
          id: post.id,
          name: courseNames[index],
          code: courseCodes[index],
          credits: courseCredits[index],
          grade: courseGrades[index]
        }));

        setCourses(courseLikeData);
        setLoading(false);
      } catch (err) {
        setError("Could not load courses. Please try again.");
        setLoading(false);
      }
    }

    loadCourses();
  }, []);

  useEffect(() => {
    console.log("Courses updated");
  }, [courses]);

  const handleEnroll = (courseId) => {
    const courseToAdd = courses.find(course => course.id === courseId);
    setEnrolledCourses([...enrolledCourses, courseToAdd]);
  };

  const filteredCourses = courses.filter(course =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />

      <main>
        <input
          type="text"
          placeholder="Search courses..."
          value={searchTerm}
          onChange={(event) => setSearchTerm(event.target.value)}
        />

        <div className="course-grid">
          {filteredCourses.map(course => (
            <CourseCard
              key={course.id}
              {...course}
              onEnroll={handleEnroll}
            />
          ))}
        </div>

        <StudentProfile />
      </main>

      <Footer />
    </div>
  );
}

export default App;