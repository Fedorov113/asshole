import {FETCH_FMT} from "../constants/action-types";


export function fetchFmt(recipient_id) {
  return function (dispatch) {
    fetch('/api/molot/fmt/'+recipient_id)
      .then(response => response.json())
      .then(fmt => dispatch({
        type: FETCH_FMT,
        payload: fmt
      }));
  }
}