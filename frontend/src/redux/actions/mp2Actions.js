import {FETCH_MP2, FETCH_MP2_SCATTER, FETCH_MP2_BOX} from "../constants/action-types";


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

export function fetchMp2Boxplot(df, preproc) {
  return function (dispatch) {
    fetch('/api/fs/mp2_box/?df='+df+'&preproc='+preproc)
      .then(response => response.json())
      .then(mp2_box => dispatch({
        type: FETCH_MP2_BOX,
        payload: mp2_box
      }))
  }

}

export function fetchMp2ScatterResult(level) {
  return function (dispatch) {
    fetch('/api/fs/sample/mp2_scatter/')
      .then(response => response.json())
      .then(mp2_scatter => dispatch({
        type: FETCH_MP2_SCATTER,
        payload: mp2_scatter
      }));
  }
}
