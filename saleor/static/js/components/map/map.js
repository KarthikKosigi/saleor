import ReactDOM from 'react-dom';

import React, { Component, Fragment } from 'react';

// // components:
// import Marker from './components/Marker';
// import LocationField from '../location-field';

// // examples:
// import GoogleMap from './components/GoogleMap';
// import SearchBox from './components/SearchBox';

// class Searchbox extends Component {
//   constructor(props) {
//     super(props);

//     this.state = {
//       mapApiLoaded: false,
//       mapInstance: null,
//       mapApi: null,
//       place: null
//     };
//   }

//   apiHasLoaded = (map, maps) => {
//     this.setState({
//       mapApiLoaded: true,
//       mapInstance: map,
//       mapApi: maps
//     });
//   };

//   addPlace = (place) => {
//     console.log(place);
//     const SEARCH_URI = '/reverse-geocode';

//     fetch(`${SEARCH_URI}?latlng=${place.place_id}`, {
//       method: 'GET'
//     }).then((resp) => resp.json())
//       .then(({results}) => {
//         this.setState({
//           isLoading: false,
//           place: results[0]
//         });
//       }).catch(() => {
//       });
//     // this.setState({ place: });
//   };

//   render() {
//     const {
//       place, mapApiLoaded, mapInstance, mapApi
//     } = this.state;
//     return (
//       <div style={{ height: '400px', width: '100%' }}>
//         {mapApiLoaded && <LocationField onChange={this.addPlace}></LocationField>}

//         <GoogleMap
//           defaultZoom={10}
//           defaultCenter={[34.0522, -118.2437]}
//           bootstrapURLKeys={{
//             key: 'AIzaSyCGcoq-CY4qexj4XULpxwbOSCE0ZAGPUCs',
//             libraries: ['places', 'geometry']
//           }}
//           yesIWantToUseGoogleMapApiInternals
//           onGoogleApiLoaded={({ map, maps }) => this.apiHasLoaded(map, maps)}
//         >
//           {place &&
//              <Marker
//                key={place.place_id}
//                text={place.formatted_address}
//                lat={place.geometry.location.lat}
//                lng={place.geometry.location.lng}
//              />}
//         </GoogleMap>
//       </div>
//     );
//   }
// }

import { compose, withProps } from 'recompose';
import { withScriptjs, withGoogleMap, GoogleMap, Marker } from 'react-google-maps';
// import { Location } from 'vscode-languageserver';
import LocationField from '../location-field';

const MyMapComponent = compose(
  withProps({
    googleMapURL: 'https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=AIzaSyAOo7Ul3fCYsFTLe1DEZ7EHVWRC8HgsQYk',
    loadingElement: <div style={{ height: `100%` }} />,
    containerElement: <div style={{ height: `580px`, paddingTop: '20px' }} />,
    mapElement: <div style={{ height: `100%` }} />
  }),
  withScriptjs,
  withGoogleMap)((props) =>
  <GoogleMap
    zoom={25}
    center={{ lat: props.location.lat, lng: props.location.lng }}>
    {props.isMarkerShown && <Marker position={{ lat: props.location.lat, lng: props.location.lng }} onClick={props.onMarkerClick} />}
  </GoogleMap>
);

class MyFancyComponent extends React.PureComponent {
  state = {
    isMarkerShown: false,
    place: {geometry: {location: { lat: -17.397, lng: 74.644 }}}
  }

  componentDidMount() {
    this.delayedShowMarker();
    const { placeId } = this.props;
    if (placeId) {
      this.getLatLng(placeId);
    }
  }

  delayedShowMarker = () => {
    setTimeout(() => {
      this.setState({ isMarkerShown: true });
    }, 3000);
  }

  handleMarkerClick = () => {
    this.setState({ isMarkerShown: false });
    this.delayedShowMarker();
  }

  handleChange = (place) => {
    document.getElementById('id_place_id').value = place.place_id;
    document.getElementById('id_address').value = place.description;
    this.getLatLng(place.place_id);
  }

  getLatLng = (placeId) => {
    const SEARCH_URI = '/reverse-geocode';
    fetch(`${SEARCH_URI}?latlng=${placeId}`, {
      method: 'GET'
    }).then((resp) => resp.json())
      .then(({results}) => {
        this.setState({
          isLoading: false,
          place: results[0]
        });
      }).catch(() => {
      });
  }

  render() {
    return (
      <Fragment>
        <LocationField onChange={this.handleChange}></LocationField>
        <br/>
        <MyMapComponent
          isMarkerShown={this.state.isMarkerShown}
          location = {this.state.place.geometry.location}
          onMarkerClick={this.handleMarkerClick}
        />
      </Fragment>
    );
  }
}

export default $(document).ready((e) => {
  const locationPicker = document.getElementById('store-map');

  if (locationPicker) {
    const placeId = locationPicker.getAttribute('data-place-id');
    ReactDOM.render(
      <MyFancyComponent placeId={placeId}></MyFancyComponent>
      ,
      locationPicker
    );
  }
});
