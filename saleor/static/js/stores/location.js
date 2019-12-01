import { extendObservable } from 'mobx';

class LocationStore {
  constructor() {
    extendObservable(this, {
      location: $.cookie('location'),
      latlng: null,
      stores: [],
      get name() {
        let obj = JSON.parse(localStorage.getItem(this.location));
        return this.location ? obj.description || obj.formatted_address : 'Enter a location';
      }
    });
  }

  addStores(stores) {
    this.stores = stores;
  }

  setLocation(location) {
    this.location = location || null;
  }

  setLatlng(latlng) {
    this.latlng = latlng || null;
  }
}

const location = new LocationStore();

export default location;
