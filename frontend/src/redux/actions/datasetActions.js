import {FETCH_DATASETS, NEW_DATASET} from "../constants/action-types";

export function fetchDatasets() {
  return function (dispatch) {
    fetch("/api/molot/dataset")
      .then(response => response.json())
      .then(datasets => dispatch({
        type: FETCH_DATASETS,
        payload: datasets
      }));
  }
}

export function createDataset(datasetData) {
  return function (dispatch) {
    fetch("/api/molot/")
      .then(response => response.json())
      .then(datasets => dispatch({
        type: FETCH_DATASETS,
        payload: datasets
      }));
  }
}