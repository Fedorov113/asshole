import {FETCH_DATASETS, FETCH_DATASET_LIST, FETCH_DATASETS_FS,
  FETCH_DATASET_PREPROCS, FETCH_DATASET_GENERAL_TAXA_COMPOSITION} from "../constants/action-types";

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

export function fetchDatasetsFS() {
  return function (dispatch) {
    fetch("/api/fs/dataset")
      .then(response => response.json())
      .then(datasets_fs => dispatch({
        type: FETCH_DATASETS_FS,
        payload: datasets_fs
      }));
  }
}
export function fetchDatasetList() {
  return function (dispatch) {
    fetch("/api/fs/datasets")
      .then(response => response.json())
      .then(dataset_list => dispatch({
        type: FETCH_DATASET_LIST,
        payload: dataset_list
      }));
  }
}

export function fetchDatasetsPreprocsFS(df) {
  return function (dispatch) {
    fetch("/api/fs/dataset/"+df+'/preprocs')
      .then(response => response.json())
      .then(dataset_preprocs => dispatch({
        type: FETCH_DATASET_PREPROCS,
        payload: dataset_preprocs
      }));
  }
}

export function fetchDatasetGeneralTaxaComposition(df, preproc, tool) {
  return function (dispatch) {
    fetch('/api/fs/general_taxa_composition/'+df+'/'+preproc+'/'+tool+'/')
      .then(response => response.json())
      .then(general_taxa_composition => dispatch({
        type: FETCH_DATASET_GENERAL_TAXA_COMPOSITION,
        payload: general_taxa_composition
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