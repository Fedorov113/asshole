import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';

import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import {withStyles} from '@material-ui/core/styles';

import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';



class ReferencePanel extends React.Component {
  render() {
    return (
      <div>
        <Typography variant="headline" color="textSecondary">
          {this.props.data.type}
        </Typography>
        <Divider />

        {this.props.data.seqs.map(seq =>(
          <Card>
            <CardContent>
              <Typography>
                {seq}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }
}

export default withRouter(ReferencePanel)