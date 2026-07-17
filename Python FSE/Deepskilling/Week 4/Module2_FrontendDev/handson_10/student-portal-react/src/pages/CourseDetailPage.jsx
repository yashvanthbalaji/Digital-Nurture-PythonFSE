import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getCourseById } from '../api/courseApi';

function CourseDetailPage() {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    getCourseById(courseId)
      .then((data) => {
        setCourse(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [courseId]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Could not load course: {error}</p>;
  if (!course) return <p>Course not found.</p>;

  return (
    <div className="page">
      <h1>{course.name}</h1>
      <p>Course code: {course.code}</p>
      <p>Credits: {course.credits}</p>
      <p>Grade: {course.grade}</p>
    </div>
  );
}

export default CourseDetailPage;