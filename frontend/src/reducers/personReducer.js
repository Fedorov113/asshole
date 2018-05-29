import {FETCH_PERSONS} from "../constants/action-types";

const initialState = {
  persons: [],
  person: {}
};

export default function (state = initialState, action) {
  switch (action.type) {
    case FETCH_PERSONS:
      return {
        ...state,
        persons: action.payload
      };
    default:
      return state;
  }
 }