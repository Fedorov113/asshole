import React from 'react';
import Plot from 'react-plotly.js';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Typography from '@material-ui/core/Typography';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import {connect} from 'react-redux';



import {fetchMp2Result} from "../../redux/actions/mp2Actions";

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing.unit * 2,
  },
});

class Mp2Plot extends React.Component {

  state = {
    level: 'p',
  };

  handleChange = event => {
    this.setState({ [event.target.name]: event.target.value });
    if(event.target.name === 'level'){
      this.props.fetchMp2Result(event.target.value);
    }
  };

  componentDidMount() {
    this.props.fetchMp2Result('f');
  }

  render() {


    var dataToPlot = [];

    // Prepare data for plotly
    if (this.props.mp2 !== undefined) {
      const samples = this.props.mp2.sample;
      var mp2 = this.props.mp2;

      //construct bars
      Object.keys(this.props.mp2).forEach(function (key) {
        if (key !== 'sample') {
          var data = {
            x: samples,
            y: mp2[key],
            type: 'bar',
            name: key.split('__').slice(-1)[0] // Getting only last part of string
          };
          dataToPlot.push(data)
        }
      });
    }

    const { classes } = this.props;

    return (
      <div style={{height: '100%'}}>
        <Typography variant="display2" gutterBottom>
          {'Taxonomic composition stacked bar chart'}
        </Typography>
        <form className={classes.root} autoComplete="off">
          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="level">Level</InputLabel>
            <Select
              value={this.state.level}
              onChange={this.handleChange}
              inputProps={{
                name: 'level',
                id: 'level-simple',
              }}
            >
              <MenuItem value={'f'}>Family</MenuItem>
              <MenuItem value={'p'}>Phylum</MenuItem>
              <MenuItem value={'g'}>Genus</MenuItem>
            </Select>
          </FormControl>
        </form>
        <Plot
          useResizeHandler={true}
          data={dataToPlot}
          style={{width: '100%', height: '70%'}}
          layout={{autosize: true, title: 'Taxonomic composition', barmode: 'stack'}}
        />
      </div>
    );
  }
}

const mapStateToProps = state => ({
  mp2: state.mp2.mp2
});

Mp2Plot.propTypes = {
  fetchMp2Result: PropTypes.func.isRequired,
  mp2: PropTypes.object.isRequired
};


export default connect(mapStateToProps, {fetchMp2Result}) (withStyles(styles)(Mp2Plot));