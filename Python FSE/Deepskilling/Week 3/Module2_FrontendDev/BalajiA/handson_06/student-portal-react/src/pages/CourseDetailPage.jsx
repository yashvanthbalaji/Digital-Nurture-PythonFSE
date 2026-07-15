import { useParams } from 'react-router-dom';
import { courses } from '../data';

function CourseDetailPage() {
  const { courseId } = useParams();
  const course = courses.find(c => c.id === Number(courseId));

  if (!course) {
    return <p>Course not found.</p>;
  }

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