import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';

import MenuItem from '@material-ui/core/MenuItem';
import Typography from '@material-ui/core/Typography';

import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import LinearProgress from '@material-ui/core/LinearProgress';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import Chip from '@material-ui/core/Chip';
import {withStyles} from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormLabel from '@material-ui/core/FormLabel';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import TextField from '@material-ui/core/TextField';


import {fetchSeqSets} from "../../redux/actions/seqSetsActions";
import {fetchMappingForRef, fetchMappingForHeatmap} from "../../redux/actions/mappingActions"

import MappingParser from './MappingParser'

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200
  },
  textFieldLong: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 500,
  },
  formControl: {
    margin: theme.spacing.unit * 2,
    minWidth: 120,
    padding: theme.spacing.unit,
  },
  formControlLong: {
    margin: theme.spacing.unit * 2,
    minWidth: 350,
    padding: theme.spacing.unit,
  },
  text: {
    width: 400
  },
  block: {
    margin: theme.spacing.unit,
    padding: theme.spacing.unit
  },
  group: {
    margin: `${theme.spacing.unit}px 0`,
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


class MappingSelector extends React.Component {

  state = {
    seq_types: [],
    seq_sets: [],
    type: 'None',
    seq_set_name: 'None',
    seq_sets_for_type: [],
    df: '*',
    dfs: [],
    preproc: '*',
    preprocs: [],
    tool: '*',
    tools: [],
    postproc: '*',
    postprocs: [],
    samples: [],
    chips: [],
    selected_chips: [],

    loaded: false,
    need_update: false,
    need_parsing: false,
    value: 'female',
    min_avg_cov: '',
    min_width: '',
    filter_query: 'Avg_fold_{s} > 0.5 and Covered_percent_{s} > 45 or '
  };

  componentDidMount() {
    this.props.fetchSeqSets();
  };

  componentDidUpdate(prevProps, prevState) {
    console.log('DID UPDATE');
    if (this.state.type !== prevState.type) {
      console.log('Setting seq set name to None');
      this.setState({['seq_set_name']: 'None'});
    }

    if (this.state.type !== 'None' && this.state.seq_set_name !== 'None') {
      if (this.state.type !== prevState.type || this.state.seq_set_name !== prevState.seq_set_name) {
        console.log('NEED UPDATE');
        this.setState({['need_update']: true});
      }
    }

    if (this.state.need_update) {
      console.log('FETCHING FS');
      this.props.fetchMappingForRef(this.state.df, this.state.preproc, this.state.tool, this.state.type,
        this.state.seq_set_name, this.state.postproc);
      this.setState({['need_update']: false});
      this.setState({['need_parsing']: true});
    }


    if (this.state.need_parsing) {
      this.populateSelectors(prevState);
    }

  }

  populateSelectors = (prevState) => {
    console.log('populating');
    let dfs = [];
    let preprocs = [];
    let tools = [];
    let post = [];
    let samples = [];
    let chips = [];
    if (this.props.mapping_fs.loaded === true) {
      let mapping_fs = new MappingParser(this.props.mapping_fs.data);
      dfs = mapping_fs.datasets;
      if (dfs.indexOf(this.state.df) !== -1) {
        preprocs = mapping_fs.preprocs_for_df(this.state.df);
        if (preprocs.indexOf(this.state.preproc) !== -1) {
          tools = mapping_fs.tools_for_preproc(this.state.df, this.state.preproc);
          if (tools.indexOf(this.state.tool) !== -1) {
            post = mapping_fs.postprocs_for_tool(this.state.df, this.state.preproc,
              this.state.tool);
            if (post.indexOf(this.state.postproc) !== -1) {
              samples = mapping_fs.samples_for_post(this.state.df, this.state.preproc,
                this.state.tool, this.state.postproc);
              for (let i = 0; i < samples.length; i++) {
                chips.push({key: chips.length, label: samples[i], selected: false})
              }
            }
          }
        }
      }
    }

    this.setSelectorState('dfs', dfs, prevState);
    this.setSelectorState('preprocs', preprocs, prevState);
    this.setSelectorState('tools', tools, prevState);
    this.setSelectorState('postprocs', post, prevState);

    if (JSON.stringify(this.state.chips) !== JSON.stringify(chips)) {
      this.setState({['chips']: chips});
      this.setState({['need_parsing']: false})
    }

  };

  setSelectorState = (name, object, prevState) => {
    console.log(this.state[name]);
    let short_name = name.slice(0, name.length - 1);
    if (JSON.stringify(this.state[name]) !== JSON.stringify(object) ||
      this.state[short_name] !== prevState[short_name]) {

      this.setState({[name]: object});
      if (object.length === 1) {
        this.setState({[name.slice(0, name.length - 1)]: object[0]});
      }
    }
  };

  clearParams = data => () => {
    this.setState({['type']: 'None'});
    this.setState({['seq_set_name']: 'None'});
    this.setState({['df']: 'None'});
    this.setState({['preproc']: 'None'});
    this.setState({['tool']: 'None'});
    this.setState({['postproc']: 'None'});
    this.setState({['need_update']: true});
    this.setState({['need_parsing']: true});
  };

  handleChange = event => {
    this.setState({[event.target.name]: event.target.value});
  };

  handleTextChange = name => event => {
    this.setState({
      [name]: event.target.value,
    });
  };

  handleDelete = data => () => {
    if (data.label === 'React') {
      alert('Why would you want to delete React?! :)'); // eslint-disable-line no-alert
      return;
    }

    const chipData = [...this.state.chipData];
    const chipToDelete = chipData.indexOf(data);
    chipData.splice(chipToDelete, 1);
    this.setState({chipData});
  };

  clickChip = data => () => {
    console.log(this.state.chips);

    let this_chips = this.state.chips;
    let selected_chips = this.state.selected_chips;
    let selected_chip = this_chips[data.key];

    //this_chips[data.key].selected = !data.selected;

    let index_of_selected = selected_chips.indexOf(selected_chip);
    if (index_of_selected === -1) {
      selected_chips.push(selected_chip);
    }
    else {
      selected_chips.splice(index_of_selected, 1)
    }

    this.setState({['selected_chips']: selected_chips});
  };


  selectAll = data => () => {
    let this_files = this.state.files
    for (var i = 0; i < this_files.length; i++) {
      this_files[i].selected = true;
    }
    this.setState({['files']: this_files});
  };

  drawHeatmap = data => () => {
    console.log('draw button clicked');
    let selected_samples = [];
    for (let i = 0; i < this.state.files.length; i++) {
      if (this.state.files[i].selected === true) {
        selected_samples.push(this.state.files[i].label)
      }
    }
    console.log(selected_samples);
    this.props.fetchMappingForHeatmap(this.state.df, this.state.preproc, this.state.tool, this.state.type,
      this.state.seq_set_name, this.state.postproc, selected_samples, this.state.filter_query);
  };


  render() {
    const {classes} = this.props;

    let seqs_of_type = [];
    if (this.state.type !== 'None') {
      for (let i = 0; i < this.props.seq_sets.length; i++) {
        if (this.props.seq_sets[i].type === this.state.type) {
          seqs_of_type = this.props.seq_sets[i].seqs;
        }
      }
    }

    return (
      <div>
        <Paper className={classes.block}>
          <Typography>
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

              {this.props.seq_sets.map(seq_set => (
                <MenuItem value={seq_set.type.toString()} key={seq_set.type.toString()}>
                  {seq_set.type}
                </MenuItem>
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
              {seqs_of_type.map(seq_set => (
                <MenuItem value={seq_set.toString()} key={seq_set.toString()}>{seq_set} </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Paper>

        <Paper className={classes.block}>
          <Typography>
            Select samples
          </Typography>

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
              {this.state.dfs.map(df => (
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
              {this.state.preprocs.map(prepr => (
                <MenuItem value={prepr.toString()}>{prepr} </MenuItem>
              ))}

            </Select>
          </FormControl>

          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="tool">Mapping Tool</InputLabel>
            <Select
              value={this.state.tool}
              className={classes.textField}
              onChange={this.handleChange}
              inputProps={{
                name: 'tool',
                id: 'tool',
              }}>
              <MenuItem value="None">
                <em>None</em>
              </MenuItem>
              <MenuItem value="*">
                <em>All</em>
              </MenuItem>
              {this.state.tools.map(too => (
                <MenuItem value={too.toString()}>{too} </MenuItem>
              ))}

            </Select>
          </FormControl>

          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="tool">Mapping Postprocessing</InputLabel>
            <Select
              value={this.state.postproc}
              className={classes.textField}
              onChange={this.handleChange}
              inputProps={{
                name: 'postproc',
                id: 'postproc',
              }}>
              <MenuItem value="None">
                <em>None</em>
              </MenuItem>
              <MenuItem value="*">
                <em>All</em>
              </MenuItem>
              {this.state.postprocs.map(postproc => (
                <MenuItem value={postproc.toString()}>{postproc} </MenuItem>
              ))}

            </Select>
          </FormControl>

          <div>
            <Button variant="outlined" color="primary" className={classes.button} onClick={this.selectAll(0)}>
              Select all samples
            </Button>

            <Button variant="outlined" color="primary" className={classes.button} onClick={this.clearParams(0)}>
              Clear params
            </Button>

            <Button variant="outlined" color="secondary" className={classes.button} onClick={this.drawHeatmap(0)}>
              Draw Heatmap
            </Button>
          </div>

          <Paper>
            {this.state.chips.map(data => (
              <Chip
                key={data.key}
                label={data.label}
                onClick={this.clickChip(data)}
                onDelete={this.handleDelete(data)}
                className={data.selected ? classes.chip_active : classes.chip}
              />
            ))}
          </Paper>
        </Paper>

        <div>
          <Paper className={classes.block}>
            <Typography>Filter by average coverage and coverage percent</Typography>
            <FormControl component="fieldset" required className={classes.formControl}>
              <FormLabel component="legend">Type</FormLabel>
              <RadioGroup
                aria-label="gender"
                name="gender1"
                className={classes.group}
                value={this.state.value}
                onChange={this.handleChange}
              >
                <FormControlLabel value="at_least_one" control={<Radio/>} label="At least 1 contains"/>
                <FormControlLabel
                  value="disabled"
                  disabled
                  control={<Radio/>}
                  label="(Disabled option)"
                />
              </RadioGroup>
            </FormControl>
            <FormControl className={classes.formControlLong}>
              <TextField
                fullWidth
                id="filter_query"
                label="Filter Query"
                className={classes.textFieldLong}
                value={this.state.filter_query}
                onChange={this.handleTextChange('filter_query')}
                margin="normal"
                multiline
                rowsMax="3"
              />
            </FormControl>
          </Paper>
        </div>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  seq_sets: state.seq_sets.seq_sets,
  mapping_fs: state.mapping.file_structure,
  mapping_heatmap: state.mapping.heatmap_data
});

MappingSelector.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchSeqSets: PropTypes.func.isRequired,
  fetchMappingForRef: PropTypes.func.isRequired,
  fetchMappingForHeatmap: PropTypes.func.isRequired,
};

export default connect(mapStateToProps, {
  fetchSeqSets,
  fetchMappingForRef,
  fetchMappingForHeatmap
})(withStyles(styles)(MappingSelector));