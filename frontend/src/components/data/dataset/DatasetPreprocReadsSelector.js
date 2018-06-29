import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withStyles} from '@material-ui/core/styles';

import Paper from '@material-ui/core/Paper';

import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import InputLabel from '@material-ui/core/InputLabel';

import {fetchReads} from "../../../redux/actions/sampleActions";
import {fetchDatasets, fetchDatasetsFS, fetchDatasetsPreprocsFS} from "../../../redux/actions/datasetActions";

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

let id = 0;

function createDataForTable(name, r1_size, r2_size, bp, reads) {
  id += 1;
  return {id, name, r1_size, r2_size, bp, reads}
}

class DatasetPreprocReadsSelector extends React.Component {
  state = {
    df: '*',
    preproc: '*',
    preprocs: [],
    samples_w_reads: [],
    data: [],
    dfs: [],
    need_parsing: true,
    need_update: true
  };

  parseReads = (fsNode) => {
    let sample = {};
    sample.sample_name = fsNode['node_name'];
    sample.files = [];
    let sample_name = fsNode['node_name'];
    let r1_size = '';
    let r2_size = '';
    let bp = 0;
    let reads = 0;
    for (let i = 0; i < fsNode['children'].length; i++) {
      let file = this.parseFSNode(fsNode['children'][i]);
      if (file['node_name'].includes('_R1')) {
        r1_size = file['size']
      }
      else if (file['node_name'].includes('_R2')) {
        r2_size = file['size']
      }
      bp += parseInt(file['bp']);
      reads += parseInt(file['reads']);
    }
    this.state.samples_w_reads.push(sample);
    this.state.data.push(createDataForTable(sample_name, r1_size, r2_size, bp, reads));


  };

  parseFSNode = (fsNode) => {
    if (fsNode['type'] === 'dir') {
      if (fsNode.hasOwnProperty('children')) {
        if (fsNode['children'].length > 0) {
          if (fsNode['level'] === 0) { //node containing datasets
            let dfs = [];
            for (let i = 0; i < fsNode['children'].length; i++) {
              dfs.push(fsNode['children'][i]['node_name']);
              this.parseFSNode(fsNode['children'][i])
            }
            this.setState({['dfs']: dfs});
          }
          if (fsNode['level'] === 4) {
            this.parseReads(fsNode)
          }
          else {
            for (let i = 0; i < fsNode['children'].length; i++) {
              this.parseFSNode(fsNode['children'][i])
            }
          }
        }
        return fsNode;
      }
    }
    else if (fsNode['type'] === 'file') {
      return fsNode;
    }
  };

  parseFSObject = (fsObject) => {
    this.state.samples_w_reads = [];
    if (Object.keys(fsObject).length === 0 && fsObject.constructor === Object)
      return;
    if (this.state.need_parsing === true) {
      console.log('PARSING');
      this.parseFSNode(fsObject);
      this.props.callbackFromParent({df:this.state.df, preproc:this.state.preproc});
      this.setState({['need_parsing']: false});
    }
  };

  componentDidMount() {
    console.log('DID MOUNT');
    this.props.fetchDatasetsFS();
  }

  componentDidUpdate(prevProps, prevState) {
    console.log('DID UPDATE');

    //Here we load preprocs for df
    if (this.props.datasets_fs.loaded &&
        this.state.df !== '*' &&
        this.state.df !== prevState.df){
      this.props.fetchDatasetsPreprocsFS(this.state.df);
    }

    if (this.state.need_update) {
      console.log('updating, df: ' + this.state.df);
      this.props.fetchReads(this.state.df, this.state.preproc);
      this.setState({['need_update']: false});
    }

    if ( JSON.stringify(prevProps.reads) !== JSON.stringify(this.props.reads)){
      this.setState({['need_parsing']: true});
    }

    this.parseFSObject(this.props.reads);
  }

  handleChange = event => {
    this.setState({[event.target.name]: event.target.value});
    this.setState({['need_update']: true});
    this.setState({['need_parsing']: true});
    this.setState({['data']: []});
    this.setState({['dfs']: []});
  };

  render() {
    const {classes} = this.props;

    return (
      <Paper>
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
              <MenuItem value={df.toString()}>{df} </MenuItem>
            ))}
          </Select>
        </FormControl>


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
              <MenuItem value={preproc.toString()}>{preproc} </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Paper>
    )
  }
}

const mapStateToProps = state => ({
  reads: state.sample.reads,
  datasets_fs: state.datasets.datasets_fs,
  dataset_preprocs: state.datasets.dataset_preprocs
});

DatasetPreprocReadsSelector.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchReads: PropTypes.func.isRequired,
  fetchDatasetsFS: PropTypes.func.isRequired,
  fetchDatasetsPreprocsFS: PropTypes.func.isRequired,
  datasets_fs: PropTypes.object.isRequired,
  dataset_preprocs: PropTypes.array.isRequired,
};

export default connect(mapStateToProps, {fetchReads, fetchDatasetsFS, fetchDatasetsPreprocsFS})
(withStyles(styles)(DatasetPreprocReadsSelector))