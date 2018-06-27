import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';
import {withStyles} from '@material-ui/core/styles';


import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import Plot from 'react-plotly.js';

import {fetchReads} from "../../../redux/actions/sampleActions";

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  table: {
    minWidth: 700,
  },
});

let id = 0;

function createData(name, calories, fat, carbs, protein) {
  id += 1;
  return {id, name, calories, fat, carbs, protein};
}


function createDataForTable(name, r1_size, r2_size, bp, reads) {
  id += 1;
  return {id, name, r1_size, r2_size, bp, reads}
}

class SamplesTableView extends React.Component {

  state = {
    samples_w_reads: [],
    data: []
  };

  parseReads = (fsNode) => {
    let sample = {};
            sample.sample_name = fsNode['node_name'];
            sample.files = [];
            let sample_name = fsNode['node_name'];
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
            this.state.samples_w_reads.push(sample);
            this.state.data.push(createDataForTable(sample_name, r1_size, r2_size, bp, reads))
  };

  parseFSNode = (fsNode) => {
    if (fsNode['type'] === 'dir') {
      if (fsNode.hasOwnProperty('children')) {
        if (fsNode['children'].length > 0) {
          if (fsNode['level'] === 4) {
            this.parseReads(fsNode)
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

  parseFSObject = (fsObject) => {
    this.state.samples_w_reads = [];
    if (Object.keys(fsObject).length === 0 && fsObject.constructor === Object)
      return;
    this.parseFSNode(fsObject);
  };

  componentDidMount() {
    this.props.fetchReads();
  }

  render() {
    const {classes} = this.props;
    this.parseFSObject(this.props.reads);
    console.log(this.state.samples_w_reads);

    var data = [];
    let len = 0;
    let mean = 0;
    if (this.state.data.length > 0) {
      let names = [];
      let vals = [];
      for (let i = 0; i < this.state.data.length; i++) {
        names.push(this.state.data[i].name);
        vals.push(this.state.data[i].bp);
        mean += this.state.data[i].bp;
      }
      data = [
        {
          x: vals,
          y: names,
          type: 'bar',
          orientation: 'h'
        }
      ];
      len = vals.length;
      mean = mean/len;
      console.log(mean);
    }
    return (
      <div>
        <Typography>Samples Table View</Typography>
        <Paper>
          <Table className={classes.table}>
            <TableHead>
              <TableRow>
                <TableCell>Sample Name</TableCell>
                <TableCell>R1 size</TableCell>
                <TableCell>R2 size</TableCell>
                <TableCell numeric>Base Pairs Total</TableCell>
                <TableCell numeric>Reads Total</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {this.state.data.map(n => {
                return (
                  <TableRow key={n.id}>
                    <TableCell component="a" scope="row" href="/app/ref_seq">
                      {n.name}
                    </TableCell>
                    <TableCell>{n.r1_size}</TableCell>
                    <TableCell>{n.r2_size}</TableCell>
                    <TableCell numeric>{n.bp}</TableCell>
                    <TableCell numeric>{n.reads}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </Paper>

        <Plot
          useResizeHandler={true}
          data={data}
          style={{width: '100%', minHeight: '1000px', marginTop: '12pt'}}
          layout={{
            autosize: true, title: 'Mapping Heatmap', 'shapes': [
              {
                'type': 'line',
                'x0': 4711068467,
                'y0': 0,
                'x1': {mean},
                'y1': {len},
                'line': {
                  'color': 'rgb(200, 33, 55)',
                  'width': 3,
                },
              }]
          }}
        />

      </div>
    )
  }
}

const mapStateToProps = state => ({
  reads: state.sample.reads,
});

SamplesTableView.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchReads: PropTypes.func.isRequired
};

export default withRouter(connect(mapStateToProps, {fetchReads})(withStyles(styles)(SamplesTableView)))
