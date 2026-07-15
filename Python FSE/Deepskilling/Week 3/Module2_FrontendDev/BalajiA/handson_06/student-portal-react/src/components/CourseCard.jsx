import { Link, useNavigate } from 'react-router-dom';

function CourseCard({ id, name, code, credits, grade, onEnroll }) {
  const navigate = useNavigate();

  const handleEnrollClick = () => {
    onEnroll(id);
    navigate('/profile');
  };

  return (
    <article className="course-card">
      <Link to={`/courses/${id}`} className="course-card-link">
        <h3>{name}</h3>
        <p>{code}</p>
        <span>{credits} credits</span>
        <p>Grade: {grade}</p>
      </Link>
      <button onClick={handleEnrollClick}>Enroll</button>
    </article>
  );
}

export default CourseCard;