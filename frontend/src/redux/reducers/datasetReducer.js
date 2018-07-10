import {
  FETCH_DATASETS,
  FETCH_DATASET_LIST,
  FETCH_DATASETS_FS,
  FETCH_DATASET_PREPROCS,
  FETCH_DATASET_GENERAL_TAXA_COMPOSITION,
  NEW_DATASET
} from "../constants/action-types";

const initialState = {
  datasets: [],
  dataset: {},
  dataset_preprocs: [],
  datasets_fs: {
    datasets: [],
    loaded: false
  },
  dataset_list: [],
  general_taxa_composition: [],

};

export default function (state = initialState, action) {
  switch (action.type) {
    case FETCH_DATASETS:
      return {
        ...state,
        datasets: action.payload
      };
    case FETCH_DATASETS_FS:
      return {
        ...state,
        datasets_fs:
          {
            datasets: action.payload,
            loaded: true
          }
      };
    case FETCH_DATASET_LIST:
      return {
        ...state,
        dataset_list: action.payload,
      };
    case FETCH_DATASET_PREPROCS:
      return {
        ...state,
        dataset_preprocs: action.payload,
      };
    case FETCH_DATASET_GENERAL_TAXA_COMPOSITION:
      return {
        ...state,
        general_taxa_composition: action.payload,
      };
    default:
      return state;
  }
}