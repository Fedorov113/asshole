import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';


const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
  menu: {
    width: 200,
  },
});

const genders = [
  {
    value: 'M',
    label: 'Male',
  },
  {
    value: 'F',
    label: 'Female',
  }
];

class AddSubjectForm extends React.Component {
  state = {
    name: '',
    date_of_birth: '',
    diagnosis: '',
    additional_health: '',
    selectedDate: new Date(),
    gender: '',
  };
  handleDateChange = (date) => {
    this.setState({selectedDate: date});
  };

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value,
    });
  };

  render() {
    const {classes} = this.props;
    const {selectedDate} = this.state;

    return (

        <div>
          <Typography variant="display2" gutterBottom>
            Adding new subject to {this.state.pk}
          </Typography>
          <form className={classes.container} noValidate autoComplete="off">
            <TextField
              id="subject_name"
              label="Subject full name"
              className={classes.textField}
              value={this.state.name}
              onChange={this.handleChange('name')}
              margin="normal"
            />
            <TextField
              id="diagnosis"
              label="Diagnosis"
              className={classes.textField}
              value={this.state.diagnosis}
              onChange={this.handleChange('diagnosis')}
              margin="normal"
            />
            <TextField
              id="additional-health-info"
              label="Additional health info"
              className={classes.textField}
              value={this.state.additional_health}
              onChange={this.handleChange('additional_health')}
              margin="normal"
            />
            <TextField
              id="select-gender"
              select
              label="Gender"
              className={classes.textField}
              value={this.state.gender}
              onChange={this.handleChange('gender')}
              SelectProps={{
                MenuProps: {
                  className: classes.menu,
                },
              }}
              margin="normal"
            >
              {genders.map(option => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          </form>


        </div>
    )
  }
}

AddSubjectForm.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(AddSubjectForm);