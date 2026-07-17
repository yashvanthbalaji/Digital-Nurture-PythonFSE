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

  if (loading) return 
Loading...

;
  if (error) return 
Could not load course: {error}

;
  if (!course) return 
Course not found.

;

  return (
    

      
{course.name}

      
Course code: {course.code}


      
Credits: {course.credits}


      
Grade: {course.grade}


    

  );
}

export default CourseDetailPage;