import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Link} from 'react-router-dom'
import classNames from 'classnames';

import {withStyles} from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import Checkbox from '@material-ui/core/Checkbox';
import IconButton from '@material-ui/core/IconButton';
import CommentIcon from '@material-ui/icons/Comment';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';

import {render} from 'react-dom'
import {BrowserRouter, Route, Redirect, Switch} from 'react-router-dom'
import AddSampleForm from './data/sample/AddSampleForm'

import DatasetCardsGrid from "./data/dataset/DatasetCardsGrid"
import DatasetFullInfo from './data/dataset/DatsetFullInfo'
import AddSubjectForm from './data/subject/AddSubjectForm'
import Mp2Plot from "./result/metaphlan2";
import PersonFullInfo from "./data/subject/PersonFullInfo"
import SampleFullInfo from './data/sample/SampleFullInfo'
import ReferenceExplorer from './action/reference_explorer'
import Mapping from './action/mapping'
import MappingRuleGenerator from './action/MappingRuleGenerator'
import SamplesTableView from './data/sample/SamplesTableView'
import Mp2Boxplot from "./result/Mp2Boxplot";


const drawerWidth = 240;

const styles = theme => ({
  root: {
    flexGrow: 1,
    zIndex: 1,
    overflow: 'hidden',
    position: 'relative',
    display: 'flex',
  },
  appFrame: {
    height: '100%',
    zIndex: 1,
    overflow: 'hidden',
    position: 'relative',
    display: 'flex',
    width: '100%',
  },
  appBar: {
    position: 'absolute',
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  'appBarShift-left': {
    marginLeft: drawerWidth,
  },
  'appBarShift-right': {
    marginRight: drawerWidth,
  },
  menuButton: {
    marginLeft: 12,
    marginRight: 20,
  },
  hide: {
    display: 'none',
  },
  drawerPaper: {
    position: 'relative',
    width: drawerWidth,
  },
  drawerHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.unit * 3,
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  'content-left': {
    marginLeft: -drawerWidth,
  },
  'content-right': {
    marginRight: -drawerWidth,
  },
  contentShift: {
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  'contentShift-left': {
    marginLeft: 0,
  },
  'contentShift-right': {
    marginRight: 0,
  },
  toolbar: theme.mixins.toolbar,
});

class ClippedDrawer extends React.Component {
  state = {
    open: false,
    anchor: 'left',
  };

  handleDrawerOpen = () => {
    this.setState({open: true});
  };

  handleDrawerClose = () => {
    this.setState({open: false});
  };

  render() {
    const {classes, theme } = this.props;

    const {anchor, open} = this.state;

    const drawer = (
      <Drawer
        variant="persistent"
        anchor={anchor}
        open={open}
        classes={{
          paper: classes.drawerPaper,
        }}
      >
        <div className={classes.drawerHeader}>
          <IconButton onClick={this.handleDrawerClose}>
            {theme.direction === 'rtl' ? <ChevronRightIcon/> : <ChevronLeftIcon/>}
          </IconButton>
        </div>
        <Divider/>
        <List>
          <ListItem button component="a" href="/app/dfs">
            <ListItemText primary="Datasets"/>
          </ListItem>
          <ListItem button component="a" href="/app/ref_seq">
            <ListItemText primary="Reference Sequences"/>
          </ListItem>
          <ListItem button component="a" href="/app/mapping">
            <ListItemText primary="Mapping"/>
          </ListItem>
          <ListItem button component="a" href="/app/mapping_rule">
            <ListItemText primary="Mapping Rule Generator"/>
          </ListItem>
          <ListItem button component="a" href="/app/samples_table">
            <ListItemText primary="Reads Samples Table"/>
          </ListItem>
          <ListItem button component="a" href="/app/mp2box">
            <ListItemText primary="Metaphlan2 Box Plots"/>
          </ListItem>
        </List>
      </Drawer>
    );

    let before = null;
    let after = null;

    if (anchor === 'left') {
      before = drawer;
    } else {
      after = drawer;
    }

    return (
      <div className={classes.appFrame}>
        <AppBar
          className={classNames(classes.appBar, {
            [classes.appBarShift]: open,
            [classes[`appBarShift-${anchor}`]]: open,
          })}
        >
          <Toolbar disableGutters={!open}>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              onClick={this.handleDrawerOpen}
              className={classNames(classes.menuButton, open && classes.hide)}
            >
              <MenuIcon/>
            </IconButton>
            <Typography variant="title" color="inherit" noWrap>
              ASSHOLE
            </Typography>
          </Toolbar>
        </AppBar>

        {before}


        <main className={classNames(classes.content, classes[`content-${anchor}`], {
              [classes.contentShift]: open,
              [classes[`contentShift-${anchor}`]]: open,
            })}>
          <div className={classes.drawerHeader}/>
          <BrowserRouter>
            <Switch>
              <Route exact path='/app/dfs' component={DatasetCardsGrid}/>
              <Route exact path='/app/dataset/:df_id' component={DatasetFullInfo}/>
              <Route exact path='/app/dataset/:df_id/add_subject' component={AddSubjectForm}/>
              <Route exact path='/app/dataset/:df_id/add_sample/' component={AddSampleForm}/>
              <Route exact path='/app/dataset/:df_id/sample/TFM_002_F1-2_S4/mp2' component={Mp2Plot}/>
              <Route exact path='/app/dataset/:df_id/person/:person_id' component={PersonFullInfo}/>
              <Route exact path='/app/dataset/:df_id/person/:person_id/sample/:sample_id' component={SampleFullInfo}/>

              <Route exact path='/app/ref_seq' component={ReferenceExplorer}/>
              <Route exact path='/app/mapping' component={Mapping}/>
              <Route exact path='/app/mapping_rule' component={MappingRuleGenerator}/>

              <Route exact path='/app/samples_table' component={SamplesTableView}/>
              <Route exact path='/app/mp2box' component={Mp2Boxplot}/>

            </Switch>
          </BrowserRouter>
        </main>
        {after}

      </div>
    );
  }
}

ClippedDrawer.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(ClippedDrawer);
