import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withStyles} from '@material-ui/core/styles';
import {withRouter} from 'react-router-dom';

import Typography from '@material-ui/core/Typography';

import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import LinearProgress from '@material-ui/core/LinearProgress';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import Chip from '@material-ui/core/Chip';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import indigo from '@material-ui/core/colors/indigo';

import {fetchSeqSets} from "../../redux/actions/seqSetsActions";


const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
  },
  menu: {
    width: 200,
  },
  chip: {
    margin: theme.spacing.unit / 2,
  },
  chip_active: {
    background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
    margin: theme.spacing.unit / 2,
  },
  button: {
    margin: theme.spacing.unit,
  },
});

class MappingRuleGenerator extends React.Component {

  state = {
    seq_types: [],
    seq_sets: [],
    type: '*',
    seq_set_name: '*',
    seq_sets_for_type: [],
    need_update: false,
    df: '',
    dfs: [],
    preproc:'*',
    preprocs: [],
  };

  componentDidMount() {
    console.log('Did Mount');
    this.props.fetchSeqSets();
    console.log('called fetchSeqSets');
  }

  componentDidUpdate(prevProps, prevState) {
    console.log('Did Update');
    if (this.state.need_update === true) {
      // At this point, we're in the "commit" phase, so it's safe to load the new data.
      this.props.fetchSeqSets();
      this.setState({['need_update']: false});
    }
  }

  handleChange = event => {
    this.setState({[event.target.name]: event.target.value});
    //this.setState({['need_update']: true});
  };


  render() {
    console.log('Rendering');
    const {classes} = this.props;

    let seq_types = [];
    for (let i = 0; i < this.props.seq_sets.length; i++) {
      seq_types.push(this.props.seq_sets[i]);
    }
    this.state.seq_types = seq_types;

    let seqs = [];
    console.log(this.state.type);
    if (this.state.seq_types.length > 0 && (this.state.type !== '*' && this.state.type !== '')) {
      for (let i = 0; i < this.state.seq_types.length; i++) {
        if (this.state.seq_types[i].type === this.state.type) {
          seqs = this.state.seq_types[i].seqs;
        }
      }
    }
    this.state.seq_sets = seqs;
    console.log(seqs);

    return (
      <div>
        <Typography variant="display1">Generate SNAKEMAKE rule for mapping</Typography>
        <div>
          <Typography >
            Select reference
          </Typography>
          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="type">Sequence type</InputLabel>
            <Select
              value={this.state.type}
              className={classes.textField}
              onChange={this.handleChange}
              inputProps={{
                name: 'type',
                id: 'seq-type',
              }}>
              <MenuItem value="None">
                <em>None</em>
              </MenuItem>
              <MenuItem value="*">
                <em>All</em>
              </MenuItem>

              {this.state.seq_types.map(seq_type => (
                <MenuItem key={seq_type.type.toString()} value={seq_type.type.toString()}>{seq_type.type}</MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="seq_set_name">Sequence name</InputLabel>

            <Select
              value={this.state.seq_set_name}
              className={classes.textField}
              onChange={this.handleChange}
              inputProps={{
                name: 'seq_set_name',
                id: 'seq__name',
              }}>
              <MenuItem value="None">
                <em>None</em>
              </MenuItem>
              <MenuItem value="*">
                <em>All</em>
              </MenuItem>
              {this.state.seq_sets.map(seq_set => (
                <MenuItem key={seq_set.toString()} value={seq_set.toString()}>{seq_set} </MenuItem>
              ))}
            </Select>
          </FormControl>
        </div>

        <div>
          <Typography>Select samples</Typography>
          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="type">Dataset</InputLabel>
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

              {this.state.dfs.map(df => (
                <MenuItem key={df.toString()} value={df.toString()}>{df}</MenuItem>
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
                {this.state.preprocs.map(prepr => (
                  <MenuItem key={prepr.toString()} value={prepr.toString()}>{prepr} </MenuItem>
                ))}

              </Select>
            </FormControl>
        </div>

        <div>
          <Typography>Select mapping options</Typography>
        </div>

      </div>
    )
  }
}


const mapStateToProps = state => ({
  seq_sets: state.seq_sets.seq_sets,
});

MappingRuleGenerator.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchSeqSets: PropTypes.func.isRequired,
};


export default withRouter(connect(mapStateToProps, {fetchSeqSets})(withStyles(styles)(MappingRuleGenerator)))