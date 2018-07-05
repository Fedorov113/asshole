import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';
import {withStyles} from '@material-ui/core/styles';

import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

import Plot from 'react-plotly.js';

import {fetchMp2Boxplot} from '../../redux/actions/mp2Actions'

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

class Mp2BoxplotViz extends React.Component {

  state = {
    need_parsing: true,
    data_to_plot: []
  };

  componentDidUpdate(prevProps, prevState) {
    console.log('Mp2BoxViz did update');

    if (JSON.stringify(prevProps.dfs_to_plot) !== JSON.stringify(this.props.dfs_to_plot)) {
      this.setState({['data_to_plot']: []});
      for (let i = 0; i < this.props.dfs_to_plot.length; i++) {
        console.log('sending fetch ' + this.props.dfs_to_plot[i].df + ' ' + this.props.dfs_to_plot[i].preproc);
        this.props.fetchMp2Boxplot(this.props.dfs_to_plot[i].df, this.props.dfs_to_plot[i].preproc)
      }
    }

    if (this.props.mp2_box !== 'None' && JSON.stringify(prevProps.mp2_box) !== JSON.stringify(this.props.mp2_box)) {
      let data_to_plot = {df: this.props.mp2_box['df'], preproc: this.props.mp2_box['preproc'], data: []};
      console.log('PARSING');

      // Check every taxa node
      for (let key in this.props.mp2_box['mp2box']) {
        if (this.props.mp2_box['mp2box'].hasOwnProperty(key)) {
          const taxa_node = this.props.mp2_box['mp2box'][key];
          let data_node = {name: key, data: []};

          // Check every sample
          for (let key in taxa_node) {
            if (taxa_node.hasOwnProperty(key)) {
              if (taxa_node[key] !== 'none') {
                data_node.data.push(taxa_node[key])
              }
            }
          }
          data_to_plot.data.push(data_node)
        }
      }

      console.log(data_to_plot);
      let dd = this.state.data_to_plot;
      dd.push(data_to_plot);
      this.setState({['need_parsing']: false});
      this.setState({['data_to_plot']: dd});
    }
  }

  render() {
    //WE ALWAYS DO THIS
    const {classes} = this.props;
    let data_to_plot = [];
    let layout = {
      autosize: true,
      title: 'Metaphlan2 Box Plot',
      boxmode: "group",
      showlegend: false
    };
    //--------------------


    // Here I assume that this component works with standart [{df: 'df_name', preproc: 'preproc_name'}]
    let dfs_to_plot = this.props.dfs_to_plot;

    //Fetched?
    console.log(this.state.data_to_plot);
    for (let j = 0; j < this.state.data_to_plot.length; j++) {
      let data_to_plot_node = this.state.data_to_plot[j];
      for (let i = 0; i < data_to_plot_node.data.length; i++) {
        if(data_to_plot_node.data[i].data.length > 10){
          let name = data_to_plot_node.data[i].name.split('|');
          name = name[name.length - 1];
          data_to_plot.push({
            y: data_to_plot_node.data[i].data,
            x: data_to_plot_node.data[i].data.map(() => name),
            name: data_to_plot_node['df'],
            type: 'box',
          })}
      }
    }

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
          : <Typography style={{marginTop: '12pt'}}> Select at least one dataset </Typography>
        }
      </div>

    );
  }
}

const mapStateToProps = state => ({
  mp2_box: state.mp2.mp2_box
});


Mp2BoxplotViz.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchMp2Boxplot: PropTypes.func.isRequired,
};

export default withRouter(connect(mapStateToProps, {fetchMp2Boxplot})(withStyles(styles)(Mp2BoxplotViz)))