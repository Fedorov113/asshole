import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';

import Typography from '@material-ui/core/Typography';
import {withStyles} from '@material-ui/core/styles';

import {fetchSeqSets} from "../../redux/actions/seqSetsActions";
import {fetchFmt} from "../../redux/actions/fmtActions";
import {fetchSubject} from "../../redux/actions/personActions";

import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import LinearProgress from '@material-ui/core/LinearProgress';

import ReferencePanel from './ReferencePanel'

class ReferenceExplorer extends React.Component {

  state = {
    type: ''
  };

  componentDidMount() {
    this.props.fetchSeqSets();
  }

  render() {
    let arrayLength = this.props.seq_sets.length;
    for (let i = 0; i < arrayLength; i++) {
      console.log(this.props.seq_sets[i]);
      //Do something
    }
    if (arrayLength > 0) {
      return (
        <div>
          <Typography variant="display1">
            Reference Explorer
          </Typography>

          <Select value={this.state.type}>
            <MenuItem value="None">
              <em>None</em>
            </MenuItem>
            {this.props.seq_sets.map(seq_set => (
              <MenuItem value={'type'+seq_set.type.toString()}>{seq_set.type} </MenuItem>
            ))}

          </Select>

          {/*{type: [references]}*/}
          <div>
            {this.props.seq_sets.map(seq_set => (
              <ReferencePanel data={seq_set}/>
            ))}
          </div>
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
  seq_sets: state.seq_sets.seq_sets
});

ReferenceExplorer.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchSeqSets: PropTypes.func.isRequired,
};

export default withRouter(connect(mapStateToProps, {fetchSeqSets})(ReferenceExplorer))