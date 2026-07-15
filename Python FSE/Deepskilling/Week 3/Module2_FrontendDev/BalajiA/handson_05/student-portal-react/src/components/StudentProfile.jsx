import { useState } from 'react';

function StudentProfile() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [semester, setSemester] = useState('');

  return (
    <div className="student-profile">
      <h2>Student Profile</h2>

      <label>
        Name:
        <input
          type="text"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
      </label>

      <label>
        Email:
        <input
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
      </label>

      <label>
        Semester:
        <input
          type="text"
          value={semester}
          onChange={(event) => setSemester(event.target.value)}
        />
      </label>

      <p>Preview: {name}, {email}, Semester {semester}</p>
    </div>
  );
}

export default StudentProfile;

