import React from 'react';
import Plot from 'react-plotly.js';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import {connect} from 'react-redux';

import Typography from '@material-ui/core/Typography';

import {fetchMp2ScatterResult} from "../../redux/actions/mp2Actions";

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

class Mp2ScatterPlot extends React.Component {

  componentDidMount() {
    this.props.fetchMp2ScatterResult();
  }

  render() {

    let dataToPlot = [];

    // Prepare data for plotly
    if (this.props.mp2_scatter !== undefined) {
      const samples = this.props.mp2_scatter;
      let mp2 = this.props.mp2_scatter;
      console.log(this.props.mp2_scatter);
      console.log(mp2);

      //construct bars
      let i = 0;
      Object.keys(mp2).forEach(function (key) {
        if (key !== 'sample') {
          console.log(mp2[key]);
          let data = {
            x: [0, 1, 2, 3],
            y: mp2[key],
            type: 'scatter',
            mode: 'lines+points',
            marker: {color: 'red'},
            name: key.split('__').slice(-1)[0] // Getting only last part of string
          };
          dataToPlot.push(data)
        }
      });


    }

    const {classes} = this.props;

    return (
      <div style={{height: '100%'}}>
        <Typography variant="display2" gutterBottom>
          {'Изменение таксономического профиля'}
        </Typography>
        <Plot
          useResizeHandler={true}
          data={dataToPlot}
          style={{width: '100%', height: '70%'}}
          layout={{autosize: true, title: 'Taxonomic composition'}}
        />
      </div>
    );
  }
}

const mapStateToProps = state => ({
  mp2_scatter: state.mp2.mp2_scatter
});

Mp2ScatterPlot.propTypes = {
  fetchMp2ScatterResult: PropTypes.func.isRequired,
  mp2_scatter: PropTypes.object.isRequired
};


export default connect(mapStateToProps, {fetchMp2ScatterResult})(withStyles(styles)(Mp2ScatterPlot));

