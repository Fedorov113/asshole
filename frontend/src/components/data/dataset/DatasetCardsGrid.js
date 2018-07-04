import React from 'react';
import PropTypes from 'prop-types';
import {Link} from 'react-router-dom';
import {connect} from 'react-redux';

import {withStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Radio, {RadioGroup} from '@material-ui/core/Radio';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

import {fetchDatasets, fetchDatasetList} from "../../../redux/actions/datasetActions";
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

  componentDidMount() {
    this.props.fetchDatasets();
    this.props.fetchDatasetList()
  }

  render() {
    const {classes} = this.props;
    return (
      <div>
        <Typography variant="display2" gutterBottom>
          Datasets in system
        </Typography>

        <Grid container className={classes.root} spacing={16}>
          <Grid container className={classes.demo} spacing={24}>
            {this.props.dataset_list.map(df => (
              <Grid key={df.toString()} item>
                <DfCard df_info={df}/>
              </Grid>
            ))}
          </Grid>
        </Grid>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  datasets: state.datasets.datasets,
  dataset_list: state.datasets.dataset_list,
});

DatasetCardsGrid.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchDatasets: PropTypes.func.isRequired,
  fetchDatasetList: PropTypes.func.isRequired,
  datasets: PropTypes.array.isRequired
};

export default connect(mapStateToProps, {fetchDatasets, fetchDatasetList})(withStyles(styles)(DatasetCardsGrid));