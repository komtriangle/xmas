import logo from './logo.svg';
import './styles/styles.scss';
import Header from "./Compotents/Header/Header";
import Body from "./Compotents/Body/Body";
import SpinnerComp from './Compotents/SpinnerComp';
import { connect } from "react-redux"
import { NotificationContainer } from 'react-notifications';
import 'react-notifications/lib/notifications.css';

function App(props) {
  return (
    <div className="App">
      <NotificationContainer />
      <Header />
      <Body />
      {props.spinner ? (
        <SpinnerComp />
      ) : (
        <div></div>
      )}
    </div>
  );
}

function mapStateToProps(state) {
  return {
    spinner: state.ui.spinner,
  }
}


export default connect(mapStateToProps)(App)



