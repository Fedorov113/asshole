import {FETCH_READS} from "../constants/action-types";

export function fetchReads(df, preproc) {
  return function (dispatch) {
    fetch('/api/fs/reads/'+df+'/'+preproc)
      .then(response => response.json())
      .then(reads => dispatch({
        type: FETCH_READS,
        payload: reads
      }));
  }
}