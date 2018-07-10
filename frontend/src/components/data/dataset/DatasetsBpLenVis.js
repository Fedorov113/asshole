import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';
import {withStyles} from '@material-ui/core/styles';

import {fetchReads} from "../../../redux/actions/sampleActions";

import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

import Plot from 'react-plotly.js';

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

class DatasetsBpLenVis extends React.Component {

  state = {
    samples_w_reads: [],
    data: [],
    need_parsing: true,
    need_update: true
  };

  componentDidUpdate(prevProps, prevState) {

    console.log('DatasetsBpLenVis did update');
    console.log(this.props.data_to_plot);
    console.log(this.props.reads);

    if (JSON.stringify(prevProps.data_to_plot) !== JSON.stringify(this.props.data_to_plot)) {
      this.setState({['data']: []});
      for (let i = 0; i < this.props.data_to_plot.length; i++) {
        console.log('sending fetch ' + this.props.data_to_plot[i].df + ' ' + this.props.data_to_plot[i].preproc);
        this.props.fetchReads(this.props.data_to_plot[i].df, this.props.data_to_plot[i].preproc)
      }
    }

    if (this.props.reads !== 'None' && this.props.reads !== prevProps.reads) {
      let data = this.state.data;
      let need_to_parse = true;
      if (this.state.data.length > 0) {
        for (let j = 0; j < this.state.data.length; j++) {
          if (this.props.reads.children[0].node_name === this.state.data[j].df
            && this.props.reads.children[0].children[0].children[0].node_name === this.state.data[j].preproc) {
            need_to_parse = false
          }
        }
      }
      if (need_to_parse) {
        let sample_data = this.parseReadsFolder(this.props.reads.children[0].children[0].children[0]);
        data.push({
          df: this.props.reads.children[0].node_name,
          preproc: this.props.reads.children[0].children[0].children[0].node_name,
          data: sample_data
        });
        this.setState({['data']: data});
      }
    }
  }

  parseSampleFolder = (fsNode) => {
    let sample = {};
    sample.sample_name = fsNode['node_name'];
    sample.files = [];
    let r1_size = '';
    let r2_size = '';
    let bp = 0;
    let reads = 0;
    for (let i = 0; i < fsNode['children'].length; i++) {
      let file = this.parseFSNode(fsNode['children'][i]);
      if (file['node_name'].includes('_R1')) {
        r1_size = file['size']
      }
      else if (file['node_name'].includes('_R2')) {
        r2_size = file['size']
      }
      bp += parseInt(file['bp']);
      reads += parseInt(file['reads']);
    }
    sample.r1_size = r1_size;
    sample.r2_size = r2_size;
    sample.bp = bp;
    sample.reads = reads;
    return (sample);
  };

  parseReadsFolder = (fsNode) => {
    let reads_ar = [];
    if (fsNode.hasOwnProperty('children')) {
      if (fsNode['children'].length > 0) {
        for (let i = 0; i < fsNode['children'].length; i++) {
          reads_ar.push(this.parseSampleFolder(fsNode['children'][i]))
        }
      }
    }
    return reads_ar
  };


  parseFSNode = (fsNode) => {
    if (fsNode['type'] === 'dir') {
      if (fsNode.hasOwnProperty('children')) {
        if (fsNode['children'].length > 0) {
          if (fsNode['level'] === 3) {
            let sample_data = this.parseReadsFolder(fsNode);
            let data = this.state.data;
            data.push(sample_data);
            this.setState({['data']: data});
            return sample_data;
          }
          else {
            for (let i = 0; i < fsNode['children'].length; i++) {
              this.parseFSNode(fsNode['children'][i])
            }
          }
        }
        return fsNode;
      }
    }
    else if (fsNode['type'] === 'file') {
      return fsNode;
    }
  };

  render() {
    const {classes} = this.props;
    const data_to_plot = this.props.data_to_plot;
    console.log(this.state.data);

    let data = [];
    let len = 0;
    let mean = 0;
    if (this.state.data.length > 0) {
      let total_vals = [];
      for (let i = 0; i < this.state.data.length; i++) {
        let names = [];
        let vals = [];
        const presort_node = this.state.data[i].data;
        let node = presort_node.sort((a, b) => {
          return b.bp - a.bp;
        });

        for (let j = 0; j < node.length; j++) {
          names.push(node[j].sample_name);
          vals.push(node[j].bp);
          total_vals.push(node[j].bp);
          mean += node[j].bp;
        }
        let tmp_data = {
          x: vals,
          y: names,
          type: 'bar',
          orientation: 'h',
          name: this.state.data[i].df + ' ' + this.state.data[i].preproc
        };
        data.push(tmp_data)
      }
      len = total_vals.length;
      mean = mean / len;
    }
    mean = Number(mean);
    mean = mean.toFixed(0);

    let layout = {
      autosize: true,
      title: 'Base Pairs in Samples',
      shapes: [
        {
          type: 'line',
          x0: mean,
          y0: 0,
          x1: mean,
          y1: 10,
          line: {
            color: 'rgb(200, 33, 55)',
            width: 3,
          },
        }]
    };
    return (
      <div>
        {data_to_plot.length !== 0 ?
          <Paper>
            <Plot
              useResizeHandler={true}
              data={data}
              style={{width: '100%', minHeight: '1000px', marginTop: '12pt'}}
              layout={layout}
            />
          </Paper>
          : <Typography style={{marginTop:'12pt'}}> Select at least one dataset </Typography>
        }
      </div>

    )
  }
}

const mapStateToProps = state => ({
  reads: state.sample.reads
});


DatasetsBpLenVis.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchReads: PropTypes.func.isRequired,
};

export default withRouter(connect(mapStateToProps, {fetchReads})(withStyles(styles)(DatasetsBpLenVis)))