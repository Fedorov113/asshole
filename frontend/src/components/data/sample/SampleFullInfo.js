import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';

import Typography from '@material-ui/core/Typography';
import {withStyles} from '@material-ui/core/styles';

class SampleFullInfo extends React.Component {

  render() {
    return (
      <div>
        <Typography color="textSecondary">
          Full sample info
        </Typography>
      </div>
    )
  }
}

export default withRouter(SampleFullInfo)