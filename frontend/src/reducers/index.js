import  { combineReducers } from 'redux';
import datasetReducer from './datasetReducer';
import mp2Reducer from './mp2Reducer'

export default combineReducers({
  datasets: datasetReducer,
  mp2: mp2Reducer
});