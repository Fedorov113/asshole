import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import Typography from '@material-ui/core/Typography';
import {withStyles} from '@material-ui/core/styles';
import {withRouter} from 'react-router-dom';
import { Link } from 'react-router-dom';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import {fetchReads} from "../../../redux/actions/sampleActions";

import ReadsParser from '../sample/ReadsParser'

const DarkTableCell = withStyles(theme => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 14,
  },
}))(TableCell);

const styles = theme => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    height: 140,
    width: 100,
  },
  control: {
    padding: 24,
  },
  content: {
    marginLeft: 18,
  },
  table: {
    minWidth: 700,
  },
});


class DatasetFullInfo extends React.Component {

  state = {
    prepr_of_fs: []
  };


  constructor() {
    super();
    this.state = {};
  }

  componentDidMount() {
    const df = this.props.match.params.df;
    const preproc = '*';

    this.props.fetchReads(df, preproc)
  }

  componentDidUpdate(prevProps, prevState) {

    if (this.props.reads !== 'None' && this.props.reads !== prevProps.reads) {
      let representation_of_df_reads = new ReadsParser(this.props.reads);
      let preprocs = representation_of_df_reads.preprocs;

      console.log(representation_of_df_reads.reads_for_preproc(preprocs[0]))
    }
  }

  clickedCell = () => {
    console.log('clicked')
  };
  render() {
    const {classes} = this.props;

    const df = this.props.match.params.df;

    let samples = [];
    let preproc = 'None';
    if (this.props.reads !== 'None') {
      let representation_of_df_reads = new ReadsParser(this.props.reads);
      let preprocs = representation_of_df_reads.preprocs;
      preproc = preprocs[0];
      samples = representation_of_df_reads.reads_for_preproc(preprocs[0]);
    }

    return (
      <div>
        <Typography variant="display1" gutterBottom>
          Study <b>{df}</b>
        </Typography>

        <div  className={classes.content}>
        <Typography variant="headline" gutterBottom>
          Samples
        </Typography>
        <Paper>
          <Table className={classes.table}>
            <TableHead>
              <TableRow>
                <DarkTableCell>Sample Name</DarkTableCell>
                <DarkTableCell>R1 size</DarkTableCell>
                <DarkTableCell>R2 size</DarkTableCell>
                <DarkTableCell >Base Pairs Total</DarkTableCell>
                <DarkTableCell >Reads Total</DarkTableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {samples.map(n => {
                return (
                  <TableRow key={n.sample_name}>
                    {/*<TableCell component="a" scope="row"*/}
                               {/*href={"/app/dataset/" + df + "/preproc/" + preproc + "/sample/" + n.sample_name}>*/}
                      {/*{n.sample_name}*/}
                    {/*</TableCell>*/}
                    <TableCell component={Link} to={"/app/dataset/" + df + "/preproc/" + preproc + "/sample/" + n.sample_name}>
                      {n.sample_name}
                    </TableCell>
                    <TableCell>{n.r1_size}</TableCell>
                    <TableCell>{n.r2_size}</TableCell>
                    <TableCell>{n.bp}</TableCell>
                    <TableCell>{n.reads}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </Paper>
        </div>
      </div>
    )
  }
}


const mapStateToProps = state => ({
  reads: state.sample.reads
});

DatasetFullInfo.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withRouter(connect(mapStateToProps, {fetchReads})(withStyles(styles)(DatasetFullInfo)))