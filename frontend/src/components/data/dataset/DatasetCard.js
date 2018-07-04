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

class DfCard extends React.Component {

  cardClicked = () => {
    let loc = 'dataset/' + this.props.df_info;
    this.props.history.push(loc);
  };

  render() {
    const {classes} = this.props;
    return (
      <div>
        <Card className={classes.card}>
          <ButtonBase
            className={this.props.classes.cardAction}
            onClick={this.cardClicked}>
            <CardContent>
              <Typography variant="headline" component="h2">
                {this.props.df_info}
              </Typography>
              <Typography color="textSecondary">
                {/*{this.props.data.df_description}*/}
                No description yet
              </Typography>
            </CardContent>
          </ButtonBase>
        </Card>
      </div>
    )
  }
}

DfCard.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withRouter(withStyles(styles)(DfCard));

