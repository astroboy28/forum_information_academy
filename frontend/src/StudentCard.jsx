function StudentCard({ name, studentNumber, nationality }) {
  return (
    <div style={{ border: "1px solid #ccc", borderRadius: 8, padding: 16, maxWidth: 240 }}>
      <h2>{name}</h2>
      <p>{studentNumber} · {nationality}</p>
    </div>
  );
}

export default StudentCard;