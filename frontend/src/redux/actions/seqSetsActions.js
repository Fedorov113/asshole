import {FETCH_SEQ_SETS} from "../constants/action-types";


export function fetchSeqSets() {
  return function (dispatch) {
    fetch('/api/fs/ref_seqs/')
      .then(response => response.json())
      .then(seq_sets => dispatch({
        type: FETCH_SEQ_SETS,
        payload: seq_sets
      }));
  }
}