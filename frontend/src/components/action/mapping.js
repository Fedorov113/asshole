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


import MappingSelector from './MappingSelector'

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
  };

  componentDidMount() {

  }

  render() {
    const {classes} = this.props;

    return (
      <div>

        <Typography variant="display1">
          Mapping Explorer
        </Typography>

        <MappingSelector />

      </div>
    )
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
