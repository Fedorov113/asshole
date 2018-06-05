import React from 'react';
import PropTypes from 'prop-types';
import {Link} from 'react-router-dom';
import {connect} from 'react-redux';

import {withStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Radio, {RadioGroup} from '@material-ui/core/Radio';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

import {fetchDatasets} from "../../../redux/actions/datasetActions";
import DfCard from "./DatasetCard";

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

class DatasetCardsGrid extends React.Component {

  componentDidMount(){
    this.props.fetchDatasets();
  }

  render() {
    const {classes} = this.props;
    return (
      <div>
        <Typography variant="display2" gutterBottom>
          {'Available Datasets'}
        </Typography>

        <Grid container className={classes.root} spacing={16}>
          <Grid container className={classes.demo} spacing={24}>
            {this.props.datasets.map(df => (
              <Grid key={df.id} item>
                <DfCard data={df}/>
              </Grid>
            ))}
          </Grid>
        </Grid>

        <Button variant="raised" color="primary" className={classes.button}>
          Add new dataset
        </Button>

      </div>

    );
  }
}

const mapStateToProps = state => ({
  datasets: state.datasets.datasets
});

DatasetCardsGrid.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchDatasets: PropTypes.func.isRequired,
  datasets: PropTypes.array.isRequired
};

export default connect(mapStateToProps, {fetchDatasets})(withStyles(styles)(DatasetCardsGrid));