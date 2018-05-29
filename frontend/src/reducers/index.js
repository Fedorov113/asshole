import  { combineReducers } from 'redux';
import datasetReducer from './datasetReducer';
import mp2Reducer from './mp2Reducer'
import personReducer from './personReducer'

export default combineReducers({
  datasets: datasetReducer,
  mp2: mp2Reducer,
  persons: personReducer
});