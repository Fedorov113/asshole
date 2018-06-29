import {FETCH_DATASETS, FETCH_DATASETS_FS, FETCH_DATASET_PREPROCS, NEW_DATASET} from "../constants/action-types";

const initialState = {
  datasets: [],
  dataset: {},
  dataset_preprocs: [],
  datasets_fs: {
    datasets: [],
    loaded: false
  },

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
    case FETCH_DATASET_PREPROCS:
      return {
        ...state,
        dataset_preprocs: action.payload,
      };
    default:
      return state;
  }
}