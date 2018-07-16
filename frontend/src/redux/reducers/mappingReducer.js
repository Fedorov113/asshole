import {FETCH_MAPPING_FOR_REF, FETCH_MAPPING_FOR_HEATMAP} from "../constants/action-types";

const initialState = {
  file_structure: {
    data: {},
    loaded: false
  },
  heatmap_data: {}
};

export default function (state = initialState, action) {
  switch (action.type) {
    case FETCH_MAPPING_FOR_REF:
      return {
        ...state,
        file_structure: {
          data: action.payload,
          loaded: true
        }
      };
    case FETCH_MAPPING_FOR_HEATMAP:
      return {
        ...state,
        heatmap_data: action.payload
      };
    default:
      return state;
  }
}