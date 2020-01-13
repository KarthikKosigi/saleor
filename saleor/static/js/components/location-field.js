import React from 'react';

import {AsyncTypeahead} from 'react-bootstrap-typeahead';
import Button from '@material-ui/core/Button';
import PropTypes from 'prop-types';
import LocationOnIcon from '@material-ui/icons/LocationOn';
import ListItemText from '@material-ui/core/ListItemText';
import ListItem from '@material-ui/core/ListItem';
import location from '../stores/location';

const LocationMenuItem = ({item}) => (
  <ListItem style={{'white-space': 'normal', padding: 0}}>
    <LocationOnIcon/>
    <ListItemText primary={item.structured_formatting.main_text} secondary={item.structured_formatting.secondary_text} />
  </ListItem>
);

LocationMenuItem.propTypes = {
  item: PropTypes.shape({
  })
};

class LocationField extends React.Component {
  timeout;
  state = {
    allowNew: false,
    isLoading: false,
    multiple: false,
    options: []
  };

  static defaultProps = {
    acceptUserLocation: false
  }

  render() {
    const {acceptUserLocation} = this.props;
    return (
      <React.Fragment>
        <AsyncTypeahead
          {...this.state}
          labelKey="description"
          minLength={3}
          onChange = {this._handleChange}
          onSearch={this._handleSearch}
          placeholder="Enter your delivery address"
          renderMenuItemChildren={(option, props) => (
            <LocationMenuItem key={option.id} item={option} style={{padding: 0}}/>
          )}/>
        { acceptUserLocation &&
        <Button
          color="primary"
          variant="contained"
          style={{marginTop: 10}} onClick={this.getLocation.bind(this)}>
          Get Location
        </Button>
        }
      </React.Fragment>
    );
  }

  _handleChange = (e) => {
    if (e && e.length && this.props.onChange) {
      this.props.onChange(e[0]);
    }
  }

  getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(this.getLocationDetails.bind(this));
    } else {
      alert('Geolocation is not supported by this browser.');
    }
  }

  getLocationDetails(position) {
    const {latitude, longitude} = position.coords;
    const SEARCH_URI = '/reverse-geocode';

    fetch(`${SEARCH_URI}?latlng=` + latitude + ',' + longitude,
      {
        method: 'GET'
      })
      .then((resp) => resp.json())
      .then(({results}) => {
        if (results && results.length) {
          let locationObj = results[0];
          $.cookie('location', locationObj.place_id, { path: '/' });
          localStorage.setItem(locationObj.place_id, JSON.stringify(locationObj));
          location.setLocation(locationObj.place_id);
          document.location.reload();
        }
      }).catch(() => {
      });
  }

  getLocations = (query) => {
    this.setState({isLoading: true});
    const SEARCH_URI = '/locations';

    fetch(`${SEARCH_URI}?q=${query}+&types=`, {
      method: 'GET'
    }).then((resp) => resp.json())
      .then(({results}) => {
        this.setState({
          isLoading: false,
          options: results
        });
      }).catch(() => {
      });
  }

  _handleSearch = (query) => {
    clearTimeout(this.timeout);

    // Make a new timeout set to go off in 800ms
    this.timeout = setTimeout(function () {
      this.getLocations(query);
    }.bind(this), 1000);
  }
}

LocationField.propTypes = {
  onChange: PropTypes.func
};

export default LocationField;
