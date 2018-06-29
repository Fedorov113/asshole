import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withStyles} from '@material-ui/core/styles';

import Paper from '@material-ui/core/Paper';

import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import InputLabel from '@material-ui/core/InputLabel';


import Button from '@material-ui/core/Button';
import DeleteIcon from '@material-ui/icons/Delete';
import IconButton from '@material-ui/core/IconButton';
import Tooltip from '@material-ui/core/Tooltip';

import {fetchDatasetsFS, fetchDatasetsPreprocsFS} from "../../../redux/actions/datasetActions";

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
});

class DatasetPreprocReadsSelector extends React.Component {
  state = {
    df: '*',
    dfs: [],
    preproc: '*',
    preprocs: [],
    need_parsing: true,
    need_update: true
  };

  componentDidMount() {
    this.props.fetchDatasetsFS();
  }

  componentDidUpdate(prevProps, prevState) {
    //Here we load preprocs for df
    if (this.props.datasets_fs.loaded &&
      this.state.df !== '*' &&
      this.state.df !== prevState.df) {
      this.props.fetchDatasetsPreprocsFS(this.state.df);
    }

    if (this.state.need_update) {
      this.setState({['need_update']: false});
    }

    if ((this.state.df !== prevState.df || this.state.preproc !== prevState.preproc)
      && this.state.df !== '*' && this.state.preproc !== '*') {
      this.setState({['need_parsing']: true});
      this.props.callbackFromParent({
        id: this.props.id,
        selection: {
          df: this.state.df,
          preproc: this.state.preproc
        }
      });
    }
  }

  handleChange = event => {
    this.setState({[event.target.name]: event.target.value});
    this.setState({['need_update']: true});
    this.setState({['need_parsing']: true});
    this.setState({['dfs']: []});
  };


  render() {
    const {classes} = this.props;
    return (
      <Paper>
        <Tooltip id="tooltip-icon" title="Delete" placement="right">
          <Button
            aria-label="Delete"
            onClick={()=>this.props.removeSelector(this.props.id)}>
            <DeleteIcon/>
          </Button>
        </Tooltip>
        <div>
          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="df">Dataset</InputLabel>
            <Select
              value={this.state.df}
              className={classes.textField}
              onChange={this.handleChange}
              inputProps={{
                name: 'df',
                id: 'df',
              }}>
              <MenuItem value="None">
                <em>None</em>
              </MenuItem>
              <MenuItem value="*">
                <em>All</em>
              </MenuItem>
              {this.props.datasets_fs.datasets.map(df => (
                <MenuItem key={df.toString()} value={df.toString()}>{df} </MenuItem>
              ))}
            </Select>
          </FormControl>
        </div>

        <div>
          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="preproc">Preprocessing</InputLabel>
            <Select
              value={this.state.preproc}
              className={classes.textField}
              onChange={this.handleChange}
              inputProps={{
                name: 'preproc',
                id: 'preproc',
              }}>
              <MenuItem value="None">
                <em>None</em>
              </MenuItem>
              <MenuItem value="*">
                <em>All</em>
              </MenuItem>
              {this.props.dataset_preprocs.map(preproc => (
                <MenuItem key={preproc.toString()}
                          value={preproc.toString()}>
                  {preproc}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </div>

      </Paper>
    )
  }
}

const mapStateToProps = state => ({
  datasets_fs: state.datasets.datasets_fs,
  dataset_preprocs: state.datasets.dataset_preprocs
});

DatasetPreprocReadsSelector.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchDatasetsFS: PropTypes.func.isRequired,
  fetchDatasetsPreprocsFS: PropTypes.func.isRequired,
  datasets_fs: PropTypes.object.isRequired,
  dataset_preprocs: PropTypes.array.isRequired,
};

export default connect(mapStateToProps, {fetchDatasetsFS, fetchDatasetsPreprocsFS})
(withStyles(styles)(DatasetPreprocReadsSelector))