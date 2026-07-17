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
    return 
Loading courses...

;
  }

  if (error) {
    return Could not load courses: {error}

;
  }

  return (
    

      
Enrolled Courses


      
{searchTerm}
 setSearchTerm(event.target.value)}
      />

      

        {filteredCourses.map(course => (
          
        ))}
      

    

  );
}

export default CoursesPage;