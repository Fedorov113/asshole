import {FETCH_READS, FETCH_FASTQC} from "../constants/action-types";

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

export function fetchFastqc(df, preproc, sample) {
  return function (dispatch) {
    fetch('/api/fs/fastqc/'+df+'/'+preproc+'/'+sample)
      .then(response => response.text())
      .then(fastqc => dispatch({
        type: FETCH_FASTQC,
        payload: fastqc
      }));
  }
}