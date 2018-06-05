import React from 'react'
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/List';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import {withStyles} from '@material-ui/core/styles';
import ControlledExpansionPanels from '../sample/SamplesExpandableList'
import Button from '@material-ui/core/Button';
import {withRouter} from 'react-router-dom';
import SamplesByDirTabs from '../sample/SampleByDirTabs'
import PersonCardsGrid from '../subject/PersonCardsGrid'

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
  }
});


class DatasetFullInfo extends React.Component {
  constructor() {
    super();
    this.state = {
      df: '',
      samples: [],
      loaded: false,
      placeholder: "Loading...",
    };
  }

  componentDidMount() {
    // Get list of samples
    fetch("/api/fs/sample")
      .then(response => {
        if (response.status !== 200) {
          return this.setState({placeholder: "Something went wrong"});
        }
        return response.json();
      })
      .then(data => this.setState({samples: data.sample_name, loaded: true}));

    // Get dataset info
    var df_id = this.props.match.params.df_id;

    fetch("/api/molot/dataset/" + df_id)
      .then(response => {
        if (response.status !== 200) {
          return this.setState({placeholder: "Something went wrong"});
        }
        return response.json();
      })
      .then(data => this.setState({df: data, loaded: true}));
  }

  render() {
    const {classes} = this.props;
    if (this.state.loaded) {
      console.log(this.state.samples);
      return <div>
        <Typography variant="display3" gutterBottom>
          Study {'FHM'}
        </Typography>
        <div className={classes.content}>

          <PersonCardsGrid/>

          <Typography variant="display2" gutterBottom>
            Samples
          </Typography>
          <Button variant="raised"
                  color="primary"
                  className={classes.button}
                  onClick={event => {
                    const loc = this.state.df.pk + '/add_sample';
                    this.props.history.push({
                      pathname: loc,
                      state: {df_pk: this.state.df.pk}
                    });
                  }}>
            Add new sample
          </Button>

          <ControlledExpansionPanels samples={this.state.samples}/>
        </div>
      </div>
    }
    else {
      return this.state.placeholder
    }

  }
}

DatasetFullInfo.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withRouter(withStyles(styles)(DatasetFullInfo));

