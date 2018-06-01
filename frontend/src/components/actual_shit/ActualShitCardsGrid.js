import React from 'react';
import PropTypes from 'prop-types';
import {Link} from 'react-router-dom';
import {connect} from 'react-redux';

import {withStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Radio, {RadioGroup} from '@material-ui/core/Radio';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';


import ActualShitCard from "./ActualShitCard";

const styles = theme => ({
  root: {
    flexGrow: 1,
  },
  button: {
    margin: 18,
    marginTop: 32
  },
  paper: {
    height: 140,
    width: 100,
  },
  control: {
    padding: 24,
  },
});

class ActualShitCardsGrid extends React.Component {


  render() {

    function isEmpty(obj) {
      for (var key in obj) {
        if (obj.hasOwnProperty(key))
          return false;
      }
      return true;
    }

    const {classes} = this.props;
    if (!isEmpty(this.props.data)) {
      console.log(this.props.data);
      return (
      <div>
        <Typography variant="display2" gutterBottom>
          {'Samples of this subject'}
        </Typography>

        <Grid container className={classes.root} spacing={16}>
          <Grid container className={classes.demo} spacing={24}>
            {this.props.data.shit_samples.map(shit_sample => (
              <Grid key={shit_sample.id} item>
                <ActualShitCard data={shit_sample}/>
              </Grid>
            ))}
          </Grid>
        </Grid>
      </div>

    );
    }
    else{
      return (
        <div>
          <Typography variant="display2" gutterBottom>
          {'Loading'}
        </Typography>
        </div>
      )
    }




  }
}

ActualShitCardsGrid.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(ActualShitCardsGrid);