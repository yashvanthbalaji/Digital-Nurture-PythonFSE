import { useState } from 'react';
import { useDispatch } from 'react-redux';
import CourseCard from '../components/CourseCard';
import { courses } from '../data';
import { enroll } from '../features/enrollmentSlice';

function CoursesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const dispatch = useDispatch();

  const filteredCourses = courses.filter(course =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleEnroll = (courseId) => {
    const courseToAdd = courses.find(course => course.id === courseId);
    dispatch(enroll(courseToAdd));
  };

  return (
    <div className="page">
      <h1>Enrolled Courses</h1>
      <input
        type="text"
        placeholder="Search courses..."
        value={searchTerm}
        onChange={(event) => setSearchTerm(event.target.value)}
      />
      <div className="course-grid">
        {filteredCourses.map(course => (
          <CourseCard key={course.id} {...course} onEnroll={handleEnroll} />
        ))}
      </div>
    </div>
  );
}

export default CoursesPage;