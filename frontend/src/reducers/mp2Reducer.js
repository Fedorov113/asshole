import {FETCH_MP2} from "../constants/action-types";

const initialState = {
  mp2: {}
};

export default function (state = initialState, action) {
  switch (action.type){
    case FETCH_MP2:
      return {
        ...state,
        mp2: action.payload
      };
    default:
      return state;
  }
}