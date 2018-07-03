import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withStyles} from '@material-ui/core/styles';

import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import AddIcon from '@material-ui/icons/Add';
import Tooltip from '@material-ui/core/Tooltip';

import DatasetPreprocReadsSelector from '../dataset/DatasetPreprocReadsSelector'

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

class DatasetSelect extends React.Component {

  state = {
    df_preproc_selectors:
      [
        {
          id: 0,
          selection: 'None'
        }
      ],
  };

  componentDidUpdate(prevProps, prevState) {
    console.log('Dataset did update');
    console.log(this.state.df_preproc_selectors);
    console.log(prevState.df_preproc_selectors);
    //compare selectors with prev state
    if (JSON.stringify(this.state.df_preproc_selectors) !== JSON.stringify(prevState.df_preproc_selectors)) {
      let dfs_to_plot = [];
      console.log('Dataset not the same selectors');
      for (let i = 0; i < this.state.df_preproc_selectors.length; i++) {
        if (this.state.df_preproc_selectors[i].selection !== 'None') {
          dfs_to_plot.push(this.state.df_preproc_selectors[i].selection)
        }
      }
      this.props.datasetSelectionReady(dfs_to_plot);
    }
  }

  addSelector = () => {
    let prev_selectors = this.state.df_preproc_selectors;
    const last_id = prev_selectors[prev_selectors.length - 1].id;
    prev_selectors.push({id: last_id + 1, selection: 'None'});
    this.setState({['df_preproc_selectors']: prev_selectors});
  };

  getDataFromSelector = (data_from_selector) => {
    //Why slice - https://github.com/facebook/react/issues/2914
    let df_preproc_selectors = this.state.df_preproc_selectors.slice();
    for (let i = 0; i < df_preproc_selectors.length; i++) {
      if (df_preproc_selectors[i].id === data_from_selector.id) {
        df_preproc_selectors[i] = data_from_selector;
      }
    }
    this.setState({['df_preproc_selectors']: df_preproc_selectors});
  };

  removeSelector = (id) => {
    console.log('remove selector');
    if (this.state.df_preproc_selectors.length < 2) {
      return
    }
    let prev_selectors = this.state.df_preproc_selectors.slice();
    for (let i = 0; i < prev_selectors.length; i++) {
      if (prev_selectors[i].id === id) {
        prev_selectors.splice(i, 1)
      }
    }
    this.setState({['df_preproc_selectors']: prev_selectors});
  };

  render() {
    const {classes} = this.props;


    return (
      <div>
        {/*Assuming this is a component with dataset level selection*/}
        <Typography>Select Dataset and Preprocessing</Typography>
        <Grid container spacing={16}>
          <Grid container spacing={24}>
            {this.state.df_preproc_selectors.map(selector => (
              <Grid key={selector.id} item>
                <DatasetPreprocReadsSelector
                  id={selector.id}
                  removeSelector={this.removeSelector}
                  getDataFromSelector={this.getDataFromSelector}
                />
              </Grid>
            ))}
            <Grid>
              <Tooltip id="tooltip-fab" title="Add">
                <Button variant="fab"
                        color="primary"
                        aria-label="Add"
                        onClick={this.addSelector}
                        className={classes.fab}>
                  <AddIcon/>
                </Button>
              </Tooltip>
            </Grid>
          </Grid>
        </Grid>

      </div>
    )
  }
}


DatasetSelect.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default (withStyles(styles)(DatasetSelect))
