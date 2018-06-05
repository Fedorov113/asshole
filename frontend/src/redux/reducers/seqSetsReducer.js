import {FETCH_SEQ_SETS} from "../constants/action-types";

const initialState = {
  seq_sets: []
};

export default function (state = initialState, action) {
  switch (action.type){
    case FETCH_SEQ_SETS:
      return {
        ...state,
        seq_sets: action.payload
      };
    default:
      return state;
  }
}