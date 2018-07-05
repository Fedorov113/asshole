import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';
import {withStyles} from '@material-ui/core/styles';

import Typography from '@material-ui/core/Typography';
import DatasetSelect from '../dataset/DatasetSelect'

import DatasetsBpLenVis from '../dataset/DatasetsBpLenVis'


const styles = theme => ({
    container: {
      display: 'flex',
      flexWrap: 'wrap',
    },
  })
;

class DfsSamplesBpLenView extends React.Component {

  state = {
    dfs_to_plot: []
  };

  datasetSelectionReady = (dfs_selection) => {
    console.log(dfs_selection);
    this.setState({['dfs_to_plot']:dfs_selection});
  };

  render() {
    const {classes} = this.props;
    return (
      <div>
        <DatasetSelect datasetSelectionReady={this.datasetSelectionReady}/>
        <DatasetsBpLenVis data_to_plot={this.state.dfs_to_plot}/>
      </div>
    )
  }
}


DfsSamplesBpLenView.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withRouter((withStyles(styles)(DfsSamplesBpLenView)))
