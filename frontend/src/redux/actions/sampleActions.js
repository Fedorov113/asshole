import {FETCH_READS} from "../constants/action-types";

export function fetchReads() {
  return function (dispatch) {
    fetch('/api/fs/reads/FHM/final')
      .then(response => response.json())
      .then(reads => dispatch({
        type: FETCH_READS,
        payload: reads
      }));
  }
}