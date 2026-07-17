import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

function Header() {
  const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);

  return (
    <header className="header">
      <div className="site-name">Student Portal</div>
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/courses">Courses</Link></li>
          <li><Link to="/profile">Profile</Link></li>
        </ul>
      </nav>
      <div className="enrolled-count">Enrolled: {enrolledCourses.length}</div>
    </header>
  );
}

export default Header;