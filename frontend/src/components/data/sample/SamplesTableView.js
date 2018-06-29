import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';
import {withStyles} from '@material-ui/core/styles';

import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import AddIcon from '@material-ui/icons/Add';
import Tooltip from '@material-ui/core/Tooltip';

import DatasetPreprocReadsSelector from '../dataset/DatasetPreprocReadsSelector'
import DatasetsBpLenVis from '../dataset/DatasetsBpLenVis'


const styles = theme => ({
    container: {
      display: 'flex',
      flexWrap: 'wrap',
    },
    table: {
      minWidth: 700,
    },
    textField: {
      marginLeft: theme.spacing.unit,
      marginRight: theme.spacing.unit,
      width: 200
    },
    formControl: {
      margin: theme.spacing.unit * 2,
      minWidth: 120,
      padding: theme.spacing.unit,
    },
    fab: {
      position: 'relative',
      top: '50%',
      transform: 'translateY(-50%)',
    },
  })
;

let id = 0;

function createDataForTable(name, r1_size, r2_size, bp, reads) {
  id += 1;
  return {id, name, r1_size, r2_size, bp, reads}
}

class SamplesTableView extends React.Component {

  state = {
    df_preproc_selectors:
      [
        {
          id: 0,
          selection: 'None'
        }
      ],
  };


  addSelector = () => {
    let prev_selectors = this.state.df_preproc_selectors;
    const last_id = prev_selectors[prev_selectors.length - 1].id;
    prev_selectors.push({id: last_id + 1, selection: 'None'});
    this.setState({['df_preproc_selectors']: prev_selectors});
  };

  getDataFromSelector = (data_from_selector) => {
    console.log('getDataFromSelector');

    let df_preproc_selectors = this.state.df_preproc_selectors;

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
    let prev_selectors = this.state.df_preproc_selectors;
    for (let i = 0; i < prev_selectors.length; i++) {
      if (prev_selectors[i].id === id) {
        prev_selectors.splice(i, 1)
      }
    }
    this.setState({['df_preproc_selectors']: prev_selectors});
  };

  render() {
    const {classes} = this.props;

    let data_to_plot = [];
    for (let i = 0; i < this.state.df_preproc_selectors.length; i++) {
      if (this.state.df_preproc_selectors[i].selection !== 'None') {
        data_to_plot.push(this.state.df_preproc_selectors[i].selection)
      }
    }

    return (
      <div>
        <Grid container spacing={16}>
          <Grid container spacing={24}>
            {this.state.df_preproc_selectors.map(selector => (
              <Grid key={selector.id} item>
                <DatasetPreprocReadsSelector
                  id={selector.id}
                  removeSelector={this.removeSelector}
                  callbackFromParent={this.getDataFromSelector}
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

        <DatasetsBpLenVis data_to_plot={data_to_plot}/>


      </div>
    )
  }
}


SamplesTableView.propTypes = {

  classes: PropTypes.object.isRequired,
};

export default withRouter((withStyles(styles)(SamplesTableView)))
