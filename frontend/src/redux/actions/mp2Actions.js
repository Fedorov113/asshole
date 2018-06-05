import {FETCH_MP2} from "../constants/action-types";


export function fetchMp2Result(level) {
  return function (dispatch) {
    fetch('/api/fs/sample/mp2/?level='+level)
      .then(response => response.json())
      .then(mp2 => dispatch({
        type: FETCH_MP2,
        payload: mp2
      }));
  }
}