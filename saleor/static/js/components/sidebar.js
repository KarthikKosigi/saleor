import React from 'react';
import Drawer from '@material-ui/core/Drawer';
import Button from '@material-ui/core/Button';
import LocationField from './location-field';
import ReactDOM from 'react-dom';
import { Observer } from 'mobx-react';
import location from '../stores/location';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ImageIcon from '@material-ui/icons/AccessTime';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

function TemporaryDrawer(props) {
  const [state, setState] = React.useState({
    top: false,
    left: false,
    bottom: false,
    right: false
  });

  React.useEffect(() => {
    loadStores();
  }, [props.location]);

  const toggleDrawer = (side, open) => event => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }

    setState({ ...state, [side]: open });
  };

  const sideList = side => (
    <div
      role="presentation" style={{padding: '20px'}}>
      <LocationField onChange={loadStores} acceptUserLocation={true} ></LocationField>
    </div>
  );

  function itemClick(event, key) {
    $.cookie('location', key, { expires: 10 });
    location.setLocation(key);
    document.location.reload();
  }

  function getRecentSearches() {
    var items = [];
    for (let [key, value] of Object.entries(localStorage)) {
      const obj = JSON.parse(value);
      items.push(
        <ListItem
          button
          onClick={ event => itemClick(event, obj.place_id)}>
          <ImageIcon />
          {obj.formatted_address && <ListItemText primary={obj.formatted_address}></ListItemText>}
          {obj.structured_formatting &&
          <ListItemText primary={obj.structured_formatting.main_text} secondary={obj.structured_formatting.secondary_text}/>}
        </ListItem>);
    }

    return (
      <React.Fragment>
        <List>
          <ListItem>
              Recent Searches
          </ListItem>
          {items}
        </List>
      </React.Fragment>
    );
  }

  function loadStores(locationObj) {
    if (locationObj) {
      $.cookie('location', locationObj.place_id, { expires: 10 });
      localStorage.setItem(locationObj.place_id, JSON.stringify(locationObj));
      location.setLocation(locationObj.place_id);
      document.location.reload();
      return;
    }

    const SEARCH_URI = '/reverse-geocode';

    fetch(`${SEARCH_URI}?latlng=` + location.location,
      {
        method: 'GET'
      })
      .then((resp) => resp.json())
      .then(({results}) => {
        let locationObj = results[0].geometry.location;
        let latlng = locationObj.lat + ',' + locationObj.lng;
        location.setLatlng(latlng);
        let search = window.location.search;
        let params = new URLSearchParams(search);
        let query = params.get('q') || '';
        $('#stores-container').load('/stores/near-by/?q=' + query + '&latlng=' + latlng);
      }).catch(() => {
      });
  }

  return (
    <div>
      <Button onClick={toggleDrawer('left', true)} >
        <Observer>{() => <div>{props.location.name} <ExpandMoreIcon/></div>}</Observer>
      </Button>
      <Drawer open={state.left} onClose={toggleDrawer('left', false)} style={{width: '30%'}}>
        {sideList('left')}
        {getRecentSearches()}
      </Drawer>
    </div>
  );
}

export default $(document).ready((e) => {
  const locationPicker = document.getElementById('sidebar-picker');

  if (locationPicker) {
    ReactDOM.render(
      <TemporaryDrawer location={location}></TemporaryDrawer>, locationPicker
    );
  }
});
