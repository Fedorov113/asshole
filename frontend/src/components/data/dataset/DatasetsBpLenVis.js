import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';
import {withStyles} from '@material-ui/core/styles';

import {fetchReads} from "../../../redux/actions/sampleActions";

import Plot from 'react-plotly.js';

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

class DatasetsBpLenVis extends React.Component {

}

const mapStateToProps = state => ({
  reads: state.sample.reads
});


DatasetsBpLenVis.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchReads: PropTypes.func.isRequired,
};

export default withRouter(connect(mapStateToProps, {fetchReads})(withStyles(styles)(DatasetsBpLenVis)))