import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Link} from 'react-router-dom'

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

const drawerWidth = 240;

const styles = theme => ({
  root: {
    flexGrow: 1,
    zIndex: 1,
    overflow: 'hidden',
    position: 'relative',
    display: 'flex',
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
  },
  drawerPaper: {
    position: 'relative',
    width: drawerWidth,
  },
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    minWidth: 0, // So the Typography noWrap works
    padding: 24
  },
  toolbar: theme.mixins.toolbar,
});

function ClippedDrawer(props) {

  const {classes} = props;

  return (
    <div className={classes.root}>
      <AppBar position="absolute" className={classes.appBar}>
        <Toolbar>
          <Typography variant="title" color="inherit" noWrap>
            ASSHOLE
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        classes={{
          paper: classes.drawerPaper,
        }}>
        <div className={classes.toolbar}/>
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
        </List>
      </Drawer>

      <main className={classes.content}>
        <div className={classes.toolbar}/>
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

          </Switch>
        </BrowserRouter>
      </main>

    </div>
  );
}

ClippedDrawer.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ClippedDrawer);
