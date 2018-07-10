import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';

import Typography from '@material-ui/core/Typography';
import {withStyles} from '@material-ui/core/styles';
import {fetchFastqc} from "../../../redux/actions/sampleActions";

import ReactHtmlParser, {processNodes, convertNodeToElement, htmlparser2} from 'react-html-parser';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    marginTop: theme.spacing.unit * 4,
  },
  fastqc_div: {
    display: 'flex',
    flexWrap: 'wrap',
    width: '200px'
  },
});

class SampleFullInfo extends React.Component {

  componentDidMount() {
    console.log(this.props.match.params);
  }

  // We need dataset and sample name to fetch info
  render() {
    const {classes} = this.props;
    console.log(this.props.match.params);

    let df = this.props.match.params.df;
    let preproc = this.props.match.params.preproc;
    let sample = this.props.match.params.sample;
    let fastqc_r1 = "/api/fs/fastqc/"+df+"/"+preproc+"/"+sample+"/R1/";
    let fastqc_r2 = "/api/fs/fastqc/"+df+"/"+preproc+"/"+sample+"/R2/";
    let krona_centr = "/api/fs/krona/"+df+"/"+preproc+"/"+sample+"/centr/";
    return (
      <div>
        <Typography variant="headline" gutterBottom>
          Full sample info
        </Typography>
        <Typography>
          Dataset: <b>{df}</b>
        </Typography>
        <Typography>
          Preprocessing: <b>{preproc}</b>
        </Typography>
        <Typography>
          Sample name: <b>{sample}</b>
        </Typography>
        <Typography>
          Reads in sample: <b>none</b>
        </Typography>
        <Typography>
          Base pairs in sample: <b>none</b>
        </Typography>

        <Typography component='a' href={fastqc_r1} target="_blank">
          FastQC for strand 1
        </Typography>
        <Typography  component='a' href={fastqc_r2} target="_blank">
          FastQC for strand 2
        </Typography>
        <Typography  component='a' href={krona_centr} target="_blank">
          Krona taxonomic Centrifuge visualization
        </Typography>
      </div>

    )
  }
}

const mapStateToProps = state => ({
  fastqc: state.sample.fastqc
});

export default withRouter(connect(mapStateToProps, {fetchFastqc})(withStyles(styles)(SampleFullInfo)))