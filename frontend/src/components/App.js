import React from "react";
import ReactDOM from "react-dom";
import ClippedDrawer from "./AppBar";
import {Provider} from "react-redux";
import store from "../redux/store/index"

function App() {
  return (
    <Provider store={store}>
      <ClippedDrawer/>
    </Provider>
  );
}

ReactDOM.render(<App/>, document.querySelector('#app'));