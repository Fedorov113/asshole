import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';

import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';

import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Grid from '@material-ui/core/Grid';
import {Link} from 'react-router-dom'
import Button from '@material-ui/core/Button';


const styles = theme => ({
  grid: {
    flexGrow: 1,
  },
  root: {
    width: '100%',
  },
  panel: {
    width: 510
  },
  heading: {
    fontSize: theme.typography.pxToRem(15),
    flexBasis: '33.33%',
    flexShrink: 0,
  },
  secondaryHeading: {
    fontSize: theme.typography.pxToRem(15),
    color: theme.palette.text.secondary,
  },
});

class ControlledExpansionPanels extends React.Component {
  state = {
    expanded: null,
  };

  handleChange = panel => (event, expanded) => {
    this.setState({
      expanded: expanded ? panel : false,
    });
  };

  render() {
    const {classes} = this.props;
    const {expanded} = this.state;

    return (
      <div className={classes.root}>
        <Grid container className={classes.grid} spacing={16}>
          <Grid container className={classes.demo} spacing={24}>
            {this.props.samples.map(sample => (
              <Grid key={sample} item>
                <ExpansionPanel onChange={this.handleChange({sample})} className={classes.panel}>
                  <ExpansionPanelSummary expandIcon={<ExpandMoreIcon/>}>
                    <Typography className={classes.heading}>
                      {sample}
                    </Typography>
                    <Typography className={classes.secondaryHeading}>
                      I am a sample panel. Open me.
                    </Typography>
                  </ExpansionPanelSummary>
                  <ExpansionPanelDetails>
                    <Typography>
                      Info about sample:
                    </Typography>
                    <Button component={Link} to="/app/dataset/1/sample/TFM_002_F1-2_S4/mp2">
                      Metaphlan2 results
                    </Button>
                  </ExpansionPanelDetails>
                </ExpansionPanel>
              </Grid>

            ))}
          </Grid>
        </Grid>

      </div>
    );
  }
}

ControlledExpansionPanels.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ControlledExpansionPanels);