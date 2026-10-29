import StudentCard from "./StudentCard";

const students = [
  { id: 1, name: "Oshadha", studentNumber: "202520", nationality: "Sri Lanka" },
  { id: 2, name: "Kenji", studentNumber: "202521", nationality: "Japan" },
  { id: 3, name: "Maria", studentNumber: "202522", nationality: "Philippines" },
  { id: 4, name: "Ahmed", studentNumber: "202523", nationality: "Egypt" },
  { id: 5, name: "Alice", studentNumber: "202524", nationality: "Australia" },
];

function StudentList() {
  return (
    <div>
      {students.map((s) => (
        <StudentCard key={s.id} name={s.name} studentNumber={s.studentNumber} nationality={s.nationality} />
      ))}
    </div>
  );
}

export default StudentList;