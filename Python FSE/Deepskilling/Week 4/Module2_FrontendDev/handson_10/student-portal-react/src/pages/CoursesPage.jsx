import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import CourseCard from '../components/CourseCard';
import {
  fetchAllCourses,
  selectCourses,
  selectCoursesLoading,
  selectCoursesError
} from '../features/coursesSlice';
import { enroll } from '../features/enrollmentSlice';

function CoursesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const dispatch = useDispatch();

  const courses = useSelector(selectCourses);
  const loading = useSelector(selectCoursesLoading);
  const error = useSelector(selectCoursesError);

  useEffect(() => {
    dispatch(fetchAllCourses());
  }, [dispatch]);

  const filteredCourses = courses.filter(course =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleEnroll = (courseId) => {
    const courseToAdd = courses.find(course => course.id === courseId);
    dispatch(enroll(courseToAdd));
  };

  if (loading) {
    return <p>Loading courses...</p>;
  }

  if (error) {
    return <p>Could not load courses: {error}</p>;
  }

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