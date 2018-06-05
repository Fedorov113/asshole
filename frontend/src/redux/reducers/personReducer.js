import {FETCH_PERSONS, FETCH_SUBJECT} from "../constants/action-types";

const initialState = {
  persons: [],
  subject: {}
};

export default function (state = initialState, action) {
  switch (action.type) {
    case FETCH_PERSONS:
      return {
        ...state,
        persons: action.payload
      };
    case FETCH_SUBJECT:
      return{
        ...state,
        subject: action.payload
      };
    default:
      return state;
  }
 }