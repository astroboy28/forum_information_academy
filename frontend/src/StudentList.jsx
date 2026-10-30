import { useState } from "react";
import StudentCard from "./StudentCard";
import { Link } from "react-router-dom";

const students = [
  { id: 1, name: "Oshadha", studentNumber: "202520", nationality: "Sri Lanka" },
  { id: 2, name: "Kenji", studentNumber: "202521", nationality: "Japan" },
  { id: 3, name: "Maria", studentNumber: "202522", nationality: "Philippines" },
  { id: 4, name: "Ahmed", studentNumber: "202523", nationality: "Egypt" },
  { id: 5, name: "Alice", studentNumber: "202524", nationality: "Australia" },
];

function StudentList() {
  const [search, setSearch] = useState("");
  const [nationality, setNationality] = useState("");

  const filtered = students.filter((s) =>
    s.name.toLowerCase().includes(search.toLowerCase()) &&
    (nationality === "" || s.nationality === nationality)
  );

  return (
     <div>
       <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search by name..." />
       <select value={nationality} onChange={(e) => setNationality(e.target.value)}>
         <option value="">All nationalities</option>
         <option value="Sri Lanka">Sri Lanka</option>
         <option value="Japan">Japan</option>
         <option value="Philippines">Philippines</option>
         <option value="Egypt">Egypt</option>
         <option value="Australia">Australia</option>
       </select>
       {filtered.map((s) => (
   <Link key={s.id} to={`/students/${s.id}`} style={{ textDecoration: "none", color: "inherit" }}>
     <StudentCard name={s.name} studentNumber={s.studentNumber} nationality={s.nationality} />
   </Link>
 ))}
     </div>
   );
 }

 export default StudentList;