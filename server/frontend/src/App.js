import LoginPanel from "./components/Login/Login"
import { Routes, Route } from "react-router-dom";
import Register from "./components/Register/Register";
import Dealers from './components/Dealers/Dealer';

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/Register" element={<Register />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/dealer/:id" element={<Dealer/>} />
    </Routes>
  );
}
export default App;
