import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';
import {withStyles} from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

import Plot from 'react-plotly.js';
import {fetchDatasetGeneralTaxaComposition} from "../../../redux/actions/datasetActions";

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    marginTop: theme.spacing.unit * 4,
  },
  plot: {
    display: 'flex',
    flexWrap: 'wrap',
  },
});

class DatasetReadsContentViz extends React.Component {

  state = {};

  componentDidMount() {
    let df = this.props.df;
    let preproc = this.props.preproc;
    let tool = 'centr';
    this.props.fetchDatasetGeneralTaxaComposition(df, preproc, tool)

  }

  render() {
    let data_to_plot = [];
    console.log(this.props.general_taxa_composition);

    const taxa = this.props.general_taxa_composition;
    let samples = [];
    let bacteria = [];
    let vir = [];
    let archaea = [];
    let homo = [];
    let uncl = [];
    let other = [];

    if (taxa.length > 0) {
      for (let i = 0; i < taxa.length; i++) {
        samples.push(taxa[i].sample);
        bacteria.push(taxa[i].bacteria);
        vir.push(taxa[i].vir);
        archaea.push(taxa[i].archaea);
        homo.push(taxa[i].homo);
        uncl.push(taxa[i].uncl);
        other.push(taxa[i].other);
      }

      data_to_plot.push({
        y: samples,
        x: bacteria,
        name: 'bacteria',
        type: 'bar',
        orientation: 'h',
      });
      data_to_plot.push({
        y: samples,
        x: vir,
        name: 'virus',
        type: 'bar',
        orientation: 'h',
      });
      data_to_plot.push({
        y: samples,
        x: archaea,
        name: 'archaea',
        type: 'bar',
        orientation: 'h',
      });
      data_to_plot.push({
        y: samples,
        x: homo,
        name: 'homo',
        type: 'bar',
        orientation: 'h',
      });
      data_to_plot.push({
        y: samples,
        x: uncl,
        name: 'unclassified',
        type: 'bar',
        orientation: 'h',
      });
      data_to_plot.push({
        y: samples,
        x: other,
        name: 'other',
        type: 'bar',
        orientation: 'h',
      });
    }

    let layout = {
      autosize: true,
      barmode: 'stack',
      title: 'Sample reads composition',
    };


    return (
      <div>
        {data_to_plot.length !== 0 ?
          <Paper>
            <Plot
              useResizeHandler={true}
              data={data_to_plot}
              style={{width: '100%', minHeight: '1000px', marginTop: '12pt'}}
              layout={layout}
            />
          </Paper>
          : <Typography style={{marginTop: '12pt'}}> WAIT </Typography>
        }
      </div>
    )
  }

}

const mapStateToProps = state => ({
  general_taxa_composition: state.datasets.general_taxa_composition
});


DatasetReadsContentViz.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchDatasetGeneralTaxaComposition: PropTypes.func.isRequired,
};

export default withRouter(connect(mapStateToProps, {fetchDatasetGeneralTaxaComposition})(withStyles(styles)(DatasetReadsContentViz)))