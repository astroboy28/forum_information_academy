import { useEffect } from "react";
import { useParams } from "react-router-dom";

function StudentDetail() {
  const { id } = useParams();

  useEffect(() => {
    document.title = `Student ${id} | Forum Information Academy`;
  }, [id]);

  return (
    <div>
      <h1>Student Detail</h1>
      <p>Showing details for student ID: {id}</p>
    </div>
  );
}

export default StudentDetail;