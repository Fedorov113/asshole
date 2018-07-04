import React from 'react'
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {withRouter} from 'react-router-dom';

import Typography from '@material-ui/core/Typography';
import {withStyles} from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';

import Plot from 'react-plotly.js';

import ActualShitCardsGrid from '../actual_shit/ActualShitCardsGrid'
import Mp2ScatterPlot from '../../result/mp2_scatter'
import {fetchSubject} from "../../../redux/actions/personActions";
import {fetchFmt} from "../../../redux/actions/fmtActions";

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
  button: {
    margin: 18,
  },
  content: {
    marginLeft: 18,
  },
  card: {
    width: 400,

  },
  cardAction: {
    display: 'block',
    textAlign: 'initial',
    minWidth: 325,
  },
  title: {
    marginBottom: 16,
    fontSize: 14,
  },
  pos: {
    margin: 12,
  },
});


class PersonFullInfo extends React.Component {
  constructor() {
    super();
  }

  componentDidMount(){
    this.props.fetchSubject(this.props.match.params.person_id);
    this.props.fetchFmt(this.props.match.params.person_id);
  }

  render() {
    const {classes} = this.props;
    console.log(this.props.match.params.person_id);
    return <div>
      <Typography variant="display3" gutterBottom>
        Subject <b>{this.props.subject.subject_nickname}</b>
      </Typography>
      <Typography>
        Пол: <b>{this.props.subject.gender}</b>
      </Typography>
      <Typography>
        Диагноз: <b>{this.props.subject.diagnosis_name_in_study}</b>
      </Typography>
      <Typography>
        Возвраст: <b>{this.props.subject.age}</b>
      </Typography>


      <Grid container>
        <Grid item xs={12} sm={6}>
          <Plot
          data={[
            {
              x: [0, 1, 7],
              y: [6, 6, 1],
              type: 'scatter',
              mode: 'lines+points',
              marker: {color: 'red'},
            }
          ]}
          layout={{width: 400, height: 350, title: 'Индекс активности заболевания'}}
        />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Card className={classes.card}>
          <CardContent>
            <Typography variant="headline" component="h2">
              Фекалотрансплантация
            </Typography>
            <Typography color="textSecondary">
              Донор: <b>DFM_003</b>
            </Typography>
            <Typography color="textSecondary">
              Донорский образец: <b>DFM_003_F1_S10</b>
            </Typography>
            <Typography color="textSecondary">
              Дата процедуры: <b>10.08.2017</b>
            </Typography>
          </CardContent>
        </Card>
        </Grid>
      </Grid>

      <Mp2ScatterPlot/>

      <div className={classes.content}>
        <ActualShitCardsGrid data={this.props.subject}/>
      </div>
    </div>


  }
}

const mapStateToProps = state => ({
  subject: state.persons.subject,
  fmt: state.fmt.fmt
});

PersonFullInfo.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchSubject: PropTypes.func.isRequired,
  subject: PropTypes.object.isRequired
};


export default withRouter(connect(mapStateToProps, {fetchFmt, fetchSubject})(withStyles(styles)(PersonFullInfo)))


