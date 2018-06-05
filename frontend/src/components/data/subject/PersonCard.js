import React from 'react'
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Button from '@material-ui/core/Button';
import ButtonBase from "@material-ui/core/ButtonBase";
import Typography from '@material-ui/core/Typography';
import {withRouter} from 'react-router-dom';

const styles = {
  card: {
    minWidth: 325,

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
};

class PersonCard extends React.Component {

  render() {
    const {classes} = this.props;
    return (
      <div>
        <Card className={classes.card}>
          <ButtonBase className={this.props.classes.cardAction}
                      onClick={event => {
                        var loc = '1/person/' + this.props.data.pk;
                        this.props.history.push(loc);
                      }}>
            <CardContent>
              <Typography variant="headline" component="h2">
                <b>{this.props.data.subject_nickname}</b>
              </Typography>
              <Typography color="textSecondary">
                Пол:  <i>{this.props.data.gender}</i>
              </Typography>
              <Typography color="textSecondary">
                Диагноз: <i>{this.props.data.diagnosis_name_in_study}</i>
              </Typography>

            </CardContent>

          </ButtonBase>
        </Card>
      </div>
    )
  }
}

PersonCard.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withRouter(withStyles(styles)(PersonCard));