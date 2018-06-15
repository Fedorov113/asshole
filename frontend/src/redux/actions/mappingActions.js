import {FETCH_MAPPING_FOR_REF, FETCH_MAPPING_FOR_HEATMAP} from "../constants/action-types";


export function fetchMappingForRef(df, preproc, tool, seq_type, seq_name, postproc) {
  return function (dispatch) {
    let url = '/api/fs/mapping/'+df+'/'+preproc+'/'+tool+'/'+seq_type+'/'+seq_name+'/'+postproc;
    console.log(url);
    fetch(url)
      .then(response => response.json())
      .then(file_structure => dispatch({
        type: FETCH_MAPPING_FOR_REF,
        payload: file_structure
      }));
  }
}

export function fetchMappingForHeatmap(df, preproc, tool, seq_type, seq_name, postproc, samples) {
  return function (dispatch) {
    if (samples.length < 1)
      return 0;
    let url = '/api/fs/mapping/'+df+'/'+preproc+'/'+tool+'/'+seq_type+'/'+seq_name+'/'+postproc+'/?samples=';

    for (let i = 0; i < samples.length; i++){
      url += samples[i];
      if (i !== samples.length-1)
        url += ','
    }
    console.log(url);
    fetch(url)
      .then(response => response.json())
      .then(heatmap_data => dispatch({
        type: FETCH_MAPPING_FOR_HEATMAP,
        payload: heatmap_data
      }));
  }
}