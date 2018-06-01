import {FETCH_PERSONS, FETCH_SUBJECT} from "../constants/action-types";

export function fetchPersons() {
  return function (dispatch) {
    fetch("/api/molot/subject")
      .then(response => response.json())
      .then(persons => dispatch({
        type: FETCH_PERSONS,
        payload: persons
      }));
  }
}

export function fetchSubject(subject_id) {
  return function (dispatch) {
    console.log(subject_id);
    fetch("/api/molot/subject/"+subject_id.toString())
      .then(response => response.json())
      .then(subject => dispatch({
        type: FETCH_SUBJECT,
        payload: subject
      }));
  }
}