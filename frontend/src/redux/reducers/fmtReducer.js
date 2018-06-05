import {FETCH_FMT} from "../constants/action-types";

const initialState = {
  fmt: {}
};

export default function (state = initialState, action) {
  switch (action.type){
    case FETCH_FMT:
      return {
        ...state,
        fmt: action.payload
      };
    default:
      return state;
  }
}