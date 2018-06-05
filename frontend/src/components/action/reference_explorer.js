import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';

import Typography from '@material-ui/core/Typography';
import {withStyles} from '@material-ui/core/styles';

import {fetchSeqSets} from "../../redux/actions/seqSetsActions";
import {fetchFmt} from "../../redux/actions/fmtActions";
import {fetchSubject} from "../../redux/actions/personActions";

import ReferencePanel from './ReferencePanel'

class ReferenceExplorer extends React.Component {

  componentDidMount() {
    this.props.fetchSeqSets();
  }

  render() {
    let arrayLength = this.props.seq_sets.length;
    for (var i = 0; i < arrayLength; i++) {
      console.log(this.props.seq_sets[i]);
      //Do something
    }
    return (
      <div>
        <Typography variant="display1" >
          Reference Explorer
        </Typography>

        {/*{type: [references]}*/}
        <div>
          {this.props.seq_sets.map(seq_set => (
              <ReferencePanel data={seq_set}/>
            ))}
        </div>
      </div>
    )
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