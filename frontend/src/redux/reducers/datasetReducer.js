import {FETCH_DATASETS, NEW_DATASET} from "../constants/action-types";

const initialState = {
  datasets: [],
  dataset: {}
};

export default function (state = initialState, action) {
  switch (action.type) {
    case FETCH_DATASETS:
      return {
        ...state,
        datasets: action.payload
      };
    default:
      return state;
  }
 }