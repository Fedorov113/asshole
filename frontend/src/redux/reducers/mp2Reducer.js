import {FETCH_MP2,FETCH_MP2_SCATTER} from "../constants/action-types";

const initialState = {
  mp2: {},
  mp2_scatter: {}
};

export default function (state = initialState, action) {
  switch (action.type){
    case FETCH_MP2:
      return {
        ...state,
        mp2: action.payload
      };
    case FETCH_MP2_SCATTER:
      return {
        ...state,
        mp2_scatter: action.payload
      };
    default:
      return state;
  }
}