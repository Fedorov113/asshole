import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import Plot from 'react-plotly.js';

import {fetchMappingForHeatmap} from "../../redux/actions/mappingActions"

class MappingHeatmap extends React.Component{

  render(){
    // let dataToPlot = [];
    //
    // if (this.props.mapping_heatmap !== undefined) {
    //   dataToPlot = [
    //     {
    //       z: this.props.mapping_heatmap.data,
    //       x: this.props.mapping_heatmap.columns,
    //       y: this.props.mapping_heatmap.index,
    //       type: 'heatmap'
    //     }
    //   ];
    // }

    return (
      <Plot
            useResizeHandler={true}
            data={dataToPlot}
            style={{width: '100%', minHeight: '1000px', marginTop: '12pt'}}
            layout={{autosize: true, title: 'Mapping Heatmap'}}
          />
    )
  }
}

export default MappingHeatmap