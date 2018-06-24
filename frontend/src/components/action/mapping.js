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



import Plot from 'react-plotly.js';


import {fetchSeqSets} from "../../redux/actions/seqSetsActions";
import {fetchMappingForRef, fetchMappingForHeatmap} from "../../redux/actions/mappingActions"

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
    margin: theme.spacing.unit * 2,
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

class Mapping extends React.Component {
  state = {
    seq_types: [],
    seq_sets: [],
    type: '*',
    seq_set_name: '*',
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
    files: [],
    loaded: false,
    need_update: false,
    need_parsing: true,
    value: 'female',
    min_avg_cov: '',
    min_width: '',
    filter_query: 'Avg_fold_{s} > 0.5 and Covered_percent_{s} > 45 or '
  };

  componentDidMount() {
    this.props.fetchSeqSets();
    this.props.fetchMappingForRef(this.state.df, this.state.preproc, this.state.tool, this.state.type,
      this.state.seq_set_name, this.state.postproc);
    this.state.need_parsing = true;
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.state.need_update === true) {
      // At this point, we're in the "commit" phase, so it's safe to load the new data.
      this.props.fetchMappingForRef(this.state.df, this.state.preproc, this.state.tool, this.state.type,
        this.state.seq_set_name, this.state.postproc);
      this.state.need_update = false;
      this.state.need_parsing = true;
    }
  }


  handleChange = event => {
    this.setState({[event.target.name]: event.target.value});
    this.state.need_update = true;
    this.state.need_parsing = true;
  };

  handleTextChange = name => event => {
    this.setState({
      [name]: event.target.value,
    });
  };

  parseFileStructure(df, preproc, tool, seq_type, seq_name, postproc) {
    //console.log(this.props.mapping_files);
    if (Object.keys(this.props.mapping_files).length === 0 && this.props.mapping_files.constructor === Object
    )
      return;
    let mapped_node = this.props.mapping_files['FHM'][0]['mapped'];

    this.state.preprocs = [];
    this.state.tools = [];
    this.state.seq_types = [];
    this.state.seq_sets = [];
    this.state.postprocs = [];
    this.state.files = [];

    for (let key in mapped_node) {
      if (mapped_node.hasOwnProperty(key)) {
        this.state.preprocs.push(Object.keys(mapped_node[key])[0]);
        let preproc_node = mapped_node[key];

        //console.log(mapped_node[key]);

        for (let key in preproc_node) {
          if (preproc_node.hasOwnProperty(key)) {
            for (let i = 0; i < preproc_node[key].length; i++) {
              tool = Object.keys(preproc_node[key][i])[0];
              if (this.state.tools.indexOf(tool) === -1) {
                this.state.tools.push(tool);
              }
              //console.log(preproc_node[key][i]);

              let tool_node = preproc_node[key][i];
              for (let key in tool_node) {
                if (tool_node.hasOwnProperty(key)) {
                  for (let i = 0; i < tool_node[key].length; i++) {
                    let type = Object.keys(tool_node[key][i])[0];
                    if (this.state.seq_types.indexOf(type) === -1) {
                      this.state.seq_types.push(type);
                    }
                    //console.log(tool_node[key][i]);

                    let seq_type_node = tool_node[key][i];
                    for (let key in seq_type_node) {
                      if (seq_type_node.hasOwnProperty(key)) {
                        for (let i = 0; i < seq_type_node[key].length; i++) {
                          let type = Object.keys(seq_type_node[key][i])[0];
                          if (this.state.seq_sets.indexOf(type) === -1) {
                            this.state.seq_sets.push(type);
                          }
                          //console.log(seq_type_node[key][i]);

                          let seq_set_node = seq_type_node[key][i];
                          for (let key in seq_set_node) {
                            if (seq_set_node.hasOwnProperty(key)) {
                              for (let i = 0; i < seq_set_node[key].length; i++) {
                                let seq_set = Object.keys(seq_set_node[key][i])[0];
                                if (this.state.postprocs.indexOf(seq_set) === -1) {
                                  this.state.postprocs.push(seq_set);
                                }
                                //console.log(seq_set_node[key][i]);
                                let postproc_node = seq_set_node[key][i];
                                for (let key in postproc_node) {
                                  if (postproc_node.hasOwnProperty(key)) {
                                    for (let i = 0; i < postproc_node[key].length; i++) {
                                      let file = postproc_node[key][i];
                                      if (this.state.files.indexOf(file) === -1) {
                                        this.state.files.push(
                                          {
                                            key: this.state.files.length,
                                            label: file,
                                            selected: false
                                          });
                                      }
                                      //console.log(postproc_node[key][i]);
                                    }
                                  }
                                }

                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }

    this.state.loaded = true;
    this.state.need_parsing = false
  }

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
    let this_files = this.state.files;
    console.log(this_files);
    this_files[data.key].selected = !data.selected;
    console.log(this_files);
    this.setState({['files']: this_files});
  };

  drawHeatmap = data => () => {
    console.log('draw button clicked');
    let selected_samples = [];
    for (var i = 0; i < this.state.files.length; i++) {
      if (this.state.files[i].selected === true) {
        selected_samples.push(this.state.files[i].label)
      }
    }
    console.log(selected_samples);
    this.props.fetchMappingForHeatmap(this.state.df, this.state.preproc, this.state.tool, this.state.type,
      this.state.seq_set_name, this.state.postproc, selected_samples, this.state.filter_query);
  };

  selectAll = data => () => {
    let this_files = this.state.files
    for (var i = 0; i < this_files.length; i++) {
      this_files[i].selected = true;
    }
    this.setState({['files']: this_files});
  };

  clearParams = data => () => {
    this.setState({['type']: '*'});
    this.setState({['seq_set_name']: '*'});
    this.setState({['df']: '*'});
    this.setState({['preproc']: '*'});
    this.setState({['tool']: '*'});
    this.setState({['postproc']: '*'});
    this.setState({['need_update']: true});
    this.setState({['need_parsing']: true});
  };


  render() {
    const {classes} = this.props;

    console.log('rendering');
    console.log(this.state.files);
    console.log(this.state.min_width);

    this.state.dfs = [];
    for (let key in this.props.mapping_files) {
      if (this.props.mapping_files.hasOwnProperty(key)) {
        this.state.dfs.push(key);
      }
    }

    if (this.state.need_parsing === true) {
      this.parseFileStructure(this.state.df, this.state.preproc, this.state.tool, this.state.type,
        this.state.seq_set_name, this.state.postproc);
      // if(this.state.dfs.length === 1)
      //   this.setState({['df']: this.state.dfs[0]});
      // if(this.state.postprocs.length === 1)
      //   this.setState({['postproc']: this.state.postprocs[0]});
      // if(this.state.preprocs.length === 1)
      //   this.setState({['preproc']: this.state.preprocs[0]});
      // if(this.state.tools.length === 1)
      //   this.setState({['tool']: this.state.tools[0]});
    }

    let dataToPlot = [];

    if (this.props.mapping_heatmap !== undefined) {
      dataToPlot = [
        {
          z: this.props.mapping_heatmap.data,
          x: this.props.mapping_heatmap.columns,
          y: this.props.mapping_heatmap.index,
          type: 'heatmap'
        }
      ];
    }

    if (this.state.loaded === true) {
      return (
        <div>
          <Typography variant="display1">
            Mapping Explorer
          </Typography>
          <div>
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
                <MenuItem value="*">
                  <em>All</em>
                </MenuItem>

                {this.state.seq_types.map(seq_type => (
                  <MenuItem value={seq_type.toString()}>{seq_type}</MenuItem>
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
                  <MenuItem value={seq_set.toString()}>{seq_set} </MenuItem>
                ))}
              </Select>
            </FormControl>
          </div>

          <div>
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
              {this.state.files.map(data => (
                <Chip
                  key={data.key}
                  label={data.label}
                  onClick={this.clickChip(data)}
                  onDelete={this.handleDelete(data)}
                  className={data.selected ? classes.chip_active : classes.chip}
                />
              ))}
            </Paper>
          </div>

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
          <Plot
            useResizeHandler={true}
            data={dataToPlot}
            style={{width: '100%', minHeight: '1000px', marginTop: '12pt'}}
            layout={{autosize: true, title: 'Mapping Heatmap'}}
          />
        </div>
      )
    }
    else {
      return (
        <LinearProgress color="secondary"/>
      )
    }
  }
}

const mapStateToProps = state => ({
  seq_sets: state.seq_sets.seq_sets,
  mapping_files: state.mapping.file_structure,
  mapping_heatmap: state.mapping.heatmap_data
});

Mapping.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchSeqSets: PropTypes.func.isRequired,
  fetchMappingForRef: PropTypes.func.isRequired,
  fetchMappingForHeatmap: PropTypes.func.isRequired,
};

export default withRouter(connect(mapStateToProps, {
  fetchSeqSets,
  fetchMappingForRef,
  fetchMappingForHeatmap
})(withStyles(styles)(Mapping)))
