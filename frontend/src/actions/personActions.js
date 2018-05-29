import {FETCH_PERSONS} from "../constants/action-types";

export function fetchPersons() {
  return function (dispatch) {
    fetch("/api/mis/person")
      .then(response => response.json())
      .then(persons => dispatch({
        type: FETCH_PERSONS,
        payload: persons
      }));
  }
}