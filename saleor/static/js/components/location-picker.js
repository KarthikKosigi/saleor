import React from 'react';
import ReactDOM from 'react-dom';
import LocationField from './location-field';
import locationStore from '../stores/location';

export default $(document).ready((e) => {
  const locationPicker = document.getElementById('location-picker');

  function handleChange(locationObj) {
    if (locationObj) {
      $.cookie('location', locationObj.place_id, { path: '/' });
      localStorage.setItem(locationObj.place_id, JSON.stringify(locationObj));
      locationStore.setLocation(locationObj.place_id);
      document.location.reload();
    }
  }

  if (locationPicker) {
    ReactDOM.render(
      <LocationField onChange={handleChange} acceptUserLocation={true}></LocationField>, locationPicker
    );
  }
});
