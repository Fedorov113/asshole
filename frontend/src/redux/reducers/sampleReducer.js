import {FETCH_READS} from "../constants/action-types";

const initialState = {
  reads: {}
};

export default function (state = initialState, action) {
  switch (action.type) {
    case FETCH_READS:
      return {
        ...state,
        reads: action.payload
      };
    default:
      return state;
  }
}