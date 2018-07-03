import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';
import {withStyles} from '@material-ui/core/styles';

import DatasetSelect from '../data/dataset/DatasetSelect'
import Mp2BoxplotViz from './Mp2BoxplotViz'


const styles = theme => ({
    container: {
      display: 'flex',
      flexWrap: 'wrap',
    },
    fab: {
      position: 'relative',
      top: '50%',
      transform: 'translateY(-50%)',
    },
  })
;

class Mp2Boxplot extends React.Component {

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
        {/*Assuming this is a component with dataset level selection*/}
        <DatasetSelect datasetSelectionReady={this.datasetSelectionReady}/>

        {/*We need to pass the component to plot here*/}
        <Mp2BoxplotViz dfs_to_plot={this.state.dfs_to_plot}/>
      </div>
    )
  }
}


Mp2Boxplot.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withRouter((withStyles(styles)(Mp2Boxplot)))
