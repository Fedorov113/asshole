import  { combineReducers } from 'redux';
import datasetReducer from './datasetReducer';
import mp2Reducer from './mp2Reducer'
import personReducer from './personReducer'
import fmtReducer from './fmtReducer'
import seqSetsReducer from './seqSetsReducer'

export default combineReducers({
  datasets: datasetReducer,
  mp2: mp2Reducer,
  persons: personReducer,
  fmt:fmtReducer,
  seq_sets: seqSetsReducer
});