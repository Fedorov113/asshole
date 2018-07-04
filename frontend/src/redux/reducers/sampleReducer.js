import {FETCH_READS, FETCH_FASTQC} from "../constants/action-types";

const initialState = {
  reads: 'None',
  fastqc: 'None'
};

export default function (state = initialState, action) {
  switch (action.type) {
    case FETCH_READS:
      return {
        ...state,
        reads: action.payload
      };
    case FETCH_FASTQC:
      return {
        ...state,
        fastqc: action.payload
      };
    default:
      return state;
  }
}