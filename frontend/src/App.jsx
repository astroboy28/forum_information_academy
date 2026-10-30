import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import StudentList from "./StudentList";
import StudentDetail from "./StudentDetail";

function App() {
   return (
     <BrowserRouter>
       <h1>Forum Information Academy</h1>
       <nav>
         <Link to="/students">Students</Link>
       </nav>
       <Routes>
         <Route path="/students" element={<StudentList />} />
         <Route path="/students/:id" element={<StudentDetail />} />
       </Routes>
     </BrowserRouter>
   );
 }

 export default App;