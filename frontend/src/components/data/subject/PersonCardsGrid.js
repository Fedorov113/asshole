import React from 'react';
import PropTypes from 'prop-types';
import {Link} from 'react-router-dom';
import {connect} from 'react-redux';

import {withStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Radio, {RadioGroup} from '@material-ui/core/Radio';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

import {fetchPersons} from "../../../redux/actions/personActions";
import PersonCard from "./PersonCard";

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

class PersonCardsGrid extends React.Component {

  componentDidMount(){
    this.props.fetchPersons();
  }

  render() {
    const {classes} = this.props;
    return (
      <div>
        <Typography variant="display2" gutterBottom>
          {'Subjects in study'}
        </Typography>

        <Grid container className={classes.root} spacing={16}>
          <Grid container className={classes.demo} spacing={24}>
            {this.props.persons.map(person => (
              <Grid key={person.pk} item>
                <PersonCard data={person}/>
              </Grid>
            ))}
          </Grid>
        </Grid>

        <Button variant="raised" color="primary" className={classes.button}>
          Add new
        </Button>

      </div>

    );
  }
}

const mapStateToProps = state => ({
  persons: state.persons.persons
});

PersonCardsGrid.propTypes = {
  classes: PropTypes.object.isRequired,
  fetchPersons: PropTypes.func.isRequired,
  persons: PropTypes.array.isRequired
};

export default connect(mapStateToProps, {fetchPersons})(withStyles(styles)(PersonCardsGrid));