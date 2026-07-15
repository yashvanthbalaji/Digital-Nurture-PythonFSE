import { useSelector, useDispatch } from 'react-redux';
import StudentProfile from '../components/StudentProfile';
import { unenroll } from '../features/enrollmentSlice';

function ProfilePage() {
  const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);
  const dispatch = useDispatch();

  return (
    <div className="page">
      <h1>My Profile</h1>
      <h2>Enrolled Courses</h2>
      {enrolledCourses.length === 0 && <p>You haven't enrolled in any courses yet.</p>}
      <ul>
        {enrolledCourses.map(course => (
          <li key={course.id}>
            {course.name} ({course.code})
            <button onClick={() => dispatch(unenroll(course.id))}>Remove</button>
          </li>
        ))}
      </ul>
      <StudentProfile />
    </div>
  );
}

export default ProfilePage;