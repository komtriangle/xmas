import './styles/styles.scss';
import Work from './Compotents/Work';
import ErrorFeedBack from "./Compotents/ErrorFeedback"
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Work />} exact />
        <Route path="/ErrorFeedBack" element={<ErrorFeedBack />} exact />
      </Routes>
    </Router>
  );
}

export default App



